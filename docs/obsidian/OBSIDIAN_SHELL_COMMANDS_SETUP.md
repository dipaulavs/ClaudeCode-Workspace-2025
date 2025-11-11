# 🔌 Obsidian Shell Commands → Claude Code
**Setup rápido:** 10 minutos | **Vault:** Claude-code-ios

---

## 📦 1. Instalar Plugin

1. Abrir Obsidian → Settings (⚙️)
2. Community Plugins → Browse
3. Buscar: **"Shell commands"**
4. Instalar + Enable

**Alternativa manual:**
```bash
cd ~/Documents/Obsidian/Claude-code-ios/.obsidian/plugins
git clone https://github.com/Taitava/obsidian-shellcommands.git shell-commands
cd shell-commands && npm install && npm run build
```

---

## ⚙️ 2. Configurar Comandos

### 2.1 Settings → Shell commands → New shell command

**Comando 1: Enviar nota para Claude Code**
```bash
# Nome: 📤 Send to Claude Code
# Shell command:
/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/SCRIPTS/obsidian/send_to_claude.sh "{{file_path:absolute}}"

# Atalho sugerido: Cmd+Shift+C
# Working directory: /Users/felipemdepaula/Desktop/ClaudeCode-Workspace
```

**Comando 2: Executar script Python com conteúdo da nota**
```bash
# Nome: 🐍 Run Python with note
# Shell command:
python3 /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/SCRIPTS/obsidian/process_note.py "{{file_path:absolute}}"

# Atalho sugerido: Cmd+Shift+P
```

**Comando 3: Criar tarefa rápida no terminal**
```bash
# Nome: ✅ Quick Task
# Shell command:
echo "{{selection}}" >> /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/QUICK_TASKS.txt && echo "✅ Task added!"

# Atalho sugerido: Cmd+Shift+T
```

**Comando 4: Enviar para webhook Claude Code (remoto)**
```bash
# Nome: 🌐 Send to Claude Remote
# Shell command:
curl -X POST http://localhost:8000/obsidian/process \
  -H "Content-Type: application/json" \
  -d "{\"file\":\"{{file_path:absolute}}\",\"content\":\"{{file_content:absolute}}\"}"

# Atalho sugerido: Cmd+Shift+R
```

---

## 🛠️ 3. Variáveis Disponíveis

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `{{file_path:absolute}}` | Caminho completo | `/Users/.../nota.md` |
| `{{file_path:relative}}` | Caminho relativo ao vault | `00 - Inbox/nota.md` |
| `{{file_name}}` | Nome do arquivo | `nota.md` |
| `{{file_content:absolute}}` | Conteúdo do arquivo | Texto completo |
| `{{selection}}` | Texto selecionado | Texto marcado |
| `{{vault_path}}` | Caminho do vault | `/Users/.../Claude-code-ios` |

---

## 📜 4. Scripts Criados

### `send_to_claude.sh`
Envia nota para Claude Code processar via MCP

### `process_note.py`
Processa nota com Python e retorna resultado

### `webhook_listener.py`
Servidor local que recebe comandos do Obsidian

---

## 🚀 5. Uso

1. **No Obsidian:**
   - Abrir nota
   - Cmd+P → "Shell commands"
   - Escolher comando
   - OU usar atalho direto

2. **Resultado:**
   - Executa script
   - Mostra notificação no Obsidian
   - Processa no Claude Code

---

## 🔗 6. Integração com MCP

**Webhook local** (opcional para comandos remotos):
```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/SCRIPTS/obsidian
python3 webhook_listener.py
```

**URL:** http://localhost:8000
**Endpoints:**
- `POST /obsidian/process` - Processar nota
- `POST /obsidian/task` - Criar tarefa
- `GET /status` - Status do servidor

---

## ⚡ Exemplos de Uso

**1. Enviar nota para processar:**
```
Obsidian → Select note → Cmd+Shift+C → Claude Code recebe
```

**2. Executar Python com seleção:**
```
Obsidian → Select text → Cmd+Shift+P → Script processa
```

**3. Criar tarefa rápida:**
```
Obsidian → Select text → Cmd+Shift+T → Adiciona a QUICK_TASKS.txt
```

---

## 🎯 Próximos Passos

Agora vou criar os scripts bash/Python de integração.
