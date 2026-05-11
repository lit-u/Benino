## graphify

This folder contains files imported from https://github.com/safishamsi/graphify.

Agent compatibility:
- Codex reads `AGENTS.md`.
- Claude Code reads `CLAUDE.md`.
- Keep both files in sync when changing local agent instructions.

Project graph rules:
- If `graphify-out/GRAPH_REPORT.md` exists, read it before answering architecture or codebase questions.
- If `graphify-out/wiki/index.md` exists, navigate it instead of reading raw files.
- After modifying code files in this folder, run `graphify update .` when available to keep the graph current.
