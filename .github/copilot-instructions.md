# GitHub Copilot CLI - project guidance

This file is Copilot-CLI-specific guidance for this repository. It does not
duplicate project conventions — `CLAUDE.md` (tech stack, commands, coding
standards, agent rules) is the source of truth and is loaded automatically by
Copilot CLI as well. Read `CLAUDE.md` first.

## Why this file exists

Copilot CLI auto-loads both `CLAUDE.md` and the root `AGENTS.md`. The root
`AGENTS.md` is explicitly scoped as "Codex project guidance" (`.codex/` and
`.agents/` are the Codex-specific layer, agents defined as `.toml`, skills
invoked with `$skill-name`). Those specifics do not apply to Copilot CLI:

- Do not use `.codex/agents/*.toml` — they are Codex's agent definitions.
  Copilot CLI's custom agents live in `.github/agents/*.md` (a synced copy of
  `.claude/agents/*.md`) and are invoked through the `task` tool with
  `agent_type` set to `backend-developer`, `frontend-developer`,
  `fullstack-architect`, `product-manager-analyst`, `qa-tester`,
  `web-styles-designer`, or `workshop-mentor`.
- Ignore the `$skill-name` invocation syntax from `AGENTS.md`; Copilot CLI
  discovers skills automatically and you load one via the `skill` tool using
  its plain name (e.g. `api-patterns`, `testing-patterns`).
- Everything else in `AGENTS.md` (project description, repository commands,
  working agreements, backend/frontend conventions, completion criteria) is
  accurate and applies to Copilot CLI too.

## File ownership

- Never edit `CLAUDE.md`, `.claude/`, `AGENTS.md`, `.codex/`, or `.agents/` —
  those belong to Claude Code and Codex respectively.
- This file and `.github/agents/*.md` are the only files that are Copilot
  CLI's own; keep changes to those scoped here.

## Skills

Skills are auto-discovered from `.claude/skills/*/SKILL.md` (a valid location
for Copilot CLI) and are also mirrored under `.agents/skills/` and
`.github/skills/` (OpenSpec ones only) with equivalent content — use whichever
copy the `skill` tool lists; content is identical.

The five legacy Claude Code slash commands have no Copilot slash-command
equivalent. Use their skill equivalents instead:

| Claude Code command | Copilot CLI skill |
|---|---|
| `/generar` | `generar-codigo` |
| `/crear-modulo-crud` | `crear-modulo-crud` |
| `/test` | `test-runner` |
| `/servicios` | `gestion-servicios` |
| `/generate-mr-description` | `generate-mr-description` |

OpenSpec `/opsx` slash commands (Claude Code) and `.github/prompts/opsx-*.prompt.md`
(Codex/VS Code prompt files) are not executed by Copilot CLI as commands.
Use the equivalent skills instead: `openspec-explore`, `openspec-propose`,
`openspec-apply-change`, `openspec-archive-change`.

## Agent pipeline

Follow the same sequential pipeline as Claude Code and Codex — each stage
depends on the previous one's output, so never run steps in parallel:

```
product-manager-analyst -> fullstack-architect -> backend-developer
  -> qa-tester (backend) -> frontend-developer -> qa-tester (frontend/integration)
```

For small, well-scoped tasks, use only the relevant agent or work directly
instead of forcing the full pipeline.
