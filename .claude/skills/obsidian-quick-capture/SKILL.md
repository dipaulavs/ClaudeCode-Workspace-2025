# obsidian-quick-capture

**Captura rápida de ideias → identificação automática → organização visual no Obsidian**

## 🎯 Quando Usar

AUTO-INVOCA quando:
- "Anota isso rapidamente"
- "Tenho uma ideia"
- "Captura isso"
- "Organiza essa nota bagunçada"
- Usuário mencionar nota desorganizada/bagunçada

## ⚡ Fluxo Automático

```
ENTRADA (bagunçada)
       │
       ▼
┌──────────────┐
│ IDENTIFICAR  │ → Tarefa? Ideia? Projeto? Nota?
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ FORMATAR     │ → Visual ASCII (boxes/fluxos)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ ORGANIZAR    │ → Local correto no Obsidian
└──────────────┘
```

## 🧠 Identificação de Tipo

| Tipo | Características | Destino |
|------|----------------|---------|
| **Tarefa** | Ação/fazer/lembrar/deadline | `📋 TAREFAS/` |
| **Ideia** | Conceito/possibilidade/insight | `💡 IDEIAS/` |
| **Projeto** | Múltiplas etapas/complexo | `📂 PROJETOS/` |
| **Nota** | Referência/estudo/conhecimento | `📝 NOTAS/` |

## 📐 Template Visual Padrão

**Obrigatório em TODA nota processada:**

```
# 🔷 [TÍTULO LIMPO]

**Tipo:** [Tarefa|Ideia|Projeto|Nota]
**Capturado:** [Data/Hora BR]
**Status:** [Pendente|Em Andamento|Concluído]

---

## 🎯 Resumo Visual

[Diagrama ASCII boxes/fluxo]

---

## 📝 Detalhes

[Conteúdo organizado]

---

## ✅ Próximos Passos

- [ ] Ação 1
- [ ] Ação 2
```

## ⚙️ Integração com MCP Filesystem

```python
from tools import Read, Write

VAULT_PATH = "/Users/felipemdepaula/Library/Mobile Documents/iCloud~md~obsidian/Documents/Claude-code-ios"

# Criar nota
Write(
    file_path=f"{VAULT_PATH}/📋 TAREFAS/titulo.md",
    content=conteudo_formatado
)

# Ler nota existente
content = Read(file_path=f"{VAULT_PATH}/📋 TAREFAS/titulo.md")
```

**Ver detalhes técnicos:** `REFERENCE.md`
**Ver exemplos reais:** `EXAMPLES.md`
**Troubleshooting:** `TROUBLESHOOTING.md`
