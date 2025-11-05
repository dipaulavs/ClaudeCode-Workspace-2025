# 🚀 Guia Completo de Setup das APIs - chatbot-template/

## Status Atual de Segurança

| Componente | Status | Prioridade |
|------------|--------|-----------|
| Chatwoot + Evolution | ✅ JSON seguro | ✓ Feito |
| OpenAI + OpenRouter | 🔴 Hardcoded | 🔴 URGENTE |
| Redis Upstash | 🔴 Hardcoded (2 locais) | 🔴 URGENTE |
| Google OAuth | ✅ JSON seguro | ✓ Feito |

---

## 1. Validar Configuração Atual

```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/chatbot-template

# Executar validador
python3 validar_configuracao.py

# Resultado esperado:
# 🟢 STATUS: OK - Tudo configurado! (ou)
# 🟡 STATUS: AVISO - Alguns itens opcionais não configurados
# 🔴 STATUS: FALHA - Configure os itens com ❌ acima
```

---

## 2. Configurar Chatwoot + Evolution

**Arquivo:** `chatwoot_config_automaia.json`

### 2.1 Obter Chatwoot Config

1. Acesse seu Chatwoot: https://chatwoot.seu-dominio.com
2. Vá para: **Settings → API → API Access Tokens**
3. Copie o token (ou crie um novo)
4. Vá para: **Settings → Inboxes** e anote o ID da inbox
5. Vá para: **Settings → Account** e anote o ID da conta

```json
{
  "chatwoot": {
    "url": "https://chatwoot.seu-dominio.com",
    "token": "COPIE_AQUI_O_TOKEN",
    "account_id": "ID_DA_CONTA",
    "inbox_id": "ID_DA_INBOX"
  },
```

### 2.2 Obter Evolution API Config

1. Acesse Evolution API: https://evolution.seu-dominio.com
2. Vá para: **Settings → API Keys**
3. Copie a API Key
4. Anote a URL base
5. Anote o nome da instância WhatsApp

```json
  "evolution": {
    "url": "https://evolution.seu-dominio.com",
    "api_key": "API_KEY_AQUI",
    "instance": "nome-da-instancia"
  }
}
```

### 2.3 Gerar QR Code da Instância

```bash
# Gerar QR code para conectar WhatsApp
python3 gerar_qrcode.py

# Escanear com WhatsApp do seu telefone
# Aguardar "Instância conectada"
```

### ✅ Validar

```bash
python3 validar_configuracao.py
# Deve mostrar ✅ para todos os campos Chatwoot e Evolution
```

---

## 3. Configurar OpenAI e OpenRouter (HARDCODED - Perigoso!)

**Arquivos:**
- `chatbot_automaia_v4.py` linhas 40-41

⚠️ **AVISO CRÍTICO**: Essas chaves estão HARDCODED no código!
Nunca commitar com chaves reais em repositório público.

### 3.1 Obter OpenAI API Key

1. Acesse: https://platform.openai.com/api-keys
2. Clique: **Create new secret key**
3. Copie a chave (começa com `sk-proj-`)
4. Ative o modelo **GPT-4 Vision** para análise de imagens
5. Ative **Whisper API** para transcrição

### 3.2 Obter OpenRouter API Key

1. Acesse: https://openrouter.ai/keys
2. Clique: **Create New Key**
3. Copie a chave (começa com `sk-or-v1-`)
4. Define limite de quota se desejar

### 3.3 Atualizar (TEMPORÁRIO - Para desenvolvimento apenas)

```python
# Arquivo: chatbot_automaia_v4.py (APENAS PARA TESTES)
OPENROUTER_API_KEY = "sk-or-v1-COLE_AQUI"
OPENAI_API_KEY = "sk-proj-COLE_AQUI"
```

### ⚠️ Alternativa Segura: Usar .env

```bash
# 1. Copiar template
cp .env.example .env

# 2. Editar .env
nano .env
# OPENAI_API_KEY=sk-proj-...
# OPENROUTER_API_KEY=sk-or-v1-...

# 3. Instalar python-dotenv
pip install python-dotenv

# 4. Modificar chatbot_automaia_v4.py para usar:
# from dotenv import load_dotenv
# load_dotenv()
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
```

---

## 4. Configurar Redis Upstash (HARDCODED - Perigoso!)

**Arquivos:**
- `chatbot_automaia_v4.py` linhas 56-57
- `componentes/followup/sistema_followup.py` linhas 16-22

⚠️ **AVISO**: Redis credentials estão HARDCODED em 2 lugares!

### 4.1 Criar Banco Redis Upstash

1. Acesse: https://console.upstash.com
2. Clique: **Create Database**
3. Escolha: **Redis** (não Kafka)
4. Nome: `chatbot-cache`
5. Região: Próxima a você
6. Clique: **Create**

### 4.2 Obter Credenciais

1. Na página do banco: **Details**
2. Copie: **REST API URL**
3. Copie: **REST API Token**

Formato:
```
https://default:TOKEN@HOST:PORT
```

### 4.3 Atualizar (TEMPORÁRIO - Para testes)

**chatbot_automaia_v4.py (linhas 56-57):**
```python
redis = Redis(
    url="https://default:TOKEN@HOST.upstash.io",
    token="TOKEN"
)
```

**componentes/followup/sistema_followup.py (linhas 16-22):**
```python
REDIS_HOST = "HOST.upstash.io"
REDIS_PORT = 42128
REDIS_PASSWORD = "TOKEN"
```

### ⚠️ Alternativa Segura: Usar .env

```bash
# .env
REDIS_URL=https://default:TOKEN@HOST:PORT
# ou
REDIS_HOST=HOST.upstash.io
REDIS_PORT=42128
REDIS_PASSWORD=TOKEN
```

Depois modificar código Python para usar `os.getenv()`.

---

## 5. Configurar Google Sheets (OPCIONAL)

Se quer agendar visitas com agenda real (não MOCK):

### 5.1 Obter Google Sheet ID

1. Abra: https://sheets.google.com
2. Crie uma nova planilha (ou use existente)
3. Copie o ID da URL:
   ```
   https://docs.google.com/spreadsheets/d/ESTE-E-O-ID/edit
   ```
4. Atualize `chatwoot_config_automaia.json`:
   ```json
   "google_sheet_id": "COLE_ID_AQUI"
   ```

### 5.2 Autenticar com Google

```bash
cd componentes/escalonamento

# Executar autenticação
python3 autenticar_google.py

# 1. Abrirá navegador
# 2. Login com sua conta Google
# 3. Autorize acesso a Sheets
# 4. Token salvo em: config/google_token.pickle
```

### 5.3 Configurar Planilha

Formato esperado da planilha:

| Data | Hora | Vendedor | Status |
|------|------|----------|--------|
| 2025-11-10 | 10:00 | João | Disponível |
| 2025-11-10 | 14:00 | Maria | Disponível |

---

## 6. Estrutura Final de Arquivos

Após tudo configurado:

```
chatbot-template/
├── chatwoot_config_automaia.json      ✅ Preenchido
├── .env                               ✅ Com todas as chaves (não commitado!)
├── .env.example                       ✅ Template para outros devs
├── chatbot_automaia_v4.py             ⚠️  Com hardcoded (remover em prod)
├── gerar_qrcode.py                    ✅ Pronto para usar
├── validar_configuracao.py            ✅ Executado e OK
├── SETUP_APIS.md                      📄 Este arquivo
├── config/
│   └── google_token.pickle            ✅ Token Google (ignorado no Git)
├── componentes/
│   ├── escalonamento/
│   │   ├── config/
│   │   │   └── google_credentials.json ✅ Credenciais Google
│   │   └── autenticar_google.py       ✅ Script de auth
│   ├── followup/
│   │   └── sistema_followup.py        ⚠️  Com hardcoded
│   └── ...
└── carros/                             ✅ Com produtos
```

---

## 7. Checklist de Setup Completo

### Pré-requisitos
- [ ] Python 3.8+
- [ ] pip instalado
- [ ] Git (para versionar, sem .env!)
- [ ] Conta Chatwoot ativa
- [ ] Conta Evolution API ativa
- [ ] Conta OpenAI ativa
- [ ] Conta OpenRouter ativa
- [ ] Conta Upstash ativa
- [ ] (Opcional) Conta Google ativa

### Fase 1: Configuração Básica
- [ ] Copiar `.env.example` para `.env`
- [ ] Preencher `chatwoot_config_automaia.json`
  - [ ] `chatwoot.url`
  - [ ] `chatwoot.token`
  - [ ] `chatwoot.account_id`
  - [ ] `chatwoot.inbox_id`
  - [ ] `evolution.url`
  - [ ] `evolution.api_key`
  - [ ] `evolution.instance`
- [ ] Executar `python3 gerar_qrcode.py`
- [ ] Escanear QR code com WhatsApp

### Fase 2: IA e Cache
- [ ] Preencher OPENAI_API_KEY em `.env`
- [ ] Preencher OPENROUTER_API_KEY em `.env`
- [ ] Preencher Redis credentials em `.env`
- [ ] Testar conexão Redis

### Fase 3: Agendamento (Opcional)
- [ ] Criar planilha Google Sheets
- [ ] Preencher `google_sheet_id` em `chatwoot_config_automaia.json`
- [ ] Executar `python3 autenticar_google.py`
- [ ] Escanear QR code de autenticação

### Fase 4: Validação
- [ ] Executar `python3 validar_configuracao.py`
- [ ] Resultado: 🟢 STATUS: OK ou 🟡 STATUS: AVISO (aceitável)
- [ ] Adicionar `.env` ao `.gitignore`
- [ ] Adicionar `google_token.pickle` ao `.gitignore`

### Fase 5: Teste Final
- [ ] Iniciar bot: `python3 chatbot_automaia_v4.py`
- [ ] Enviar mensagem WhatsApp
- [ ] Verificar resposta no Chatwoot
- [ ] Enviar áudio (testa Whisper)
- [ ] Enviar foto (testa GPT-4 Vision)

---

## 8. Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'dotenv'"
```bash
pip install python-dotenv
```

### Erro: "Chatwoot token invalid"
```bash
# Verificar token em:
# Chatwoot → Settings → Integrations → API
# Token deve começar com letras/números aleatórios

# Regenerar se necessário:
# Chatwoot → Settings → API Access Tokens → Regenerate
```

### Erro: "Evolution API unreachable"
```bash
# Verificar URL em chatwoot_config_automaia.json
# Testar manualmente: curl https://evolution.seu-dominio.com
# Verificar firewall/CORS
```

### Erro: "Redis connection timeout"
```bash
# Verificar URL em .env
# Formato correto: https://default:TOKEN@HOST:PORT
# Teste de conexão:
python3 -c "from upstash_redis import Redis; r = Redis.from_url('sua-url'); print(r.ping())"
```

### Erro: "Google authentication failed"
```bash
# Regenerar credenciais:
python3 componentes/escalonamento/autenticar_google.py

# Ou deletar token antigo:
rm config/google_token.pickle
# Depois tentar novamente
```

### Erro: "OpenAI rate limit exceeded"
```bash
# Verificar uso em: https://platform.openai.com/account/billing/overview
# Aumentar limite em: https://platform.openai.com/account/billing/limits
# Ou usar OpenRouter como fallback
```

---

## 9. Verificação de Segurança Final

```bash
# 1. Verificar se .env está no .gitignore
grep -i ".env" .gitignore
# Resultado esperado: .env (listado)

# 2. Verificar se google_token.pickle está ignorado
grep -i "pickle\|google_token" .gitignore
# Resultado esperado: *.pickle ou google_token.pickle

# 3. Verificar se há credenciais no código
grep -r "sk-proj-\|sk-or-v1-" --include="*.py" .
# Resultado esperado: (nada - apenas em .env)

# 4. Validar novamente
python3 validar_configuracao.py
# Resultado esperado: 🟢 ou 🟡
```

---

## 10. Próximos Passos

### Curto Prazo (1-2 dias)
1. ✅ Completar checklist de setup acima
2. ✅ Executar validador
3. ✅ Testar fluxo básico (receber/enviar mensagens)

### Médio Prazo (1-2 semanas)
1. Remover hardcoded keys do código Python
2. Implementar carregamento via `python-dotenv`
3. Adicionar validação de variáveis obrigatórias
4. Criar script de setup automático

### Longo Prazo (1 mês+)
1. Usar AWS Secrets Manager ou similiar para prod
2. Implementar rotação automática de chaves
3. Adicionar logs de auditoria
4. Documentar política de segurança

---

## 📞 Suporte

Se encontrar problemas:

1. Executar validador: `python3 validar_configuracao.py`
2. Verificar logs: `tail -f logs/chatbot.log`
3. Consultar seção Troubleshooting acima
4. Abrir issue no repositório com logs

**Última atualização:** 2025-11-05
**Versão:** 1.0
