---
name: api-contract
description: Standardized API contract format used to hand off endpoint specifications between the fullstack-architect and backend/frontend developers.
---

# API Contract - Workshop

Template estandarizado para definir contratos de API entre arquitecto y desarrolladores.

## Uso

- El **fullstack-architect** escribe el contrato en la spec (`docs/specs/*.md`)
- El **backend-developer** implementa segun el contrato
- El **frontend-developer** consume segun el contrato
- El **qa-tester** verifica que la implementacion cumple el contrato

## Template de Contrato

Para cada endpoint, usar este formato:

```markdown
### `METHOD /ruta`

**Descripcion**: Que hace este endpoint

**Auth**: FirebaseAuthGuard + IsActiveGuard | AdminRoleGuard | Public

**Request**:
| Campo | Tipo | Requerido | Validacion | Descripcion |
|-------|------|-----------|------------|-------------|
| field | string | si | @IsNotEmpty() | Descripcion |
| count | number | no | @IsOptional(), @Min(0) | Descripcion |

**Request ejemplo**:
```json
{
  "field": "valor",
  "count": 5
}
```

**Response 200/201**:
| Campo | Tipo | Descripcion |
|-------|------|-------------|
| id | string | ID del recurso |
| field | string | Campo devuelto |
| createdAt | string (ISO) | Fecha de creacion |

**Response ejemplo**:
```json
{
  "id": "abc123",
  "field": "valor",
  "createdAt": "2025-01-15T10:30:00Z"
}
```

**Errores**:
| Codigo | Cuando | Body |
|--------|--------|------|
| 400 | Validacion falla | `{ "message": ["field must not be empty"], "error": "Bad Request" }` |
| 401 | Token invalido | `{ "message": "Unauthorized" }` |
| 404 | Recurso no existe | `{ "message": "Resource not found" }` |
| 409 | Duplicado | `{ "message": "Resource already exists" }` |
```

## Secciones del Contrato Completo

```markdown
## API Contract

### Base URL
- Dev: `http://localhost:3001`

### Autenticacion
Los endpoints protegidos requieren:
- Header: `Authorization: Bearer <token>` (Add Authorization header if auth-flow is enabled.)
- Guards: `FirebaseAuthGuard` + `IsActiveGuard`

### Endpoints

#### Modulo: [NombreModulo]

##### `GET /recurso`
[... usar template de arriba ...]

##### `POST /recurso`
[... usar template de arriba ...]

##### `GET /recurso/:id`
[... usar template de arriba ...]

##### `PUT /recurso/:id`
[... usar template de arriba ...]

##### `DELETE /recurso/:id`
[... usar template de arriba ...]

### DTOs

#### CreateRecursoDto
```typescript
export class CreateRecursoDto {
  @IsString()
  @IsNotEmpty()
  field: string;

  @IsOptional()
  @IsNumber()
  @Min(0)
  count?: number;
}
```

#### RecursoResponseDto
```typescript
export class RecursoResponseDto {
  id: string;
  field: string;
  createdAt: Date;
}
```

### Schema MongoDB

```typescript
@Schema({ timestamps: true })
export class Recurso {
  @Prop({ required: true })
  field: string;

  @Prop({ default: 0 })
  count: number;
}
```
```

## Principios del Contrato

1. **Exhaustivo**: Cada endpoint documenta request, response y errores
2. **Verificable**: Los ejemplos son JSON valido que se puede usar en tests
3. **Consistente**: Misma estructura para todos los endpoints
4. **Versionado**: El contrato vive en la spec y se commitea con el codigo
5. **Single Source of Truth**: Si hay discrepancia entre contrato e implementacion, el contrato manda (y la implementacion debe corregirse)
