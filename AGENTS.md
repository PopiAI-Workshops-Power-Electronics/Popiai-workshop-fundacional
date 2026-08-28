# Codex project guidance

## Scope

This file and the `.codex/` and `.agents/` directories are the Codex-specific layer for this repository.

- Do not modify `CLAUDE.md` or anything under `.claude/` unless the user explicitly asks for Claude configuration changes.
- Keep Codex-specific agents in `.codex/agents/` and Codex-discoverable skills in `.agents/skills/`.
- Preserve unrelated user changes and generated artifacts already present in the worktree.

## Project

This is the base monorepo for the PopiAI workshop on development with AI coding agents.

- Package manager: npm workspaces; Node.js 20 or newer.
- Backend: NestJS 11, TypeScript, Mongoose and MongoDB, under `apps/backend/`.
- Frontend: Next.js 15 App Router, React 19 and Tailwind CSS 4, under `apps/frontend/`.
- Backend URL: `http://localhost:3001/api`.
- Frontend URL: `http://localhost:3000`.
- MongoDB URL: `mongodb://localhost:27017/workshop`.
- Authentication with Firebase is planned but is not part of the current source baseline.

## Repository commands

Run commands from the repository root unless a command says otherwise.

```bash
npm install
npm run start:backend
npm run start:frontend
npm run build
npm run build:backend
npm run build:frontend
npm run test:backend
npm run lint:backend
npm run lint:frontend
npm run docker:up
npm run docker:down
npm run verify
```

Useful app-level checks:

```bash
npm run test:cov --workspace=apps/backend
npm run test:e2e --workspace=apps/backend
npm run e2e --workspace=apps/frontend
```

`npm run lint:backend` uses ESLint with `--fix`, so treat it as a mutating command. Do not rely on `npm run verify` as the only completion gate: also run the checks relevant to the files changed and inspect their exit status.

## Working agreements

- Inspect the current implementation before proposing or writing changes; generated `dist/`, `.next/` and `coverage/` output is not source of truth.
- Use TypeScript strictly and follow existing patterns before introducing new abstractions.
- Add no production dependency without explaining why it is needed.
- Do not create branches, commits, pushes or pull requests unless the user explicitly requests them.
- If Git operations are requested, use feature branches named `feature/<kebab-case>` or fixes named `fix/<kebab-case>`, conventional commits, and target `main`.
- Never push or create a pull request without explicit user approval.
- Keep backend and frontend changes for one feature on the same branch.
- Do not expose or commit `.env` or `.env.local` values.

## Codex skills

Repository skills are available from `.agents/skills/` and should be loaded when their descriptions match the task.

- Backend: `api-patterns`, `mongodb-patterns`, `auth-flow`, `api-contract`.
- Frontend: `frontend-patterns`, `api-client`, `brand-design`, `design-guidelines`, `tailwind-design`, `frontend-design`, `vercel-react-best-practices`, `web-design-guidelines`.
- Quality and workflow: `testing-patterns`, `verification-checklist`, `git-workflow`.
- Reusable workshop actions: `generar-codigo`, `crear-modulo-crud`, `test-runner`, `gestion-servicios`, `generate-mr-description`.
- OpenSpec: `openspec-explore`, `openspec-propose`, `openspec-apply-change`, `openspec-archive-change`.

Use `$skill-name` when the user asks to invoke one explicitly. The reusable-action skills are the Codex equivalent of the custom slash commands used by other tools.

## Custom agents and workflow

Project-scoped custom agents live in `.codex/agents/`:

- `product-manager-analyst`: turn a feature idea into a reviewable functional specification.
- `fullstack-architect`: design backend, frontend and the API contract together.
- `backend-developer`: implement NestJS and MongoDB work from an approved design.
- `frontend-developer`: implement Next.js UI and API integration from an approved design and real backend behavior.
- `qa-tester`: create and run backend, frontend or integration tests and report evidence.
- `web-styles-designer`: implement or review visual design and styling.
- `workshop-mentor`: explain the workshop methodology without editing code.

For a full feature workflow, delegate sequentially because every stage depends on the previous output:

```text
product-manager-analyst
  -> fullstack-architect
  -> backend-developer
  -> qa-tester (backend)
  -> frontend-developer
  -> qa-tester (frontend/integration)
```

Wait for each stage to complete and review its output before starting the next. Do not run the backend and frontend implementation agents in parallel. For small, well-scoped tasks, use only the relevant agent or work directly instead of forcing the full pipeline.

## Backend conventions

- Put domain modules under `apps/backend/src/<feature>/`.
- Use NestJS modules, controllers, injectable services and dependency injection.
- Validate request DTOs with `class-validator` and use NestJS HTTP exceptions for expected errors.
- Use Mongoose schemas with timestamps when persistence is required.
- Register every new feature module in `apps/backend/src/app.module.ts`.
- Follow the existing global `/api` prefix and CORS configuration.
- Cover service behavior and meaningful error paths with Jest; add e2e coverage when endpoint behavior changes.

## Frontend conventions

- Use the App Router under `apps/frontend/app/`; the repository does not use an `apps/frontend/src/` directory.
- Prefer Server Components and add `'use client'` only for client-side state, effects or browser APIs.
- Keep props and API payloads typed; use the `@/*` alias for frontend imports.
- API-consuming UI must represent loading, error, empty and success states.
- Use mobile-first layouts, semantic HTML, keyboard-accessible controls and visible focus states.
- Follow `brand-design` before applying the broader frontend or Tailwind design guidance.
- Verify user-facing changes in a browser and inspect console and network errors before calling them complete.

## Completion criteria

- Run focused tests for the behavior changed.
- Run the relevant build and type checks.
- Run lint only with awareness of whether it mutates files.
- For API changes, exercise the endpoint when the required services are available.
- For frontend changes, verify the affected flow in a browser at relevant viewport sizes.
- Report commands run, results, and any check that could not be completed.
