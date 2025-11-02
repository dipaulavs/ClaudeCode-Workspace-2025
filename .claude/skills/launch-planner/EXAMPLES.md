# Launch Planner - Examples

## Example 1: SaaS Dashboard Builder MVP

### User Request
"Help me plan the launch of a tool that lets developers create custom dashboards for their SaaS products without coding."

### Launch Plan Output

```markdown
# 📱 DashForge - MVP Launch Plan

## 🎯 Core Problem & Solution

**Problem:** SaaS developers spend 5-10 hours building admin dashboards from scratch for every new project.

**Solution:** Visual dashboard builder that generates React components and API endpoints from a drag-and-drop interface.

**Validation:**
- 120 signups on landing page (20% conversion)
- 15 developers said "I'd pay $20/mo for this" in interviews
- GitHub issue searches show 400+ "need dashboard" requests

## 🚀 MVP Scope

### The ONE Core Feature
**Visual Dashboard Builder**
- Drag-and-drop components (charts, tables, stats)
- Connect to user's database (read-only)
- Generate embeddable React component
- Export code to copy-paste

### Supporting Features (3 essentials)
1. **Database Connection** - Support PostgreSQL and MySQL with connection string
2. **Template Library** - 5 pre-built dashboard templates (analytics, e-commerce, support, etc.)
3. **Live Preview** - Real-time preview with user's actual data

### NOT in V1 (ship later)
- ❌ Custom component builder (use pre-built only)
- ❌ Collaboration features (single user only)
- ❌ Version history (save latest version only)
- ❌ Hosted dashboards (export code only)
- ❌ Multiple data sources (one database per dashboard)
- ❌ Custom styling (use default theme only)
- ❌ User permissions (no RBAC)

## 🏗️ Tech Stack

**Frontend:**
- Next.js 14 (App Router)
- Tailwind CSS + shadcn/ui
- React DnD (drag-and-drop)
- Recharts (chart library)

**Backend:**
- Next.js API Routes
- Supabase (PostgreSQL) for app data
- Node-postgres for user database connections

**Hosting:**
- Vercel (frontend + API)
- Supabase (database)

## 📊 Database Schema

```sql
-- Core tables only
create table users (
  id uuid primary key default uuid_generate_v4(),
  email text unique not null,
  created_at timestamptz default now()
);

create table dashboards (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references users(id) on delete cascade,
  name text not null,
  database_connection jsonb not null, -- encrypted connection string
  layout jsonb not null, -- component positions and config
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create table templates (
  id uuid primary key default uuid_generate_v4(),
  name text not null,
  category text not null,
  layout jsonb not null,
  preview_image text,
  created_at timestamptz default now()
);

-- Row Level Security
alter table dashboards enable row level security;

create policy "Users can CRUD own dashboards"
  on dashboards for all
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);
```

## 🗺️ 2-Week Sprint Plan

### Week 1: Foundation
**Day 1-2: Setup & Auth**
- Next.js 14 project setup
- Supabase configuration
- Email authentication
- Basic layout (sidebar + main area)

**Day 3-4: Database Connection**
- Connection form (host, port, user, password, database)
- Test connection endpoint
- Store encrypted credentials
- Query builder (basic SELECT only)

**Day 5-7: Core Builder**
- Drag-and-drop canvas (React DnD)
- 5 basic components (line chart, bar chart, stat card, table, text)
- Component property panel (title, data source)
- Save/load layout to database

### Week 2: Polish & Ship
**Day 8-9: Templates & Export**
- 5 pre-built templates
- Template preview gallery
- "Apply template" feature
- Code export (React component + API endpoint)

**Day 10-11: Live Preview & Testing**
- Connect to test database
- Live data preview
- Handle connection errors
- Edge case testing (empty data, large datasets)

**Day 12-13: UI Polish & Deploy**
- Responsive design (mobile-friendly)
- Loading states and error messages
- Deploy to Vercel
- Test production environment

**Day 14: Launch Prep**
- Landing page copy
- Demo video (2 min)
- Product Hunt submission
- Launch tweet thread

## 🎬 Starter Prompts for Claude Code

### 1. Initial Setup
```
Set up a Next.js 14 project with App Router, Supabase integration, Tailwind CSS, and shadcn/ui. Include authentication pages (login/signup) using Supabase Auth.
```

### 2. Database Schema
```
Create Supabase tables for dashboards, users, and templates with the following schema:
[paste schema above]
Add Row Level Security policies so users can only access their own dashboards.
```

### 3. Core Feature (Dashboard Builder)
```
Build a dashboard builder component using React DnD. The canvas should allow dragging components (LineChart, BarChart, StatCard) from a sidebar. Each component should be configurable (title, data source query). Save the layout to Supabase as JSONB.
```

### 4. Database Connection
```
Create an API endpoint that accepts database connection details (host, port, database, user, password) and tests the connection. If successful, execute a user-provided SQL query and return results as JSON. Store connection details encrypted in Supabase.
```

### 5. Code Export
```
Build a feature that generates a standalone React component from the dashboard layout. The component should include all necessary imports (Recharts), the layout structure, and sample data fetching code. Provide a "Copy to Clipboard" button.
```

## 📈 Success Metrics (Week 1 Post-Launch)

**Acquisition:**
- 50 signups (from Product Hunt + Twitter)
- 20 created dashboards

**Activation:**
- 10 users connected their database
- 5 users exported code

**Feedback:**
- 3 user interviews scheduled
- Identify top 2 friction points

## 💰 Monetization (V2 - Not MVP)

**Free Tier:**
- 1 dashboard
- 5 components max
- Community templates only

**Pro Tier ($20/mo):**
- Unlimited dashboards
- Unlimited components
- Premium templates
- Priority support

---

## Example 2: AI Writing Assistant for Developers

### User Request
"I want to build an AI tool that helps developers write better documentation."

### Launch Plan Output

```markdown
# 📱 DocuGenius - MVP Launch Plan

## 🎯 Core Problem & Solution

**Problem:** Developers hate writing documentation and often produce unclear, incomplete docs that confuse users.

**Solution:** AI assistant that reads your code and generates clear, comprehensive documentation in your project's style.

**Validation:**
- 200+ upvotes on Reddit r/programming for idea
- 80 developers joined waitlist in 48 hours
- Personal pain point: spent 3 hours documenting API last week

## 🚀 MVP Scope

### The ONE Core Feature
**Code-to-Docs Generator**
- Upload code file (JS, Python, Go, Rust)
- AI analyzes functions/classes
- Generates markdown documentation
- Download as .md file

### Supporting Features (2 essentials)
1. **GitHub Integration** - Connect repo, select files, bulk generate
2. **Style Presets** - Choose doc style (API reference, tutorial, README)

### NOT in V1 (ship later)
- ❌ Real-time collaboration
- ❌ Version control integration (track doc changes with code)
- ❌ Custom AI models (use GPT-4 only)
- ❌ Multi-language support (English only)
- ❌ Diagram generation
- ❌ Code examples generation (just document existing code)
- ❌ Team workspaces

## 🏗️ Tech Stack

**Frontend:**
- Next.js 14 (App Router)
- Tailwind CSS + shadcn/ui
- React Markdown for preview

**Backend:**
- Next.js Server Actions
- OpenAI API (GPT-4)
- GitHub API (OAuth)

**Database:**
- Supabase (PostgreSQL)

**Hosting:**
- Vercel

## 📊 Database Schema

```sql
create table users (
  id uuid primary key default uuid_generate_v4(),
  email text unique not null,
  github_username text,
  github_access_token text, -- encrypted
  created_at timestamptz default now()
);

create table documents (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references users(id) on delete cascade,
  title text not null,
  code_input text not null, -- original code
  markdown_output text not null, -- generated docs
  language text not null, -- js, python, go, etc.
  style text not null, -- api-reference, tutorial, readme
  created_at timestamptz default now()
);

-- Row Level Security
alter table documents enable row level security;

create policy "Users can CRUD own documents"
  on documents for all
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);
```

## 🗺️ 2-Week Sprint Plan

### Week 1: Foundation
**Day 1-2: Setup**
- Next.js project + Supabase
- Email authentication
- Landing page + dashboard layout

**Day 3-5: Core Feature**
- File upload component
- OpenAI API integration (prompt engineering for docs)
- Markdown preview component
- Download .md file

**Day 6-7: Style Presets**
- 3 style presets (API reference, tutorial, README)
- Prompt templates for each style
- Style selector UI

### Week 2: Polish & Ship
**Day 8-9: GitHub Integration**
- GitHub OAuth setup
- Repo file browser
- Bulk generate (select multiple files)

**Day 10-11: Polish & Testing**
- Loading states (AI generation takes 5-10s)
- Error handling (API limits, invalid code)
- Responsive design

**Day 12-13: Deploy & Final Testing**
- Vercel deployment
- Test with real codebases
- Edge case fixes

**Day 14: Launch**
- Product Hunt submission
- Post on Dev.to, Hacker News
- Share on Twitter with demo video

## 🎬 Starter Prompts for Claude Code

### 1. Initial Setup
```
Create a Next.js 14 project with Supabase authentication, Tailwind CSS, and shadcn/ui. Build a landing page and dashboard layout.
```

### 2. Core Feature
```
Build a file upload component that accepts code files (.js, .py, .go, .rs). Send the code to OpenAI GPT-4 with a prompt to generate documentation. Display the generated markdown in a preview panel using react-markdown. Add a download button to save as .md file.
```

### 3. GitHub Integration
```
Implement GitHub OAuth using Supabase. Create an API endpoint that fetches repository files using the GitHub API. Build a file browser UI that lets users select multiple files to generate docs for.
```

## 📈 Success Metrics (Week 1 Post-Launch)

**Acquisition:**
- 100 signups
- 50 documents generated

**Activation:**
- 20 users connected GitHub
- 10 users downloaded docs

**Feedback:**
- Survey: "How useful was the generated documentation?" (1-10)
- Top requested feature?

---

## Example 3: Micro-SaaS Idea Validator

### User Request
"I want to build a tool that helps indie hackers validate their SaaS ideas before building."

### Launch Plan Output

```markdown
# 📱 ValidateThis - MVP Launch Plan

## 🎯 Core Problem & Solution

**Problem:** Indie hackers waste months building products nobody wants because they skip validation.

**Solution:** Guided validation framework with competitor research, market size estimation, and demand signals analysis.

**Validation:**
- Personal pain: Built 2 failed products without validation
- 50+ indie hackers in Twitter poll said "I need this"
- Similar tool (IdeaBuddy) charges $49/mo and has 10k users

## 🚀 MVP Scope

### The ONE Core Feature
**Validation Report Generator**
- User describes idea (1 paragraph)
- AI analyzes: competition, market size, demand signals
- Generates validation report with GO/NO-GO recommendation
- Export as PDF

### Supporting Features (2 essentials)
1. **Competitor Finder** - Automatic Google/Twitter search for similar products
2. **Demand Checker** - Search Reddit, Twitter, forums for people asking for solution

### NOT in V1
- ❌ Save multiple ideas (one validation at a time)
- ❌ User accounts (anonymous usage)
- ❌ Share reports (download only)
- ❌ Custom validation criteria
- ❌ Historical data tracking
- ❌ Team collaboration

## 🏗️ Tech Stack

**Frontend:** Next.js 14 + Tailwind
**Backend:** Next.js Server Actions + OpenAI API
**Database:** None needed for MVP (stateless)
**Hosting:** Vercel

## 📊 Database Schema

```sql
-- V1 doesn't need database (stateless)
-- V2 will add user accounts and saved reports
```

## 🗺️ 2-Week Sprint Plan

### Week 1: Foundation
**Day 1-2:** Landing page + validation form
**Day 3-5:** OpenAI API integration (validation prompt)
**Day 6-7:** Report display + PDF export

### Week 2: Ship
**Day 8-9:** Competitor finder (web scraping API)
**Day 10-11:** Polish + testing
**Day 12-14:** Deploy + launch (Product Hunt, Twitter)

## 🎬 Starter Prompts for Claude Code

### 1. Landing Page
```
Create a landing page for "ValidateThis" - a tool that helps indie hackers validate SaaS ideas. Include hero section, benefits, and a CTA button to "Validate My Idea".
```

### 2. Validation Form
```
Build a form that collects: idea description (textarea), target audience (text), and estimated price (number). On submit, call a Server Action that sends data to OpenAI API with a validation prompt.
```

### 3. Report Generator
```
Create a validation report component that displays: market analysis, competition level, demand signals, and a GO/NO-GO recommendation with reasoning. Add a button to export as PDF using jsPDF.
```

---

**More Examples:**
- E-commerce analytics dashboard
- Customer feedback aggregator
- API monitoring tool
- Email template builder
- Social media scheduler

**Related:** See `TROUBLESHOOTING.md` for common planning issues.
