# 📖 VibeCode Premium Builder - Exemplos Práticos

## Exemplo 1: Criar App de Fitness Tracker (do Zero)

### Input do Usuário

```
Quero criar um app premium de fitness tracker para registrar treinos e ver estatísticas.
Precisa ter lista de treinos, adicionar exercícios, e gráficos de progresso.
```

### Skill Ativada: vibecode-premium-builder

**Detecção:** Cenário A (criar do zero)

---

### Output da Skill

```markdown
✅ Plano VibeCode Premium: FitTracker

## 📱 FRONTEND (VibeCode)

Cole os prompts abaixo em SEQUÊNCIA no VibeCode:

### Prompt 1: Estrutura Base
```
Create a fitness tracker app with 3 tabs: Workouts, Stats, and Profile.

Workouts tab:
- List of workout sessions (card format)
- Each card shows: workout name, date, duration, exercises count
- Floating action button (+) to add new workout

Stats tab:
- Weekly/monthly progress charts
- Total workouts count
- Total time exercised
- Favorite exercises list

Profile tab:
- User info (name, photo, goal)
- Settings (notifications, units)
- About section

Use iOS native design: white background, SF Pro font, blue accent (#007AFF).
```

### Prompt 2: Bottom Tab Bar
```
Use react-native-bottom-tabs and @bottom-tabs/react-navigation package to implement Native bottom tabs.

Tab 1: "Workouts" (icon: dumbbell)
Tab 2: "Stats" (icon: chart.bar)
Tab 3: "Profile" (icon: person.circle)
```

### Prompt 3: Large Headers (Workouts Screen)
```
We want a large header title on the Workouts screen. Using a React Navigation Native Stack navigator, set `headerLargeTitle: true` and `headerTransparent: true` in screen options.
```

### Prompt 4: Large Headers (Stats Screen)
```
We want a large header title on the Stats screen. Using a React Navigation Native Stack navigator, set `headerLargeTitle: true` and `headerTransparent: true` in screen options.
```

### Prompt 5: Context Menu (Workout Cards)
```
Use Zeego ContextMenu on workout cards; open on long-press; map items/submenus with native look (no custom styling).

Context menu options:
- Edit Workout
- Delete Workout
- Share Progress
- Duplicate Workout
```

### Prompt 6: Bottom Sheet (Add Workout)
```
Use the @gorhom/bottom-sheet for adding new workouts; define snap points ['50%', '90%'], backdrop, and enablePanDownToClose for iOS feel.

Bottom sheet content:
- Input: Workout name
- Date picker: Workout date
- Input: Duration (minutes)
- Button: Add Exercises
- Button: Save Workout
```

### Prompt 7: Date Picker (Workout Date)
```
Use @react-native-community/datetimepicker in the Add Workout bottom sheet; present mode="date" and handle onChange inline/modal on iOS. Use black text color for white background.
```

### Prompt 8: Switch (Notifications Settings)
```
Use the native iOS style switch component in Profile > Settings screen. You can import this from "react-native".

Switches needed:
- Workout reminders
- Progress notifications
- Weekly summary
```

### Prompt 9: Haptics (Manual)
```
❌ NÃO É PROMPT! Configure manualmente no VibeCode:

Adicione haptics nos seguintes locais:
1. Ao salvar novo treino → "success" haptic
2. Ao deletar treino → "heavy" haptic
3. Ao mudar de tab → "light" haptic
4. Ao abrir bottom sheet (add workout) → "light" haptic
5. Ao toggle switches (settings) → "light" haptic
6. Erro de validação (nome vazio) → "error" haptic
```

## 🔧 BACKEND (Claude Code)

### Endpoints necessários:

```
BASE_URL/api/v1

Auth:
  POST /auth/register
  POST /auth/login
  POST /auth/refresh

Workouts:
  GET    /workouts           # List user workouts
  GET    /workouts/:id       # Get workout details
  POST   /workouts           # Create workout
  PUT    /workouts/:id       # Update workout
  DELETE /workouts/:id       # Delete workout

Exercises:
  GET    /workouts/:id/exercises    # List exercises in workout
  POST   /workouts/:id/exercises    # Add exercise to workout
  DELETE /exercises/:id             # Remove exercise

Stats:
  GET /stats/summary        # Weekly/monthly stats
  GET /stats/progress       # Progress chart data
```

### Database Schema:

```sql
users
  id              UUID PRIMARY KEY
  email           VARCHAR(255) UNIQUE
  password_hash   VARCHAR(255)
  name            VARCHAR(100)
  photo_url       TEXT
  goal            VARCHAR(255)
  created_at      TIMESTAMP

workouts
  id              UUID PRIMARY KEY
  user_id         UUID REFERENCES users(id)
  name            VARCHAR(255)
  date            DATE
  duration        INTEGER  -- minutes
  created_at      TIMESTAMP
  updated_at      TIMESTAMP

exercises
  id              UUID PRIMARY KEY
  workout_id      UUID REFERENCES workouts(id) ON DELETE CASCADE
  name            VARCHAR(255)
  sets            INTEGER
  reps            INTEGER
  weight          DECIMAL(5,2)  -- kg
  notes           TEXT
```

### Autenticação:
- Método: JWT (simples, stateless)
- Tokens: Access (15min) + Refresh (7 dias)

### Stack Sugerida:
```
Backend: FastAPI (Python)
Database: PostgreSQL (Supabase)
Hosting: Railway
Storage: Nextcloud (fotos de perfil)
```

## 🎯 Próximos Passos:

1. ✅ Cole Prompt 1 no VibeCode → aguarde app base
2. ✅ Cole Prompt 2 → adiciona tabs nativos
3. ✅ Cole Prompt 3 e 4 → headers animados
4. ✅ Cole Prompt 5 → context menus
5. ✅ Cole Prompt 6 e 7 → bottom sheet + date picker
6. ✅ Cole Prompt 8 → switches Liquid Glass
7. ⚠️ Configure haptics manualmente (seguir Prompt 9)
8. ✅ Teste o app no iPhone
9. ✅ Confirme para eu construir o backend aqui

**Tempo estimado VibeCode:** 15-20 minutos
**Tempo estimado Backend:** 2-3 horas
```

---

### Resultado Final

**Frontend:** App iOS nativo com aparência Apple premium
**Backend:** API REST completa + PostgreSQL
**Features Premium:** ✅ Todos os 7 elementos (Large Headers, Context Menus, Bottom Tabs, Bottom Sheets, Date Pickers, Switches, Haptics)

---

## Exemplo 2: Replicar App "Notion" (Método 4 - Site)

### Input do Usuário

```
Quero replicar o Notion para iOS. Crie algo parecido com visual deles e funcionalidade de notas.
```

### Skill Ativada: vibecode-premium-builder

**Detecção:** Cenário B (replicar app)

---

### Skill Pergunta:

```
Qual método prefere para análise do Notion?
1. 📸 Screenshot (arraste imagens aqui)
2. 🔗 Link App Store
3. 🎥 Vídeo YouTube (demo do app)
4. 🌐 Site/Landing Page
```

### Usuário Responde:

```
4 - Site oficial: https://www.notion.so
```

---

### Skill Invoca website-cloner:

```bash
Skill("website-cloner")
Input: https://www.notion.so
```

### website-cloner Retorna:

```yaml
colors:
  background: "#FFFFFF"
  sidebar: "#F7F6F3"
  primary: "#000000"
  secondary: "#37352F"
  accent: "#2EAADC"
  border: "#E9E9E7"

typography:
  heading1: "Inter, 40px, 700"
  heading2: "Inter, 30px, 600"
  heading3: "Inter, 24px, 600"
  body: "Inter, 16px, 400"
  caption: "Inter, 14px, 400"

spacing:
  page_padding: "96px"
  section: "48px"
  card: "16px"

components:
  - Top navigation (sticky)
  - Sidebar (collapsible)
  - Content editor
  - Card grid (templates)
  - Breadcrumb navigation
```

---

### Skill Adapta Web → iOS:

**Tradução:**
- Top nav (sticky) → **Large Header**
- Sidebar → **Bottom Tab Bar** (3 tabs: Pages, Templates, Settings)
- Content editor → **Bottom Sheet** (full screen)
- Card long-press → **Context Menu** (Edit, Delete, Duplicate, Share)
- Toggle switches → **Liquid Glass Switches** (Dark mode, Notifications)

---

### Output da Skill:

```markdown
✅ Análise completa: Notion Clone para iOS

## 🎨 Design System Extraído

**Cores (adaptadas do site):**
- Background: #FFFFFF
- Sidebar: #F7F6F3
- Text Primary: #000000
- Text Secondary: #37352F
- Accent: #2EAADC
- Borders: #E9E9E7

**Tipografia (adaptada para SF Pro):**
- Large Title: SF Pro Display, 34px, Bold
- Title: SF Pro Display, 28px, Semibold
- Headline: SF Pro Text, 17px, Semibold
- Body: SF Pro Text, 17px, Regular
- Caption: SF Pro Text, 13px, Regular

**Componentes identificados:**
- Navigation bar → Large Header
- Sidebar → Bottom Tab Bar
- Content editor → Bottom Sheet
- Template cards → Context Menu

## 📱 FRONTEND (VibeCode)

Cole os prompts abaixo em SEQUÊNCIA:

### Prompt 1: Estrutura Base (Notion Clone)
```
Create a notes app inspired by Notion with 3 tabs: My Pages, Templates, and Settings.

My Pages tab:
- List of user notes/pages (card format)
- Each card shows: page icon, title, preview text, last edited date
- Floating action button (+) to create new page
- Search bar at top

Templates tab:
- Grid of template cards
- Categories: Work, Personal, Goals, Projects
- Each template shows preview thumbnail

Settings tab:
- User profile section
- App settings (dark mode, notifications, sync)
- About & Support

Design:
- Background: #FFFFFF
- Cards background: #F7F6F3
- Text primary: #000000
- Accent: #2EAADC
- Use Inter-like font (SF Pro)
```

### Prompt 2: Bottom Tab Bar
```
Use react-native-bottom-tabs and @bottom-tabs/react-navigation package to implement Native bottom tabs.

Tab 1: "My Pages" (icon: doc.text)
Tab 2: "Templates" (icon: square.grid.2x2)
Tab 3: "Settings" (icon: gear)
```

### Prompt 3: Large Header (My Pages)
```
We want a large header title "My Pages" on the first tab screen. Using a React Navigation Native Stack navigator, set `headerLargeTitle: true` and `headerTransparent: true` in screen options.
```

### Prompt 4: Context Menu (Page Cards)
```
Use Zeego ContextMenu on page cards; open on long-press; map items/submenus with native look (no custom styling).

Context menu options:
- Open Page
- Edit
- Duplicate
- Move to...
- Delete
- Share
```

### Prompt 5: Bottom Sheet (Create/Edit Page)
```
Use the @gorhom/bottom-sheet for creating/editing pages; define snap points ['90%', '100%'], backdrop, and enablePanDownToClose for iOS feel.

Bottom sheet content:
- Page icon selector (emoji picker)
- Title input (large, bold)
- Rich text editor (simple: bold, italic, lists)
- Formatting toolbar
- Save button (top-right)
```

### Prompt 6: Switch (Settings)
```
Use the native iOS style switch component in Settings tab. You can import this from "react-native".

Switches:
- Dark Mode (appearance)
- Push Notifications
- Auto-sync
- Show previews in list
```

### Prompt 7: Haptics (Manual)
```
❌ NÃO É PROMPT! Configure manualmente:

1. Ao criar nova página → "success" haptic
2. Ao deletar página → "heavy" haptic
3. Ao duplicar página → "medium" haptic
4. Ao mudar de tab → "light" haptic
5. Ao abrir bottom sheet (editor) → "light" haptic
6. Ao toggle switches → "light" haptic
```

## 🔧 BACKEND (Claude Code)

### Endpoints:

```
Pages:
  GET    /pages              # List user pages
  GET    /pages/:id          # Get page content
  POST   /pages              # Create page
  PUT    /pages/:id          # Update page
  DELETE /pages/:id          # Delete page
  POST   /pages/:id/duplicate # Duplicate page

Templates:
  GET /templates             # List available templates
  GET /templates/:id         # Get template
  POST /pages/from-template  # Create page from template
```

### Database Schema:

```sql
pages
  id              UUID PRIMARY KEY
  user_id         UUID REFERENCES users(id)
  title           VARCHAR(255)
  icon            VARCHAR(10)  -- emoji
  content         JSONB         -- rich text blocks
  parent_id       UUID REFERENCES pages(id)  -- nested pages
  created_at      TIMESTAMP
  updated_at      TIMESTAMP
  last_edited     TIMESTAMP

templates
  id              UUID PRIMARY KEY
  name            VARCHAR(255)
  category        VARCHAR(50)
  icon            VARCHAR(10)
  content         JSONB
  thumbnail_url   TEXT
```

### Stack:
```
Backend: FastAPI (Python)
Database: PostgreSQL (Supabase)
Rich Text: JSON format (Notion-like blocks)
```

## 🎯 Próximos Passos:

1-7. Cole prompts sequencialmente no VibeCode
8. Configure haptics manualmente
9. Teste no iPhone
10. Confirme para backend

**Design fidelity:** ~85% (web → iOS adaptação)
```

---

### Resultado Final

**Frontend:** Notion Clone para iOS com design adaptado + premium features
**Backend:** API REST para páginas/templates + PostgreSQL
**Integração:** website-cloner extraiu design automaticamente

---

## Exemplo 3: Quick Request (Apenas Prompts)

### Input do Usuário

```
Me dá só os prompts VibeCode para adicionar large header e haptics em qualquer app.
```

### Output da Skill

```markdown
✅ Prompts VibeCode - Quick Reference

### Large Header
```
We want a large header title on the screen. Using a React Navigation Native Stack navigator, set `headerLargeTitle: true` and `headerTransparent: true` in screen options.
```

### Haptics (Manual - não é prompt)
Configure no VibeCode app:
1. Clique botão "Haptics"
2. Selecione ação/componente
3. Escolha tipo: light, medium, heavy, success, error

**Recomendações:**
- Criar item → success
- Deletar → heavy
- Tab change → light
- Abrir modal → light
- Erro → error
```

---

**Nota:** Para casos simples, skill retorna apenas prompts solicitados sem plano completo.

---

## Padrões Identificados nos Exemplos

### Pattern 1: Apps Multi-Screen
- Sempre adicionar **Bottom Tab Bar**
- Large Headers em **todas** as tabs principais
- Context Menus em **listas/cards**

### Pattern 2: Apps com Formulários
- Sempre usar **Bottom Sheets** para create/edit
- Date/Time Pickers quando lidar com **datas**
- Switches para **configurações booleanas**

### Pattern 3: Haptics Universal
```
Create → success
Delete → heavy
Update → medium
Navigate → light
Error → error
```

---

**Última atualização:** 2025-11-04
**Versão:** 1.0
