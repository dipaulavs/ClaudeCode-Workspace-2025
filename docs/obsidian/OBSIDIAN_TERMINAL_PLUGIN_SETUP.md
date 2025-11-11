# 🖥️ Obsidian Terminal Plugin → Claude Code
**Plugin:** Terminal | **Setup:** 5 minutos | **Vault:** Claude-code-ios

---

## ⚙️ 1. Configuração Básica

### 1.1 Abrir Settings do Plugin
```
Obsidian → Settings → Terminal → Configure
```

### 1.2 Definir Terminal Padrão
```
Terminal: /bin/zsh
Working Directory: /Users/felipemdepaula/Desktop/ClaudeCode-Workspace
```

---

## 🎯 2. Comandos Disponíveis

### Via Command Palette (Cmd+P)

**Comando 1: Abrir Terminal no Workspace**
```
Terminal: Open terminal
→ Abre terminal em ClaudeCode-Workspace
```

**Comando 2: Executar comando rápido**
```
Terminal: Run command
→ Digite comando e execute
```

**Comando 3: Executar script salvo**
```
Terminal: Execute saved command
→ Escolhe da lista de favoritos
```

---

## 📜 3. Scripts Claude Code

### 3.1 Enviar nota atual para Claude
Criar no Terminal:
```bash
# Copiar caminho da nota
note_path="{{vault}}/{{file}}"

# Enviar para workspace
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace
./SCRIPTS/obsidian/send_to_claude.sh "$note_path"
```

### 3.2 Processar nota com Python
```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace
python3 SCRIPTS/obsidian/process_note.py "{{vault}}/{{file}}"
```

### 3.3 Abrir VS Code no workspace
```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace
code .
```

### 3.4 Iniciar webhook listener
```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace
python3 SCRIPTS/obsidian/webhook_listener.py
```

---

## 🔥 4. Comandos Salvos (Favoritos)

Adicionar em **Settings → Terminal → Saved Commands**:

### 4.1 Abrir Claude Code
```json
{
  "name": "🤖 Open Claude Code Workspace",
  "command": "cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace && code .",
  "hotkey": "cmd+shift+c"
}
```

### 4.2 Enviar nota atual
```json
{
  "name": "📤 Send Current Note",
  "command": "cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace && ./SCRIPTS/obsidian/send_to_claude.sh \"$OBSIDIAN_CURRENT_FILE\"",
  "hotkey": "cmd+shift+s"
}
```

### 4.3 Processar nota
```json
{
  "name": "🐍 Process with Python",
  "command": "cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace && python3 SCRIPTS/obsidian/process_note.py \"$OBSIDIAN_CURRENT_FILE\"",
  "hotkey": "cmd+shift+p"
}
```

### 4.4 Iniciar webhook
```json
{
  "name": "🌐 Start Webhook Server",
  "command": "cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace && python3 SCRIPTS/obsidian/webhook_listener.py",
  "hotkey": "cmd+shift+w"
}
```

---

## 🚀 5. Uso Rápido

### Opção A: Via Command Palette
```
1. Cmd+P
2. "Terminal: Open terminal"
3. Digite comando
4. Enter
```

### Opção B: Via Favoritos
```
1. Cmd+P
2. "Terminal: Execute saved command"
3. Escolhe da lista
4. Enter
```

### Opção C: Via Hotkey (se configurado)
```
1. Cmd+Shift+C → Abre workspace
2. Cmd+Shift+S → Envia nota
3. Cmd+Shift+P → Processa nota
```

---

## 🔗 6. Variáveis de Ambiente

O plugin Terminal suporta estas variáveis:

| Variável | Valor |
|----------|-------|
| `$OBSIDIAN_VAULT` | `/Users/felipemdepaula/Documents/Obsidian/Claude-code-ios` |
| `$OBSIDIAN_CURRENT_FILE` | Caminho completo da nota atual |
| `$OBSIDIAN_FILE_NAME` | Nome do arquivo atual |

Usar nos comandos:
```bash
echo "Processando: $OBSIDIAN_CURRENT_FILE"
```

---

## ⚡ 7. Integração Completa

### Workflow: Obsidian → Claude Code

```
┌─────────────┐
│  Obsidian   │
│  (Terminal) │
└──────┬──────┘
       │ comando
       ↓
┌─────────────┐
│   Script    │
│ send_to_    │
│  claude.sh  │
└──────┬──────┘
       │ copia
       ↓
┌─────────────┐
│ Claude Code │
│  Workspace  │
│   (temp/)   │
└─────────────┘
```

### Exemplo prático:
```bash
# 1. No Obsidian, abrir nota "Ideia de projeto"
# 2. Cmd+P → Terminal: Execute saved command
# 3. Escolher: "📤 Send Current Note"
# 4. Nota copiada para ClaudeCode-Workspace/temp/obsidian/
# 5. Notificação no macOS confirma
```

---

## 🛠️ 8. Troubleshooting

**Erro: "command not found"**
```bash
# Verificar se script é executável
chmod +x /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/SCRIPTS/obsidian/*.sh
```

**Erro: "Permission denied"**
```bash
# Adicionar permissão total
chmod 755 /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/SCRIPTS/obsidian/*
```

**Terminal não abre no diretório correto**
```
Settings → Terminal → Working Directory
Definir: /Users/felipemdepaula/Desktop/ClaudeCode-Workspace
```

---

## 📌 Próximos Passos

1. Testar comandos básicos
2. Adicionar favoritos personalizados
3. Configurar hotkeys
4. Integrar com webhook (opcional)
