---
name: design-guidelines
description: Project brand identity and visual standards. Use when writing any frontend code to ensure consistency with the brand system — colors, typography, components, and layout patterns.
metadata:
  author: workshop-base
  version: "1.0"
---

Apply these design guidelines when writing any frontend code. These are the project's brand identity and visual standards. **Always follow these rules when creating or modifying UI components.**

## Brand Identity

Define your project brand identity here. (Wordmark, tagline, personality, and target audience are project-specific — customize per project.)

## Typography

- **Font family**: Inter (loaded via `next/font/google`)
- **CSS variable**: `--font-inter`
- **Usage**: All text across the application. No secondary font needed.

## Color Palette

### Primary (action, CTAs, brand identity)
| Token | Tailwind | Hex | Usage |
|-------|----------|-----|-------|
| Primary | `teal-500` | `#14B8A6` | Buttons, links, brand accents |
| Primary hover | `teal-600` | `#0D9488` | Hover states |
| Primary soft | `teal-50` | `#F0FDFA` | Soft backgrounds, highlights |

### Neutrals (text, backgrounds, borders)
| Token | Tailwind | Hex | Usage |
|-------|----------|-----|-------|
| Title | `slate-900` | `#0F172A` | Headings, strong text |
| Body | `slate-600` | `#475569` | Body text, descriptions |
| Border | `slate-200` | `#E2E8F0` | Borders, dividers |
| Surface alt | `slate-50` | `#F8FAFC` | Alternate section backgrounds |
| Surface | `white` | `#FFFFFF` | Main background |

### Semantic (feedback, status)
| Token | Tailwind | Hex | Usage |
|-------|----------|-----|-------|
| Accent | `amber-500` | `#F59E0B` | Highlights, badges, secondary CTAs |
| Error | `rose-500` | `#F43F5E` | Errors, destructive actions |
| Success | `emerald-500` | `#10B981` | Success states, confirmations |

### Design Tokens (CSS variables in globals.css)
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

## Visual Style

- **Corners**: Use `rounded-xl` for cards and containers, `rounded-lg` for buttons and inputs.
- **Spacing**: Generous whitespace. Prefer spacious layouts over compact ones.
- **Shadows**: Subtle — `shadow-sm` for cards, avoid heavy shadows.
- **Text**: Short, direct, no jargon. Prefer icons over text where possible.
- **Mode**: Light mode only (no dark mode for now).
- **Neutrals**: Use Slate scale (not Gray or Zinc) — its blue undertone harmonizes with Teal.

## Component Patterns

- **Primary button**: `bg-teal-500 hover:bg-teal-600 text-white rounded-lg px-6 py-3 font-medium`
- **Secondary button**: `border border-slate-200 hover:bg-slate-50 text-slate-900 rounded-lg px-6 py-3 font-medium`
- **Section heading**: `text-3xl font-semibold text-slate-900`
- **Body text**: `text-base text-slate-600 leading-relaxed`
- **Card**: `bg-white border border-slate-200 rounded-xl p-6 shadow-sm`

## Layout Structure

Define your page/section structure here. A typical layout uses alternating backgrounds:

| Section | Background | Purpose |
|---------|-----------|---------|
| Navbar | white + backdrop-blur, fixed | Navigation |
| Hero | white | Value proposition |
| Features/Benefits | white | Key feature grid |
| How it works | slate-50 | Step-by-step explanation |
| Final CTA | teal-500 | Call to action |
| Footer | slate-900 | Links, legal, contact |
