# 🎯 MÉTODO MAIS FÁCIL - OAuth (Login Google)

## ⚡ SUPER SIMPLES: Login + Clica "Autorizar"

**Tempo total:** 3-5 minutos
**Dificuldade:** ⭐☆☆☆☆ (Muito fácil)

Esqueça Service Account! Use OAuth:
1. Login com sua conta Google
2. Clica "Autorizar"
3. Pronto! ✅

---

## 🚀 PASSO A PASSO COMPLETO

### **PRÉ-REQUISITO** (só 1 vez)

```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

---

### **PASSO 1: Criar Credenciais OAuth** (2 minutos)

#### 1.1 Criar Projeto
- Acesse: https://console.cloud.google.com
- Clicar: "Selecionar projeto" → "NOVO PROJETO"
- Nome: `automaia-bot`
- Clicar: "CRIAR"

#### 1.2 Habilitar APIs
- Menu → "APIs e serviços" → "Biblioteca"
- Buscar e habilitar (2x):
  - ✅ **Google Sheets API**
  - ✅ **Google Drive API**

#### 1.3 Criar ID OAuth
- Menu → "APIs e serviços" → "Credenciais"
- Clicar: **"+ CRIAR CREDENCIAIS"**
- Escolher: **"ID do cliente OAuth"**
- Se aparecer "Configurar tela de consentimento":
  - Clicar → Externo → Criar
  - Nome do app: `Automaia Bot`
  - Email de suporte: seu email
  - Salvar e continuar (3x até chegar em "Voltar ao painel")
  - Voltar para "Credenciais"
- Tipo de aplicativo: **"Aplicativo para computador"**
- Nome: `Automaia Desktop`
- Clicar: **"CRIAR"**

#### 1.4 Baixar JSON
- Vai aparecer popup com credenciais
- Clicar: **"FAZER DOWNLOAD DO JSON"**
- Arquivo baixa: `client_secret_XXXXXX.json`

#### 1.5 Salvar no Projeto
```bash
mkdir -p config
mv ~/Downloads/client_secret_*.json config/google_credentials.json

# Verificar
ls -lh config/google_credentials.json
```

---

### **PASSO 2: Autenticar** (1 minuto)

```bash
python3 componentes/escalonamento/autenticar_google.py
```

**O que acontece:**
1. 🌐 Abre navegador automaticamente
2. 🔐 Login com sua conta Google
3. ⚠️ Pode aparecer: "Google não verificou este app"
   - Clicar: **"Avançado"**
   - Clicar: **"Acessar Automaia Bot (não seguro)"**
4. ✅ Permitir acesso:
   - Ver e gerenciar planilhas
   - Ver e gerenciar arquivos Drive
5. ✅ Página confirma: "Autenticação concluída!"
6. 💾 Token salvo em: `config/google_token.pickle`

**Pronto! Autenticado!** ✅

---

### **PASSO 3: Criar Planilha** (30 segundos)

```bash
python3 componentes/escalonamento/criar_agenda_publica_oauth.py
```

**O que acontece:**
```
🚀 CRIANDO PLANILHA DE AGENDA
===============================
📝 Nome: Agenda Automaia
📅 Dias: 7
👥 Vendedores: Bruno, Fernanda
⏰ Horários: 10:00, 14:00, 15:00, 16:00

1️⃣ Criando planilha...
✅ Planilha criada: 1A2B3C4D5E6F7G8H9I0J

2️⃣ Adicionando header...
✅ Header adicionado

3️⃣ Adicionando horários...
✅ 56 horários adicionados

4️⃣ Formatando colunas...
✅ Colunas formatadas

5️⃣ Adicionando validação...
✅ Validação adicionada

6️⃣ Adicionando cores...
✅ Cores adicionadas

7️⃣ Tornando pública...
✅ Planilha pública!

===============================
✅ PLANILHA CRIADA COM SUCESSO!
===============================

📊 ID: 1A2B3C4D5E6F7G8H9I0J
🔗 Link: https://docs.google.com/spreadsheets/d/1A2B3C4D5E6F7G8H9I0J/edit

💾 Salvar no config:
   "google_sheet_id": "1A2B3C4D5E6F7G8H9I0J"

🔧 Quer configurar no bot? (s/n): s

✅ ID salvo em: chatwoot_config_automaia.json
🔄 Reinicie o bot
```

**Pronto! Planilha criada!** 🎉

---

### **PASSO 4: Usar no Bot** (10 segundos)

```bash
./PARAR_BOT_AUTOMAIA.sh
./INICIAR_COM_NGROK.sh
```

**Testar:**
```
Cliente: "quero agendar"
Bot: Mostra horários da planilha! ✅
```

---

## 🎨 CUSTOMIZAR

### Nome Customizado
```bash
python3 componentes/escalonamento/criar_agenda_publica_oauth.py \
  --nome "Agenda Completa 2025"
```

### Mais Dias
```bash
python3 componentes/escalonamento/criar_agenda_publica_oauth.py \
  --dias 14
```

### Vendedores e Horários
```bash
python3 componentes/escalonamento/criar_agenda_publica_oauth.py \
  --vendedores "Bruno,Fernanda,Carlos" \
  --horarios "09:00,10:00,14:00,15:00,16:00"
```

---

## 🔄 TOKEN EXPIRA?

**Não precisa fazer nada!**
- Token dura 7 dias
- Renova automaticamente
- Só precisa autenticar 1x

Se expirar (raro):
```bash
python3 componentes/escalonamento/autenticar_google.py
```

---

## 🆚 COMPARAÇÃO: OAuth vs Service Account

| Aspecto | OAuth (Login) | Service Account |
|---------|---------------|-----------------|
| **Setup inicial** | 2-3 min | 5-10 min |
| **Dificuldade** | ⭐☆☆☆☆ | ⭐⭐⭐☆☆ |
| **Passos** | 3 passos | 6 passos |
| **Autenticação** | Clica "Autorizar" | Baixa JSON |
| **Planilha criada em** | Seu Drive | Service Account Drive |
| **Compartilhar** | Automático (sua conta) | Manual |
| **Token expira** | Renova automático | Nunca |
| **Recomendado para** | **Testes rápidos** | **Produção** |

**Conclusão:** OAuth = Mais fácil! 🎯

---

## 🐛 SOLUÇÃO DE PROBLEMAS

### Erro: google_credentials.json não encontrado

```
❌ Arquivo de credenciais não encontrado!
   Esperado: config/google_credentials.json
```

**Solução:**
1. Baixar JSON do Google Cloud Console
2. Renomear para: `google_credentials.json`
3. Mover para: `config/`

---

### Erro: "Google não verificou este app"

**É normal!** App é de uso pessoal.

**Clicar:**
1. "Avançado"
2. "Acessar Automaia Bot (não seguro)"

---

### Erro: Token expirado

```
⚠️ Erro ao renovar: Token has been expired or revoked
```

**Solução:**
```bash
# Deletar token antigo
rm config/google_token.pickle

# Autenticar novamente
python3 componentes/escalonamento/autenticar_google.py
```

---

### Navegador não abre

**Solução manual:**

1. Script vai mostrar URL:
   ```
   Please visit this URL to authorize:
   https://accounts.google.com/o/oauth2/auth?...
   ```

2. Copiar URL
3. Abrir no navegador manualmente
4. Seguir passos de autorização

---

## 📱 PLANILHA NO SEU DRIVE

**Onde fica:**
- ✅ Seu Google Drive (raiz)
- ✅ Aparece na sua lista de planilhas
- ✅ Você é o dono

**Vantagens:**
- ✅ Fácil encontrar
- ✅ Já compartilhada com você
- ✅ Controle total

---

## 🔐 SEGURANÇA

### O que o app pode fazer?

OAuth concede permissões para:
- ✅ Ver e criar planilhas
- ✅ Ver e criar arquivos Drive
- ❌ NÃO pode ver emails
- ❌ NÃO pode ver outras coisas

### Revogar acesso (se quiser)

1. Acesse: https://myaccount.google.com/permissions
2. Encontrar: "Automaia Bot"
3. Clicar: "Remover acesso"

---

## 📚 ARQUIVOS CRIADOS

Após autenticar:
```
config/
├── google_credentials.json    (credenciais OAuth - mantém)
└── google_token.pickle         (token salvo - renova automático)
```

**NÃO commitar no git!** (já está no .gitignore)

---

## 🎯 RESUMO RÁPIDO

```bash
# 1. Instalar (só 1x)
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client

# 2. Obter credenciais (2 min)
# - Google Cloud Console
# - Criar OAuth Client ID
# - Baixar e salvar: config/google_credentials.json

# 3. Autenticar (1 min)
python3 componentes/escalonamento/autenticar_google.py
# → Login + Clica "Autorizar"

# 4. Criar planilha (30s)
python3 componentes/escalonamento/criar_agenda_publica_oauth.py

# 5. Usar no bot
./PARAR_BOT_AUTOMAIA.sh
./INICIAR_COM_NGROK.sh
```

**Total:** 3-5 minutos ✅

---

## 💡 DICA FINAL

**Para testes rápidos:** Use OAuth (este método)

**Para produção:** Use Service Account
- Ver: `CRIACAO_AUTOMATICA.md`
- Mais robusto para servidores

---

**✅ MÉTODO MAIS FÁCIL DO MUNDO!** 🎉
