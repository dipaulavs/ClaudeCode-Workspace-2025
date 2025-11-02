# ⚡ Terminal Chat - Guia de Uso

Interface de chat mobile-first para executar comandos do Claude Code diretamente pelo navegador, como se fosse o terminal do Mac.

## 🎯 O Que É?

Um chatbot estilo WhatsApp/ChatGPT que executa os comandos que você digita **exatamente** como se estivesse no terminal. Qualquer comando que você digitaria no Claude Code CLI funciona aqui!

## ✨ Características

- 📱 **Mobile First** - Otimizado para celular/tablet
- 💬 **Interface de Chat** - Bolhas de mensagem tipo WhatsApp
- ⚡ **Execução em Tempo Real** - Comandos executam no seu Mac instantaneamente
- 💾 **Histórico Persistente** - Salvo no navegador (localStorage)
- ⌨️ **Comandos Rápidos** - Botões para comandos frequentes
- 🎨 **Design Moderno** - Gradientes, animações, responsivo

## 🚀 Como Usar

### 1. Iniciar os Serviços

```bash
cd web-interface
bash start-all.sh
```

Isso inicia:
- ✅ Backend API (porta 8000)
- ✅ Frontend Web (porta 3000)
- ✅ Terminal Web (porta 7681)

### 2. Acessar o Terminal Chat

**No Mac:**
- Abra http://localhost:3000
- Clique no card "⚡ Terminal Chat"

**No Celular/Remoto:**
- Execute `bash start-cloudflare.sh` em outro terminal
- Acesse a URL gerada (ex: https://xxxxx.trycloudflare.com)
- Clique no card "⚡ Terminal Chat"

### 3. Usar o Chat

Digite comandos normalmente, como faria no terminal:

```bash
# Comandos do Claude Code
/new
/context
/usage
/clear

# Comandos bash
ls tools/
cat README.md
pwd
ls -la ~/Downloads

# Executar ferramentas Python
python3 tools/generate_image_nanobanana.py "gato fofo" --format PNG

# Navegar no sistema
cd web-interface
ls -la
```

## 💡 Exemplos de Uso

### Exemplo 1: Iniciar Nova Conversa
```
Você: /new
Bot: 🤖 Nova conversa iniciada!
```

### Exemplo 2: Listar Ferramentas
```
Você: ls tools/
Bot: 🤖 Executando...
     ✅ generate_image_nanobanana.py
        generate_image.py
        generate_audio_elevenlabs.py
        ...
```

### Exemplo 3: Gerar Imagem
```
Você: python3 tools/generate_image_nanobanana.py "cachorro surfando" --format PNG
Bot: 🤖 Gerando imagem...
     ✅ Imagem salva em: ~/Downloads/cachorro_surfando_123.png
```

### Exemplo 4: Ver Contexto
```
Você: /context
Bot: 🤖 Context usage: 45000/200000 tokens
     Projects: 3 active
     ...
```

## 🎮 Comandos Rápidos (Botões)

A interface inclui botões para comandos frequentes:

- `/new` - Nova conversa
- `/context` - Ver contexto
- `/usage` - Ver uso de tokens
- `ls tools/` - Listar ferramentas
- `cat README.md` - Ver README

## ⌨️ Atalhos de Teclado

- `Cmd/Ctrl + K` - Limpar histórico
- `Cmd/Ctrl + /` - Focar no campo de input
- `Enter` - Enviar mensagem
- `Shift + Enter` - Nova linha (no textarea)

## 🔧 Como Funciona

```
[Você digita no chat]
    ↓
[Frontend envia para API]
    ↓
[Backend executa no Mac]
    ↓
[Output retorna para o chat]
    ↓
[Você vê o resultado]
```

## 📱 Vantagens do Terminal Chat vs Terminal Web

| Feature | Terminal Chat | Terminal Web (ttyd) |
|---------|--------------|---------------------|
| Interface | Bolhas de chat modernas | Terminal tradicional |
| Mobile | Otimizado para toque | Difícil de usar |
| Histórico | Salvo automaticamente | Session-based |
| UX | Intuitivo tipo WhatsApp | Requer conhecimento CLI |
| Copy/Paste | Fácil | Complicado no mobile |
| Comandos Rápidos | Botões prontos | Precisa digitar tudo |

## 🎨 Personalização

### Adicionar Novos Comandos Rápidos

Edite `chat-terminal.html` e adicione botões na seção `quick-commands`:

```html
<button onclick="sendQuickCommand('seu comando')"
        class="quick-command px-3 py-1.5 bg-blue-100 text-blue-700 rounded-full text-xs font-semibold whitespace-nowrap">
    <i class="fas fa-icon mr-1"></i>Nome
</button>
```

### Mudar Cores/Tema

O arquivo usa Tailwind CSS. Edite as classes para personalizar:

```css
/* Gradiente do fundo */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Cores das mensagens do usuário */
.user-message {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Cores das mensagens do bot */
.bot-message {
    background: white;
}
```

## 🐛 Troubleshooting

### "Backend offline" no status

```bash
# Verificar se backend está rodando
lsof -i :8000

# Se não estiver, iniciar
cd web-interface
bash start-backend.sh
```

### Comandos não executam

```bash
# Verificar logs do backend
tail -f /tmp/claude-backend.log

# Reiniciar backend
pkill -f "uvicorn"
bash start-backend.sh
```

### Histórico não salva

- Verifique se o navegador permite localStorage
- Em modo privado/anônimo, o histórico não persiste
- Limpe o cache do navegador

### Interface não carrega

```bash
# Verificar se frontend está rodando
lsof -i :3000

# Se não estiver, iniciar
cd web-interface
bash start-frontend.sh
```

## 🔒 Segurança

### Local (Mac)
- ✅ Totalmente seguro
- ✅ Comandos executam com suas permissões
- ✅ Nada sai do seu Mac

### Remoto (Cloudflare Tunnel)
- ⚠️ **CUIDADO**: Qualquer pessoa com a URL pode executar comandos
- 💡 Recomendações:
  - Use URLs temporárias (trycloudflare.com)
  - Não compartilhe a URL publicamente
  - Adicione autenticação se expor permanentemente
  - Use apenas em redes confiáveis

### Adicionar Autenticação (Opcional)

Para acesso remoto seguro, você pode adicionar autenticação básica:

```python
# No backend/main.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "seu_usuario" or credentials.password != "sua_senha":
        raise HTTPException(status_code=401)
    return credentials

# Adicionar em cada endpoint
@app.post("/api/terminal/execute", dependencies=[Depends(verify_credentials)])
```

## 📊 Limitações

1. **Comandos Interativos**: Comandos que requerem input (como `vim`, `nano`) não funcionam
2. **Comandos Longos**: Timeout de 2 minutos (configurável no backend)
3. **Output Grande**: Limitado a 1000 caracteres (configurável)
4. **Sessão Separada**: Cada comando executa em sessão nova (não mantém `cd`, variáveis)

### Soluções

Para comandos que mudam diretório:
```bash
# Ao invés de:
cd /pasta
ls

# Use:
ls /pasta
```

Para comandos sequenciais:
```bash
# Use && para encadear
cd /pasta && ls && cat arquivo.txt
```

## 🎯 Casos de Uso

### 1. Controle Remoto do Mac
Use no celular para executar comandos no seu Mac de qualquer lugar

### 2. Interface Amigável para Não-Técnicos
Compartilhe com pessoas que têm dificuldade com terminal tradicional

### 3. Automação Rápida
Botões de comando rápido para tarefas frequentes

### 4. Monitoramento
Verificar status, logs, processos do Mac remotamente

### 5. Desenvolvimento
Testar comandos e ferramentas com feedback visual bonito

## 💰 Custos

- **Infraestrutura**: R$ 0 (roda no seu Mac)
- **APIs**: R$ 0 (usa suas credenciais Claude Code)
- **Cloudflare Tunnel**: R$ 0 (grátis)
- **Total**: R$ 0 🎉

## 🚀 Próximos Passos

Após iniciar, você pode:

1. ✅ Testar comandos básicos (`ls`, `pwd`, `/new`)
2. ✅ Adicionar comandos rápidos personalizados
3. ✅ Configurar acesso remoto via Cloudflare
4. ✅ Usar no celular/tablet
5. ✅ Personalizar cores e tema

## 🆘 Suporte

Se tiver problemas:

1. Verifique se `bash start-all.sh` está rodando
2. Acesse http://localhost:8000/docs para ver a API
3. Verifique os logs em `/tmp/claude-*.log`
4. Reinicie todos os serviços

---

**Desenvolvido para Claude Code Workspace** 🤖

Interface moderna e mobile-first para executar comandos do terminal pelo navegador! 🚀
