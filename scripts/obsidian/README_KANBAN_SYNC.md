# 🔄 Sincronização Automática Kanban → Dashboard

Sistema automático que sincroniza status das tarefas entre Kanban e Dashboard.

## 📊 Como Funciona

```
Kanban (visual)              Frontmatter (dados)           Dashboard (exibição)
      ↓                              ↓                             ↓
┌─────────────┐              ┌──────────────┐              ┌─────────────────┐
│ 📥 A Fazer  │    sync →    │ status:      │    query →   │ Tarefas Abertas │
│             │              │ aberta       │              │                 │
└─────────────┘              └──────────────┘              └─────────────────┘

┌─────────────┐              ┌──────────────┐              ┌─────────────────┐
│ ✅ Concluído│    sync →    │ status:      │    query →   │ Tarefas         │
│             │              │ concluída    │              │ Concluídas      │
└─────────────┘              └──────────────┘              └─────────────────┘
```

## 🚀 Uso Rápido

### Opção 1: Manual (após mover tarefas)
```bash
cd SCRIPTS/obsidian
python3 sync_kanban_status.py
```

### Opção 2: Automático (monitoramento contínuo)
```bash
cd SCRIPTS/obsidian
./watch_kanban.sh
```

Deixe rodando em terminal separado. Sincroniza automaticamente ao detectar mudanças no Kanban.

## 📋 Workflow Completo

### Criar Nova Tarefa
1. Claude cria arquivo: `📋 Tarefas/Nome da Tarefa.md`
2. Adiciona frontmatter: `criada: DD/MM/YYYY HH:mm`, `status: aberta`
3. Adiciona ao Kanban: `- [ ] [[Nome da Tarefa]]` em "📥 A Fazer"
4. Executa sync: `python3 sync_kanban_status.py`
5. Aparece automaticamente em "Tarefas Abertas" no dashboard

### Concluir Tarefa
1. Usuário arrasta tarefa no Kanban: A Fazer → Concluído
2. Script sync detecta mudança
3. Atualiza frontmatter: `status: concluída`
4. Aparece automaticamente em "✅ Tarefas Concluídas" no dashboard

## 🔧 Mapeamento de Status

| Coluna Kanban      | Status Frontmatter   | Dashboard Section      |
|--------------------|---------------------|------------------------|
| 📥 A Fazer         | `status: aberta`    | Tarefas Abertas        |
| 🔨 Em Andamento    | `status: em_andamento` | (filtro futuro)     |
| ✅ Concluído       | `status: concluída` | Tarefas Concluídas     |

## 📂 Arquivos Envolvidos

- `sync_kanban_status.py` - Script de sincronização
- `watch_kanban.sh` - Monitor automático (requer fswatch)
- `📋 Tarefas/📊 Kanban.md` - Arquivo Kanban monitorado
- `📊 Tarefas.md` - Dashboard com queries Dataview

## 🎯 Queries Dataview

### Última Tarefa Criada
```dataview
TABLE WITHOUT ID
  ("**" + criada + "**") as "Data",
  file.link as "Tarefa"
FROM "📋 Tarefas"
WHERE file.name != "📊 Kanban"
SORT file.ctime DESC
LIMIT 1
```

### Tarefas Abertas
```dataview
TABLE WITHOUT ID
  file.link as "Tarefa",
  criada as "Criada",
  status as "Status"
FROM "📋 Tarefas"
WHERE status = "aberta" AND file.name != "📊 Kanban"
SORT file.ctime DESC
```

### Tarefas Concluídas
```dataview
TABLE WITHOUT ID
  file.link as "Tarefa",
  criada as "Criada"
FROM "📋 Tarefas"
WHERE status = "concluída" AND file.name != "📊 Kanban"
SORT file.ctime DESC
```

## ⚙️ Instalação fswatch (Opcional)

Para monitoramento automático:
```bash
brew install fswatch
```

## 🐛 Troubleshooting

**Tarefas não aparecem no dashboard?**
1. Verificar frontmatter tem `status:` e `criada:`
2. Executar `python3 sync_kanban_status.py`
3. Atualizar Obsidian (Cmd+R)

**Dashboard vazio?**
1. Verificar plugin Dataview está ativo
2. Verificar arquivos estão em `📋 Tarefas/`
3. Verificar frontmatter está correto

**Sync não funciona?**
1. Verificar arquivo Kanban existe: `📋 Tarefas/📊 Kanban.md`
2. Verificar links no Kanban correspondem aos nomes dos arquivos
3. Executar script manualmente para ver erros

## 🎉 Resultado Final

✅ Mover tarefa no Kanban → Aparece automaticamente no dashboard
✅ Dados sempre sincronizados
✅ Zero fricção para o usuário
