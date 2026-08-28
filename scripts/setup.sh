#!/usr/bin/env bash
set -e

echo "🚀 PopiAI Workshop — Setup automático"
echo "======================================"

# Verificar Node.js
echo ""
echo "📦 Verificando Node.js..."
NODE_VERSION=$(node --version 2>/dev/null || echo "none")
if [[ "$NODE_VERSION" == "none" ]]; then
  echo "❌ Node.js no encontrado. Instala Node v20 con: nvm install 20"
  exit 1
fi
echo "✅ Node.js $NODE_VERSION"

# Instalar dependencias
echo ""
echo "📦 Instalando dependencias..."
npm install
echo "✅ Dependencias instaladas"

# Levantar Docker
echo ""
echo "🐳 Levantando MongoDB con Docker..."
if ! command -v docker &> /dev/null; then
  echo "❌ Docker no encontrado. Instala Docker Desktop."
  exit 1
fi

docker-compose up -d
echo "✅ MongoDB iniciado"

# Esperar a MongoDB
echo ""
echo "⏳ Esperando a que MongoDB esté listo..."
MAX_RETRIES=30
RETRIES=0
until docker exec workshop-mongodb mongosh --eval "db.adminCommand('ping')" &> /dev/null; do
  RETRIES=$((RETRIES + 1))
  if [ $RETRIES -ge $MAX_RETRIES ]; then
    echo "❌ MongoDB no respondió después de ${MAX_RETRIES} intentos"
    exit 1
  fi
  echo "  Intento $RETRIES/$MAX_RETRIES..."
  sleep 2
done
echo "✅ MongoDB listo"

echo ""
echo "======================================"
echo "✅ Setup completado exitosamente!"
echo ""
echo "Próximos pasos:"
echo "  cd apps/backend && npm run start:dev"
echo "  cd apps/frontend && npm run dev  (otra terminal)"
echo ""
echo "Verifica el setup con: ./scripts/verify.sh"
