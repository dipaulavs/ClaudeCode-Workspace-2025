# 🌐 Interface Web para Claude Code Workspace

Interface web bonita para acessar suas ferramentas de IA de qualquer lugar, diretamente do seu Mac.

## ✨ Características

- **🎨 Interface Web Moderna** - Dashboard bonito tipo ChatGPT
- **💻 Terminal Web** - Acesse o Claude Code pelo navegador
- **📱 Acesso Remoto** - Use no celular/tablet de qualquer lugar do mundo
- **🔒 Execução Local** - Tudo roda no seu Mac (zero custos de API externa)
- **📥 Downloads no Mac** - Arquivos salvos em ~/Downloads do seu Mac
- **🌍 Cloudflare Tunnel** - Acesso remoto grátis e seguro

## 🏗️ Arquitetura

```
[Celular/Tablet/PC]
    ↓
[Cloudflare Tunnel - Grátis]
    ↓
[Mac - Interface Web] :3000 ← Você acessa aqui
    ↓
[Mac - Backend API] :8000 ← Executa ferramentas
    ↓
[Mac - Terminal Web] :7681 ← Claude Code no navegador
    ↓
[Ferramentas Python] → ~/Downloads
```

## 🚀 Setup Inicial (Apenas uma vez)

```bash
cd web-interface
bash setup.sh
```

Isso irá instalar:
- FastAPI e dependências do backend
- ttyd (terminal web)
- cloudflared (Cloudflare Tunnel)

## ▶️ Como Usar

### 1. Iniciar Todos os Serviços

```bash
cd web-interface
bash start-all.sh
```

Isso inicia:
- ✅ Backend API (porta 8000)
- ✅ Frontend Web (porta 3000)
- ✅ Terminal Web (porta 7681)

### 2. Acessar Localmente (No Mac)

Abra o navegador e acesse:

- **Interface Web**: http://localhost:3000
- **Terminal Claude**: http://localhost:7681
- **API Docs**: http://localhost:8000/docs

### 3. Acessar Remotamente (Celular/Qualquer Lugar)

Em outro terminal, execute:

```bash
cd web-interface
bash start-cloudflare.sh
```

Você receberá uma URL tipo:
```
https://xxxxx.trycloudflare.com
```

**Acesse essa URL no seu celular!** 🎉

## 🎨 Funcionalidades da Interface

### 1. Gerar Imagens
- **Nano Banana** (Gemini 2.5 Flash)
- **GPT-4o** (Kie.ai)
- Formatos: PNG, JPEG
- Salva em ~/Downloads automaticamente

### 2. Gerar Áudio
- **ElevenLabs TTS**
- Vozes: Felipe (masculina), Michele (feminina)
- Qualidade: Alta, Ultra, Média
- Salva em ~/Downloads

### 3. Gerar Vídeos
- **Sora 2** (OpenAI)
- Formatos: Portrait, Landscape, Square
- ~15 segundos
- Tempo de geração: 2-5 minutos
- Salva em ~/Downloads

### 4. Transcrever
- YouTube, TikTok, Instagram, etc.
- Idiomas: Português, Inglês, Espanhol
- Salva transcrição em ~/Downloads

### 5. Arquivos
- Lista todos os arquivos gerados
- Download direto pelo navegador
- Ordenados por data (mais recentes primeiro)

### 6. Terminal Claude Code
- Acesso ao Claude Code pelo navegador
- 7 botões de ação rápida (Nova Conversa, Ver Uso, etc)
- Atalhos de teclado (Ctrl+N, Ctrl+K, etc)
- Copia comandos automaticamente para área de transferência
- Mesma sessão logada
- Zero custos de API

## 📂 Estrutura dos Arquivos

```
web-interface/
├── backend/
│   ├── main.py              # API FastAPI
│   └── requirements.txt     # Dependências Python
├── frontend/
│   ├── index.html          # Interface web
│   └── server.py           # Servidor HTTP
├── setup.sh                # Instalação de dependências
├── start-all.sh            # Inicia todos os serviços
├── start-backend.sh        # Apenas backend
├── start-frontend.sh       # Apenas frontend
├── start-terminal.sh       # Apenas terminal
└── start-cloudflare.sh     # Túnel para acesso remoto
```

## 🔧 Scripts Individuais

Se você quiser iniciar cada componente separadamente:

```bash
# Backend API
bash start-backend.sh

# Frontend Web
bash start-frontend.sh

# Terminal Web
bash start-terminal.sh

# Cloudflare Tunnel
bash start-cloudflare.sh
```

## 💡 Dicas de Uso

### Para Deixar Rodando 24/7

1. **Prevenir Sleep do Mac:**
```bash
# Em Configurações do Sistema > Bateria/Energia
# Configure para "Nunca" desligar a tela quando conectado
```

2. **Iniciar Automaticamente no Boot:**
```bash
# Adicione ao crontab:
crontab -e

# Adicione a linha:
@reboot cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/web-interface && bash start-all.sh
```

### Acesso Remoto Seguro

O Cloudflare Tunnel já é seguro (HTTPS automático), mas você pode adicionar:

1. **Autenticação Básica** (opcional)
2. **VPN com Tailscale** (para acesso privado)
3. **Firewall do Mac** configurado

### URLs Permanentes

Por padrão, o Cloudflare Tunnel gera URLs temporárias. Para URLs permanentes:

```bash
# Criar túnel permanente
cloudflared tunnel create meu-workspace
cloudflared tunnel route dns meu-workspace workspace.seudominio.com

# Editar start-cloudflare.sh para usar o túnel nomeado
```

## 🐛 Troubleshooting

### Backend não inicia
```bash
# Reinstalar dependências
cd backend
pip3 install --user -r requirements.txt
```

### Terminal não aparece
```bash
# Verificar se ttyd está instalado
which ttyd

# Se não estiver, instalar:
brew install ttyd
```

### Porta já em uso
```bash
# Verificar o que está usando a porta
lsof -i :3000
lsof -i :8000
lsof -i :7681

# Matar o processo se necessário
kill -9 PID
```

### Cloudflare Tunnel não conecta
```bash
# Verificar instalação
cloudflared --version

# Reinstalar se necessário
brew reinstall cloudflare/cloudflare/cloudflared
```

## 💰 Custos

- **VPS/Cloud**: R$ 0 (roda no seu Mac)
- **API Externa**: R$ 0 (usa sua conta Claude Code)
- **Cloudflare Tunnel**: R$ 0 (grátis)
- **Energia Mac 24h**: ~R$ 20-30/mês

## 🔒 Segurança

- ✅ HTTPS automático via Cloudflare
- ✅ Execução local (nada sai do seu Mac)
- ✅ Sem APIs externas cobradas
- ✅ Arquivos apenas em ~/Downloads local
- ⚠️ Considere adicionar autenticação se expor publicamente

## 📝 Próximos Passos

Após rodar `bash start-all.sh`:

1. Acesse http://localhost:3000 no navegador
2. Teste gerar uma imagem
3. Abra outro terminal e rode `bash start-cloudflare.sh`
4. Copie a URL gerada e acesse no seu celular
5. Pronto! Use de qualquer lugar do mundo 🌍

## 🆘 Suporte

Se tiver problemas:

1. Verifique os logs em `/tmp/claude-*.log`
2. Execute `bash setup.sh` novamente
3. Reinicie todos os serviços

---

**Desenvolvido para Claude Code Workspace** 🤖
