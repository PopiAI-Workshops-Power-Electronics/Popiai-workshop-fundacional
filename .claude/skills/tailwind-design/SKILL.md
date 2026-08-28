---
name: tailwind-design
description: Tailwind CSS v4 patterns and responsive design for Workshop. Use for layout, responsive, and structural styling patterns. Defer to brand-design for colors and brand specifics.
metadata:
  author: workshop-base
  version: "1.1"
---

# Tailwind Design Skill

Use this skill for layout patterns, responsive design, and structural UI. **For brand colors and component styling, defer to `brand-design` first.**

## When to Activate
- Building responsive layouts
- Implementing grid/flex patterns
- Working with spacing and containers
- Creating loading states and animations
- Structuring page layouts

## Tailwind v4 Notes

This project uses **Tailwind CSS v4** with `@theme inline` in `globals.css`. There is no `tailwind.config.ts` — all tokens are CSS custom properties.

- Design tokens: defined in `apps/frontend/app/globals.css`
- PostCSS plugin: `@tailwindcss/postcss`
- Font: `--font-sans` set to `var(--font-inter)` via `@theme inline`

## Layout Patterns

### Page Container
```tsx
<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  {/* Centered content with responsive padding */}
</div>
```

### Section Container
```tsx
<section className="py-16 sm:py-20 lg:py-24">
  <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <h2 className="text-3xl font-semibold text-foreground">Section Title</h2>
    <p className="mt-4 text-body text-base leading-relaxed max-w-2xl">
      Section description
    </p>
  </div>
</section>
```

### Alternating Section Backgrounds
```tsx
{/* White section */}
<section className="bg-background py-16">...</section>

{/* Alt background section */}
<section className="bg-surface-alt py-16">...</section>
```

### Grid Layout
```tsx
{/* Responsive grid: 1 → 2 → 3 columns */}
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
  {/* Items */}
</div>

{/* 2x2 grid */}
<div className="grid grid-cols-1 md:grid-cols-2 gap-6">
  {/* Items */}
</div>

{/* Two column form */}
<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
  {/* Form fields */}
</div>
```

### Flex Layout
```tsx
{/* Horizontal with space between */}
<div className="flex items-center justify-between">
  <span>Left</span>
  <span>Right</span>
</div>

{/* Centered */}
<div className="flex items-center justify-center min-h-[400px]">
  {/* Content */}
</div>

{/* With gap */}
<div className="flex items-center gap-3">
  {/* Items */}
</div>

{/* Wrap on small screens */}
<div className="flex flex-wrap gap-4">
  {/* Items */}
</div>
```

### Stack Layout
```tsx
{/* Vertical stack with consistent spacing */}
<div className="space-y-4">
  {/* Items */}
</div>
```

## Responsive Breakpoints
```
sm:  640px   (mobile landscape)
md:  768px   (tablet)
lg:  1024px  (desktop)
xl:  1280px  (large desktop)
2xl: 1536px  (extra large)
```

### Responsive Patterns
```tsx
{/* Hide on mobile, show on desktop */}
<div className="hidden md:block">Desktop only</div>

{/* Show on mobile, hide on desktop */}
<div className="md:hidden">Mobile only</div>

{/* Responsive text sizes */}
<h1 className="text-3xl md:text-4xl lg:text-5xl font-bold">Title</h1>

{/* Responsive padding */}
<div className="px-4 sm:px-6 lg:px-8">Content</div>

{/* Responsive flex direction */}
<div className="flex flex-col md:flex-row gap-4">
  {/* Stack on mobile, row on desktop */}
</div>
```

## State & Animation Patterns

### Loading Spinner
```tsx
<div className="animate-spin h-8 w-8 border-2 border-primary border-t-transparent rounded-full" />
```

### Skeleton Loading
```tsx
<div className="animate-pulse space-y-4">
  <div className="h-4 bg-slate-200 rounded w-3/4"></div>
  <div className="h-4 bg-slate-200 rounded w-1/2"></div>
  <div className="h-4 bg-slate-200 rounded w-5/6"></div>
</div>
```

### Transitions
```tsx
{/* Color transition (buttons, links) */}
<button className="transition-colors duration-200">...</button>

{/* All properties */}
<div className="transition-all duration-300">...</div>

{/* Hover scale */}
<div className="transition-transform hover:scale-105">...</div>
```

## Navbar Pattern (Fixed with Blur)
```tsx
<nav className="fixed top-0 inset-x-0 z-50 bg-background/80 backdrop-blur-md border-b border-border">
  <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
    {/* Logo + links + CTA */}
  </div>
</nav>
{/* Spacer for fixed navbar */}
<div className="h-16" />
```

## Labels & Form Layout
```tsx
<label className="block text-sm font-medium text-foreground mb-1.5">
  Field Label
</label>
<input className="w-full rounded-lg border border-border bg-background px-3 py-2 text-foreground placeholder:text-body/50 focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-colors" />
```

## Overflow & Scroll
```tsx
{/* Horizontal scroll */}
<div className="overflow-x-auto">
  <table className="min-w-full">...</table>
</div>

{/* Scrollable container with max height */}
<div className="max-h-96 overflow-y-auto">
  {/* Long content */}
</div>
```

## Spacing Conventions

Workshop uses generous whitespace. Preferred spacing scale:

| Context | Spacing |
|---------|---------|
| Between sections | `py-16 sm:py-20 lg:py-24` |
| Inside cards | `p-6` |
| Between card items | `space-y-4` |
| Grid gaps | `gap-6` |
| Button padding | `px-6 py-3` |
| Form field gap | `space-y-4` or `gap-4` |
| Text below heading | `mt-4` |

## File Locations
- Global styles + tokens: `apps/frontend/app/globals.css`
- Layout (font loading): `apps/frontend/app/layout.tsx`
- Components: `apps/frontend/components/`
