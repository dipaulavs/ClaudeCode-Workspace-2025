# Design Cloning - Specialized Prompts

Prompts tested and proven from original methodology (https://www.youtube.com/watch?v=vcJVnyhmLS4)

---

## Phase 1: Extract Styles (Automated)

This is handled by `extract_styles.py` - no prompts needed.

---

## Phase 2: Co-Create Reference Page

### Prompt 2.1: Initial Reference Page Creation

```
Help me rebuild the exact same UI design in single HTML as reference.html.

I've extracted the CSS from [SITE_URL] and saved it in:
- design-clones/[site]/extracted/styles.css
- design-clones/[site]/extracted/computed_styles.json
- design-clones/[site]/extracted/screenshot.png (visual reference)

Please:
1. Use the extracted CSS as the foundation
2. Create a simple, clean page that captures the FULL ESSENCE of the style
3. Focus on getting the core visual elements right:
   - Background colors
   - Typography (fonts, sizes, weights)
   - Primary button style
   - Card/container style
   - Spacing and layout
4. Keep the HTML simple - we're establishing a reference, not building the full site

The goal is to create a reference implementation that we can iterate on until it's 100% pixel-perfect with the original design.
```

### Prompt 2.2: Color Correction

```
The [element] color looks slightly different from the original.

Looking at the screenshot, the [background/text/border] should be [COLOR_VALUE].

Please update reference.html to use the exact color.
```

### Prompt 2.3: Typography Correction

```
The typography doesn't match exactly.

From computed_styles.json, I see:
- Font family should be: [FONT_FAMILY]
- Font size should be: [SIZE]
- Font weight should be: [WEIGHT]
- Line height should be: [LINE_HEIGHT]

Please update reference.html to match these exact values.
```

### Prompt 2.4: Spacing Correction

```
The spacing feels off. Looking at the original:
- [Element] padding should be [VALUE]
- [Element] margin should be [VALUE]
- Gap between elements should be [VALUE]

Please adjust the spacing in reference.html to match precisely.
```

### Prompt 2.5: Final Validation

```
Great! The reference page now looks very close. Let me do a final check:

[User validates each aspect:]
✓ Background color matches
✓ Typography is correct
✓ Button style is perfect
✓ Spacing is accurate
✓ Overall feeling matches original

This reference page is now 100% accurate. Let's proceed to extract the style guide.
```

---

## Phase 3: Extract Detailed Style Guide

### Prompt 3.1: Complete Style Guide Extraction

**IMPORTANT:** Only use this prompt AFTER reference page is pixel-perfect.

```
Excellent! Now that we have a pixel-perfect reference page, let's extract a comprehensive style guide that captures every detail of this design system.

Please generate a detailed style guide in Markdown format. You MUST include ALL of the following sections with SPECIFIC, EXACT values (not approximations):

## 1. Overview
- Design philosophy (modern, minimal, bold, etc)
- Key visual characteristics
- Brand personality (professional, playful, elegant, etc)
- Use cases (best for SaaS, e-commerce, portfolio, etc)

## 2. Color Palette

### Primary Colors
List with:
- Variable name
- Hex code
- RGB equivalent
- Usage description

Example:
- `--primary-bg`: #0B1729 | rgb(11, 23, 41) | Main background color
- `--accent`: #FF6B35 | rgb(255, 107, 53) | CTAs and highlights

### Neutral Scale (if applicable)
- Gray-50 through Gray-900
- Usage for each shade

### Semantic Colors
- Success, Error, Warning, Info
- With hex codes and usage

### Gradients (if used)
- Full CSS gradient syntax
- Where used (hero, cards, buttons)

## 3. Typography

### Font Families
```css
--font-primary: 'Inter', -apple-system, sans-serif;
--font-mono: 'Roboto Mono', monospace;
```

### Type Scale
For each level (xs, sm, base, lg, xl, 2xl, 3xl, 4xl):
- Font size (px or rem)
- Line height (unitless ratio or px)
- Font weight
- Letter spacing (if relevant)

Example:
```css
--text-xl: {
  font-size: 20px;
  line-height: 1.6;
  font-weight: 600;
  letter-spacing: -0.01em;
}
```

### Font Weights
- Available weights (400, 500, 600, 700)
- When to use each

### Text Hierarchy
- H1, H2, H3, H4, H5, H6
- Body text
- Small text / captions
- With exact sizes and weights for each

## 4. Spacing System

### Base Scale
```css
--spacing-1: 4px;
--spacing-2: 8px;
--spacing-3: 12px;
--spacing-4: 16px;
--spacing-6: 24px;
--spacing-8: 32px;
--spacing-12: 48px;
--spacing-16: 64px;
--spacing-20: 80px;
--spacing-24: 96px;
```

### Usage Guidelines
- When to use each spacing value
- Margin vs padding conventions
- Gap in flex/grid layouts

## 5. Component Styles

For EACH component, provide complete CSS with exact values:

### Buttons

**Primary Button:**
```css
.btn-primary {
  background: var(--accent-color);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 16px;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background: var(--accent-dark);
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(255, 107, 53, 0.3);
}

.btn-primary:active {
  transform: translateY(0);
}
```

**Secondary Button:**
[Full CSS]

**Outline Button:**
[Full CSS]

### Cards
```css
.card {
  background: [...];
  border: [...];
  border-radius: [...];
  padding: [...];
  box-shadow: [...];
  transition: [...];
}

.card:hover {
  [...];
}
```

### Form Elements

**Input:**
[Full CSS]

**Textarea:**
[Full CSS]

**Select:**
[Full CSS]

### Navigation
[Full CSS for nav, header, etc]

### Other Components
- Badges
- Tags
- Modals
- Tooltips
- Alerts
- Loading states

## 6. Shadows & Elevation

```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.2);
--shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.3);
--shadow-2xl: 0 25px 50px rgba(0, 0, 0, 0.4);
```

### Usage Guidelines
- When to use each shadow level
- Hover state shadows
- Active state shadows

## 7. Border Radius

```css
--radius-sm: 4px;   /* badges, tags */
--radius-base: 8px; /* buttons, inputs */
--radius-md: 12px;  /* cards */
--radius-lg: 16px;  /* modals, large cards */
--radius-xl: 24px;  /* hero sections */
--radius-full: 9999px; /* pills, avatars */
```

## 8. Animations & Transitions

### Timing Functions
```css
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
```

### Durations
```css
--duration-fast: 150ms;
--duration-base: 250ms;
--duration-slow: 350ms;
```

### Common Transitions
- Button hover
- Card hover
- Link hover
- Modal open/close
- Fade in/out

### Keyframe Animations (if any)
[Full @keyframes code]

## 9. Grid & Layout System

### Container
```css
.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
}
```

### Breakpoints
```css
--breakpoint-sm: 640px;   /* Mobile */
--breakpoint-md: 768px;   /* Tablet */
--breakpoint-lg: 1024px;  /* Desktop */
--breakpoint-xl: 1280px;  /* Wide desktop */
--breakpoint-2xl: 1536px; /* Ultra-wide */
```

### Grid System
- Columns (12-col, flexbox, CSS grid)
- Gutters
- Spacing between sections

## 10. Best Practices & Guidelines

- How to combine colors
- How to choose spacing values
- How to maintain hierarchy
- Common patterns to use
- Common mistakes to avoid

---

Remember: Be EXTREMELY specific with all values. Use actual numbers, hex codes, and CSS syntax. This guide will be the single source of truth for all future designs using this system.
```

---

## Phase 4: Apply Style Guide to New Designs

### Prompt 4.1: Generate New Page/Feature

```
Help me design a [FEATURE/PAGE] based on the style guide from design-clones/[site]/style_guide.md

Requirements:
- Follow the style guide EXACTLY
- Use the exact colors from the palette
- Follow the typography scale precisely
- Apply the correct spacing system
- Use the defined component styles
- Include appropriate shadows and border radius
- Add transitions where appropriate

Make it pixel-perfect and completely consistent with the design system.

[Optional: Add specific feature requirements]
```

### Prompt 4.2: Convert to React/Next.js

```
Great! Now let's convert this to a production-ready Next.js application.

Please:
1. Create a Next.js project structure with TypeScript and Tailwind
2. Extract design tokens into lib/constants.ts:
   - Colors
   - Spacing
   - Typography
   - Shadows
   - Border radius
   - Transitions

3. Create reusable components in components/ui/:
   - Button (with variants: primary, secondary, outline)
   - Card
   - Input
   - Badge
   - [other components]

4. Create layout components in components/layout/:
   - Header
   - Footer
   - Container

5. Set up globals.css with:
   - CSS reset
   - CSS variables
   - Base styles

Make everything pixel-perfect and production-ready.
```

### Prompt 4.3: Create Animated Demo

```
Using Framer Motion, create an animated demo that showcases [FEATURE].

Requirements:
- Use the style guide colors, typography, and spacing
- Follow the transition timings from the style guide
- Create smooth, professional animations
- Make it interactive
- Should be exportable as video for marketing

Specific animation flow:
[Describe the flow]

Use the actual UI components from our design system.
```

### Prompt 4.4: Generate Slide Deck

```
Create a slide deck presentation using the style guide from design-clones/[site]/style_guide.md

Topic: [TOPIC]
Number of slides: [NUMBER]

Requirements:
- Follow brand colors exactly
- Use the typography scale
- Apply proper spacing
- Include smooth transitions
- Professional, on-brand design

Slide breakdown:
1. [Title slide]
2. [Content slide]
...
```

---

## Debugging Prompts

### Debug 1: Color Mismatch

```
I'm comparing the generated [element] with the original, and the color doesn't match exactly.

Original color (from color picker): [HEX]
Current color in code: [HEX]

Please update to use the exact color from the original.
```

### Debug 2: Spacing Issues

```
The spacing looks off. Let me check the style guide...

According to the style guide, [element] should have:
- Padding: [VALUE]
- Margin: [VALUE]
- Gap: [VALUE]

But the current code has different values. Please fix to match the style guide exactly.
```

### Debug 3: Typography Inconsistency

```
The text styling doesn't match the style guide.

From style guide:
- Font: [FAMILY]
- Size: [SIZE]
- Weight: [WEIGHT]
- Line height: [HEIGHT]

Please update the [element] to match these exact values.
```

---

## Best Practices

1. **Always extract styles first** using `extract_styles.py`
2. **Never rush the reference page** - iterate until 100% perfect
3. **Only extract style guide after reference page is perfect**
4. **Use exact values** - never approximate
5. **Reference style guide in all future prompts**
6. **Validate against reference page** after each new design
7. **Use CSS variables** for consistency
8. **Build component library** for reusability

---

## Anti-Patterns (Don't Do This)

❌ **Skip extraction and use screenshots only**
- Result: 60-70% accuracy, not good enough

❌ **Extract style guide before reference page is perfect**
- Result: Style guide will have approximated values

❌ **Use vague descriptions in style guide**
- "Blue color" instead of "#635BFF"
- "Medium spacing" instead of "16px"

❌ **Generate new designs without referencing style guide**
- Result: Inconsistent designs that drift from original

❌ **Accept "good enough"**
- Goal is always 100% fidelity

---

## Success Metrics

### Reference Page
- ✅ Colors match exactly (verified with color picker)
- ✅ Typography is pixel-perfect
- ✅ Spacing is precise
- ✅ Component styles replicated
- ✅ Indistinguishable from original

### Style Guide
- ✅ All hex codes specified
- ✅ All spacing values in px/rem
- ✅ Complete CSS code blocks for components
- ✅ Exact transition timings
- ✅ No vague descriptions

### Generated Designs
- ✅ 100% consistent with style guide
- ✅ Uses design tokens
- ✅ Maintains brand coherence
- ✅ Professional quality
- ✅ Production-ready code
