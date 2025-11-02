# Roadmap Builder - Troubleshooting

## Common Problems & Solutions

---

## Problem 1: Building Everything Users Ask For

### Symptoms
- Backlog has 50+ feature requests
- Building features no one uses
- Roadmap changes every week based on latest request
- Losing focus on core value prop

### Root Cause
- Fear of saying no to users
- Confusing requests with needs
- No prioritization framework
- Trying to please everyone

### Solution

**The "5 User Rule"**

Don't build until 5 different users request the same underlying need.

```markdown
EXAMPLE:

User 1: "Add PDF export"
User 2: "I need to download reports"
User 3: "Can you email me the data?"
User 4: "Excel export would be great"
User 5: "API endpoint to fetch results"

ANALYSIS:
❌ DON'T build 5 separate features
✅ DO identify pattern: Everyone wants DATA OUT

BUILD: CSV export (solves 4/5 requests simply)
DEFER: API (complex, only 1 request)
```

**The "Underlying Need" Question**

When user requests feature, ask:
```
1. "Why do you want this?"
2. "What are you trying to accomplish?"
3. "What would you do if this feature didn't exist?"

EXAMPLE:

User: "I need dark mode"

You: "Why dark mode specifically?"
User: "I work at night and the white background hurts my eyes"

You: "What if we just reduced the brightness of the interface?"
User: "That would work too"

SOLUTION: Reduce contrast (2 hours) instead of full dark mode (2 weeks)
```

**When to Say No**

Use this script:
```
"Thanks for the suggestion! We're focusing on [core value prop] right now.

If this becomes a common request (we track all feedback), we'll prioritize it.

For now, here's a workaround: [alternative solution]"
```

---

## Problem 2: Constant Context Switching

### Symptoms
- Starting 5 features, finishing none
- Always "almost done" but nothing ships
- Users asking "what happened to [feature]?"
- Low sense of accomplishment

### Root Cause
- No sprint commitment
- Reacting to latest urgent request
- Underestimating task complexity
- Poor time management

### Solution

**Weekly Sprint Commitment**

```markdown
MONDAY PLANNING:

1. Pick 1-2 features for the week
2. Write them down
3. Commit publicly ("Shipping [X] this week")
4. Say NO to everything else until Friday

FRIDAY REVIEW:

Did you ship what you committed?
- YES → Celebrate, plan next week
- NO → Why? Adjust estimates, try again
```

**The "Finish First" Rule**

```
Before starting new feature, ask:
"Is there something 80% done I should finish first?"

If YES → Finish it
If NO → Start new feature

AVOID: 5 features at 80% done
PREFER: 4 features shipped, 1 in progress
```

**Context Switch Budget**

```
Maximum 2 active tasks per week:
- Main feature (80% of time)
- Small fix/improvement (20% of time)

Emergency? Replace one task, don't add.
```

---

## Problem 3: Feature Graveyard (Built but Unused)

### Symptoms
- Built 10 features, users use 2
- No idea which features are valuable
- Wasted months on unused code
- Users don't discover new features

### Root Cause
- Building before validating demand
- No usage tracking
- Poor feature discovery
- Building for yourself, not users

### Solution

**Validate Before Building**

```markdown
INSTEAD OF:
"User asked for webhooks → Build webhooks"

DO THIS:
1. Ask 5 users: "Would you use webhooks?"
2. If 4/5 say yes: "What would you hook up to?"
3. Build simple prototype (1 day)
4. Test with 3 beta users
5. If they use it weekly → Build full version
6. If not → Discard, try different approach
```

**Measure Everything**

```javascript
// Track feature usage
analytics.track('CSV_Export_Used', {
  user_id: user.id,
  timestamp: new Date()
});

// Review monthly
"CSV Export: Used by 40% of users (build more export formats)
 Dark Mode: Used by 5% of users (low priority)
 API Access: Used by 2% of users (consider deprecating)"
```

**Feature Announcement Checklist**

When shipping new feature:
- [ ] In-app notification (banner/modal)
- [ ] Email to all users
- [ ] Changelog entry
- [ ] Tweet/social post
- [ ] Update onboarding to highlight it

**The 20% Usage Rule**

```
If < 20% of users use feature 30 days after launch:
→ Investigate why (poor discoverability? Wrong feature?)
→ Consider removing (reduces maintenance burden)

Example:
"We built custom dashboards. Only 3% of users created one.
Turns out default dashboard was good enough.
DECISION: Remove feature, simplify codebase."
```

---

## Problem 4: Analysis Paralysis (Can't Decide What to Build)

### Symptoms
- Spending days debating features
- No clear winner in prioritization
- Asking for more user feedback endlessly
- Roadmap stuck, nothing shipping

### Root Cause
- Trying to make perfect decision
- Fear of building wrong thing
- Over-analyzing without evidence
- No decision-making framework

### Solution

**The "Build Small" Approach**

```markdown
INSTEAD OF:
"Should we build Feature A or Feature B?" (3 days of debate)

DO THIS:
1. Build simplest version of both (1 day each)
2. Ship to 10 users each
3. Measure which one gets used more
4. Invest in the winner

TIME SAVED: 1 day (vs 3 days debating + risk of wrong choice)
```

**The Forcing Function**

```
Set a timer: 30 minutes to decide

Use RICE scoring:
- Feature A: RICE = 240
- Feature B: RICE = 180

DECISION: Build Feature A (higher score)

If close (< 20% difference): Pick either, ship faster matters more
```

**The "Reversible Decision" Framework**

```
Is this decision reversible?

YES (most features) → Decide in 30 min, ship, learn
NO (database migration, API breaking changes) → Take time, plan carefully

EXAMPLE:

Reversible: "Should we show 10 or 20 items per page?"
→ Pick one, ship, A/B test, change if wrong (1 hour)

Irreversible: "Should we switch from SQL to NoSQL?"
→ Analyze, prototype, test thoroughly (2 weeks)
```

---

## Problem 5: Ignoring Technical Debt Until It's Painful

### Symptoms
- Features that used to take 2 days now take 2 weeks
- Afraid to change code (might break things)
- Bugs appearing faster than you fix them
- New dev would take month to onboard

### Root Cause
- "Ship features first, fix later"
- Debt compounds silently
- No time allocated for quality
- Code reviews skipped

### Solution

**The 80/20 Sprint Allocation**

```markdown
Every sprint:
- 80% features (4 days)
- 20% quality (1 day)

Quality day tasks:
- Add tests for new features
- Refactor code touched this week
- Fix top 3 annoying bugs
- Update docs
```

**The "Boy Scout Rule"**

```
"Leave code better than you found it"

When touching file:
- Add 1 test
- Fix 1 code smell
- Update 1 outdated comment

Small improvements compound.
```

**Debt Threshold Triggers**

```
TRIGGER: Feature velocity slowing
SYMPTOMS: Features taking 2x longer than 3 months ago
ACTION: Dedicate 1 full sprint to refactoring

TRIGGER: Bugs increasing
SYMPTOMS: 5+ bugs reported per week (was 1-2)
ACTION: Add integration tests, fix root causes

TRIGGER: Fear of shipping
SYMPTOMS: Manual testing > 30 minutes
ACTION: Add automated tests for critical paths
```

---

## Problem 6: Premature Scaling/Optimization

### Symptoms
- Building features for future users (not current)
- Optimizing for 1M users when you have 100
- Complex architecture for simple problems
- Over-engineering everything

### Root Cause
- Fear of having to refactor later
- Following "best practices" blindly
- Comparing to established companies
- Perfectionism

### Solution

**The Current Scale Question**

```
Before building, ask:
"What's the minimum that works for my CURRENT users?"

EXAMPLE:

Current: 100 users
Premature: "Build distributed caching for 1M QPS"
Right-sized: "Add basic Redis cache, scales to 10k users"

Current: Solo dev
Premature: "Set up CI/CD with 15 stages"
Right-sized: "Deploy with git push, add tests later"

Current: 10 sign-ups/day
Premature: "Build complex fraud detection"
Right-sized: "Manual review for first 1000 users"
```

**The 10x Rule**

```
Build for 10x current scale, not 100x.

Current: 100 users → Build for 1,000
Don't: Build for 100,000 (you'll pivot before then)

Current: $1k MRR → Optimize for $10k
Don't: Optimize for $100k (product will change)
```

**The "You Aren't Gonna Need It" (YAGNI) Test**

```
Before adding complexity, ask:
"Do I need this TODAY?"

NO → Don't build it

EXAMPLE:

"Should I support multiple currencies?"
→ Do you have international users TODAY? NO → Don't build
→ Someone asking to pay in EUR? NO → Don't build
→ When yes: Build for that ONE currency, not all 180
```

---

## Problem 7: Roadmap Doesn't Align with Metrics

### Symptoms
- Building features but metrics not improving
- Activation rate still 20% after 5 features
- Churn increasing despite new features
- No clear connection between work and outcomes

### Root Cause
- Building without hypothesis
- Not tracking impact of features
- Vanity metrics instead of actionable
- No review process

### Solution

**Feature Hypothesis Template**

```markdown
BEFORE building, write:

## Feature: CSV Export

**Hypothesis:**
Adding CSV export will increase activation from 30% to 40%
because users currently abandon when they can't get data out.

**How we'll measure:**
- % of users who export CSV (target: 50%)
- Activation rate (target: 40%, currently 30%)
- Time in product after first export (target: +5 min)

**Success criteria (30 days after launch):**
- 50%+ users export CSV at least once
- Activation improves from 30% → 35%+

**If hypothesis is wrong:**
- Activation doesn't improve → Problem is elsewhere (investigate onboarding)
- Users don't export → Maybe they don't need data out (remove feature)
```

**Monthly Metrics Review**

```markdown
LAST MONTH:
✅ Shipped: CSV Export, Email Alerts
📊 Metrics:
- Activation: 30% → 34% (+4% - good!)
- Retention: 25% → 27% (+2% - slight improvement)
- Signups: 200 → 240 (+40 - growing)

ANALYSIS:
CSV Export working (users using it)
Email Alerts not moving retention (investigate why)

THIS MONTH FOCUS:
- Keep building activation features (working)
- Fix retention (email alerts not enough)
- Hypothesis: Users churn because no value after initial setup
- Test: Add weekly digest email with insights
```

**The North Star Metric**

```
Pick ONE metric that represents value delivered:

API Monitor → # of APIs being actively monitored
Dashboard Builder → # of dashboards created and used
Doc Generator → # of documents generated per user

Build features that improve THIS metric.
Ignore features that don't.
```

---

## Quick Reference: Decision Flowcharts

### Should I Build This Feature?

```
5+ users requested it?
├─ NO → Backlog (wait for more requests)
└─ YES ↓

Strengthens core value prop?
├─ NO → Politely decline
└─ YES ↓

Can I build in < 1 week?
├─ NO → Can I build smaller version? → YES: Build small | NO: Defer
└─ YES ↓

✅ BUILD NOW (add to sprint)
```

### Feature Not Being Used?

```
< 20% usage after 30 days?
├─ NO → Feature is successful
└─ YES ↓

Is it discoverable?
├─ NO → Improve announcement, add to onboarding
└─ YES ↓

Did users actually want this?
├─ NO → Consider removing (reduces complexity)
└─ YES → Interview users: Why not using?
```

---

**Related:** See `REFERENCE.md` for prioritization frameworks and `EXAMPLES.md` for complete roadmaps.
