# Backend Planning Framework

Standard patterns for backend architecture planning when building VibeCode apps.

## API Endpoint Structure

### Base Pattern

```
BASE_URL/api/v1

Authentication:
  POST /auth/register       - Create new user
  POST /auth/login          - Get access token
  POST /auth/refresh        - Refresh access token
  POST /auth/logout         - Invalidate token
  GET  /auth/me             - Get current user

Resource CRUD (example: tasks):
  GET    /tasks             - List all (with pagination)
  GET    /tasks/:id         - Get single item
  POST   /tasks             - Create new item
  PUT    /tasks/:id         - Update item
  PATCH  /tasks/:id         - Partial update
  DELETE /tasks/:id         - Delete item
```

### Pagination Pattern

```
GET /tasks?page=1&limit=20&sort=-created_at

Response:
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8
  }
}
```

### Filtering Pattern

```
GET /tasks?status=active&due_date_gt=2025-01-01&assigned_to=user_id
```

---

## Database Schema Standards

### User Table (Always Required)

```sql
users
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid()
  email           VARCHAR(255) UNIQUE NOT NULL
  password_hash   VARCHAR(255) NOT NULL
  name            VARCHAR(100)
  avatar_url      TEXT
  created_at      TIMESTAMP DEFAULT NOW()
  updated_at      TIMESTAMP DEFAULT NOW()
  last_login      TIMESTAMP
```

### Resource Table Pattern

```sql
[resource_name]
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid()
  user_id         UUID REFERENCES users(id) ON DELETE CASCADE
  title           VARCHAR(255) NOT NULL
  description     TEXT
  status          VARCHAR(50) DEFAULT 'active'
  created_at      TIMESTAMP DEFAULT NOW()
  updated_at      TIMESTAMP DEFAULT NOW()

  -- Add resource-specific fields here
```

### Common Field Types

```sql
-- Dates/Times
created_at      TIMESTAMP DEFAULT NOW()
updated_at      TIMESTAMP DEFAULT NOW()
due_date        DATE
scheduled_time  TIME

-- Boolean flags
is_active       BOOLEAN DEFAULT true
is_public       BOOLEAN DEFAULT false
completed       BOOLEAN DEFAULT false

-- Enums (PostgreSQL)
status          VARCHAR(50) CHECK (status IN ('draft', 'active', 'archived'))
priority        VARCHAR(20) CHECK (priority IN ('low', 'medium', 'high'))

-- Relationships
parent_id       UUID REFERENCES [table_name](id)
user_id         UUID REFERENCES users(id) ON DELETE CASCADE

-- JSON data (flexible fields)
metadata        JSONB
settings        JSONB
```

---

## Authentication Methods

### 1. JWT (Recommended - Simple & Stateless)

**Flow:**
```
1. User registers/logs in
2. Server returns access token (15min) + refresh token (7 days)
3. Client stores tokens securely
4. Client includes access token in headers: Authorization: Bearer <token>
5. When access expires, use refresh token to get new access token
```

**Implementation:**
- Library: PyJWT (Python) or jsonwebtoken (Node.js)
- Storage: Client stores in secure storage (iOS Keychain)
- Refresh: Automatic refresh on 401 response

### 2. Session-Based (Traditional)

**Flow:**
```
1. User logs in
2. Server creates session, stores in Redis/DB
3. Returns session cookie
4. Client sends cookie with each request
5. Server validates session on each request
```

**Use when:** Need server-side session control, logout all devices feature

### 3. OAuth (Google/Apple Sign In)

**Flow:**
```
1. User clicks "Sign in with Apple"
2. VibeCode app redirects to OAuth provider
3. User authorizes
4. Provider returns token
5. Server validates token with provider
6. Create/login user in DB
```

**Use when:** Want social login, reduce friction

**Recommended default:** JWT (simplest, stateless, mobile-friendly)

---

## Stack Recommendations

### Backend Framework

**Python (Recommended for AI/ML features):**
```
Framework: FastAPI
ORM: SQLAlchemy or Prisma
Validation: Pydantic
Task Queue: Celery + Redis
```

**Node.js (Recommended for real-time features):**
```
Framework: Express or Fastify
ORM: Prisma or TypeORM
Validation: Zod
Task Queue: Bull + Redis
```

### Database

**PostgreSQL (Recommended):**
- Best for: Structured data, complex queries, JSONB support
- Hosting: Supabase (includes auth + storage)

**MongoDB:**
- Best for: Flexible schemas, rapid prototyping
- Hosting: MongoDB Atlas

### Hosting Options

**Railway (Recommended):**
- Deploy from GitHub
- Auto-scaling
- PostgreSQL included
- $5/month starter

**Render:**
- Similar to Railway
- Free tier available
- Good for small projects

**Vercel (Serverless):**
- Best for: Edge functions, global distribution
- Not ideal for: Long-running processes

### File Storage

**Nextcloud (Recommended for privacy):**
- Self-hosted or managed
- WebDAV API
- Image previews built-in

**S3-compatible:**
- Cloudflare R2 (no egress fees)
- DigitalOcean Spaces
- AWS S3

---

## Common Patterns by App Type

### Social/Content Apps

```sql
posts
  id, user_id, content, image_url, likes_count, created_at

comments
  id, post_id, user_id, content, created_at

likes
  id, post_id, user_id, created_at
  UNIQUE(post_id, user_id)

follows
  id, follower_id, following_id, created_at
  UNIQUE(follower_id, following_id)
```

### E-commerce Apps

```sql
products
  id, name, description, price, stock, image_urls, category_id

orders
  id, user_id, total, status, created_at

order_items
  id, order_id, product_id, quantity, price

cart_items
  id, user_id, product_id, quantity
```

### Productivity Apps

```sql
tasks
  id, user_id, title, description, due_date, completed, priority

projects
  id, user_id, name, description, created_at

task_project
  task_id, project_id
```

### Fitness/Health Apps

```sql
workouts
  id, user_id, name, date, duration, notes

exercises
  id, workout_id, name, sets, reps, weight

stats
  id, user_id, date, metric_name, value
```

---

## API Response Format

### Success Response

```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "title": "Task name",
    "created_at": "2025-01-07T10:30:00Z"
  }
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title is required",
    "field": "title"
  }
}
```

### List Response

```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150
  }
}
```

---

## Security Checklist

- [ ] Password hashing (bcrypt/argon2)
- [ ] JWT secret key environment variable
- [ ] HTTPS only in production
- [ ] CORS configured correctly
- [ ] SQL injection prevention (ORM parameterized queries)
- [ ] Rate limiting on auth endpoints
- [ ] Input validation on all endpoints
- [ ] User owns resource checks before CRUD
- [ ] Secure file upload validation

---

**Last updated:** 2025-01-07
