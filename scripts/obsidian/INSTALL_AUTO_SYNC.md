# 🚀 Instalação: Sincronização 100% Automática

Plugin customizado que sincroniza tarefas entre Kanban e Dashboard automaticamente.

## 📦 O que foi criado

```
.obsidian/plugins/kanban-auto-sync/
├── manifest.json    → Metadados do plugin
├── main.js          → Código (escuta mudanças no Kanban)
└── README.md        → Documentação
```

## ✅ Como ativar

### 1️⃣ Abrir Settings no Obsidian
```
Cmd + , (ou clique engrenagem ⚙️)
```

### 2️⃣ Ir em Community Plugins
```
Settings → Community plugins
```

### 3️⃣ Desabilitar Safe Mode (se necessário)
```
Se "Safe mode" estiver ON → Desligar
```

### 4️⃣ Ativar o Plugin
```
Procurar "Kanban Auto Sync" na lista
Toggle ON ✅
```

### 5️⃣ Verificar se funcionou
```
1. Cmd + Option + I (abre Console)
2. Procurar: "Loading Kanban Auto Sync plugin"
3. Fechar console
```

## 🧪 Testar

### Teste rápido:
1. Abrir Kanban: `📋 Tarefas/📊 Kanban`
2. Mover qualquer tarefa para "✅ Concluído"
3. **Aguardar 1-2 segundos**
4. Ver notificação: "✅ Tarefas sincronizadas!"
5. Abrir Dashboard: `📊 Tarefas.md`
6. Tarefa aparece em "Tarefas Concluídas" ✅

## 🎯 Como funciona agora

```
ANTES (manual)
┌────────────────────────────────────────┐
│ Move no Kanban                         │
│      ↓                                 │
│ Rodar script manualmente               │
│      ↓                                 │
│ Aparece no Dashboard                   │
└────────────────────────────────────────┘

AGORA (automático)
┌────────────────────────────────────────┐
│ Move no Kanban                         │
│      ↓ (plugin detecta)                │
│ Script executa automaticamente         │
│      ↓                                 │
│ Aparece no Dashboard INSTANTÂNEO ✅    │
└────────────────────────────────────────┘
```

## 🔍 Verificar logs (opcional)

Se quiser ver o que está acontecendo:

1. **Abrir Console:** `Cmd + Option + I`
2. **Mover tarefa no Kanban**
3. **Ver logs:**
   - `Kanban modified, syncing status...`
   - `Sync output: 🔄 Sincronizando...`
   - `✅ X tarefas atualizadas!`

## ❗ Troubleshooting

### Plugin não aparece na lista?
**Solução:**
1. Verificar pasta existe: `.obsidian/plugins/kanban-auto-sync/`
2. Verificar arquivos: `manifest.json`, `main.js`, `README.md`
3. Reiniciar Obsidian (Cmd+R)

### Sync não funciona?
**Solução:**
1. Abrir Console (Cmd+Option+I)
2. Procurar erros em vermelho
3. Testar script manualmente:
   ```bash
   cd ClaudeCode-Workspace
   python3 SCRIPTS/obsidian/sync_kanban_status.py
   ```

### Notificação não aparece?
**Solução:**
- Sync pode estar funcionando mas notificação falhou
- Verificar Dashboard manualmente (tarefa deve estar lá)
- Verificar Console para confirmar sync executou

## 🎉 Pronto!

Agora toda vez que você mover uma tarefa no Kanban, ela atualiza automaticamente no Dashboard!

**Zero fricção. 100% automático. ✅**

---

**Documentação completa:** `.obsidian/plugins/kanban-auto-sync/README.md`
