# Launch Planner - Reference Documentation

## Technical Framework Deep Dive

### MVP Scoping Methodology

#### The 2-Week Sprint Philosophy

**Why 2 weeks?**
- Forces ruthless prioritization
- Maintains momentum and motivation
- Enables quick market validation
- Prevents perfectionism paralysis
- Short enough to course-correct cheaply

**Timeline breakdown:**
- **Days 1-3:** Foundation (Next.js setup, database schema, auth)
- **Days 4-7:** Core feature implementation (the ONE unique thing)
- **Days 8-10:** UI polish and user flow
- **Days 11-12:** Integration testing and bug fixes
- **Days 13-14:** Deployment and launch prep

### Tech Stack Decision Framework

#### Next.js 14+ (App Router)
**Why:**
- Server Components reduce client bundle
- Server Actions eliminate API route boilerplate
- Built-in optimization (images, fonts, scripts)
- Excellent DX with hot reload
- SEO-friendly by default

**When to use alternatives:**
- Static sites only → Astro/Hugo
- Heavy client interactivity → Vite + React
- No React knowledge → Remix/SvelteKit

#### Supabase (PostgreSQL)
**Why:**
- Auth built-in (email, OAuth, magic links)
- Real-time subscriptions out of box
- Row Level Security (RLS) for permissions
- Generous free tier (50k monthly active users)
- Hosted Postgres (no DevOps)

**Schema design principles:**
- Start with 2-4 tables maximum
- Add foreign keys for relationships
- Use `uuid` for IDs (better for distributed systems)
- Add `created_at`, `updated_at` timestamps
- Enable RLS from day 1

**When to use alternatives:**
- Need MongoDB → Firebase/MongoDB Atlas
- Serverless functions heavy → AWS Amplify
- GraphQL required → Hasura/Apollo

#### Vercel
**Why:**
- Zero-config Next.js deployment
- Automatic HTTPS and CDN
- Preview deployments for PRs
- Built-in analytics
- Free tier is generous

**When to use alternatives:**
- High traffic expected → Railway/Fly.io (cheaper scaling)
- Need WebSocket persistence → Render/Railway
- Heavy compute → AWS/GCP

### Database Schema Patterns

#### Core Entity Pattern
```sql
-- Every MVP has ONE core entity
-- Example: SaaS dashboard builder
create table dashboards (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references auth.users not null,
  name text not null,
  config jsonb not null, -- Flexible schema
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Enable RLS
alter table dashboards enable row level security;

-- Users can only see their own
create policy "Users can CRUD own dashboards"
  on dashboards for all
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);
```

#### Relationship Patterns
```sql
-- One-to-Many (User → Items)
create table items (
  id uuid primary key default uuid_generate_v4(),
  dashboard_id uuid references dashboards(id) on delete cascade,
  content text not null,
  position int not null,
  created_at timestamptz default now()
);

-- Many-to-Many (with join table)
create table dashboard_shares (
  dashboard_id uuid references dashboards(id) on delete cascade,
  shared_with_user_id uuid references auth.users on delete cascade,
  permission text check (permission in ('view', 'edit')),
  primary key (dashboard_id, shared_with_user_id)
);
```

### Feature Scoping Decision Tree

```
Is this feature critical to the core value prop?
├─ YES → Is it the ONE unique thing?
│   ├─ YES → Include, build first
│   └─ NO → Is it blocking without it?
│       ├─ YES → Include, build second
│       └─ NO → V2 (defer)
└─ NO → Does removing it break the happy path?
    ├─ YES → Include, but simplify
    └─ NO → V2 (defer)
```

### PRD Components Explained

#### 1. Core Problem & Solution
**Format:**
```markdown
**Problem:** [User's pain point in one concrete sentence]
**Solution:** [Your product's approach in one sentence]
**Validation:** [Evidence that this problem is real]
```

**Good example:**
```markdown
**Problem:** Developers spend 2-3 hours manually creating social media images for blog posts.
**Solution:** Auto-generate Open Graph images from blog post titles using AI.
**Validation:** 50 developers said they'd pay $10/mo for this (landing page signups).
```

**Bad example:**
```markdown
**Problem:** Social media is hard.
**Solution:** We make it easier.
**Validation:** Everyone uses social media.
```

#### 2. MVP Scope (The Forcing Function)

**The ONE Core Feature:**
- Must be the unique value proposition
- Must be demonstrable in 30 seconds
- Must solve the core problem end-to-end
- Cannot be "we're better at X" (needs to be different)

**Supporting Features (2-3 max):**
- Auth (only if you need user accounts)
- Basic CRUD (create, read, update, delete)
- One export/share mechanism

**NOT in V1 (Explicit Exclusions):**
- Forces you to think about what you're NOT building
- Prevents feature creep during development
- Helps communicate to stakeholders/users

#### 3. Database Schema
**Minimal tables only:**
- Start with 2-4 tables
- No premature optimization (indexes, views)
- Include RLS policies
- Focus on core entities only

#### 4. 2-Week Sprint Plan

**Week 1: Foundation**
- Day 1-2: Next.js setup, Supabase config, auth
- Day 3-4: Database schema, basic queries
- Day 5-7: Core feature (the ONE thing)

**Week 2: Polish & Ship**
- Day 8-9: UI polish, responsive design
- Day 10-11: Integration testing, edge cases
- Day 12-13: Deploy to Vercel, final testing
- Day 14: Launch (Product Hunt, Twitter, etc.)

#### 5. Starter Prompts for Claude Code

**Purpose:** Give the developer copy-paste prompts to build faster

**Pattern:**
```markdown
## 🎬 Starter Prompts for Claude Code

### 1. Initial Setup
"Set up a Next.js 14 project with App Router, Supabase integration, and Tailwind CSS. Configure environment variables for Supabase."

### 2. Database Schema
"Create Supabase tables for [core entity] with the following schema: [paste schema]. Add Row Level Security policies."

### 3. Core Feature
"Build a [specific feature] that [specific outcome]. Use Server Actions for mutations and include loading states."
```

## Advanced Patterns

### When to Break the 2-Week Rule

**Extend to 3-4 weeks if:**
- Complex authentication (e.g., enterprise SSO)
- Payment integration is critical (Stripe setup)
- Real-time collaboration (WebSockets, CRDTs)
- API integration requires partner approval

**Never go beyond 4 weeks for MVP**

### Handling Complex Features

**Break down complex features:**
```
Feature: "Collaborative editing"

V1 (MVP):
- [ ] Save state to database
- [ ] Show who else is viewing (presence)
- [ ] Manual refresh to see changes

V2 (post-launch):
- [ ] Real-time cursor positions
- [ ] Operational transform (conflict resolution)
- [ ] Undo/redo across users
```

### Scaling Considerations (NOT for MVP)

**Database:**
- Start: Supabase free tier (50k MAU)
- Scale: Supabase Pro ($25/mo → 100k MAU)
- Scale more: Supabase Team/Enterprise

**Compute:**
- Start: Vercel Hobby (free)
- Scale: Vercel Pro ($20/mo)
- Scale more: Self-host on Railway/Fly.io

**Storage:**
- Start: Supabase Storage (1GB free)
- Scale: S3/Cloudflare R2

## Common Anti-Patterns

### ❌ The "Enterprise Features" Trap
**Symptoms:**
- Adding user roles before you have teams
- Building audit logs before you have customers
- Creating admin dashboards before manual work is painful

**Solution:** Wait for explicit customer demand

### ❌ The "Best Practices" Trap
**Symptoms:**
- Microservices for MVP
- E2E testing before any users
- CI/CD pipeline with 15 stages
- Abstract architectures for 2 tables

**Solution:** Start monolithic, refactor with evidence

### ❌ The "Platform" Trap
**Symptoms:**
- Building APIs for future integrations
- Plugin systems for extensibility
- Marketplace for third-party extensions

**Solution:** Do one thing well first

### ❌ The "Perfect UX" Trap
**Symptoms:**
- Pixel-perfect designs before validating value
- Animations and micro-interactions everywhere
- Onboarding flows with 10 steps

**Solution:** Make it work, then make it beautiful

## Tech Stack Alternatives Matrix

| Requirement | Default | Alternative 1 | Alternative 2 |
|-------------|---------|---------------|---------------|
| **Frontend** | Next.js 14 | Remix | Astro + React |
| **Backend** | Next.js API | tRPC + Next.js | Hono + Cloudflare |
| **Database** | Supabase | PlanetScale | Neon |
| **Auth** | Supabase Auth | Clerk | NextAuth.js |
| **Styling** | Tailwind + shadcn | Tailwind + DaisyUI | Panda CSS |
| **Hosting** | Vercel | Railway | Fly.io |
| **File Storage** | Supabase Storage | Cloudflare R2 | UploadThing |

## Launch Checklist (Day 14)

**Technical:**
- [ ] Environment variables configured
- [ ] Custom domain connected
- [ ] HTTPS working
- [ ] Database backups enabled
- [ ] Error logging (Sentry/LogSnag)

**Product:**
- [ ] Landing page live
- [ ] Sign up flow works
- [ ] Core feature functional
- [ ] Test accounts ready for demos
- [ ] Pricing page (even if free)

**Marketing:**
- [ ] Product Hunt submission ready
- [ ] Launch tweet drafted
- [ ] 5-10 relevant communities identified
- [ ] Friends/beta users ready to support

**Post-Launch:**
- [ ] Analytics installed (Plausible/Posthog)
- [ ] User feedback mechanism (email/form)
- [ ] Changelog setup
- [ ] Monitoring/uptime checks

## Resources

**Starter Templates:**
- [create-t3-app](https://create.t3.gg) - Next.js + tRPC + Prisma
- [Supabase Starter Kit](https://vercel.com/templates/next.js/supabase) - Next.js + Supabase
- [Next.js SaaS Starter](https://github.com/leerob/next-saas-starter) - Lee Robinson's template

**Component Libraries:**
- [shadcn/ui](https://ui.shadcn.com) - Copy-paste components
- [DaisyUI](https://daisyui.com) - Tailwind components
- [Aceternity UI](https://ui.aceternity.com) - Animated components

**Inspiration:**
- [IndieHackers](https://indiehackers.com) - Real MVPs and timelines
- [Microfounder](https://microfounder.com) - Solo founder playbook
- [12 Startups in 12 Months](https://levels.io) - Pieter Levels approach

---

**Related:** See `EXAMPLES.md` for full MVP examples and `TROUBLESHOOTING.md` for common issues.
