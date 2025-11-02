# Marketing Writer - Reference Documentation

## Copywriting Frameworks

### The AIDA Framework (Attention, Interest, Desire, Action)

**Structure:**
```
Attention: Hook that stops the scroll
Interest: Problem/benefit that resonates
Desire: Show what life looks like with solution
Action: Clear next step
```

**Landing page example:**
```markdown
# [ATTENTION] Know when your API breaks before your users do

[INTEREST] You built a great product, but one API failure can ruin everything.
Manual monitoring doesn't scale. By the time you see the error, users are already frustrated.

[DESIRE] Imagine getting a Slack message the second something breaks.
Fix it before anyone notices. Sleep better knowing you'll always know first.

[ACTION] Start monitoring free → [Button]
```

### The PAS Framework (Problem, Agitate, Solve)

**When to use:** When the problem is acute and emotional

**Structure:**
```
Problem: State the pain point clearly
Agitate: Make them feel the pain (without being manipulative)
Solve: Present your solution as the relief
```

**Example:**
```markdown
# [PROBLEM] Spending 5 hours every week writing API documentation?

[AGITATE] You know you should document your code, but it's tedious work that
takes you away from building features. Your team asks the same questions over and over.
New developers take weeks to ramp up. Meanwhile, your docs get more and more outdated.

[SOLVE] DocuGenius generates comprehensive documentation from your code in minutes.
Upload a file, get beautiful markdown docs. Focus on building, not documenting.

[CTA] Try it free → [Button]
```

### The Before-After-Bridge (BAB) Framework

**When to use:** To show transformation clearly

**Structure:**
```
Before: Current frustrating state
After: Ideal future state
Bridge: How your product gets them there
```

**Example:**
```markdown
# [BEFORE] Every Monday morning: "Did anyone update the docs?"

[AFTER] What if documentation updated itself every time you pushed code?

[BRIDGE] With AutoDocs GitHub integration, your documentation stays in sync
automatically. Push to main, docs update instantly. Zero manual work.

[CTA] Connect GitHub → [Button]
```

## Voice & Tone Guidelines

### Brand Voice Spectrum

**Where to position your voice:**

```
Formal ←--------→ Casual
Technical ←--------→ Simple
Serious ←--------→ Playful
Corporate ←--------→ Personal
```

**For indie hackers/solo devs (recommended):**
- 70% casual (conversational but professional)
- 60% simple (technical when needed, but clear)
- 50% balanced (not too playful, not too serious)
- 80% personal (authentic, relatable)

### Tone Adjustments by Context

**Landing page:** Confident, benefit-focused
```
❌ "Our advanced solution potentially helps with data management."
✅ "Turn messy data into insights in minutes."
```

**Error messages:** Helpful, apologetic, action-oriented
```
❌ "Error 500: Internal server error"
✅ "Oops, something went wrong on our end. We've been notified and are fixing it. Try again in a few minutes?"
```

**Success states:** Encouraging, celebratory (but not over-the-top)
```
❌ "Operation completed successfully."
✅ "All set! Your dashboard is live."
```

**Onboarding:** Friendly, guiding, patient
```
❌ "Configure your API keys in settings."
✅ "Let's connect to your database. This takes about 2 minutes."
```

## Copywriting Principles

### 1. Lead with Benefits, Not Features

**Framework: "So what?" test**

Keep asking "so what?" until you get to the benefit:
```
Feature: "Real-time API monitoring"
  → So what? "You get instant alerts"
    → So what? "You fix issues before users notice"
      → So what? "Your app stays reliable and users stay happy"

Final benefit: "Keep your app reliable and your users happy"
```

**Examples:**

| Feature (technical) | Benefit (outcome) |
|---------------------|-------------------|
| "Real-time data sync" | "Your team sees changes instantly" |
| "AES-256 encryption" | "Your data stays private and secure" |
| "99.9% uptime SLA" | "Your service never goes down" |
| "Webhook integration" | "Connect your favorite tools in minutes" |

### 2. Specificity Beats Vagueness

**Vague claims lose trust. Specific numbers build credibility.**

```
❌ "Save time" → How much? When? Doing what?
✅ "Save 5 hours per week on manual data entry"

❌ "Increase conversions" → By how much? For whom?
✅ "Increase sign-ups by 20% with optimized forms"

❌ "Fast performance" → How fast? Compared to what?
✅ "Load your dashboard in under 500ms (3x faster than Excel)"
```

**Data hierarchy (use the best you have):**
1. **Real user data:** "2,000+ developers use this daily"
2. **Estimated impact:** "Save ~5 hours/week"
3. **Comparison:** "3x faster than manual work"
4. **Process detail:** "Get results in 3 clicks"
5. **Avoid:** Vague claims with no numbers

### 3. Active Voice > Passive Voice

**Passive voice is weak and unclear. Active voice is direct and strong.**

```
❌ Passive: "Documents can be generated by our AI"
✅ Active: "Our AI generates documents for you"

❌ Passive: "Your data is protected by encryption"
✅ Active: "We encrypt your data end-to-end"

❌ Passive: "Insights will be provided based on your usage"
✅ Active: "Get insights from your usage data"
```

**How to spot passive voice:**
- Look for "by" + actor ("by our system", "by the user")
- "Can be", "will be", "is done", "was created"

**Active voice structure:**
```
[Actor] [Action] [Object]

You | create | dashboards
We | encrypt | your data
Users | see | real-time updates
```

### 4. Power Words for Conversion

**Emotional triggers that drive action:**

**Urgency:**
- Now, today, instantly, immediately
- Limited time, deadline, expires
- "Don't miss out", "Act now"

**Exclusivity:**
- Exclusive, members-only, invite-only
- Join, become part of, access
- "Be one of the first"

**Trust:**
- Guaranteed, proven, certified
- Safe, secure, protected
- "No credit card required"

**Ease:**
- Simple, easy, effortless
- Quick, fast, instant
- "In 3 clicks", "No setup"

**Value:**
- Free, save, bonus
- Unlimited, included, no hidden fees
- "$0 to start"

### 5. Social Proof Patterns

**Hierarchy of credibility (strongest to weakest):**

1. **Testimonials with full names + companies**
   ```
   "Saves me 10 hours every week."
   — Sarah Chen, Founder @ TechCo
   ```

2. **Usage statistics**
   ```
   "Trusted by 2,000+ developers at Google, Stripe, and Vercel"
   ```

3. **Star ratings + review count**
   ```
   "4.9/5 stars from 150+ reviews on Product Hunt"
   ```

4. **Generic numbers**
   ```
   "Join 10,000+ users building better products"
   ```

5. **Logos only** (weakest, but still valid)
   ```
   [Logo grid: Google, Microsoft, Amazon]
   ```

## Content Types Deep Dive

### Landing Page Structure

**The 7 Essential Sections:**

```markdown
1. Hero (Above the fold)
   - Headline: What it does + who it's for
   - Subheadline: Key benefit
   - CTA button: Clear action
   - Visual: Product screenshot/demo

2. Problem Section
   - State the pain clearly
   - Make it relatable
   - 2-3 sentences max

3. Solution Section
   - How your product solves it
   - 3-5 key benefits (bullet points)
   - Focus on outcomes, not features

4. How It Works (optional)
   - 3 simple steps
   - Shows it's easy
   - Removes friction

5. Social Proof
   - Testimonials OR
   - Usage stats OR
   - Logo grid

6. Pricing (if applicable)
   - Simple tiers
   - Highlight recommended tier
   - FAQ link

7. Final CTA
   - Restate benefit
   - Clear action
   - Low friction ("Start free", not "Buy now")
```

**Headline formulas:**

```
1. Outcome + Timeframe
   "Ship your MVP in 2 weeks, not 2 months"

2. Action + Benefit
   "Build dashboards without code"

3. Before → After
   "From idea to launch in 14 days"

4. Question + Answer
   "Need API monitoring? We've got you covered."

5. Controversial/Bold claim
   "Stop wasting time on boilerplate"
```

### Launch Tweet Structure

**The 5-Tweet Formula:**

```
Tweet 1: Hook
[Problem or interesting stat]
Make them want to read more.

Tweet 2: What it is
[One sentence description]
Clear value proposition.

Tweet 3-4: Benefits
[Bullet points - 3-4 benefits]
Why they should care.

Tweet 5: CTA
[Call to action + link]
What to do next.
```

**Example:**
```
1/ I wasted 20 hours building the same auth flow for the 5th time.

Never again.

2/ I built a Next.js starter with everything built-in:
↳ Auth (email + OAuth)
↳ Payments (Stripe)
↳ Database (Supabase)
↳ UI (Tailwind + shadcn)

3/ What you get:
• Deploy to Vercel in 5 minutes
• Focus on your unique features
• Skip the boring setup
• Ship this weekend

4/ Perfect for:
→ Indie hackers building fast
→ Developers tired of boilerplate
→ Anyone who wants to ship, not setup

5/ Start building: [link]

100% free, open source, MIT license.
```

### Product Hunt Launch Description

**Structure (1000 characters):**

```markdown
## The Problem (100 chars)
[One sentence - relatable pain]

## Our Solution (150 chars)
[What you built + why it's different]

## Who This Is For (100 chars)
[Specific audience]

## Key Features (300 chars)
[5-6 features with 1-line explanations]
- Feature 1: Benefit
- Feature 2: Benefit
[...]

## Why We Built This (150 chars)
[Founder story - personal pain point]

## What's Next (100 chars)
[Roadmap - what you're adding based on feedback]

## Try It Now (100 chars)
[CTA + special offer if any]
```

**Tagline (60 characters):**
```
[What it does] + [who it's for]

Examples:
"API monitoring for developers who want to sleep better"
"Turn code into docs in minutes, not hours"
"Ship MVPs in 2 weeks with Next.js + Supabase"
```

### Email Sequences

**Welcome email (sent immediately after signup):**

```markdown
Subject: Welcome to [Product] 👋

Hey [Name],

Thanks for signing up! Here's what happens next:

1. [First step] - takes 2 minutes
2. [Second step] - optional but recommended
3. [Third step] - you're ready to go

Need help? Reply to this email (I read every response).

[Your name]
Founder, [Product]

P.S. [Helpful tip or resource]
```

**Onboarding sequence (days 1, 3, 7):**

```markdown
Day 1: "How to get started" (guide)
Day 3: "Have you tried [feature]?" (feature highlight)
Day 7: "How's it going?" (check-in + ask for feedback)
```

## SEO Copywriting

### Writing for Humans AND Search Engines

**Primary keyword placement:**
- [ ] Page title (H1)
- [ ] First paragraph (first 100 words)
- [ ] At least one H2 subheading
- [ ] URL slug
- [ ] Meta description

**Natural keyword density:**
- Primary keyword: 3-5 times per 1000 words
- Secondary keywords: 2-3 times
- Related terms: Naturally throughout

**Example (primary keyword: "API monitoring tool"):**

```markdown
# Best API Monitoring Tool for Developers

[First paragraph - include keyword naturally]
When your API goes down, every second counts. Our API monitoring tool
alerts you instantly via Slack, email, or SMS, so you can fix issues
before they impact users.

## Why Choose Our API Monitoring Tool?

[Include keyword in at least one H2]

## How It Works

[Related terms: uptime monitoring, API health checks, status page]
```

### Meta Descriptions (155 characters)

**Formula:**
```
[Benefit] + [How] + [CTA]

Example:
"Monitor your APIs 24/7 with real-time alerts. Get notified in Slack when things break. Start free today."
```

## A/B Testing Copy Variations

### What to Test

**High-impact tests:**
1. Headlines (biggest impact)
2. CTA button text
3. Benefit order
4. Social proof placement
5. Pricing presentation

**Low-impact tests (don't bother):**
- Color tweaks
- Punctuation
- Synonyms that mean the same thing

### Headline Variations to Test

**Test 1: Benefit vs. Outcome**
```
A: "API Monitoring Made Simple"
B: "Sleep Better with 24/7 API Monitoring"
```

**Test 2: Question vs. Statement**
```
A: "Know When Your API Breaks"
B: "Does Your API Monitor Itself?"
```

**Test 3: Specific vs. Generic**
```
A: "Monitor Your APIs"
B: "Get Alerted in 3 Seconds When Your API Fails"
```

### CTA Variations to Test

```
Generic → Specific:
"Get Started" → "Start Monitoring Free"

Action → Outcome:
"Sign Up" → "Get Instant Alerts"

Friction → Frictionless:
"Create Account" → "See Your Dashboard"

Fear → Opportunity:
"Don't Miss Out" → "Join 2,000+ Developers"
```

## Tools & Resources

**Headline analyzers:**
- [CoSchedule Headline Analyzer](https://coschedule.com/headline-analyzer)
- [Sharethrough Headline Analyzer](https://headlines.sharethrough.com)

**Readability checkers:**
- [Hemingway Editor](https://hemingwayapp.com) - Highlights complex sentences
- [Grammarly](https://grammarly.com) - Grammar + tone

**Inspiration:**
- [Really Good Emails](https://reallygoodemails.com) - Email examples
- [Swiped.co](https://swiped.co) - Copywriting swipe file
- [GoodSalesEmails](https://goodsalesemails.com) - Sales email examples

**Competitor research:**
- View source on landing pages
- Save Product Hunt descriptions
- Screenshot effective tweets
- Build a swipe file

## Word Choice Guidelines

### Words to Avoid

**Buzzwords (overused, meaningless):**
- Revolutionary, game-changing, disruptive
- Synergy, leverage, utilize
- Cutting-edge, next-generation
- World-class, best-in-class

**Vague modifiers:**
- Very, really, quite
- Amazing, incredible, awesome
- Powerful, robust, advanced

**Passive/Weak verbs:**
- Is able to, can be used to
- Helps to, allows you to
- Facilitates, enables

### Words to Use More

**Action verbs:**
- Build, create, ship
- Get, start, launch
- Save, gain, earn
- Discover, learn, master

**Concrete nouns:**
- Hours, dollars, customers
- Clicks, minutes, days
- Features, results, outcomes

**Trust builders:**
- Free, guaranteed, proven
- Secure, private, safe
- Simple, easy, quick

---

**Related:** See `EXAMPLES.md` for full copy examples and `TROUBLESHOOTING.md` for common writing issues.
