# MotherDuck Design System Style Guide

**Extracted from:** https://motherduck.com
**Date:** 2025-11-04
**Design Philosophy:** Minimal, warm, technical, retro-modern with monospaced typography

---

## 🎨 Overview

MotherDuck employs a distinctive design language that combines:
- **Warm neutrals** (beige backgrounds)
- **Bold accents** (yellow highlights)
- **Monospaced typography** (technical aesthetic)
- **Sharp edges** (minimal border-radius, 2px max)
- **Offset shadows** (4-8px solid black shadows on hover)
- **High contrast** (dark text on light bg)

This creates a retro-modern, developer-friendly aesthetic that feels both approachable and technically sophisticated.

---

## 🎨 Color Palette

### Primary Colors

| Color Name | Hex/RGB | Usage | Example |
|------------|---------|-------|---------|
| **Background Beige** | `rgb(244, 239, 234)` <br> `#F4EFEA` | Main page background, neutral base | Body, sections |
| **Text Dark** | `rgb(56, 56, 56)` <br> `#383838` | Primary text, headings, borders | H1, H2, borders |
| **Accent Yellow** | `rgb(255, 222, 0)` <br> `#FFDE00` | CTAs, badges, highlights | Buttons, tags |
| **Text Black** | `rgb(0, 0, 0)` <br> `#000000` | Body text, links | Paragraphs, nav links |
| **White** | `rgb(255, 255, 255)` <br> `#FFFFFF` | Card backgrounds, input focus | Cards, modals |
| **Input Background** | `rgba(248, 248, 247, 0.7)` <br> Semi-transparent white | Form inputs default state | Input fields |

### Color Usage Guidelines

- **Backgrounds:** Beige (#F4EFEA) for warmth, White (#FFFFFF) for elevation (cards)
- **Text:** Dark gray (#383838) for headings, Black (#000000) for body text
- **Accents:** Yellow (#FFDE00) sparingly for CTAs and emphasis
- **Borders:** Always Dark gray (#383838), 2px solid

---

## 📝 Typography

### Font Families

#### Primary: Aeonik Mono
- **Type:** Monospaced sans-serif
- **Usage:** Headings (H1-H3), navigation, body text
- **Weights:** 400 (regular)
- **Fallback:** `monospace, sans-serif`

```css
font-family: "Aeonik Mono", monospace, sans-serif;
```

#### Secondary: Aeonik Fono
- **Type:** Proportional sans-serif
- **Usage:** Paragraph text, longer content
- **Weights:** 400 (regular)
- **Fallback:** `"Aeonik Mono", monospace`

```css
font-family: "Aeonik Fono", "Aeonik Mono", monospace;
```

#### Tertiary: Inter
- **Type:** Sans-serif
- **Usage:** Buttons, form inputs
- **Weights:** 300, 400, 600, 700
- **Fallback:** `sans-serif`

```css
font-family: Inter, sans-serif;
```

### Typography Scale

| Element | Font | Size | Line Height | Letter Spacing | Weight | Color |
|---------|------|------|-------------|----------------|--------|-------|
| **H1** | Aeonik Mono | 72px | 86.4px (1.2) | 1.44px | 400 | #383838 |
| **H2** | Aeonik Mono | 32px | 44.8px (1.4) | normal | 400 | #383838 |
| **H3** | Aeonik Mono | 18px | 25.2px (1.4) | normal | 400 | #383838 |
| **Body (P)** | Aeonik Fono | 15px | 18px (1.2) | normal | 400 | #000000 |
| **Base** | Aeonik Mono | 16px | 16px (1.0) | normal | 400 | #383838 |
| **Button** | Inter | 16px | 19.2px (1.2) | 0.32px | 400 | #383838 |
| **Input** | Inter | 16px | 25.6px (1.6) | 0.32px | 400 | #000000 |

### Typography Guidelines

- **Line height:** Tight for headings (1.2), comfortable for body (1.4-1.6)
- **Letter spacing:** Generous for large headings (H1: 1.44px)
- **Font weight:** Consistently 400 (regular) for uniform, technical feel
- **Margins:** Headings have zero margin by default (controlled via layout)

---

## 📐 Spacing System

### Padding Scale

| Size | Value | Usage |
|------|-------|-------|
| **xs** | 4px | H3 vertical padding |
| **sm** | 8px | Button padding, small gaps |
| **md** | 12px | H2 bottom padding |
| **lg** | 16px | H3 horizontal, input horizontal, button padding |
| **xl** | 24px | Input horizontal, card padding |
| **2xl** | 32px | Card padding, section spacing |
| **3xl** | 40px | Header/footer padding |
| **4xl** | 80px | Hero section padding |

### Margin Scale

Same as padding scale, use consistently.

### Gap Scale (Flexbox/Grid)

| Size | Value |
|------|-------|
| **sm** | 16px |
| **md** | 24px |
| **lg** | 32px |

---

## 🧱 Component Styles

### Buttons

#### Base Button
```css
.btn {
  font-family: Inter, sans-serif;
  font-size: 16px;
  font-weight: 400;
  line-height: 19.2px;
  letter-spacing: 0.32px;
  color: rgb(56, 56, 56);
  background-color: transparent;
  border: 1px solid rgba(0, 0, 0, 0);
  border-radius: 2px;
  padding: 8px 16px;
  cursor: pointer;
  transition: all 0.2s ease;
}
```

#### Primary Button
```css
.btn-primary {
  background-color: rgb(255, 222, 0); /* Yellow */
  border: 2px solid rgb(56, 56, 56); /* Dark border */
  color: rgb(56, 56, 56);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 4px 4px 0px rgb(56, 56, 56); /* Offset shadow */
}
```

**Guidelines:**
- Always use yellow background for primary actions
- 2px solid border in dark gray
- Offset shadow on hover (4px x/y, no blur)
- Slight Y-axis lift on hover (-2px)
- Border-radius: 2px (sharp but not harsh)

---

### Form Inputs

#### Text Input
```css
input[type="text"],
input[type="email"] {
  font-family: Inter;
  font-size: 16px;
  line-height: 25.6px;
  letter-spacing: 0.32px;
  color: rgb(0, 0, 0);
  background-color: rgba(248, 248, 247, 0.7);
  border: 2px solid rgb(56, 56, 56);
  border-radius: 2px;
  padding: 16px 24px;
  width: 100%;
  max-width: 382px;
  transition: all 0.2s ease-in-out;
}

input:focus {
  outline: none;
  background-color: rgb(255, 255, 255);
  box-shadow: 4px 4px 0px rgb(56, 56, 56);
}
```

**Guidelines:**
- Semi-transparent white background (default)
- Solid white background (focus)
- Always 2px solid border
- Offset shadow on focus
- 16px vertical, 24px horizontal padding

---

### Cards

```css
.card {
  background-color: rgb(255, 255, 255);
  border: 2px solid rgb(56, 56, 56);
  border-radius: 0px; /* Completely sharp */
  padding: 32px;
  transition: transform 0.2s ease;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 8px 8px 0px rgb(56, 56, 56); /* Larger offset shadow */
}
```

**Guidelines:**
- White background for elevation
- 2px solid border
- Zero border-radius (sharp edges)
- Larger lift on hover (-4px)
- Larger shadow on hover (8px)
- 32px padding

---

### Badges / Tags

```css
.badge {
  display: inline-block;
  background-color: rgb(255, 222, 0);
  border: 2px solid rgb(56, 56, 56);
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 16px;
}
```

**Guidelines:**
- H3 elements often used as badges
- Yellow background
- 2px border
- Small padding (8px vertical, 16px horizontal)
- Uppercase text common (implement via `text-transform: uppercase`)

---

### Navigation

```css
nav {
  display: flex;
  gap: 24px;
  font-family: "Aeonik Mono", monospace, sans-serif;
  font-size: 16px;
}

nav a {
  color: rgb(0, 0, 0);
  text-decoration: none;
  transition: opacity 0.2s;
}

nav a:hover {
  opacity: 0.7;
}
```

**Guidelines:**
- Horizontal flex layout
- 24px gap between items
- Simple opacity fade on hover (0.7)
- No underlines
- Black text

---

## 🌑 Shadows & Elevation

### Shadow System

| Level | Shadow | Usage |
|-------|--------|-------|
| **None** | `none` | Default state (cards, buttons) |
| **Low** | `4px 4px 0px rgb(56, 56, 56)` | Button hover, input focus |
| **Medium** | `8px 8px 0px rgb(56, 56, 56)` | Card hover |

**Guidelines:**
- **Always** use solid, offset shadows (never blur)
- **X and Y offset equal** (4px/4px or 8px/8px)
- **Color:** Always dark gray `rgb(56, 56, 56)`
- **No spread:** Only X/Y offset, no blur radius
- **Pair with transform:** `translateY(-2px)` or `translateY(-4px)` for lift effect

---

## 🔲 Border Radius Patterns

| Element | Border Radius | Rationale |
|---------|---------------|-----------|
| **Cards** | `0px` | Sharp, technical |
| **Buttons** | `2px` | Subtle softness |
| **Inputs** | `2px` | Consistency with buttons |
| **Badges** | `0px` | Sharp edges |

**Guidelines:**
- **Minimize border-radius** for technical aesthetic
- **Maximum:** 2px
- **Most elements:** 0px (sharp)

---

## 🎬 Animations & Transitions

### Transition Timing

| Property | Duration | Easing |
|----------|----------|--------|
| **Hover effects** | 0.2s | `ease` |
| **Input focus** | 0.2s | `ease-in-out` |
| **Transform** | 0.2s | `ease` |
| **Opacity** | 0.2s | Linear |

### Common Patterns

#### Hover Lift
```css
.element:hover {
  transform: translateY(-2px); /* or -4px */
  box-shadow: 4px 4px 0px rgb(56, 56, 56); /* or 8px 8px */
}
```

#### Opacity Fade
```css
.element {
  opacity: 1;
  transition: opacity 0.2s;
}

.element:hover {
  opacity: 0.7;
}
```

**Guidelines:**
- Keep transitions **fast** (0.2s)
- **Lift + Shadow** always paired
- No bounce or elastic easing (stay subtle)

---

## 📏 Grid & Layout System

### Container Widths

| Breakpoint | Max Width | Padding |
|------------|-----------|---------|
| **Desktop** | 1200px | 20px |
| **Tablet** | 100% | 24px |
| **Mobile** | 100% | 16px |

### Header Layout
```css
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 40px;
}
```

### Grid Patterns

**Auto-fit cards:**
```css
display: grid;
grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
gap: 24px;
```

---

## ✨ Key Design Principles

1. **Monospaced Typography:** Technical, developer-friendly aesthetic
2. **Warm Color Palette:** Beige + yellow (approachable, not cold)
3. **Sharp Edges:** Minimal border-radius (0-2px max)
4. **Offset Shadows:** Solid, non-blurred shadows for hover states
5. **High Contrast:** Dark text on light backgrounds
6. **Minimal Animation:** Fast, subtle transitions only
7. **Yellow Accents:** Use sparingly for primary CTAs and emphasis
8. **2px Borders:** Standard border width across all components

---

## 🚀 Usage Examples

### Hero Section
```html
<section class="hero">
  <h3 class="badge">SERVERLESS ANALYTICS</h3>
  <h1>Analytics at the speed of thought</h1>
  <p>Run analytics workloads faster with DuckDB in the cloud.</p>
  <button class="btn btn-primary">Get Started</button>
</section>
```

### Feature Card
```html
<div class="card">
  <span class="badge">LIGHTNING FAST</span>
  <h2>Built on DuckDB</h2>
  <p>Experience the power of DuckDB's columnar engine.</p>
</div>
```

### Form
```html
<form>
  <input type="email" placeholder="Enter your email">
  <button class="btn btn-primary">Start Free Trial</button>
</form>
```

---

## 📦 Export Formats

This style guide can be implemented in:

- ✅ **Plain HTML/CSS** (reference.html)
- ✅ **Tailwind CSS** (custom config needed for fonts/colors)
- ✅ **React/Next.js** (CSS modules or styled-components)
- ✅ **Vue/Nuxt** (scoped styles)
- ✅ **Figma** (design tokens)
- ✅ **Slide Decks** (Reveal.js, Slidev)
- ✅ **Framer Motion** (animations)

---

## 📝 Notes

- **Font Loading:** Aeonik Mono/Fono are custom fonts. If unavailable, fallback to monospace works well.
- **Accessibility:** Ensure 2px borders provide sufficient contrast for focus states.
- **Performance:** Offset shadows are GPU-accelerated (better than blur shadows).
- **Responsive:** Test sharp edges on mobile (may need subtle radius on small screens).

---

**Generated:** 2025-11-04
**Source:** https://motherduck.com
**Tool:** Playwright CSS Extraction + AI Style Guide Generation
