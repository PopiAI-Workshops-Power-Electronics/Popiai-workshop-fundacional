---
name: verification-checklist
description: Unified completion criteria for backend and frontend — lint, build, test, and browser verification checklists. Use before considering any task complete.
---

# Verification Checklist - Workshop

Criterios de finalizacion unificados para backend y frontend. Una tarea NO esta completa hasta pasar TODAS las verificaciones de su seccion.

## Backend Verification

Ejecutar en orden. Si alguno falla, corregir antes de continuar.

### 1. Linting
```bash
cd apps/backend && npm run lint
```
- DEBE pasar sin errores

### 2. Compilacion TypeScript
```bash
cd apps/backend && npm run build
```
- DEBE compilar sin errores

### 3. Tests
```bash
cd apps/backend && npm run test
```
- TODOS los tests DEBEN pasar

### 4. Arranque de la Aplicacion
```bash
npm run start:backend
```
- La aplicacion DEBE arrancar sin errores
- El servidor DEBE responder en http://localhost:3001

### 5. Verificacion Manual
```bash
curl http://localhost:3001/[endpoint]
```
- Los endpoints implementados DEBEN responder correctamente

### Backend Checklist
```
[ ] cd apps/backend && npm run lint → Sin errores
[ ] cd apps/backend && npm run build → Compilacion exitosa
[ ] cd apps/backend && npm run test → Todos los tests pasan
[ ] npm run start:backend → Arranca sin errores
[ ] Endpoint testeado con curl
[ ] Codigo committed a la rama
```

---

## Frontend Verification

Ejecutar en orden. Si alguno falla, corregir antes de continuar.

### 1. Linting
```bash
cd apps/frontend && npm run lint
```
- DEBE terminar sin errores

### 2. Build
```bash
cd apps/frontend && npm run build
```
- DEBE compilar sin errores de TypeScript
- DEBE generar el build de Next.js exitosamente

### 3. Servidor de Desarrollo
```bash
npm run start:frontend
```
- El servidor DEBE arrancar sin errores
- http://localhost:3000 DEBE responder

### 4. Verificacion en Navegador (OBLIGATORIO)

1. **Abrir la pagina**: `http://localhost:3000/[ruta]`
2. **DevTools (F12)**: Consola limpia, sin errores rojos ni warnings de React
3. **Renderizado**: Componentes se muestran, estilos aplicados, layout correcto
4. **Funcionalidad**: Clicks, forms, navegacion, modals funcionan
5. **Network tab**: Llamadas API responden correctamente (200, 201)
6. **Responsive** (si aplica): Verificar en viewport mobile
7. **Dark mode** (si aplica): Verificar que estilos cambian

### Frontend Checklist
```
[ ] cd apps/frontend && npm run lint → Sin errores
[ ] cd apps/frontend && npm run build → Compilacion exitosa
[ ] npm run start:frontend → Servidor arranca
[ ] Pagina abierta en http://localhost:3000/[ruta]
[ ] DevTools (F12) → Consola limpia
[ ] Pagina renderiza correctamente
[ ] Funcionalidad interactiva probada
[ ] Llamadas API funcionan (Network tab)
[ ] Responsive verificado (si aplica)
[ ] Dark mode funciona (si aplica)
[ ] Codigo committed a la rama
```

---

## Reporte de Verificacion

Al completar una tarea, incluir este formato:

```markdown
## Verificacion Completada

1. Linting: [resultado]
2. Build: [resultado]
3. Tests: [resultado] (solo backend)
4. Dev server: [resultado]
5. Navegador: [URL probada] (solo frontend)
6. Consola: [resultado] (solo frontend)
7. Funcionalidad probada:
   - [Listar cada interaccion]
8. Network: [resultado] (solo frontend)
9. Git: Committed a [rama]
```

## Reglas

1. **NO declarar tarea completada** sin pasar TODAS las verificaciones
2. **NO asumir que funciona** porque el codigo compila
3. **SI hay errores**: corregir y repetir todo el proceso
4. **Documentar resultados** de la verificacion en el output
