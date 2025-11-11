# Recommended Workflows - Army of Agents

Proven multi-agent workflows for common creative tasks.

## Flow 1: Hook/Headline (Simple)

**Time:** 2-3 min | **Cost:** ~$0.03

```
Researcher → Copywriter → Critic Hormozi → Director
```

**Use for:**
- Social media hooks
- Email subject lines
- Ad headlines
- Blog post titles

**Execution:**
1. Researcher analyzes audience (30s)
2. Copywriter creates 3 options (45s)
3. Critic evaluates with Hormozi framework (60s)
4. Director approves best + final tweaks (30s)

---

## Flow 2: Landing Page (Complex)

**Time:** 5-8 min | **Cost:** ~$0.10

```
Strategist (parallel) Content Designer
       ↓
Researcher
       ↓
Copywriter
       ↓
Critic Hormozi
       ↓
Director
       ↓
Revisor
```

**Use for:**
- Product landing pages
- Service pages
- Sales pages
- Lead generation pages

**Execution:**
1. Strategist + Content Designer work in parallel (60s)
2. Researcher analyzes market (45s)
3. Copywriter writes full page (90s)
4. Critic evaluates sections (60s)
5. Director applies feedback (45s)
6. Revisor polishes (45s)

---

## Flow 3: Email Sequence

**Time:** 4-6 min | **Cost:** ~$0.08

```
Researcher (parallel) Strategist
       ↓
Copywriter (3 emails)
       ↓
Critic Hormozi (evaluates each)
       ↓
Director (final adjustments)
```

**Use for:**
- Product launches
- Welcome sequences
- Nurture campaigns
- Re-engagement series

**Execution:**
1. Researcher + Strategist work in parallel (90s)
2. Copywriter writes 3 emails (120s)
3. Critic evaluates each email (90s)
4. Director applies feedback (60s)

---

## Flow 4: Video Script

**Time:** 4-8 min | **Cost:** ~$0.08-0.15

```
Researcher
       ↓
Content Designer
       ↓
Copywriter
       ↓
Revisor
```

**Use for:**
- YouTube videos
- Explainer videos
- Product demos
- Educational content

**Execution:**
1. Researcher analyzes audience (45s)
2. Content Designer creates structure (60s)
3. Copywriter writes full script with timing (120s)
4. Revisor simplifies language + adds pauses (45s)

---

## Flow 5: Social Media Campaign

**Time:** 6-10 min | **Cost:** ~$0.12-0.18

```
Strategist (campaign planning)
       ↓
Researcher (parallel) Content Designer
       ↓
Copywriter (multiple posts)
       ↓
Critic Hormozi
       ↓
Director
```

**Use for:**
- Multi-post campaigns
- Product launches on social
- Thought leadership series
- Engagement campaigns

**Execution:**
1. Strategist plans campaign arc (90s)
2. Researcher + Content Designer work in parallel (90s)
3. Copywriter creates 5-7 posts (150s)
4. Critic evaluates series flow (90s)
5. Director finalizes + orders posts (60s)

---

## Execution Principles

### When to Run Parallel

Execute agents in parallel when:
- Tasks are independent
- No output dependency
- Time efficiency matters

**Example:**
```python
# Parallel execution
researcher = Task(...)
strategist = Task(...)
# Both run simultaneously
```

### When to Run Sequential

Execute agents sequentially when:
- Output of one feeds another
- Dependencies exist
- Quality over speed

**Example:**
```python
# Sequential execution
researcher_output = Task(...)
# Wait for completion
copywriter_output = Task(context=researcher_output)
```

### Iteration Limits

**Maximum rounds:** 3
- Round 1: Initial execution
- Round 2: Feedback + refinement
- Round 3: Final approval (if needed)

**Why limit?**
- Prevents infinite loops
- Diminishing returns after 3 rounds
- Cost control

---

## Role Selection Guide

| Task Type | Required Roles | Optional Roles |
|-----------|---------------|----------------|
| Hook/Headline | Researcher, Copywriter, Critic | Director |
| Landing Page | All roles | - |
| Email Sequence | Researcher, Strategist, Copywriter, Critic | Director |
| Video Script | Researcher, Content Designer, Copywriter | Revisor |
| Social Campaign | Strategist, Researcher, Copywriter, Critic | Director |

---

## Optimization Tips

### Reduce Cost
- Skip Director for simple tasks
- Use parallel execution when possible
- Limit to 2 rounds for non-critical copy

### Increase Quality
- Always include Critic Hormozi for sales copy
- Add Revisor for customer-facing content
- Use 3 rounds for high-stakes projects

### Save Time
- Parallel execution for independent tasks
- Pre-load context from previous similar tasks
- Reuse Researcher insights across similar campaigns
