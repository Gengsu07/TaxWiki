#!/usr/bin/env python3
"""
train.py — Unsloth LoRA fine-tune for the TaxWiki agent model.

Run on a GPU box (RunPod / Colab T4+ / Lambda):
    pip install unsloth
    python dataset/train.py --data-dir dataset --model unsloth/Phi-4-mini-instruct

Then export GGUF for CPU inference on the laptop:
    python dataset/train.py --export-gguf

Expected: 1 epoch, 30-60 min on an L4/A10/4090, <$1 on RunPod spot.
Dataset size (hundreds of samples) is the constraint, NOT compute — do not
train longer than ~1-2 epochs or you will overfit the format.

Notes:
- Phi-4-mini (3.8B) is the default: best instruction following per GB, good
  Indonesian, 128K context. Alternatives: unsloth/gemma-3-4b-it,
  unsloth/Qwen2.5-3B-Instruct-bnb-4bit.
- T4 (16GB): fp16 + 4-bit loading works. L4/A10 (24GB): can use bf16.
"""

import argparse
import glob
import json
import os
from pathlib import Path

import torch
from datasets import Dataset
from transformers import TrainingArguments
from trl import SFTTrainer
from unsloth import FastLanguageModel, is_bfloat16_supported
from unsloth.chat_templates import get_chat_template, standardize_sharegpt


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="unsloth/Phi-4-mini-instruct")
    p.add_argument("--data-dir", default="dataset")
    p.add_argument("--max-seq-length", type=int, default=4096)
    p.add_argument("--epochs", type=float, default=1.0)
    p.add_argument("--batch-size", type=int, default=2)
    p.add_argument("--grad-accum", type=int, default=4)
    p.add_argument("--lr", type=float, default=2e-4)
    p.add_argument("--r", type=int, default=16)
    p.add_argument("--output", default="outputs")
    p.add_argument("--export-gguf", action="store_true",
                   help="merge LoRA + export GGUF (needs llama-cpp-python)")
    return p.parse_args()


def load_jsonl_sharegpt(data_dir: str):
    """Load task-*.jsonl and qa-*.jsonl (ShareGPT format) into one list."""
    rows = []
    for pat in ("task-train.jsonl", "qa-train.jsonl"):
        for f in glob.glob(os.path.join(data_dir, pat)):
            with open(f, encoding="utf-8") as fh:
                rows += [json.loads(l) for l in fh if l.strip()]
    if not rows:  # fallback: hand-made examples so the pipeline is testable
        for f in glob.glob(os.path.join(data_dir, "examples", "*.jsonl")):
            with open(f, encoding="utf-8") as fh:
                rows += [json.loads(l) for l in fh if l.strip()]
    print(f"loaded {len(rows)} training conversations")
    return rows


def build_dataset(tokenizer, rows):
    ds = Dataset.from_list(rows)
    ds = standardize_sharegpt(ds)  # {"from","value"} -> {"role","content"}
    def fmt(ex):
        msgs = [{"role": m["role"], "content": m["content"]}
                for m in ex["conversations"]]
        return {"text": tokenizer.apply_chat_template(
            msgs, tokenize=False, add_generation_prompt=False)}
    ds = ds.map(fmt)
    return ds


def main():
    args = parse_args()
    Path(args.output).mkdir(parents=True, exist_ok=True)

    print(f"loading {args.model} ...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=args.model,
        max_seq_length=args.max_seq_length,
        dtype=None,  # auto: bf16 on Ampere+, fp16 on T4
        load_in_4bit=True,
    )

    # Chat template: Phi-4-mini / Gemma3 / Qwen all work with chatml here.
    tokenizer = get_chat_template(
        tokenizer,
        chat_template="chatml",
        mapping={"role": "from", "content": "value",
                 "user": "human", "assistant": "gpt"},
    )

    model = FastLanguageModel.get_peft_model(
        model,
        r=args.r,
        lora_alpha=16,
        lora_dropout=0,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=42,
        use_rslora=False,
        loftq_config=None,
    )

    ds = build_dataset(tokenizer, load_jsonl_sharegpt(args.data_dir))
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=ds,
        dataset_text_field="text",
        max_seq_length=args.max_seq_length,
        dataset_num_proc=1,
        packing=False,
        args=TrainingArguments(
            per_device_train_batch_size=args.batch_size,
            gradient_accumulation_steps=args.grad_accum,
            num_train_epochs=args.epochs,
            warmup_steps=10,
            learning_rate=args.lr,
            fp16=not is_bfloat16_supported(),
            bf16=is_bfloat16_supported(),
            logging_steps=1,
            optim="adamw_8bit",
            weight_decay=0.01,
            lr_scheduler_type="cosine",
            seed=42,
            output_dir=args.output,
            report_to="none",
        ),
    )

    print(f"training {args.epochs} epoch(s), "
          f"steps = {len(ds) * args.epochs // (args.batch_size * args.grad_accum)}")
    trainer.train()

    # Keep only LoRA adapters (small download if you want to iterate later).
    model.save_pretrained(os.path.join(args.output, "lora"))
    tokenizer.save_pretrained(os.path.join(args.output, "lora"))
    print(f"saved LoRA adapters -> {args.output}/lora")

    if args.export_gguf:
        print("merging + exporting GGUF q4_k_m ...")
        model.save_pretrained_merged(
            os.path.join(args.output, "merged"), tokenizer, save_method="merged_16bit")
        model.save_pretrained_gguf(
            os.path.join(args.output, "gguf"), tokenizer,
            quantization_method=["q4_k_m"])
        print(f"saved GGUF -> {args.output}/gguf")


if __name__ == "__main__":
    main()
