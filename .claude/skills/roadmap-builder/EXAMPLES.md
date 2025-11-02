# Roadmap Builder - Examples

## Example 1: Early-Stage SaaS Roadmap (Post-MVP)

### User Request
"I just launched my API monitoring tool. 50 users signed up this week. What should I build next?"

### Roadmap Output

```markdown
# 🗺️ Product Roadmap: APIWatch

## 🎯 Core Value Proposition
Real-time API monitoring with instant Slack alerts so developers fix issues before users notice.

## 📊 Current State Analysis (Week 1 Post-Launch)

**What's working:**
- 50 signups in first week (good Product Hunt traction)
- 15 users actively monitoring APIs (30% activation)
- Slack alerts working reliably
- Core monitoring loop stable

**Known friction points:**
- 10 users asked "How do I add my second API?"
- 5 users confused about alert settings
- 3 users want email alerts (currently Slack-only)
- Response time graph is slow to load

**Current focus:**
Users primarily monitoring 1-2 critical APIs. Using basic alerting. Not exploring advanced features yet.

---

## 🚫 DO NOT BUILD (Yet)

### Dashboard Analytics
**Why not:** Only 15 active users. You don't need analytics on 15 users - you can talk to them directly.
**Reconsider when:** 500+ active users and manual analysis becomes painful

### Team Collaboration (user roles, permissions)
**Why not:** 90% of users are solo developers. No one asked for this yet.
**Reconsider when:** 5+ users explicitly request it or you target larger teams

### Mobile App
**Why not:** Web works fine on mobile for checking status. Building native app is months of work.
**Reconsider when:** Users say "I need mobile app" more than "I need [specific feature]"

### Custom Dashboards
**Why not:** Premature - users barely using the default dashboard.
**Reconsider when:** Power users requesting specific customizations

---

## 🤔 MAYBE WORTH IT (Backlog - Low Priority)

### Dark Mode
**Impact:** Low | **Effort:** Low (2 days)
**Why it's backlog:** 3 users mentioned it. Nice to have but doesn't improve core value.
**Build only if:** Slow week and no higher-priority items

### Export Historical Data
**Impact:** Low | **Effort:** Medium (3 days)
**Why it's backlog:** 2 users asked. Not blocking anyone.
**Build only if:** Becomes common request (5+ users)

---

## 🎯 HIGH IMPACT, NEEDS VALIDATION (Next Month)

### Webhook Notifications
**Impact:** High | **Effort:** High (5 days)
**Value hypothesis:** Users want to trigger custom actions (create ticket, restart server) when API fails
**Validation needed:**
- Interview 5 users: "What would you do with webhooks?"
- Test: Would you upgrade to Pro for webhooks?
**Estimated effort:** 5 days (webhook system, security, docs)
**Priority:** February (after validating demand)

### Multi-Region Monitoring
**Impact:** High | **Effort:** High (7 days)
**Value hypothesis:** Global APIs need checks from multiple locations to catch regional outages
**Validation needed:**
- Survey: "Do you serve users in multiple regions?"
- Check: Are users' APIs global or regional?
**Estimated effort:** 7 days (infrastructure, latency testing)
**Priority:** March (strategic but requires validation)

---

## ✅ BUILD NOW (This Week)

### 1. Multiple API Support (UI Improvement)
**Impact:** High | **Effort:** Low (1 day)
**Why now:** 10 users explicitly asked "How do I add my second API?"
**Success metric:** 50% of users monitoring 2+ APIs within a week
**Estimated effort:** 1 day
**Technical approach:**
- Add "Add Another API" button to dashboard
- Show list of monitored APIs (not just one)
- Allow switching between API views

### 2. Email Alerts
**Impact:** High | **Effort:** Low (2 days)
**Why now:**
- 5 users requested it
- Removes Slack dependency (increases activation)
- Table stakes feature (expected by users)
**Success metric:** 20% of users enable email alerts
**Estimated effort:** 2 days (email service integration, template design)
**Technical approach:**
- Integrate SendGrid/Resend
- Email template for alerts
- User settings for email preferences

### 3. Response Time Performance Fix
**Impact:** Medium | **Effort:** Low (1 day)
**Why now:** Users complain graph is slow. Easy fix, improves UX.
**Success metric:** Graph loads in < 1 second
**Estimated effort:** 1 day (optimize query, add caching)
**Technical approach:**
- Add database index on timestamp
- Cache last 24h of data
- Lazy load historical data

---

## 📅 Suggested Sprint Sequence

### Sprint 1 (This Week - Jan 15-19)
**Goal:** Remove friction for existing users

- [x] Day 1-2: Multiple API support UI
- [x] Day 3-4: Email alerts integration
- [x] Day 5: Response time performance fix

**Ship:** Friday Jan 19
**Announce:** Changelog + email to 50 users

### Sprint 2 (Next Week - Jan 22-26)
**Goal:** Validate webhook demand

- [ ] Day 1: User interviews (5 calls)
- [ ] Day 2-3: Build webhook prototype (if validated)
- [ ] Day 4-5: Test with 3 beta users

**Decision:** If 4/5 users say "I'd use this weekly" → build it
If not → defer and focus on activation improvements

### Sprint 3 (Week After - Jan 29-Feb 2)
**Goal:** Improve activation rate (currently 30%)

- [ ] Analyze: Where do users drop off?
- [ ] Build: Onboarding improvements
- [ ] Test: A/B test new onboarding flow

**Success:** Activation > 40% (from 30%)

---

## 📈 Success Metrics to Track

**Acquisition (signups):**
- Target: 100 signups by end of month
- Measure: Weekly signup count

**Activation (users monitoring APIs):**
- Current: 30% (15/50)
- Target: 40% by end of month
- Measure: % users with >= 1 API monitored

**Retention (coming back):**
- Target: 40% Day 7 retention
- Measure: Users checking dashboard in week 2

**Feedback:**
- Target: 10 user interviews completed
- Identify: Top 3 requested features

**Decision Rules:**
- If activation < 35% after sprint 2 → Focus on onboarding (not new features)
- If users request same feature 5+ times → Add to "Build Now"
- If user says feature is blocking paid upgrade → Prioritize immediately

---

## 🔄 Roadmap Review Cadence

**Weekly (every Friday):**
- Did we ship what we committed?
- What feedback did we get?
- Adjust next week's priorities

**Monthly (first Monday):**
- Review metrics (signups, activation, retention)
- Update roadmap based on learning
- Communicate changes to users (public changelog)

**Quarterly (every 3 months):**
- Major roadmap revision
- Evaluate if core value prop still resonates
- Consider pivots if metrics aren't improving
```

---

## Example 2: Feature Request Triage

### User Request
"Users are asking for 10 different features. Help me decide what to build."

### Analysis Output

```markdown
# Feature Request Analysis

## Requests Received (Last 30 Days)

### REQUEST #1: Dark Mode
**Requested by:** 3 users
**Underlying need:** Prefer dark UI for night work
**Current workaround:** Browser dark mode extension
**RICE Score:**
- Reach: 50 users (assume 20% might use) = 10 users/month
- Impact: 0.5 (low - cosmetic preference)
- Confidence: 50% (small sample size)
- Effort: 0.5 (1 week with proper implementation)
- **RICE = (10 × 0.5 × 0.5) / 0.5 = 5**

**DECISION:** ⏸️ BACKLOG - Nice-to-have but low impact

---

### REQUEST #2: CSV Export
**Requested by:** 12 users
**Underlying need:** Want data in Excel for reporting to management
**Current workaround:** Manual copy-paste from UI
**RICE Score:**
- Reach: 100 users (assume all users export monthly) = 100 users/month
- Impact: 2 (high - removes manual work)
- Confidence: 100% (many users requested, clear need)
- Effort: 0.25 (2-3 days implementation)
- **RICE = (100 × 2 × 1.0) / 0.25 = 800**

**DECISION:** ✅ BUILD NOW - High impact, low effort, clear demand

---

### REQUEST #3: Mobile App
**Requested by:** 5 users
**Underlying need:** Want to check status on phone
**Current workaround:** Web app on mobile browser (works but not optimized)
**RICE Score:**
- Reach: 100 users (all users check mobile occasionally) = 100 users/month
- Impact: 1 (medium - improves mobile experience)
- Confidence: 60% (web version works, is native really needed?)
- Effort: 3 (3 months - iOS + Android)
- **RICE = (100 × 1 × 0.6) / 3 = 20**

**DECISION:** ❌ DO NOT BUILD - High effort for unclear impact. Make web responsive first.

---

### REQUEST #4: Webhook Alerts
**Requested by:** 8 users
**Underlying need:** Auto-create Jira ticket / Restart server / Trigger PagerDuty when alert fires
**Current workaround:** Manual action after seeing Slack alert
**RICE Score:**
- Reach: 300 users (if we get more power users) = 300 users/month
- Impact: 3 (massive - enables automation)
- Confidence: 80% (clear use cases, multiple requests)
- Effort: 1 (2 weeks - webhook system + docs)
- **RICE = (300 × 3 × 0.8) / 1 = 720**

**DECISION:** ✅ BUILD NEXT SPRINT - High impact, medium effort, validated demand

---

### REQUEST #5: Team Collaboration
**Requested by:** 2 users
**Underlying need:** Want multiple team members to see same dashboard
**Current workaround:** Share login credentials (bad security)
**RICE Score:**
- Reach: 20 users (only larger teams need this) = 20 users/month
- Impact: 2 (high for those who need it)
- Confidence: 50% (only 2 requests, might not be widespread need)
- Effort: 2 (4 weeks - user management, permissions)
- **RICE = (20 × 2 × 0.5) / 2 = 10**

**DECISION:** ⏸️ DEFER - Wait for 5+ requests before building

---

## Priority Ranking (by RICE Score)

1. **CSV Export (800)** → Build this sprint
2. **Webhook Alerts (720)** → Build next sprint
3. **Mobile App (20)** → Backlog (low priority)
4. **Team Collaboration (10)** → Defer until more demand
5. **Dark Mode (5)** → Backlog (nice-to-have)

---

## Recommended Sprint Plan

**This Sprint:**
- CSV Export (2-3 days)
- Quick wins: Fix 2-3 small bugs

**Next Sprint:**
- Webhook Alerts (2 weeks)
- Validate: Interview 5 users about use cases first

**Next Month:**
- Monitor: Track if more users request team features
- Build: Only if 5+ users request it

**Never (or much later):**
- Mobile App: Make web responsive instead
- Dark Mode: Build only if user count grows and requests increase
```

---

## Example 3: Technical Debt vs. Features

### User Request
"Should I refactor my messy codebase or build new features users are asking for?"

### Decision Framework Output

```markdown
# Technical Debt Assessment

## Current State

**Codebase health:**
- 6 months old, ~15k lines of code
- Test coverage: 40%
- No type safety (vanilla JS, considering TypeScript)
- Some duplicated code (3 similar API endpoint patterns)
- Works fine, but adding features takes longer than month 1

**User requests:**
- 10 users want CSV export
- 8 users want webhook alerts
- 5 users want email notifications

---

## Debt Analysis

### DEBT ITEM #1: Add TypeScript
**Pain level:** Medium
- Occasionally causes runtime bugs
- Slows down development (fear of breaking things)
- Not blocking new features yet

**Effort:** 2 weeks (convert all files, add types)

**DECISION:** ⏸️ DEFER
**Why:** Not blocking new features. Velocity still acceptable. Convert new files to TS incrementally instead.

**Alternative:** Start writing new code in TypeScript, convert old code opportunistically.

---

### DEBT ITEM #2: Add Integration Tests
**Pain level:** High
- Manual testing takes 30 min before each deploy
- Broke webhook feature twice last month
- Fear of deploying on Fridays

**Effort:** 1 week (set up test framework, write critical path tests)

**DECISION:** ✅ BUILD NOW
**Why:** Blocking confident shipping. 1 week investment will save hours weekly.

**Plan:** Allocate 1 sprint to testing infrastructure before building more features.

---

### DEBT ITEM #3: Refactor Duplicated API Code
**Pain level:** Low
- 3 similar endpoint patterns copy-pasted
- Works fine, just not DRY
- Aesthetic issue, not functional

**Effort:** 2 days

**DECISION:** ⏸️ DEFER
**Why:** Not causing bugs. Not slowing velocity. Fix when touching that code next.

---

## Recommended Sprint Plan

### Sprint 1 (This Week)
**Theme:** Testing Infrastructure

- [ ] Set up Jest/Vitest
- [ ] Write integration tests for critical paths (auth, alerts, monitoring)
- [ ] Add GitHub Actions CI

**Skip features this sprint** - communicate to users: "Improving reliability this week, new features next week"

### Sprint 2 (Next Week)
**Theme:** High-value features

- [ ] CSV Export (user request #1 - 3 days)
- [ ] Email Notifications (user request #3 - 2 days)

**Now you can ship confidently with tests**

### Sprint 3 (Week After)
**Theme:** Continue features

- [ ] Webhook Alerts (5 days)

**Convert to TypeScript incrementally** - 20% of sprint time on new code only

---

## Decision Framework

**When to prioritize tech debt:**
- [ ] Velocity slowing (features taking 2x longer)
- [ ] Bugs increasing (breaking things on every deploy)
- [ ] Fear of shipping (manual testing > 30 min)
- [ ] Onboarding new dev would take > 1 week

**When to prioritize features:**
- [ ] Users explicitly asking
- [ ] Debt not blocking velocity
- [ ] Need to learn from user feedback
- [ ] Clear market demand

**Current situation:**
- ✅ Velocity slowing slightly (but manageable)
- ✅ Bugs increasing (broke webhooks twice)
- ✅ Fear of shipping (manual testing painful)
- ❌ Onboarding not relevant (solo dev)

**VERDICT:** Invest 1 sprint in testing infrastructure, then back to features.

---

## 80/20 Rule Going Forward

**Sprint capacity allocation:**
- 80% features (user-facing value)
- 20% tech debt (developer-facing quality)

**Example Sprint:**
- 4 days: New features
- 1 day: Add tests, refactor opportunistically

This prevents debt from piling up while maintaining feature velocity.
```

---

**Related:** See `REFERENCE.md` for prioritization frameworks and `TROUBLESHOOTING.md` for common roadmap issues.
