> **Documento de referencia, no skill instalada.** Describe la skill `doc-update` y el agente `doc-update` que el asistente
> crea en el bloque "Gestión Documental: Specs y Wiki Autoactualizable" (ver `docs/PROMPTS.md`, Prompt 8).
> Para convertirlo en skill: copiar desde el frontmatter hasta el final de la sección "Reglas" a
> `.claude/skills/doc-update/SKILL.md`. La definición del agente está al final.

---
name: doc-update
description: Actualiza la documentación viva del proyecto (docs/specs, docs/adr, docs/api, docs/onboarding, CLAUDE.md anidados) después de cada implementación, leyendo el código real y reflejando los cambios. Usar al terminar una feature, al archivar un change de OpenSpec, al detectar que la documentación no coincide con el código, o cuando se invoque el agente doc-update.
---

# Doc Update — Wiki autoactualizable del Workshop

> "La documentación que no se actualiza sola, no se actualiza."

`/docs` es la **wiki del proyecto**: la leen personas y agentes. El agente la actualiza automáticamente después de cada
feature a partir del código real, de forma que la siguiente sesión (o el siguiente agente) lee la wiki en vez de
redescubrir el código. `CLAUDE.md` es el **archivo de contexto maestro**: corto, siempre cargado, y con el mapa hacia la wiki.

## Cuándo activar
- Último paso del cierre de una feature (después de tests, auditoría y revisión)
- Al archivar un change (`/opsx archive`)
- Al empezar una sesión si la wiki contradice el código (se corrige antes de seguir)
- Cuando el usuario lance el agente `doc-update`

## Estructura de `/docs`

```
docs/
├── README.md              ← Portada de la wiki: qué hay en cada carpeta y cómo navegar (índice)
├── specs/                 ← Qué debe hacer cada feature (requisitos, criterios de aceptación). Una por feature.
│   └── {feature}.md
├── adr/                   ← Architecture Decision Records: una decisión por archivo, numerados, nunca se borran.
│   └── 0001-{titulo-kebab}.md
├── api/                   ← Documentación de la API generada desde los controllers: una por módulo.
│   └── {feature}.md
├── onboarding/            ← Guías para personas y agentes nuevos: setup, configuración, troubleshooting, glosario.
│   ├── SETUP.md
│   ├── CONFIGURACION-PROYECTO.md
│   └── TROUBLESHOOTING.md
└── PROMPTS.md             ← Material del workshop (no forma parte de la wiki del producto)
```

Más los **índices que carga Claude Code**:

| Archivo | Quién lo carga | Contenido |
|---------|----------------|-----------|
| `CLAUDE.md` (raíz) | Siempre | Reglas, comandos, arquitectura y la sección "Documentation Map" (qué leer para cada pregunta). **≤ ~200 líneas** (a partir de ahí el agente empieza a ignorarlo): lo que crezca, se mueve a `docs/` y se enlaza |
| `apps/backend/CLAUDE.md` | Al trabajar dentro de `apps/backend` | Tabla de módulos: una línea + enlace a `docs/api/{modulo}.md` y `docs/specs/{feature}.md` |
| `apps/frontend/CLAUDE.md` | Al trabajar dentro de `apps/frontend` | Tabla de rutas/páginas: una línea + componentes clave + enlace a la spec |
| `openspec/specs/{capability}/spec.md` | OpenSpec | Requisitos y escenarios sincronizados por `/opsx archive`; `docs/specs/{feature}.md` enlaza aquí cuando exista |
| `openspec/config.yaml` → `context:` | OpenSpec al crear artefactos | Stack, convenciones y dominio en ≤ 15 líneas |

Regla de oro: **cada documento responde a una pregunta y tiene un dueño**. Si dos responden a la misma, uno sobra.

| Pregunta | Documento |
|----------|-----------|
| ¿Qué debe hacer? | `docs/specs/{feature}.md` |
| ¿Cómo se llama a la API? | `docs/api/{modulo}.md` |
| ¿Por qué se hizo así? | `docs/adr/NNNN-*.md` |
| ¿Cómo arranco / configuro / arreglo? | `docs/onboarding/*` |
| ¿Qué módulos hay y dónde están? | `apps/*/CLAUDE.md` |
| ¿Qué reglas sigo al programar? | `CLAUDE.md` raíz + skills |

## Plantillas

### `docs/api/{modulo}.md` — generado desde el controller, los DTOs y el schema

````markdown
# API — {Módulo}

> Sincronizado: {fecha} · commit {sha corto} · fuente: apps/backend/src/{modulo}/{modulo}.controller.ts

## Modelo `{Model}`
| Campo | Tipo | Requerido | Notas |
|-------|------|-----------|-------|
| nombre | string | sí | único, máx 100 |
| createdAt / updatedAt | Date | auto | timestamps de Mongoose |

## Endpoints
| Método | Ruta | Body / Query | Respuesta | Errores |
|--------|------|--------------|-----------|---------|
| POST | /api/{modulo} | Create{Model}Dto | 201 { id, ...fields, createdAt, updatedAt } | 400 validación · 409 duplicado |
| GET | /api/{modulo}?page&limit&search | Query DTO | 200 { total, items, page, limit } | 400 |
| GET | /api/{modulo}/:id | — | 200 | 404 |
| PATCH | /api/{modulo}/:id | Update{Model}Dto (parcial) | 200 | 400 · 404 · 409 |
| DELETE | /api/{modulo}/:id | — | 204 | 404 |

## Ejemplo
```bash
curl -X POST http://localhost:3001/api/{modulo} -H 'Content-Type: application/json' -d '{"nombre":"Demo"}'
```

## Reglas de negocio que no se ven en los tipos
- Lista (unicidad, estados, límites, permisos)

## Consumidores en el frontend
- `apps/frontend/app/{feature}/hooks/use{Feature}.ts`
````

### `docs/specs/{feature}.md` — qué debe hacer

```markdown
# Spec — {Feature}

> Estado: implementada | en curso · OpenSpec: openspec/specs/{capability}/spec.md · API: ../api/{modulo}.md

## Objetivo
Una frase: problema y para quién.

## Requisitos
- R1. ...
- R2. ...

## Criterios de aceptación
- [ ] Dado … cuando … entonces …

## Fuera de alcance
- ...

## Decisiones relacionadas
- [ADR-0001](../adr/0001-titulo.md)
```

### `docs/adr/NNNN-{titulo}.md` — por qué se hizo así

```markdown
# ADR-NNNN — {Título en una frase}

- Fecha: {fecha} · Estado: aceptada | sustituida por ADR-MMMM
- Afecta a: módulos / archivos

## Contexto
Qué problema había y qué opciones se barajaron.

## Decisión
Qué se eligió.

## Consecuencias
Qué hacer y qué no hacer a partir de ahora.
```

### `apps/backend/CLAUDE.md` — índice que carga Claude Code dentro de la carpeta

```markdown
# Backend — índice de módulos

Antes de tocar un módulo, lee su API doc y su spec. Si no coinciden con el código, corrige la wiki primero.

| Módulo | Qué hace | API | Spec |
|--------|----------|-----|------|
| categories | CRUD de categorías con unicidad por nombre | ../../docs/api/categories.md | ../../docs/specs/categorias.md |
```

### Sección "Documentation Map" en el `CLAUDE.md` raíz

```markdown
## Documentation Map (read before coding)

| Question | Read |
|----------|------|
| What modules exist and where? | `apps/backend/CLAUDE.md`, `apps/frontend/CLAUDE.md` |
| What should feature X do? | `docs/specs/{feature}.md` (+ `openspec/specs/`) |
| How do I call the API? | `docs/api/{module}.md` |
| Why was it done this way? | `docs/adr/` |
| Setup / config / troubleshooting | `docs/onboarding/` |
| Wiki home | `docs/README.md` |
```

## Procedimiento — después de cada implementación

1. **Detectar qué cambió**: `git diff main...HEAD --stat` (o desde el último commit `docs(`). Agrupar por módulo backend y página frontend. Ignorar cambios solo de tests.
2. **Regenerar desde el código, no desde la memoria**:
   - `docs/api/{modulo}.md`: leer controller (`@Get/@Post/@Patch/@Delete`, rutas, pipes), DTOs (decoradores de validación) y schema (campos, índices). Reescribir las tablas enteras; no parchear a mano.
   - `docs/specs/{feature}.md`: si viene de OpenSpec, enlazar a `openspec/specs/`; marcar criterios cumplidos según los tests existentes.
   - `docs/adr/`: si en la sesión hubo una decisión no obvia (librería, patrón, cambio de contrato, trade-off), crear el siguiente número. Si se revierte una decisión, nueva ADR que sustituye, nunca editar la antigua.
   - `apps/backend/CLAUDE.md` y `apps/frontend/CLAUDE.md`: añadir/renombrar filas.
   - `docs/README.md`: añadir el enlace si hay documento nuevo.
   - `CLAUDE.md` raíz: **solo** si cambia una regla, un comando o aparece un tipo de documento nuevo. Si supera ~200 líneas, mover contenido a `docs/onboarding/` y dejar el enlace.
   - `openspec/config.yaml` → `context:` si cambió el stack o el dominio.
3. **Verificar coherencia** (automático, sin criterio):
   ```bash
   # Cada enlace relativo de la wiki apunta a un archivo existente
   grep -rhoE "\]\((\.\./|\./)?[A-Za-z0-9_./-]+\.md" docs apps/*/CLAUDE.md CLAUDE.md | sort -u   # revisar con ls
   # Cada endpoint documentado existe en el controller
   grep -nE "@(Get|Post|Patch|Put|Delete)\(" apps/backend/src/{modulo}/{modulo}.controller.ts
   # CLAUDE.md sigue corto
   wc -l CLAUDE.md
   ```
4. **Commit separado**: `docs({feature}): sync wiki`. Nunca mezclar con código.
5. **Informe**: lista de documentos creados/actualizados y discrepancias encontradas entre wiki y código.

## Procedimiento — al empezar una sesión sobre un módulo existente

1. Leer `apps/*/CLAUDE.md` → `docs/api/{modulo}.md` → `docs/specs/{feature}.md` → ADRs enlazadas, **antes** de abrir el código.
2. Contrastar en dos minutos con el controller y el schema. Si no coincide: corregir la wiki, avisar al usuario (alguien cerró sin sincronizar) y seguir.

## Reglas
- La wiki se genera **desde el código**; la memoria de la conversación solo aporta el "por qué" (ADRs).
- Corta y enlazada: ningún documento de la wiki supera ~100 líneas; `CLAUDE.md` raíz ≤ ~200.
- Todo documento generado lleva fecha y commit de sincronización.
- No duplicar: si está en `CLAUDE.md`, una skill o la spec de OpenSpec, se enlaza.
- Si wiki y código discrepan, gana el código y se arregla la wiki en el mismo turno.
- Solo toca `docs/`, `apps/*/CLAUDE.md`, `CLAUDE.md` raíz y `openspec/config.yaml`. Nunca código fuente.

---

## Agente `doc-update` (referencia)

El agente envuelve la skill para poder lanzarla con un solo prompt ("ejecuta el agente doc-update sobre lo de hoy")
o desde un hook. Copiar a `.claude/agents/doc-update.md` (alias `model: sonnet`) y a `.github/agents/doc-update.md`
(id `claude-sonnet-4.5`), como el resto de agentes del proyecto.

````markdown
---
name: doc-update
description: "Use this agent after implementing or modifying features to update the living documentation (docs/specs, docs/adr, docs/api, docs/onboarding, nested CLAUDE.md) from the real code. Examples: user says 'actualiza la documentación de lo que hemos hecho hoy', 'ejecuta doc-update sobre categories', or a feature was just closed."
model: sonnet
color: blue
---

Eres el responsable de la wiki del proyecto. Aplicas la skill `doc-update` al pie de la letra.

## Entrada
Recibes en el prompt el alcance: una lista de módulos/páginas, o "todo lo cambiado desde main" (`git diff main...HEAD --stat`).

## Proceso
1. Lee la skill `doc-update` y el `CLAUDE.md` raíz.
2. Determina los módulos afectados y, para cada uno, lee controller, DTOs, schema, página, hooks y tests.
3. Regenera los documentos según las plantillas de la skill. Reescribe tablas enteras desde el código.
4. Crea ADRs solo para decisiones no obvias que aparezcan en el diff o que el usuario te indique.
5. Ejecuta las verificaciones de coherencia de la skill y corrige lo que falle.
6. No hagas commit: deja los cambios en el árbol y entrega el informe.

## Restricciones
- Solo escribes en `docs/`, `apps/*/CLAUDE.md`, `CLAUDE.md` raíz y `openspec/config.yaml`. Nunca tocas código ni tests.
- `CLAUDE.md` raíz: solo si cambia una regla, un comando o aparece un tipo de documento nuevo; nunca por encima de ~200 líneas.
- Si encuentras una discrepancia entre wiki y código, gana el código; documéntala en el informe.

## Salida
```
## Doc update — {alcance}
Creados: …
Actualizados: …
ADRs nuevas: …
Discrepancias wiki↔código corregidas: …
Pendiente de decisión humana: …
```
````
