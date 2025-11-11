# 📚 VibeCode Premium Builder - Documentação Técnica

## Índice

1. [⚠️ REGRA CRÍTICA: Consultar Documentação](#regra-crítica-consultar-documentação)
2. [Prompts VibeCode Completos](#prompts-vibecode-completos)
3. [Análise de Apps (4 Métodos)](#análise-de-apps-4-métodos)
4. [Backend Planning Framework](#backend-planning-framework)
5. [Integração com website-cloner](#integração-com-website-cloner)
6. [Haptics Strategy](#haptics-strategy)

---

## ⚠️ REGRA CRÍTICA: Consultar Documentação

### SEMPRE Fazer WebFetch ANTES de Gerar Prompts

**URL obrigatória:**
```
https://vibecodeapp.com/docs/prompting/native-ui-components
```

**Processo:**

```
1. WebFetch(https://vibecodeapp.com/docs/prompting/native-ui-components)
   ↓
2. Extrair prompts EXATOS para cada componente:
   - Large Header Titles
   - Context Menu
   - Bottom Tab Bar
   - Bottom Sheets/Modals
   - Date/Time Pickers
   - iOS-Style Switch
   ↓
3. Armazenar texto EXATO de cada prompt
   ↓
4. NUNCA inventar/modificar estrutura dos prompts
   ↓
5. APENAS adaptar variáveis contextuais:
   - Nomes de telas
   - Nomes de tabs
   - Itens de menu
   - Snap points específicos
   - Mode do date picker
```

**Exemplo de adaptação CORRETA:**

```
❌ ERRADO (inventar):
"Add a large animated header to the Workouts screen"

✅ CERTO (doc + adaptar):
Passo 1: WebFetch → extrair prompt exato:
  "We want a large header title on the screen. Using a React
   Navigation Native Stack navigator, set `headerLargeTitle: true`
   and `headerTransparent: true` in screen options."

Passo 2: Adaptar contexto:
  "We want a large header title on the WORKOUTS screen. Using a React
   Navigation Native Stack navigator, set `headerLargeTitle: true`
   and `headerTransparent: true` in screen options."
```

**Por quê essa regra existe:**

1. **Docs podem mudar** - Packages, props, métodos atualizados
2. **Precisão técnica** - Prompts específicos = funcionamento garantido
3. **Evitar erros** - Prompts "inventados" podem não funcionar no VibeCode
4. **Consistência** - Sempre usar linguagem que VibeCode entende

**Quando não consultar docs:**

- ❌ NUNCA - SEMPRE consultar, sem exceções

---

## Prompts VibeCode Completos

**⚠️ ATENÇÃO:** Prompts abaixo são REFERÊNCIA. SEMPRE fazer WebFetch para versão mais atualizada antes de usar.

### 1. Large Header Titles

**Prompt:**
```
We want a large header title on the screen. Using a React Navigation Native Stack navigator, set `headerLargeTitle: true` and `headerTransparent: true` in screen options.
```

**Quando usar:**
- Telas principais (Home, Lista, Perfil)
- Header precisa diminuir ao scrollar

**Resultado:** Header grande → pequeno (animado)

---

### 2. Context Menu

**Prompt:**
```
Use Zeego ContextMenu; open on long-press; map items/submenus with native look (no custom styling).
```

**Quando usar:**
- Itens de lista (tarefas, posts, produtos)
- Cards clicáveis
- Ações rápidas (delete, edit, share)

**Resultado:** Long-press → menu nativo iOS

---

### 3. Bottom Tab Bar

**Prompt:**
```
Use react-native-bottom-tabs and @bottom-tabs/react-navigation package to implement Native bottom tabs.
```

**Quando usar:**
- App com 2+ seções principais
- Navegação entre telas independentes

**Resultado:** Tabs inferiores nativas (igual App Store)

---

### 4. Bottom Sheet/Modal

**Prompt:**
```
Use the @gorhom/bottom-sheet; define snap points, backdrop, and enablePanDownToClose for iOS feel. Make multiple snap points including a full screen version.
```

**Snap points sugeridos:** `['10%', '50%', '75%', '100%']`

**Quando usar:**
- Formulários (adicionar item, editar)
- Detalhes expansíveis
- Filtros/opções

**Resultado:** Modal deslizante de baixo (Apple Maps style)

---

### 5. Date/Time Pickers

**Prompt:**
```
Use @react-native-community/datetimepicker; present mode="date" / "time" and handle onChange inline/modal on iOS. Use black text color for white background apps.
```

**Variações:**
- `mode="date"` → Seletor de data
- `mode="time"` → Seletor de hora
- `mode="datetime"` → Ambos

**Quando usar:**
- Agendamentos, lembretes, eventos
- Filtros por data

**Resultado:** Picker rolante nativo iOS

---

### 6. Liquid Glass Switch

**Prompt:**
```
Use the native iOS style switch component. You can import this from "react-native"
```

**Quando usar:**
- Toggles on/off (notificações, modo escuro)
- Configurações

**Resultado:** Switch com efeito Liquid Glass

---

### 7. Haptics

**Não precisa de prompt!** Use interface VibeCode:

**Tipos de haptic:**
- `light` → Toque suave (ações comuns)
- `medium` → Toque médio (confirmações)
- `heavy` → Toque forte (ações críticas)
- `success` → Feedback de sucesso
- `error` → Feedback de erro

**Locais estratégicos:**
1. Ao criar/salvar item → `success`
2. Ao deletar item → `heavy`
3. Ao mudar de tab → `light`
4. Ao abrir bottom sheet → `light`
5. Ao toggle switch → `light`
6. Erro de validação → `error`

---

## Análise de Apps (4 Métodos)

### Método 1: Screenshot

**Input:** Imagens do usuário (drag & drop)

**Análise:**
```
Para cada screenshot:
1. Layout Structure
   - Grid/Stack/List?
   - Quantas seções?
   - Hierarquia visual

2. Color Palette
   - Background: #XXXXXX
   - Primary: #XXXXXX
   - Secondary: #XXXXXX
   - Accent: #XXXXXX
   - Text: #XXXXXX

3. Typography
   - Header: [font] [size]
   - Body: [font] [size]
   - Caption: [font] [size]

4. Components Detectados
   - [ ] Tabs
   - [ ] Cards
   - [ ] Lists
   - [ ] Forms
   - [ ] Buttons
   - [ ] Images

5. Spacing/Padding
   - Container: [value]
   - Between items: [value]
```

**Output:** Prompts VibeCode adaptados

---

### Método 2: Link App Store

**Input:** URL App Store (ex: `https://apps.apple.com/br/app/...`)

**Processo:**
1. WebFetch da página
2. Extrair screenshots oficiais
3. Analisar igual Método 1

---

### Método 3: Vídeo YouTube

**Input:** URL YouTube com demo

**Processo:**
1. Usar `scripts/extraction/transcribe_video.py`
2. Analisar transcrição (features mencionadas)
3. Identificar componentes verbalmente descritos
4. Gerar prompts baseado em funcionalidades

---

### Método 4: Site/Landing Page

**Input:** URL do site oficial

**Processo:**
1. 🚨 **CHAMAR SKILL `website-cloner`:**
   ```
   Skill("website-cloner")
   Input: URL do site
   Output: Style guide completo
   ```

2. **Receber style guide:**
   - Cores (hex codes)
   - Fontes (família + tamanhos)
   - Espaçamentos
   - Layout patterns
   - Componentes usados

3. **Adaptar Web → iOS:**
   ```
   Web Component          iOS Equivalent
   ─────────────────      ──────────────
   <nav>                  Bottom Tab Bar
   <header>               Large Header
   <dialog>               Bottom Sheet
   <input type="date">    DateTimePicker
   <input type="checkbox"> Switch
   Hover effects          Haptics
   ```

4. **Gerar prompts VibeCode** com design adaptado

---

## Backend Planning Framework

### Estrutura Padrão

Para qualquer app, gerar:

#### 1. API Endpoints

```
BASE_URL/api/v1

Auth:
  POST /auth/register
  POST /auth/login
  POST /auth/refresh
  POST /auth/logout

Resource (exemplo: tasks):
  GET    /tasks          # List all
  GET    /tasks/:id      # Get one
  POST   /tasks          # Create
  PUT    /tasks/:id      # Update
  DELETE /tasks/:id      # Delete
```

#### 2. Database Schema

```sql
-- Exemplo: App de tarefas

users
  id              UUID PRIMARY KEY
  email           VARCHAR(255) UNIQUE
  password_hash   VARCHAR(255)
  name            VARCHAR(100)
  created_at      TIMESTAMP
  updated_at      TIMESTAMP

tasks
  id              UUID PRIMARY KEY
  user_id         UUID REFERENCES users(id)
  title           VARCHAR(255)
  description     TEXT
  due_date        TIMESTAMP
  completed       BOOLEAN DEFAULT false
  created_at      TIMESTAMP
  updated_at      TIMESTAMP
```

#### 3. Autenticação

**Opções (perguntar ao usuário):**
- JWT (simples, stateless)
- Session-based (tradicional)
- OAuth (Google/Apple Sign In)

**Padrão recomendado:** JWT

#### 4. Stack Sugerida

```
Frontend: VibeCode (React Native)
Backend: FastAPI (Python) ou Express (Node.js)
Database: PostgreSQL (Supabase) ou MongoDB
Hosting: Railway / Render / Vercel (backend)
Storage: Nextcloud / S3 (imagens/arquivos)
```

---

## Integração com website-cloner

### Quando Ativar

```
if método_análise == "Site/Landing Page":
    invoke Skill("website-cloner")
```

### Input para website-cloner

```
URL: [site fornecido pelo usuário]
Objetivo: Extrair design system para adaptar em iOS
```

### Output Esperado

```yaml
colors:
  background: "#FFFFFF"
  primary: "#007AFF"
  secondary: "#5856D6"
  text: "#000000"

typography:
  heading: "SF Pro Display, 34px, bold"
  body: "SF Pro Text, 17px, regular"
  caption: "SF Pro Text, 13px, regular"

spacing:
  container: "16px"
  section: "32px"
  item: "12px"

components:
  - Navigation bar
  - Hero section
  - Card grid
  - Contact form
  - Footer
```

### Tradução Web → iOS

**Usar tabela de equivalências:**

| Web | iOS (VibeCode) | Prompt |
|-----|----------------|--------|
| Sticky nav | Large Header | Prompt 1 |
| Dropdown menu | Context Menu | Prompt 2 |
| Modal dialog | Bottom Sheet | Prompt 4 |
| Date input | DateTimePicker | Prompt 5 |
| Toggle switch | Switch | Prompt 6 |

---

## Haptics Strategy

### Mapa de Eventos → Haptics

```javascript
// Usuário CRIA algo
onCreate → success (vibração de recompensa)

// Usuário SALVA/ATUALIZA
onSave → medium (confirmação)

// Usuário DELETA
onDelete → heavy (ação irreversível)

// Navegação
onTabChange → light (transição suave)
onBottomSheetOpen → light (movimento)

// Interações
onSwitchToggle → light (feedback imediato)
onButtonPress → light (toque registrado)

// Erros
onValidationError → error (alerta)
onNetworkError → error (problema)
```

### Implementação no VibeCode

**Usuário faz manualmente:**
1. Clicar botão **Haptics** na interface
2. Selecionar componente/ação
3. Escolher tipo de haptic
4. Salvar

**Nosso output:** Listar ONDE adicionar haptics + QUAL tipo

---

## Ordem de Execução dos Prompts

**IMPORTANTE:** Prompts devem ser colados em SEQUÊNCIA no VibeCode.

```
1º → Estrutura base do app
      (telas, navegação, componentes básicos)

2º → Bottom Tab Bar (se multi-tela)

3º → Large Headers (telas principais)

4º → Context Menus (itens de lista)

5º → Bottom Sheets (formulários/detalhes)

6º → Date/Time Pickers (se necessário)

7º → Switches (toggles)

8º → Haptics (últimos, pois dependem dos componentes)
```

**Razão:** Componentes básicos antes de animações/interações.

---

## VibeCode Docs

**Fonte oficial:** https://vibecodeapp.com/docs/prompting/native-ui-components

**Atualização:** Verificar docs antes de gerar prompts (podem ter mudanças).

---

## Templates de Resposta

### Template: App do Zero

```markdown
✅ Plano VibeCode Premium: [NOME DO APP]

## 📱 FRONTEND (VibeCode)

Cole os prompts abaixo em SEQUÊNCIA:

### Prompt 1: Estrutura Base
```
[prompt inicial com descrição do app + telas principais]
```

### Prompt 2: Large Headers
```
[prompt large header]
```

[...continuar para todos os 7 prompts]

## 🔧 BACKEND (Claude Code)

### Endpoints necessários:
- [lista de endpoints]

### Database Schema:
```sql
[schema SQL]
```

### Autenticação:
- Método: [JWT/OAuth/Session]

## 🎯 Próximos Passos:
1. Cole Prompt 1 no VibeCode → aguarde completar
2. Cole Prompt 2 → aguarde completar
3. [...continuar sequencialmente]
4. Adicione haptics manualmente (locais indicados)
5. Confirme para eu construir o backend
```

### Template: Replicar App

```markdown
✅ Análise completa: [NOME DO APP ORIGINAL]

## 🎨 Design System Extraído

**Cores:**
- Background: #XXXXXX
- Primary: #XXXXXX
- [...]

**Tipografia:**
- Headers: [especificação]
- [...]

**Componentes identificados:**
- [lista]

## 📱 Adaptação para iOS (VibeCode)

[...mesma estrutura do template anterior, mas adaptando design]
```

---

**Última atualização:** 2025-11-04
**Versão:** 1.0
