# Configuracion por Proyecto

Este documento explica que necesitas personalizar cuando uses este proyecto base como punto de partida para un nuevo proyecto.

## 1. Identidad Visual (Brand)

El workshop incluye una identidad visual por defecto que puedes personalizar completamente.

### Archivos a modificar

| Archivo | Que contiene |
|---------|-------------|
| `.claude/skills/brand-design/SKILL.md` | Reglas de marca: colores, tipografia, tokens, patrones de componentes, anti-patrones |
| `.claude/skills/design-guidelines/SKILL.md` | Referencia completa: paleta, tipografia, estructura de paginas |
| `apps/frontend/app/globals.css` | Variables CSS del tema (`@theme inline`) |

### Valores por defecto

| Token | Color | Hex |
|-------|-------|-----|
| Primary | Teal | `#14B8A6` |
| Primary Hover | Teal dark | `#0D9488` |
| Primary Soft | Teal light | `#F0FDFA` |
| Accent | Amber | `#F59E0B` |
| Error | Rose | `#F43F5E` |
| Success | Emerald | `#10B981` |
| Foreground | Slate 900 | `#0F172A` |
| Body | Slate 600 | `#475569` |
| Border | Slate 200 | `#E2E8F0` |
| Surface Alt | Slate 50 | `#F8FAFC` |
| Background | White | `#FFFFFF` |

**Tipografia:** Inter (via `next/font/google`)
**Escala de grises:** Slate (no gray, no zinc)
**Modo:** Light only (no dark mode)

### Como personalizar

1. Edita `globals.css` — cambia los valores hex en `@theme inline { }`
2. Edita `brand-design/SKILL.md` — actualiza las reglas para que los agentes respeten tu nueva marca
3. Edita `design-guidelines/SKILL.md` — actualiza la referencia visual completa

## 2. Autenticacion

### Estado actual: Sin autenticacion activa

Los endpoints del backend son publicos por defecto. Sin embargo, la skill de `auth-flow` ya esta incluida con el patron de Firebase Auth listo para usar.

### Para activar Firebase Auth

1. **Backend**: Instalar Firebase Admin SDK
   ```bash
   cd apps/backend && npm install firebase-admin
   ```

2. **Crear guards** siguiendo el patron de `.claude/skills/auth-flow/SKILL.md`:
   - `FirebaseAuthGuard` — valida el token de Firebase
   - `IsActiveGuard` — verifica que el usuario esta activo en DB
   - Decorador `@AllowAnonymous()` para endpoints publicos

3. **Frontend**: Instalar Firebase Web SDK
   ```bash
   cd apps/frontend && npm install firebase
   ```

4. **Variables de entorno** necesarias:
   ```
   # apps/backend/.env
   FIREBASE_PROJECT_ID=your-project-id
   FIREBASE_PRIVATE_KEY=your-private-key
   FIREBASE_CLIENT_EMAIL=your-client-email

   # apps/frontend/.env.local
   NEXT_PUBLIC_FIREBASE_API_KEY=your-api-key
   NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-auth-domain
   NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
   ```

5. **Actualizar agentes**: Los agentes ya incluyen patrones de Firebase Auth en sus templates de controllers. Solo necesitas que los guards existan en el codigo.

### Alternativa: JWT con Passport

Si prefieres no usar Firebase:
1. Instala `@nestjs/passport` y `passport-jwt`
2. Crea un `JwtAuthGuard` similar al patron de `FirebaseAuthGuard`
3. Actualiza la skill `auth-flow/SKILL.md` con tus patrones

## 3. Variables de Entorno

### Backend (`apps/backend/.env`)

| Variable | Default | Descripcion |
|----------|---------|-------------|
| `MONGODB_URI` | `mongodb://localhost:27017/workshop` | URI de conexion MongoDB |
| `PORT` | `3001` | Puerto del backend |

### Frontend (`apps/frontend/.env.local`)

| Variable | Default | Descripcion |
|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | `http://localhost:3001/api` | URL base de la API |

### Agregar nuevas variables

- Backend: Agrega en `.env` y accede via `@nestjs/config` (`ConfigService.get('VAR_NAME')`)
- Frontend: Prefija con `NEXT_PUBLIC_` para que sean accesibles en el cliente

## 4. Puertos y URLs

| Servicio | Puerto Default | URL |
|----------|---------------|-----|
| Backend (NestJS) | 3001 | http://localhost:3001/api |
| Frontend (Next.js) | 3000 | http://localhost:3000 |
| MongoDB | 27017 | mongodb://localhost:27017/workshop |

### Para cambiar puertos

- **Backend**: Cambia `PORT` en `apps/backend/.env`
- **Frontend**: Usa `next dev -p XXXX` o agrega `"dev": "next dev -p XXXX"` al package.json
- **MongoDB**: Cambia el puerto en `docker-compose.yml` y actualiza `MONGODB_URI`
- **Agentes/Skills**: Busca y reemplaza los puertos en `.claude/agents/`, `.github/agents/`, `.claude/skills/`, `.claude/commands/`

## 5. Nombre del Proyecto

Si quieres cambiar el nombre del proyecto de "Workshop PopiAI", actualiza estos archivos:

| Archivo | Que cambiar |
|---------|-------------|
| `package.json` (root) | Campo `name` |
| `apps/backend/package.json` | Campo `name` |
| `apps/frontend/package.json` | Campo `name` |
| `CLAUDE.md` | Titulo y descripcion del proyecto |
| `apps/frontend/app/layout.tsx` | Metadata title y texto del header |
| `.claude/agents/*.md` y `.github/agents/*.md` | Descripcion del proyecto en cada agente (recuerda actualizar ambas copias) |

## 6. Base de Datos

### Actual: MongoDB local via Docker

```bash
docker-compose up -d    # Inicia MongoDB
docker-compose down     # Para MongoDB
```

Contenedor: `workshop-mongodb`, datos persistidos en volumen `mongodb_data`.

### Para MongoDB Atlas (produccion)

1. Crea un cluster en [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Obtiene la URI de conexion
3. Actualiza `MONGODB_URI` en `apps/backend/.env`:
   ```
   MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/workshop
   ```
4. Ya no necesitas Docker para MongoDB local

## 7. Deploy

### Actual: Local only

El proyecto esta configurado para desarrollo local. No hay CI/CD ni deploy automatico.

### Opciones de produccion

**Vercel (frontend) + Railway/Render (backend):**
- Frontend: Conecta el repo a Vercel, configura el root directory como `apps/frontend`
- Backend: Deploy en Railway o Render como servicio Node.js

**Docker Compose (fullstack):**
- Agrega un Dockerfile para el backend
- Usa el `docker-compose.yml` existente como base
- Agrega servicio de frontend con `next start`

**Solo necesitas:**
- Configurar variables de entorno en el proveedor
- Actualizar `NEXT_PUBLIC_API_URL` para apuntar al backend en produccion
- Configurar CORS en el backend para el dominio de produccion
