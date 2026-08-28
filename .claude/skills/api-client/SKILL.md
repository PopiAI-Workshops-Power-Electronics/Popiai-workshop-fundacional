---
name: api-client
description: Frontend API wrapper, error handling and patterns for calling the NestJS backend from Next.js (fetch, forms, uploads, auth tokens).
---

# API Client Skill

Use this skill when making API calls from the frontend to the NestJS backend.

## When to Activate
- Fetching data from the API
- Submitting forms to the backend
- Uploading files
- Handling API errors
- Working with authentication tokens

## Core API Function

### apiFetch
Location: `apps/frontend/lib/api.ts`

```typescript
import { apiFetch } from '@/lib/api'

// GET request
const data = await apiFetch('/resources')

// POST request
const created = await apiFetch('/resources', {
  method: 'POST',
  body: { name: 'Resource Name' },
})

// PATCH request
const updated = await apiFetch(`/resources/${id}`, {
  method: 'PATCH',
  body: { name: 'Updated Name' },
})

// DELETE request
await apiFetch(`/resources/${id}`, { method: 'DELETE' })
```

### Features
- Automatically adds `Authorization: Bearer <token>` from Firebase
- Auto-retries on 401 with token refresh
- Handles JSON and text responses
- Throws Error with message from API on failure

## File Upload

### Multipart Form Data
```typescript
async function uploadImage(file: File) {
  const formData = new FormData()
  formData.append('file', file)

  const result = await apiFetch('/upload', {
    method: 'POST',
    body: formData,
    isMultipart: true,  // Important: don't set Content-Type
  })

  return result
}
```

### With File Input
```tsx
<input
  type="file"
  accept="image/*"
  onChange={async (e) => {
    const file = e.target.files?.[0]
    if (file) {
      await uploadImage(file)
    }
  }}
/>
```

## Common Patterns

### Data Fetching Hook Pattern
```typescript
"use client"

import { useState, useEffect, useCallback } from 'react'
import { apiFetch } from '@/lib/api'

export function useResources(filter?: string) {
  const [resources, setResources] = useState<Resource[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      const query = filter ? `?filter=${filter}` : ''
      const data = await apiFetch(`/resources${query}`)
      setResources(data)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [filter])

  useEffect(() => {
    load()
  }, [load])

  return { resources, loading, error, reload: load }
}
```

### Form Submission Pattern
```typescript
async function handleSubmit(e: React.FormEvent) {
  e.preventDefault()
  setSaving(true)
  setError(null)

  try {
    await apiFetch('/endpoint', {
      method: 'POST',
      body: formData,
    })
    // Success handling
    onSuccess?.()
  } catch (err: any) {
    setError(err.message)
  } finally {
    setSaving(false)
  }
}
```

### Optimistic Update Pattern
```typescript
async function toggleStatus(id: string, currentStatus: boolean) {
  // Optimistic update
  setItems(prev => prev.map(item =>
    item.id === id ? { ...item, active: !currentStatus } : item
  ))

  try {
    await apiFetch(`/items/${id}`, {
      method: 'PATCH',
      body: { active: !currentStatus },
    })
  } catch (err: any) {
    // Revert on error
    setItems(prev => prev.map(item =>
      item.id === id ? { ...item, active: currentStatus } : item
    ))
    setError(err.message)
  }
}
```

## Error Handling

### API Error Structure
```typescript
// API returns errors like:
{
  "statusCode": 400,
  "message": ["name should not be empty"],
  "error": "Bad Request"
}

// Or:
{
  "statusCode": 404,
  "message": "Resource not found"
}
```

### Error Display Pattern
```tsx
{error && (
  <div className="rounded bg-red-50 dark:bg-red-900/20 p-4 text-red-600 dark:text-red-400">
    {error}
  </div>
)}
```

### Try-Catch Pattern
```typescript
try {
  const result = await apiFetch('/endpoint')
  return result
} catch (err: any) {
  // err.message contains the API error message
  console.error('API Error:', err.message)
  throw err  // or handle gracefully
}
```

## Query Parameters

### Building Query Strings
```typescript
function buildQuery(params: Record<string, string | number | undefined>) {
  const query = new URLSearchParams()
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== '') {
      query.append(key, String(value))
    }
  }
  const str = query.toString()
  return str ? `?${str}` : ''
}

// Usage
const query = buildQuery({ filter: 'active', limit: 20, sort: undefined })
const data = await apiFetch(`/resources${query}`)
```

## API Endpoints Reference

### Common Patterns
```
GET    /resources           - List
GET    /resources/:id       - Get one
POST   /resources           - Create
PATCH  /resources/:id       - Update
DELETE /resources/:id       - Delete

# Admin endpoints
GET    /admin/resources     - Admin list (all)
POST   /admin/resources/:id/action  - Admin action
```

### Authentication
- All requests automatically include Firebase token
- 401 responses trigger token refresh and retry
- Anonymous endpoints work without token

## File Locations
- API wrapper: `apps/frontend/lib/api.ts`
- Auth helpers: `apps/frontend/lib/auth.ts`
- Firebase config: `apps/frontend/lib/firebase.ts`
