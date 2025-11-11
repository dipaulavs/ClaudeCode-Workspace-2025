# 🔄 Setup Syncthing - Obsidian Remote CLI

Guia para conectar Mac ↔ VPS e sincronizar vault do Obsidian.

## ✅ Status Atual

- ✅ Syncthing instalado no Mac (http://localhost:8384)
- ✅ Syncthing instalado na VPS (82.25.68.132)
- ✅ Ambos rodando como serviços

## 📋 Device IDs

**VPS Device ID:**
```
4MDCXYP-NJUX2NJ-HKX5ADR-LNLTQCN-4GYM25J-ENSGTOV-AL4TYUR-TKWVEA2
```

**Mac Device ID:**
- Abrir: http://localhost:8384
- Actions → Show ID
- Copiar o código que aparece

## 🔗 Passo 1: Conectar Mac → VPS

### No Mac (http://localhost:8384):

1. Clicar em **"+ Add Remote Device"** (canto inferior direito)
2. **Device ID:** Colar `4MDCXYP-NJUX2NJ-HKX5ADR-LNLTQCN-4GYM25J-ENSGTOV-AL4TYUR-TKWVEA2`
3. **Device Name:** VPS Loop9
4. Clicar **"Save"**

## 🔗 Passo 2: Aceitar conexão na VPS

### Acessar Syncthing da VPS via túnel SSH:

```bash
# Criar túnel SSH (rodar em novo terminal)
ssh -L 8385:localhost:8384 root@82.25.68.132
```

**Deixar esse terminal aberto!**

### No navegador, abrir: http://localhost:8385

1. Vai aparecer notificação: **"New Device"**
2. Clicar **"Add Device"**
3. Verificar Device ID do Mac está correto
4. Clicar **"Save"**

## 📁 Passo 3: Compartilhar pasta Obsidian

### No Mac (http://localhost:8384):

1. Clicar em **"+ Add Folder"** (canto inferior esquerdo)
2. Preencher:
   - **Folder Label:** Obsidian Claude Code
   - **Folder Path:** `/Users/felipemdepaula/Documents/Obsidian/Claude-code-ios`
   - **Folder Type:** Send & Receive
3. Ir na aba **"Sharing"**
4. Marcar checkbox: **VPS Loop9** ✅
5. Clicar **"Save"**

## 📥 Passo 4: Aceitar pasta na VPS

### No navegador (http://localhost:8385):

1. Vai aparecer notificação: **"New Folder"**
2. Clicar **"Add"**
3. Modificar **Folder Path:** `/root/Obsidian/Claude-code-ios`
4. Clicar **"Save"**

## ⏳ Passo 5: Aguardar sincronização inicial

A primeira sincronização pode demorar dependendo do tamanho do vault.

**No Mac (http://localhost:8384):**
- Ver progresso em "Remote Devices" → VPS Loop9
- Quando aparecer "Up to Date" ✅ está pronto!

## ✅ Passo 6: Verificar na VPS

```bash
ssh root@82.25.68.132
ls -la /root/Obsidian/Claude-code-ios/

# Deve listar seus arquivos do Obsidian
```

## 🐳 Passo 7: Atualizar Docker Compose

Quando sincronização estiver completa:

```bash
cd ~/Desktop/ClaudeCode-Workspace/SWARM/automations/obsidian-remote-cli

# Editar docker-compose.yml
# Descomentar volumes:
#   - /root/Obsidian/Claude-code-ios:/vault:ro
#   - /root/ClaudeCode-Workspace:/workspace

git add . && git commit -m "feat: ativar volumes Syncthing" && git push

# Na VPS, atualizar
ssh root@82.25.68.132 "cd /root/obsidian-remote-cli && git pull && docker service update --force obsidian-cli_app"
```

## 🎯 Passo 8: Atualizar app.py

```python
# Mudar de:
OBSIDIAN_VAULT = "/vault"  # Placeholder

# Para:
OBSIDIAN_VAULT = "/vault"  # Path real via Syncthing
```

Remover o retorno de "CONFIGURAÇÃO PENDENTE" e ativar a lógica real.

## 🧪 Passo 9: Testar

```bash
# Criar nota de teste no Mac
echo "# Teste Sync" > ~/Documents/Obsidian/Claude-code-ios/teste-sync.md

# Aguardar ~2 segundos

# Verificar na VPS
ssh root@82.25.68.132 "ls -la /root/Obsidian/Claude-code-ios/teste-sync.md"

# Deve aparecer! ✅
```

## 🐛 Troubleshooting

### Syncthing não conecta?

**Verificar firewalls:**
```bash
# Na VPS
sudo ufw allow 22000/tcp
sudo ufw allow 21027/udp
```

**Verificar status:**
```bash
# Mac
brew services list | grep syncthing

# VPS
ssh root@82.25.68.132 "systemctl status syncthing@root"
```

### Pasta não sincroniza?

1. Verificar em Actions → Show ID se Device IDs estão corretos
2. Verificar pasta está compartilhada com device remoto
3. Forçar rescan: Folder → Edit → Advanced → Scan Interval

### Túnel SSH não funciona?

```bash
# Fechar todos os túneis
killall ssh

# Recriar
ssh -L 8385:localhost:8384 root@82.25.68.132
```

## 📊 Monitoramento

### Ver status em tempo real:

**Mac:**
```bash
open http://localhost:8384
```

**VPS (via túnel):**
```bash
ssh -L 8385:localhost:8384 root@82.25.68.132
open http://localhost:8385
```

### Logs:

**Mac:**
```bash
tail -f ~/Library/Application\ Support/Syncthing/syncthing.log
```

**VPS:**
```bash
ssh root@82.25.68.132 "journalctl -u syncthing@root -f"
```

## 🎉 Resultado Final

Quando tudo estiver configurado:

```
Mac → Criar/Modificar nota
      ↓ (2-5 segundos)
VPS → Nota aparece automaticamente
      ↓
API detecta → Executa Claude Code
      ↓ (processa)
VPS → Escreve notas organizadas
      ↓ (2-5 segundos)
Mac → Recebe notas organizadas ✅
```

**Zero intervenção manual! 🚀**

---

**Próximos passos após setup:**
1. Testar endpoint `/organize-notes` via Obsidian
2. Criar alias deploy para updates
3. Documentar no projeto README

**Setup completo:** ~15-20 minutos
**Manutenção:** Zero (automático)
