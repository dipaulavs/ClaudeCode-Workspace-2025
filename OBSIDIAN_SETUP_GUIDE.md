# 🚀 Obsidian - Guia Rápido de Setup

**Tempo estimado:** 5-10 minutos

---

## ✅ Checklist de Instalação

### Etapa 1: Plugin Local REST API (5 min)

**No Obsidian que você já instalou:**

1. ⚙️ **Abra Settings** (canto inferior esquerdo ou `Cmd + ,`)

2. 🔌 **Ative Community Plugins:**
   - No menu lateral → **Community plugins**
   - Se aparecer aviso → Clique **"Turn on community plugins"**

3. 🔍 **Instale o plugin:**
   - Clique em **"Browse"**
   - Na busca, digite: **"Local REST API"**
   - Encontre: **"Local REST API"** (autor: coddingtonbear)
   - Clique **"Install"**
   - Clique **"Enable"**

4. 🔑 **Copie sua API Key:**
   - Settings → **Local REST API**
   - Você verá um campo **"API Key"** com uma chave longa
   - Clique no ícone de copiar ao lado
   - **GUARDE ESSA KEY** (vamos usar em breve)

✅ **Plugin instalado!**

---

### Etapa 2: Configurar API Key no Workspace (1 min)

**No terminal:**

```bash
# Navegue para o workspace
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace

# Adicione a API Key ao .env
echo 'OBSIDIAN_API_KEY=SUA_API_KEY_AQUI' >> .env
```

**⚠️ IMPORTANTE:** Substitua `SUA_API_KEY_AQUI` pela key que você copiou no passo anterior!

**Exemplo:**
```bash
echo 'OBSIDIAN_API_KEY=abc123def456ghi789...' >> .env
```

✅ **API Key configurada!**

---

### Etapa 3: Testar Conexão (1 min)

**No terminal:**

```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace

# Testar conexão com Obsidian
python3 scripts/obsidian/obsidian_client.py
```

**Resultado esperado:**
```
🔍 Testando conexão com Obsidian...
✅ Conexão estabelecida!

📊 Vault: /Users/felipemdepaula/Library/Mobile Documents/iCloud~md~obsidian/Documents/Claude-code-ios
```

**Se deu erro:**
- Certifique-se que Obsidian está **aberto**
- Verifique se plugin está **ativado** (Settings → Community plugins → Local REST API → ON)
- Confirme que API Key está correta no `.env`

✅ **Conexão testada!**

---

### Etapa 4: Criar Primeira Nota de Teste (1 min)

```bash
# Criar nota rápida
python3 scripts/obsidian/quick_note.py "Minha primeira nota via automação!"
```

**Resultado esperado:**
```
✅ Nota criada com sucesso!
📍 Localização: 00 - Inbox/Quick Note - 20251102-081500.md
```

**Verificar no Obsidian:**
1. Vá para a pasta **"00 - Inbox"**
2. Você verá a nota criada!

✅ **Primeira nota criada!**

---

### Etapa 5: Testar Captura de Ideia (1 min)

```bash
# Capturar ideia estruturada
python3 scripts/obsidian/capture_idea.py "App de Delivery Fitness" \
  --desc "App para entrega de marmitas fitness" \
  --tags "negocio,app,fitness"
```

**Resultado esperado:**
```
✅ Ideia capturada com sucesso!
💡 Título: App de Delivery Fitness
📍 Localização: 02 - Ideias/App de Delivery Fitness.md
🏷️  Tags: #ideia #negocio #app #fitness
```

**Verificar no Obsidian:**
1. Vá para **"02 - Ideias"**
2. Abra a nota criada
3. Veja a estrutura completa!

✅ **Sistema funcionando perfeitamente!**

---

## 🎉 Pronto! Agora você pode:

### 📝 Criar Notas Rápidas
```bash
python3 scripts/obsidian/quick_note.py "Sua nota aqui"
```

### 💡 Capturar Ideias
```bash
python3 scripts/obsidian/capture_idea.py "Nome da Ideia" --desc "Descrição"
```

### 📅 Criar Daily Note
```bash
python3 scripts/obsidian/create_daily.py
```

### 📂 Criar Projeto
```bash
python3 scripts/obsidian/new_project.py "Nome do Projeto"
```

---

## 📱 Próximo Passo: iPhone (Opcional)

1. **Baixe Obsidian iOS:** [App Store](https://apps.apple.com/app/obsidian-connected-notes/id1557175442)
2. **Abra o app**
3. **Selecione "Open folder as vault"**
4. **Escolha:** iCloud Drive → Obsidian [meu cerebro] → dipaula → **claude-code**
5. **Pronto!** Sincronizado automaticamente ✨

---

## 📚 Documentação Completa

- **Scripts:** `scripts/obsidian/README.md`
- **Integração:** `docs/tools/obsidian_integration.md`
- **Estrutura:** `ÍNDICE GERAL.md` (no vault Obsidian)

---

## 🆘 Problemas Comuns

### ❌ "Não foi possível conectar"
- Obsidian está aberto?
- Plugin está ativado?
- API Key está correta no `.env`?

### ❌ "OBSIDIAN_API_KEY não configurada"
- Verifique se adicionou no `.env`:
  ```bash
  cat .env | grep OBSIDIAN_API_KEY
  ```
- Se não aparecer nada, adicione novamente

### ❌ Nota não aparece no Obsidian
- Atualize a visualização (Cmd + R)
- Verifique se está na pasta correta

---

## 🎯 Próximos Passos Sugeridos

1. ✅ Explorar a estrutura de pastas no Obsidian
2. ✅ Ler os READMEs de cada pasta
3. ✅ Criar sua primeira daily note
4. ✅ Capturar algumas ideias
5. ✅ Criar um projeto de teste
6. ✅ Instalar no iPhone para sincronizar

---

**Última atualização:** 2025-11-02
**Criado por:** Claude Code
**Suporte:** Ver documentação completa em `docs/tools/obsidian_integration.md`
