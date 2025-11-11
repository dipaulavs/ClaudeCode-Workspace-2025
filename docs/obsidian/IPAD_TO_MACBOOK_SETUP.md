# 📱 iPad Obsidian → 💻 MacBook Claude Code
**Setup:** 5 minutos | **Rede:** Wi-Fi local | **IP MacBook:** 192.168.18.11

---

## 🎯 Fluxo

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│  iPad       │  HTTP   │  MacBook    │  File   │ Claude Code │
│  Obsidian   │ ──────> │  Webhook    │ ──────> │  Workspace  │
│  Terminal   │         │  :8000      │         │             │
└─────────────┘         └─────────────┘         └─────────────┘
```

---

## 🚀 PASSO 1: Iniciar Servidor no MacBook

### No Terminal do MacBook:
```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace
./SCRIPTS/obsidian/start_webhook_server.sh
```

**Deve aparecer:**
```
🌐 Iniciando webhook server...
📡 IP Local: 192.168.18.11
🔗 URL: http://192.168.18.11:8000

📱 No iPad, usar:
   http://192.168.18.11:8000/obsidian/process
   http://192.168.18.11:8000/obsidian/task

🛑 Para parar: Ctrl+C
```

**Deixar rodando!** (não fechar terminal)

---

## 📱 PASSO 2: Configurar Obsidian no iPad

### Opção A: Plugin Terminal

**No Obsidian iPad:**
1. Abrir nota que quer enviar
2. Abrir Terminal (Cmd+P → Terminal)
3. Executar:

```bash
# Enviar nota atual
curl -X POST http://192.168.18.11:8000/obsidian/process \
  -H "Content-Type: application/json" \
  -d "{\"file\":\"nota.md\",\"content\":\"$(cat nota.md)\"}"
```

### Opção B: Criar comandos salvos

**Settings → Terminal → Saved Commands:**

**Comando 1: Enviar para Claude Code**
```bash
curl -X POST http://192.168.18.11:8000/obsidian/process \
  -H "Content-Type: application/json" \
  -d "{\"file\":\"$OBSIDIAN_FILE_NAME\",\"content\":\"$(cat $OBSIDIAN_CURRENT_FILE)\"}"
```

**Comando 2: Criar tarefa rápida**
```bash
curl -X POST http://192.168.18.11:8000/obsidian/task \
  -H "Content-Type: application/json" \
  -d "{\"task\":\"Nova tarefa do iPad\"}"
```

**Comando 3: Verificar status**
```bash
curl http://192.168.18.11:8000/status
```

---

## ⚡ PASSO 3: Usar

### No iPad:

**Via Terminal Plugin:**
```
1. Cmd+P
2. "Terminal: Execute saved command"
3. Escolher "Enviar para Claude Code"
4. ✅ Nota enviada!
```

**Via comando direto:**
```bash
# Testar conexão
curl http://192.168.18.11:8000/status

# Enviar tarefa
curl -X POST http://192.168.18.11:8000/obsidian/task \
  -H "Content-Type: application/json" \
  -d '{"task":"Implementar feature X"}'
```

---

## 📂 PASSO 4: Ver resultado no MacBook

**Arquivos salvos em:**
```
ClaudeCode-Workspace/temp/obsidian/
```

**Tarefas salvas em:**
```
ClaudeCode-Workspace/QUICK_TASKS.txt
```

**Ver em tempo real:**
```bash
# No MacBook
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace
ls -la temp/obsidian/          # Ver notas recebidas
tail -f QUICK_TASKS.txt        # Monitorar tarefas
```

---

## 🔧 Comandos Úteis

### No iPad (testar conexão):
```bash
# Ping simples
curl http://192.168.18.11:8000/status

# Deve retornar:
# {"status":"online","timestamp":"...","workspace":"..."}
```

### No MacBook (verificar logs):
```bash
# Terminal onde o servidor está rodando mostra:
✅ Nota processada: exemplo.md
✅ Tarefa adicionada: Nova tarefa
```

---

## 🛠️ Troubleshooting

**Erro: "Connection refused"**
- Verificar se servidor está rodando no MacBook
- Verificar firewall: System Preferences → Security → Firewall
- Permitir conexões Python

**Erro: "Network unreachable"**
- iPad e MacBook na mesma rede Wi-Fi?
- Testar ping: `ping 192.168.18.11`

**IP mudou?**
```bash
# No MacBook, descobrir novo IP:
ipconfig getifaddr en0

# Atualizar comandos no iPad com novo IP
```

**Permitir conexões (se necessário):**
```bash
# No MacBook
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/bin/python3
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblockapp /usr/bin/python3
```

---

## 🚀 Servidor Automático (Opcional)

**Iniciar sempre que ligar MacBook:**

```bash
# Criar serviço LaunchAgent
cat > ~/Library/LaunchAgents/com.claudecode.webhook.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.claudecode.webhook</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/SCRIPTS/obsidian/start_webhook_server.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

# Ativar
launchctl load ~/Library/LaunchAgents/com.claudecode.webhook.plist
```

---

## 📋 Resumo

**No MacBook (1x):**
```bash
./SCRIPTS/obsidian/start_webhook_server.sh
```

**No iPad (sempre que quiser):**
```bash
curl -X POST http://192.168.18.11:8000/obsidian/process \
  -H "Content-Type: application/json" \
  -d '{"file":"nota.md","content":"conteúdo..."}'
```

**Resultado:**
```
📱 iPad → 💻 MacBook → 📁 temp/obsidian/nota.md
```

---

## 🎯 Endpoints Disponíveis

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/status` | GET | Status do servidor |
| `/obsidian/process` | POST | Processar nota |
| `/obsidian/task` | POST | Criar tarefa |

**Payload exemplo:**
```json
{
  "file": "minha-nota.md",
  "content": "# Título\nConteúdo da nota..."
}
```

---

**IP MacBook:** `192.168.18.11`
**Porta:** `8000`
**URL Base:** `http://192.168.18.11:8000`
