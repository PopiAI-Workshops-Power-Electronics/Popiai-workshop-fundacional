---
name: gestion-servicios
description: "Gestiona los servicios del proyecto Workshop PopiAI: MongoDB, API backend, Web frontend. Permite iniciar, detener, reiniciar, verificar el estado o ver logs de los servicios. Usa esta skill cuando el usuario pida iniciar, detener, reiniciar, ver el estado, o ver logs de MongoDB, la API o el frontend."
license: MIT
---

# Gestion de Servicios

Esta skill facilita la gestion de todos los servicios del proyecto Workshop PopiAI.

## Instrucciones

Identifica la accion solicitada (iniciar, detener, reiniciar, verificar estado, o ver logs) y el servicio objetivo (mongodb, api, web, o todos) y ejecuta las acciones correspondientes.

### Acciones Disponibles

#### 1. Iniciar servicios

**Pasos:**
- **mongodb**: `docker compose up -d`
- **api**: `npm run start:backend` (en background)
- **web**: `npm run start:frontend` (en background)
- **todo**: Iniciar MongoDB primero, luego API y Web

#### 2. Detener servicios

**Pasos:**
- **mongodb**: `docker compose down`
- **api**: Matar proceso en puerto 3001
- **web**: Matar proceso en puerto 3000
- **todo**: Detener todos los servicios

#### 3. Reiniciar servicios

**Pasos:**
- Detener el servicio especificado
- Esperar 2 segundos
- Iniciar el servicio nuevamente

#### 4. Verificar estado

**Verificar:**
- **MongoDB**: `docker compose ps` - deberia mostrar mongo running
- **API**: Verificar si proceso escucha en puerto 3001: `lsof -i :3001`
- **Web**: Verificar si proceso escucha en puerto 3000: `lsof -i :3000`

Mostrar un resumen al usuario:
```
Estado de servicios Workshop:
- MongoDB: Running (puerto 27017)
- API: Running (http://localhost:3001)
- Web: Running (http://localhost:3000)
```

#### 5. Ver logs

**Comandos:**
- **mongodb**: `docker compose logs -f mongo`
- **api**: Mostrar logs del proceso de API
- **web**: Mostrar logs del proceso de Web

### Comportamiento por Defecto

Si el usuario pide gestionar servicios sin especificar accion:
1. Mostrar el estado actual de todos los servicios
2. Preguntar que accion quiere realizar
3. Ofrecer opciones: iniciar, detener, reiniciar, ver logs

### Manejo de Errores

- Si MongoDB no esta corriendo y el usuario intenta iniciar API, iniciarlo automaticamente primero
- Si un puerto esta ocupado (3001 o 3000), informar al usuario y ofrecer matar el proceso
- Si Docker no esta corriendo, informar que debe iniciar Docker Desktop

### Verificaciones de Salud

Despues de iniciar servicios, verificar que esten respondiendo:
- **API**: `curl http://localhost:3001/api`
- **Web**: `curl http://localhost:3000`
- **MongoDB**: Verificar conexion mediante Docker

### Puertos del Proyecto Workshop

| Servicio | Puerto | URL |
|----------|--------|-----|
| API (NestJS) | 3001 | http://localhost:3001 |
| Web (Next.js) | 3000 | http://localhost:3000 |
| MongoDB | 27017 | mongodb://localhost:27017 |

### Variables de entorno importantes

- `MONGODB_URI` - Conexion a MongoDB
