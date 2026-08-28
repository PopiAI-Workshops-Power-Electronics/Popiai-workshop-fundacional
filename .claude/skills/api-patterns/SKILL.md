---
name: api-patterns
description: NestJS controllers, services, DTOs, guards and DI patterns for backend API code. Use when creating endpoints, controllers, request/response DTOs or service layer logic.
---

# API Patterns Skill

Use this skill when working with NestJS backend API code: controllers, services, DTOs, and responses.

## When to Activate
- Creating new API endpoints
- Adding controllers or routes
- Working with request/response DTOs
- Implementing service layer logic
- Adding Swagger documentation

## Project API Architecture

### Controller Pattern
All controllers follow this structure:

```typescript
import { Controller, Get, Post, Patch, Body, Req, UseGuards, Inject, Query } from '@nestjs/common';
import { ApiBearerAuth, ApiOkResponse, ApiNotFoundResponse } from '@nestjs/swagger';
import { plainToInstance } from 'class-transformer';
import { FirebaseAuthGuard } from '../auth/firebase-auth.guard';
import { IsActiveGuard } from '../auth/is-active.guard';
import { AuthenticatedRequest } from '../shared/interfaces/authenticated-request';

@Controller('resources')
export class ResourcesController {
  constructor(
    @Inject(IRESOURCE_SERVICE)
    private readonly resourceService: IResourceService,
  ) {}

  @Get('/')
  @ApiBearerAuth('access-token')
  @UseGuards(FirebaseAuthGuard, IsActiveGuard)
  @ApiOkResponse({ description: 'List of resources', type: ResourceResponseDto, isArray: true })
  async getList(@Req() req: AuthenticatedRequest, @Query() query: ListQueryDto) {
    const result = await this.resourceService.getList(req.db_user.uuid, query);
    return plainToInstance(ResourceResponseDto, result, { excludeExtraneousValues: true });
  }
}
```

### Guards (Auth Flow)
Always use guards in this order:
```typescript
@UseGuards(FirebaseAuthGuard, IsActiveGuard)
```

- `FirebaseAuthGuard`: Validates Firebase ID token, sets `request.user`
- `IsActiveGuard`: Checks user is ACTIVE in DB, sets `request.db_user`

### Anonymous Endpoints
For endpoints that support anonymous access:
```typescript
@AllowAnonymous()
@UseGuards(FirebaseAuthGuard, IsActiveGuard)
async myEndpoint(@Req() req: AuthenticatedRequest) {
  const userId = req?.db_user?.uuid;  // May be undefined for anonymous
  if (userId) {
    // Authenticated flow
  } else {
    // Anonymous flow
  }
}
```

### Service Injection Pattern (DDD)
Services use interfaces for dependency injection:

```typescript
// Interface file: Iresource.service.ts
export const IRESOURCE_SERVICE = 'IRESOURCE_SERVICE';
export interface IResourceService {
  getList(userId: string, query: ListQueryDto): Promise<Resource[]>;
  create(dto: CreateResourceDto): Promise<Resource>;
}

// Implementation file: resource.service.ts
@Injectable()
export class ResourceService implements IResourceService {
  constructor(
    @InjectModel(Resource.name)
    private readonly resourceModel: Model<Resource>,

    @Inject(IOTHER_SERVICE_INTERNAL)
    private readonly otherServiceInternal: IOtherServiceInternal,
  ) {}
}

// Module registration
providers: [
  {
    provide: IRESOURCE_SERVICE,
    useClass: ResourceService,
  },
],
```

### Internal vs External Services
- `IRESOURCE_SERVICE`: Used by controllers (external API)
- `IRESOURCE_SERVICE_INTERNAL`: Used by other services (cross-domain)

```typescript
// External (controller uses this)
@Inject(IRESOURCE_SERVICE)
private readonly resourceService: IResourceService,

// Internal (service-to-service)
@Inject(IRESOURCE_SERVICE_INTERNAL)
private readonly resourceServiceInternal: IResourceServiceInternal,
```

## DTO Patterns

### Request DTO (Input)
```typescript
import { IsString, IsOptional, IsEnum, IsNotEmpty, IsArray } from 'class-validator';

export class CreateResourceRequestDto {
  @IsString()
  @IsNotEmpty()
  name: string;

  @IsString()
  @IsOptional()
  description?: string;

  @IsEnum(ResourceTypeEnum)
  type: ResourceTypeEnum;

  @IsArray()
  @IsString({ each: true })
  @IsOptional()
  tags?: string[];
}
```

### Response DTO (Output)
```typescript
import { Expose, Type } from 'class-transformer';

export class ResourceResponseDto {
  @Expose()
  id: string;

  @Expose()
  name: string;

  @Expose()
  @Type(() => NestedResponseDto)
  nested?: NestedResponseDto;

  @Expose()
  createdAt: Date;
}
```

### Query DTO (GET params)
```typescript
import { IsOptional, IsString, IsEnum } from 'class-validator';
import { Transform } from 'class-transformer';

export class ListQueryDto {
  @IsOptional()
  @IsString()
  search?: string;

  @IsOptional()
  @IsEnum(SortEnum)
  sort?: SortEnum;

  @IsOptional()
  @Transform(({ value }) => parseInt(value, 10))
  limit?: number;
}
```

## Response Transformation
Always use `plainToInstance` for responses:
```typescript
return plainToInstance(ResponseDto, result, { excludeExtraneousValues: true });
```

## File Upload Pattern
```typescript
@Post('/upload')
@UseGuards(FirebaseAuthGuard, IsActiveGuard)
@UseInterceptors(FileInterceptor('file', { storage: memoryStorage() }))
@ApiConsumes('multipart/form-data')
@ApiBody({
  schema: {
    type: 'object',
    properties: {
      file: { type: 'string', format: 'binary' },
    },
  },
})
async uploadFile(
  @Req() req: AuthenticatedRequest,
  @UploadedFile() file: Express.Multer.File
) {
  if (!file) throw new BadRequestException('No file uploaded');
  return await this.service.uploadFile(req.db_user.uuid, file);
}
```

## Swagger Documentation
Always add these decorators:
- `@ApiBearerAuth('access-token')` - For protected endpoints
- `@ApiOkResponse({ description, type })` - Success response
- `@ApiNotFoundResponse({ description })` - 404 cases
- `@ApiBadRequestResponse({ description })` - Validation errors
- `@ApiCreatedResponse({ description, type })` - POST success

## Error Handling
```typescript
import { NotFoundException, BadRequestException, ForbiddenException } from '@nestjs/common';

// In service
if (!resource) throw new NotFoundException('Resource not found');
if (!isOwner) throw new ForbiddenException('Not owner of resource');
if (!isValid) throw new BadRequestException('Invalid data');
```

## File Locations
- Controllers: `apps/backend/src/[module]/[module].controller.ts`
- Admin controllers: `apps/backend/src/[module]/admin/[module].admin.controller.ts`
- Services: `apps/backend/src/[module]/[module].service.ts`
- Interfaces: `apps/backend/src/[module]/I[module].service.ts`
- DTOs: `apps/backend/src/[module]/dto/*.dto.ts`
- Shared DTOs: `apps/backend/src/shared/dto/*.dto.ts`
