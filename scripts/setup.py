#!/usr/bin/env python3
"""
PopiAI Workshop — Setup automático

Equivalente multiplataforma de scripts/setup.sh:
  1. Verifica que Node.js está instalado
  2. Instala las dependencias (npm install)
  3. Levanta MongoDB con Docker Compose
  4. Espera a que MongoDB responda

Uso (Windows, Linux o macOS — solo necesita Python 3.8+, sin dependencias):
  python scripts/setup.py       (Windows)
  python3 scripts/setup.py      (Linux / macOS)

Sale con código 1 si algún paso falla.
"""

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Optional

IS_WIN = sys.platform.startswith("win")
ROOT = Path(__file__).resolve().parent.parent
MONGO_CONTAINER = "workshop-mongodb"
MAX_RETRIES = 30
RETRY_DELAY_S = 2

if IS_WIN:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def which(cmd: str) -> Optional[str]:
    return shutil.which(cmd)


def run(cmd: str, args: List[str], quiet: bool = False) -> int:
    """Ejecuta un comando en la raíz del repo y devuelve su código de salida."""
    path = which(cmd)
    if path is None:
        return 127
    try:
        return subprocess.run(
            [path] + args,
            cwd=ROOT,
            stdout=subprocess.DEVNULL if quiet else None,
            stderr=subprocess.DEVNULL if quiet else None,
            shell=False,
        ).returncode
    except OSError:
        return 1


def output(cmd: str, args: List[str]) -> Optional[str]:
    path = which(cmd)
    if path is None:
        return None
    try:
        return subprocess.run(
            [path] + args, capture_output=True, text=True, check=True, shell=False
        ).stdout.strip()
    except (subprocess.CalledProcessError, OSError):
        return None


def fail(msg: str) -> int:
    print(f"❌ {msg}")
    return 1


def main() -> int:
    print("🚀 PopiAI Workshop — Setup automático")
    print("======================================")

    # Verificar Node.js
    print()
    print("📦 Verificando Node.js...")
    node_version = output("node", ["--version"])
    if node_version is None:
        return fail("Node.js no encontrado. Instala Node v20 desde https://nodejs.org o con: nvm install 20")
    print(f"✅ Node.js {node_version}")

    # Instalar dependencias
    print()
    print("📦 Instalando dependencias...")
    if run("npm", ["install"]) != 0:
        return fail("npm install falló")
    print("✅ Dependencias instaladas")

    # Levantar Docker
    print()
    print("🐳 Levantando MongoDB con Docker...")
    if which("docker") is None:
        return fail("Docker no encontrado. Instala Docker Desktop.")

    if run("docker", ["compose", "up", "-d"]) != 0:
        return fail("docker compose up falló (¿está arrancado Docker Desktop?)")
    print("✅ MongoDB iniciado")

    # Esperar a MongoDB
    print()
    print("⏳ Esperando a que MongoDB esté listo...")
    ping = ["exec", MONGO_CONTAINER, "mongosh", "--eval", "db.adminCommand('ping')"]
    retries = 0
    while run("docker", ping, quiet=True) != 0:
        retries += 1
        if retries >= MAX_RETRIES:
            return fail(f"MongoDB no respondió después de {MAX_RETRIES} intentos")
        print(f"  Intento {retries}/{MAX_RETRIES}...")
        time.sleep(RETRY_DELAY_S)
    print("✅ MongoDB listo")

    sep = "\\" if IS_WIN else "/"
    print()
    print("======================================")
    print("✅ Setup completado exitosamente!")
    print()
    print("Próximos pasos:")
    print(f"  cd apps{sep}backend && npm run start:dev")
    print(f"  cd apps{sep}frontend && npm run dev  (otra terminal)")
    print()
    py = "python" if IS_WIN else "python3"
    print(f"Verifica el setup con: {py} scripts{sep}verify.py")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print()
        sys.exit(130)
