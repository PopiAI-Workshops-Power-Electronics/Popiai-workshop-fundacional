---
name: git-workflow
description: Centralized git workflow rules for all agents — branch naming, conventional commits, and PR rules. Use before creating branches, commits, or PRs.
---

# Git Workflow - Workshop

Skill centralizada para el flujo de trabajo con Git. Todos los agentes deben seguir estas instrucciones.

## Reglas Fundamentales

1. **NUNCA crear rama nueva** sin permiso explicito del usuario
2. **NUNCA hacer push** sin que el usuario lo pida
3. **NUNCA crear PR** sin que el usuario lo pida
4. **SIEMPRE verificar en que rama estas** antes de hacer cualquier cambio

## Verificar Rama Actual

```bash
git branch --show-current
```

Si no estas en la rama correcta:

```bash
git checkout feature/[nombre-feature]
git pull origin feature/[nombre-feature] 2>/dev/null || true
```

## Branch Naming

| Tipo | Formato | Ejemplo |
|------|---------|---------|
| Feature | `feature/[nombre-kebab-case]` | `feature/user-dashboard` |
| Fix | `fix/[nombre-kebab-case]` | `fix/login-redirect` |
| Refactor | `refactor/[nombre-kebab-case]` | `refactor/auth-module` |

**Importante**: UNA sola rama por feature (backend + frontend juntos).

## Crear Rama (solo PM Analyst, solo si el usuario lo autoriza)

```bash
git checkout main
git pull origin main
git checkout -b feature/[nombre-descriptivo]
```

## Commits (Conventional Commits)

### Formato

```bash
git commit -m "$(cat <<'EOF'
<tipo>(<scope>): <descripcion>

- Detalle 1
- Detalle 2

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Prefijos por scope

| Scope | Uso |
|-------|-----|
| `feat(backend):` | Nueva funcionalidad backend |
| `feat(frontend):` | Nueva funcionalidad frontend |
| `fix(backend):` | Correccion backend |
| `fix(frontend):` | Correccion frontend |
| `refactor(backend):` | Refactorizacion backend |
| `refactor(frontend):` | Refactorizacion frontend |
| `test(backend):` | Tests backend |
| `test(frontend):` | Tests frontend |
| `style(frontend):` | Estilos frontend |
| `docs:` | Documentacion |

### Staging de archivos

Preferir `git add <archivos-especificos>` sobre `git add .` para evitar incluir archivos sensibles.

## Push y PR (solo cuando el usuario lo pida)

```bash
git push -u origin feature/[nombre-feature]

gh pr create --base main --title "<tipo>: <descripcion>" --body "$(cat <<'EOF'
## Summary
- [Cambios principales]

## Changes
- [ ] Detalle de cambio 1
- [ ] Detalle de cambio 2

## Test Plan
- [ ] Tests que ejecutar
- [ ] Verificaciones manuales

Generated with Claude Code
EOF
)"
```

## Git Flow del Proyecto

- Feature branches desde `main`
- PRs hacia `main`
- Local development only (sin deploy automatico)
- Una rama por feature (backend + frontend juntos)
