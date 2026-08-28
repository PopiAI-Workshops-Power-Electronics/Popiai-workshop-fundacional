#!/usr/bin/env python3
"""
PopiAI Workshop — Verificación del entorno

Equivalente multiplataforma de scripts/verify.sh:
  1. Node.js v20+
  2. Docker instalado
  3. Contenedor MongoDB corriendo y respondiendo
  4. Backend respondiendo en http://localhost:3001/api/health
  5. Frontend compila (tsc --noEmit)

Uso (Windows, Linux o macOS — solo necesita Python 3.8+, sin dependencias):
  python scripts/verify.py      (Windows)
  python3 scripts/verify.py     (Linux / macOS)

Sale con código 1 si hay errores (los avisos ⚠️ no cuentan como error).
"""

import json
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import List, Optional

IS_WIN = sys.platform.startswith("win")
ROOT = Path(__file__).resolve().parent.parent
MONGO_CONTAINER = "workshop-mongodb"
HEALTH_URL = "http://localhost:3001/api/health"
REQUIRED_NODE_MAJOR = 20

if IS_WIN:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def output(cmd: str, args: List[str], cwd: Optional[Path] = None) -> Optional[str]:
    """Ejecuta un comando y devuelve su stdout, o None si no existe/falla."""
    path = shutil.which(cmd)
    if path is None:
        return None
    try:
        return subprocess.run(
            [path] + args,
            cwd=cwd or ROOT,
            capture_output=True,
            text=True,
            check=True,
            shell=False,
        ).stdout.strip()
    except (subprocess.CalledProcessError, OSError):
        return None


def main() -> int:
    print("🔍 PopiAI Workshop — Verificación del entorno")
    print("===============================================")

    errors = 0
    sep = "\\" if IS_WIN else "/"

    # 1. Node.js v20+
    print()
    print("1. Node.js...")
    node_version = output("node", ["--version"])
    if node_version is None:
        print("   ❌ Node.js no encontrado")
        errors += 1
    else:
        try:
            major = int(node_version.lstrip("v").split(".")[0])
        except ValueError:
            major = 0
        if major >= REQUIRED_NODE_MAJOR:
            print(f"   ✅ {node_version}")
        else:
            print(f"   ❌ Node.js {node_version} — se requiere v{REQUIRED_NODE_MAJOR}+")
            errors += 1

    # 2. Docker
    print()
    print("2. Docker...")
    docker_version = output("docker", ["--version"])
    if docker_version is None:
        print("   ❌ Docker no encontrado")
        errors += 1
    else:
        parts = docker_version.split()
        version = parts[2].rstrip(",") if len(parts) > 2 else docker_version
        print(f"   ✅ Docker {version}")

    # 3. MongoDB corriendo
    print()
    print("3. MongoDB (Docker)...")
    names = output("docker", ["ps", "--format", "{{.Names}}"]) or ""
    if MONGO_CONTAINER in names.splitlines():
        ping = output("docker", ["exec", MONGO_CONTAINER, "mongosh", "--eval", "db.adminCommand('ping')"])
        if ping is not None:
            print("   ✅ MongoDB corriendo y respondiendo")
        else:
            print("   ⚠️  Contenedor existe pero MongoDB no responde aún")
    else:
        print(f"   ❌ Contenedor {MONGO_CONTAINER} no está corriendo")
        print("      Ejecuta: docker compose up -d")
        errors += 1

    # 4. Backend /api/health
    print()
    print(f"4. Backend ({HEALTH_URL})...")
    try:
        with urllib.request.urlopen(HEALTH_URL, timeout=3) as resp:
            body = resp.read().decode("utf-8", errors="replace")
        try:
            status_ok = json.loads(body).get("status") == "ok"
        except (ValueError, AttributeError):
            status_ok = False
        if status_ok:
            print(f"   ✅ Backend respondiendo: {body}")
        else:
            print(f"   ⚠️  Backend responde pero sin status ok: {body}")
    except (urllib.error.URLError, OSError, ValueError):
        print(f"   ⚠️  Backend no responde (¿está corriendo? cd apps{sep}backend && npm run start:dev)")

    # 5. Frontend compila
    print()
    print("5. Frontend (compilación TypeScript)...")
    frontend = ROOT / "apps" / "frontend"
    if frontend.is_dir():
        if output("npx", ["tsc", "--noEmit"], cwd=frontend) is not None:
            print("   ✅ TypeScript compila sin errores")
        else:
            print(f"   ⚠️  Errores de TypeScript (ejecuta 'npx tsc --noEmit' en apps{sep}frontend para verlos)")
    else:
        print(f"   ❌ Directorio apps{sep}frontend no encontrado")
        errors += 1

    # Resultado
    print()
    print("===============================================")
    if errors == 0:
        print("✅ Todo listo para el workshop!")
    else:
        print(f"❌ {errors} problema(s) encontrado(s). Ver TROUBLESHOOTING.md")
    return 1 if errors else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print()
        sys.exit(130)
