# Roadmap Builder - Reference Documentation

## Feature Prioritization Frameworks

### RICE Score (Reach, Impact, Confidence, Effort)

**Formula:**
```
RICE = (Reach × Impact × Confidence) / Effort

Where:
- Reach: How many users affected per time period (monthly)
- Impact: 3 = Massive, 2 = High, 1 = Medium, 0.5 = Low, 0.25 = Minimal
- Confidence: 100% = High, 80% = Medium, 50% = Low
- Effort: Person-months (0.5 = 2 weeks, 1 = 1 month)
```

**Example:**
```
Feature: Email notifications when form submitted

Reach: 1000 users/month (all users submit forms)
Impact: 2 (high - reduces checking manually)
Confidence: 100% (we know users want this)
Effort: 0.5 (1 week to build)

RICE = (1000 × 2 × 1.0) / 0.5 = 4000

Compare to:

Feature: Dark mode

Reach: 200 users/month (20% might use)
Impact: 0.5 (low - nice-to-have)
Confidence: 50% (some users asked)
Effort: 1 (2 weeks to do properly)

RICE = (200 × 0.5 × 0.5) / 1 = 50

DECISION: Build notifications first (4000 > 50)
```

### Value vs. Complexity Matrix

```
High Value, Low Complexity          High Value, High Complexity
┌──────────────────────┐           ┌──────────────────────┐
│                      │           │                      │
│   BUILD NOW          │           │   ROADMAP            │
│   (Quick Wins)       │           │   (Strategic Bets)   │
│                      │           │                      │
│ - Simple features    │           │ - Core innovations   │
│ - Small fixes        │           │ - Differentiators    │
│ - UI improvements    │           │ - Platform features  │
│                      │           │                      │
└──────────────────────┘           └──────────────────────┘

Low Value, Low Complexity           Low Value, High Complexity
┌──────────────────────┐           ┌──────────────────────┐
│                      │           │                      │
│   MAYBE              │           │   AVOID              │
│   (Backlog)          │           │   (Don't Build)      │
│                      │           │                      │
│ - Nice-to-haves      │           │ - Premature optim.   │
│ - Polish items       │           │ - Edge cases         │
│ - Minor features     │           │ - Vanity features    │
│                      │           │                      │
└──────────────────────┘           └──────────────────────┘
```

### The Kano Model (User Satisfaction)

**Three types of features:**

**1. Basic Expectations (Must-haves)**
- Users expect these by default
- Absence causes dissatisfaction
- Presence doesn't create delight
- Example: Auth, data persistence, core CRUD

**2. Performance Features (Linear satisfaction)**
- More is better
- Directly impacts satisfaction
- Example: Speed, reliability, accuracy

**3. Delighters (Unexpected wow factors)**
- Users don't expect them
- Presence creates delight
- Absence doesn't cause dissatisfaction
- Example: Smart defaults, automation, AI features

**Strategic approach:**
```
MVP: Focus on Basic Expectations only
V1.1: Add top Performance Features
V2.0: Add one Delighter (after you have traction)
```

## Product Metrics & Success Criteria

### North Star Metric

**Definition:** The ONE metric that best captures core value delivered to users.

**Good North Star metrics:**
- Slack: Daily Active Users sending messages
- Airbnb: Nights booked
- Netflix: Hours watched
- Notion: Weekly active users creating pages

**For SaaS:**
```
BAD: Sign-ups (vanity metric)
GOOD: Weekly Active Users (usage metric)

BAD: Number of features used
GOOD: Users completing core action weekly

BAD: Page views
GOOD: Time to first value
```

**Finding yours:**
```
Ask: What action represents value being delivered?

API Monitor → APIs being monitored actively
Dashboard Builder → Dashboards created and exported
Doc Generator → Documents generated and downloaded
```

### AARRR Funnel (Pirate Metrics)

```
Acquisition → How they find you
Activation → First value experience
Retention → Coming back
Revenue → Paying
Referral → Telling others
```

**Metrics at each stage:**

**Acquisition:**
- Traffic sources (organic, paid, referral)
- Sign-up rate (visitors → accounts)
- Cost per acquisition (if paid)

**Activation:**
- Time to first value
- % completing onboarding
- % completing core action

**Retention:**
- Day 1, Day 7, Day 30 retention
- Weekly/Monthly active users
- Churn rate

**Revenue:**
- Conversion to paid (if freemium)
- Average revenue per user (ARPU)
- Lifetime value (LTV)

**Referral:**
- Referral rate (% inviting others)
- Viral coefficient (< 1 = not viral)
- Word-of-mouth NPS

**Focus areas by stage:**
```
MVP (0-100 users): Activation only
- Get % completing core action > 40%

Growth (100-1000): Activation + Retention
- Get Day 7 retention > 30%

Scale (1000+): All metrics
- Optimize full funnel
```

## Roadmap Cadence & Planning

### Sprint Length Strategy

**Weekly sprints (solo dev):**
- Best for: MVPs, fast iteration
- Ship: 1-2 small features per week
- Review: Friday afternoon
- Plan: Monday morning (30 min)

**Bi-weekly sprints (small team):**
- Best for: Post-MVP products
- Ship: 3-5 features per sprint
- Review: Last Friday
- Plan: Following Monday (1 hour)

**Monthly releases (established product):**
- Best for: Mature products with users
- Ship: One major feature + fixes
- Plan: First week of month
- Announce: Changelog + email

### Roadmap Horizons

**Now (This sprint - 1-2 weeks):**
- Committed features
- Clear specs
- No scope changes

**Next (Following sprints - 1-2 months):**
- High-confidence features
- Rough specs
- May be reordered based on feedback

**Later (3-6 months):**
- Strategic bets
- Directional ideas
- Will change based on learning

**Never:**
- Features that don't strengthen core value prop
- Premature optimizations
- "Just in case" features

## User Feedback Processing

### Feature Request Triage

```
New request comes in →

1. Understand the underlying need
   "Why do you want this?"
   "What are you trying to accomplish?"
   "What happens if this doesn't exist?"

2. Check if existing features can solve it
   "Have you tried [existing feature]?"
   "Would [alternative approach] work?"

3. Assess request against criteria
   - Strengthens core value prop? YES/NO
   - Affects > 20% of users? YES/NO
   - Can build in < 1 week? YES/NO
   - Is this 3rd request for same need? YES/NO

4. Categorize
   ✅ 3+ YES → Consider for next sprint
   ⏸️ 1-2 YES → Backlog
   ❌ 0 YES → Politely decline
```

### The "5 User Rule"

**Don't build until 5 different users request the same underlying need.**

Example:
```
User 1: "I need CSV export"
User 2: "Can I export to Excel?"
User 3: "Add Google Sheets integration"
User 4: "Let me download my data"
User 5: "API endpoint to fetch all records"

PATTERN: Everyone wants to GET DATA OUT
BUILD: CSV export (simplest solution that solves all requests)
```

### Feedback Channels Hierarchy

**High signal (act on these):**
1. Paying customers asking for feature
2. Users churning because of missing feature
3. Multiple users requesting same thing
4. Users offering to pay for specific feature

**Medium signal (consider):**
5. Free users requesting feature
6. One-off requests with strong use case
7. Competitor has it and users mention

**Low signal (usually ignore):**
8. Random feature ideas with no context
9. Features you personally want
10. "Nice to have" with no pain point

## Competitive Analysis

### When to Care About Competitors

**DO consider competitors when:**
- They have a feature that 50%+ of your users ask for
- You're losing deals specifically because of missing feature
- Industry-standard expectation (e.g., SSO for enterprise)

**DON'T blindly copy when:**
- Competitor has feature but your users don't ask
- It would dilute your core differentiation
- It's complex and you can differentiate by being simpler

### Feature Gap Analysis

```markdown
| Feature | Competitor A | Competitor B | Your Product | User Requests |
|---------|--------------|--------------|--------------|---------------|
| Core Feature | ✅ | ✅ | ✅ | N/A (table stakes) |
| Export CSV | ✅ | ✅ | ❌ | 15 requests |
| Dark Mode | ✅ | ❌ | ❌ | 3 requests |
| API Access | ✅ | ✅ | ❌ | 8 requests |
| Mobile App | ✅ | ✅ | ❌ | 1 request |

DECISION:
- Build CSV export (high requests, competitive gap)
- Build API access (medium requests, competitive gap)
- Skip Dark Mode (low requests)
- Skip Mobile App (low requests, high effort)
```

## Technical Debt & Refactoring

### When to Prioritize Tech Debt

**Signals it's time:**
- Velocity slowing (features taking 2x as long)
- Bugs increasing (regressions on every deploy)
- Onboarding new devs takes > 2 weeks
- Fear of touching certain code

**When to defer:**
- No users yet (ship first, refactor later)
- Velocity still fast
- Team understands codebase
- Debt isn't blocking new features

### The 80/20 Rule for Refactoring

**Allocate sprint capacity:**
```
80% - New features (user-facing)
20% - Tech debt/refactoring (developer-facing)

Exception: Major architectural change
→ Full sprint dedicated to refactor
→ Communicate to users (no new features this sprint)
```

### Refactor Prioritization

**High priority (do soon):**
- Code blocking new features
- Security vulnerabilities
- Performance issues affecting users
- Frequent bug sources

**Low priority (defer):**
- "Not clean" but functional code
- Old libraries that still work
- "This could be better" feelings
- Aesthetic improvements

## Roadmap Communication

### Internal Roadmap (for team)

**Format:**
```markdown
## This Sprint (Week of Jan 15)
- [ ] Feature A: Detailed spec link
- [ ] Bug Fix B: GitHub issue #123
- [ ] Refactor C: Tech debt item

## Next Sprint (Week of Jan 22)
- [ ] Feature D: In review
- [ ] Feature E: Needs spec

## This Quarter (Q1 2024)
- Strategic Bet 1: Rough idea
- Strategic Bet 2: Under consideration
```

**Update frequency:** Weekly

### Public Roadmap (for users)

**What to include:**
- Now: Features in development (this month)
- Next: Validated features (next 2-3 months)
- Later: Strategic direction (6 months+)

**What NOT to include:**
- Specific dates (you'll miss them)
- Every small feature
- Technical debt items
- Unvalidated ideas

**Format (simple Notion page):**
```markdown
# Product Roadmap

Last updated: Jan 15, 2024

## 🚧 In Progress
- CSV export (shipping this week)
- API documentation improvements

## 🎯 Coming Soon (Next 2-3 months)
- API endpoints for data access
- Webhook notifications
- Team collaboration features

## 💡 Exploring (Under consideration)
- Mobile app
- Advanced analytics
- White-label options

## ✅ Recently Shipped
- Dark mode (Jan 10)
- Bulk import (Jan 3)
- Performance improvements (Dec 20)
```

## Resources

**Books:**
- Inspired by Marty Cagan
- The Lean Startup by Eric Ries
- Sprint by Jake Knapp

**Frameworks:**
- Jobs To Be Done (JTBD)
- Opportunity Solution Trees
- Lean Canvas

**Tools:**
- Linear (roadmap planning)
- Productboard (feature prioritization)
- Notion (simple public roadmap)
- Canny (feature voting)

---

**Related:** See `EXAMPLES.md` for complete roadmaps and `TROUBLESHOOTING.md` for prioritization issues.
