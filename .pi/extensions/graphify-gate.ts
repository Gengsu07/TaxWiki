import { isToolCallEventType, type ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { existsSync } from "node:fs";
import { join } from "node:path";

/**
 * Graphify gate extension
 *
 * Reminds the model about the knowledge graph when running bash commands,
 * but only once per session and only if a graph.json exists.
 *
 * Ported from the original OpenCode plugin (.opencode/plugins/graphify.js).
 */
export default function (pi: ExtensionAPI) {
  let reminded = false;

  pi.on("tool_call", async (event, ctx) => {
    if (reminded) return;
    if (!isToolCallEventType("bash", event)) return;

    const graphPath = join(ctx.cwd, "graphify-out", "graph.json");
    if (!existsSync(graphPath)) return;

    const reminder =
      'echo "[graphify] Knowledge graph available. Read graphify-out/GRAPH_REPORT.md for god nodes and architecture context before searching files."';

    event.input.command = `${reminder} && ${event.input.command}`;
    reminded = true;
  });
}
