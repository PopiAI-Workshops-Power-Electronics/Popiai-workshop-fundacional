# Troubleshooting — PopiAI Workshop

## Problemas comunes y soluciones

---

### ❌ Error: `Cannot find module '@nestjs/core'`

**Causa:** Las dependencias no están instaladas.

**Solución:**
```bash
cd apps/backend
npm install
```

---

### ❌ Error: MongoDB connection failed

**Causa:** MongoDB no está corriendo.

**Solución:**
```bash
# Verificar estado del contenedor
docker ps

# Si no está corriendo:
docker-compose up -d

# Verificar logs de MongoDB
docker logs workshop-mongodb
```

Si Docker Desktop no está iniciado, ábrelo primero.

---

### ❌ Error: `Port 3001 already in use`

**Causa:** Otro proceso está usando el puerto 3001.

**Solución:**
```bash
# Encontrar el proceso
lsof -i :3001

# Matar el proceso (reemplaza PID)
kill -9 <PID>
```

---

### ❌ Error: `Port 3000 already in use`

```bash
lsof -i :3000
kill -9 <PID>
```

---

### ❌ CORS error en el browser

**Causa:** El backend no tiene CORS configurado para localhost:3000.

**Verificar:** En `apps/backend/src/main.ts`, confirma que `enableCors` apunta a `http://localhost:3000`.

---

### ❌ Error: `node: command not found` o versión incorrecta

**Solución:**
```bash
nvm install 20
nvm use
node --version  # debe ser v20.x.x
```

---

### ❌ Frontend no compila: error de TypeScript

**Causa:** Tipos incompatibles o módulos faltantes.

**Solución:**
```bash
cd apps/frontend
npm install
npm run build
```

---

### ❌ `docker-compose: command not found`

**En macOS con Docker Desktop:** Docker Compose v2 viene integrado como `docker compose` (sin guión):
```bash
docker compose up -d
```

---

### ❌ MongoDB no persiste datos entre reinicios

**Causa:** El volumen de Docker no está configurado correctamente.

**Verificar:** El `docker-compose.yml` debe tener el volumen `mongodb_data` definido.

**Solución:**
```bash
docker-compose down
docker volume rm popi-workshop-base_mongodb_data
docker-compose up -d
```

---

## ¿Nada funciona?

1. Reinstala todo desde cero:
```bash
docker-compose down -v
rm -rf node_modules apps/backend/node_modules apps/frontend/node_modules
npm install
docker-compose up -d
```

2. Contacta al instructor con el output de `./scripts/verify.sh` (Linux/macOS) o `python scripts/verify.py` (Windows).
