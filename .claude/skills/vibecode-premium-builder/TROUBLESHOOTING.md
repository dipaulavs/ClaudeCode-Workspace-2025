# 🔧 VibeCode Premium Builder - Troubleshooting

## Problema 1: Prompts VibeCode Não Funcionam Como Esperado

### Sintomas
- VibeCode não aplica Large Header corretamente
- Bottom Sheet não aparece
- Context Menu não funciona no long-press
- Date Picker não mostra

### Causas Possíveis

#### Causa 1.1: Ordem Errada dos Prompts
```
❌ ERRADO: Aplicar haptics antes de criar componentes
❌ ERRADO: Adicionar context menu antes de ter lista

✅ CERTO: Ordem sequencial
  1. Estrutura base
  2. Bottom Tab Bar
  3. Large Headers
  4. Context Menus (após ter listas)
  5. Bottom Sheets
  6. Date/Time Pickers
  7. Switches
  8. Haptics (por último)
```

**Solução:** Cole prompts na ordem indicada, aguardando cada um completar antes do próximo.

---

#### Causa 1.2: Prompt Genérico Demais
```
❌ ERRADO:
"Add a header to the app"

✅ CERTO:
"We want a large header title on the Workouts screen. Using a React Navigation Native Stack navigator, set `headerLargeTitle: true` and `headerTransparent: true` in screen options."
```

**Solução:** Use os prompts EXATOS fornecidos pela skill. VibeCode precisa de especificidade técnica (packages, props, métodos).

---

#### Causa 1.3: Componente Não Existe Ainda
```
❌ Tentou adicionar Context Menu em lista que não foi criada
❌ Tentou adicionar Date Picker em form que não existe
```

**Solução:** Sempre verificar se componente-alvo existe antes de aplicar features premium.

**Checklist:**
```
Antes de aplicar Large Header:
  [ ] Screen/navegação existe?

Antes de aplicar Context Menu:
  [ ] Lista/cards existem?

Antes de aplicar Bottom Sheet:
  [ ] Trigger (botão/ação) existe?

Antes de aplicar Date Picker:
  [ ] Form/input existe?
```

---

### Solução Geral: Debugging VibeCode

**Passo 1:** Verificar logs do VibeCode (se disponível)

**Passo 2:** Testar prompts isoladamente
```
1. Crie app mínimo
2. Aplique 1 prompt por vez
3. Teste imediatamente
4. Se funcionar → próximo prompt
5. Se não funcionar → reformular prompt
```

**Passo 3:** Consultar docs oficiais
```
https://vibecodeapp.com/docs/prompting/native-ui-components
```

**Passo 4:** Reformular prompt com mais contexto
```
Exemplo:
"Add large header to the WORKOUTS tab screen (first tab in bottom navigation). The header should show 'My Workouts' text and use the iOS native large title style that collapses on scroll."
```

---

## Problema 2: website-cloner Não Retorna Informações Úteis

### Sintomas
- Skill invocou website-cloner mas retornou design genérico
- Cores extraídas não batem com site original
- Componentes não foram identificados corretamente

### Causas Possíveis

#### Causa 2.1: Site com Proteção Anti-Scraping
```
Sites que BLOQUEIAM extração:
- Sites com Cloudflare aggressive mode
- Sites que requerem login para ver design
- Sites com conteúdo dinâmico (JS-heavy)
```

**Solução:** Usar método alternativo.

```
Se website-cloner falhar:
  ↓
Perguntar ao usuário:
  "Site tem proteção. Prefere usar método alternativo?"
  1. Screenshot (você tira prints e envia)
  2. Link App Store (se app já existe)
  3. Vídeo YouTube (demo do site/app)
```

---

#### Causa 2.2: Site com Design Inconsistente
```
Problema: Site usa 15 tons de azul diferentes
Resultado: website-cloner retorna palette confusa
```

**Solução:** Simplificar manualmente.

```python
# Pegar cores DOMINANTES apenas
cores_extraídas = ['#0066CC', '#0070D9', '#0073E6', '#0075F0', ...]
cores_simplificadas = ['#007AFF']  # iOS blue padrão

# Usar palette iOS nativa quando site for "bagunçado"
iOS_palette = {
  'blue': '#007AFF',
  'green': '#34C759',
  'red': '#FF3B30',
  'orange': '#FF9500',
  'purple': '#AF52DE'
}
```

---

#### Causa 2.3: Site É Landing Page Marketing (Não App)
```
Problema: https://exemplo.com é só página de vendas
Resultado: website-cloner retorna design de hero section, CTAs, etc
          (não serve para estrutura de APP)
```

**Solução:** Focar apenas em componentes relevantes.

```
Ignorar:
❌ Hero sections
❌ Footers gigantes
❌ Formulários de newsletter
❌ Pricing tables

Extrair apenas:
✅ Color palette
✅ Typography
✅ Button styles
✅ Card designs (se houver)
✅ Navigation (se houver)
```

---

### Solução Geral: Quando website-cloner Falha

**Fallback Strategy:**

```
1. Tentar website-cloner (método 4)
   ↓
   [FALHOU ou resultado ruim]
   ↓
2. Pedir screenshot do usuário (método 1)
   "Por favor, tire screenshots das telas principais
    do app/site e envie aqui"
   ↓
3. Analisar manualmente as imagens
   ↓
4. Gerar prompts VibeCode com design adaptado
```

**Comunicar ao usuário:**
```
⚠️ website-cloner teve dificuldade com este site.
Pode enviar screenshots? Assim consigo extrair o design com precisão.

Ou prefere que eu crie design original inspirado em iOS nativo?
```

---

## Problema 3: Backend e Frontend Desconectados

### Sintomas
- Frontend (VibeCode) pronto
- Backend (construído aqui) pronto
- Mas não conseguem se comunicar

### Causas Possíveis

#### Causa 3.1: CORS Não Configurado

```python
# Backend (FastAPI) sem CORS
app = FastAPI()

# ❌ Frontend não consegue fazer requests
```

**Solução:**

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção: especificar domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

#### Causa 3.2: URL do Backend Hardcoded

```javascript
// ❌ ERRADO no VibeCode
const API_URL = "http://localhost:8000"
// Só funciona em desenvolvimento local
```

**Solução:**

```javascript
// ✅ CERTO: Usar variáveis de ambiente
const API_URL = __DEV__
  ? "http://localhost:8000"  // Desenvolvimento
  : "https://api.seuapp.com"  // Produção

// Dizer ao usuário no plano:
"Configure API_URL no VibeCode:
 - Dev: http://localhost:8000
 - Prod: [URL_DEPLOY_BACKEND]"
```

---

#### Causa 3.3: Formato de Dados Incompatível

```javascript
// Frontend envia:
{ "workout_name": "Treino A" }

// Backend espera:
{ "name": "Treino A" }

// ❌ 422 Unprocessable Entity
```

**Solução:** Documentar contrato de API claramente.

```markdown
## Contrato de API (incluir no plano)

### POST /workouts

**Request Body:**
```json
{
  "name": "string",      // Nome do treino
  "date": "2025-11-04",  // Formato ISO
  "duration": 60         // Minutos (integer)
}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "string",
  "date": "2025-11-04",
  "duration": 60,
  "created_at": "2025-11-04T10:30:00Z"
}
```
```

**Dizer ao usuário:**
```
⚠️ IMPORTANTE: Use estes campos EXATAMENTE como especificado.
Frontend (VibeCode) e Backend precisam estar alinhados.
```

---

## Problema 4: Haptics Não Funcionam

### Sintomas
- Usuário configurou haptics no VibeCode
- App não vibra no iPhone

### Causas Possíveis

#### Causa 4.1: Haptics Não Configurados (Usuário Pulou)

```
Problema: Usuário colou todos os prompts mas esqueceu haptics
Razão: Haptics NÃO são prompt, são configuração manual
```

**Solução:** Lembrar explicitamente.

```markdown
### ⚠️ AÇÃO MANUAL OBRIGATÓRIA: Haptics

Haptics NÃO são aplicados via prompt. Você precisa:

1. Abrir app no VibeCode
2. Clicar botão "Haptics" (interface)
3. Para cada ação abaixo, adicionar haptic:

   ✅ Criar item → "success"
   ✅ Deletar item → "heavy"
   ✅ Mudar tab → "light"
   [... lista completa]

❌ SEM este passo, app não terá vibrações!
```

---

#### Causa 4.2: Dispositivo/Simulador Sem Suporte

```
Problema: Testando em simulador iOS (Mac)
Resultado: Haptics não funcionam (simulador não vibra)
```

**Solução:**

```
⚠️ Haptics só funcionam em DISPOSITIVO FÍSICO (iPhone).

Para testar:
1. Abra VibeCode no seu iPhone
2. Execute o app
3. Interaja com ações que têm haptics

Simulador (Mac) não suporta haptics.
```

---

## Problema 5: Prompts Muito Longos/Complexos

### Sintomas
- VibeCode não responde ou retorna erro genérico
- Timeout ao processar prompt

### Causa
```
Prompt com 500+ linhas de especificação detalhada
VibeCode AI não consegue processar
```

### Solução: Dividir em Prompts Menores

```
❌ ERRADO:
"Create complete fitness app with 10 screens,
 all with large headers, context menus, bottom sheets,
 date pickers, switches, haptics, and [300 more lines]"

✅ CERTO:
Prompt 1: "Create basic fitness app with 3 tabs"
Prompt 2: "Add large header to workouts tab"
Prompt 3: "Add context menu to workout cards"
[... continuar sequencialmente]
```

**Regra geral:** Máximo 10-15 linhas por prompt.

---

## Problema 6: Design "Não Parece iOS Nativo"

### Sintomas
- App criado mas não tem "cara de iOS"
- Parece web app ou Android

### Causa
```
Prompt não especificou design iOS nativo
VibeCode usou componentes genéricos
```

### Solução: Sempre Especificar iOS Design

```
❌ ERRADO:
"Create a task app"

✅ CERTO:
"Create a task app with iOS native design:
 - White background (#FFFFFF)
 - SF Pro font
 - iOS blue accent (#007AFF)
 - Native iOS components (no custom styling)
 - Follow Apple Human Interface Guidelines"
```

**Adicionar em TODOS os prompts base:**
```
Use iOS native design: white background, SF Pro font,
blue accent (#007AFF), native iOS components.
```

---

## Quick Fixes (Soluções Rápidas)

### Fix 1: Large Header Não Aparece
```
Adicione ao prompt:
"Make sure to import from '@react-navigation/native-stack'
and set options on the Screen component, not Navigator"
```

### Fix 2: Context Menu Não Abre
```
Verifique:
- [ ] Componente é touchable? (precisa receber gestures)
- [ ] Zeego está instalado? (prompt menciona package)
```

### Fix 3: Bottom Sheet Não Desliza
```
Adicione ao prompt:
"Test that gestures work by enabling gesture handler
and setting up GestureHandlerRootView wrapper"
```

### Fix 4: Date Picker Com Texto Branco (Invisível)
```
SEMPRE adicionar ao prompt:
"Use black text color for white background apps"
```

### Fix 5: Tabs Não Aparecem
```
Prompt deve mencionar:
"Use @bottom-tabs/react-navigation package
(not @react-navigation/bottom-tabs)"
```

---

## Quando Escalar Para Usuário

Se após tentativas ainda não funcionar:

```
❌ Tentei 3 vezes com prompts diferentes
❌ Consultei REFERENCE.md
❌ Testei em ordem sequencial
❌ Simplifiquei prompt
❌ Ainda não funciona

✅ Comunicar ao usuário:
"Encontrei dificuldade com [componente X].
Pode tentar [solução Y] diretamente no VibeCode?
Ou prefere que eu sugira alternativa?"
```

**Nunca:** Ficar preso indefinidamente. Após 3 tentativas, envolver usuário.

---

## Recursos Adicionais

**Docs Oficiais VibeCode:**
https://vibecodeapp.com/docs

**Community/Support:**
- Discord VibeCode (se existir)
- GitHub Issues (se open source)

**Alternativas:**
- Se VibeCode não funcionar para caso específico, sugerir:
  - Lovable (web app)
  - Claude Code completo (React Native Expo aqui)

---

**Última atualização:** 2025-11-04
**Versão:** 1.0
