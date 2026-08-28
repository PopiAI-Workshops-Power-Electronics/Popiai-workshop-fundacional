---
name: test-runner
description: "Ejecuta tests del backend, genera tests para modulos nuevos, ejecuta tests especificos con watch mode, arregla tests que fallan y genera reportes de cobertura para el proyecto Workshop PopiAI. Usa esta skill cuando el usuario pida ejecutar, generar o arreglar tests, o ver cobertura."
license: MIT
---

# Testing Automatizado

Esta skill facilita la ejecucion y generacion de tests en el proyecto Workshop PopiAI.

## Instrucciones

Identifica la accion solicitada por el usuario (ejecutar, generar, ver cobertura, arreglar, o modo watch) y sigue las instrucciones correspondientes.

### Acciones Disponibles

#### 1. Ejecutar tests

**Comandos:**
- **Todos**: `cd apps/backend && npm run test`
- **Watch**: `cd apps/backend && npm run test:watch`
- **Archivo especifico**: `cd apps/backend && npm run test -- --testPathPattern=benefits.service.spec`
- **E2E**: `cd apps/backend && npm run test:e2e`
- **Cobertura**: `cd apps/backend && npm run test:cov`

#### 2. Generar tests para un modulo

Ejemplos de solicitud: "genera tests para el modulo benefits", "genera solo el test del service de benefits", "genera el test e2e de benefits".

**Pasos:**
1. Leer el codigo del modulo (service y controller)
2. Generar tests unitarios con:
   - Mocks apropiados (Mongoose model, Firebase Auth, dependencies)
   - Tests para cada metodo (create, findAll, findOne, update, remove)
   - Tests de casos de error (NotFoundException, validacion)
   - Configuracion del TestingModule con guards mockeados
3. Generar tests e2e si se solicita con:
   - Setup de testing database
   - Tests de endpoints completos
   - Validacion de responses y status codes

**Template de test de service:**
```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { getModelToken } from '@nestjs/mongoose';
import { [Nombre]Service } from './[nombre].service';
import { [Nombre] } from './schemas/[nombre].schema';

describe('[Nombre]Service', () => {
  let service: [Nombre]Service;
  let model: any;

  const mockModel = {
    create: jest.fn(),
    find: jest.fn(),
    findOne: jest.fn(),
    findOneAndUpdate: jest.fn(),
    deleteOne: jest.fn(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        [Nombre]Service,
        {
          provide: getModelToken([Nombre].name),
          useValue: mockModel,
        },
      ],
    }).compile();

    service = module.get<[Nombre]Service>([Nombre]Service);
    model = module.get(getModelToken([Nombre].name));
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  // ... mas tests
});
```

**Template de test de controller con Guards:**
```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { [Nombre]Controller } from './[nombre].controller';
import { FirebaseAuthGuard } from '../auth/firebase-auth.guard';
import { IsActiveGuard } from '../auth/is-active.guard';

describe('[Nombre]Controller', () => {
  let controller: [Nombre]Controller;

  const mockService = {
    create: jest.fn(),
    findAll: jest.fn(),
    findOne: jest.fn(),
    update: jest.fn(),
    remove: jest.fn(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [[Nombre]Controller],
      providers: [
        { provide: 'I[NOMBRE]_SERVICE', useValue: mockService },
      ],
    })
      .overrideGuard(FirebaseAuthGuard)
      .useValue({ canActivate: () => true })
      .overrideGuard(IsActiveGuard)
      .useValue({ canActivate: () => true })
      .compile();

    controller = module.get<[Nombre]Controller>([Nombre]Controller);
  });

  // ... tests
});
```

#### 3. Ver reporte de cobertura

**Pasos:**
1. Ejecutar `cd apps/backend && npm run test:cov`
2. Mostrar resumen de cobertura
3. Identificar archivos con baja cobertura
4. Sugerir tests adicionales si es necesario

#### 4. Arreglar tests que fallan

**Pasos:**
1. Ejecutar los tests y capturar errores
2. Analizar los mensajes de error
3. Identificar el problema (mock incorrecto, expectativa erronea, etc.)
4. Proponer solucion o arreglar automaticamente
5. Re-ejecutar para verificar

#### 5. Modo watch interactivo

Ejecuta `cd apps/backend && npm run test:watch` y mantiene el proceso corriendo.

### Comportamiento por Defecto

Si el usuario solo pide "ejecutar los tests" sin mas contexto:
1. Ejecutar todos los tests del backend
2. Mostrar resumen de resultados
3. Si hay fallos, preguntar si quiere ver detalles o arreglar

### Estructura de Tests en Workshop

```
apps/backend/src/
├── [module]/
│   ├── [module].controller.spec.ts
│   └── [module].service.spec.ts
apps/backend/test/
    └── [module].e2e-spec.ts
```

### Mocking Firebase Auth en Tests

```typescript
const mockFirebaseAuthGuard = {
  canActivate: jest.fn().mockReturnValue(true),
};

const mockRequest = {
  db_user: {
    uuid: 'test-user-uuid',
    name: 'Test User',
    status: 'ACTIVE',
  },
};

// En TestingModule:
.overrideGuard(FirebaseAuthGuard)
.useValue(mockFirebaseAuthGuard)
```

### Mejores Practicas

- **Usar mocks apropiados**: Para Mongoose Models, Firebase
- **Aislar unidades**: Tests unitarios no deben depender de la base de datos real
- **Cubrir casos de error**: NotFoundException, validacion, etc.
- **Nombres descriptivos**: Nombres claros de que se esta probando
- **beforeEach para setup**: Limpiar estado entre tests
- **Cobertura minima recomendada**: 70% en todas las metricas
