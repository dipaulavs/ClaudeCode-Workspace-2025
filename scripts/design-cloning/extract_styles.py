#!/usr/bin/env python3
"""
Extract CSS styles and design system from any website.

Uses Playwright to:
- Capture all external stylesheets
- Extract inline styles
- Compute styles of key elements
- Capture CSS variables
- Take screenshot for reference

Usage:
    python3 scripts/design-cloning/extract_styles.py https://example.com
    python3 scripts/design-cloning/extract_styles.py https://example.com --output custom-name

Based on methodology from: https://www.youtube.com/watch?v=vcJVnyhmLS4
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ Error: playwright not installed")
    print("   Install with: pip3 install playwright")
    print("   Then run: playwright install chromium")
    sys.exit(1)


def sanitize_filename(url: str) -> str:
    """Convert URL to safe directory name."""
    parsed = urlparse(url)
    domain = parsed.netloc.replace('www.', '')
    return re.sub(r'[^\w\-]', '-', domain)


def extract_styles(url: str, output_name: str = None) -> dict:
    """
    Extract all CSS styles from a website.

    Returns dict with:
    - styles_css: Concatenated CSS from all sources
    - computed_styles: JSON of computed styles for key elements
    - variables_css: CSS variables only
    - screenshot_path: Path to screenshot
    """

    print("=" * 70)
    print("🎨 WEBSITE STYLE EXTRACTION")
    print("=" * 70)
    print()
    print(f"🔗 URL: {url}")
    print(f"⏳ Starting extraction...\n")

    # Setup output directory
    if output_name:
        site_name = output_name
    else:
        site_name = sanitize_filename(url)

    output_dir = Path.cwd() / 'design-clones' / site_name / 'extracted'
    output_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        # Launch browser
        print("🌐 Launching browser...")
        browser = p.chromium.launch(headless=True)

        # Create context with realistic user agent
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='en-US'
        )

        page = context.new_page()

        try:
            # Navigate to URL
            print(f"📄 Loading {url}...")
            page.goto(url, wait_until='networkidle', timeout=60000)

            # Wait a bit for any JS-injected styles
            page.wait_for_timeout(2000)

            print("✅ Page loaded successfully\n")

            # 1. Extract all stylesheets
            print("📋 Extracting stylesheets...")
            all_styles = page.evaluate('''
            () => {
                const styles = [];

                // Get all <style> tags (inline and injected)
                document.querySelectorAll('style').forEach(style => {
                    if (style.textContent) {
                        styles.push({
                            type: 'inline',
                            content: style.textContent
                        });
                    }
                });

                // Get all <link> stylesheets
                document.querySelectorAll('link[rel="stylesheet"]').forEach(link => {
                    styles.push({
                        type: 'external',
                        href: link.href
                    });
                });

                return styles;
            }
            ''')

            # Concatenate all styles
            styles_content = []
            for style in all_styles:
                if style['type'] == 'inline':
                    styles_content.append(f"/* Inline/Injected Styles */\n{style['content']}\n")
                else:
                    styles_content.append(f"/* External: {style['href']} */\n")

            all_css = "\n".join(styles_content)

            # 2. Extract CSS variables
            print("🎨 Extracting CSS variables...")
            css_variables = page.evaluate('''
            () => {
                const root = document.querySelector(':root');
                const styles = getComputedStyle(root);
                const variables = {};

                for (let prop of styles) {
                    if (prop.startsWith('--')) {
                        variables[prop] = styles.getPropertyValue(prop).trim();
                    }
                }

                return variables;
            }
            ''')

            # Build CSS variables file
            variables_css = ":root {\n"
            for var_name, var_value in css_variables.items():
                variables_css += f"  {var_name}: {var_value};\n"
            variables_css += "}\n"

            # 3. Extract computed styles of key elements
            print("🔍 Computing styles for key elements...")
            computed_styles = page.evaluate('''
            () => {
                const elements = {};

                // Key elements to extract
                const selectors = [
                    'body',
                    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                    'p', 'a',
                    'button', 'input', 'textarea',
                    'nav', 'header', 'footer', 'main',
                    '.card', '.btn', '.button'
                ];

                selectors.forEach(selector => {
                    const el = document.querySelector(selector);
                    if (el) {
                        const computed = getComputedStyle(el);

                        elements[selector] = {
                            // Colors
                            color: computed.color,
                            backgroundColor: computed.backgroundColor,
                            borderColor: computed.borderColor,

                            // Typography
                            fontFamily: computed.fontFamily,
                            fontSize: computed.fontSize,
                            fontWeight: computed.fontWeight,
                            lineHeight: computed.lineHeight,
                            letterSpacing: computed.letterSpacing,

                            // Spacing
                            margin: computed.margin,
                            padding: computed.padding,

                            // Box model
                            width: computed.width,
                            height: computed.height,
                            borderWidth: computed.borderWidth,
                            borderStyle: computed.borderStyle,
                            borderRadius: computed.borderRadius,

                            // Effects
                            boxShadow: computed.boxShadow,
                            opacity: computed.opacity,

                            // Layout
                            display: computed.display,
                            position: computed.position,

                            // Transform & transition
                            transform: computed.transform,
                            transition: computed.transition
                        };
                    }
                });

                return elements;
            }
            ''')

            # 4. Take screenshot
            print("📸 Taking screenshot...")
            screenshot_path = output_dir / 'screenshot.png'
            page.screenshot(path=str(screenshot_path), full_page=True)

            # Save all extracted data
            print("\n💾 Saving extracted data...")

            # Save concatenated CSS
            styles_file = output_dir / 'styles.css'
            with open(styles_file, 'w', encoding='utf-8') as f:
                f.write(all_css)
            print(f"   ✓ {styles_file.relative_to(Path.cwd())}")

            # Save CSS variables
            variables_file = output_dir / 'variables.css'
            with open(variables_file, 'w', encoding='utf-8') as f:
                f.write(variables_css)
            print(f"   ✓ {variables_file.relative_to(Path.cwd())}")

            # Save computed styles as JSON
            computed_file = output_dir / 'computed_styles.json'
            with open(computed_file, 'w', encoding='utf-8') as f:
                json.dump(computed_styles, f, indent=2)
            print(f"   ✓ {computed_file.relative_to(Path.cwd())}")

            # Save screenshot
            print(f"   ✓ {screenshot_path.relative_to(Path.cwd())}")

            # Generate summary
            print("\n" + "=" * 70)
            print("✅ EXTRACTION COMPLETE!")
            print("=" * 70)
            print()
            print(f"📂 Output directory: {output_dir.relative_to(Path.cwd())}")
            print()
            print("📊 Summary:")
            print(f"   • CSS extracted: {len(all_css)} characters")
            print(f"   • CSS variables: {len(css_variables)} found")
            print(f"   • Elements analyzed: {len(computed_styles)}")
            print()

            # Try to identify key design characteristics
            print("🎨 Key Design Characteristics:")

            if 'body' in computed_styles:
                body = computed_styles['body']
                print(f"   • Background: {body['backgroundColor']}")
                print(f"   • Text color: {body['color']}")
                print(f"   • Font: {body['fontFamily']}")
                print(f"   • Base font size: {body['fontSize']}")

            # Look for common color variables
            if css_variables:
                color_vars = {k: v for k, v in css_variables.items() if 'color' in k.lower() or 'bg' in k.lower()}
                if color_vars:
                    print("\n   Color Variables:")
                    for var, value in list(color_vars.items())[:5]:
                        print(f"      {var}: {value}")

            print()
            print("📝 Next Steps:")
            print("   1. Review extracted CSS in styles.css")
            print("   2. Check computed_styles.json for precise values")
            print("   3. Use screenshot.png as visual reference")
            print("   4. Create reference.html using extracted styles")
            print("   5. Iterate until pixel-perfect match")
            print("   6. Extract detailed style guide")
            print()
            print("=" * 70)

            return {
                'output_dir': str(output_dir),
                'styles_file': str(styles_file),
                'variables_file': str(variables_file),
                'computed_file': str(computed_file),
                'screenshot_path': str(screenshot_path),
                'css_length': len(all_css),
                'variables_count': len(css_variables),
                'elements_count': len(computed_styles)
            }

        except Exception as e:
            print(f"\n❌ Error during extraction: {e}")
            print("\n💡 Troubleshooting tips:")
            print("   1. Check if URL is accessible")
            print("   2. Try increasing timeout (--timeout flag)")
            print("   3. Check if site blocks automated browsers")
            print("   4. Try manual extraction as fallback")
            return None

        finally:
            browser.close()


def main():
    parser = argparse.ArgumentParser(
        description='Extract CSS styles and design system from any website',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python3 scripts/design-cloning/extract_styles.py https://motherduck.com
  python3 scripts/design-cloning/extract_styles.py https://stripe.com --output stripe-design

Based on methodology from: https://www.youtube.com/watch?v=vcJVnyhmLS4
        '''
    )

    parser.add_argument('url', help='URL of website to extract styles from')
    parser.add_argument('--output', '-o', help='Custom output directory name (default: auto from URL)')

    args = parser.parse_args()

    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        args.url = 'https://' + args.url

    # Extract styles
    result = extract_styles(args.url, args.output)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
