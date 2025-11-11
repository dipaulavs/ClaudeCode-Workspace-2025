# App Analysis Methods

Complete guide for analyzing existing apps to replicate in VibeCode.

## Method 1: Screenshot Analysis

**Input:** User-provided screenshots

**Analysis Framework:**

### 1. Layout Structure
- Grid/Stack/List arrangement
- Number of sections
- Visual hierarchy
- Navigation patterns

### 2. Color Palette
Extract exact hex codes:
- Background: #XXXXXX
- Primary: #XXXXXX
- Secondary: #XXXXXX
- Accent: #XXXXXX
- Text: #XXXXXX

### 3. Typography
Identify font characteristics:
- Header: [font family] [size] [weight]
- Body: [font family] [size] [weight]
- Caption: [font family] [size] [weight]

### 4. Components Detected
- [ ] Bottom Tabs
- [ ] Cards
- [ ] Lists
- [ ] Forms
- [ ] Buttons
- [ ] Images/Icons

### 5. Spacing/Padding
- Container: [value]px
- Between items: [value]px
- Section margins: [value]px

**Output:** Design system + VibeCode prompts adapted to detected patterns

---

## Method 2: App Store Link

**Input:** App Store URL (e.g., `https://apps.apple.com/us/app/...`)

**Process:**

1. WebFetch the App Store page
2. Extract official screenshots
3. Apply Method 1 analysis to screenshots
4. Read app description for feature insights
5. Check reviews for UX patterns mentioned

**Output:** Same as Method 1 + feature list from description

---

## Method 3: YouTube Demo Video

**Input:** YouTube URL with app demonstration

**Process:**

1. Use `scripts/extraction/transcribe_video.py` to transcribe
2. Analyze transcript for:
   - Features mentioned verbally
   - User flows described
   - Components referenced
3. Identify UI patterns from video frames
4. Map functionality to VibeCode components

**Output:** Feature list + component mapping + VibeCode prompts

---

## Method 4: Website/Landing Page

**Input:** Official website URL

**Process:**

1. **Invoke website-cloner skill:**
   ```
   Skill("website-cloner")
   Input: Website URL
   Output: Complete style guide
   ```

2. **Receive extracted design system:**
   ```yaml
   colors:
     background: "#FFFFFF"
     primary: "#007AFF"
     secondary: "#5856D6"
     text: "#000000"

   typography:
     heading: "SF Pro Display, 34px, bold"
     body: "SF Pro Text, 17px, regular"

   spacing:
     container: "16px"
     section: "32px"

   components:
     - Navigation
     - Hero section
     - Card grid
     - Forms
   ```

3. **Web → iOS Component Mapping:**

   | Web Component | iOS Equivalent | VibeCode Prompt |
   |---------------|----------------|-----------------|
   | Sticky nav | Large Header | Prompt: Large Headers |
   | Dropdown menu | Context Menu | Prompt: Context Menu |
   | Modal dialog | Bottom Sheet | Prompt: Bottom Sheet |
   | `<input type="date">` | DateTimePicker | Prompt: Date Picker |
   | Toggle/checkbox | Switch | Prompt: Switch |
   | Hover effects | Haptics | Manual config |
   | Tab bar | Bottom Tab Bar | Prompt: Bottom Tabs |

4. **Adapt design system to iOS:**
   - Use SF Pro font family
   - Adjust spacing for mobile (reduce by ~30%)
   - Apply iOS color semantics
   - Convert web interactions to touch patterns

**Output:** iOS-adapted design system + complete VibeCode prompt sequence

---

## Analysis Quality Checklist

Before generating prompts, ensure:

- [ ] All colors extracted with hex codes
- [ ] Typography fully specified (family, size, weight)
- [ ] Spacing values measured consistently
- [ ] All interactive components identified
- [ ] Navigation pattern clear (tabs/stack/modal)
- [ ] Data inputs mapped to iOS pickers
- [ ] Haptic opportunities identified

---

## Common Patterns

### E-commerce Apps
- Bottom Tabs: Home, Search, Cart, Profile
- Context Menu: Product cards (Save, Share, Add to Cart)
- Bottom Sheet: Filters, Product details
- Large Header: Category screens

### Social Apps
- Bottom Tabs: Feed, Explore, Post, Notifications, Profile
- Context Menu: Posts (Save, Share, Report, Hide)
- Bottom Sheet: Create post, Comments
- Large Header: Profile screen

### Productivity Apps
- Bottom Tabs: Tasks, Calendar, Notes, Settings
- Context Menu: Task items (Edit, Delete, Duplicate, Move)
- Bottom Sheet: Create/Edit forms
- Date/Time Pickers: Due dates, reminders
- Large Header: Main list screens

---

**Last updated:** 2025-01-07
