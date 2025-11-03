# Obsidian Organizer Skill

**Ativa quando:** Usuário pede para anotar, salvar, organizar ou registrar algo no Obsidian.

**O que faz:** Entende o sistema minimalista de organização do usuário e cria conteúdo automaticamente no formato e local corretos.

---

## 🎯 Sistema do Usuário (Minimalista)

O usuário tem 3 categorias principais:

### 📋 Tarefas
- **Quando:** Coisas a fazer, checklist, ações
- **Formato:** Template com status, data/hora BR, detalhes opcionais
- **Local:** `📋 Tarefas/`
- **Kanban:** Pode ser adicionada ao board visual

### 💡 Anotações
- **Quando:** Ideias rápidas, rascunhos, pensamentos, links interessantes
- **Formato:** Livre, sem estrutura obrigatória, data/hora BR
- **Local:** `💡 Anotações/`
- **Estilo:** Ultra-rápido, zero firula

### 📺 Vídeos YouTube
- **Quando:** Vídeo assistido que ensinou algo
- **Formato:** Link, categoria, resumo, aprendizados, transcrição (oculta)
- **Local:** `📺 Vídeos/`
- **Categoria obrigatória:** notícia, tutorial, curso, aula, review, etc

---

## 🤖 Como Decidir

**Fluxo de decisão:**

```
Usuário pediu para anotar/salvar algo?
├─ É tarefa/ação? → Criar em 📋 Tarefas/
├─ É vídeo YouTube? → Criar em 📺 Vídeos/
└─ É ideia/rascunho? → Criar em 💡 Anotações/
```

**Indicadores:**
- **Tarefa:** "preciso fazer", "tenho que", "tarefa", checklist
- **Vídeo:** URL YouTube, "assisti vídeo", "vi um tutorial"
- **Anotação:** "ideia rápida", "vi isso", "quero lembrar", link qualquer

---

## 📝 Templates

### Tarefa
```yaml
---
criada: DD/MM/YYYY HH:mm
status: aberta
---

# Título

## 📝 Detalhes
[Opcional]

## ✅ Checklist
- [ ] Item
```

### Anotação Rápida
```yaml
---
criada: DD/MM/YYYY HH:mm
tags:
  - anotacao
---

# Título

[Conteúdo livre]
```

### Vídeo YouTube
```yaml
---
assistido: DD/MM/YYYY HH:mm
categoria: [OBRIGATÓRIO]
link: [URL]
tags:
  - youtube
---

# Título

## 🎬 Informações
**Link:** URL
**Categoria:** categoria
**Assistido em:** DD/MM/YYYY HH:mm

## 📝 Resumo
[Resumo breve]

## 💡 Principais Aprendizados
- Item 1

> [!note]- 📄 Transcrição Completa (clique para expandir)
> [Transcrição se tiver]
```

---

## ⚡ Regras de Ouro

1. **Minimalista sempre** - Sem poluição visual
2. **Data/hora brasileira** - DD/MM/YYYY HH:mm
3. **Categorias obrigatórias** - Vídeos precisam de categoria
4. **Transcrição oculta** - Usar callout colapsável `> [!note]-`
5. **Último primeiro** - Mais recente sempre no topo
6. **Ação direta** - Criar e confirmar, sem perguntar muito

---

## 🚀 Execução

**Quando usuário pedir:**
1. Identificar tipo (tarefa/anotação/vídeo)
2. Criar arquivo no local correto
3. Aplicar template apropriado
4. Usar data/hora atual (formato BR)
5. Preencher com informações fornecidas
6. Confirmar criação

**Comunicação:**
- Concisa e direta
- Mostrar o que foi criado
- Indicar onde está salvo

---

**Vault path:** `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Claude-code-ios/`

Para detalhes técnicos → [[REFERENCE.md]]
Para exemplos práticos → [[EXAMPLES.md]]
