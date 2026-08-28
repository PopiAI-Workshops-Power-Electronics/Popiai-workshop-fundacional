---
name: mongodb-patterns
description: Mongoose schemas, queries, aggregations and indexes. Use when creating schemas, writing database queries, or handling document relationships.
---

# MongoDB Patterns Skill

Use this skill when working with Mongoose schemas, database queries, and MongoDB operations.

## When to Activate
- Creating new Mongoose schemas
- Writing database queries
- Adding indexes
- Working with aggregations
- Handling document relationships

## Schema Pattern

### Basic Schema
```typescript
import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document } from 'mongoose';
import { v4 as uuidv4 } from 'uuid';

@Schema({ timestamps: true })
export class Resource {
  @Prop({ unique: true, required: true, default: uuidv4 })
  resourceId: string;

  @Prop({ required: true })
  name: string;

  @Prop()
  description?: string;

  @Prop({ type: String, enum: StatusEnum, default: StatusEnum.ACTIVE })
  status: StatusEnum;

  @Prop({ type: [String], default: [] })
  tags: string[];

  @Prop({ default: false })
  isDeleted: boolean;

  // Timestamps (auto-generated)
  createdAt: Date;
  updatedAt: Date;
}

export const ResourceSchema = SchemaFactory.createForClass(Resource);
export type ResourceDocument = Resource & Document;
```

### Schema with References
```typescript
import { Types } from 'mongoose';

@Schema({ timestamps: true })
export class Transaction {
  @Prop({ unique: true, required: true, default: uuidv4 })
  transactionId: string;

  // Reference by UUID (preferred for cross-service)
  @Prop({ required: true })
  userId: string;

  // Reference by ObjectId (for same-module)
  @Prop({ type: Types.ObjectId, ref: 'Profile' })
  profileRef: Types.ObjectId;

  @Prop({ type: Number, required: true })
  amount: number;
}
```

### Nested Objects
```typescript
@Prop({
  type: {
    confidence: { type: Number },
    rationale: { type: String },
    matchedSignals: { type: [String], default: [] },
    generatedAt: { type: Date },
  },
  default: undefined,
})
metadata?: {
  confidence?: number;
  rationale?: string;
  matchedSignals?: string[];
  generatedAt?: Date;
};
```

### Array of Objects
```typescript
@Prop({
  type: [{
    itemId: { type: String, required: true },
    note: { type: String, default: '' },
    tags: { type: [String], default: [] },
  }],
  default: [],
})
items: Array<{
  itemId: string;
  note?: string;
  tags?: string[];
}>;
```

## Indexes

### Define Indexes After Schema
```typescript
export const ResourceSchema = SchemaFactory.createForClass(Resource);
ResourceSchema.loadClass(Resource);

// Single field indexes
ResourceSchema.index({ name: 1 });
ResourceSchema.index({ status: 1 });
ResourceSchema.index({ createdAt: -1 });

// Compound indexes
ResourceSchema.index({ status: 1, createdAt: -1 });

// Text index for search
ResourceSchema.index({ name: 'text', description: 'text' });
```

## Middleware (Hooks)

### Pre-save Hook
```typescript
function normalizeText(s?: string): string {
  if (!s) return '';
  return s
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}

ResourceSchema.pre('save', function (next) {
  const doc = this as any;
  doc.nameNormalized = normalizeText(doc.name);
  next();
});
```

### Pre-update Hook
```typescript
ResourceSchema.pre('findOneAndUpdate', function (next) {
  const query = this as any;
  const update = query.getUpdate() || {};
  const set = update.$set || {};

  if (typeof set.name === 'string') {
    set.nameNormalized = normalizeText(set.name);
  }

  if (Object.keys(set).length > 0) {
    query.setUpdate({ ...update, $set: set });
  }
  next();
});
```

## JSON Transform
```typescript
ResourceSchema.set('toJSON', {
  transform: function (_, ret) {
    delete ret._id;
    delete ret.__v;
    return ret;
  }
});
```

## Query Patterns

### Basic CRUD in Service
```typescript
@Injectable()
export class ResourceService {
  constructor(
    @InjectModel(Resource.name)
    private readonly resourceModel: Model<Resource>,
  ) {}

  async findAll(query: ListQueryDto): Promise<Resource[]> {
    const filter: any = {};
    if (query.status) filter.status = query.status;

    return this.resourceModel
      .find(filter)
      .sort({ createdAt: -1 })
      .limit(query.limit || 50)
      .lean()
      .exec();
  }

  async findById(resourceId: string): Promise<Resource | null> {
    return this.resourceModel.findOne({ resourceId }).lean().exec();
  }

  async create(dto: CreateDto): Promise<Resource> {
    return this.resourceModel.create(dto);
  }

  async update(resourceId: string, dto: UpdateDto): Promise<Resource | null> {
    return this.resourceModel
      .findOneAndUpdate(
        { resourceId },
        { $set: dto },
        { new: true }
      )
      .lean()
      .exec();
  }

  async delete(resourceId: string): Promise<boolean> {
    const result = await this.resourceModel.deleteOne({ resourceId });
    return result.deletedCount > 0;
  }
}
```

### Pagination
```typescript
async findPaginated(query: PaginatedQuery): Promise<{ items: Resource[]; total: number }> {
  const { page = 1, limit = 20, ...filters } = query;
  const skip = (page - 1) * limit;

  const [items, total] = await Promise.all([
    this.resourceModel
      .find(filters)
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(limit)
      .lean()
      .exec(),
    this.resourceModel.countDocuments(filters),
  ]);

  return { items, total };
}
```

### Aggregation Example
```typescript
async getStats(): Promise<Stats> {
  const result = await this.resourceModel.aggregate([
    { $match: { status: 'ACTIVE' } },
    {
      $group: {
        _id: '$category',
        count: { $sum: 1 },
        avgRating: { $avg: '$rating' },
      },
    },
    { $sort: { count: -1 } },
  ]);

  return result;
}
```

## Module Registration
```typescript
import { MongooseModule } from '@nestjs/mongoose';

@Module({
  imports: [
    MongooseModule.forFeature([
      { name: Resource.name, schema: ResourceSchema },
    ]),
  ],
  providers: [ResourceService],
  exports: [ResourceService],
})
export class ResourceModule {}
```

## File Locations
- Schemas: `apps/backend/src/[module]/schemas/[name].schema.ts`
- Or: `apps/backend/src/[module]/[name].schema.ts`
