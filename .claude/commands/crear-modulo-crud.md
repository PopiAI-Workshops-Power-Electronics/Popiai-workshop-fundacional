---
name: crear-modulo-crud
description: "Crea un modulo CRUD completo con backend NestJS (schema, DTOs, service, controller, tests) y frontend NextJS (pagina, componentes, hooks)"
---

# Crear Modulo CRUD Completo

Este comando automatiza la creacion de un modulo CRUD completo en el proyecto Workshop.

## Instrucciones

Cuando el usuario invoque `/crear-modulo-crud [nombre]`, sigue estos pasos:

### 1. Validacion y Preparacion
- Solicita el nombre del modulo si no se proporciona (en singular, minusculas)
- Pregunta por los campos del schema con sus tipos (ej: "name: string, description: string, price: number, isActive: boolean")
- Confirma con el usuario antes de generar el codigo

### 2. Backend (NestJS)

Genera los siguientes archivos en `apps/backend/src/[nombre]/`:

#### Schema (`[nombre].schema.ts`)
```typescript
import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { HydratedDocument } from 'mongoose';
import { v4 as uuidv4 } from 'uuid';

export type [Nombre]Document = HydratedDocument<[Nombre]>;

@Schema({ timestamps: true })
export class [Nombre] {
  @Prop({ unique: true, required: true, default: uuidv4 })
  [nombre]Id: string;

  // Campos segun los especificados por el usuario
}

export const [Nombre]Schema = SchemaFactory.createForClass([Nombre]);
```

#### DTOs (`dto/create-[nombre].dto.ts` y `dto/update-[nombre].dto.ts`)
- CreateDto con validadores class-validator
- UpdateDto usando PartialType

#### Service Interface (`I[nombre].service.ts`)
```typescript
export const I[NOMBRE]_SERVICE = 'I[NOMBRE]_SERVICE';

export interface I[Nombre]Service {
  create(dto: Create[Nombre]Dto): Promise<[Nombre]>;
  findAll(): Promise<[Nombre][]>;
  findOne(id: string): Promise<[Nombre]>;
  update(id: string, dto: Update[Nombre]Dto): Promise<[Nombre]>;
  remove(id: string): Promise<void>;
}
```

#### Service (`[nombre].service.ts`)
- Implementa I[Nombre]Service
- Metodos CRUD completos: create, findAll, findOne, update, remove
- Inyeccion de Model de Mongoose
- Manejo de errores con NotFoundException

#### Controller (`[nombre].controller.ts`)
- Rutas REST completas: POST /, GET /, GET /:id, PATCH /:id, DELETE /:id
- Decoradores apropiados (@Body, @Param, etc.)
- Guards: FirebaseAuthGuard, IsActiveGuard
- plainToInstance para response DTOs

#### Module (`[nombre].module.ts`)
- Configuracion de MongooseModule.forFeature
- Providers con interface injection pattern
- Controllers registrados
- **Importar en app.module.ts**

#### Tests (`[nombre].service.spec.ts`)
- Tests unitarios basicos para el service
- Mocks del Mongoose model
- Tests para create, findAll, findOne, update, remove
- Tests de error cases

### 3. Frontend (NextJS)

Genera los siguientes archivos en `apps/frontend/src/`:

#### Pagina principal (`app/[nombre]s/page.tsx`)
```typescript
import { [Nombre]List } from '@/components/[nombre]s/[Nombre]List';

export default function [Nombre]sPage() {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">[Nombre]s</h1>
      <[Nombre]List />
    </div>
  );
}
```

#### Componente List (`components/[nombre]s/[Nombre]List.tsx`)
- Componente cliente con 'use client'
- Fetching de datos con useEffect
- Renderizado de lista con estados de loading, error y vacio
- Botones para crear, editar, eliminar
- Estilos con Tailwind CSS v4

#### Hook personalizado (`hooks/use[Nombre]s.ts`)
- Custom hook para manejar CRUD operations
- Estados de loading y error
- Funciones: fetch, create, update, delete
- Integracion con apiFetch

### 4. Verificacion Final

Ejecutar en orden:
```bash
cd apps/backend && npm run lint
cd apps/backend && npm run build
cd apps/backend && npm run test
cd apps/frontend && npm run lint
cd apps/frontend && npm run build
```

Sugerir al usuario ejecutar `npm run start:backend` y `npm run start:frontend` para probar.

## Convenciones Workshop

- **Nombres**: Singular para entity/schema, plural para controllers/services/rutas
- **Paths Backend**: `apps/backend/src/[feature]/`
- **Paths Frontend**: `apps/frontend/src/`
- **Estilos**: Tailwind CSS v4
- **Validacion**: class-validator en DTOs del backend
- **Error handling**: NotFoundException cuando no se encuentra un recurso
- **TypeScript**: Tipos estrictos en todos los archivos
- **Tests**: Al menos cobertura basica en service
- **Auth**: FirebaseAuthGuard + IsActiveGuard en controllers protegidos
- **Service Pattern**: Interface injection con tokens (I[NOMBRE]_SERVICE)

## Ejemplo de Uso

```
Usuario: /crear-modulo-crud benefit
Claude: ¿Que campos necesitas para el modelo Benefit?
Usuario: name: string, description: string, discount: number, category: string, isActive: boolean
Claude: [Genera todos los archivos...]

Archivos generados:
  - apps/backend/src/benefit/benefit.schema.ts
  - apps/backend/src/benefit/dto/create-benefit.dto.ts
  - apps/backend/src/benefit/dto/update-benefit.dto.ts
  - apps/backend/src/benefit/Ibenefit.service.ts
  - apps/backend/src/benefit/benefit.service.ts
  - apps/backend/src/benefit/benefit.controller.ts
  - apps/backend/src/benefit/benefit.module.ts
  - apps/backend/src/benefit/benefit.service.spec.ts
  - apps/frontend/src/app/benefits/page.tsx
  - apps/frontend/src/components/benefits/BenefitList.tsx
  - apps/frontend/src/hooks/useBenefits.ts
  - Updated apps/backend/src/app.module.ts
```
