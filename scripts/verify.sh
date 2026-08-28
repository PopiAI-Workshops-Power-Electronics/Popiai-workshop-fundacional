#!/usr/bin/env bash

echo "🔍 PopiAI Workshop — Verificación del entorno"
echo "==============================================="

ERRORS=0

# 1. Verificar Node.js v20+
echo ""
echo "1. Node.js..."
NODE_VERSION=$(node --version 2>/dev/null || echo "none")
if [[ "$NODE_VERSION" == "none" ]]; then
  echo "   ❌ Node.js no encontrado"
  ERRORS=$((ERRORS + 1))
else
  MAJOR=$(echo "$NODE_VERSION" | sed 's/v//' | cut -d. -f1)
  if [ "$MAJOR" -ge 20 ]; then
    echo "   ✅ $NODE_VERSION"
  else
    echo "   ❌ Node.js $NODE_VERSION — se requiere v20+"
    ERRORS=$((ERRORS + 1))
  fi
fi

# 2. Verificar Docker
echo ""
echo "2. Docker..."
if ! command -v docker &> /dev/null; then
  echo "   ❌ Docker no encontrado"
  ERRORS=$((ERRORS + 1))
else
  echo "   ✅ Docker $(docker --version | cut -d' ' -f3 | tr -d ',')"
fi

# 3. Verificar MongoDB corriendo
echo ""
echo "3. MongoDB (Docker)..."
if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "workshop-mongodb"; then
  if docker exec workshop-mongodb mongosh --eval "db.adminCommand('ping')" &>/dev/null; then
    echo "   ✅ MongoDB corriendo y respondiendo"
  else
    echo "   ⚠️  Contenedor existe pero MongoDB no responde aún"
  fi
else
  echo "   ❌ Contenedor workshop-mongodb no está corriendo"
  echo "      Ejecuta: docker-compose up -d"
  ERRORS=$((ERRORS + 1))
fi

# 4. Verificar backend /api/health
echo ""
echo "4. Backend (http://localhost:3001/api/health)..."
HEALTH=$(curl -s --connect-timeout 3 http://localhost:3001/api/health 2>/dev/null || echo "error")
if echo "$HEALTH" | grep -q '"status":"ok"'; then
  echo "   ✅ Backend respondiendo: $HEALTH"
else
  echo "   ⚠️  Backend no responde (¿está corriendo? cd apps/backend && npm run start:dev)"
fi

# 5. Verificar frontend compila
echo ""
echo "5. Frontend (compilación TypeScript)..."
if [ -d "apps/frontend" ]; then
  cd apps/frontend
  if npx tsc --noEmit 2>/dev/null; then
    echo "   ✅ TypeScript compila sin errores"
  else
    echo "   ⚠️  Errores de TypeScript (ver output de tsc)"
  fi
  cd ../..
else
  echo "   ❌ Directorio apps/frontend no encontrado"
  ERRORS=$((ERRORS + 1))
fi

# Resultado
echo ""
echo "==============================================="
if [ $ERRORS -eq 0 ]; then
  echo "✅ Todo listo para el workshop!"
else
  echo "❌ $ERRORS problema(s) encontrado(s). Ver TROUBLESHOOTING.md"
fi
