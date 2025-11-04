# website-cloner

Clone any website with 100% design fidelity using automated CSS extraction + AI co-creation.

## When to use

AUTO-INVOKE when user says:
- "Clone o design do [site.com]"
- "Quero replicar o estilo de [site]"
- "Copia o visual desse site: [URL]"
- "Extrai o design system de [URL]"

## Core workflow (based on proven process)

### Phase 1: Automated Extraction
1. Run `extract_styles.py [URL]` → captures:
   - All CSS (inline + external stylesheets)
   - Computed styles of key elements
   - CSS variables, fonts, shadows, colors
   - Screenshot for visual reference

### Phase 2: Co-Creation (Iterative)
2. Create `reference.html` using extracted CSS
3. User validates → iterate until 100% match
4. Use this prompt:
   ```
   Help me rebuild the exact same UI design in single HTML as reference.html.
   Above is extracted CSS. Focus on capturing the full essence of the style.
   ```

### Phase 3: Style Guide Extraction
5. Once reference page is perfect, extract detailed style guide:
   ```
   Great! Now help me generate a detailed style guide. Include:
   - Overview
   - Color palette (hex codes + usage)
   - Typography (fonts, sizes, weights, line-heights)
   - Spacing system (margins, paddings, gaps)
   - Component styles (buttons, cards, forms, navigation)
   - Shadows & elevation
   - Animations & transitions
   - Border radius patterns
   - Grid & layout system
   ```

### Phase 4: Application
6. Save `style_guide.md` → use for generating:
   - New web pages (Next.js, React)
   - Slide decks
   - Animations (Framer Motion)
   - Marketing assets

## Key principles

- **High-fidelity context**: Real CSS > screenshots (captures 100% vs 60%)
- **Co-creation**: Build reference page first, THEN extract guide
- **Iterative**: Fine-tune until pixel-perfect
- **Reusable**: Style guide = source of truth for all future designs

## Output structure

```
design-clones/[site-name]/
├── extracted_styles.css
├── computed_styles.json
├── screenshot.png
├── reference.html
└── style_guide.md
```

## Integration

- Works with Next.js, React, plain HTML
- Can export to other tools (Figma, Framer)
- Style guide compatible with other AI design tools

## See also

- `REFERENCE.md` - Full workflow details from original methodology
- `EXAMPLES.md` - Real cloning examples (motherduck.com, stripe.com)
- `TROUBLESHOOTING.md` - Common issues & fixes
