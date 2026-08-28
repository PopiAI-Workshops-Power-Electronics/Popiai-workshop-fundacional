# Prompts del Workshop — PopiAI

Colección de prompts para usar con Claude Code durante el workshop.

---

## Prompt 1: Implementar CRUD de Categorías (Bloque 4)

```
Lee la spec en specs/categories.md.

Implementa el CRUD de Categorías completo siguiendo las convenciones del CLAUDE.md.

### Backend (apps/backend/)

1. Schema: src/categories/schemas/category.schema.ts
   - Campos: nombre (string, requerido, max 100), descripcion (string, opcional), activo (boolean, default true)
   - Timestamps automáticos
   - Índice único en nombre

2. DTOs: src/categories/dto/
   - create-category.dto.ts con validaciones class-validator
   - update-category.dto.ts con PartialType

3. Service: src/categories/categories.service.ts
   - create(dto) → Category
   - findAll() → Category[]
   - findOne(id) → Category | 404
   - update(id, dto) → Category | 404
   - remove(id) → void | 404
   - Manejo de duplicate key error → 409

4. Controller: src/categories/categories.controller.ts
   - POST /api/categories
   - GET /api/categories
   - GET /api/categories/:id
   - PATCH /api/categories/:id
   - DELETE /api/categories/:id

5. Module: src/categories/categories.module.ts → registrar en app.module.ts

6. Tests: categories.service.spec.ts con ≥80% coverage

### Frontend (apps/frontend/)

7. Tipos: app/categorias/types.ts
8. Hook: app/categorias/hooks/useCategorias.ts (fetch, create, update, delete)
9. Página: app/categorias/page.tsx con tabla de categorías
10. Formulario: app/categorias/components/CategoryForm.tsx

Verifica que compila y que los tests pasan.
Go.
```

---

## Prompt 2: Debugging (Demo errores)

```
Tengo un error en el CRUD de Categorías.

Síntoma: [describe qué pasa]

Error en consola:
[pega el error]

Arréglalo verificando que los tests siguen pasando.
```

---

## Prompt 3: Agregar paginación a GET /api/categories

```
Modifica GET /api/categories para soportar paginación.

Query params: ?page=1&limit=10 (defaults)
Respuesta: { total, items, page, limit }

Actualiza el frontend para mostrar controles de paginación.
Los tests existentes no deben romperse.
```

---

## Prompt 4: Agregar búsqueda por nombre

```
Agrega búsqueda a GET /api/categories con query param ?search=texto.
Debe buscar por nombre (case-insensitive, partial match).
Combina con la paginación existente.
```

---

## Prompt 5: Skill de Branding desde cero (Bloque 5)

> Una skill es un archivo `SKILL.md` con instrucciones que el agente aplica a todo lo que construye.
> El proyecto ya trae dos skills de marca con valores por defecto (Teal + Inter + Slate):
> `.claude/skills/brand-design/SKILL.md` (reglas y patrones) y `.claude/skills/design-guidelines/SKILL.md` (referencia visual).
> El ejercicio consiste en sustituir esos valores por una marca propia, definida desde cero con ayuda del agente.
>
> Recomendado: usar un modelo de alto razonamiento (`/model opus`) para la fase de entrevista y propuesta.

### Paso 1 — Entrevista y propuesta de marca

```
Quiero definir la identidad visual de este proyecto desde cero y plasmarla en las skills de marca.

Antes de proponer nada, hazme las preguntas clave una a una (usa AskUserQuestion):
- Sector y tipo de producto
- Audiencia objetivo (edad, contexto de uso, nivel técnico)
- Personalidad de marca (3 adjetivos) y qué NO queremos transmitir
- Referentes visuales que me gustan o que quiero evitar
- Restricciones: accesibilidad (contraste AA mínimo), modo claro/oscuro, tipografía disponible en Google Fonts

Con mis respuestas, propón 2-3 direcciones de marca. Para cada una:
- Nombre de la dirección y justificación en una frase (por qué encaja con el sector y la audiencia)
- Paleta: primary, primary-hover, primary-soft, accent, error, success, foreground, body, border, surface-alt, background (hex)
- Tipografía (una sola familia de Google Fonts) y escala tipográfica
- Radios, sombras y densidad de espaciado
- Verificación de contraste texto/fondo para las combinaciones principales

No toques ningún archivo todavía. Espera a que elija una dirección.
```

### Paso 2 — Aplicar la marca elegida

```
Elijo la dirección [nombre]. Aplícala al proyecto:

1. Actualiza .claude/skills/brand-design/SKILL.md:
   - Reglas MUST (escala de grises, fuente, color primario, sombras, radios, modo)
   - Tabla "Color Quick Reference" con los nuevos hex
   - Bloque @theme inline con los nuevos tokens
   - Patrones de componentes (botones, card, input, badges, alerts) adaptados
   - Sección Anti-Patterns con lo que NO se debe usar en esta marca
   - Corrige el frontmatter: description concreta para esta marca, author y version

2. Actualiza .claude/skills/design-guidelines/SKILL.md:
   - Brand Identity: nombre, tagline, personalidad, audiencia
   - Paleta completa con tokens, clases Tailwind y hex
   - Tipografía y escala

3. Actualiza apps/frontend/app/globals.css:
   - Sustituye los valores de @theme inline por los nuevos tokens
   - Si cambia la fuente, actualiza también apps/frontend/app/layout.tsx (next/font/google y la variable CSS)

4. Actualiza la tabla "Valores por defecto" de docs/CONFIGURACION-PROYECTO.md §1.

Mantén los NOMBRES de los tokens (--color-primary, --color-body, etc.) para que los componentes existentes sigan funcionando.
No añadas dependencias ni cambies ningún puerto.
Al terminar, arranca el frontend y comprueba en el navegador que la página de inicio refleja la nueva marca.
```

### Paso 3 — Comprobar que la skill se aplica

```
Crea un componente de ejemplo en apps/frontend/app/components/BrandShowcase.tsx
que muestre: botón primario, botón secundario, card con título y texto, input con label,
un badge de cada estado y un alert de cada tipo.
Úsalo en la página de inicio.

Solo puedes usar los tokens de la skill brand-design (nada de hex hardcodeados ni colores fuera de la paleta).
Verifícalo en el navegador y adjunta una captura.
```

### Variantes del punto de partida

Si en lugar de partir de cero se dispone de material, sustituye el Paso 1 por uno de estos:

**Desde una web existente**
```
Analiza https://[url-de-la-web] y extrae su identidad visual: paleta (con hex), tipografías,
radios, sombras, densidad y tono. Preséntamelo como propuesta con la misma estructura
que pide el Paso 1 y espera mi confirmación antes de tocar archivos.
```

**Desde un brandbook**
```
Lee el brandbook en docs/brand/[archivo].pdf y estructúralo en la forma que necesitan
las skills brand-design y design-guidelines: tokens de color, tipografía, escala, reglas MUST
y anti-patrones. Señálame qué información falta en el brandbook y propón valores para cubrirla.
Espera mi confirmación antes de tocar archivos.
```

### Qué debe quedar al final

- [ ] `brand-design/SKILL.md` y `design-guidelines/SKILL.md` describen la nueva marca sin restos de Teal/Inter
- [ ] `globals.css` tiene los nuevos tokens con los mismos nombres de variable
- [ ] La fuente se carga por `next/font/google` en `layout.tsx`
- [ ] Contraste AA en texto principal y botones
- [ ] La página de inicio se ve con la nueva marca en el navegador
- [ ] Un componente nuevo generado por el agente usa solo tokens de la skill

---

## Prompt 6: Landing page (Implementación)

> Ejercicio pensado para después del Bloque 5: la landing es la primera pieza que aplica la marca definida en
> `brand-design` / `design-guidelines`. La estructura de secciones recomendada está en `design-guidelines` → "Layout Structure".
> Sustituye la página de inicio actual (`apps/frontend/app/page.tsx`, placeholder "Workshop PopiAI — Ready").
>
> Atención a `apps/frontend/app/layout.tsx`: envuelve todo con un header y un `<main class="max-w-7xl px-6 py-8">`.
> Una landing necesita secciones a ancho completo y navbar propio, así que el layout raíz debe quedarse solo con
> `html`/`body`/fuente y el contenedor moverse a las páginas internas.

### Paso 1 — Estructura y copy

```
Quiero construir la landing page del proyecto en la ruta / aplicando la marca de .claude/skills/brand-design/SKILL.md.

Antes de escribir código, pregúntame (una a una, con AskUserQuestion):
- Qué producto/servicio vendemos y cuál es la propuesta de valor en una frase
- A quién va dirigida y qué acción principal queremos que haga (CTA)
- 3-4 beneficios o features clave
- Cómo funciona en 3 pasos
- Si hay prueba social (logos, testimonios, cifras) o no
- Enlaces del footer (legal, contacto, redes)

Con mis respuestas, propón la estructura de la landing sección a sección siguiendo la tabla
"Layout Structure" de design-guidelines (Navbar, Hero, Features, How it works, CTA final, Footer),
con el copy completo de cada sección (titulares, textos, etiquetas de botones) en español.
No toques archivos todavía; espera mi confirmación.
```

### Paso 2 — Implementación

```
Implementa la landing con la estructura y el copy confirmados:

1. Reestructura apps/frontend/app/layout.tsx: déjalo solo con html, body y la carga de la fuente.
   El header y el contenedor max-w-7xl actuales no deben aplicarse a la landing.
   Si hay páginas internas (p. ej. /categorias), dales su propio layout.tsx con ese contenedor.

2. Crea un componente por sección en apps/frontend/app/components/landing/:
   Navbar.tsx, Hero.tsx, Features.tsx, HowItWorks.tsx, CtaFinal.tsx, Footer.tsx
   y compónlos en apps/frontend/app/page.tsx.

3. Reglas:
   - Server Components por defecto; 'use client' solo donde haya interacción (menú móvil)
   - Solo tokens de brand-design (bg-primary, text-body, border-border…); nada de hex hardcodeados
   - Mobile-first: comprueba 375px, 768px y 1280px
   - HTML semántico (header, nav, main, section con aria-labelledby, footer) y navegación por teclado
   - Iconos con SVG inline; sin dependencias nuevas
   - Imágenes con next/image si las hay; metadata (title, description) en page.tsx

4. Arranca el frontend y verifica en el navegador los tres anchos. Corrige lo que no cuadre con la marca.
```

### Paso 3 — Auditoría y test

```
Audita la landing con la skill web-design-guidelines (accesibilidad, contraste, jerarquía, UX)
y corrige los hallazgos.

Después crea un test E2E con Playwright en apps/frontend/e2e/landing.spec.ts que compruebe:
- La página carga y muestra el titular del hero
- El CTA principal es visible y enlaza a la ruta esperada
- La navegación del navbar lleva a cada sección (anchors)
- El footer contiene los enlaces definidos

Ejecuta `npm run e2e` y deja los tests en verde.
```

### Qué debe quedar al final

- [ ] `app/page.tsx` es la landing; el placeholder "Ready" ha desaparecido
- [ ] `app/layout.tsx` reducido a html/body/fuente; las páginas internas conservan su contenedor
- [ ] Una carpeta `app/components/landing/` con un componente por sección
- [ ] Solo tokens de la skill de marca, sin colores fuera de la paleta
- [ ] Se ve correcta en móvil, tablet y escritorio
- [ ] Sin errores en la auditoría de accesibilidad; E2E de Playwright en verde


---

## Prompt 7: Cierre del loop (Implementación)

> "Cerrar el loop" = el agente no da una tarea por terminada hasta que **demuestra** que está bien, en tres niveles:
>
> 1. **Tests y verificación** — lint, build, tests con cobertura, arranque y comprobación en el navegador.
> 2. **Auditoría de código** — seguridad y calidad del diff (inputs, errores, secretos, dependencias, patrones del proyecto).
> 3. **Revisión general** — una segunda mirada con contexto limpio que compara lo hecho con lo pedido (spec, CLAUDE.md, skills).
>
> Primero el agente cierra el loop por sí mismo (Partes A-C); después se automatiza lo que es automatizable con un hook `Stop` (Parte D).
>
> Material del repo: skills `verification-checklist` (orden de verificación y formato de reporte) y `testing-patterns`
> (qué debe cubrir un test, Playwright E2E); agente `qa-tester` (modos backend / frontend / integration);
> comandos integrados de Claude Code `/security-review`, `/code-review` y `/simplify`.
> Las skills `security-review` y `code-review` **no vienen instaladas**: el asistente las crea en el Paso 0 a partir de
> `docs/skills/security-review.md` y `docs/skills/code-review.md` (qué mirar, severidad, formato del informe).

### Paso 0 — Crear las skills de auditoría y revisión

```
Crea dos skills nuevas en .claude/skills/ a partir de los documentos de referencia:
- .claude/skills/security-review/SKILL.md desde docs/skills/security-review.md
- .claude/skills/code-review/SKILL.md desde docs/skills/code-review.md

Para cada una: conserva el frontmatter (name, description), quita la nota inicial de "documento de referencia"
y adapta lo que no encaje con el estado actual del proyecto (p. ej. la sección de auth si aún no hay auth).
Regístralas en la tabla "Skills (auto-activated)" de CLAUDE.md con una línea cada una.
Comprueba que Claude Code las detecta: pídele que audite un archivo cualquiera y verifica que cita la skill.
```

### Parte A — Tests y verificación

Usa este prompt sobre una feature ya implementada (p. ej. el CRUD de Categorías del Prompt 1):

```
Antes de darme por terminada la feature de [nombre], cierra el loop siguiendo la skill verification-checklist:

1. Backend: lint, build, tests con cobertura (npm run test:cov, ≥80% en los módulos tocados) y arranque.
   Si falta algún *.spec.ts para un controller/service/guard tocado, créalo: caso feliz, casos de error (400/404/409)
   y dependencias mockeadas. Si algo falla, corrígelo y vuelve a empezar desde el paso que falló.
2. Frontend: lint, build y arranque.
3. Abre http://localhost:3000/[ruta] en el navegador y comprueba: consola sin errores, la página renderiza,
   el flujo completo funciona (crear, listar, editar, borrar), las llamadas a la API responden 200/201 en Network
   y la vista móvil se ve bien.
4. Cada fallo que encuentres: arréglalo, vuelve a ejecutar los tests y vuelve a comprobarlo en el navegador.
   No me preguntes, itera hasta que todo esté en verde.

Termina con el "Reporte de Verificación" en el formato de la skill, con los comandos ejecutados y sus resultados reales.
No marques nada como verificado que no hayas ejecutado.
```

Variante con agente QA (para enseñar la delegación):

```
Lanza el agente qa-tester en modo integration sobre la feature de [nombre].
Debe ejecutar el flujo completo frontend → backend real, probar los estados de error
y devolverme la lista de fallos. Corrige cada fallo y vuelve a lanzarlo hasta que no reporte ninguno.
```

### Parte B — Auditoría de código

Con los tests en verde, se audita el diff. Primero con los comandos integrados y después con una pasada manual contra los patrones del proyecto:

```
Ejecuta /security-review sobre los cambios de esta rama y después /code-review.
Corrige todos los hallazgos de severidad alta y media; los bajos, justifica por escrito si no los corriges.
```

Auditoría manual (si los comandos no están disponibles, o como segunda pasada):

```
Audita el diff de esta rama contra main (git diff main...HEAD) siguiendo las skills security-review y code-review. Revisa, en este orden:

Seguridad
- Todos los DTOs tienen class-validator y el ValidationPipe global (whitelist, forbidNonWhitelisted) sigue activo
- Ningún endpoint devuelve campos sensibles (passwordHash, tokens) ni acepta ids sin validar (ObjectId)
- Sin secretos, credenciales ni URLs de producción hardcodeados; las variables nuevas están en .env.example
- Errores HTTP correctos (400/404/409) sin filtrar stack traces ni mensajes internos
- npm audit --audit-level=high sin vulnerabilidades en apps/backend y apps/frontend

Calidad y convenciones (CLAUDE.md + skills api-patterns, mongodb-patterns, frontend-patterns, brand-design)
- Módulo registrado en app.module.ts; formato de respuesta { id, ...fields, createdAt, updatedAt }; timestamps automáticos
- Índices en los campos que se consultan; sin queries N+1; paginación { total, items, page, limit } si aplica
- Frontend: Server Components por defecto, 'use client' solo donde hay interacción; fetch solo en hooks; cuatro estados (loading/error/empty/success)
- Solo tokens de brand-design; sin hex hardcodeados; HTML semántico y accesible
- Sin código muerto, console.log, TODOs sin ticket ni duplicación evitable

Tests
- Cada service/controller tocado tiene spec con caso feliz + errores + mocks; nada testea detalles de implementación

Entrega una tabla: hallazgo | severidad (alta/media/baja) | archivo:línea | acción. Corrige alta y media, y vuelve a ejecutar los tests.
```

### Parte C — Revisión general (segunda mirada con contexto limpio)

El agente que ha escrito el código es el peor juez de su propio trabajo. La revisión final la hace un subagente
que parte de cero, leyendo solo lo que se pidió y lo que se entregó:

```
Lanza un subagente general-purpose con contexto limpio que actúe como revisor final. Pásale:
- Lo que se pidió: [pega el prompt original o la ruta de la spec]
- Las reglas del proyecto: CLAUDE.md y las skills code-review, security-review y testing-patterns
- Lo entregado: git diff main...HEAD

Debe seguir el proceso y el formato de informe de la skill code-review y responder a cuatro preguntas, con evidencia (archivo:línea o comando ejecutado):
1. ¿Se ha implementado TODO lo pedido? Lista lo que falta o se ha hecho distinto.
2. ¿Se ha hecho algo que NO se pidió? (scope creep, cambios de config, dependencias nuevas)
3. ¿Cumple CLAUDE.md y las skills? Señala cada desviación.
4. ¿Los tests prueban lo importante, o solo lo fácil?

Veredicto final: APROBADO / CAMBIOS NECESARIOS con la lista priorizada.
Si es CAMBIOS NECESARIOS, aplícalos y vuelve a lanzar el revisor hasta obtener APROBADO.
```

Variante con el agente del repo: `junior-branch-reviewer` (si está instalado) hace esta revisión y además devuelve la lista de cosas a probar a mano.

### Parte D — Automatizar el cierre con un hook `Stop`

Un hook `Stop` se ejecuta cada vez que Claude Code va a terminar un turno. Si el hook "bloquea",
Claude recibe el motivo como nuevo prompt y sigue trabajando. Automatiza la parte mecánica (A y parte de B);
la auditoría y la revisión (B manual y C) siguen siendo trabajo del modelo, pero el hook puede exigir que se hayan hecho.

```
Crea un hook Stop de Claude Code que impida terminar el turno si el código tocado no está verificado.

1. Script: scripts/hooks/check-tests-quality.js (Node, sin dependencias, que funcione en macOS/Linux/Windows).
   Debe:
   - Leer el JSON del evento por stdin (campos: session_id, cwd, hook_event_name, stop_hook_active, last_assistant_message).
   - Obtener los archivos modificados con `git diff --name-only HEAD` + `git ls-files --others --exclude-standard`.
   - Si no hay archivos tocados en apps/backend/src ni apps/frontend/app → salir con exit 0 (no bloquear).
   - Tests (backend): para cada controller/service/guard tocado, exigir que exista su *.spec.ts.
     Ejecutar `npm run test:cov -- --coverageReporters=json-summary --silent` en apps/backend y leer
     coverage/coverage-summary.json; bloquear si los tests fallan o la cobertura de líneas es < 80%.
   - Robustez de los specs tocados: más de un caso `it(`, al menos un caso de error (error/invalid/not found/throw/404/409)
     y uso de mocks (jest.fn / Test.createTestingModule).
   - Calidad (auditoría automatizable): `npm run lint` en el app tocado; `npm run build` en apps/frontend si se tocó;
     `npm audit --audit-level=high` en el app tocado; rechazar si el diff añade console.log, secretos con pinta de
     credencial (API_KEY=, password:, sk-…) o colores hex hardcodeados en className.
   - Revisión hecha: si se tocó código, exigir que last_assistant_message contenga las secciones
     "## Verificación Completada" y "## Revisión final" (veredicto APROBADO). Si no están, bloquear con
     el mensaje "Falta la auditoría/revisión final: ejecuta las Partes B y C del cierre del loop y reporta el resultado".
   - Para bloquear: escribir el motivo en stderr (lista concreta de lo que falta, con rutas) y salir con exit code 2.
     Para permitir: exit 0 sin salida.
   - Leer stop_hook_active: si es true, el hook ya forzó una continuación en este turno; aun así vuelve a verificar,
     pero que el mensaje de bloqueo sea corto e idempotente. Claude Code corta a los 8 bloqueos consecutivos.
   - Usar process.env.CLAUDE_PROJECT_DIR (o cwd del JSON) como raíz del repo; nunca rutas absolutas.

2. Regístralo en .claude/settings.json:
   {
     "hooks": {
       "Stop": [
         {
           "hooks": [
             { "type": "command", "command": "node \"$CLAUDE_PROJECT_DIR/scripts/hooks/check-tests-quality.js\"", "timeout": 300 }
           ]
         }
       ]
     }
   }

3. Pruébalo tú mismo:
   - Ejecuta el script a mano con `echo '{"hook_event_name":"Stop","stop_hook_active":false}' | node scripts/hooks/check-tests-quality.js; echo "exit=$?"`
     y comprueba exit 0 con el árbol limpio.
   - Crea un service sin su spec, vuelve a ejecutarlo y comprueba exit 2 con el motivo en stderr.
   - Añade un console.log y un hex hardcodeado en un componente, comprueba que también bloquea.
   - Borra los archivos de prueba.

Documenta el hook en docs/CONFIGURACION-PROYECTO.md (qué comprueba, cómo desactivarlo, cómo subir el umbral).
```

Después, demostración en vivo: pedir a Claude que implemente un service nuevo **sin decirle nada de tests ni de revisión**
y observar cómo el hook le obliga a escribir los tests, auditar y pasar la revisión antes de poder terminar.

### Variante para Copilot CLI

El mismo script sirve para el evento `agentStop` de GitHub Copilot CLI cambiando dos cosas: el registro va en
`.github/hooks/quality-check.json` (`"hooks": { "agentStop": [ { "type": "command", "command": "node scripts/hooks/check-tests-quality.js", "cwd": ".", "timeoutSec": 120 } ] }`)
y para bloquear hay que escribir por stdout `{"decision":"block","reason":"..."}` con exit 0 en vez de exit 2.
Se puede soportar ambos detectando `hook_event_name === 'Stop'` en el JSON de entrada.

### Qué debe quedar al final

- [ ] Parte A: Reporte de Verificación con comandos reales, cobertura ≥80% y URL comprobada en el navegador
- [ ] Parte B: tabla de auditoría (hallazgo / severidad / archivo:línea / acción) con altas y medias corregidas; `npm audit` limpio
- [ ] Parte C: veredicto APROBADO de un revisor con contexto limpio, con evidencia
- [ ] `scripts/hooks/check-tests-quality.js` ejecutable a mano con exit 0 / exit 2 según el estado del árbol
- [ ] Hook registrado en `.claude/settings.json` bajo `Stop` y probado en vivo: el agente no puede terminar sin tests, auditoría y revisión
- [ ] Hook documentado en `docs/CONFIGURACION-PROYECTO.md`


---

## Prompt 8: Gestión documental — specs y wiki autoactualizable (Implementación)

> "La documentación que no se actualiza sola, no se actualiza."
>
> Otra forma de cerrar el loop: al terminar una feature, el agente **deja contexto persistente** (specs, ADRs, API docs,
> índices) que la siguiente sesión lee en vez de redescubrir el código. El bloque tiene cinco pasos, que siguen la diapositiva:
> estructura de `/docs` → skill `doc-update` → wiki autoactualizable → `CLAUDE.md` conciso → ejercicio práctico.
>
> Palancas de Claude Code: `CLAUDE.md` raíz (siempre cargado), `CLAUDE.md` anidados en `apps/backend` y `apps/frontend`
> (se cargan al trabajar dentro), documentos enlazados bajo demanda (`docs/`), specs de OpenSpec (`/opsx archive`),
> `openspec/config.yaml` → `context:`, agentes, y hooks `Stop`/`SessionEnd` + `claude -p` para automatizar.
>
> La skill y el agente `doc-update` **no vienen instalados**: se crean desde `docs/skills/doc-update.md`.

### Paso 1 — Estructura de `/docs`

```
Reorganiza docs/ como wiki del proyecto siguiendo la estructura de docs/skills/doc-update.md:
- docs/README.md como portada e índice
- docs/specs/ (qué debe hacer cada feature), docs/adr/ (decisiones, numeradas), docs/api/ (API por módulo),
  docs/onboarding/ (mueve aquí SETUP.md, CONFIGURACION-PROYECTO.md y TROUBLESHOOTING.md con git mv)
- docs/PROMPTS.md y docs/skills/ se quedan donde están (material del workshop)
Actualiza todas las referencias a los archivos movidos (README.md raíz, CLAUDE.md, skills, agentes) y comprueba con grep que no queda ninguna rota.
No crees documentos vacíos "por rellenar": cada carpeta solo tiene lo que existe de verdad.
```

### Paso 2 — Skill `doc-update`

```
Crea .claude/skills/doc-update/SKILL.md a partir de docs/skills/doc-update.md (desde el frontmatter hasta la sección "Reglas").
Crea también el agente: .claude/agents/doc-update.md con model: sonnet y su copia .github/agents/doc-update.md con
model: claude-sonnet-4.5, usando la definición que hay al final del mismo documento.
Regístralos en CLAUDE.md (tabla de skills y tabla de agentes) con una línea cada uno.
```

### Paso 3 — Wiki autoactualizable

Primero a mano, sobre una feature ya hecha (p. ej. el CRUD de Categorías del Prompt 1):

```
Ejecuta el agente doc-update sobre el módulo de categorías.
Debe generar docs/api/categories.md y docs/specs/categorias.md desde el código real, crear la ADR-0001 con la decisión
de adoptar esta wiki, crear apps/backend/CLAUDE.md y apps/frontend/CLAUDE.md con el índice, y enlazarlo todo desde docs/README.md.
Cuando termine, comprueba tú que cada endpoint de la tabla existe en el controller y que cada enlace abre.
```

Después, que se actualice sola. Dos niveles:

**Nivel 1 — el hook exige la wiki al día** (amplía el hook `Stop` del Prompt 7):

```
Amplía scripts/hooks/check-tests-quality.js: si el diff toca apps/backend/src/{modulo}/ o apps/frontend/app/{pagina}/
y no toca docs/api/{modulo}.md ni docs/specs/ (o el doc no existe), bloquea con el mensaje
"Wiki desincronizada: ejecuta el agente doc-update sobre {modulo}". Exime a los cambios que solo tocan tests.
```

**Nivel 2 — el agente monitoriza los cambios y actualiza la wiki sin intervención** (hook `SessionEnd` + `claude -p`):

```
Crea scripts/hooks/sync-docs.sh que, al terminar la sesión, detecte con git los módulos tocados desde el último commit
que empiece por "docs(" y, si los hay, ejecute en modo no interactivo:
  claude -p "Ejecuta el agente doc-update sobre: [lista]. Solo toca docs/, apps/*/CLAUDE.md, CLAUDE.md y openspec/config.yaml." --allowedTools "Read,Glob,Grep,Write,Edit,Bash(git *),Agent"
Regístralo en .claude/settings.json bajo "SessionEnd" con timeout 300.
El comando no puede tocar código ni hacer commit: deja los cambios en el árbol para revisarlos.
Pruébalo: modifica un service, cierra la sesión y comprueba que docs/api/{modulo}.md se ha actualizado.
```

Variante fuera del repo (demo del ponente): wiki por repositorio en Obsidian sincronizada desde `SessionEnd`, sin escribir
nada dentro del repo y consultada por el agente con una skill de lectura. Misma idea, distinto almacén.

### Paso 4 — `CLAUDE.md` como archivo de contexto maestro

```
Revisa CLAUDE.md como archivo de contexto maestro: debe ser conciso (~200 líneas como máximo: a partir de ahí el agente empieza a ignorarlo) y extremadamente útil. Mide primero cuántas tiene (wc -l CLAUDE.md) y dime qué sobra.
- Añade la sección "Documentation Map" (plantilla en la skill doc-update) y corrige la referencia a docs/specs/.
- Todo lo que sea explicación larga (setup, configuración, troubleshooting) se mueve a docs/onboarding/ y se enlaza.
- Lo que el agente necesita en cada turno (reglas, comandos, estructura, puertos) se queda.
- Rellena el bloque context: de openspec/config.yaml con stack, convenciones y dominio en ≤ 15 líneas.
Muéstrame el diff antes de aplicarlo.
```

### Paso 5 — Ejercicio práctico

```
Ejecuta el agente doc-update sobre todo lo que hemos construido y modificado hoy (git diff main...HEAD --stat).
Al terminar, dame el informe: documentos creados, actualizados, ADRs nuevas y discrepancias entre wiki y código.
```

Y la prueba de que la wiki sirve, en una sesión nueva (`/clear`):

```
Añade el campo "color" (string opcional, hex validado) a las categorías, en backend y frontend.
Antes de abrir ningún archivo de código, dime qué documentación has leído y qué sabes del módulo gracias a ella.
```

Qué observar: el agente debe citar `apps/backend/CLAUDE.md`, `docs/api/categories.md` y la spec antes de tocar código.
Si va directo al código, la wiki no está bien enlazada o el "Documentation Map" no es claro.
Segunda prueba: renombra a mano una ruta del controller sin tocar la wiki y pide "revisa el módulo de categorías
antes de empezar"; debe detectar la discrepancia, corregir la wiki y avisar.

### Qué debe quedar al final

- [ ] `docs/` con README índice, `specs/`, `adr/`, `api/`, `onboarding/`; sin enlaces rotos
- [ ] Skill `doc-update` y agente `doc-update` (ambas copias) creados y registrados en `CLAUDE.md`
- [ ] `docs/api/categories.md`, `docs/specs/categorias.md`, ADR-0001, `apps/backend/CLAUDE.md`, `apps/frontend/CLAUDE.md`
- [ ] `CLAUDE.md` ≤ ~200 líneas con "Documentation Map"; `openspec/config.yaml` con `context:`
- [ ] Hook que bloquea con wiki desincronizada (nivel 1) o la regenera al cerrar sesión (nivel 2)
- [ ] Prueba en sesión nueva: el agente lee la wiki antes que el código y detecta desincronizaciones

---

## Prompt 9: Mejoras al harness — testing, QA, seguridad y RGPD (Bloque 9)

> El "harness" es todo lo que rodea al modelo. En este bloque se refuerza en cinco frentes, siguiendo la diapositiva:
> seguridad → RGPD → permisos del agente → checklist de producción → skill de auditoría.
>
> Riesgos que se atacan: brechas de seguridad (acceso no autorizado, manipulación de datos), incumplimiento normativo
> (RGPD), agentes incontrolados (acciones imprevistas del agente sobre archivos, red o secretos) y fallos en producción.
>
> Material de referencia (documentado, no instalado — el asistente crea las skills): `docs/skills/security-review.md`
> (auditoría de seguridad + sección RGPD), `docs/skills/production-checklist.md`, `docs/skills/code-review.md`.
> Skills ya instaladas que se usan: `api-patterns`, `auth-flow`, `verification-checklist`.

### Paso 1 — Seguridad: endurecer el backend

Sobre el backend tal como esté (con o sin auth implementada):

```
Endurece el backend siguiendo la sección 1-5 de docs/skills/security-review.md. En concreto:

1. Validación de entrada: comprueba que todos los endpoints reciben DTOs con class-validator, que los ids de ruta
   se validan como ObjectId (400, no 500) y que la paginación tiene limit máximo. Corrige lo que falte.
2. Limitación de tasa: añade @nestjs/throttler con un límite global razonable (p. ej. 100 req/min por IP) y uno más
   estricto en los endpoints de autenticación si existen (p. ej. 5 req/min). Configurable por variables de entorno.
3. Cabeceras: añade helmet en main.ts.
4. Caducidad de JWT (si hay auth): access token ≤ 15 min, refresh token rotado y revocable, cookies httpOnly + sameSite.
   Si no hay auth, documenta en docs/onboarding/ qué valores usar cuando se implemente.
5. Gestión de secretos: crea apps/backend/.env.example y apps/frontend/.env.example con todas las variables (sin valores),
   valida al arrancar que las obligatorias existen (falla rápido con mensaje claro), y comprueba con git que ningún .env
   está trackeado.
6. Búsquedas: escapa la entrada antes de construir RegExp.

Para cada cambio: tests unitarios actualizados, `npm run test:cov` en verde, y una línea en docs/onboarding/ explicando
la variable o el límite nuevo. No cambies puertos ni el ValidationPipe global.
```

### Paso 2 — RGPD / GDPR

```
Aplica la sección 8 (RGPD) de docs/skills/security-review.md al proyecto:

1. Inventario: lista qué schemas guardan datos personales y qué campos. Para cada campo, justificación o propuesta de eliminarlo (minimización).
2. Consentimiento: si algún dato no es imprescindible (marketing, analítica), añade al schema un subdocumento
   consents: { [finalidad]: { granted: boolean, at: Date } } y en la UI una casilla sin pre-marcar con enlace a la política de privacidad.
3. Derecho de acceso y borrado: añade GET /api/users/me/export (todos los datos del usuario en JSON) y DELETE /api/users/me
   que borre o anonimice al usuario en TODAS las colecciones donde aparece (incluidos tokens y logs). Si aún no hay usuarios,
   implementa el patrón sobre la entidad que corresponda y documenta cómo se extenderá.
4. Retención: índices TTL (expireAfterSeconds) en colecciones con caducidad.
5. Registros de auditoría: módulo audit-log que registre quién, qué, cuándo y sobre quién en operaciones sensibles
   (login, cambio de rol, export, borrado, acceso admin), sin guardar el contenido del dato. Un método auditService.log()
   llamado desde los services, no desde los controllers.
6. Logs de aplicación: sustituye cualquier console.log por el Logger de NestJS y asegúrate de que no se loguean emails,
   tokens ni bodies.

Tests para export, borrado (verifica que no queda rastro en ninguna colección) y audit-log. Documenta en
docs/onboarding/RGPD.md qué datos se tratan, para qué, cuánto tiempo y cómo ejercer los derechos.
```

### Paso 3 — Permisos del agente

Controlar qué puede hacer Claude Code sobre archivos, red y variables de entorno. Se configura en `.claude/settings.json`
(compartido con el equipo, va en git) y `.claude/settings.local.json` (personal, ignorado). Precedencia: `deny` → `ask` → `allow`.

```
Configura los permisos del agente para este repositorio:

1. Crea .claude/settings.json con:
   {
     "permissions": {
       "deny": [
         "Read(./.env)", "Read(./.env.*)", "Read(./apps/*/.env)", "Read(./apps/*/.env.*)",
         "Read(~/.ssh/**)", "Read(~/.aws/**)",
         "Bash(rm -rf *)", "Bash(git push --force*)", "Bash(git reset --hard*)",
         "Bash(curl * | sh)", "Bash(curl * | bash)",
         "Edit(./.claude/settings.json)"
       ],
       "ask": [
         "Bash(git push *)", "Bash(npm install *)", "Bash(npm uninstall *)",
         "Bash(docker *)", "Edit(./apps/backend/src/main.ts)", "Edit(./package.json)", "Edit(./apps/*/package.json)"
       ],
       "allow": [
         "Bash(npm run *)", "Bash(npx jest *)", "Bash(npx playwright *)", "Bash(git status)", "Bash(git diff *)",
         "Bash(git log *)", "Bash(git add *)", "Bash(git commit *)",
         "Read(./apps/**)", "Read(./docs/**)", "Edit(./apps/**)", "Edit(./docs/**)",
         "WebFetch(domain:docs.nestjs.com)", "WebFetch(domain:nextjs.org)", "WebFetch(domain:mongoosejs.com)"
       ],
       "disableBypassPermissionsMode": true
     }
   }
   Ajusta los patrones a lo que realmente usa el proyecto. Explícame qué hace cada bloque.

2. Sandbox (macOS/Linux): añade al mismo archivo
   "sandbox": {
     "enabled": true,
     "network": { "allowedDomains": ["registry.npmjs.org", "github.com", "localhost"] },
     "credentials": { "envVars": [ { "name": "JWT_SECRET", "mode": "deny" }, { "name": "MONGODB_URI", "mode": "deny" } ] }
   }
   y explícame la diferencia entre lo que bloquean las reglas de permisos (herramientas de Claude Code) y lo que bloquea el
   sandbox (cualquier proceso hijo a nivel de sistema operativo).

3. Pruébalo tú mismo y dime qué pasa en cada caso: intenta leer apps/backend/.env; intenta `cat apps/backend/.env` por Bash;
   intenta `git push`; intenta hacer una petición a un dominio no permitido; intenta editar .claude/settings.json.

4. Documenta en docs/onboarding/PERMISOS-AGENTE.md: qué puede hacer el agente sin preguntar, qué pide confirmación,
   qué está prohibido, dónde lo cambia cada persona (settings.local.json) y cómo verlo en vivo (/permissions, /sandbox, /status).
```

Opcional, para enseñar el bloqueo dinámico: un hook `PreToolUse` con `matcher: "Bash"` que inspeccione el comando
(`tool_input.command` del JSON por stdin) y salga con `exit 2` + motivo en stderr para denegar, por ejemplo cualquier
comando que contenga `mongosh` contra una URI que no sea `localhost`.

### Paso 4 — Checklist de producción

```
Crea .claude/skills/production-checklist/SKILL.md a partir de docs/skills/production-checklist.md (conserva el frontmatter,
quita la nota inicial) y regístrala en CLAUDE.md.

Después recórrela entera sobre el proyecto tal como está, como si fuéramos a desplegar mañana: cada punto con evidencia
(comando ejecutado y su salida, archivo y línea, o "no aplica" justificado). Entrega el informe "Production readiness"
de la skill, con bloqueantes y veredicto. No corrijas nada todavía: primero quiero ver la foto completa.
```

Y con el informe delante:

```
Corrige los bloqueantes del informe en orden de severidad. Para cada uno: cambio, test que lo cubre, y vuelve a marcar
el punto del checklist con la evidencia nueva. Los que necesiten decisión humana (proveedor de hosting, dominio,
política de backups), déjalos listados con las opciones y tu recomendación.
```

### Paso 5 — Skill de auditoría

Si no se creó en el Prompt 7 (Paso 0):

```
Crea .claude/skills/security-review/SKILL.md a partir de docs/skills/security-review.md (frontmatter incluido, sin la nota
inicial) y regístrala en CLAUDE.md.
```

Ejercicio: auto-auditoría de todo el proyecto.

```
Ejecuta la skill security-review sobre TODO el código de apps/backend y apps/frontend (no solo el diff), incluida la
sección RGPD. Entrega la tabla de hallazgos con severidad, archivo:línea y acción, más el resultado de las comprobaciones
automáticas. Corrige los altos y medios, vuelve a ejecutar los tests y repite la auditoría hasta que no queden altos ni medios.
```

Demostración para cerrar el bloque: introducir a propósito una vulnerabilidad (p. ej. un endpoint que devuelve el documento
crudo del usuario con `passwordHash`, o un `find({ nombre: req.query.nombre })` sin DTO) y pedir "cierra el loop" — la
auditoría del Prompt 7 debe detectarla y el hook `Stop` impedir terminar hasta corregirla.

### Qué debe quedar al final

- [ ] Backend con throttler, helmet, validación de ObjectId, `.env.example` en ambos apps y validación de variables al arrancar
- [ ] Endpoints de exportación y borrado de datos personales, consentimiento con fecha, índices TTL y módulo audit-log, con tests
- [ ] `docs/onboarding/RGPD.md` y `docs/onboarding/PERMISOS-AGENTE.md`
- [ ] `.claude/settings.json` con `deny`/`ask`/`allow` y sandbox, probado caso por caso
- [ ] Skill `production-checklist` creada y el informe "Production readiness" con veredicto y bloqueantes corregidos
- [ ] Skill `security-review` creada y auditoría completa del proyecto sin hallazgos altos ni medios
