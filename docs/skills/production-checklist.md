> **Documento de referencia, no skill instalada.** Describe lo que debe contener la skill `production-checklist`
> que el asistente crea en el Bloque 9 (ver `docs/PROMPTS.md`, Prompt 9). Para convertirlo en skill:
> copiar este contenido a `.claude/skills/production-checklist/SKILL.md` conservando el frontmatter de abajo.

---
name: production-checklist
description: Lista de verificación rigurosa antes de desplegar a producción el backend NestJS y el frontend Next.js — configuración, seguridad, datos, observabilidad, rendimiento, despliegue y rollback. Usar cuando se prepare un release, se configure un entorno de producción o el usuario pregunte si algo está listo para salir.
---

# Production Checklist — Workshop

`verification-checklist` dice si una feature está terminada en desarrollo. Esta skill dice si el proyecto puede **salir a producción**.
Se recorre entera antes de cada despliegue; cada punto se marca con evidencia (comando ejecutado, archivo, URL), nunca "de memoria".

## Cuándo activar
- Antes del primer despliegue y de cada release
- Al crear o cambiar la configuración de un entorno (staging, producción)
- Cuando el usuario pregunte "¿está listo para producción?"

## 1. Configuración y secretos

- [ ] Ningún secreto en el repo: `git log -p --all -S "JWT_SECRET" -- '*.ts' '*.json' '*.md'` sin resultados; `.env` ignorado
- [ ] Todas las variables de `.env.example` existen en el entorno de producción con valores propios (no los de desarrollo: `workshop-secret-…`, `localhost`)
- [ ] Secretos con entropía real (`openssl rand -base64 48`) y rotables sin redeploy del código
- [ ] `NODE_ENV=production` en el backend; `next build` en el frontend (no `next dev`)
- [ ] `NEXT_PUBLIC_API_URL` apunta al dominio real con HTTPS; ninguna variable `NEXT_PUBLIC_*` contiene un secreto
- [ ] CORS con el origen de producción exacto; `credentials: true` solo si hay cookies
- [ ] Puertos y hosts configurados por entorno, no hardcodeados

## 2. Seguridad (resumen de `security-review`, verificado en el build final)

- [ ] `ValidationPipe` global con `whitelist` + `forbidNonWhitelisted`
- [ ] `helmet` activado; cabeceras `Content-Security-Policy`, `X-Frame-Options`, `Strict-Transport-Security` presentes (comprobar con `curl -I`)
- [ ] `@nestjs/throttler` en login/signup y endpoints públicos costosos
- [ ] Cookies de sesión con `httpOnly`, `secure`, `sameSite` adecuados al dominio real; JWT con caducidad corta y refresh revocable
- [ ] `npm audit --audit-level=high` limpio en ambos apps; dependencias sin versiones `latest`/rangos abiertos peligrosos en el lockfile
- [ ] Endpoints de salud y métricas no exponen información interna (versiones, rutas, stack)
- [ ] Auditoría `security-review` ejecutada sobre el diff del release sin hallazgos altos ni medios

## 3. Datos (MongoDB) y RGPD

- [ ] Conexión con usuario de base de datos de mínimo privilegio (no root), TLS y `authSource` correctos; IP allowlist si es Atlas
- [ ] Índices creados en producción (`autoIndex` desactivado y migración/script que los crea, o verificación manual con `db.collection.getIndexes()`)
- [ ] Índices TTL en colecciones con caducidad (tokens, sesiones, logs)
- [ ] Copias de seguridad automáticas y **una restauración probada** en un entorno aparte
- [ ] Política de privacidad publicada y enlazada desde la UI donde se recogen datos
- [ ] Endpoints de exportación y borrado de datos de usuario funcionando (o procedimiento manual documentado con plazo)
- [ ] Registro de actividades de tratamiento actualizado si aplica (qué datos, para qué, cuánto tiempo, con quién se comparten)
- [ ] Logs sin datos personales; retención de logs definida

## 4. Calidad y tests

- [ ] `npm run lint`, `npm run build` y `npm run test:cov` en verde en CI, no solo en local; cobertura ≥ 80%
- [ ] E2E de Playwright del flujo principal en verde contra un entorno tipo producción (staging)
- [ ] Revisión final (`code-review`) con veredicto APROBADO sobre el diff del release
- [ ] Migraciones de datos (si las hay) probadas en staging con datos realistas y con plan de reversión

## 5. Observabilidad

- [ ] Logs estructurados (JSON) con nivel configurable por entorno; sin `console.log` sueltos
- [ ] Cada request con un identificador de correlación que aparece en los logs del backend
- [ ] Captura de errores no controlados (proceso y HTTP 5xx) hacia un sistema de alertas, con alerta probada a propósito
- [ ] Endpoint `/api/health` usado por el orquestador/monitor; health de MongoDB incluido
- [ ] Métricas mínimas: latencia p95, tasa de 5xx, uso de memoria; un panel donde mirarlas

## 6. Rendimiento y resiliencia

- [ ] Paginación obligatoria en todos los listados; `limit` máximo acotado
- [ ] Timeouts en llamadas salientes; reintentos solo en operaciones idempotentes
- [ ] Tamaño máximo de body configurado; subida de archivos limitada
- [ ] Frontend: `next build` sin warnings de bundle; imágenes con `next/image`; sin fetch en cascada evitables (ver `react-best-practices`)
- [ ] Prueba de carga básica del endpoint más usado (p. ej. `autocannon` 30 s) con p95 aceptable y sin fugas de memoria

## 7. Despliegue y rollback

- [ ] Build reproducible (`npm ci`, versión de Node de `.nvmrc`, lockfile commiteado)
- [ ] Despliegue automatizado desde `main` con el mismo artefacto que pasó CI
- [ ] Variables de entorno inyectadas por el entorno, no en la imagen
- [ ] Proceso supervisado (reinicio automático) y apagado limpio (`app.enableShutdownHooks()`)
- [ ] Rollback probado: se sabe cómo volver a la versión anterior en minutos, incluidas migraciones
- [ ] Changelog/notas de la release y etiqueta de versión (`git tag`)

## 8. Permisos del agente en el entorno de producción

Si un agente (Claude Code, CI con `claude -p`) toca el entorno de producción:

- [ ] Trabaja con credenciales de solo lectura salvo para la acción concreta que se le pide
- [ ] No tiene acceso a `.env` de producción ni a secretos (reglas `deny` de permisos + secretos inyectados por el entorno)
- [ ] Despliegues y migraciones requieren confirmación humana (modo de permisos sin bypass)
- [ ] Acciones registradas (qué comando, cuándo, quién lo aprobó)

## Formato del informe

```markdown
## Production readiness — {versión / fecha}

| Sección | Estado | Evidencia / pendiente |
|---------|--------|-----------------------|
| 1. Configuración y secretos | ✅ | … |
| 2. Seguridad | ⚠️ | Falta helmet — PR #… |
| … | | |

**Bloqueantes:** lista (no se despliega con ninguno abierto)
**Aceptados con riesgo:** lista con responsable y fecha límite
**Veredicto:** LISTO | NO LISTO
```

## Reglas
- Un punto sin evidencia no está marcado.
- Los bloqueantes son: cualquier punto de las secciones 1, 2 y 3, y el rollback de la 7.
- El checklist se guarda con la release (`docs/releases/{version}.md` o en la PR) para poder auditar qué se comprobó.
