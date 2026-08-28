> **Documento de referencia, no skill instalada.** Describe lo que debe contener la skill `security-review`
> que el asistente crea durante el cierre del loop (ver `docs/PROMPTS.md`, Prompt 7). Para convertirlo en skill:
> copiar este contenido a `.claude/skills/security-review/SKILL.md` conservando el frontmatter de abajo.

---
name: security-review
description: Checklist de auditoría de seguridad y RGPD para el stack del proyecto (NestJS + Mongoose + Next.js). Usar al auditar un diff o una feature antes de darla por terminada, al revisar un PR, o cuando se toquen inputs, auth, cookies, queries, datos personales o variables de entorno.
---

# Security Review — Workshop

Criterios de seguridad y protección de datos que debe cumplir cualquier código del proyecto. Se aplica sobre el **diff** de la rama
(`git diff main...HEAD`) y sobre el código que ese diff toca. Es la referencia de la Parte B del "cierre del loop".

## Cuándo activar
- Antes de dar por terminada una feature (junto con `verification-checklist` y `code-review`)
- Al revisar un PR
- Siempre que se toquen: DTOs, controllers, queries de Mongoose, auth/cookies, `main.ts`, variables de entorno, `fetch` en el frontend

## Cómo auditar

1. Lista los archivos del diff y clasifícalos: entrada de datos (DTO/controller), acceso a datos (service/schema), salida (response), frontend, config.
2. Recorre las secciones de abajo **en orden**. Para cada punto, busca evidencia en el código (archivo:línea); no asumas.
3. Ejecuta las comprobaciones automáticas del final.
4. Entrega el informe en el formato indicado. Corrige todo lo de severidad alta y media antes de cerrar.

## 1. Entrada de datos (backend)

| Comprobar | Cómo debe estar |
|-----------|-----------------|
| Todo body/query pasa por un DTO | Clase con decoradores `class-validator` (`@IsString`, `@IsEmail`, `@MaxLength`, `@IsEnum`, `@IsOptional`…). Nunca `@Body() body: any` |
| `ValidationPipe` global intacto | `main.ts` mantiene `whitelist: true`, `forbidNonWhitelisted: true`, `transform: true` → evita *mass assignment* |
| Ids de ruta validados | `@Param('id', ParseObjectIdPipe)` o validación explícita de `ObjectId` → 400, no 500 |
| Límites de tamaño | Strings con `@MaxLength`, arrays con `@ArrayMaxSize`, paginación con `limit` acotado (`@Max(100)`) |
| Enums y valores cerrados | `@IsEnum` en lugar de strings libres (role, status, sort) |
| Subida de archivos | Tipo MIME y tamaño limitados; nombre de archivo nunca usado tal cual en rutas |

## 2. Acceso a datos (Mongoose)

| Comprobar | Cómo debe estar |
|-----------|-----------------|
| Sin inyección NoSQL | Nunca pasar objetos del request directamente a `find`/`findOne`/`updateOne`. Los campos del filtro se construyen en el service a partir de valores ya validados (string, no objeto) |
| Operadores `$` | Un valor de entrada no puede convertirse en `{ $gt: '' }`, `{ $ne: null }`, `{ $where }`; `ValidationPipe` + tipos primitivos en DTO lo evitan — verificar que el DTO no acepta `object` |
| Búsqueda por texto | Escapar la entrada antes de construir un `RegExp` (`new RegExp(escapeRegex(search), 'i')`) |
| Updates acotados | `findByIdAndUpdate(id, { $set: dto })` con DTO `PartialType` — nunca `{ ...req.body }` |
| Borrados | Soft delete o comprobación de pertenencia si hay usuario; nunca `deleteMany` con filtro construido desde el request |

## 3. Salida de datos (respuestas)

| Comprobar | Cómo debe estar |
|-----------|-----------------|
| Campos sensibles | `passwordHash`, tokens, secretos, campos internos: excluidos con `select: false` en el schema o `@Exclude()` + `ClassSerializerInterceptor`; nunca devolver el documento crudo |
| Formato estable | `{ id, ...fields, createdAt, updatedAt }` — sin `_id`, `__v` ni campos de Mongoose |
| Errores | Solo `HttpException` de NestJS (400/401/403/404/409). Sin `stack`, sin mensajes de Mongo (`E11000…`) ni rutas internas en el body |
| Logs | Sin `console.log` de bodies, tokens ni cookies |

## 4. Autenticación y sesión (cuando exista)

| Comprobar | Cómo debe estar |
|-----------|-----------------|
| Guards en todo lo no público | Endpoints protegidos por defecto; lo público marcado explícitamente (`@AllowAnonymous()`) — ver skill `auth-flow` |
| Autorización, no solo autenticación | Recursos filtrados por usuario/rol en el **service**, no solo en el guard |
| Contraseñas | Hash con `bcrypt` (cost ≥ 10). Nunca en claro, nunca en logs, nunca comparadas con `===` |
| Tokens/cookies | Cookies `httpOnly`, `sameSite` (`lax` en dev, `strict`/`none`+`secure` según despliegue), `secure` fuera de local; expiraciones cortas; refresh rotado y revocable |
| Mensajes de login | Mismo mensaje para "usuario no existe" y "contraseña incorrecta" |
| CSRF | Si la sesión va en cookie, las mutaciones necesitan `sameSite` adecuado o token CSRF |

## 5. Configuración y secretos

| Comprobar | Cómo debe estar |
|-----------|-----------------|
| Sin secretos en el código | Ni en `.ts`, ni en tests, ni en docs. Patrones sospechosos: `password:`, `secret`, `apiKey`, `sk-`, `mongodb+srv://user:pass@` |
| Variables de entorno | Toda variable nueva documentada en `.env.example` (sin valor real) y en `docs/CONFIGURACION-PROYECTO.md` |
| `.env` ignorado | `.gitignore` cubre `.env`, `.env.local`; `git ls-files | grep .env` no devuelve nada |
| CORS | `origin` explícito (`http://localhost:3000`), nunca `*` con `credentials: true` |
| Cabeceras | `helmet` recomendado si el backend se expone fuera de local |
| Rate limiting | `@nestjs/throttler` en login/signup y endpoints costosos si hay auth |
| Puertos | No se cambian (3000/3001) — regla del proyecto |

## 6. Frontend (Next.js)

| Comprobar | Cómo debe estar |
|-----------|-----------------|
| XSS | Sin `dangerouslySetInnerHTML` con datos de usuario; sin construir HTML por concatenación |
| Secretos en cliente | Solo variables `NEXT_PUBLIC_*` llegan al navegador y **no** deben contener secretos. Las claves privadas viven en Server Components / Route Handlers |
| Llamadas a la API | Solo desde hooks (`apps/frontend/lib/api.ts` o equivalente), con `NEXT_PUBLIC_API_URL`; sin URLs hardcodeadas de otros entornos |
| Cookies de sesión | `credentials: 'include'` solo hacia la API propia |
| Redirecciones | `redirect`/`router.push` solo a rutas internas; nunca a una URL que venga de query params sin validar |
| Datos mostrados | Escapar/limitar lo que se renderiza de la API (longitudes, tipos); no confiar en que el backend ya filtró |

## 7. Dependencias

| Comprobar | Cómo debe estar |
|-----------|-----------------|
| Vulnerabilidades | `npm audit --audit-level=high` limpio en `apps/backend` y `apps/frontend` |
| Dependencias nuevas | Justificadas, mantenidas (último release < 1 año), sin alternativas ya presentes en el proyecto |
| Lockfile | `package-lock.json` actualizado y commiteado junto a `package.json` |

## 8. RGPD / GDPR (datos personales)

Aplica en cuanto un schema guarde datos de personas (email, nombre, IP, identificadores de usuario, contenido que una persona escribe).

| Comprobar | Cómo debe estar |
|-----------|-----------------|
| Minimización | Solo se guardan los campos necesarios para la función. Cada campo personal nuevo en un schema tiene justificación en la spec; nada "por si acaso" |
| Base legal y consentimiento | Si el dato no es imprescindible para el servicio (marketing, analítica), hay un campo de consentimiento explícito con fecha (`consents: { marketing: { granted: boolean, at: Date } }`) y la UI lo pide sin pre-marcar |
| Información al usuario | La UI que recoge datos enlaza a la política de privacidad y dice para qué se usan |
| Derecho de acceso | Existe (o está planificado) un endpoint que devuelve todos los datos de un usuario en formato exportable (`GET /api/users/me/export`) |
| Derecho al borrado | Existe `DELETE /api/users/me` (o equivalente admin) que borra o anonimiza **todas** las colecciones donde aparece el usuario, incluidos logs y tokens; soft delete solo si se anonimiza (`email → deleted-{id}@anon`, nombre → null) |
| Retención | Los datos con caducidad (tokens, logs, sesiones) tienen índice TTL en Mongo (`expireAfterSeconds`) o un job de purga documentado |
| Registros de auditoría | Las operaciones sensibles (login, cambio de rol, export, borrado, acceso admin a datos de otro usuario) se registran: quién, qué, cuándo, sobre quién — sin guardar el contenido del dato |
| Logs de aplicación | Sin datos personales en `console.log`/logger (emails, tokens, bodies completos). Se loguea el `id`, no el email |
| Datos en tests y seeds | Datos inventados (`user1@example.com`), nunca exportes de producción |
| Transferencias | Si se usa un tercero (email, analítica, IA), está documentado en `docs/onboarding/` qué datos recibe y dónde se procesan |
| Cifrado | TLS fuera de local; contraseñas con bcrypt; campos especialmente sensibles (documentos de identidad, salud) cifrados en reposo o no almacenados |

Señales de alarma en un diff: un campo `email`/`phone`/`address`/`birthDate` nuevo sin mención en la spec; un `find()` sin filtro por usuario en un endpoint de usuario; un `console.log(req.body)`; un `deleteOne` que borra el usuario pero no sus documentos relacionados.

## Comprobaciones automáticas

```bash
# Vulnerabilidades
cd apps/backend && npm audit --audit-level=high
cd apps/frontend && npm audit --audit-level=high

# Secretos y logs en el diff
git diff main...HEAD | grep -nEi "(password|secret|api[_-]?key|token)\s*[:=]\s*['\"][^'\"]+['\"]|sk-[A-Za-z0-9]{10,}|mongodb(\+srv)?://[^:]+:[^@]+@"
git diff main...HEAD | grep -nE "^\+.*console\.log"

# .env nunca trackeado
git ls-files | grep -E "\.env($|\.)" && echo "¡.env en el repo!" || echo "OK"

# ValidationPipe sigue global
grep -n "forbidNonWhitelisted: true" apps/backend/src/main.ts
```

## Severidad

| Nivel | Criterio | Acción |
|-------|----------|--------|
| **Alta** | Explotable sin autenticación o expone datos sensibles/secretos (inyección, campos sensibles en respuesta, secreto en código, endpoint sin guard, datos personales sin base legal o sin posibilidad de borrado) | Bloquea el cierre. Corregir ya |
| **Media** | Requiere condiciones (usuario autenticado, configuración concreta) o degrada defensas (CORS laxo, sin límites, errores que filtran internals) | Corregir antes de cerrar |
| **Baja** | Endurecimiento recomendable (helmet, throttler, logs) | Corregir o justificar por escrito |

## Formato del informe

```markdown
## Auditoría de seguridad — [feature]

| # | Hallazgo | Severidad | Archivo:línea | Acción |
|---|----------|-----------|---------------|--------|
| 1 | Búsqueda construye RegExp sin escapar la entrada | Media | categories.service.ts:42 | Escapar con escapeRegex() |

Comprobaciones automáticas: npm audit backend [OK/KO], frontend [OK/KO], secretos en diff [OK/KO], .env [OK/KO], ValidationPipe [OK/KO]
Corregidos: #1, #2. Justificados sin corregir: #3 (motivo).
```

## Reglas
- Evidencia siempre: cada hallazgo con archivo y línea, o comando ejecutado y su salida.
- No inventar hallazgos para rellenar la tabla; "sin hallazgos" con las comprobaciones ejecutadas es un resultado válido.
- Corregir un hallazgo implica volver a ejecutar los tests (`verification-checklist`).
