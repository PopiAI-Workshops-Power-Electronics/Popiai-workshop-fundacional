> **Documento de referencia, no skill instalada.** Describe lo que debe contener la skill `code-review`
> que el asistente crea durante el cierre del loop (ver `docs/PROMPTS.md`, Prompt 7). Para convertirlo en skill:
> copiar este contenido a `.claude/skills/code-review/SKILL.md` conservando el frontmatter de abajo.

---
name: code-review
description: Qué mirar al revisar código de este proyecto (NestJS + Mongoose + Next.js) y cómo reportarlo. Usar al revisar un diff, un PR o una feature antes de darla por terminada, o al actuar como revisor con contexto limpio en el cierre del loop.
---

# Code Review — Workshop

Criterios y proceso para revisar código del proyecto. Es la referencia de las Partes B (calidad) y C (revisión general)
del "cierre del loop". La seguridad tiene su propia skill: `security-review`. Los tests, la suya: `testing-patterns`.

## Cuándo activar
- Antes de dar por terminada una feature
- Al revisar un PR o una rama (`git diff main...HEAD`)
- Cuando un subagente actúa como revisor final con contexto limpio

## Principio

Una revisión responde a cuatro preguntas, en este orden de importancia:

1. **¿Hace lo que se pidió?** (correctitud frente a la spec / el prompt original)
2. **¿Hace solo lo que se pidió?** (sin scope creep, sin cambios colaterales)
3. **¿Lo hace como se hace en este proyecto?** (CLAUDE.md + skills)
4. **¿Está demostrado que funciona?** (tests y verificación reales)

El estilo (formato, nombres, imports) lo cubre el linter; no es objeto de la revisión salvo que afecte a la legibilidad de forma clara.

## Proceso

1. **Lee lo que se pidió** antes de leer el código: spec en `openspec/changes/*/` o `docs/specs/`, o el prompt original.
2. **Lista el diff**: `git diff main...HEAD --stat`. Cualquier archivo fuera del alcance esperado es un hallazgo de la pregunta 2 (configs, puertos, dependencias, archivos generados).
3. **Recorre el diff por capas** con las checklists de abajo. Anota cada hallazgo con `archivo:línea`.
4. **Ejecuta, no supongas**: lint, build y tests (`verification-checklist`). Si el autor dice que algo está probado, compruébalo.
5. **Aplica `security-review`** sobre el mismo diff.
6. **Reporta** con el formato del final y un veredicto.

## Checklist — Backend (NestJS)

| Mirar | Esperado |
|-------|----------|
| Estructura del módulo | `src/{feature}/` con `module`, `controller`, `service`, `schemas/`, `dto/`, `*.spec.ts`; módulo registrado en `app.module.ts` |
| Controller | Solo orquesta: recibe DTO, llama al service, devuelve. Sin lógica de negocio ni acceso directo al modelo |
| Service | Lógica de negocio aquí; lanza `NotFoundException`/`ConflictException`/`BadRequestException`; no conoce `Request`/`Response` |
| DTOs | `create-*.dto.ts` con `class-validator`; `update-*.dto.ts` con `PartialType`; query DTO para paginación/filtros |
| Respuestas | `{ id, ...fields, createdAt, updatedAt }`; paginación `{ total, items, page, limit }` |
| Errores | 400 validación, 404 no encontrado, 409 conflicto (duplicate key capturado, no 500) |
| Inyección de dependencias | Por constructor; sin `new Service()`; sin singletons manuales |
| Async | Sin promesas sin `await`; sin `try/catch` que trague errores y devuelva `null` |
| Config | Sin cambios en `main.ts`, puertos, `ValidationPipe`, CORS salvo que la tarea lo pida |

## Checklist — Datos (Mongoose)

| Mirar | Esperado |
|-------|----------|
| Schema | `@Schema({ timestamps: true })`; tipos explícitos; `required`/`default`/`enum` donde toca |
| Índices | En campos que se consultan o deben ser únicos (`unique: true` + manejo del E11000 → 409) |
| Queries | `lean()` en lecturas; proyección de campos sensibles; sin N+1 (bucles con `findById` dentro) |
| Paginación | `skip/limit` acotados y `countDocuments` para `total` |
| Transformación | `_id` → `id`, sin `__v` en la respuesta (`toJSON` transform o mapeo en service) |

## Checklist — Frontend (Next.js)

| Mirar | Esperado |
|-------|----------|
| Estructura | `app/{feature}/page.tsx`, `components/`, `hooks/`, `types.ts` |
| Server vs Client | Server Components por defecto; `'use client'` solo en el componente que necesita estado/eventos, no en la página entera |
| Datos | `fetch` solo en hooks o en Server Components; nunca en el cuerpo de un componente cliente; `NEXT_PUBLIC_API_URL` como base |
| Cuatro estados | loading, error, empty, success — todos renderizados, no solo success |
| Tipos | Interfaces para props y respuestas de API; sin `any` |
| Marca | Solo tokens de `brand-design` (`bg-primary`, `text-body`, `border-border`…); sin hex, sin `gray-*`, sin `dark:` |
| Accesibilidad | HTML semántico, `label` asociado a cada input, botones con texto o `aria-label`, foco visible, navegable con teclado |
| Responsive | Mobile-first; comprobado en móvil |
| Rendimiento | Sin `useEffect` para derivar estado; listas con `key` estable; imágenes con `next/image`; ver `react-best-practices` si hay dudas |

## Checklist — Tests

| Mirar | Esperado |
|-------|----------|
| Existencia | Cada `service`/`controller`/`guard` tocado tiene `*.spec.ts` |
| Cobertura | ≥ 80% en los módulos tocados (`npm run test:cov`) |
| Qué prueban | Caso feliz **y** errores (404, 409, 400) **y** algún edge case (vacío, límites) — no solo el camino fácil |
| Aislamiento | Modelo de Mongoose y servicios externos mockeados; sin DB real en unit tests |
| Señales de test débil | Un único `it`; `expect(true)`; asserts solo sobre `toHaveBeenCalled` sin comprobar el resultado; tests que replican la implementación |
| Frontend | E2E de Playwright para el flujo principal si la feature tiene UI (ver `testing-patterns`) |

## Checklist — Alcance y limpieza

| Mirar | Esperado |
|-------|----------|
| Scope | Nada fuera de lo pedido: ni refactors "de paso", ni dependencias nuevas sin justificar, ni cambios en configs/puertos/CLAUDE.md |
| Código muerto | Sin `console.log`, código comentado, imports sin usar, TODOs sin contexto |
| Duplicación | Reutiliza lo que ya existe (`api-client`, helpers, DTOs compartidos) antes de crear algo nuevo |
| Nombres | Revelan intención; coherentes con el resto del módulo |
| Docs | `.env.example`/`docs/CONFIGURACION-PROYECTO.md` actualizados si hay variables o pasos nuevos |
| Git | Conventional commits, una rama por feature (`git-workflow`) |

## Severidad

| Nivel | Criterio |
|-------|----------|
| **Alta** | Incumple lo pedido, rompe algo existente, bug reproducible, o hallazgo alto de `security-review` |
| **Media** | Viola una convención del proyecto (CLAUDE.md/skills), test débil o ausente, scope creep |
| **Baja** | Mejora de legibilidad o mantenibilidad sin impacto funcional |

## Formato del informe

```markdown
## Revisión final — [feature]

**Lo pedido:** [una línea con la fuente: spec / prompt]
**Alcance del diff:** N archivos; fuera de alcance: [ninguno | lista]

| # | Hallazgo | Severidad | Archivo:línea | Acción |
|---|----------|-----------|---------------|--------|
| 1 | update() no captura E11000 → devuelve 500 en nombre duplicado | Alta | categories.service.ts:58 | Capturar y lanzar ConflictException |

**Verificación ejecutada:** lint [OK/KO] · build [OK/KO] · tests [N pasan, cobertura X%] · navegador [URL/KO/n.a.]
**Seguridad:** ver auditoría (`security-review`) — [sin hallazgos altos | #…]

**Veredicto:** APROBADO | CAMBIOS NECESARIOS
```

## Reglas
- Lee la spec antes que el código; si no hay spec, pide el prompt original.
- Evidencia en cada hallazgo (`archivo:línea` o comando + salida). Sin evidencia, no es un hallazgo.
- Un veredicto APROBADO exige: cero altas, cero medias sin justificar, verificación ejecutada de verdad.
- Quien revisa no es quien escribió el código: en el cierre del loop, la revisión final la hace un subagente con contexto limpio.
- No aprobar por cansancio: si tras corregir hay cambios nuevos, se vuelven a revisar.
