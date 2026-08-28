---
name: testing-patterns
description: Jest mocks, unit tests and e2e tests for the NestJS backend, plus Playwright E2E for the Next.js frontend. Use when writing tests for services/controllers/pages, mocking dependencies, deciding what to test, or analyzing test failures.
---

# Testing Patterns Skill

Use this skill when writing or working with tests in the NestJS backend.

## When to Activate
- Writing unit tests for services
- Writing unit tests for controllers
- Mocking dependencies (Mongoose, Firebase, services)
- Running tests and analyzing failures
- Writing e2e tests

## Test File Structure

```
apps/backend/src/
├── [module]/
│   ├── [module].service.ts
│   ├── [module].service.spec.ts     # Service unit tests
│   ├── [module].controller.ts
│   └── [module].controller.spec.ts  # Controller unit tests
apps/backend/test/
    └── [module].e2e-spec.ts         # E2E tests
```

## Service Unit Test Pattern

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { getModelToken } from '@nestjs/mongoose';
import { ResourceService } from './resource.service';
import { Resource } from './schemas/resource.schema';

describe('ResourceService', () => {
  let service: ResourceService;
  let model: any;

  // Mock Mongoose model
  const mockModel = {
    create: jest.fn(),
    find: jest.fn(),
    findOne: jest.fn(),
    findOneAndUpdate: jest.fn(),
    deleteOne: jest.fn(),
  };

  // Mock other services
  const mockOtherService = {
    someMethod: jest.fn(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        ResourceService,
        {
          provide: getModelToken(Resource.name),
          useValue: mockModel,
        },
        {
          provide: 'IOTHER_SERVICE_INTERNAL',
          useValue: mockOtherService,
        },
      ],
    }).compile();

    service = module.get<ResourceService>(ResourceService);
    model = module.get(getModelToken(Resource.name));
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  describe('create', () => {
    it('should create a resource', async () => {
      const createDto = { name: 'Test' };
      const expected = { resourceId: '123', ...createDto };
      mockModel.create.mockResolvedValue(expected);

      const result = await service.create(createDto);

      expect(result).toEqual(expected);
      expect(mockModel.create).toHaveBeenCalledWith(createDto);
    });
  });

  describe('findOne', () => {
    it('should return a resource', async () => {
      const expected = { resourceId: '123', name: 'Test' };
      mockModel.findOne.mockReturnValue({
        lean: jest.fn().mockReturnValue({
          exec: jest.fn().mockResolvedValue(expected),
        }),
      });

      const result = await service.findOne('123');

      expect(result).toEqual(expected);
    });

    it('should throw NotFoundException when not found', async () => {
      mockModel.findOne.mockReturnValue({
        lean: jest.fn().mockReturnValue({
          exec: jest.fn().mockResolvedValue(null),
        }),
      });

      await expect(service.findOne('invalid')).rejects.toThrow();
    });
  });
});
```

## Controller Unit Test Pattern

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { ResourceController } from './resource.controller';
import { FirebaseAuthGuard } from '../auth/firebase-auth.guard';
import { IsActiveGuard } from '../auth/is-active.guard';

describe('ResourceController', () => {
  let controller: ResourceController;

  const mockService = {
    findAll: jest.fn(),
    findOne: jest.fn(),
    create: jest.fn(),
    update: jest.fn(),
    delete: jest.fn(),
  };

  const mockRequest = {
    db_user: {
      uuid: 'test-user-uuid',
      name: 'Test User',
      status: 'ACTIVE',
    },
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [ResourceController],
      providers: [
        {
          provide: 'IRESOURCE_SERVICE',
          useValue: mockService,
        },
      ],
    })
      // Override guards to always allow
      .overrideGuard(FirebaseAuthGuard)
      .useValue({ canActivate: () => true })
      .overrideGuard(IsActiveGuard)
      .useValue({ canActivate: () => true })
      .compile();

    controller = module.get<ResourceController>(ResourceController);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('findAll', () => {
    it('should return array of resources', async () => {
      const expected = [{ resourceId: '1' }, { resourceId: '2' }];
      mockService.findAll.mockResolvedValue(expected);

      const result = await controller.findAll(mockRequest as any, {});

      expect(result).toBeDefined();
      expect(mockService.findAll).toHaveBeenCalledWith(
        mockRequest.db_user.uuid,
        {}
      );
    });
  });
});
```

## Mocking Patterns

### Mongoose Model Mock
```typescript
const mockModel = {
  create: jest.fn(),
  find: jest.fn().mockReturnValue({
    sort: jest.fn().mockReturnValue({
      limit: jest.fn().mockReturnValue({
        lean: jest.fn().mockReturnValue({
          exec: jest.fn().mockResolvedValue([]),
        }),
      }),
    }),
  }),
  findOne: jest.fn().mockReturnValue({
    lean: jest.fn().mockReturnValue({
      exec: jest.fn().mockResolvedValue(null),
    }),
  }),
  findOneAndUpdate: jest.fn().mockReturnValue({
    lean: jest.fn().mockReturnValue({
      exec: jest.fn().mockResolvedValue(null),
    }),
  }),
  deleteOne: jest.fn().mockResolvedValue({ deletedCount: 1 }),
  countDocuments: jest.fn().mockResolvedValue(0),
  aggregate: jest.fn().mockResolvedValue([]),
};
```

### Auth Guard Mock (when auth is implemented — see `auth-flow`)
```typescript
// In test setup
jest.mock('firebase-admin', () => ({
  auth: () => ({
    verifyIdToken: jest.fn().mockResolvedValue({
      user_id: 'firebase-user-id',
      email: 'test@example.com',
    }),
  }),
  apps: [],
  initializeApp: jest.fn(),
  credential: {
    cert: jest.fn(),
  },
}));
```

### Internal Service Mock
```typescript
const mockUsersServiceInternal = {
  getProfile: jest.fn().mockResolvedValue({
    uuid: 'user-123',
    name: 'Test User',
    status: 'ACTIVE',
  }),
  getRawProfile: jest.fn().mockResolvedValue({
    uuid: 'user-123',
    name: 'Test User',
    status: 'ACTIVE',
  }),
};

// In providers
{
  provide: 'IUSERS_SERVICE_INTERNAL',
  useValue: mockUsersServiceInternal,
}
```

## Test Commands

```bash
# Run all tests
cd apps/backend && npm run test

# Run tests in watch mode
cd apps/backend && npm run test:watch

# Run specific test file
cd apps/backend && npm run test -- --testPathPattern=resource.service.spec

# Run with coverage
cd apps/backend && npm run test:cov

# Run e2e tests
cd apps/backend && npm run test:e2e
```

## Best Practices

### 1. Isolate Unit Tests
- Mock all external dependencies
- Don't hit real database or external APIs
- Each test should be independent

### 2. Test Names
```typescript
describe('methodName', () => {
  it('should do X when Y', async () => {});
  it('should throw NotFoundException when resource not found', async () => {});
  it('should return empty array when no results', async () => {});
});
```

### 3. Arrange-Act-Assert
```typescript
it('should create resource', async () => {
  // Arrange
  const dto = { name: 'Test' };
  mockModel.create.mockResolvedValue({ id: '1', ...dto });

  // Act
  const result = await service.create(dto);

  // Assert
  expect(result.id).toBe('1');
  expect(mockModel.create).toHaveBeenCalledWith(dto);
});
```

### 4. Test Error Cases
```typescript
it('should throw NotFoundException', async () => {
  mockModel.findOne.mockReturnValue({
    lean: () => ({ exec: () => Promise.resolve(null) }),
  });

  await expect(service.findOne('invalid'))
    .rejects
    .toThrow(NotFoundException);
});
```

### 5. Coverage Goals
- Minimum 80% coverage for all metrics when the task or specification requires it (see `AGENTS.md` and the applicable spec)
- Focus on business logic in services
- Controllers mostly test guard setup and DTO transformation

### 6. What a Good Test File Must Have (minimum)
- Happy path for every public method
- At least one error case per method that can fail (404, 409, 400)
- At least one edge case (empty list, boundary value, optional field missing)
- All external dependencies mocked (Mongoose model, other services)
- Assertions on the RESULT, not only on `toHaveBeenCalled`

Weak-test smells a reviewer will flag: a single `it`, `expect(true).toBe(true)`, tests that mirror the implementation line by line, mocks that return whatever makes the test pass without checking inputs.

## Frontend E2E (Playwright)

`apps/frontend` already has `@playwright/test` and the script `npm run e2e`. Tests live in `apps/frontend/e2e/*.spec.ts` and need a `playwright.config.ts`:

```typescript
// apps/frontend/playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  use: { baseURL: 'http://localhost:3000', trace: 'on-first-retry' },
  projects: [
    { name: 'desktop', use: { ...devices['Desktop Chrome'] } },
    { name: 'mobile', use: { ...devices['Pixel 5'] } },
  ],
  webServer: { command: 'npm run dev', url: 'http://localhost:3000', reuseExistingServer: true },
});
```

First run: `npx playwright install chromium`.

### E2E Pattern (complete flow, not isolated clicks)

```typescript
// apps/frontend/e2e/categorias.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Categorías', () => {
  test('should create, edit and delete a category', async ({ page }) => {
    await page.goto('/categorias');
    await expect(page.getByRole('heading', { name: 'Categorías' })).toBeVisible();

    await page.getByRole('button', { name: 'Nueva categoría' }).click();
    await page.getByLabel('Nombre').fill('E2E test');
    await page.getByRole('button', { name: 'Guardar' }).click();
    await expect(page.getByRole('cell', { name: 'E2E test' })).toBeVisible();

    await page.getByRole('row', { name: /E2E test/ }).getByRole('button', { name: 'Editar' }).click();
    await page.getByLabel('Nombre').fill('E2E editado');
    await page.getByRole('button', { name: 'Guardar' }).click();
    await expect(page.getByRole('cell', { name: 'E2E editado' })).toBeVisible();

    await page.getByRole('row', { name: /E2E editado/ }).getByRole('button', { name: 'Eliminar' }).click();
    await expect(page.getByRole('cell', { name: 'E2E editado' })).toHaveCount(0);
  });

  test('should show validation error when name is empty', async ({ page }) => {
    await page.goto('/categorias');
    await page.getByRole('button', { name: 'Nueva categoría' }).click();
    await page.getByRole('button', { name: 'Guardar' }).click();
    await expect(page.getByRole('alert')).toBeVisible();
  });
});
```

### E2E Rules
- Locators by role/label (`getByRole`, `getByLabel`), not by CSS class or test id unless unavoidable
- One test per user flow (create → list → edit → delete), plus one per error state
- Backend and MongoDB must be running (`npm run start:backend`, `docker-compose up -d`); tests create their own data and clean it up
- Run the mobile project too when the feature has responsive UI

## File Locations
- Backend unit tests: same directory as source file (`.spec.ts`)
- Backend E2E tests: `apps/backend/test/`
- Backend test utilities: `apps/backend/test/utils/`
- Frontend E2E tests: `apps/frontend/e2e/*.spec.ts` (+ `playwright.config.ts`)
