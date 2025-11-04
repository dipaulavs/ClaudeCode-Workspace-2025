# website-cloner - Reference Documentation

## Original Methodology Source

**Video:** "How to Teach AI Agents to Clone Websites with 100% Fidelity"
**URL:** https://www.youtube.com/watch?v=vcJVnyhmLS4
**Author:** AI design automation expert

## The Problem

When you give AI agents screenshots and ask to replicate a design, you typically get 60-70% accuracy:
- Colors are slightly off
- Spacing doesn't match
- Fine-grain details get lost
- Typography isn't exact
- Component styles are approximated

This creates a compounding problem: whatever the first page looks like sets the standard for all future pages.

## The Solution: High-Fidelity Context + Co-Creation

### Why Screenshots Alone Fail

Large language models aren't great at extracting precise values from images:
- Can't read exact hex colors
- Can't measure exact spacing
- Can't identify exact font weights
- Miss CSS variables and design tokens

### What Works: Real CSS + Computed Styles

Extract the ACTUAL CSS from the website:
1. Right-click → Inspect Element
2. Copy computed styles from DevTools
3. Or use automated extraction (Playwright/Puppeteer)

This gives you:
- Exact color values (#RRGGBB)
- Precise spacing (px, rem, em)
- Real font stacks and weights
- Actual shadows, transitions, animations
- CSS variables and design tokens

## Step-by-Step Workflow (From Video)

### Step 1: Extract High-Fidelity Context

**Manual approach (from video):**
```
1. Open target website (e.g., motherduck.com)
2. Right-click → Inspect
3. Select HTML element
4. Copy ALL styles from Styles panel
5. Also take screenshots for visual reference
```

**Automated approach (our improvement):**
```bash
python3 scripts/design-cloning/extract_styles.py https://motherduck.com
```

This captures:
- All external stylesheets
- Inline styles
- Computed styles of key elements
- CSS variables (--primary-color, etc)
- Fonts (@font-face rules)
- Keyframe animations
- Media queries

### Step 2: Co-Create Reference Page

**Goal:** Build ONE simple page that captures 100% of the style essence.

**Prompt to use:**
```
Help me rebuild the exact same UI design in single HTML as reference.html.
Above is extracted CSS. Focus on capturing the full essence of the style.
Start with recreating a simple page that represents the overall look and feel.
```

**What this does:**
- Creates playground for fine-tuning
- Establishes reference implementation
- Gives you control over every detail
- Sets the standard for future designs

### Step 3: Iterate to Pixel-Perfect

**Use tools like VistBug (mentioned in video):**
- Click any UI element
- See exact styles (color, spacing, etc)
- Compare with your reference page
- Feed corrections back to AI

**Example iteration:**
```
The background color should be #0A1628 (not #0B1629)
The heading font-weight should be 700 (not 600)
The border-radius should be 8px (not 12px)
```

Keep iterating until reference page is indistinguishable from original.

### Step 4: Extract Detailed Style Guide

**Once reference page is perfect, use this exact prompt:**

```
Great! Now help me generate a detailed style guide.

You must include the following sections:

1. **Overview**
   - Design philosophy
   - Key visual characteristics
   - Brand personality

2. **Color Palette**
   - Primary colors (hex + usage)
   - Secondary colors
   - Neutral colors
   - Semantic colors (success, error, warning)
   - Color scale (50-900 if applicable)

3. **Typography**
   - Font families (primary, secondary)
   - Font sizes scale
   - Font weights used
   - Line heights
   - Letter spacing
   - Text hierarchy (h1-h6, body, caption)

4. **Spacing System**
   - Spacing scale (4px, 8px, 16px, 24px, etc)
   - Margin conventions
   - Padding conventions
   - Gap usage in flex/grid

5. **Component Styles**
   - Buttons (primary, secondary, outline, ghost)
   - Cards (elevation, borders, padding)
   - Forms (inputs, selects, textareas)
   - Navigation (header, sidebar, breadcrumbs)
   - Modals & overlays
   - Badges & tags
   - Loading states

6. **Shadows & Elevation**
   - Shadow scale (sm, md, lg, xl)
   - Usage guidelines (when to use each)

7. **Animations & Transitions**
   - Transition timings
   - Easing functions
   - Hover states
   - Active states
   - Loading animations

8. **Border Radius**
   - Border radius scale
   - Usage per component type

9. **Grid & Layout**
   - Container max-width
   - Grid columns
   - Breakpoints (mobile, tablet, desktop)
   - Spacing between sections
```

### Step 5: Apply to New Designs

**Now you can generate on-brand designs:**

```
Help me design a [personal to-do app] based on this style guide.
Make it pixel-perfect and follow the design system exactly.
Create it as todo.html
```

**The AI will now:**
- Use exact colors from palette
- Follow spacing system precisely
- Apply correct typography scale
- Replicate component styles
- Match shadows and border radius
- Maintain consistent look & feel

## Advanced Applications (From Video)

### 1. Next.js Application

```
Great, now let's rebuild this interface in Next.js app in design-app folder.
Make it pixel perfect with reusable components.
```

Benefits:
- Break down into React components
- Maintain consistency across pages
- Easy to add new features
- Production-ready code

### 2. Animated Demos

```
Please use Framer Motion to create a demo animation where users type in
task details and add a new task, using the real UI components.
```

Creates:
- Smooth, on-brand animations
- Interactive demos
- Video-ready content
- Marketing materials

### 3. Slide Decks

```
Please make a slide deck based on this style guide.
```

Generates:
- Presentations matching brand
- Consistent visual language
- Professional-looking slides

### 4. Export to Design Tools

The style guide can be imported into:
- Figma (via plugins)
- Framer (design mode)
- Google Stitches (AI design tool mentioned in video)
- Other AI design tools

**Example from video:**
```
Copy style guide → Paste in Google Stitches → Ask to design all screens
for a habit tracker app → Get full UI stack in similar style
```

## Tools Mentioned in Video

### VistBug
- Chrome extension
- Click elements to see exact styles
- Quick way to get color values, spacing, etc
- Helps verify AI output matches original

### Framer Motion
- Animation library for React
- Create smooth, interactive animations
- Export as video or embed in website

### Google Stitches
- AI design tool
- Accepts style guide as input
- Generates full screen designs

### Super Design Extension (Tool from video creator)
- Chrome extension
- Automatically extracts design system from any webpage
- Clones page pixel-perfect
- Scans all style files
- Generates high-fidelity style guide
- Exports production-ready React project
- Link: [provided in video description]

## Key Success Factors

### 1. Start with Reference Page
Don't go straight to building your app. First create a simple page that proves you captured the style 100%.

### 2. Iterate Without Mercy
Don't accept "good enough." Keep fine-tuning until it's indistinguishable from the original.

### 3. Style Guide is Source of Truth
Once you have the perfect style guide, treat it as sacred. All future designs must reference it.

### 4. Use Real CSS, Not Approximations
Real CSS values are precise. Screenshots and descriptions lead to approximations.

### 5. Co-Create, Don't Generate
Work WITH the AI to refine the design, rather than expecting perfect output on first try.

## Why This Works

**Traditional approach:**
```
Screenshot → AI guesses → 60% match → Build on flawed foundation →
Inconsistent designs → Redesign work → Wasted time
```

**High-fidelity approach:**
```
Extract CSS → Co-create reference → 100% match → Extract style guide →
Consistent designs → Ship faster → Professional results
```

## Workflow Summary

```
┌─────────────────────────────────────────────────────────────┐
│ 1. EXTRACT                                                  │
│    • Get real CSS from target website                       │
│    • Capture computed styles                                │
│    • Take screenshots for reference                         │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. CO-CREATE                                                │
│    • Build simple reference page                            │
│    • Use extracted CSS                                      │
│    • Iterate until pixel-perfect                            │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. EXTRACT STYLE GUIDE                                      │
│    • Colors, typography, spacing                            │
│    • Components, shadows, animations                        │
│    • Grid, layout, patterns                                 │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. APPLY                                                    │
│    • Generate new pages                                     │
│    • Create apps (Next.js, React)                           │
│    • Build animations, slide decks                          │
│    • Export to other tools                                  │
└─────────────────────────────────────────────────────────────┘
```

## Common Mistakes to Avoid

❌ **Skipping reference page** → Going straight to building app → Inconsistent styles
❌ **Using only screenshots** → AI guesses values → 60-70% accuracy
❌ **Not iterating** → Accepting first output → Mediocre results
❌ **Skipping style guide** → No source of truth → Future designs drift
❌ **Manual inspection only** → Time-consuming → Easy to miss details

✅ **Extract real CSS** → High-fidelity context
✅ **Co-create reference page** → 100% accuracy baseline
✅ **Iterate to perfection** → Pixel-perfect match
✅ **Extract comprehensive guide** → Source of truth
✅ **Automate extraction** → Fast, complete, accurate

## Technical Details

### What to Extract

**CSS Files:**
- External stylesheets (style.css, main.css)
- Inline `<style>` blocks
- Computed styles from DevTools

**Key Properties:**
- Colors (background, text, border)
- Typography (font-family, size, weight, line-height)
- Spacing (margin, padding, gap)
- Shadows (box-shadow, text-shadow)
- Borders (width, style, color, radius)
- Transitions & animations
- Z-index & positioning
- Display & layout (flex, grid)

**Design Tokens:**
- CSS variables (--primary, --spacing-md)
- @import statements
- @font-face rules
- @keyframes animations
- @media queries

### Where to Store Extracted Data

```
design-clones/[site-name]/
├── extracted/
│   ├── styles.css           # All CSS concatenated
│   ├── computed_styles.json # Computed styles as JSON
│   ├── variables.css        # CSS variables only
│   └── screenshot.png       # Visual reference
├── reference.html           # Co-created reference page
└── style_guide.md          # Final style guide
```

## Measurement of Success

**60-70% accuracy:** Colors slightly off, spacing approximate, details lost
**80-90% accuracy:** Looks similar but lacks polish, inconsistencies visible
**100% accuracy:** Indistinguishable from original, pixel-perfect match ✓

The goal is always 100%.
