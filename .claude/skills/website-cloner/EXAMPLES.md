# website-cloner - Examples

## Example 1: Cloning MotherDuck.com (From Original Video)

**Context:** User wants to replicate MotherDuck's dark, modern, data-focused design.

### User Request
```
Clone o design do motherduck.com
```

### Skill Execution

**Step 1: Extract styles**
```bash
python3 scripts/design-cloning/extract_styles.py https://motherduck.com
```

**Output:**
```
✅ CSS extraction complete!

📂 Saved to: design-clones/motherduck/extracted/
   • styles.css (12.4 KB)
   • computed_styles.json (8.1 KB)
   • variables.css (1.2 KB)
   • screenshot.png

🎨 Key findings:
   - Color scheme: Dark blue (#0A1628) with orange accents (#FF6B35)
   - Typography: Inter (primary), Roboto Mono (code)
   - Spacing: 8px base scale
   - Border radius: 8px standard
```

**Step 2: Co-create reference page**

Assistant creates `reference.html` and presents to user:

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    /* Extracted CSS applied here */
    :root {
      --primary-bg: #0A1628;
      --accent-orange: #FF6B35;
      --text-primary: #FFFFFF;
      --spacing-md: 16px;
    }
    /* ... rest of styles ... */
  </style>
</head>
<body>
  <!-- Simple page showcasing the style -->
  <header>
    <h1>Sample Header</h1>
    <button class="cta">Get Started</button>
  </header>
  <!-- ... -->
</body>
</html>
```

**Step 3: User validates and iterates**

User: "The background color looks slightly different"

Assistant checks computed styles:
```
Found: Background should be #0B1729 (not #0A1628)
Updated in reference.html
```

User: "Perfect! Now it matches 100%"

**Step 4: Extract style guide**

Assistant uses the specialized prompt:
```
Great! Now help me generate a detailed style guide...
```

**Generated `style_guide.md`:**
```markdown
# MotherDuck Style Guide

## Overview
Modern, data-centric design with dark theme and warm orange accents.
Professional yet approachable. Focus on clarity and readability.

## Color Palette

### Primary Colors
- `--primary-bg`: #0B1729 (Deep navy background)
- `--accent-orange`: #FF6B35 (CTA and highlights)
- `--text-primary`: #FFFFFF (Primary text)
- `--text-secondary`: #94A3B8 (Secondary text)

### Neutral Scale
- `--gray-50`: #F8FAFC
- `--gray-100`: #F1F5F9
- ...
- `--gray-900`: #0F172A

## Typography

### Font Families
- Primary: 'Inter', -apple-system, sans-serif
- Monospace: 'Roboto Mono', monospace

### Type Scale
- `--text-xs`: 12px / 1.4
- `--text-sm`: 14px / 1.5
- `--text-base`: 16px / 1.5
- `--text-lg`: 18px / 1.6
- `--text-xl`: 20px / 1.6
- `--text-2xl`: 24px / 1.3
- `--text-3xl`: 30px / 1.2
- `--text-4xl`: 36px / 1.1

### Font Weights
- Regular: 400
- Medium: 500
- Semibold: 600
- Bold: 700

## Spacing System
Base: 4px

- `--spacing-1`: 4px
- `--spacing-2`: 8px
- `--spacing-3`: 12px
- `--spacing-4`: 16px
- `--spacing-6`: 24px
- `--spacing-8`: 32px
- `--spacing-12`: 48px
- `--spacing-16`: 64px

## Component Styles

### Buttons

**Primary Button:**
```css
background: var(--accent-orange);
color: white;
padding: 12px 24px;
border-radius: 8px;
font-weight: 600;
transition: transform 0.2s, box-shadow 0.2s;

hover: transform: translateY(-2px);
       box-shadow: 0 8px 16px rgba(255, 107, 53, 0.3);
```

**Secondary Button:**
```css
background: transparent;
border: 1px solid var(--accent-orange);
color: var(--accent-orange);
/* ... */
```

### Cards
```css
background: rgba(255, 255, 255, 0.05);
border: 1px solid rgba(255, 255, 255, 0.1);
border-radius: 12px;
padding: 24px;
backdrop-filter: blur(10px);
```

## Shadows & Elevation

- `--shadow-sm`: 0 1px 2px rgba(0, 0, 0, 0.05)
- `--shadow-md`: 0 4px 6px rgba(0, 0, 0, 0.1)
- `--shadow-lg`: 0 10px 15px rgba(0, 0, 0, 0.2)
- `--shadow-xl`: 0 20px 25px rgba(0, 0, 0, 0.3)

## Animations

### Transitions
- Fast: 150ms ease
- Base: 250ms ease
- Slow: 350ms ease

### Hover Effects
- Lift: translateY(-2px)
- Scale: scale(1.05)
- Glow: box-shadow increase

## Border Radius
- Small: 4px (badges, tags)
- Base: 8px (buttons, inputs)
- Medium: 12px (cards)
- Large: 16px (modals)
- Full: 9999px (pills, avatars)

## Grid & Layout

### Container
- Max-width: 1280px
- Padding: 0 24px

### Breakpoints
- Mobile: 640px
- Tablet: 768px
- Desktop: 1024px
- Wide: 1280px
```

**Step 5: Apply to new designs**

User: "Now create a personal to-do app with this style"

Assistant generates `todo.html` following the style guide exactly:
- Uses #0B1729 background
- Orange accent buttons
- Inter typography
- 8px border radius
- Proper spacing scale
- Glassmorphic cards

Result: **100% consistent** with MotherDuck brand.

---

## Example 2: Cloning Stripe.com for SaaS Landing Page

**Context:** User building SaaS product wants Stripe's clean, professional aesthetic.

### User Request
```
Clone o design do stripe.com para usar no meu produto SaaS
```

### Skill Execution

**Step 1: Extract**
```bash
python3 scripts/design-cloning/extract_styles.py https://stripe.com
```

**Output:**
```
✅ CSS extraction complete!

📂 Saved to: design-clones/stripe/extracted/
   • styles.css (18.7 KB)
   • computed_styles.json (11.3 KB)
   • variables.css (2.1 KB)
   • screenshot.png

🎨 Key findings:
   - Color scheme: White/light gray with purple accents (#635BFF)
   - Typography: Söhne (custom), fallback to system fonts
   - Spacing: 4px base scale
   - Border radius: Varied (4px-16px)
   - Heavy use of gradients and subtle animations
```

**Step 2-3: Co-create & iterate**

Assistant builds reference page, user validates:
- "The purple is slightly more vibrant" → Updated to #635BFF
- "Font fallback should be cleaner" → Updated to system-ui stack
- "Gradient needs more stops" → Refined gradient

Result: Pixel-perfect reference page.

**Step 4: Extract style guide**

Key sections from generated guide:

```markdown
# Stripe Style Guide

## Color Palette

### Brand Colors
- `--purple-primary`: #635BFF (Primary CTA)
- `--purple-dark`: #0A2540 (Headings)
- `--blue-accent`: #00D4FF (Accents)

### Gradients
- Hero: linear-gradient(180deg, #635BFF 0%, #0A2540 100%)
- Card: linear-gradient(135deg, #F6F9FC 0%, #FFFFFF 100%)

## Typography

### Font Stack
- Primary: 'Söhne', system-ui, -apple-system, sans-serif
- Code: 'Söhne Mono', 'Courier New', monospace

### Hierarchy
- Hero (h1): 72px / 1.1 / 700
- Section (h2): 48px / 1.2 / 600
- Subsection (h3): 32px / 1.3 / 600
- Body: 18px / 1.6 / 400

## Component Styles

### CTA Button
```css
background: var(--purple-primary);
color: white;
padding: 14px 28px;
border-radius: 6px;
font-weight: 500;
font-size: 16px;
transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);

hover:
  background: #554CD4;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(99, 91, 255, 0.4);
```

### Feature Card
```css
background: white;
border: 1px solid #E3E8EF;
border-radius: 12px;
padding: 32px;
box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
transition: box-shadow 0.3s, transform 0.3s;

hover:
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  transform: translateY(-4px);
```

## Animations

### Page Transitions
- Fade-in: opacity 0 → 1 over 400ms
- Slide-up: translateY(20px) → 0 over 500ms
- Stagger: 80ms delay between elements

### Micro-interactions
- Button hover: 150ms cubic-bezier
- Card hover: 300ms ease-out
- Link underline: 200ms ease
```

**Step 5: Apply to SaaS landing**

User: "Create a landing page for my SaaS product with pricing section"

Assistant generates:
- Hero section with Stripe-style gradient
- Feature cards with hover effects
- Pricing cards with purple accents
- Footer matching Stripe's layout
- All animations and transitions included

Result: Professional SaaS landing page, **100% on-brand** with Stripe aesthetic.

---

## Example 3: Converting Clone to Next.js App

**Context:** User wants to turn cloned design into production app.

### User Request (After cloning motherduck.com)
```
Convert this to a Next.js app with reusable components
```

### Skill Execution

**Step 1: Create Next.js structure**

```bash
npx create-next-app@latest design-app --typescript --tailwind --app
```

**Step 2: Generate component library**

Assistant breaks down reference.html into:

```
design-app/
├── app/
│   ├── layout.tsx          # Root layout with theme
│   ├── page.tsx            # Homepage
│   └── globals.css         # Global styles from style guide
├── components/
│   ├── ui/
│   │   ├── Button.tsx      # Primary, secondary, outline variants
│   │   ├── Card.tsx        # Glassmorphic card component
│   │   ├── Input.tsx       # Form inputs
│   │   └── Badge.tsx       # Status badges
│   └── layout/
│       ├── Header.tsx      # Navigation header
│       ├── Footer.tsx      # Footer
│       └── Container.tsx   # Max-width container
└── lib/
    └── constants.ts        # Design tokens from style guide
```

**Generated `lib/constants.ts`:**
```typescript
export const colors = {
  primaryBg: '#0B1729',
  accentOrange: '#FF6B35',
  textPrimary: '#FFFFFF',
  textSecondary: '#94A3B8',
  // ... from style guide
}

export const spacing = {
  1: '4px',
  2: '8px',
  3: '12px',
  // ... from style guide
}

export const typography = {
  fontFamily: {
    primary: 'Inter, -apple-system, sans-serif',
    mono: 'Roboto Mono, monospace',
  },
  // ... from style guide
}
```

**Generated `components/ui/Button.tsx`:**
```typescript
import { colors, spacing } from '@/lib/constants'

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline'
  children: React.ReactNode
  onClick?: () => void
}

export function Button({ variant = 'primary', children, onClick }: ButtonProps) {
  const styles = {
    primary: {
      background: colors.accentOrange,
      color: 'white',
      // ... exact styles from style guide
    },
    // ... other variants
  }

  return (
    <button
      className="px-6 py-3 rounded-lg font-semibold transition-all hover:-translate-y-0.5"
      style={styles[variant]}
      onClick={onClick}
    >
      {children}
    </button>
  )
}
```

Result: Production-ready Next.js app with pixel-perfect components.

---

## Example 4: Creating Animated Demo Video

**Context:** User needs product demo video matching cloned brand.

### User Request
```
Create an animated demo showing task creation flow with Framer Motion
```

### Skill Execution

**Using Framer Motion with style guide:**

```typescript
import { motion } from 'framer-motion'
import { Button, Card, Input } from '@/components/ui'

export function TaskCreationDemo() {
  return (
    <div className="demo-container">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Card>
          <motion.h2
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            Create New Task
          </motion.h2>

          <motion.div
            initial={{ width: 0 }}
            animate={{ width: '100%' }}
            transition={{ delay: 0.6, duration: 0.8 }}
          >
            <Input placeholder="Enter task details..." />
          </motion.div>

          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 1.2, type: 'spring' }}
          >
            <Button>Add Task</Button>
          </motion.div>
        </Card>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ delay: 1.8 }}
        className="task-list"
      >
        {/* Animated task list appears */}
      </motion.div>
    </div>
  )
}
```

Result:
- Smooth animations matching brand timing (from style guide)
- Colors and typography exactly from style guide
- Can export as MP4 for marketing
- Interactive on website

---

## Key Takeaways from Examples

### What Makes These Work

1. **Real CSS extraction** → 100% accuracy (not 60-70% from screenshots)
2. **Co-creation process** → Iterative refinement to pixel-perfect
3. **Detailed style guide** → Single source of truth
4. **Reusable across contexts** → Web, mobile, slides, videos, animations

### Common Pattern

```
Extract → Co-create → Style Guide → Apply Everywhere
```

### Results

- MotherDuck clone: Dark theme to-do app (100% consistent)
- Stripe clone: SaaS landing page (professional quality)
- Next.js conversion: Production-ready component library
- Animated demos: On-brand motion design

All achieved **pixel-perfect fidelity** through high-fidelity context + co-creation process.