---
name: brand-design
description: Project brand implementation rules. The authoritative source for brand-consistent UI code. Agents check this skill FIRST before frontend-design or tailwind-design.
metadata:
  author: workshop-base
  version: "1.0"
---

# Project Brand Design (Workshop Defaults)

> These are default brand values for the workshop base project. Customize per project — see docs/CONFIGURACION-PROYECTO.md.

**This is the primary brand skill.** Use it whenever creating or modifying any UI component. For the full reference palette and landing page structure, see also `design-guidelines`.

## Brand Rules (MUST follow)

1. **Light mode only** — No `dark:` prefixes, no `prefers-color-scheme: dark`, no dark mode variables.
2. **Slate scale only** — Never use `gray-*`, `zinc-*`, or `neutral-*`. Always use `slate-*` (blue undertone harmonizes with Teal).
3. **Inter font only** — No Geist, no Geist_Mono, no secondary fonts. Loaded via `next/font/google`.
4. **Teal as primary** — All CTAs, links, brand accents use `teal-500`. Never use blue, indigo, or purple as primary.
5. **Generous whitespace** — Spacious layouts. When in doubt, add more space.
6. **No heavy shadows** — Use `shadow-sm` for cards. Avoid `shadow-md`, `shadow-lg`, `shadow-xl`.
7. **Rounded corners** — `rounded-xl` for cards/containers, `rounded-lg` for buttons/inputs.

## Color Quick Reference

| Purpose | Tailwind class | CSS variable |
|---------|---------------|-------------|
| Primary action | `bg-primary` / `text-primary` | `--color-primary` (#14B8A6) |
| Primary hover | `bg-primary-hover` | `--color-primary-hover` (#0D9488) |
| Primary soft bg | `bg-primary-soft` | `--color-primary-soft` (#F0FDFA) |
| Title text | `text-foreground` | `--color-foreground` (#0F172A) |
| Body text | `text-body` | `--color-body` (#475569) |
| Borders | `border-border` | `--color-border` (#E2E8F0) |
| Alt background | `bg-surface-alt` | `--color-surface-alt` (#F8FAFC) |
| Main background | `bg-background` | `--color-background` (#FFFFFF) |
| Accent | `text-accent` / `bg-accent` | `--color-accent` (#F59E0B) |
| Error | `text-error` / `bg-error` | `--color-error` (#F43F5E) |
| Success | `text-success` / `bg-success` | `--color-success` (#10B981) |

## Design Tokens (globals.css)

All tokens are defined as CSS custom properties via Tailwind v4 `@theme inline` in `apps/frontend/app/globals.css`:

```css
@theme inline {
  --color-background: #ffffff;
  --color-foreground: #0f172a;
  --color-primary: #14b8a6;
  --color-primary-hover: #0d9488;
  --color-primary-soft: #f0fdfa;
  --color-surface-alt: #f8fafc;
  --color-body: #475569;
  --color-border: #e2e8f0;
  --color-accent: #f59e0b;
  --color-error: #f43f5e;
  --color-success: #10b981;
  --font-sans: var(--font-inter);
}
```

These generate Tailwind utilities automatically (e.g., `bg-primary`, `text-body`, `border-border`).

## Component Patterns (copy-paste ready)

### Primary Button
```tsx
<button className="bg-primary hover:bg-primary-hover text-white rounded-lg px-6 py-3 font-medium transition-colors">
  Empezar gratis
</button>
```

### Secondary Button
```tsx
<button className="border border-border hover:bg-surface-alt text-foreground rounded-lg px-6 py-3 font-medium transition-colors">
  Saber más
</button>
```

### Section Heading
```tsx
<h2 className="text-3xl font-semibold text-foreground">Heading</h2>
<p className="text-body text-base leading-relaxed">Description text</p>
```

### Card
```tsx
<div className="bg-background border border-border rounded-xl p-6 shadow-sm">
  {/* content */}
</div>
```

### Link
```tsx
<a className="text-primary hover:text-primary-hover font-medium transition-colors" href="#">
  Link text
</a>
```

### Status Badges
```tsx
{/* Success */}
<span className="inline-flex items-center rounded-full bg-emerald-50 px-2.5 py-0.5 text-xs font-medium text-emerald-700">
  Activo
</span>

{/* Warning */}
<span className="inline-flex items-center rounded-full bg-amber-50 px-2.5 py-0.5 text-xs font-medium text-amber-700">
  Pendiente
</span>

{/* Error */}
<span className="inline-flex items-center rounded-full bg-rose-50 px-2.5 py-0.5 text-xs font-medium text-rose-700">
  Error
</span>
```

### Form Input
```tsx
<input
  type="text"
  className="w-full rounded-lg border border-border bg-background px-3 py-2 text-foreground placeholder:text-body/50 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors"
/>
```

### Alert Boxes
```tsx
{/* Error */}
<div className="rounded-lg bg-rose-50 border border-rose-200 p-4 text-rose-700">
  Error message
</div>

{/* Success */}
<div className="rounded-lg bg-emerald-50 border border-emerald-200 p-4 text-emerald-700">
  Success message
</div>

{/* Info */}
<div className="rounded-lg bg-primary-soft border border-teal-200 p-4 text-teal-700">
  Info message
</div>
```

## Wordmark

Define your project wordmark here. See docs/CONFIGURACION-PROYECTO.md for customization guidance.

## Typography Scale

| Element | Classes |
|---------|---------|
| Page title (h1) | `text-4xl md:text-5xl font-bold text-foreground` |
| Section title (h2) | `text-3xl font-semibold text-foreground` |
| Subsection (h3) | `text-xl font-semibold text-foreground` |
| Body | `text-base text-body leading-relaxed` |
| Small/caption | `text-sm text-body` |
| Label | `text-sm font-medium text-foreground` |

## Anti-Patterns (NEVER do)

- `dark:bg-*`, `dark:text-*` — No dark mode
- `text-gray-*`, `bg-zinc-*` — Use Slate
- `shadow-lg`, `shadow-xl` — Too heavy
- `font-mono`, Geist references — Inter only
- `bg-blue-500` as primary — Teal only
- Hardcoded hex colors in className — Use CSS variables/Tailwind tokens
