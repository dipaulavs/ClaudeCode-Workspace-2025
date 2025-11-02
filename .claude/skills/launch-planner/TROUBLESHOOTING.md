# Launch Planner - Troubleshooting

## Common Problems & Solutions

---

## Problem 1: Scope Creep During Planning

### Symptoms
- MVP plan includes 10+ features
- "Core feature" is actually 3 features bundled
- User keeps adding "just one more thing"
- Timeline extends beyond 2-4 weeks

### Root Cause
- Difficulty saying no to good ideas
- Fear of shipping incomplete product
- Comparing to mature competitors
- Not understanding MVP purpose

### Solution

**Step 1: Identify the ONE thing**
Ask the forcing question:
> "If you could only ship ONE feature in week 1, what would create value for users?"

**Step 2: Apply the 80/20 rule**
```
Which features deliver 80% of the value?
├─ Feature A: 50% of value (CORE)
├─ Feature B: 25% of value (INCLUDE)
├─ Feature C: 15% of value (INCLUDE)
├─ Feature D: 7% of value (V2)
└─ Feature E: 3% of value (V2)
```

**Step 3: Use the "Defer to V2" framework**
For each feature, ask:
1. Can users accomplish their goal without this?
2. Can I manually handle this for first 10 users?
3. Will users leave if this doesn't exist?

If answers are YES, NO, NO → defer to V2.

**Example dialogue:**
```
User: "I also need user profiles, notifications, and a feed."

You: "Let's test that against our core value prop: 'Generate dashboards from database connections.'

- User profiles: Users can generate dashboards without profiles. V2.
- Notifications: What would we notify about? We don't have user actions yet. V2.
- Feed: Who would see it? We're single-user for MVP. V2.

For V1, let's focus on: connect database → generate dashboard → export code.
That's the full value loop. Agree?"
```

---

## Problem 2: Tech Stack Paralysis

### Symptoms
- User asks: "Should I use X or Y?"
- Long debates about framework choices
- Research phase taking days
- Over-optimization for scale

### Root Cause
- Fear of choosing wrong tool
- Premature optimization
- Trying to future-proof
- Analysis paralysis

### Solution

**Use the Default Stack Decision Tree:**

```
Does user have strong preference/experience?
├─ YES → Use their stack (faster for them)
└─ NO → Use default (Next.js + Supabase + Vercel)

Special requirements?
├─ Real-time collaboration → Add Supabase Realtime
├─ Heavy client state → Add Zustand/Jotai
├─ Complex forms → Add React Hook Form
└─ None → Stick to defaults
```

**Quick decision framework:**

| User Says | Default Answer | Why |
|-----------|----------------|-----|
| "React or Vue?" | React | Larger ecosystem, more jobs, better docs |
| "Supabase or Firebase?" | Supabase | Open source, PostgreSQL, better DX |
| "Tailwind or CSS-in-JS?" | Tailwind | Faster, smaller bundle, easier responsive |
| "REST or GraphQL?" | REST | Simpler, less setup, fine for MVP |
| "Vercel or AWS?" | Vercel | Zero config, preview deploys, cheaper for MVP |

**Response template:**
```
"Let's use [DEFAULT STACK]. It's optimized for shipping fast, which is our goal.

We can always migrate later if needed, but 99% of MVPs never need to.

The stack choice matters less than shipping. Sound good?"
```

---

## Problem 3: Unclear Value Proposition

### Symptoms
- Can't explain product in one sentence
- "It's like X but for Y" comparisons
- Multiple different target audiences
- Vague benefits ("makes things easier")

### Root Cause
- Trying to serve too many use cases
- Fear of being too niche
- Not understanding user's actual problem
- Feature-focused instead of outcome-focused

### Solution

**Use the Value Prop Formula:**

```
[Product Name] helps [specific audience] [accomplish outcome] by [unique approach].
```

**Bad examples:**
- "A platform for managing data" (vague)
- "Slack for developers" (comparison without differentiation)
- "Makes documentation easier" (how?)

**Good examples:**
- "DocuGenius helps developers create comprehensive documentation by analyzing their code with AI."
- "DashForge helps SaaS developers build admin dashboards by generating React components from database connections."

**Extraction Process:**

Ask user these questions:
1. **Who is this for specifically?** (not "everyone")
2. **What outcome do they want?** (not feature, outcome)
3. **Why can't they achieve it today?** (the gap)
4. **What's your unique approach?** (how you're different)

**Example dialogue:**
```
User: "It's a tool for managing social media."

You: "Let's get more specific:

1. Who specifically? Marketing teams? Solo creators? Agencies?
2. What outcome? Schedule posts? Analyze engagement? Generate content?
3. Why existing tools don't work? Too expensive? Too complex? Missing feature?
4. What's different about your approach? AI-powered? Free tier? Design-focused?

This helps us focus the MVP on solving one problem really well."
```

---

## Problem 4: Overengineered Database Schema

### Symptoms
- 10+ tables in MVP schema
- Complex many-to-many relationships
- Abstract base classes/inheritance
- Normalization to 4th or 5th normal form
- JSON fields avoided (trying to be "proper")

### Root Cause
- Coming from enterprise background
- Following "best practices" blindly
- Optimizing for future scale
- Fear of technical debt

### Solution

**MVP Database Rules:**

1. **2-4 tables maximum** for V1
2. **Use JSONB liberally** for flexible/nested data
3. **Denormalize if it simplifies** (normalize later)
4. **Add foreign keys** (but don't over-index)
5. **Skip migrations** (use Supabase UI for V1)

**Simplification Examples:**

**BEFORE (overengineered):**
```sql
-- 7 tables for a simple product catalog
create table products (id, name, description, created_at);
create table categories (id, name);
create table product_categories (product_id, category_id);
create table tags (id, name);
create table product_tags (product_id, tag_id);
create table images (id, product_id, url, order);
create table prices (id, product_id, currency, amount, valid_from, valid_to);
```

**AFTER (MVP-ready):**
```sql
-- 1 table, JSONB for flexibility
create table products (
  id uuid primary key,
  name text not null,
  description text,
  price numeric not null,
  categories text[], -- Simple array
  tags text[],
  images jsonb, -- [{"url": "...", "order": 1}]
  created_at timestamptz default now()
);
```

**Decision Framework:**

```
Do I need to query/filter by this field independently?
├─ YES → Separate column/table
└─ NO → JSONB

Will I have millions of rows?
├─ YES → Normalize
└─ NO (< 100k) → Denormalize for simplicity
```

---

## Problem 5: No Clear Success Metrics

### Symptoms
- Can't define what "success" means for MVP
- No concrete numbers or targets
- "Let's just see what happens" attitude
- No way to measure if features work

### Root Cause
- Avoiding accountability
- Not thinking about post-launch
- Focusing on building, not validating
- No hypothesis to test

### Solution

**MVP Success Framework:**

Define 3 metrics:
1. **Acquisition:** How many sign up?
2. **Activation:** How many complete core action?
3. **Feedback:** What do they say?

**Week 1 Post-Launch Targets (realistic):**
```
Conservative:
- 20 signups
- 5 activated users (25%)
- 3 qualitative feedback responses

Optimistic:
- 100 signups (good Product Hunt launch)
- 30 activated users (30%)
- 10 feedback responses
```

**Core Action Definition:**

Must be the ONE thing that delivers value:
- DocuGenius: Generate and download documentation
- DashForge: Create dashboard and export code
- ValidateThis: Complete validation and view report

**Example metrics section for PRD:**

```markdown
## 📈 Success Metrics (Week 1 Post-Launch)

**Acquisition:**
- Target: 50 signups from Product Hunt + Twitter
- Measure: Supabase user count

**Activation:**
- Target: 20 users complete core action (40%)
- Measure: Database query for users with >= 1 [completed_action]

**Retention (optional for MVP):**
- Target: 5 users return within 7 days
- Measure: Login activity

**Feedback:**
- Target: 10 user interviews scheduled
- Identify: Top 2 friction points blocking activation

**Decision Rule:**
- If < 30% activation → UX problem, fix onboarding
- If < 10 signups → Marketing problem, try different channels
- If low engagement → Value prop problem, pivot or iterate
```

---

## Problem 6: "But What About [Edge Case]?"

### Symptoms
- User raises 10+ edge cases during planning
- Planning stalls on "what if" scenarios
- Every feature gets complex exception handling
- Timeline doubles to handle edge cases

### Root Cause
- Perfectionism
- Enterprise mindset (handle all cases upfront)
- Fear of users encountering errors
- Not understanding MVP philosophy

### Solution

**The Edge Case Rule:**

```
Will this edge case affect > 80% of users in week 1?
├─ YES → Handle it
└─ NO → Defer to V2 (show error message)
```

**Example edge cases to SKIP in MVP:**

| Edge Case | V1 Solution | V2 Solution |
|-----------|-------------|-------------|
| User uploads 10GB file | Show error: "Max 10MB" | Stream processing |
| Database has 10M rows | Show error: "Max 100k rows" | Pagination/streaming |
| Connection times out | Show error: "Try again" | Retry logic |
| Unicode in names | Show error: "ASCII only" | Full Unicode support |
| Simultaneous edits | Last write wins | Conflict resolution |

**Response Template:**

```
"Great question. For V1, if [edge case] happens, we'll show an error message: '[User-friendly error]'

This lets us launch in 2 weeks. If more than 10% of users hit this, we'll prioritize it for V2.

For now, let's focus on the happy path for the 90% use case. Agree?"
```

---

## Problem 7: Fear of Launching "Incomplete" Product

### Symptoms
- "Just one more feature before launch"
- Delaying launch for polish
- Comparing MVP to mature competitors
- Wanting to perfect everything first

### Root Cause
- Fear of judgment/criticism
- Misunderstanding MVP purpose
- Perfectionism
- Not seeing MVPs in the wild

### Solution

**MVP Reality Check:**

Show examples of successful "incomplete" V1s:

**Stripe V1:**
- 7 API endpoints only
- No web dashboard (API-only)
- Only worked in US
- Manual review for every signup

**Twitter V1:**
- No images, videos, or GIFs
- No retweets
- No hashtags
- Just text posts

**Figma V1:**
- Single-user only (no collaboration)
- Web-only (no desktop app)
- Limited shapes and tools
- No plugins

**The Launching Mantra:**

> "If you're not embarrassed by V1, you launched too late."
> — Reid Hoffman, LinkedIn founder

**Action Plan:**

1. **Set a launch deadline** (e.g., Friday 2 weeks from now)
2. **Define "launch-ready" criteria:**
   - Core feature works end-to-end
   - Sign up flow functions
   - One perfect happy path
   - Error handling for obvious failures
3. **Commit publicly** (tweet launch date)
4. **Launch no matter what**

**Response Template:**

```
"I hear you wanting to add [feature] before launch. Let's ask:

Can users get value from the core feature without it?
- If YES → V2. Launch now, add later based on feedback.
- If NO → Must have, but let's simplify it.

Remember: V1 is about learning, not perfection.

Users won't expect a polished product from a solo dev. They'll be excited to be early and give feedback.

Let's commit to launching in 2 weeks with [CORE FEATURE ONLY]. You can always add [extra feature] in V1.1 the following week.

Sound good?"
```

---

## Decision Flowchart: "Should I Add This Feature?"

```
Is this the core value prop?
├─ YES → Include
└─ NO ↓

Can users accomplish their goal without it?
├─ YES → V2
└─ NO ↓

Can I manually handle this for first 10 users?
├─ YES → V2 (do it manually first)
└─ NO ↓

Is it blocking the happy path?
├─ YES → Simplify and include
└─ NO → V2
```

---

## Quick Reference: When User Says...

| User Says | Your Response |
|-----------|---------------|
| "Should I use X or Y framework?" | "Let's use [DEFAULT]. Speed matters more than the perfect choice for MVP." |
| "What about [edge case]?" | "Show an error message for V1. We'll add handling if > 10% of users hit it." |
| "I need [complex feature]" | "What outcome are you trying to enable? Let's find the simplest version." |
| "Should I add [nice-to-have]?" | "Can users accomplish their goal without it? If yes, V2." |
| "Is 2 weeks realistic?" | "Yes, if we focus on ONE core feature. Here's the sprint plan..." |
| "I'm not ready to launch" | "If you're not embarrassed by V1, you launched too late. Let's set a date." |

---

**Related:** See `REFERENCE.md` for technical deep dives and `EXAMPLES.md` for complete MVP plans.
