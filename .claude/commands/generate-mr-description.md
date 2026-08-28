---
name: generate-mr-description
description: "Genera descripcion de PR/MR comparando la rama actual contra main"
---

Generate a merge/pull request description by comparing the current branch against the target branch.

**Arguments:** $ARGUMENTS (optional: target branch, defaults to "main")

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
- `apps/frontend/src/path/file.tsx` - [brief description]

## Testing
- [ ] Backend tests pass (`cd apps/backend && npm run test`)
- [ ] Frontend builds (`cd apps/frontend && npm run build`)
- [ ] Manual testing completed
- [ ] Verified [specific functionality]

## Screenshots
[Add screenshots if UI changes were made]

---
Generated with [Claude Code](https://claude.ai/code)
```

5. Offer options to the user:
   - Create PR on GitHub using `gh pr create`
   - Just display for manual copy

**Usage:**
- `/generate-mr-description` - Compare against main (default)
- `/generate-mr-description develop` - Compare against a different branch

**Tips:**
- Run this after your feature is complete and ready for review
- Review and edit the generated description before submitting
- PRs target `main` branch by default
