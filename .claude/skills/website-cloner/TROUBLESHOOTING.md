# website-cloner - Troubleshooting

## Common Issues & Solutions

### Issue 1: Colors Look Different from Original Site

**Symptoms:**
- Background color is close but not exact (#0A1628 instead of #0B1729)
- Accent colors appear duller or more saturated
- Gradients don't match precisely

**Causes:**
- AI approximating from screenshot instead of using extracted CSS
- Using RGB instead of exact hex values
- Missing alpha channels in rgba() colors
- Display color profiles causing perception differences

**Solutions:**

✅ **Verify extracted CSS was actually used:**
```bash
# Check if extracted styles are present
grep "#0B1729" design-clones/[site]/extracted/styles.css
```

✅ **Use browser DevTools to confirm exact values:**
```
1. Open original site
2. Right-click element → Inspect
3. In Styles panel, check computed color value
4. Copy EXACT hex/rgba value
5. Update reference.html with exact value
```

✅ **Check for CSS variables:**
```css
/* Original might use variables */
:root {
  --primary-bg: #0B1729;
}

/* Make sure these are in your reference.html */
```

✅ **Compare side-by-side:**
```
1. Open original site in one browser tab
2. Open reference.html in another tab
3. Use color picker tool (Digital Color Meter on Mac)
4. Sample exact pixels from both
5. Adjust until values match exactly
```

---

### Issue 2: Playwright Script Fails to Extract CSS

**Symptoms:**
- Script times out
- No CSS files extracted
- Error: "Navigation timeout exceeded"
- Empty styles.css file

**Causes:**
- Site requires JavaScript to load
- Slow network connection
- Site blocks automated browsers
- Anti-bot protection (Cloudflare, etc)

**Solutions:**

✅ **Increase timeout:**
```python
# In extract_styles.py
page.goto(url, timeout=60000)  # Increase from 30s to 60s
```

✅ **Wait for network idle:**
```python
page.goto(url, wait_until='networkidle')
```

✅ **Handle redirects:**
```python
page.goto(url, wait_until='domcontentloaded')
page.wait_for_load_state('networkidle')
```

✅ **Bypass bot detection:**
```python
# Use stealth mode
from playwright.sync_api import sync_playwright

context = browser.new_context(
    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
    viewport={'width': 1920, 'height': 1080},
    locale='en-US'
)
```

✅ **Manual fallback:**
If script still fails, use manual extraction:
```
1. Open site in browser
2. Right-click → Inspect
3. In Styles panel, select all CSS
4. Copy to design-clones/[site]/extracted/styles.css
5. Proceed with co-creation step
```

---

### Issue 3: Reference Page Doesn't Look Right

**Symptoms:**
- Layout is broken
- Fonts don't load
- Images are missing
- Spacing is way off

**Causes:**
- Missing external resources (fonts, images)
- CSS specificity conflicts
- Media queries not applied
- Box-sizing differences

**Solutions:**

✅ **Check font loading:**
```html
<!-- Add to reference.html <head> -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

✅ **Add CSS reset:**
```css
/* Add to top of styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
```

✅ **Verify viewport:**
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

✅ **Check for missing CSS:**
```bash
# Look for @import statements in extracted CSS
grep "@import" design-clones/[site]/extracted/styles.css

# Download those imported files too
```

✅ **Simplify first:**
Start with minimal HTML to test CSS is working:
```html
<!DOCTYPE html>
<html>
<head>
  <style>
    /* Paste extracted CSS here */
  </style>
</head>
<body>
  <div style="background: var(--primary-bg); padding: 20px;">
    <h1>Test Heading</h1>
    <button class="btn-primary">Test Button</button>
  </div>
</body>
</html>
```

If this works, gradually add more HTML structure.

---

### Issue 4: Style Guide is Too Generic

**Symptoms:**
- Style guide has vague descriptions
- Missing specific values (colors say "blue" instead of "#635BFF")
- Component styles are approximated
- No clear hierarchy or system

**Causes:**
- AI generated guide from screenshot instead of reference page
- Prompt didn't specify enough detail
- Reference page wasn't pixel-perfect yet

**Solutions:**

✅ **ALWAYS co-create reference page FIRST:**
```
Do NOT ask for style guide until reference.html is 100% accurate
```

✅ **Use the exact prompt from methodology:**
```
Great! Now help me generate a detailed style guide. Include:
- Overview
- Color palette (WITH HEX CODES + usage descriptions)
- Typography (fonts, sizes IN PX OR REM, weights AS NUMBERS, line-heights)
- Spacing system (EXACT values: 4px, 8px, 16px, etc)
- Component styles (WITH CSS CODE BLOCKS)
- Shadows & elevation (EXACT box-shadow values)
- Animations & transitions (EXACT timing functions)
- Border radius patterns (EXACT values)
- Grid & layout system (EXACT max-width, breakpoints)

Be extremely specific with all values. Use code blocks for CSS.
```

✅ **Iterate on the style guide:**
```
User: "The button padding in the style guide is wrong, it should be 12px 24px"
Assistant: *Updates style guide with correct values*
```

✅ **Extract from reference page directly:**
```
Inspect element in reference.html → Copy computed styles → Add to style guide
```

---

### Issue 5: Consistency Issues When Applying Style Guide

**Symptoms:**
- New pages don't quite match reference page
- Colors are close but slightly off
- Spacing inconsistent between pages
- Button styles vary slightly

**Causes:**
- AI not strictly following style guide
- Style guide has ambiguous descriptions
- CSS variables not being used
- Manual overrides in code

**Solutions:**

✅ **Use design tokens / CSS variables:**
```css
/* In globals.css or constants.ts */
:root {
  --color-primary: #0B1729;
  --color-accent: #FF6B35;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --border-radius-base: 8px;
}

/* Then in components, ALWAYS reference variables */
.button {
  background: var(--color-accent);  /* NOT #FF6B35 */
  padding: var(--spacing-md);       /* NOT 16px */
  border-radius: var(--border-radius-base);
}
```

✅ **Create component library:**
Don't recreate styles each time. Build reusable components:
```typescript
// components/ui/Button.tsx
import { COLORS, SPACING, RADIUS } from '@/lib/constants'

export function Button() {
  // Uses design tokens from single source of truth
}
```

✅ **Reference style guide in every prompt:**
```
Help me design a settings page.
Use the style guide from design-clones/motherduck/style_guide.md
Follow it EXACTLY - same colors, spacing, typography, components.
```

✅ **Validate against reference page:**
After generating new page, compare side-by-side with reference.html:
- Same background color? ✓
- Same button style? ✓
- Same spacing? ✓
- Same typography? ✓

---

### Issue 6: Site Has Dynamic Styles (CSS-in-JS, styled-components)

**Symptoms:**
- Playwright extracts very little CSS
- Styles are generated at runtime
- Can't find styles in extracted files

**Causes:**
- Site uses CSS-in-JS (styled-components, emotion, etc)
- Styles are injected by JavaScript after page load
- Inline styles on elements instead of stylesheets

**Solutions:**

✅ **Wait for JS execution:**
```python
# In extract_styles.py
page.goto(url)
page.wait_for_timeout(3000)  # Wait for JS to inject styles
```

✅ **Extract computed styles:**
```python
# Instead of just grabbing <style> tags, compute styles
computed_styles = page.evaluate('''
() => {
  const elements = document.querySelectorAll('*');
  const styles = {};

  elements.forEach(el => {
    const computed = window.getComputedStyle(el);
    // Extract all computed properties
    styles[el.tagName] = {
      color: computed.color,
      background: computed.background,
      // ... etc
    };
  });

  return styles;
}
''')
```

✅ **Extract from <style> tags injected by JS:**
```python
# After page loads, check for injected <style> tags
injected_styles = page.evaluate('''
() => {
  const styleTags = document.querySelectorAll('style[data-styled], style[data-emotion]');
  return Array.from(styleTags).map(tag => tag.textContent).join('\n');
}
''')
```

✅ **Use browser DevTools as fallback:**
```
1. Open site in Chrome
2. Inspect element
3. In Styles panel, see computed styles
4. Copy relevant CSS manually
```

---

### Issue 7: Fonts Look Different

**Symptoms:**
- Font rendering doesn't match original
- Font weights appear incorrect
- Fallback fonts being used

**Causes:**
- Custom fonts not loaded
- Missing @font-face rules
- Font weights not available
- Incorrect font stack

**Solutions:**

✅ **Extract @font-face rules:**
```bash
# Check extracted CSS for font imports
grep "@font-face" design-clones/[site]/extracted/styles.css
grep "font-family" design-clones/[site]/extracted/styles.css
```

✅ **Load fonts from CDN:**
```html
<!-- Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

<!-- Or use @import in CSS -->
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700');
```

✅ **Download custom fonts:**
If site uses proprietary fonts (like Stripe's Söhne):
```
1. Find font files in Network tab (DevTools)
2. Download .woff2 files
3. Add @font-face rules:

@font-face {
  font-family: 'Söhne';
  src: url('./fonts/soehne-buch.woff2') format('woff2');
  font-weight: 400;
}
```

✅ **Use proper fallback stack:**
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
```

---

### Issue 8: Generated Pages Don't Work on Mobile

**Symptoms:**
- Layout breaks on small screens
- Text too small or too large
- Horizontal scroll appears

**Causes:**
- Missing responsive styles
- No viewport meta tag
- Fixed widths instead of responsive units
- Media queries not extracted

**Solutions:**

✅ **Ensure viewport meta tag:**
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

✅ **Extract media queries:**
```bash
grep "@media" design-clones/[site]/extracted/styles.css
```

✅ **Use responsive units:**
```css
/* Instead of fixed px */
.container {
  max-width: 1280px;  /* OK for max */
  padding: clamp(16px, 4vw, 24px);  /* Responsive */
  font-size: clamp(14px, 2vw, 16px);
}
```

✅ **Test at multiple breakpoints:**
```
- Mobile: 375px (iPhone)
- Tablet: 768px (iPad)
- Desktop: 1280px
- Wide: 1920px
```

---

### Issue 9: Animations Don't Work

**Symptoms:**
- Hover effects missing
- Transitions not smooth
- Keyframe animations don't play

**Causes:**
- @keyframes not extracted
- transition properties missing
- JavaScript-based animations not captured

**Solutions:**

✅ **Extract @keyframes:**
```bash
grep "@keyframes" design-clones/[site]/extracted/styles.css
```

✅ **Check for transition properties:**
```css
/* Make sure these are in extracted CSS */
.button {
  transition: all 0.2s ease;
}

.card {
  transition: transform 0.3s, box-shadow 0.3s;
}
```

✅ **For JS animations (like GSAP):**
```
These won't be in CSS. Check original site's JavaScript.
If using Framer Motion or similar, implement manually based on visual observation.
```

✅ **Add common transitions if missing:**
```css
/* Sensible defaults based on style */
* {
  transition: background 0.2s, color 0.2s, border-color 0.2s;
}

button, a {
  transition: all 0.2s ease;
}
```

---

## General Troubleshooting Steps

### Step 1: Verify Extraction Worked
```bash
ls -lh design-clones/[site]/extracted/
# Should see CSS files with reasonable size (not 0 bytes)
```

### Step 2: Test Extracted CSS in Isolation
```html
<!DOCTYPE html>
<html>
<head>
  <style>
    /* Paste ONLY extracted CSS */
  </style>
</head>
<body>
  <h1>Test</h1>
</body>
</html>
```

### Step 3: Compare Side-by-Side
- Original site (left)
- Your reference page (right)
- Use color picker to verify exact colors
- Use ruler to measure spacing

### Step 4: Iterate Until Perfect
Don't move to style guide extraction until reference page is 100%.

### Step 5: Validate Style Guide
After generating style guide, spot-check values against reference page.

---

## When to Ask for Help

If after trying solutions above you still have issues:

1. **Check original video** (https://www.youtube.com/watch?v=vcJVnyhmLS4)
2. **Review REFERENCE.md** for methodology details
3. **Compare with EXAMPLES.md** to see if similar pattern
4. **Ask user for clarification** on specific design intent

Remember: The goal is 100% fidelity, not "good enough."
