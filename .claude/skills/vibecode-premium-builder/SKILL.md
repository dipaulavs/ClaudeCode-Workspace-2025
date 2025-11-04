# 📱 VibeCode Premium Builder

## Quando Usar

Automaticamente quando usuário pedir:
- **Criar app iOS:** "Quero criar app de [ideia]" ou "Preciso de um app para [propósito]"
- **Replicar app existente:** "Quero clonar/replicar [app X]" ou "Crie algo parecido com [app Y]"

**IMPORTANTE:** Skill gera prompts VibeCode + plano de backend. Sempre aplica features premium iOS.

---

## Workflow Automático

### ⚠️ PASSO 0: Consultar Documentação Oficial (OBRIGATÓRIO)

**ANTES de gerar qualquer prompt, SEMPRE fazer:**

```
WebFetch(https://vibecodeapp.com/docs/prompting/native-ui-components)
↓
Extrair prompts EXATOS para:
  - Large Headers
  - Context Menus
  - Bottom Tab Bar
  - Bottom Sheets
  - Date/Time Pickers
  - Switches
↓
❌ NUNCA inventar prompts
✅ SEMPRE usar texto exato da documentação
✅ APENAS adaptar contexto (nome de tela, variáveis)
```

**Por quê:** Docs podem ter atualizações. Prompts precisos = funcionamento garantido.

---

### Detectar Cenário

```
Usuário menciona "criar app" ou "replicar app"?
├─ CRIAR NOVO → Cenário A
└─ REPLICAR → Cenário B (perguntar método)
```

### **Cenário A: Criar App do Zero**

1. **Consultar docs** (Passo 0 obrigatório - WebFetch)
2. **Analisar ideia** (propósito, features principais)
3. **Gerar prompts VibeCode sequenciais** (usando prompts EXATOS da doc):
   - Prompt 1: Estrutura base + tabs (se multi-tela) - [criar manualmente]
   - Prompt 2: Large Headers - [copiar EXATO da doc + adaptar nome da tela]
   - Prompt 3: Context Menus - [copiar EXATO da doc + adaptar itens do menu]
   - Prompt 4: Bottom Sheets - [copiar EXATO da doc + adaptar snap points]
   - Prompt 5: Date/Time Pickers - [copiar EXATO da doc + adaptar mode]
   - Prompt 6: Liquid Glass Switches - [copiar EXATO da doc]
   - Prompt 7: Haptics - [instruções manuais, não é prompt]
4. **Planejar backend:** API endpoints, DB schema, autenticação
5. **Apresentar plano completo** ao usuário

### **Cenário B: Replicar App Existente**

1. **Consultar docs** (Passo 0 obrigatório - WebFetch)
2. **Perguntar método de análise:**
   ```
   Qual método prefere para análise?
   1. 📸 Screenshot (arraste imagens aqui)
   2. 🔗 Link App Store
   3. 🎥 Vídeo YouTube (demo do app)
   4. 🌐 Site/Landing Page
   ```

3. **Processar conforme método:**
   - **Método 1 (Screenshot):** Analisar layout, cores, componentes
   - **Método 2 (App Store):** WebFetch screenshots oficiais
   - **Método 3 (YouTube):** Transcrever vídeo demo
   - **Método 4 (Site):** 🚨 **CHAMAR `website-cloner` skill**
     ```
     Skill("website-cloner") → Retorna style guide
     ↓
     Adaptar: Web design → iOS nativo
     ```

4. **Gerar prompts VibeCode** (usando prompts EXATOS da doc consultada) + adaptar design
5. **Planejar backend** (igual Cenário A)

---

## Features Premium (Sempre Incluir)

✅ **Large Headers** (animação scroll)
✅ **Context Menus** (long-press)
✅ **Bottom Tab Bar** (se multi-tela)
✅ **Bottom Sheets** (modals deslizantes)
✅ **Date/Time Pickers** (se datas/horários)
✅ **Liquid Glass Switches** (toggles nativos)
✅ **Haptics** (feedback tátil estratégico)

---

## Output Final

```
✅ Plano VibeCode Premium completo!

📱 FRONTEND (VibeCode):
  → Prompt 1: [estrutura base]
  → Prompt 2: [large headers]
  → Prompt 3: [context menus]
  → Prompt 4: [bottom sheets]
  → Prompt 5: [switches + haptics]

🔧 BACKEND (Claude Code):
  → Endpoints: [lista]
  → Database: [schema]
  → Auth: [método]

🎯 Próximos passos:
  1. Cole os prompts no VibeCode (順序!)
  2. Aguarde frontend ficar pronto
  3. Confirme para eu construir backend
```

---

## Docs Adicionais

- **Prompts detalhados + técnicas:** Ver [REFERENCE.md](REFERENCE.md)
- **Exemplos completos:** Ver [EXAMPLES.md](EXAMPLES.md)
- **Problemas comuns:** Ver [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Skill Type:** Model-invoked
**Integrações:** `website-cloner` (método 4)
**Docs VibeCode:** https://vibecodeapp.com/docs/prompting/native-ui-components
