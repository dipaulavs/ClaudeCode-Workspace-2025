# 🚀 Início Rápido - Interface Web

## ▶️ Em 3 Passos

### 1️⃣ Iniciar os Serviços

```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/web-interface
bash start-all.sh
```

Aguarde alguns segundos até ver:
```
✅ Todos os serviços foram iniciados!
```

### 2️⃣ Acessar no Seu Mac

Abra o navegador e acesse:

🎨 **Interface Principal**: http://localhost:3000

💻 **Terminal Claude Code**: http://localhost:7681

### 3️⃣ Acessar no Celular (Qualquer Lugar)

**Abra um SEGUNDO terminal** e execute:

```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/web-interface
bash start-cloudflare.sh
```

Você verá algo como:
```
Your quick Tunnel has been created! Visit it at (it may take some time to be reachable):
https://xxxxx-xxx-xxx.trycloudflare.com
```

**🎉 Copie essa URL e cole no navegador do seu celular!**

---

## 📱 Usando no Celular

1. Abra o navegador do celular
2. Cole a URL do Cloudflare (`https://xxxxx.trycloudflare.com`)
3. Use normalmente como se estivesse no Mac!

### O que você pode fazer:
- ✅ Gerar imagens (salvam no Mac)
- ✅ Gerar áudios (salvam no Mac)
- ✅ Gerar vídeos (salvam no Mac)
- ✅ Transcrever vídeos
- ✅ Ver e baixar todos os arquivos gerados
- ✅ Usar o terminal do Claude Code pelo navegador

---

## 🛑 Parar os Serviços

No terminal onde você rodou `start-all.sh`, pressione:

```
Ctrl + C
```

---

## 💡 Dicas

### Manter Rodando
Se fechar o terminal, os serviços param. Para manter rodando:
```bash
# Usar tmux ou screen
tmux
bash start-all.sh
# Pressione: Ctrl+B depois D (para desanexar)

# Para voltar:
tmux attach
```

### URL Temporária
A URL do Cloudflare é temporária e muda cada vez que você roda `start-cloudflare.sh`.

Para URL permanente, veja: `README.md` (seção "URLs Permanentes")

### Segurança
- A interface não tem senha por padrão
- Use apenas em redes confiáveis
- Ou configure autenticação (veja README.md)

---

## ❓ Problemas?

### "Connection refused"
- Aguarde 5-10 segundos após iniciar
- Verifique se o terminal não mostrou erros

### "Port already in use"
```bash
# Matar processos antigos
lsof -i :3000
lsof -i :8000
kill -9 [PID]

# Reiniciar
bash start-all.sh
```

### Arquivos não aparecem
- Clique em "Atualizar Lista" na aba "Arquivos"
- Verifique se estão em `~/Downloads`

---

**Pronto! Agora você pode usar suas ferramentas de IA de qualquer lugar! 🌍**
