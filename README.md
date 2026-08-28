# Popiai-workshop-fundacional

Repositorio base del **Workshop Fundacional** (`PopiAI-Workshops-Power-Electronics/Popiai-workshop-fundacional`). Monorepo NestJS + Next.js para el workshop **"Desarrollo con AI Agents y Claude Code"** de PopiAI Software Services.

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Backend | NestJS | 11 |
| Frontend | Next.js | 15 |
| UI | React | 19 |
| Styling | Tailwind CSS | 4 |
| Database | MongoDB | 7 |
| Language | TypeScript | 5.7 |
| AI Tooling | Claude Code | CLI + Agents |

## Requisitos previos

- Node.js v20 LTS (`nvm use`)
- Docker Desktop instalado y corriendo
- npm v10+
- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) (para el sistema de agentes)

### Comprobar los requisitos del workshop

Antes del workshop, ejecuta el script de comprobacion. Verifica que el equipo cumple
los requisitos del documento *Requisitos de sala y setup*: acceso HTTPS a los dominios
necesarios (GitHub, Anthropic, npm, Docker Hub, etc.), software instalado (Git, Node.js 20,
npm, Docker + Docker Compose) y que hay al menos una herramienta de IA disponible
(Claude Code, GitHub Copilot CLI o Codex CLI).

Hay dos versiones equivalentes, elige la que te resulte mas comoda:

```bash
# Con Python 3 (no necesita Node instalado)
python3 scripts/check-requirements.py    # Linux / macOS
python scripts/check-requirements.py     # Windows

# Con Node.js
node scripts/check-requirements.js
# o, si ya tienes las dependencias instaladas:
npm run check-requirements
```

Si algun requisito no se cumple, el script lo indica en el resumen final y termina con
codigo de salida 1.

## Setup rapido

```bash
# 1. Usar la version correcta de Node
nvm use

# 2. Instalar dependencias
npm install

# 3. Levantar MongoDB local
docker compose up -d

# 4. Verificar que todo esta bien
npm run verify                 # Linux / macOS
python scripts/verify.py       # Windows
```

### Setup automatico (alternativa)

Los pasos 2 a 4 tambien se pueden hacer con un unico script, que instala las dependencias,
levanta MongoDB y espera a que responda. Hay dos versiones equivalentes:

```bash
# Con bash (Linux / macOS)
npm run setup                  # o ./scripts/setup.sh
npm run verify                 # o ./scripts/verify.sh

# Con Python 3.8+ (Windows, o cualquier sistema; no necesita bash ni PowerShell)
python scripts/setup.py        # en Linux / macOS: python3 scripts/setup.py
python scripts/verify.py       # en Linux / macOS: python3 scripts/verify.py
```

Ambos scripts se ejecutan desde la raiz del repositorio y terminan con codigo de salida 1
si algo falla.

## Iniciar el proyecto

```bash
# Desde la raiz del monorepo:
npm run start:backend    # NestJS en puerto 3001 (hot reload)
npm run start:frontend   # Next.js en puerto 3000 (hot reload)

# O desde cada app:
cd apps/backend && npm run start:dev
cd apps/frontend && npm run dev
```

## Comandos disponibles

### Desarrollo

| Comando | Descripcion |
|---------|-------------|
| `npm run start:backend` | Inicia backend NestJS (puerto 3001, hot reload) |
| `npm run start:frontend` | Inicia frontend Next.js (puerto 3000, hot reload) |
| `npm run build` | Build de backend + frontend |
| `npm run build:backend` | Build solo del backend |
| `npm run build:frontend` | Build solo del frontend |
| `npm run test:backend` | Tests unitarios del backend |
| `npm run lint:backend` | Lint del backend |
| `npm run lint:frontend` | Lint del frontend |

### Infraestructura

| Comando | Descripcion |
|---------|-------------|
| `npm run docker:up` | Levanta MongoDB con Docker |
| `npm run docker:down` | Detiene MongoDB |
| `npm run setup` | Setup automatico completo (Linux/macOS; en Windows usa `python scripts/setup.py`) |
| `npm run verify` | Verifica que todo esta configurado (Linux/macOS; en Windows usa `python scripts/verify.py`) |
| `npm run check-requirements` | Comprueba los requisitos del workshop (dominios, software, herramienta de IA) |

## URLs

| Servicio | Puerto | URL |
|----------|--------|-----|
| Frontend | 3000 | http://localhost:3000 |
| Backend API | 3001 | http://localhost:3001/api |
| Health check | 3001 | http://localhost:3001/api/health |
| MongoDB | 27017 | mongodb://localhost:27017/workshop |

## Sistema de AI Agents

Este proyecto incluye un sistema completo de agentes AI para desarrollo asistido con Claude Code.

### Pipeline de desarrollo

```
PM Analyst → Fullstack Architect → Backend Developer → QA Tester → Frontend Developer → QA Tester
```

Cada paso debe completarse antes de iniciar el siguiente. Ver `CLAUDE.md` para la documentacion completa de agentes, skills y comandos.

### Slash Commands (Claude Code)

| Comando | Descripcion |
|---------|-------------|
| `/generar [tipo] [nombre]` | Genera codigo (componente, hook, service, dto, schema, etc.) |
| `/crear-modulo-crud [nombre]` | Crea modulo CRUD completo (backend + frontend) |
| `/test [action]` | Ejecuta/genera/corrige tests |
| `/servicios [action]` | Gestiona servicios (start, stop, status) |
| `/generate-mr-description` | Genera descripcion de PR |
| `/opsx propose` | Propone un cambio y genera todos sus artefactos |
| `/opsx explore` | Explora ideas antes de crear un cambio |
| `/opsx apply` | Implementa tareas de un cambio |
| `/opsx archive` | Archiva un cambio completado |

## Estructura del proyecto

```
apps/backend/    → API NestJS (puerto 3001)
apps/frontend/   → App Next.js (puerto 3000)
.claude/         → Agentes, skills y comandos para Claude Code
  agents/        → 7 agentes especializados (fuente; Claude Code los lee de aqui)
  skills/        → 20+ skills auto-activadas (compartidas: tambien las lee Copilot CLI)
  commands/      → Slash commands (especificos de Claude Code)
.github/agents/  → Copia de los 7 agentes para GitHub Copilot CLI (unica ubicacion que Copilot lee)
openspec/        → Configuracion OpenSpec (workflow spec-driven)
specs/           → Specs de features
docs/            → Documentacion y guias
scripts/         → Scripts de setup y verificacion
```

## Documentacion

- **`CLAUDE.md`** — Referencia completa del proyecto para Claude Code y Copilot CLI (agentes, skills, convenciones). Ambas CLIs lo cargan automaticamente.
- **`docs/SETUP.md`** — Guia de setup paso a paso
- **`docs/CONFIGURACION-PROYECTO.md`** — Personalizacion del proyecto (branding, auth, env vars)
- **`docs/TROUBLESHOOTING.md`** — Solucion a problemas comunes

## Compatibilidad con Claude Code y GitHub Copilot CLI

Este repositorio soporta ambas CLIs de AI agents:

| Recurso | Claude Code | Copilot CLI |
|---|---|---|
| Instrucciones del proyecto | `CLAUDE.md` | `CLAUDE.md` (soportado nativamente) |
| Skills | `.claude/skills/*/SKILL.md` | Mismos archivos (`.claude/skills` es una ubicacion valida para Copilot) |
| Agentes | `.claude/agents/*.md` | `.github/agents/*.md` (copia con `model` mapeado a IDs de Copilot) |
| Comandos `/generar`, `/test`, `/servicios`, `/crear-modulo-crud`, `/generate-mr-description` | `.claude/commands/*.md` | Equivalentes disponibles como skills en `.claude/skills/` (Copilot no tiene comandos custom) |

Si agregas o modificas un agente en `.claude/agents/`, actualiza tambien su copia en `.github/agents/` para mantener Copilot CLI sincronizado.

## Durante el workshop

Los asistentes implementaran features completas usando el pipeline de AI Agents:

1. Definir la feature con el **PM Analyst**
2. Disenar la arquitectura con el **Fullstack Architect**
3. Implementar backend con el **Backend Developer**
4. Testear con el **QA Tester**
5. Implementar frontend con el **Frontend Developer**
6. Verificar en browser con el **QA Tester**

Si tienes dudas sobre el flujo de trabajo, usa el agente **Workshop Mentor** para guia metodologica.

## Problemas comunes

Ver `docs/TROUBLESHOOTING.md` para soluciones a problemas frecuentes.
