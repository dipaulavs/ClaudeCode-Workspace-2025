# 🛠️ Comandos Úteis - Interface Web

## 🚀 Operações Básicas

### Iniciar Tudo
```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/web-interface
bash start-all.sh
```

### Parar Tudo
```bash
# No terminal onde rodou start-all.sh:
Ctrl + C

# Ou forçar:
pkill -f "python3 main.py"
pkill -f "python3 server.py"
pkill -f "ttyd"
```

### Iniciar Apenas Backend
```bash
bash start-backend.sh
```

### Iniciar Apenas Frontend
```bash
bash start-frontend.sh
```

### Iniciar Apenas Terminal
```bash
bash start-terminal.sh
```

### Iniciar Cloudflare Tunnel
```bash
bash start-cloudflare.sh
```

## 🔍 Verificar Status

### Backend está rodando?
```bash
curl http://localhost:8000/api/health
# Esperado: {"status":"healthy","timestamp":"..."}
```

### Frontend está rodando?
```bash
curl -I http://localhost:3000
# Esperado: HTTP/1.0 200 OK
```

### Terminal está rodando?
```bash
curl -I http://localhost:7681
# Esperado: HTTP/1.1 200 OK
```

### Ver portas em uso
```bash
lsof -i :3000   # Frontend
lsof -i :8000   # Backend
lsof -i :7681   # Terminal
```

## 📊 Logs

### Ver logs em tempo real
```bash
# Backend
tail -f /tmp/claude-backend.log

# Frontend
tail -f /tmp/claude-frontend.log

# Terminal
tail -f /tmp/claude-terminal.log

# Todos juntos
tail -f /tmp/claude-*.log
```

### Ver últimas 50 linhas
```bash
tail -n 50 /tmp/claude-backend.log
```

### Limpar logs
```bash
rm /tmp/claude-*.log
```

## 🔧 Manutenção

### Reinstalar dependências
```bash
cd backend
pip3 install --user -r requirements.txt
```

### Verificar instalações
```bash
# Python
python3 --version

# FastAPI
python3 -c "import fastapi; print(fastapi.__version__)"

# ttyd
which ttyd
ttyd --version

# cloudflared
which cloudflared
cloudflared --version
```

### Atualizar Homebrew packages
```bash
brew upgrade ttyd
brew upgrade cloudflared
```

## 🌍 Cloudflare Tunnel

### Iniciar túnel rápido (temporário)
```bash
cloudflared tunnel --url http://localhost:3000
```

### Criar túnel permanente
```bash
# 1. Login
cloudflared tunnel login

# 2. Criar túnel
cloudflared tunnel create meu-workspace

# 3. Configurar DNS
cloudflared tunnel route dns meu-workspace workspace.seudominio.com

# 4. Rodar túnel
cloudflared tunnel run meu-workspace
```

### Listar túneis
```bash
cloudflared tunnel list
```

## 📦 Teste Individual de Ferramentas

### Testar geração de imagem via API
```bash
curl -X POST http://localhost:8000/api/generate/image \
  -H "Content-Type: application/json" \
  -d '{"prompt": "gato fofo", "tool": "nanobanana", "format": "PNG"}'
```

### Testar listagem de arquivos
```bash
curl http://localhost:8000/api/files | python3 -m json.tool
```

### Testar health check
```bash
curl http://localhost:8000/api/health | python3 -m json.tool
```

### Testar lista de ferramentas
```bash
curl http://localhost:8000/api/tools | python3 -m json.tool
```

## 🔐 Segurança

### Ver conexões ativas
```bash
netstat -an | grep LISTEN | grep -E "3000|8000|7681"
```

### Bloquear acesso externo (apenas localhost)
```bash
# Editar backend/main.py, linha:
# uvicorn.run(app, host="0.0.0.0", port=8000)
# Mudar para:
# uvicorn.run(app, host="127.0.0.1", port=8000)

# Fazer o mesmo em frontend/server.py
```

### Adicionar senha básica (Cloudflare Access)
```bash
cloudflared access login
# Seguir instruções para configurar autenticação
```

## 🎯 Desenvolvimento

### Testar backend isolado
```bash
cd backend
python3 main.py
# Acesse: http://localhost:8000/docs
```

### Editar frontend
```bash
# Editar: frontend/index.html
# Salvar
# Recarregar navegador (Ctrl+R)
# Não precisa reiniciar o servidor!
```

### Adicionar novo endpoint
```bash
# 1. Editar backend/main.py
# 2. Adicionar função @app.post("/api/novo-endpoint")
# 3. Reiniciar backend (Ctrl+C e bash start-backend.sh)
# 4. Testar: curl http://localhost:8000/api/novo-endpoint
```

## 🐛 Troubleshooting

### Porta já em uso
```bash
# Descobrir PID
lsof -ti :8000

# Matar processo
kill -9 $(lsof -ti :8000)
```

### Python module not found
```bash
cd backend
pip3 install --user -r requirements.txt
```

### Cloudflared não conecta
```bash
# Verificar internet
ping 1.1.1.1

# Verificar status
cloudflared tunnel list

# Logs detalhados
cloudflared tunnel --loglevel debug --url http://localhost:3000
```

### Downloads não aparecem
```bash
# Verificar permissões
ls -la ~/Downloads

# Testar criação de arquivo
touch ~/Downloads/teste.txt && ls ~/Downloads/teste.txt && rm ~/Downloads/teste.txt
```

## 📱 Mobile

### Testar acesso mobile localmente (mesma rede)
```bash
# Descobrir IP do Mac
ifconfig | grep "inet " | grep -v 127.0.0.1

# Acessar do celular:
# http://[IP-DO-MAC]:3000
```

### Gerar QR Code da URL
```bash
# Instalar qrencode
brew install qrencode

# Gerar QR Code
cloudflared tunnel --url http://localhost:3000 | grep trycloudflare | qrencode -t ansiutf8
```

## 🔄 Automação

### Iniciar automaticamente no login
```bash
# Criar LaunchAgent
cat > ~/Library/LaunchAgents/com.claudecode.webapp.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.claudecode.webapp</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/web-interface/start-all.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

# Carregar
launchctl load ~/Library/LaunchAgents/com.claudecode.webapp.plist
```

### Prevenir sleep do Mac
```bash
# Prevenir sleep enquanto script roda
caffeinate -s bash start-all.sh
```

## 🎨 Customização

### Mudar cor do tema
```bash
# Editar frontend/index.html
# Procurar por: background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# Alterar cores hexadecimais
```

### Mudar porta do frontend
```bash
# Editar frontend/server.py
# Linha: PORT = 3000
# Mudar para: PORT = 8080 (ou outra)

# Também atualizar em start-cloudflare.sh
```

### Adicionar logo personalizada
```bash
# Adicionar em frontend/index.html antes do <h1>:
# <img src="https://seu-logo.com/logo.png" class="w-20 h-20 mx-auto mb-4">
```

## 📊 Monitoramento

### Ver uso de CPU/RAM
```bash
# Processos Python
ps aux | grep python3

# Uso de rede
nettop -P -J bytes_in,bytes_out
```

### Estatísticas do backend
```bash
# Quantas requisições
grep -c "GET\|POST" /tmp/claude-backend.log

# Últimas requisições
tail -20 /tmp/claude-backend.log | grep "INFO"
```

---

**💡 Dica:** Salve este arquivo como favorito para consulta rápida!
