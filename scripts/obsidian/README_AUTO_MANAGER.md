# 🤖 Obsidian Auto Manager - Solução Definitiva

Sistema automático que gerencia tarefas no Obsidian **100% transparente**.

## 🎯 O que faz

```
┌─────────────────────────────────────────────┐
│ 1. Criar arquivo em 📋 Tarefas              │
│    ↓                                        │
│    Adiciona automaticamente ao Kanban       │
│    (coluna "aberta")                        │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ 2. Mover tarefa no Kanban                   │
│    ↓                                        │
│    Atualiza status no frontmatter           │
│    ↓                                        │
│    Dashboard atualiza automaticamente       │
└─────────────────────────────────────────────┘
```

## 📦 Instalação

### 1. Instalar fswatch (ferramenta de monitoramento)
```bash
brew install fswatch
```

### 2. Iniciar Auto Manager
```bash
cd SCRIPTS/obsidian
./INICIAR_AUTO_MANAGER.sh
```

Pronto! O script roda em background.

## 🚀 Como usar

### Criar Nova Tarefa

**Opção 1: Pelo Obsidian**
1. Criar arquivo em `📋 Tarefas/`
2. **Auto Manager detecta** → Adiciona ao Kanban automaticamente
3. Aparece na coluna "aberta" ✅

**Opção 2: Pelo Claude**
1. Pedir: "Cria tarefa X"
2. Claude cria arquivo
3. **Auto Manager detecta** → Adiciona ao Kanban
4. Pronto! ✅

### Trabalhar na Tarefa

1. **Arrastar no Kanban:** `aberta` → `em_andamento`
2. **Auto Manager detecta** → Atualiza `status: em_andamento`
3. Dashboard reflete mudança ✅

### Concluir Tarefa

1. **Arrastar no Kanban:** `em_andamento` → `concluída`
2. **Auto Manager detecta** → Atualiza `status: concluída`
3. Aparece em "Tarefas Concluídas" no dashboard ✅

## 🎯 Workflow Completo

```
CRIAR TAREFA
     ↓
Criar arquivo .md em 📋 Tarefas/
     ↓
Auto Manager detecta (0.5s)
     ↓
Adiciona ao Kanban (coluna "aberta")
     ↓
Aparece no Dashboard "Tarefas Abertas"
────────────────────────────────────
MOVER NO KANBAN
     ↓
Arrastar tarefa entre colunas
     ↓
Auto Manager detecta mudança
     ↓
Atualiza frontmatter: status: [coluna]
     ↓
Dashboard atualiza automaticamente
```

## 🔧 Comandos

### Iniciar
```bash
cd SCRIPTS/obsidian
./INICIAR_AUTO_MANAGER.sh
```

### Parar
```bash
cd SCRIPTS/obsidian
./PARAR_AUTO_MANAGER.sh
```

### Ver logs (em tempo real)
```bash
tail -f /tmp/obsidian_auto_manager.log
```

### Verificar se está rodando
```bash
ps aux | grep obsidian_auto_manager
```

## 📊 Dashboard

As queries Dataview funcionam automaticamente:

```dataview
WHERE status = "aberta"      → Tarefas Abertas
WHERE status = "em_andamento" → Em Andamento
WHERE status = "concluída"   → Tarefas Concluídas
```

## 🐛 Troubleshooting

### fswatch não encontrado?
```bash
brew install fswatch
```

### Auto Manager não inicia?
```bash
# Verificar se fswatch está instalado
which fswatch

# Testar manualmente
cd SCRIPTS/obsidian
./obsidian_auto_manager.sh
```

### Tarefa não foi adicionada ao Kanban?
```bash
# Ver logs
tail -20 /tmp/obsidian_auto_manager.log

# Verificar se arquivo está em 📋 Tarefas/
ls -la ~/Documents/Obsidian/Claude-code-ios/📋\ Tarefas/
```

### Status não atualiza?
```bash
# Ver logs em tempo real
tail -f /tmp/obsidian_auto_manager.log

# Mover tarefa no Kanban → Ver log mostrar:
# "🔄 Kanban modificado, sincronizando status..."
```

## ⚡ Performance

- **Detecção:** Instantânea (fswatch)
- **Adiciona ao Kanban:** ~0.5s
- **Sincroniza status:** ~1s
- **Impacto no sistema:** Mínimo (fswatch é nativo)

## 🎉 Vantagens

✅ **100% Automático** - Zero fricção
✅ **Transparente** - Funciona em background
✅ **Rápido** - Resposta instantânea
✅ **Confiável** - fswatch é nativo do macOS
✅ **Simples** - Um comando para iniciar

## 📝 Arquivos

- `obsidian_auto_manager.sh` - Script principal
- `INICIAR_AUTO_MANAGER.sh` - Inicia em background
- `PARAR_AUTO_MANAGER.sh` - Para o processo
- `sync_kanban_status.py` - Sincroniza status (usado pelo manager)

## 💡 Dica

Adicione ao startup do Mac para rodar automaticamente:
1. System Settings → General → Login Items
2. Adicionar `INICIAR_AUTO_MANAGER.sh`

---

**Tudo pronto! Agora é só criar tarefas e arrastar no Kanban. ✨**
