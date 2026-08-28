---
name: generate-mr-description
description: "Genera la descripcion de un pull/merge request comparando la rama actual contra la rama principal (main por defecto). Usa esta skill cuando el usuario pida generar una descripcion de PR/MR o preparar el texto para un pull request."
license: MIT
---

Generate a merge/pull request description by comparing the current branch against the target branch (defaults to `main` unless the user specifies another branch).

**Instructions:**

1. Get current branch info:
   ```bash
   git branch --show-current
   git log main..HEAD --oneline
   ```

2. Get the full diff against target:
   ```bash
   git diff main...HEAD --stat
   git diff main...HEAD
   ```

3. Analyze the changes:
   - What files were modified/added/deleted
   - What features or fixes were implemented
   - Backend changes (controllers, services, schemas, DTOs)
   - Frontend changes (pages, components, hooks)
   - API endpoint changes
   - Database schema changes
   - Test changes

4. Generate a PR description with this format:

```markdown
## Summary
[2-3 sentences describing the overall change]

## Changes

### [Category 1: e.g., "New Feature" / "Bug Fix" / "Refactor"]
- Change 1
- Change 2

### [Category 2 if applicable]
- Change 1

## Files Changed

### Backend (API)
- `apps/backend/src/path/file.ts` - [brief description]

### Frontend (Web)
- `apps/frontend/path/file.tsx` - [brief description]

## Testing
- [ ] Backend tests pass (`cd apps/backend && npm run test`)
- [ ] Frontend builds (`cd apps/frontend && npm run build`)
- [ ] Manual testing completed
- [ ] Verified [specific functionality]

## Screenshots
[Add screenshots if UI changes were made]
```

5. Offer options to the user:
   - Create PR on GitHub using `gh pr create` (only if the user explicitly asks to create/open the PR)
   - Just display for manual copy

**Tips:**
- Run this after your feature is complete and ready for review
- Review and edit the generated description before submitting
- PRs target `main` branch by default
- Never push or open a PR without explicit user approval
