#!/usr/bin/env node
// One-off helper: build the TaxWiki knowledge base and export a portable
// JSONL snapshot. Equivalent to running inside a fresh pi session:
//   knowledge_add raw/ "Indonesian Tax Wiki"
//   knowledge_export "Indonesian Tax Wiki" dataset/embeddings/indonesian-tax-wiki.jsonl
// NOTE: exports MUST NOT be written under wiki/ — pi-knowledge indexes the
// whole wiki dir, so a snapshot inside wiki/ gets re-indexed into the
// "TaxWiki Wiki Pages" KB (feedback loop that tripled token usage).
// dataset/ is outside that KB's scope.
import { resolve, dirname } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const repo = resolve(dirname(fileURLToPath(import.meta.url)), "..");
process.env.PI_KNOWLEDGE_DIR = resolve(repo, ".knowledge");

const { KnowledgeEngine } = await import(
  pathToFileURL(resolve(repo, ".pi/npm/node_modules/pi-knowledge/dist/src/engine.js")).href
);

const KB = "Indonesian Tax Wiki";
const engine = new KnowledgeEngine();
await engine.initialize(process.env.PI_KNOWLEDGE_DIR);

const existing = engine.list().find((k) => k.name === KB);
if (existing) {
  console.log(`[update] "${KB}" exists — incremental update`);
  const r = await engine.update(existing.id, (m) => console.log(`  ${m}`));
  console.log(`  added=${r.added} removed=${r.removed} unchanged=${r.unchanged}`);
} else {
  console.log(`[add] ${KB}`);
  const r = await engine.add(
    resolve(repo, "raw"),
    KB,
    (m) => console.log(`  ${m}`),
  );
  console.log(`  chunks=${r.chunkCount}`);
}

const out = resolve(repo, "dataset/embeddings/indonesian-tax-wiki.jsonl");
const count = await engine.exportKB(KB, out, undefined, (m) => console.log(`  ${m}`));
console.log(`[export] ${count} chunks -> ${out}`);

await engine.dispose();
console.log("[done]");
