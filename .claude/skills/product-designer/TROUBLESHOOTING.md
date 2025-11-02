# Product Designer - Troubleshooting

## Common Problems & Solutions

---

## Problem 1: Design Looks "Too AI" (Blue/Purple Gradients)

### Symptoms
- Blue → purple gradients everywhere
- Neon colors (bright cyan, magenta)
- Gradient text
- Looks like every other AI-designed site

### Root Cause
- Default AI aesthetic preferences
- Following generic design trends blindly
- Not considering brand differentiation
- Overusing color

### Solution

**Step 1: Identify the trap**
```tsx
{/* ❌ AI Default Trap */}
<div className="bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500">
  <h1 className="bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-blue-600">
    AI-Generated Look
  </h1>
</div>
```

**Step 2: Apply neutral + accent pattern**
```tsx
{/* ✅ Professional Alternative */}
<div className="bg-white">
  <h1 className="text-gray-900 font-bold">
    Clean, Professional Look
  </h1>
  <button className="bg-indigo-600 text-white hover:bg-indigo-700">
    Single Accent Color
  </button>
</div>
```

**Color palette fix:**
```tsx
// BEFORE (AI default)
const colors = {
  primary: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  secondary: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
  accent: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
};

// AFTER (professional)
const colors = {
  primary: '#2563eb',        // Solid indigo
  primaryHover: '#1d4ed8',   // Darker on hover
  text: '#111827',           // Near black
  textMuted: '#6b7280',      // Gray for secondary text
  border: '#e5e7eb',         // Subtle borders
  background: '#ffffff',     // Clean white
};
```

**Quick audit checklist:**
- [ ] Remove all gradients (except subtle backgrounds if needed)
- [ ] Use ONE accent color only
- [ ] Make backgrounds white or subtle gray (not gradients)
- [ ] Use solid colors for text (no gradient text)
- [ ] Reduce color count to 2-3 total

---

## Problem 2: Inconsistent Spacing (Random Gaps)

### Symptoms
- Some gaps are 15px, others 18px, others 22px
- Components don't align properly
- Layout feels chaotic
- "Just eyeballing it" approach

### Root Cause
- Not using spacing system
- Adjusting spacing visually instead of systematically
- Custom pixel values instead of scale

### Solution

**The 8px Grid Rule:**
```tsx
{/* ❌ Random spacing */}
<div className="mb-[15px]">  {/* Custom 15px */}
  <div className="pt-[18px] pb-[22px]">  {/* Random values */}
    <p className="ml-[13px]">Content</p>
  </div>
</div>

{/* ✅ Systematic spacing (8px increments) */}
<div className="mb-4">  {/* 16px */}
  <div className="py-6">  {/* 24px top/bottom */}
    <p className="ml-3">  {/* 12px */}
      Content
    </p>
  </div>
</div>
```

**Spacing decision tree:**
```
How related are these elements?
├─ Very related (icon + text) → space-x-2 (8px)
├─ Related (form label + input) → space-y-2 (8px)
├─ Grouped (form fields) → space-y-4 (16px)
├─ Sections within card → space-y-6 (24px)
└─ Different sections → space-y-8 or space-y-12 (32px or 48px)
```

**Common spacing patterns:**
```tsx
// Card internal spacing
<div className="p-6 space-y-4">
  {/* 24px padding, 16px between children */}
</div>

// Form spacing
<form className="space-y-6">
  {/* 24px between form fields */}
  <div className="space-y-2">
    {/* 8px between label and input */}
    <label>Email</label>
    <input />
  </div>
</form>

// Page sections
<main className="space-y-12">
  {/* 48px between major sections */}
</main>
```

**Fix existing designs:**
1. Inspect all spacing values
2. Round to nearest 4px (0.5, 1, 2, 3, 4, 6, 8, 12, 16)
3. Replace custom arbitrary values with Tailwind scale
4. Test on mobile (spacing often needs adjustment)

---

## Problem 3: Text Hierarchy Unclear

### Symptoms
- All text looks the same size
- Can't tell what's important
- Headers don't stand out
- User doesn't know where to look

### Root Cause
- Too many font sizes
- Not enough contrast between sizes
- Inconsistent font weights
- Missing visual hierarchy

### Solution

**Define clear type scale (stick to it):**
```tsx
// Typography system (use these only)
const typeScale = {
  // Display (hero sections)
  display: 'text-5xl font-bold',        // 48px

  // Headings
  h1: 'text-3xl font-bold',             // 30px - page title
  h2: 'text-xl font-semibold',          // 20px - section title
  h3: 'text-lg font-semibold',          // 18px - subsection

  // Body
  body: 'text-base font-normal',        // 16px - main text
  bodyLarge: 'text-lg font-normal',     // 18px - emphasized
  small: 'text-sm font-normal',         // 14px - secondary
  tiny: 'text-xs font-medium',          // 12px - captions
};
```

**Example hierarchy fix:**
```tsx
{/* ❌ BEFORE: No hierarchy */}
<div>
  <h1 className="text-xl">Dashboard</h1>
  <p className="text-lg">Welcome back!</p>
  <h2 className="text-lg">Recent Activity</h2>
  <span className="text-base">Updated 2 min ago</span>
</div>

{/* ✅ AFTER: Clear hierarchy */}
<div>
  <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
  <p className="text-base text-gray-600 mt-1">Welcome back!</p>

  <h2 className="text-xl font-semibold text-gray-900 mt-8 mb-4">Recent Activity</h2>
  <span className="text-sm text-gray-500">Updated 2 min ago</span>
</div>
```

**Visual hierarchy checklist:**
- [ ] Page title is biggest (text-3xl or text-4xl)
- [ ] Section titles are clearly smaller but still bold (text-xl)
- [ ] Body text is comfortable reading size (text-base, 16px)
- [ ] Secondary info is noticeably smaller and muted color (text-sm, gray)
- [ ] Only use 3-4 font sizes total

**Size jump rule:**
Each level should be 1.25x larger than the previous:
- 12px → 16px → 20px → 24px → 30px → 48px

---

## Problem 4: Mobile Layout Broken

### Symptoms
- Text too small on mobile
- Buttons too small to tap
- Horizontal scrolling
- Elements overlap
- Padding too tight

### Root Cause
- Desktop-first design
- Not testing on mobile
- Forgetting touch target sizes
- Fixed widths instead of responsive

### Solution

**Mobile-first approach:**
```tsx
{/* ❌ Desktop-first (breaks on mobile) */}
<div className="lg:w-1/2 lg:px-8">
  {/* No mobile styles defined */}
</div>

{/* ✅ Mobile-first (works everywhere) */}
<div className="w-full px-4 md:w-1/2 lg:px-8">
  {/* Base: mobile, then layer up */}
</div>
```

**Touch target fixes:**
```tsx
{/* ❌ Too small for mobile */}
<button className="px-3 py-1 text-sm">
  {/* 32px height - too small to tap */}
</button>

{/* ✅ Mobile-friendly */}
<button className="
  px-6 py-3 text-base       {/* 48px height - comfortable */}
  md:px-4 md:py-2 md:text-sm {/* Smaller on desktop OK */}
">
  Tap Me
</button>
```

**Common mobile issues:**

| Issue | Fix |
|-------|-----|
| Horizontal scroll | Remove fixed widths, use `w-full` or `max-w-*` |
| Text too small | Use `text-base` (16px) minimum for body |
| Buttons too small | Minimum 44x44px (Apple) or 48x48px (Material) |
| Padding too tight | Use `px-4` (16px) minimum on mobile |
| Stack broken | Check grid: `grid-cols-1 md:grid-cols-2` |

**Responsive testing workflow:**
1. Chrome DevTools → Device Toolbar (Cmd+Shift+M)
2. Test iPhone SE (375px - smallest modern phone)
3. Test iPad (768px - tablet breakpoint)
4. Test desktop (1280px+)
5. Check between breakpoints (resize manually)

---

## Problem 5: Low Color Contrast (Unreadable Text)

### Symptoms
- Gray text on light gray background
- Pale colors hard to read
- Users complain text is hard to see
- Fails accessibility checks

### Root Cause
- Overusing light/muted colors
- Not checking contrast ratios
- Assuming what looks good on your screen works everywhere
- Ignoring accessibility

### Solution

**Contrast standards:**
- **Normal text (16px):** 4.5:1 minimum (WCAG AA)
- **Large text (18px+):** 3:1 minimum
- **Target:** 7:1 (WCAG AAA - better)

**Common failures:**
```tsx
{/* ❌ Low contrast (2.5:1 - fails) */}
<p className="text-gray-400 bg-white">
  Hard to read (gray-400 on white = 2.5:1)
</p>

{/* ✅ Sufficient contrast (11:1 - passes AAA) */}
<p className="text-gray-700 bg-white">
  Easy to read (gray-700 on white = 11:1)
</p>

{/* ❌ Barely visible (1.5:1 - fails badly) */}
<p className="text-gray-300 bg-gray-100">
  Almost invisible
</p>

{/* ✅ Good contrast (8:1) */}
<p className="text-gray-800 bg-gray-50">
  Clear and readable
</p>
```

**Safe color combinations:**

| Text | Background | Contrast | Pass? |
|------|------------|----------|-------|
| gray-900 | white | 18:1 | AAA ✅ |
| gray-700 | white | 11:1 | AAA ✅ |
| gray-600 | white | 7:1 | AAA ✅ |
| gray-500 | white | 4.6:1 | AA ✅ |
| gray-400 | white | 2.5:1 | ❌ Fail |
| white | indigo-600 | 8:1 | AAA ✅ |
| white | indigo-500 | 4.8:1 | AA ✅ |

**Quick fix:**
1. Open Chrome DevTools
2. Inspect text element
3. Check "Accessibility" tab
4. Look for contrast ratio
5. If < 4.5:1, make text darker (or background lighter)

**Testing tool:**
```
https://webaim.org/resources/contrastchecker/
```

---

## Problem 6: Overwhelming Animations

### Symptoms
- Everything moves when you hover
- Page feels chaotic
- Slow, laggy animations
- Distracting motion everywhere

### Root Cause
- Adding animations to every element
- Long animation durations (> 300ms)
- Complex animations (multiple properties)
- Not understanding animation purpose

### Solution

**Animation purpose rule:**
```
Should this animate?
├─ Does it provide feedback? (hover, click) → YES, subtle
├─ Does it show state change? (loading → success) → YES, quick
├─ Is it decorative only? → NO, remove
└─ Does it help user understand? (modal entrance) → YES, smooth
```

**Animation fixes:**
```tsx
{/* ❌ Too much, too slow */}
<button className="
  transition-all duration-500
  hover:scale-110 hover:rotate-3 hover:shadow-2xl
">
  Overwhelming
</button>

{/* ✅ Subtle, quick */}
<button className="
  transition-colors duration-150
  hover:bg-indigo-700
">
  Just Right
</button>
```

**Animation best practices:**

| Property | Duration | Use Case |
|----------|----------|----------|
| color, background | 150ms | Hover states, buttons |
| transform (scale) | 200ms | Gentle emphasis |
| opacity | 200ms | Fade in/out |
| all | 300ms max | Multiple properties (use sparingly) |

**When NOT to animate:**
- Text content (distracting to read)
- Page layout shifts
- Every element on page
- Critical information (delays comprehension)

**Quick fix:**
1. Remove `transition-all` (too broad)
2. Reduce durations to 150-200ms
3. Limit to one property (color or transform, not both)
4. Remove animations from text

---

## Problem 7: Inconsistent Button Styles

### Symptoms
- 5 different button styles across app
- Unclear which is primary action
- Different sizes, colors, shapes
- Users don't know what to click

### Root Cause
- No button system defined
- Creating buttons on the fly
- Not distinguishing primary/secondary/tertiary
- Inconsistent implementation

### Solution

**Define button hierarchy:**
```tsx
// Button System (use consistently)

// 1. Primary (main action per screen)
const PrimaryButton = ({ children }) => (
  <button className="
    px-6 py-2.5
    bg-indigo-600 text-white font-semibold rounded-lg
    hover:bg-indigo-700
    focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2
    transition-colors duration-150
  ">
    {children}
  </button>
);

// 2. Secondary (alternative actions)
const SecondaryButton = ({ children }) => (
  <button className="
    px-6 py-2.5
    bg-white text-gray-700 font-semibold rounded-lg border-2 border-gray-300
    hover:border-gray-400 hover:bg-gray-50
    focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2
    transition-colors duration-150
  ">
    {children}
  </button>
);

// 3. Tertiary/Ghost (low-priority actions)
const TertiaryButton = ({ children }) => (
  <button className="
    px-4 py-2
    text-gray-600 font-medium
    hover:text-gray-900 hover:bg-gray-100 rounded-lg
    transition-colors duration-150
  ">
    {children}
  </button>
);

// 4. Danger (destructive actions)
const DangerButton = ({ children }) => (
  <button className="
    px-6 py-2.5
    bg-red-600 text-white font-semibold rounded-lg
    hover:bg-red-700
    focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2
    transition-colors duration-150
  ">
    {children}
  </button>
);
```

**Usage rules:**
- **One primary per screen** (the most important action)
- **Multiple secondary** (alternative actions)
- **Many tertiary** (cancel, back, etc.)
- **Danger for destructive actions only** (delete, remove)

**Quick audit:**
1. Find all buttons in app
2. Categorize: primary, secondary, tertiary, danger
3. Apply consistent styling to each category
4. Ensure only ONE primary per screen/modal

---

## Quick Reference: Common Fixes

| Problem | Quick Fix |
|---------|-----------|
| "Looks too AI" | Remove gradients, use solid accent color only |
| Random spacing | Use 8px grid (space-4, space-6, space-8) |
| No hierarchy | Define 3-4 font sizes, use consistently |
| Mobile broken | Start mobile-first, test at 375px |
| Low contrast | Use gray-700+ for text on white |
| Too many animations | Remove `transition-all`, use 150ms max |
| Inconsistent buttons | Define 3 button types, stick to them |

---

**Related:** See `REFERENCE.md` for design system details and `EXAMPLES.md` for component code.
