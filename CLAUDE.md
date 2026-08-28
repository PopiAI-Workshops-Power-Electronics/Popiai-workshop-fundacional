# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Repositorio `Popiai-workshop-fundacional` (org `PopiAI-Workshops-Power-Electronics`): monorepo base del Workshop Fundacional "Desarrollo con AI Agents y Claude Code" de PopiAI Software Services.
Contiene un backend NestJS y un frontend Next.js conectados a MongoDB.
Los asistentes implementarán features usando Claude Code como agente de desarrollo.

## Tech Stack

- **Monorepo**: npm workspaces (Node v20 LTS — see `.nvmrc`)
- **Backend** (`apps/backend`): NestJS 11, TypeScript 5.7, Mongoose 8, class-validator, class-transformer
- **Frontend** (`apps/frontend`): Next.js 15, React 19, Tailwind CSS 4, TypeScript
- **Database**: MongoDB 7 (local via Docker)
- **Tests**: Jest (backend), Playwright (frontend E2E)
- **Auth**: Firebase Auth (planned, not yet implemented) — see `auth-flow` skill

## Quick Reference

| Service | Port | URL |
|---------|------|-----|
| Backend (NestJS) | 3001 | http://localhost:3001/api |
| Frontend (Next.js) | 3000 | http://localhost:3000 |
| MongoDB | 27017 | mongodb://localhost:27017/workshop |

## Commands

```bash
# Install dependencies
npm install

# Development
npm run start:backend         # NestJS on port 3001 (hot reload)
npm run start:frontend        # Next.js on port 3000 (hot reload)

# Or from each app directory
cd apps/backend && npm run start:dev
cd apps/frontend && npm run dev

# Build
npm run build:frontend        # Next.js production build
cd apps/backend && npm run build   # NestJS build (nest build)

# Tests
npm run test:backend          # Backend unit tests
cd apps/backend && npm run test:cov   # Coverage

# Frontend E2E
cd apps/frontend && npm run e2e

# Docker (local MongoDB)
docker-compose up -d          # Start MongoDB
docker-compose down           # Stop MongoDB

# Verify setup
npm run verify                # or ./scripts/verify.sh
```

## Slash Commands

### Development
| Command | Description |
|---------|-------------|
| `/generar [tipo] [nombre]` | Generate code (componente, hook, service, dto, schema, controller, api, types) |
| `/crear-modulo-crud [nombre]` | Create complete CRUD module (backend + frontend) |
| `/test [action]` | Run/generate/fix tests (run, generate, coverage, fix, watch) |
| `/servicios [action]` | Manage services (start, stop, restart, status, logs) |

### Git & PR
| Command | Description |
|---------|-------------|
| `/generate-mr-description` | Generate PR description comparing current branch vs main |

### OpenSpec Workflow
| Command | Description |
|---------|-------------|
| `/opsx explore` | Think through ideas and problems |
| `/opsx propose` | Create a change and generate all its artifacts |
| `/opsx apply` | Implement tasks of a change |
| `/opsx archive` | Archive completed changes and sync main specs |

## Agents & Skills

> **Compatibilidad dual (Claude Code + GitHub Copilot CLI):** este proyecto soporta ambas CLIs.
> - Los 7 agentes viven en `.claude/agents/*.md` (leidos por Claude Code) con una copia
>   sincronizada en `.github/agents/*.md` (unica ubicacion que lee Copilot CLI). Si editas un
>   agente, actualiza ambas copias — el campo `model` usa alias de Claude (`sonnet/opus/haiku`)
>   en `.claude/agents/` y IDs de Copilot (`claude-sonnet-4.5`, etc.) en `.github/agents/`.
> - Las skills en `.claude/skills/` ya son leidas por ambas CLIs sin necesidad de duplicarlas.
> - Los comandos slash de Claude Code (`.claude/commands/`) no tienen equivalente nativo en
>   Copilot CLI; los 5 comandos sin skill propia (`generar`, `crear-modulo-crud`, `test`,
>   `servicios`, `generate-mr-description`) tienen su version como skill en `.claude/skills/`
>   para que Copilot pueda invocarlos igual.
> - El workflow OpenSpec (`/opsx *`) se gestiona con el CLI `openspec` (`openspec init`/`update`),
>   que genera y mantiene por si mismo los artefactos de cada herramienta: comandos en
>   `.claude/commands/opsx/` + skills `openspec-*` en `.claude/skills/` para Claude Code, y
>   prompts `.github/prompts/opsx-*.prompt.md` + skills `openspec-*` en `.github/skills/` para
>   Copilot CLI. No edites estos archivos a mano — usa `openspec update` tras cambiar el
>   perfil/workflows en `openspec/config.yaml` o la config global (`openspec config profile`).
>   Nota: los `.prompt.md` de `.github/prompts/` los genera OpenSpec para su target
>   "github-copilot" (formato de prompts reutilizables de VS Code Copilot Chat); esta CLI
>   (Copilot CLI) no los ejecuta como comandos — solo lee `.github/skills/` y `.claude/skills/`
>   como skills. Por eso los 5 comandos legacy sin equivalente OpenSpec (`generar`,
>   `crear-modulo-crud`, `test`, `servicios`, `generate-mr-description`) solo tienen skill,
>   sin `.prompt.md`.

### Developer Agents

Agents are invoked within the OpenSpec workflow or directly for specific tasks.

| Agent | Model | Role |
|-------|-------|------|
| `product-manager-analyst` | Opus | Transforms tickets into detailed functional specs |
| `fullstack-architect` | Opus | Designs unified backend + frontend architecture |
| `backend-developer` | Sonnet | Implements NestJS backend code |
| `frontend-developer` | Sonnet | Implements Next.js frontend code |
| `qa-tester` | Sonnet | Tests backend (Jest/e2e) and frontend (Testing Library/browser) |
| `web-styles-designer` | Opus | CSS/styling expert for Tailwind and responsive design |
| `workshop-mentor` | Haiku | Guides students on agent workflow methodology (does NOT write code) |

### Pipeline (via OpenSpec)

```
/opsx propose → PM Analyst (spec) → Fullstack Architect (architecture)
/opsx apply   → Backend Developer → QA Tester (backend)
/opsx apply   → Frontend Developer → QA Tester (frontend)
/opsx archive → Final verification and spec sync
```

**Rules:**
- Each step MUST complete before the next starts
- Only `product-manager-analyst` can create branches (with user permission)
- No agent pushes or creates PRs without explicit user approval
- One branch per feature (backend + frontend together)

### Skills (auto-activated)

| Skill | Purpose |
|-------|---------|
| `brand-design` | **Primary brand skill** — colors, tokens, component patterns, anti-patterns |
| `design-guidelines` | Full brand reference — palette, typography, landing structure |
| `api-patterns` | NestJS controllers, services, DTOs, guards, DI patterns |
| `mongodb-patterns` | Mongoose schemas, queries, aggregations, indexes |
| `auth-flow` | Firebase Auth guards, user context, roles (planned) |
| `frontend-patterns` | Next.js App Router, pages, components, hooks |
| `api-contract` | Standardized API contract format (architect → developer handoff) |
| `api-client` | Frontend API wrapper, error handling |
| `testing-patterns` | Jest mocks, unit tests, Playwright E2E, what a good test must cover |
| `verification-checklist` | Lint → Build → Test → Browser verification checklists |
| `git-workflow` | Branch naming, conventional commits, PR rules |
| `react-best-practices` | 45 Vercel performance optimization rules for React/Next.js |
| `tailwind-design` | Tailwind v4 layout, responsive, spacing patterns |
| `frontend-design` | Creative UI techniques, design thinking, aesthetics |
| `web-design-guidelines` | Accessibility, UX, and performance audit |
| `generar-codigo` | Equivalent of the `/generar` command, usable by Copilot CLI |
| `crear-modulo-crud` | Equivalent of the `/crear-modulo-crud` command, usable by Copilot CLI |
| `test-runner` | Equivalent of the `/test` command, usable by Copilot CLI |
| `gestion-servicios` | Equivalent of the `/servicios` command, usable by Copilot CLI |
| `generate-mr-description` | Equivalent of the `/generate-mr-description` command, usable by Copilot CLI |

## Architecture

### Monorepo Structure

```
apps/backend/    → API NestJS (port 3001)
apps/frontend/   → App Next.js (port 3000)
specs/           → Feature specifications
docs/            → Workshop documentation (see docs/CONFIGURACION-PROYECTO.md for customization)
docs/specs/      → Feature specifications (generated by PM Analyst)
docs/skills/     → Reference content for skills the attendees create themselves (security-review, code-review, doc-update, production-checklist)
scripts/         → Setup and verification scripts
openspec/        → OpenSpec configuration for spec-driven workflow
.claude/         → Agents, skills and commands (Claude Code); skills/ also read by Copilot CLI
.github/agents/  → Agent copies for GitHub Copilot CLI (kept in sync with .claude/agents/)
.github/prompts/ → OpenSpec /opsx prompts for Copilot CLI (generated by `openspec init/update`)
.github/skills/  → OpenSpec skills for Copilot CLI (generated by `openspec init/update`)
```

### Backend (`apps/backend`)

- NestJS modular architecture with dependency injection via decorators
- Entry point: `src/main.ts` (listens on port 3001)
- Global prefix: `/api`
- CORS enabled for `http://localhost:3000`
- Global ValidationPipe with whitelist and forbidNonWhitelisted
- Currently only root module (`AppModule`) with health check endpoint
- TypeScript with `emitDecoratorMetadata` and `experimentalDecorators`, target ES2023
- Tests: Jest with ts-jest, test files match `*.spec.ts`
- Feature module structure:
  - `src/{feature}/{feature}.module.ts` — NestJS module
  - `src/{feature}/{feature}.controller.ts` — REST endpoints
  - `src/{feature}/{feature}.service.ts` — business logic
  - `src/{feature}/schemas/{model}.schema.ts` — Mongoose schema
  - `src/{feature}/dto/create-{model}.dto.ts` — creation DTO with class-validator
  - `src/{feature}/dto/update-{model}.dto.ts` — update DTO (PartialType)
  - `src/{feature}/{feature}.service.spec.ts` — unit tests

### Frontend (`apps/frontend`)

- Next.js 15 App Router with layouts in `app/layout.tsx`
- Styling: Tailwind CSS 4 with `@theme inline` in `app/globals.css`
- Font: Inter via `next/font/google` (CSS var: `--font-inter`)
- Brand tokens defined in `app/globals.css` (primary: teal, neutrals: slate, light mode only)
- Path alias: `@/*` → `./*`
- Feature structure:
  - `app/{feature}/page.tsx` — page component
  - `app/{feature}/components/` — feature components
  - `app/{feature}/hooks/` — custom hooks
  - `app/{feature}/types.ts` — TypeScript types
- API base URL: `http://localhost:3001/api`
- Fetch via custom hooks, no direct API calls in components
- Four UI states: loading, error, empty, success

### Auth Flow (planned)

```
Request → FirebaseAuthGuard → IsActiveGuard → Controller
            (validates token)   (sets db_user)
```
- Not yet implemented — see `auth-flow` skill and `docs/CONFIGURACION-PROYECTO.md`
- Guards, decorators, and Firebase integration to be added as needed

### Environment Variables

```
# apps/backend/.env
MONGODB_URI=mongodb://localhost:27017/workshop
PORT=3001

# apps/frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:3001/api
```

## Coding Standards

### Git Flow
- Feature branches from `main`: `feature/[kebab-case]`, `fix/[kebab-case]`
- Conventional commits: `feat(backend):`, `feat(frontend):`, `fix(backend):`, `test(backend):`, `docs:`
- PRs target `main`
- One branch per feature (backend + frontend together)
- Never push or create PR without user approval

### Backend (NestJS)
- Modular architecture: one folder per domain under `src/`
- DTOs: class-validator decorators (`@IsNotEmpty()`, `@IsString()`, `@MaxLength()`), PartialType for updates
- Response format: `{ id, ...fields, createdAt, updatedAt }`
- Pagination format: `{ total, items: [...], page, limit }`
- Error handling: NestJS HTTP exceptions — 400 (validation), 404 (not found), 409 (conflict)
- Timestamps: automatic via Mongoose `timestamps: true`
- Register every new module in `app.module.ts`

### Frontend (Next.js)
- App Router pages, Server Components by default
- `'use client'` only when interactivity is needed
- TypeScript strict: interfaces for all props
- State management: React hooks + context
- Mobile-first responsive with Tailwind
- Accessibility: semantic HTML, ARIA labels, keyboard navigation

### Testing (mandatory)
- **Every backend service/controller MUST have a corresponding `*.spec.ts` test file**
- Backend: Jest with Mongoose model mocking
- Coverage target: ≥80%
- Descriptive test names: `should create a category`, `should return 404 when not found`
- Frontend E2E: complete flows (create, list, edit, delete)
- Mock all external dependencies
- Cover: happy path, error states, edge cases

## Agent Rules

1. **Always** read the full spec before generating code
2. **Always** register new modules in `app.module.ts`
3. **Always** include class-validator validation in DTOs
4. **Always** generate unit tests alongside code
5. **Never** modify configuration files without explicit instruction
6. **Never** change backend port (3001) or frontend port (3000)
7. If a test fails, fix it before continuing
8. Timestamps (`createdAt`, `updatedAt`) must be automatic via Mongoose `timestamps: true`
9. **Never** push or create PR without explicit user approval
10. **Never** create a branch without asking the user first
