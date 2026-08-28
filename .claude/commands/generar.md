---
name: generar
description: "Genera codigo siguiendo las convenciones del proyecto Workshop: componentes NextJS, servicios NestJS, DTOs, schemas, hooks, y mas"
---

# Generacion de Codigo

Este comando facilita la generacion de codigo siguiendo las convenciones y mejores practicas del proyecto Workshop PopiAI.

## Instrucciones

Cuando el usuario invoque `/generar [tipo] [nombre] [opciones?]`, genera el codigo correspondiente:

### Tipos Disponibles

#### 1. `componente` - Componente NextJS
```bash
# Componente basico
/generar componente Button

# Componente con props especificas
/generar componente BenefitCard --props "name:string, description:string, imageUrl:string"

# Componente de pagina completa
/generar componente DashboardPage --type page
```

**Template basico:**
```typescript
'use client';

import React from 'react';

interface [Nombre]Props {
  // Props definidas por el usuario o inferidas
}

export function [Nombre]({ /* props */ }: [Nombre]Props) {
  return (
    <div className="/* estilos Tailwind */">
      {/* Contenido del componente */}
    </div>
  );
}
```

**Ubicacion**: `apps/frontend/src/components/[categoria]/[Nombre].tsx`

**Caracteristicas**:
- TypeScript con interfaces para props
- 'use client' si tiene interactividad
- Tailwind CSS v4
- Dark mode support con clases `dark:`
- Export named (no default para componentes reutilizables)

#### 2. `hook` - Custom Hook de React
```bash
/generar hook useSubscriptions
/generar hook useBenefitSearch --returns "benefits, loading, error, search"
```

**Template:**
```typescript
'use client';

import { useState, useEffect } from 'react';
import { apiFetch } from '@/lib/api';

export function use[Nombre]() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    apiFetch('/endpoint')
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);

  return { data, loading, error };
}
```

**Ubicacion**: `apps/frontend/src/hooks/use[Nombre].ts`

#### 3. `service` - Servicio NestJS
```bash
/generar service NotificationService
/generar service SubscriptionService --inject "UsersService"
```

**Template:**
```typescript
import { Injectable } from '@nestjs/common';

@Injectable()
export class [Nombre]Service implements I[Nombre]Service {
  constructor(
    // Dependencias inyectadas
  ) {}

  // Metodos del servicio
}
```

**Ubicacion**: `apps/backend/src/[nombre]/[nombre].service.ts`

**No olvides**:
- Crear interface I[Nombre]Service
- Registrar en el module correspondiente
- Crear archivo `.spec.ts` para tests

#### 4. `dto` - Data Transfer Object
```bash
/generar dto CreateBenefitDto --fields "name:string, description:string, discount?:number"
/generar dto UpdateBenefitDto --extends CreateBenefitDto
```

**Template:**
```typescript
import { IsString, IsNumber, IsOptional, IsNotEmpty } from 'class-validator';

export class [Nombre]Dto {
  @IsString()
  @IsNotEmpty()
  name: string;

  @IsString()
  @IsOptional()
  description?: string;
}
```

**Ubicacion**: `apps/backend/src/[module]/dto/[nombre].dto.ts`

**Validadores comunes**:
- `@IsString()`, `@IsNumber()`, `@IsBoolean()`
- `@IsEmail()`, `@IsUrl()`, `@IsDate()`
- `@IsOptional()`, `@IsNotEmpty()`
- `@Min()`, `@Max()`, `@Length()`
- `@IsArray()`, `@ValidateNested()`
- `@IsEnum()` para enums

#### 5. `schema` - Schema de Mongoose
```bash
/generar schema Benefit --fields "name:string, description:string, discount:number, isActive:boolean"
/generar schema Subscription --fields "userId:string, planId:string, expiresAt:Date"
```

**Template:**
```typescript
import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { HydratedDocument } from 'mongoose';

export type [Nombre]Document = HydratedDocument<[Nombre]>;

@Schema({ timestamps: true })
export class [Nombre] {
  @Prop({ required: true })
  name: string;

  @Prop({ default: true })
  isActive: boolean;
}

export const [Nombre]Schema = SchemaFactory.createForClass([Nombre]);
```

**Ubicacion**: `apps/backend/src/[nombre]/[nombre].schema.ts`

#### 6. `controller` - Controlador NestJS
```bash
/generar controller BenefitsController
/generar controller SubscriptionController --routes "create:post, getActive:get, cancel:post"
```

**Template:**
```typescript
import {
  Controller, Get, Post, Patch, Delete, Body, Param, UseGuards,
} from '@nestjs/common';
import { FirebaseAuthGuard } from '../auth/firebase-auth.guard';
import { IsActiveGuard } from '../auth/is-active.guard';

@Controller('[nombre]s')
@UseGuards(FirebaseAuthGuard, IsActiveGuard)
export class [Nombre]sController {
  constructor(private readonly [nombre]sService: [Nombre]sService) {}

  @Post()
  create(@Body() createDto: Create[Nombre]Dto) {
    return this.[nombre]sService.create(createDto);
  }

  @Get()
  findAll() {
    return this.[nombre]sService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.[nombre]sService.findOne(id);
  }
}
```

**Ubicacion**: `apps/backend/src/[nombre]/[nombre]s.controller.ts`

#### 7. `api` - Cliente API para frontend
```bash
/generar api benefits
/generar api subscriptions --methods "create, getActive, cancel"
```

**Template:**
```typescript
import { apiFetch } from '@/lib/api';

export const [nombre]Api = {
  async getAll() {
    return apiFetch('/[nombre]s');
  },
  async getById(id: string) {
    return apiFetch(`/[nombre]s/${id}`);
  },
  async create(data: Create[Nombre]Input) {
    return apiFetch('/[nombre]s', { method: 'POST', body: data });
  },
  async update(id: string, data: Update[Nombre]Input) {
    return apiFetch(`/[nombre]s/${id}`, { method: 'PATCH', body: data });
  },
  async delete(id: string) {
    return apiFetch(`/[nombre]s/${id}`, { method: 'DELETE' });
  },
};
```

**Ubicacion**: `apps/frontend/src/lib/api/[nombre]s.ts`

#### 8. `types` - Tipos compartidos
```bash
/generar types Benefit --fields "id:string, name:string, discount:number"
```

**Template:**
```typescript
export interface [Nombre] {
  id: string;
  name: string;
  createdAt: Date;
  updatedAt: Date;
}

export type Create[Nombre]Input = Omit<[Nombre], 'id' | 'createdAt' | 'updatedAt'>;
export type Update[Nombre]Input = Partial<Create[Nombre]Input>;
```

**Ubicacion**: `packages/types/src/[nombre].ts` (si se usa shared package) o `apps/frontend/src/types/[nombre].ts`

### Opciones Globales

- `--dry-run`: Mostrar el codigo sin escribir archivos
- `--overwrite`: Sobrescribir si el archivo ya existe
- `--no-test`: No generar archivo de test

### Convenciones Workshop

**Nomenclatura**:
- Componentes: PascalCase (BenefitCard, UserProfile)
- Hooks: camelCase con 'use' prefix (useBenefits, useSubscription)
- Services: PascalCase con 'Service' suffix (SubscriptionService)
- DTOs: PascalCase con 'Dto' suffix (CreateBenefitDto)
- Schemas: PascalCase singular (Benefit, Subscription)
- Controllers: PascalCase con 'Controller' suffix (BenefitsController)

**Imports**:
- Backend: Usar imports relativos dentro del modulo
- Frontend: Usar `@/` para paths relativos a `src/`
