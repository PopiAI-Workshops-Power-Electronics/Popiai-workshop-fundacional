#!/usr/bin/env python3
"""
PopiAI Workshop — Comprobación de requisitos del equipo

Verifica lo descrito en "Requisitos de sala y setup":
  1. Acceso HTTPS a los dominios usados durante el workshop
  2. Software instalado: Git, Node.js 20 LTS (+ npm), Docker + Docker Compose
  3. Al menos una herramienta de IA disponible: Claude Code, GitHub Copilot CLI o Codex

Uso (Windows, Linux o macOS — solo necesita Python 3.8+, sin dependencias):
  python scripts/check-requirements.py      (Windows)
  python3 scripts/check-requirements.py     (Linux / macOS)

Sale con código 1 si falla algún requisito obligatorio.
"""

import http.client
import os
import platform
import shutil
import socket
import ssl
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, List, Optional, Tuple

IS_WIN = sys.platform.startswith("win")
REQUIRED_NODE_MAJOR = 20
TIMEOUT_S = 8

# ---------------------------------------------------------------------------
# Definición de requisitos
# ---------------------------------------------------------------------------

DOMAINS: List[Tuple[str, str]] = [
    ("github.com", "clonar el material del workshop"),
    ("raw.githubusercontent.com", "contenido de GitHub (*.githubusercontent.com)"),
    ("api.anthropic.com", "API de Claude"),
    ("claude.ai", "herramienta de IA"),
    ("registry.npmjs.org", "dependencias npm"),
    ("nodejs.org", "Node.js"),
    ("hub.docker.com", "imagen de la base de datos"),
    ("registry-1.docker.io", "registro Docker (*.docker.io)"),
    ("api.x.ai", "API usada en los ejercicios del día 2"),
    ("cdn.rebrickable.com", "imágenes usadas en los ejercicios del día 2"),
]


def validate_node(out: str) -> Optional[str]:
    try:
        major = int(out.lstrip("v").split(".")[0])
    except ValueError:
        return f"versión no reconocida: {out}"
    if major < REQUIRED_NODE_MAJOR:
        return f"se requiere Node.js {REQUIRED_NODE_MAJOR}+ (tienes {out})"
    return None


# (nombre, comando, args, pista de instalación, validador opcional)
SOFTWARE: List[Tuple[str, str, List[str], str, Optional[Callable[[str], Optional[str]]]]] = [
    ("Git", "git", ["--version"], "https://git-scm.com/downloads", None),
    ("Node.js", "node", ["--version"], f"https://nodejs.org (versión {REQUIRED_NODE_MAJOR} LTS)", validate_node),
    ("npm", "npm", ["--version"], "viene incluido con Node.js", None),
    ("Docker", "docker", ["--version"], "https://docs.docker.com/get-docker/", None),
    ("Docker Compose", "docker", ["compose", "version"],
     "incluido en Docker Desktop; en Linux instala el plugin docker-compose-plugin", None),
]

AI_TOOLS: List[Tuple[str, str, List[str]]] = [
    ("Claude Code", "claude", ["--version"]),
    ("GitHub Copilot CLI", "copilot", ["--version"]),
    ("Codex CLI", "codex", ["--version"]),
]

# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

USE_COLOR = sys.stdout.isatty() and not os.environ.get("NO_COLOR")
if IS_WIN:
    # Habilita secuencias ANSI en la consola de Windows 10+
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        USE_COLOR = False
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def c(code: str, s: str) -> str:
    return f"\x1b[{code}m{s}\x1b[0m" if USE_COLOR else s


def green(s: str) -> str: return c("32", s)
def red(s: str) -> str: return c("31", s)
def yellow(s: str) -> str: return c("33", s)
def bold(s: str) -> str: return c("1", s)


OK = green("✔")
KO = red("✘")
WARN = yellow("!")


def section(title: str) -> None:
    print()
    print(bold(title))
    print("-" * len(title))


def run(cmd: str, args: List[str]) -> Optional[str]:
    """Ejecuta un comando y devuelve su primera línea de salida, o None si no existe/falla."""
    path = shutil.which(cmd)
    if path is None:
        return None
    try:
        out = subprocess.run(
            [path] + args,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_S,
            check=True,
            shell=False,
        ).stdout
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError):
        return None
    lines = out.strip().splitlines()
    return lines[0] if lines else ""


def check_https(host: str) -> Tuple[bool, str]:
    """Comprueba acceso HTTPS a un host. Cualquier respuesta HTTP cuenta como accesible."""
    try:
        conn = http.client.HTTPSConnection(host, 443, timeout=TIMEOUT_S, context=ssl.create_default_context())
        conn.request("HEAD", "/", headers={"User-Agent": "popiai-check"})
        status = conn.getresponse().status
        conn.close()
        return True, f"HTTP {status}"
    except socket.timeout:
        return False, f"sin respuesta en {TIMEOUT_S}s"
    except (OSError, http.client.HTTPException, ssl.SSLError) as err:
        return False, type(err).__name__ + (f": {err}" if str(err) else "")


# ---------------------------------------------------------------------------
# Comprobaciones
# ---------------------------------------------------------------------------

failures: List[str] = []
warnings: List[str] = []


def total_ram_gb() -> Optional[float]:
    try:
        if IS_WIN:
            import ctypes

            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]

            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
            return stat.ullTotalPhys / 1024 ** 3
        if sys.platform == "darwin":
            out = subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True, check=True).stdout
            return int(out.strip()) / 1024 ** 3
        # Linux
        return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 1024 ** 3
    except Exception:
        return None


def check_system() -> None:
    section("Equipo")
    ram = total_ram_gb()
    if ram is None:
        print(f"  {WARN} No se pudo determinar la RAM (se requieren 8 GB, mejor 16)")
    elif ram < 7.5:
        print(f"  {KO} {ram:.1f} GB de RAM — se requieren 8 GB (mejor 16)")
        failures.append("RAM insuficiente (mínimo 8 GB)")
    elif ram < 15.5:
        print(f"  {WARN} {ram:.1f} GB de RAM — suficiente, aunque se recomiendan 16 GB")
        warnings.append("Menos de 16 GB de RAM (recomendado)")
    else:
        print(f"  {OK} {ram:.1f} GB de RAM")
    print(f"  {OK} {platform.system()} {platform.release()} ({platform.machine()})")


def check_domains() -> None:
    section("Acceso a dominios (HTTPS)")
    with ThreadPoolExecutor(max_workers=len(DOMAINS)) as pool:
        results = list(pool.map(lambda d: check_https(d[0]), DOMAINS))
    for (host, why), (ok, detail) in zip(DOMAINS, results):
        if ok:
            print(f"  {OK} {host:<28} {why}")
        else:
            print(f"  {KO} {host:<28} {why} — {red(detail)}")
            failures.append(f"Sin acceso HTTPS a {host} ({detail})")


def check_software() -> None:
    section("Software instalado")
    for name, cmd, args, hint, validate in SOFTWARE:
        out = run(cmd, args)
        if out is None:
            print(f"  {KO} {name:<16} no encontrado — {hint}")
            failures.append(f"{name} no está instalado ({hint})")
            continue
        problem = validate(out) if validate else None
        if problem:
            print(f"  {KO} {name:<16} {out} — {problem}")
            failures.append(f"{name}: {problem}")
        else:
            print(f"  {OK} {name:<16} {out}")

    # Docker instalado pero ¿el daemon está en marcha?
    if run("docker", ["--version"]) is not None:
        info = run("docker", ["info", "--format", "{{.ServerVersion}}"])
        if not info:
            print(f"  {WARN} {'Docker daemon':<16} no responde — arranca Docker Desktop / el servicio docker")
            warnings.append("Docker está instalado pero el daemon no está en marcha")
        else:
            print(f"  {OK} {'Docker daemon':<16} en marcha (server {info})")


def check_ai_tools() -> None:
    section("Herramienta de IA (basta con una)")
    found = 0
    for name, cmd, args in AI_TOOLS:
        out = run(cmd, args)
        if out is None:
            print(f"  {yellow('·')} {name:<20} no encontrado (comando \"{cmd}\")")
        else:
            print(f"  {OK} {name:<20} {out}")
            found += 1
    if found == 0:
        print(f"  {KO} Ninguna herramienta de IA disponible")
        failures.append(
            "No se encontró Claude Code, GitHub Copilot CLI ni Codex CLI. "
            "Instala una: `npm install -g @anthropic-ai/claude-code`, "
            "`npm install -g @github/copilot` o `npm install -g @openai/codex`"
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print(bold("PopiAI × Power Electronics — Comprobación de requisitos del workshop"))

    check_system()
    check_domains()
    check_software()
    check_ai_tools()

    section("Resumen")
    for w in warnings:
        print(f"  {WARN} {w}")
    if not failures:
        print(f"  {OK} {green('Todos los requisitos se cumplen. ¡Listo para el workshop!')}")
        return 0
    print(f"  {KO} {red(f'{len(failures)} requisito(s) NO se cumplen:')}")
    for f in failures:
        print(f"     - {f}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
