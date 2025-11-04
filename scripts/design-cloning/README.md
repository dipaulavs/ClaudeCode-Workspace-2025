# Design Cloning Scripts

Clone any website with 100% design fidelity using automated CSS extraction + AI co-creation.

**Based on methodology:** https://www.youtube.com/watch?v=vcJVnyhmLS4

---

## 📚 Overview

Traditional approach (screenshots) → 60-70% accuracy
High-fidelity approach (real CSS extraction) → 100% accuracy

This script automates the CSS extraction step, then you co-create with Claude to achieve pixel-perfect clones.

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip3 install playwright
playwright install chromium
```

### 2. Extract Styles from Any Website

```bash
python3 scripts/design-cloning/extract_styles.py https://motherduck.com
```

### 3. Output

```
design-clones/motherduck/extracted/
├── styles.css              # All CSS concatenated
├── computed_styles.json    # Computed styles of key elements
├── variables.css           # CSS variables only
└── screenshot.png          # Visual reference
```

---

## 🛠️ Usage

### Basic Usage

```bash
python3 scripts/design-cloning/extract_styles.py <URL>
```

### Custom Output Name

```bash
python3 scripts/design-cloning/extract_styles.py https://stripe.com --output stripe-design
```

### Examples

```bash
# Clone MotherDuck design
python3 scripts/design-cloning/extract_styles.py https://motherduck.com

# Clone Stripe design
python3 scripts/design-cloning/extract_styles.py https://stripe.com

# Clone Linear design
python3 scripts/design-cloning/extract_styles.py https://linear.app

# Clone with custom name
python3 scripts/design-cloning/extract_styles.py https://vercel.com --output vercel-dark
```

---

## 📋 Complete Workflow

### Phase 1: Automated Extraction (This Script)

```bash
python3 scripts/design-cloning/extract_styles.py https://example.com
```

**What it does:**
- ✅ Captures all CSS (inline + external)
- ✅ Extracts CSS variables
- ✅ Computes styles for key elements
- ✅ Takes full-page screenshot
- ✅ Organizes everything in output folder

### Phase 2: Co-Creation with Claude

1. **Create reference page:**
   ```
   Claude, help me rebuild the exact same UI design in single HTML as reference.html.
   Use the extracted CSS from design-clones/motherduck/extracted/styles.css
   Also consider the computed styles in computed_styles.json
   Focus on capturing the full essence of the style.
   ```

2. **Iterate until pixel-perfect:**
   - Compare with screenshot.png
   - Check colors with color picker
   - Measure spacing
   - Verify typography
   - Fine-tune until 100% match

### Phase 3: Extract Style Guide

Once reference page is perfect:

```
Great! Now help me generate a detailed style guide. Include:
- Overview (design philosophy)
- Color palette (exact hex codes + usage)
- Typography (fonts, sizes, weights, line-heights)
- Spacing system (exact values)
- Component styles (with CSS code blocks)
- Shadows & elevation (exact values)
- Animations & transitions (timing functions)
- Border radius patterns
- Grid & layout system

Be extremely specific with all values. Use code blocks for CSS.
```

### Phase 4: Apply to New Designs

```
Help me design a [feature/page] based on this style guide.
Make it pixel-perfect and follow the design system exactly.
```

---

## 📁 Output Structure

```
design-clones/
└── [site-name]/
    └── extracted/
        ├── styles.css           # All CSS (10-20 KB typically)
        ├── computed_styles.json # Computed styles as JSON
        ├── variables.css        # CSS variables only
        └── screenshot.png       # Full-page screenshot
```

After co-creation, you'll add:

```
design-clones/[site-name]/
├── extracted/              # (from script)
├── reference.html          # Co-created reference page
└── style_guide.md         # Extracted style guide
```

---

## 🎨 What Gets Extracted

### CSS Files
- All external stylesheets (`<link rel="stylesheet">`)
- Inline `<style>` blocks
- JS-injected styles (styled-components, emotion, etc)

### CSS Variables
```css
:root {
  --primary-color: #0B1729;
  --accent-color: #FF6B35;
  --spacing-md: 16px;
  /* ... all CSS variables */
}
```

### Computed Styles

For key elements (body, headings, buttons, cards, etc):
- Colors (background, text, border)
- Typography (font, size, weight, line-height)
- Spacing (margin, padding)
- Box model (width, height, border, border-radius)
- Effects (box-shadow, opacity)
- Transitions & transforms

### Visual Reference
- Full-page screenshot (1920x1080 viewport)
- Useful for side-by-side comparison

---

## 🔧 Advanced Options

### Custom User Agent

Edit script if site requires specific user agent:

```python
user_agent='Mozilla/5.0 ...'  # Line ~76
```

### Increase Timeout

For slow sites:

```python
page.goto(url, wait_until='networkidle', timeout=120000)  # Line ~88
```

### Wait for JavaScript

For sites with heavy JS:

```python
page.wait_for_timeout(5000)  # Line ~91 (increase from 2000)
```

---

## 🐛 Troubleshooting

### Script Times Out

**Problem:** Site takes too long to load

**Solution:**
```python
# Edit extract_styles.py line ~88
timeout=120000  # Increase from 60000
```

### Empty CSS Files

**Problem:** Site uses CSS-in-JS that loads after page

**Solution:**
```python
# Edit extract_styles.py line ~91
page.wait_for_timeout(5000)  # Increase wait time
```

### Site Blocks Automated Browsers

**Problem:** Cloudflare or similar blocking

**Solution:**
- Use manual extraction (Right-click → Inspect → Copy styles)
- Or try different user agent
- Or use browser extension approach

### Missing Fonts

**Problem:** Custom fonts not loading in extracted CSS

**Solution:**
- Check Network tab in DevTools for font URLs
- Download .woff2 files manually
- Add @font-face rules to extracted CSS

---

## 📖 Related Documentation

- **Skill:** `.claude/skills/website-cloner/SKILL.md`
- **Methodology:** `.claude/skills/website-cloner/REFERENCE.md`
- **Examples:** `.claude/skills/website-cloner/EXAMPLES.md`
- **Troubleshooting:** `.claude/skills/website-cloner/TROUBLESHOOTING.md`

---

## 🎯 Success Criteria

### 60-70% Accuracy (Screenshot Method)
- Colors are close but not exact
- Spacing is approximate
- Fine details lost
- ❌ Not good enough

### 100% Accuracy (This Method)
- ✅ Exact colors (hex matches)
- ✅ Precise spacing (px/rem match)
- ✅ Perfect typography (font/weight/size match)
- ✅ Component styles replicated
- ✅ Animations and transitions included
- ✅ Indistinguishable from original

**Goal: Always 100%**

---

## 💡 Tips

1. **Start simple:** Clone a single page first, not entire site
2. **Iterate ruthlessly:** Don't accept "good enough"
3. **Use color picker:** Verify colors match exactly
4. **Compare side-by-side:** Original vs reference page
5. **Extract guide only after perfect reference:** Don't rush
6. **Use CSS variables:** Makes future designs consistent
7. **Build component library:** Reusable across projects

---

## 🚀 Next Steps After Extraction

1. ✅ Review extracted CSS
2. ✅ Check computed styles JSON
3. ✅ Use screenshot as reference
4. ✅ Create reference.html with Claude
5. ✅ Iterate to pixel-perfect
6. ✅ Extract detailed style guide
7. ✅ Apply to new designs
8. ✅ Convert to Next.js/React if needed
9. ✅ Create animations with Framer Motion
10. ✅ Export to design tools (Figma, etc)

---

## 📦 Dependencies

```bash
# Required
pip3 install playwright

# Install browser
playwright install chromium

# Optional (for advanced features)
pip3 install beautifulsoup4  # For HTML parsing
```

---

## 🤝 Contributing

Found a bug or have improvement ideas?

1. Check TROUBLESHOOTING.md first
2. Review EXAMPLES.md for similar cases
3. Open issue with details

---

## 📄 License

Part of ClaudeCode-Workspace toolkit.

**Methodology credit:** https://www.youtube.com/watch?v=vcJVnyhmLS4
