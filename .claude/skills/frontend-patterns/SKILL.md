---
name: frontend-patterns
description: Next.js App Router patterns for pages, components, and routing. Use when creating pages, building React components, or deciding between client vs server components.
---

# Frontend Patterns Skill

Use this skill when working with Next.js 16 frontend code: pages, components, and routing.

## When to Activate
- Creating new pages or routes
- Building React components
- Working with App Router
- Client vs Server component decisions
- Layout and navigation

## Project Frontend Architecture

### Tech Stack
- **Framework**: Next.js 16 with App Router
- **React**: 19
- **Styling**: Tailwind CSS v4
- **State**: React hooks + context
- **API**: `apiFetch` wrapper with Firebase auth
- **Port: 3000 (dev)
- **Path alias**: `@/*` → `src/*`

### Directory Structure
```
apps/frontend/
├── app/                    # App Router pages
│   ├── (public)/          # Public routes (no auth required)
│   ├── (dashboard)/       # Dashboard (auth required)
│   └── layout.tsx         # Root layout
├── components/            # Shared components
├── hooks/                 # Custom React hooks
├── lib/                   # Utilities
│   ├── api.ts            # API fetch wrapper
│   ├── auth.ts           # Firebase auth helpers
│   └── firebase.ts       # Firebase config
└── styles/               # Global styles
```

## Page Patterns

### Client Page (Interactive)
```tsx
"use client"

import { useState, useEffect } from 'react'
import { apiFetch } from '@/lib/api'

export default function MyPage() {
  const [data, setData] = useState<DataType[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadData()
  }, [])

  async function loadData() {
    try {
      setLoading(true)
      const result = await apiFetch('/endpoint')
      setData(result)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div>Loading...</div>
  if (error) return <div className="text-red-500">{error}</div>

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">Title</h1>
      {/* Content */}
    </div>
  )
}
```

### Dynamic Route Page
```tsx
// app/(public)/items/[itemId]/page.tsx
"use client"

import { useParams } from 'next/navigation'
import { useState, useEffect } from 'react'
import { apiFetch } from '@/lib/api'

export default function ItemPage() {
  const params = useParams()
  const itemId = params.itemId as string
  const [item, setItem] = useState<Item | null>(null)

  useEffect(() => {
    if (itemId) loadItem()
  }, [itemId])

  async function loadItem() {
    const result = await apiFetch(`/items/${itemId}`)
    setItem(result)
  }

  // ...
}
```

## Component Patterns

### Functional Component with Props
```tsx
interface CardProps {
  title: string
  description?: string
  onClick?: () => void
  children?: React.ReactNode
}

export function Card({ title, description, onClick, children }: CardProps) {
  return (
    <div
      className="rounded-lg border border-black/10 dark:border-white/10 p-4"
      onClick={onClick}
    >
      <h3 className="font-medium">{title}</h3>
      {description && (
        <p className="text-sm text-black/70 dark:text-white/70">{description}</p>
      )}
      {children}
    </div>
  )
}
```

### Form Component
```tsx
"use client"

import { useState } from 'react'
import { apiFetch } from '@/lib/api'

interface FormData {
  name: string
  description: string
}

export function CreateForm({ onSuccess }: { onSuccess?: () => void }) {
  const [form, setForm] = useState<FormData>({ name: '', description: '' })
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setSaving(true)
    setError(null)

    try {
      await apiFetch('/endpoint', {
        method: 'POST',
        body: form,
      })
      onSuccess?.()
    } catch (err: any) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium mb-1">Name</label>
        <input
          type="text"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          className="w-full rounded border border-black/20 dark:border-white/20 bg-white dark:bg-black px-3 py-2"
          required
        />
      </div>

      {error && <div className="text-red-500 text-sm">{error}</div>}

      <button
        type="submit"
        disabled={saving}
        className="rounded px-4 py-2 font-medium bg-primary text-white disabled:opacity-50"
      >
        {saving ? 'Saving...' : 'Save'}
      </button>
    </form>
  )
}
```

## Layout Pattern (Route Groups)

```tsx
// app/(dashboard)/layout.tsx
import { Sidebar } from '@/components/Sidebar'

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 p-6">
        {children}
      </main>
    </div>
  )
}
```

## Common UI Patterns

### Loading State
```tsx
{loading && (
  <div className="flex items-center justify-center p-8">
    <div className="animate-spin h-8 w-8 border-2 border-primary border-t-transparent rounded-full" />
  </div>
)}
```

### Error State
```tsx
{error && (
  <div className="rounded bg-red-50 dark:bg-red-900/20 p-4 text-red-600 dark:text-red-400">
    {error}
  </div>
)}
```

### Empty State
```tsx
{data.length === 0 && !loading && (
  <div className="text-center py-12 text-black/50 dark:text-white/50">
    No items found
  </div>
)}
```

## Navigation

### Using Next.js Link
```tsx
import Link from 'next/link'

<Link href="/dashboard/settings" className="hover:underline">
  Settings
</Link>
```

### Programmatic Navigation
```tsx
import { useRouter } from 'next/navigation'

const router = useRouter()
router.push('/dashboard/settings')
router.back()
```

## File Locations
- Pages: `apps/frontend/app/[route-group]/[route]/page.tsx`
- Components: `apps/frontend/components/`
- Hooks: `apps/frontend/hooks/`
- Utils: `apps/frontend/lib/`
