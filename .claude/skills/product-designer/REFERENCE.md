# Product Designer - Reference Documentation

## Design System Deep Dive

### Color Theory for Web Applications

#### The Psychology of Color in UI

**Neutral Colors (Primary Use):**
- **Gray-50 to Gray-900:** Backgrounds, text, borders
- **Why:** Reduces cognitive load, keeps focus on content
- **Usage:** 80-90% of your UI should be neutral tones

**Accent Colors (Secondary Use):**
- **Purpose:** Draw attention to primary actions
- **Usage:** Buttons, links, important notifications
- **Rule:** One primary accent maximum for MVP

**Color Accessibility:**
- **WCAG AA:** 4.5:1 contrast for normal text (16px)
- **WCAG AAA:** 7:1 contrast (better, aim for this)
- **Large text:** 3:1 minimum (18px+ or 14px bold)

**Testing contrast:**
```bash
# Chrome DevTools > Inspect > Accessibility tab
# Or use: https://webaim.org/resources/contrastchecker/
```

#### Professional Color Palettes

**1. SaaS Blue (Trustworthy, Professional)**
```css
--primary: #2563eb; /* Blue-600 */
--primary-hover: #1d4ed8; /* Blue-700 */
--primary-light: #dbeafe; /* Blue-50 */
--text: #1f2937; /* Gray-800 */
--text-muted: #6b7280; /* Gray-500 */
--border: #e5e7eb; /* Gray-200 */
--background: #ffffff;
--background-alt: #f9fafb; /* Gray-50 */
```

**2. Fintech Green (Growth, Success)**
```css
--primary: #059669; /* Emerald-600 */
--primary-hover: #047857; /* Emerald-700 */
--primary-light: #d1fae5; /* Emerald-50 */
--text: #111827; /* Gray-900 */
--text-muted: #6b7280; /* Gray-500 */
--border: #d1d5db; /* Gray-300 */
```

**3. Creative Orange (Energy, Approachable)**
```css
--primary: #ea580c; /* Orange-600 */
--primary-hover: #c2410c; /* Orange-700 */
--primary-light: #ffedd5; /* Orange-50 */
--text: #1c1917; /* Stone-900 */
--text-muted: #78716c; /* Stone-500 */
--border: #e7e5e4; /* Stone-200 */
```

**4. Minimalist Black (Bold, Modern)**
```css
--primary: #000000;
--primary-hover: #171717; /* Neutral-900 */
--primary-light: #f5f5f5; /* Neutral-100 */
--text: #0a0a0a; /* Neutral-950 */
--text-muted: #737373; /* Neutral-500 */
--border: #e5e5e5; /* Neutral-200 */
```

### Typography System

#### Font Selection Strategy

**System Fonts (Zero Load Time):**
```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```
- **Pros:** Instant load, native look, free
- **Cons:** Less distinctive
- **Use when:** Performance critical, native app feel

**Web Fonts (Distinctive Brand):**
```css
/* Modern, clean (recommended) */
font-family: 'Inter', sans-serif;

/* Technical, developer-focused */
font-family: 'Geist Sans', sans-serif;

/* Editorial, content-heavy */
font-family: 'Signifier', serif;

/* Monospace for code */
font-family: 'Geist Mono', monospace;
```

**Loading Strategy:**
```html
<!-- Preload for critical fonts -->
<link rel="preload" href="/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>

<!-- Font display swap prevents invisible text -->
<style>
  @font-face {
    font-family: 'Inter';
    src: url('/fonts/inter.woff2') format('woff2');
    font-display: swap; /* Shows fallback immediately */
  }
</style>
```

#### Type Scale (Golden Ratio: 1.25)

```css
/* Base: 16px */
--text-xs: 0.75rem;    /* 12px - Captions, labels */
--text-sm: 0.875rem;   /* 14px - Secondary text */
--text-base: 1rem;     /* 16px - Body text */
--text-lg: 1.125rem;   /* 18px - Emphasized body */
--text-xl: 1.25rem;    /* 20px - Section titles */
--text-2xl: 1.5rem;    /* 24px - Card titles */
--text-3xl: 1.875rem;  /* 30px - Page headers */
--text-4xl: 2.25rem;   /* 36px - Hero sections */
--text-5xl: 3rem;      /* 48px - Landing page hero */

/* Line heights */
--leading-tight: 1.25;    /* Headings */
--leading-normal: 1.5;    /* Body text */
--leading-relaxed: 1.75;  /* Long-form content */
```

#### Font Weight Strategy

```css
/* Avoid font-weight: 500 and 600 (often look awkward) */
--font-normal: 400;    /* Body text */
--font-medium: 500;    /* Slight emphasis (use sparingly) */
--font-semibold: 600;  /* Buttons, labels (use sparingly) */
--font-bold: 700;      /* Headings */

/* Best practice: Use only 400 and 700 */
```

**Hierarchy through weight:**
```tsx
<h1 className="text-3xl font-bold">Page Title</h1>
<p className="text-base font-normal text-gray-600">Body text</p>
<span className="text-sm font-normal text-gray-500">Caption</span>
```

### Spacing System (8px Grid)

#### The 8-Point Grid System

**Why 8px?**
- Divisible by 2, 4, 8 (flexible)
- Most common screen sizes are multiples of 8
- Creates visual rhythm and consistency

**Tailwind Spacing Scale:**
```css
0.5 → 2px   (hairline, tight borders)
1   → 4px   (minimal gap between related items)
2   → 8px   (tight spacing, icons next to text)
3   → 12px  (comfortable spacing within components)
4   → 16px  (default gap between elements)
5   → 20px
6   → 24px  (spacing between sections within a card)
8   → 32px  (spacing between distinct sections)
10  → 40px
12  → 48px  (major section separation)
16  → 64px  (page-level spacing)
20  → 80px
24  → 96px  (hero section padding)
```

#### Component Internal Spacing

**Buttons:**
```tsx
// Small button
<button className="px-3 py-1.5 text-sm">
  {/* Horizontal: 12px, Vertical: 6px */}
</button>

// Default button
<button className="px-4 py-2 text-base">
  {/* Horizontal: 16px, Vertical: 8px */}
</button>

// Large button
<button className="px-6 py-3 text-lg">
  {/* Horizontal: 24px, Vertical: 12px */}
</button>
```

**Cards:**
```tsx
// Compact card (dashboard widgets)
<div className="p-4 space-y-3">
  {/* Padding: 16px, Gap: 12px */}
</div>

// Standard card
<div className="p-6 space-y-4">
  {/* Padding: 24px, Gap: 16px */}
</div>

// Spacious card (landing pages)
<div className="p-8 space-y-6">
  {/* Padding: 32px, Gap: 24px */}
</div>
```

**Forms:**
```tsx
<form className="space-y-6">
  {/* 24px between form fields */}
  <div className="space-y-2">
    {/* 8px between label and input */}
    <label>Email</label>
    <input className="px-4 py-2" />
  </div>
</form>
```

### Layout Patterns

#### Container Widths (Content Optimization)

**Reading content:**
```tsx
<div className="max-w-2xl mx-auto">
  {/* 672px max - optimal for paragraphs (60-75 characters per line) */}
</div>
```

**Forms:**
```tsx
<div className="max-w-md mx-auto">
  {/* 448px max - comfortable form width */}
</div>
```

**Dashboards:**
```tsx
<div className="max-w-7xl mx-auto">
  {/* 1280px max - full dashboard layouts */}
</div>
```

**Landing pages:**
```tsx
<div className="max-w-6xl mx-auto">
  {/* 1152px max - balanced landing page width */}
</div>
```

#### Responsive Grid Patterns

**Card grids:**
```tsx
{/* Auto-fit: Creates as many columns as fit */}
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {cards.map(card => <Card key={card.id} />)}
</div>

{/* Fixed columns with responsive breakpoints */}
<div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
  {items.map(item => <Item key={item.id} />)}
</div>
```

**Dashboard layouts:**
```tsx
{/* Sidebar + Main content */}
<div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
  <aside className="lg:col-span-1">
    {/* Sidebar: 1/4 width on desktop */}
  </aside>
  <main className="lg:col-span-3">
    {/* Main: 3/4 width on desktop */}
  </main>
</div>

{/* Stats + Chart layout */}
<div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
  <div className="lg:col-span-2">
    {/* Chart: 2/3 width */}
  </div>
  <div>
    {/* Stats: 1/3 width */}
  </div>
</div>
```

### Component State Design

#### Interactive States (Buttons)

```tsx
{/* All 5 states designed */}
<button className="
  px-4 py-2 rounded-lg
  bg-indigo-600 text-white font-medium

  hover:bg-indigo-700
  active:bg-indigo-800
  focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2
  disabled:bg-gray-300 disabled:text-gray-500 disabled:cursor-not-allowed

  transition-colors duration-150
">
  Click me
</button>
```

**State checklist:**
- [ ] Default (resting state)
- [ ] Hover (mouse over)
- [ ] Active (clicked/pressed)
- [ ] Focus (keyboard navigation)
- [ ] Disabled (not interactive)

#### Input States

```tsx
<input className="
  w-full px-4 py-2 rounded-lg
  border border-gray-300

  hover:border-gray-400
  focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-20
  disabled:bg-gray-100 disabled:cursor-not-allowed

  placeholder:text-gray-400
  transition-colors duration-150
" />

{/* Error state */}
<input className="
  border-red-500 focus:border-red-500 focus:ring-red-500
" />

{/* Success state */}
<input className="
  border-green-500 focus:border-green-500 focus:ring-green-500
" />
```

### Animation & Transitions

#### When to Animate

**✅ DO animate:**
- State changes (loading → success)
- Hover states (button color change)
- Modal/dropdown entry/exit
- Page transitions (fade in/out)
- Skeleton loaders

**❌ DON'T animate:**
- Text content (hard to read)
- Critical information (delays comprehension)
- Everything (creates chaos)
- Slow animations (> 300ms feels sluggish)

#### Animation Timing

```css
/* Fast: UI feedback (hover, click) */
transition-duration: 150ms;

/* Base: Modal, dropdown */
transition-duration: 200ms;

/* Slow: Page transitions */
transition-duration: 300ms;

/* Easing functions */
ease-out: /* Element entering (snappy start) */
ease-in: /* Element exiting (snappy end) */
ease-in-out: /* Both (smooth) */
```

**Tailwind classes:**
```tsx
<div className="transition-colors duration-150 ease-out">
  {/* Fast color change on hover */}
</div>

<div className="transition-transform duration-200 ease-in-out">
  {/* Smooth scale/translate */}
</div>

<div className="transition-all duration-300">
  {/* Animate everything (use sparingly) */}
</div>
```

### Accessibility (A11Y)

#### Keyboard Navigation

**Tab order:**
```tsx
{/* Logical tab order (top to bottom, left to right) */}
<nav>
  <a href="/">Home</a>      {/* Tab 1 */}
  <a href="/about">About</a> {/* Tab 2 */}
</nav>
<main>
  <button>CTA</button>       {/* Tab 3 */}
  <input />                  {/* Tab 4 */}
</main>
```

**Focus states (critical):**
```tsx
<button className="focus:ring-2 focus:ring-indigo-500 focus:outline-none">
  {/* Visible focus indicator for keyboard users */}
</button>
```

#### Screen Reader Support

**Semantic HTML:**
```tsx
{/* Good: Semantic */}
<nav>
  <ul>
    <li><a href="/">Home</a></li>
  </ul>
</nav>

{/* Bad: Divs for everything */}
<div className="nav">
  <div className="link">Home</div>
</div>
```

**ARIA labels:**
```tsx
{/* Icon-only button */}
<button aria-label="Close modal">
  <XIcon />
</button>

{/* Loading state */}
<div role="status" aria-live="polite">
  Loading...
</div>

{/* Skip to main content */}
<a href="#main" className="sr-only focus:not-sr-only">
  Skip to main content
</a>
```

#### Color Contrast

**Testing:**
```tsx
// Chrome DevTools > Inspect element > Accessibility tab
// Shows contrast ratio

// Minimum standards:
// Normal text: 4.5:1 (WCAG AA)
// Large text (18px+): 3:1 (WCAG AA)
```

**Common failures:**
```tsx
{/* ❌ Gray text on gray background */}
<p className="text-gray-400 bg-gray-100">Low contrast</p>

{/* ✅ Sufficient contrast */}
<p className="text-gray-700 bg-white">Good contrast (11:1)</p>
```

### Design Tokens (Reusable Values)

#### Shadow System

```css
/* Tailwind shadow classes */
shadow-sm   → 0 1px 2px rgba(0,0,0,0.05)   /* Subtle borders */
shadow      → 0 1px 3px rgba(0,0,0,0.1)    /* Cards */
shadow-md   → 0 4px 6px rgba(0,0,0,0.1)    /* Dropdown */
shadow-lg   → 0 10px 15px rgba(0,0,0,0.1)  /* Modal */
shadow-xl   → 0 20px 25px rgba(0,0,0,0.1)  /* Floating panels */
shadow-2xl  → 0 25px 50px rgba(0,0,0,0.25) /* Hero images */
```

**Usage:**
```tsx
{/* Resting card */}
<div className="bg-white shadow-sm hover:shadow-md transition-shadow">

{/* Elevated panel */}
<div className="bg-white shadow-lg">

{/* Modal */}
<div className="bg-white shadow-xl">
```

#### Border Radius System

```css
rounded-none  → 0px     /* No radius */
rounded-sm    → 2px     /* Subtle */
rounded       → 4px     /* Default */
rounded-md    → 6px     /* Comfortable */
rounded-lg    → 8px     /* Cards, buttons */
rounded-xl    → 12px    /* Larger cards */
rounded-2xl   → 16px    /* Hero sections */
rounded-3xl   → 24px    /* Rarely used */
rounded-full  → 9999px  /* Pills, avatars */
```

**Consistency:**
```tsx
{/* Stick to one or two radius values */}
<button className="rounded-lg">Primary</button>
<input className="rounded-lg" />
<div className="rounded-lg">Card</div>
```

### Mobile-First Responsive Design

#### Breakpoint Strategy

```css
/* Tailwind breakpoints */
sm: 640px   /* Tablet portrait */
md: 768px   /* Tablet landscape */
lg: 1024px  /* Desktop */
xl: 1280px  /* Large desktop */
2xl: 1536px /* XL desktop */

/* Mobile-first approach */
.element {
  /* Base: mobile (< 640px) */
  width: 100%;

  /* Tablet and up */
  @media (min-width: 768px) {
    width: 50%;
  }

  /* Desktop and up */
  @media (min-width: 1024px) {
    width: 33.333%;
  }
}
```

**Tailwind mobile-first:**
```tsx
<div className="
  w-full       {/* Mobile: full width */}
  md:w-1/2     {/* Tablet: half width */}
  lg:w-1/3     {/* Desktop: third width */}
">
```

#### Touch Target Sizes

**Minimum sizes (mobile):**
- Buttons: 44x44px (Apple) or 48x48px (Material)
- Links: 44x44px touch area (can be smaller visually with padding)

```tsx
{/* Mobile-friendly button */}
<button className="
  px-6 py-3          {/* 48px height minimum */}
  text-base
  md:px-4 md:py-2    {/* Smaller on desktop OK */}
">
  Tap me
</button>
```

## Tools & Resources

**Color Palette Generators:**
- [Coolors.co](https://coolors.co) - Generate palettes
- [Tailwind Color Palette](https://tailwindcss.com/docs/customizing-colors) - Pre-built scales
- [Realtime Colors](https://realtimecolors.com) - Preview palettes on real UI

**Typography:**
- [Typescale](https://typescale.com) - Generate type scales
- [Google Fonts](https://fonts.google.com) - Free web fonts
- [Fontsource](https://fontsource.org) - Self-host Google Fonts

**Layout:**
- [Tailwind UI](https://tailwindui.com) - Premium components ($149+)
- [shadcn/ui](https://ui.shadcn.com) - Free copy-paste components
- [Flowbite](https://flowbite.com) - Free Tailwind components

**Accessibility:**
- [WAVE](https://wave.webaim.org) - Accessibility checker
- [Axe DevTools](https://www.deque.com/axe/devtools/) - Chrome extension
- [Lighthouse](https://developers.google.com/web/tools/lighthouse) - Built into Chrome

---

**Related:** See `EXAMPLES.md` for component code and `TROUBLESHOOTING.md` for common design issues.
