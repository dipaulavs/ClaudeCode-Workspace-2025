# Obsidian Organizer - Referência Técnica

## 📂 Estrutura do Vault

```
Claude-code-ios/
├── START HERE.md              # Guia principal
├── 📊 Tarefas.md              # Dashboard de tarefas
├── 📝 Anotações.md            # Dashboard de anotações
├── 📺 Vídeos.md               # Dashboard de vídeos
│
├── 📋 Tarefas/
│   ├── 📊 Kanban.md           # Board visual
│   └── [arquivos de tarefas]
│
├── 💡 Anotações/
│   └── [arquivos de anotações]
│
├── 📺 Vídeos/
│   └── [arquivos de vídeos]
│
└── 🔧 Templates/
    ├── Tarefa.md
    ├── Anotação Rápida.md
    └── Vídeo YouTube.md
```

---

## 🛠️ Tools Necessários

### Write Tool
Usado para criar arquivos:
```python
file_path = "/Users/felipemdepaula/Library/Mobile Documents/iCloud~md~obsidian/Documents/Claude-code-ios/[pasta]/[arquivo].md"
```

### Bash Tool (Opcional)
Para obter data/hora atual:
```bash
date "+%d/%m/%Y %H:%M"
```

---

## 📋 Metadados (Frontmatter)

### Tarefa
```yaml
criada: DD/MM/YYYY HH:mm    # Obrigatório
status: aberta              # Valores: aberta, concluída
```

### Anotação
```yaml
criada: DD/MM/YYYY HH:mm    # Obrigatório
tags:
  - anotacao                # Obrigatório
```

### Vídeo
```yaml
assistido: DD/MM/YYYY HH:mm # Obrigatório
categoria: [valor]          # Obrigatório
link: [URL]                 # Recomendado
tags:
  - youtube                 # Obrigatório
```

---

## 🏷️ Categorias de Vídeos

**Valores aceitos:**
- `noticia` - Novidades e lançamentos
- `tutorial` - Como fazer algo
- `curso` - Cursos completos
- `aula` - Conteúdo educacional
- `review` - Análises e opiniões
- `documentario` - Documentários
- `palestra` - Talks e apresentações

**Regra:** Sempre em minúsculo, sem acentos.

---

## 🎨 Estilo Visual

### Callouts Colapsáveis (Obsidian)

**Sintaxe:**
```markdown
> [!note]- Título (clique para expandir)
> Conteúdo aqui
> Pode ter várias linhas
```

**Tipos:**
- `[!note]` - Azul (padrão para transcrições)
- `[!info]` - Azul claro
- `[!warning]` - Amarelo
- `[!tip]` - Verde

**Collapse:**
- `[!note]-` - Começa **fechado** (usado em transcrições)
- `[!note]+` - Começa **aberto**

---

## 📊 DataView Queries

Os dashboards usam DataView. Estrutura:

### Últimos N itens
```dataview
TABLE WITHOUT ID
  file.link as "Nome",
  criada as "Criada"
FROM "pasta"
SORT file.ctime DESC
LIMIT 5
```

### Filtro por categoria
```dataview
TABLE WITHOUT ID
  file.link as "Vídeo",
  assistido as "Assistido"
FROM "📺 Vídeos"
WHERE contains(categoria, "tutorial")
SORT file.ctime DESC
```

---

## 🔄 Kanban Board

### Estrutura
```markdown
---
kanban-plugin: board
tags:
  - kanban
  - tarefas
---

## 📥 A Fazer
- [ ] [[Nome da Tarefa]]

## 🔨 Em Andamento
- [ ]

## ✅ Concluído
- [ ]
```

### Adicionar tarefa ao Kanban
Formato: `- [ ] [[Nome do Arquivo]]`

---

## 🌍 Formato Data/Hora

**Padrão brasileiro:**
- Data: `DD/MM/YYYY`
- Hora: `HH:MM` (24h)
- Completo: `03/11/2025 13:45`

**Não usar:**
- ❌ `YYYY-MM-DD` (ISO)
- ❌ `MM/DD/YYYY` (americano)
- ❌ `12h format` (AM/PM)

---

## 🎯 Lógica de Decisão

### Detecção de Tipo

**Tarefa (📋):**
- Keywords: "preciso fazer", "tarefa", "lembrar de", "checklist"
- Estrutura: Lista de ações
- Status: Tem início e fim

**Anotação (💡):**
- Keywords: "vi isso", "ideia", "interessante", "salvar"
- Estrutura: Livre, sem padrão
- Permanente: Referência futura

**Vídeo (📺):**
- Keywords: "vídeo", "assisti", "YouTube", "tutorial"
- Sempre tem: URL do YouTube
- Categoria: Obrigatória

---

## 🚨 Validações Obrigatórias

### Tarefa
- ✅ Tem título
- ✅ Tem data/hora criada
- ✅ Status definido (aberta/concluída)

### Anotação
- ✅ Tem título
- ✅ Tem data/hora criada
- ✅ Tag `anotacao`

### Vídeo
- ✅ Tem título
- ✅ Tem data/hora assistido
- ✅ Tem categoria válida
- ✅ Tem link (recomendado)
- ✅ Transcrição em callout colapsável
- ✅ Tag `youtube`

---

## 📝 Nomenclatura de Arquivos

**Padrão:** Nome descritivo, sem data no nome

**Bom:**
- `Implementar sistema de login.md`
- `Ideia - App de produtividade.md`
- `Tutorial Claude Code.md`

**Evitar:**
- ❌ `2025-11-03 Tarefa.md` (data desnecessária)
- ❌ `tarefa1.md` (não descritivo)
- ❌ `TAREFA IMPORTANTE!!!.md` (excessivo)

---

## 🔧 Manutenção

### Limpeza
- Tarefas concluídas ficam no dashboard
- Usuário decide quando arquivar
- Não deletar automaticamente

### Organização
- Sempre nas pastas corretas
- Sempre com frontmatter completo
- Sempre com data/hora brasileira

---

## 🎓 Filosofia Minimalista

**Princípios:**
1. **Menos é mais** - Só o essencial
2. **Visual limpo** - Sem poluição
3. **Acesso rápido** - Últimos itens sempre visíveis
4. **Zero firula** - Direto ao ponto
5. **Formato brasileiro** - DD/MM/YYYY HH:MM

**Evitar:**
- Emojis excessivos (só os definidos)
- Cores desnecessárias
- Estruturas complexas
- Múltiplas tags redundantes
- Categorias demais

---

## 🔗 Links Relacionados

- [[SKILL.md]] - Instruções principais
- [[EXAMPLES.md]] - Casos de uso reais
- [[TROUBLESHOOTING.md]] - Problemas comuns
