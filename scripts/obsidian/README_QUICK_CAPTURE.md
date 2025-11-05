# 🎤 Sistema de Captura Rápida → Obsidian

Captura ideias bagunçadas (texto/voz) → identifica automaticamente → formata visual → organiza no Obsidian

---

## 🎯 Fluxo Completo

```
┌─────────────────┐
│  IDEIA SOLTA    │
│  (texto/voz)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  IDENTIFICAR    │ → Tarefa? Ideia? Projeto? Nota?
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FORMATAR       │ → Visual ASCII (boxes/fluxos)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  OBSIDIAN ✅    │
│  (estruturado)  │
└─────────────────┘
```

---

## 🚀 Como Usar

### 1️⃣ Captura por Texto (direto com Claude)

**Simplesmente fale:**
```
"Anota isso: preciso ligar pro cliente amanhã"
```

**Claude auto-invoca `obsidian-quick-capture` e:**
1. ✅ Identifica tipo (Tarefa)
2. ✅ Formata visual
3. ✅ Salva em `📋 TAREFAS/`

---

### 2️⃣ Captura por Voz (script)

**Grave áudio e processe:**
```bash
# Com arquivo de áudio
python3 scripts/obsidian/quick_capture_voice.py \
    --audio ~/nota_voz.mp3

# Ou texto direto
python3 scripts/obsidian/quick_capture_voice.py \
    --text "minha ideia maluca"
```

**Resultado:**
```
🎤 Transcrevendo áudio...
✅ Transcrição: minha ideia maluca...
🧠 Identificando tipo...
✅ Tipo: IDEIA
💾 Salvando em: 💡 IDEIAS/20251105_103045.md

✅ Capturado com sucesso!
📂 Local: 💡 IDEIAS/20251105_103045.md
🔷 Tipo: Ideia
```

---

## 📁 Estrutura Obsidian

**Antes de usar, crie essa estrutura no seu vault:**

```
Obsidian/
├── 📥 INBOX/              → Entrada temporária
├── 📋 TAREFAS/            → Ações/lembretes
│   ├── urgente/
│   ├── hoje/
│   └── semana/
├── 💡 IDEIAS/             → Insights/conceitos
│   ├── validadas/
│   └── explorando/
├── 📂 PROJETOS/           → Complexos/multi-etapas
│   ├── em-andamento/
│   └── backlog/
└── 📝 NOTAS/              → Referências/estudos
    ├── tecnico/
    ├── pessoal/
    └── trabalho/
```

**Setup rápido:**
```bash
cd ~/Obsidian/SeuVault/

mkdir -p "📥 INBOX"
mkdir -p "📋 TAREFAS/urgente" "📋 TAREFAS/hoje" "📋 TAREFAS/semana"
mkdir -p "💡 IDEIAS/validadas" "💡 IDEIAS/explorando"
mkdir -p "📂 PROJETOS/em-andamento" "📂 PROJETOS/backlog"
mkdir -p "📝 NOTAS/tecnico" "📝 NOTAS/pessoal" "📝 NOTAS/trabalho"
```

---

## 🧠 Como Funciona a Identificação

| Tipo | Gatilhos | Exemplo |
|------|----------|---------|
| **📋 Tarefa** | fazer, criar, lembrar, urgente | "preciso ligar pro cliente" |
| **💡 Ideia** | e se, poderia, seria legal | "e se criássemos um sistema..." |
| **📂 Projeto** | sistema, plataforma, desenvolver | "desenvolver chatbot completo" |
| **📝 Nota** | aprendi, descobri, http:// | "descobri que RAG usa embeddings" |

---

## 📐 Formato Visual Padrão

**Toda nota capturada fica assim:**

```markdown
# 🔷 Título Limpo

**Tipo:** Tarefa
**Capturado:** 2025-11-05 10:30 BR 🎤
**Status:** Pendente
**Prioridade:** Alta ⚠️

---

## 🎯 Resumo Visual

┌─────────────┐
│   AÇÃO      │
│   PRINCIPAL │
└──────┬──────┘
       │
   Sub-ações

---

## 📝 Detalhes

[Contexto original preservado]

---

## ✅ Próximos Passos

- [ ] Ação 1
- [ ] Ação 2
```

---

## 🔧 Configuração

### Requisitos

```bash
# Instalar dependências
pip install openai-whisper pytz

# Obsidian Plugin (obrigatório)
Settings → Community Plugins → Browse
→ Instalar "Local REST API"
→ Enable
```

### Verificar conexão

```python
from scripts.obsidian.obsidian_client import ObsidianClient

client = ObsidianClient()
print(client.active_vault())  # Deve retornar nome do vault
```

---

## 📚 Documentação Completa

- **Skill:** `.claude/skills/obsidian-quick-capture/SKILL.md`
- **Referência:** `.claude/skills/obsidian-quick-capture/REFERENCE.md`
- **Exemplos:** `.claude/skills/obsidian-quick-capture/EXAMPLES.md`
- **Troubleshooting:** `.claude/skills/obsidian-quick-capture/TROUBLESHOOTING.md`

---

## 🎯 Exemplos Rápidos

### Exemplo 1: Tarefa Urgente

**Input:**
```
"preciso lembrar de enviar orçamento pro cliente amanhã urgente"
```

**Output:**
```markdown
# 📋 Enviar Orçamento para Cliente

**Tipo:** Tarefa
**Capturado:** 2025-11-05 10:30 BR ⌨️
**Status:** Pendente
**Prioridade:** Alta ⚠️
**Deadline:** Amanhã

---

## 🎯 Resumo Visual

┌──────────────────┐
│ ENVIAR ORÇAMENTO │
└────────┬─────────┘
         │
    Cliente + Amanhã

---

## ✅ Checklist

- [ ] Preparar orçamento atualizado
- [ ] Revisar valores
- [ ] Enviar por email
```

**Local:** `📋 TAREFAS/20251105_103045.md`

---

### Exemplo 2: Ideia Criativa

**Input (voz):**
```
"e se a gente criasse um gerador automático de thumbnails"
```

**Output:**
```markdown
# 💡 Gerador Automático de Thumbnails

**Tipo:** Ideia
**Capturado:** 2025-11-05 10:31 BR 🎤
**Status:** Pendente
**Potencial:** Médio

---

## 🎯 Resumo Visual

    GERADOR THUMBNAILS
           │
    ┌──────┴──────┐
    │             │
Automação     Templates
              + Batch

---

## 🚀 Próximos Passos

- [ ] Validar viabilidade
- [ ] Pesquisar APIs (Canva?)
- [ ] Prototipar MVP
```

**Local:** `💡 IDEIAS/20251105_103100.md`

---

## ⚡ Atalho Recomendado

**Para máxima velocidade, crie alias no shell:**

```bash
# Adicione ao ~/.zshrc ou ~/.bashrc
alias qc='python3 ~/Desktop/ClaudeCode-Workspace/scripts/obsidian/quick_capture_voice.py'

# Uso:
qc --text "minha ideia"
qc --audio ~/nota.mp3
```

---

## 🔄 Workflow Ideal

```
1. Teve ideia? → Fale com Claude OU grave áudio
2. Sistema processa automaticamente
3. Abra Obsidian → Ideia organizada visualmente
4. Refine se necessário
5. Execute! ✅
```

---

## 🆘 Problemas?

Ver: `.claude/skills/obsidian-quick-capture/TROUBLESHOOTING.md`

**Mais comuns:**
- Plugin Local REST API desativado
- Estrutura de pastas não criada
- Encoding UTF-8 incorreto

---

**v1.0** | **2025-11-05** | **Integração completa** ✅
