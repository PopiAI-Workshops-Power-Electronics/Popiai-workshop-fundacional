# Guia de Setup — PopiAI Workshop

## Requisitos previos

Antes del workshop, asegurate de tener instalado:

| Herramienta | Version minima | Verificar |
|-------------|---------------|-----------|
| Node.js | 20 LTS | `node --version` |
| npm | 10+ | `npm --version` |
| Docker Desktop | Ultima | `docker --version` |
| nvm | Cualquiera | `nvm --version` |
| Git | Cualquiera | `git --version` |
| Claude Code CLI | Ultima | `claude --version` |

## Paso 1: Clonar el repositorio

```bash
git clone https://github.com/[tu-org]/popi-workshop-base.git
cd popi-workshop-base
```

## Paso 2: Configurar Node.js

```bash
# Instalar la version correcta de Node si no la tienes
nvm install 20
nvm use
# Verificar: debe mostrar v20.x.x
node --version
```

## Paso 3: Instalar dependencias

```bash
npm install
```

Esto instala las dependencias de todos los workspaces (backend + frontend).

## Paso 4: Levantar MongoDB con Docker

```bash
docker compose up -d
```

Verifica que MongoDB esta corriendo:
```bash
docker ps
# Debes ver: workshop-mongodb   Up
```

## Paso 5: Verificar todo

```bash
npm run verify                 # Linux / macOS
python scripts/verify.py       # Windows
```

Si todo esta bien, veras checkmarks verdes. Si algo falla, consulta `TROUBLESHOOTING.md`.

## Paso 6: Iniciar los servicios

```bash
# Terminal 1 — Backend
npm run start:backend

# Terminal 2 — Frontend
npm run start:frontend
```

Verifica:
- Backend: http://localhost:3001/api/health → `{"status":"ok"}`
- Frontend: http://localhost:3000 → Pagina de inicio del workshop

## Paso 7: Claude Code

Claude Code es la herramienta de AI que usaremos durante el workshop. Es un CLI que se ejecuta en tu terminal.

### Instalar Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

### Verificar instalacion

```bash
claude --version
```

### Iniciar sesion

```bash
cd popi-workshop-base
claude
```

Al abrir Claude Code en el directorio del proyecto, automaticamente carga la configuracion de agentes, skills y comandos desde `.claude/` y `CLAUDE.md`.

### Usando GitHub Copilot CLI en vez de Claude Code

El proyecto tambien es compatible con [GitHub Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli). Al iniciar `copilot` en la raiz del repo:

- Lee `CLAUDE.md` automaticamente (instrucciones del proyecto).
- Lee las skills de `.claude/skills/*/SKILL.md` (misma ubicacion que Claude Code).
- Lee los agentes especializados desde `.github/agents/*.md` (copia sincronizada de `.claude/agents/`, con el campo `model` adaptado a los IDs de Copilot).
- Los comandos `/generar`, `/crear-modulo-crud`, `/test`, `/servicios` y `/generate-mr-description` (especificos de Claude Code) tienen su equivalente como skills invocables en `.claude/skills/`.

## Sistema de Agentes

El proyecto incluye 7 agentes especializados que se invocan a traves de Claude Code:

| Agente | Rol |
|--------|-----|
| **PM Analyst** | Transforma requerimientos en specs funcionales detalladas |
| **Fullstack Architect** | Disena arquitectura backend + frontend coherente |
| **Backend Developer** | Implementa modulos NestJS (schemas, DTOs, services, controllers) |
| **Frontend Developer** | Implementa paginas y componentes Next.js |
| **QA Tester** | Ejecuta tests backend (Jest) y frontend (browser) |
| **Web Styles Designer** | Especialista en CSS/Tailwind y diseno responsive |
| **Workshop Mentor** | Guia metodologica para trabajar con agentes AI |

### Pipeline de desarrollo

Los agentes se ejecutan **siempre en secuencia**, nunca en paralelo:

```
1. PM Analyst        → Crea la spec funcional
2. Fullstack Architect → Disena la arquitectura
3. Backend Developer  → Implementa el backend
4. QA Tester (backend)→ Tests del backend
5. Frontend Developer → Implementa el frontend
6. QA Tester (frontend)→ Tests y verificacion en browser
```

### Slash Commands utiles

```bash
# Dentro de Claude Code:
/generar componente MiComponente    # Genera un componente
/crear-modulo-crud productos        # CRUD completo
/test run                           # Ejecuta tests
/servicios status                   # Estado de servicios
/opsx propose                       # Nueva feature con OpenSpec (crea y genera artefactos)
```

Para la referencia completa de agentes, skills y convenciones, ver `CLAUDE.md`.

## Setup automatico (alternativa)

```bash
# Linux / macOS
chmod +x scripts/setup.sh
./scripts/setup.sh
```

```bash
# Windows (o cualquier sistema con Python 3.8+)
python scripts/setup.py
```

Este script hace todo automaticamente: instala dependencias, levanta Docker y verifica que todo funciona.
