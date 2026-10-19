# Taste

## Environment & Tooling
- Works on Windows (projects under `F:\PROJECTS\...`); the bare `cmd` command resolves to cmd.exe, so use the `cmdc` binary to invoke Command Code CLI. Confidence: 0.85
- Keeps agent skills in a pi/OpenCode-style flat layout (`.agents/<skill-name>/SKILL.md`) rather than the default `.agents/skills/`; makes them discoverable by adding `"skills": ["./.agents"]` to `.commandcode/settings.json` instead of moving the files. Confidence: 0.75
