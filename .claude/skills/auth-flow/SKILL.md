---
name: auth-flow
description: Firebase Auth guards, user context and roles for NestJS. Use when implementing protected endpoints, accessing the current user, or handling admin-only/anonymous access.
---

# Auth Flow Skill

Use this skill when working with authentication, authorization, and user context.

## When to Activate
- Implementing protected endpoints
- Working with Firebase Auth
- Accessing current user in controllers/services
- Creating admin-only routes
- Handling anonymous access

## Authentication Flow

```
Client Request
     │
     ▼
┌─────────────────┐
│ FirebaseAuthGuard│  ← Validates Bearer token
│                 │  ← Sets request.user (Firebase decoded token)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  IsActiveGuard  │  ← Looks up user in MongoDB
│                 │  ← Checks status === ACTIVE
│                 │  ← Sets request.db_user (full user doc)
└────────┬────────┘
         │
         ▼
    Controller
```

## Guards

### FirebaseAuthGuard
Location: `apps/backend/src/auth/firebase-auth.guard.ts`

```typescript
@Injectable()
export class FirebaseAuthGuard implements CanActivate {
  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest();
    const authHeader = request.headers.authorization;

    // Check @AllowAnonymous decorator
    const allowAnonymous = this.reflector.getAllAndOverride<boolean>(
      ALLOW_ANONYMOUS_KEY,
      [context.getHandler(), context.getClass()],
    );

    if (!authHeader) {
      if (allowAnonymous) return true;
      throw new UnauthorizedException('Missing Authorization header');
    }

    const idToken = authHeader.split('Bearer ')[1];
    const decodedToken = await admin.auth().verifyIdToken(idToken);
    request.user = decodedToken;  // Firebase user
    return true;
  }
}
```

### IsActiveGuard
Location: `apps/backend/src/auth/is-active.guard.ts`

```typescript
@Injectable()
export class IsActiveGuard implements CanActivate {
  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest();
    const user = request.user;

    // Skip for anonymous routes without auth
    if (!user?.user_id && allowAnonymous) return true;

    const userFromDb = await this.usersService.getRawProfile(user.user_id);
    if (!userFromDb) throw new ForbiddenException('User not found');
    if (userFromDb.status !== USER_STATUSES_ENUM.ACTIVE) {
      throw new ForbiddenException('User is not active');
    }

    request.db_user = userFromDb;  // Full MongoDB user document
    return true;
  }
}
```

## Using Guards in Controllers

### Standard Protected Endpoint
```typescript
@Controller('resources')
export class ResourcesController {

  @Get('/')
  @ApiBearerAuth('access-token')
  @UseGuards(FirebaseAuthGuard, IsActiveGuard)
  async getResources(@Req() req: AuthenticatedRequest) {
    const userId = req.db_user.uuid;  // Always available
    return this.service.getByUser(userId);
  }
}
```

### Anonymous-Allowed Endpoint
```typescript
@Get('/public')
@AllowAnonymous()
@UseGuards(FirebaseAuthGuard, IsActiveGuard)
async getPublicData(@Req() req: AuthenticatedRequest) {
  const userId = req?.db_user?.uuid;  // May be undefined

  if (userId) {
    // Authenticated: personalized response
    return this.service.getPersonalized(userId);
  } else {
    // Anonymous: generic response
    return this.service.getGeneric();
  }
}
```

### Admin-Only Endpoint
```typescript
@Controller('admin/resources')
export class ResourcesAdminController {

  @Get('/')
  @ApiBearerAuth('access-token')
  @UseGuards(FirebaseAuthGuard, IsActiveGuard, AdminRoleGuard)
  async adminGetAll() {
    return this.service.getAllForAdmin();
  }
}
```

## Request Interface

```typescript
// apps/backend/src/shared/interfaces/authenticated-request.ts
export interface AuthenticatedRequest extends Request {
  user?: {
    user_id: string;  // Firebase UID
    email?: string;
    // ... other Firebase fields
  };
  db_user: {
    uuid: string;      // Our internal UUID
    name: string;
    email: string;
    status: USER_STATUSES_ENUM;
    role: USER_ROLES_ENUM;
    // ... full user document
  };
}
```

## AllowAnonymous Decorator

```typescript
// apps/backend/src/auth/allow-anonymous.decorator.ts
import { SetMetadata } from '@nestjs/common';

export const ALLOW_ANONYMOUS_KEY = 'allowAnonymous';
export const AllowAnonymous = () => SetMetadata(ALLOW_ANONYMOUS_KEY, true);
```

## User Roles & Statuses

```typescript
// apps/backend/src/users/enums/user.enums.ts
export enum USER_STATUSES_ENUM {
  ACTIVE = 'ACTIVE',
  INACTIVE = 'INACTIVE',
  SUSPENDED = 'SUSPENDED',
  DELETED = 'DELETED',
}

export enum USER_ROLES_ENUM {
  USER = 'USER',
  ADMIN = 'ADMIN',
}
```

## Firebase Admin Setup

```typescript
// apps/backend/src/firebase/firebase-admin.service.ts
import * as admin from 'firebase-admin';

@Injectable()
export class FirebaseAdminService {
  constructor() {
    if (!admin.apps.length) {
      admin.initializeApp({
        credential: admin.credential.cert({
          projectId: process.env.FIREBASE_PROJECT_ID,
          clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
          privateKey: process.env.FIREBASE_PRIVATE_KEY?.replace(/\\n/g, '\n'),
        }),
      });
    }
  }

  async verifyToken(idToken: string): Promise<admin.auth.DecodedIdToken> {
    return admin.auth().verifyIdToken(idToken);
  }
}
```

## Common Patterns

### Get Current User in Service
```typescript
// Pass userId from controller
async getMyData(userId: string): Promise<Data> {
  const user = await this.usersServiceInternal.getProfile(userId);
  // ...
}
```

### Check Ownership
```typescript
async updateResource(userId: string, resourceId: string, dto: UpdateDto) {
  const resource = await this.resourceModel.findOne({ resourceId });
  if (!resource) throw new NotFoundException('Resource not found');
  if (resource.ownerUserId !== userId) {
    throw new ForbiddenException('Not owner of resource');
  }
  // ... proceed with update
}
```

## File Locations
- Guards: `apps/backend/src/auth/*.guard.ts`
- Decorators: `apps/backend/src/auth/*.decorator.ts`
- Firebase: `apps/backend/src/firebase/`
- User enums: `apps/backend/src/users/enums/user.enums.ts`
