# ⚙️ Configuração de Webhooks Instagram - Guia Completo

## 🎯 Resposta Rápida: Configuração Via API?

### ❌ NÃO: Configurar Callback URL
**A URL do webhook NÃO pode ser configurada via API.** Isso deve ser feito manualmente no Meta App Dashboard.

### ✅ SIM: Subscrever Eventos
**Após configurar a URL manualmente, você PODE subscrever eventos via API** usando o endpoint `subscribed_apps`.

---

## 📋 PROCESSO COMPLETO (Híbrido Manual + API)

```
┌─────────────────────────────────────────────────────────────┐
│  ETAPA 1: MANUAL (Meta App Dashboard)                      │
├─────────────────────────────────────────────────────────────┤
│  1. Configurar Callback URL                                 │
│  2. Configurar Verify Token                                 │
│  3. Validar endpoint (GET request)                          │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  ETAPA 2: AUTOMÁTICA (Graph API)                           │
├─────────────────────────────────────────────────────────────┤
│  1. Subscrever eventos via API                              │
│  2. Configurar campos específicos                           │
│  3. Gerenciar subscrições                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 ETAPA 1: CONFIGURAÇÃO MANUAL (Dashboard)

### 1.1. Acessar Dashboard

1. Acesse: https://developers.facebook.com/apps/
2. Selecione seu App (ou crie novo)
3. No menu lateral: **Produtos** → **Webhooks**
4. Clique em **Editar subscrição** (ou Adicionar subscrição)

### 1.2. Configurar Callback URL

**Campos obrigatórios:**

| Campo | Valor | Exemplo |
|-------|-------|---------|
| **Callback URL** | Sua URL HTTPS pública | `https://seu-dominio.com/webhooks/instagram` |
| **Verify Token** | Token secreto (você define) | `meu_token_secreto_123` |

**Requisitos da URL:**
- ✅ HTTPS obrigatório
- ✅ Porta 443 (padrão HTTPS)
- ✅ Certificado SSL válido
- ✅ Responder em < 20 segundos
- ❌ Localhost NÃO funciona (use ngrok para testes)

### 1.3. Implementar Validação (GET Request)

**O que acontece:** Instagram envia GET request para validar sua URL.

**Código Python (Flask):**

```python
from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "meu_token_secreto_123"  # Mesmo do dashboard

@app.route('/webhooks/instagram', methods=['GET'])
def verify_webhook():
    """
    Instagram envia:
    GET /webhooks/instagram?hub.mode=subscribe&hub.verify_token=XXX&hub.challenge=YYY
    """
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == 'subscribe' and token == VERIFY_TOKEN:
        # Retorna o challenge para validar
        print("✅ Webhook validado com sucesso!")
        return challenge, 200
    else:
        print("❌ Erro na validação do webhook")
        return 'Erro na validação', 403
```

**Teste com ngrok (desenvolvimento local):**

```bash
# Terminal 1: Iniciar Flask
python3 webhook_server.py

# Terminal 2: Iniciar ngrok
ngrok http 5000

# Use a URL do ngrok no dashboard
# Exemplo: https://abc123.ngrok.io/webhooks/instagram
```

### 1.4. Validar no Dashboard

1. Cole a URL no campo **Callback URL**
2. Cole o token no campo **Verify Token**
3. Clique em **Verificar e salvar**
4. ✅ Se tudo certo: "URL verificada com sucesso"
5. ❌ Se erro: Verifique logs do servidor

---

## ✅ ETAPA 2: SUBSCRIÇÃO VIA API (Automático)

### 2.1. Subscrever Instagram Account a Eventos

**Endpoint:** `POST /{instagram-business-account-id}/subscribed_apps`

**Parâmetros:**

```bash
curl -X POST "https://graph.facebook.com/v18.0/{instagram-business-account-id}/subscribed_apps" \
  -d "subscribed_fields=messages,comments,mentions,messaging_postbacks,messaging_handover" \
  -d "access_token={your-page-access-token}"
```

**Campos disponíveis (subscribed_fields):**

- `messages` - Mensagens diretas
- `comments` - Comentários em posts
- `live_comments` - Comentários em lives
- `mentions` - Menções (@seu_usuario)
- `messaging_postbacks` - Cliques em botões
- `messaging_handover` - Transferência bot/humano
- `message_reactions` - Reações em mensagens
- `messaging_seen` - Status de leitura
- `story_insights` - Métricas de stories

**Exemplo Python:**

```python
import requests

def subscribe_instagram_webhooks(ig_account_id, page_access_token):
    """
    Subscreve Instagram Account para receber webhooks
    """
    url = f"https://graph.facebook.com/v18.0/{ig_account_id}/subscribed_apps"

    # Eventos que você quer receber
    fields = [
        'messages',
        'comments',
        'mentions',
        'messaging_postbacks',
        'messaging_handover'
    ]

    params = {
        'subscribed_fields': ','.join(fields),
        'access_token': page_access_token
    }

    response = requests.post(url, params=params)

    if response.status_code == 200:
        print("✅ Subscrição criada com sucesso!")
        return response.json()
    else:
        print(f"❌ Erro: {response.status_code}")
        print(response.json())
        return None

# Uso
ig_account_id = "123456789"  # Seu Instagram Business Account ID
page_token = "EAAxxxxx..."   # Seu Page Access Token

subscribe_instagram_webhooks(ig_account_id, page_token)
```

### 2.2. Verificar Subscrições Ativas

**Endpoint:** `GET /{instagram-business-account-id}/subscribed_apps`

```python
def get_active_subscriptions(ig_account_id, page_access_token):
    """
    Lista eventos subscritos atualmente
    """
    url = f"https://graph.facebook.com/v18.0/{ig_account_id}/subscribed_apps"

    params = {
        'access_token': page_access_token
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'data' in data:
        subscriptions = data['data'][0].get('subscribed_fields', [])
        print(f"✅ Eventos subscritos: {subscriptions}")
        return subscriptions
    else:
        print("❌ Nenhuma subscrição ativa")
        return []

# Uso
get_active_subscriptions(ig_account_id, page_token)
```

### 2.3. Atualizar Subscrições

**Para adicionar novos eventos:**

```python
def update_subscriptions(ig_account_id, page_access_token, new_fields):
    """
    Atualiza eventos subscritos (substitui os anteriores)
    """
    url = f"https://graph.facebook.com/v18.0/{ig_account_id}/subscribed_apps"

    params = {
        'subscribed_fields': ','.join(new_fields),
        'access_token': page_access_token
    }

    response = requests.post(url, params=params)
    return response.json()

# Adicionar story_insights aos eventos existentes
current_fields = get_active_subscriptions(ig_account_id, page_token)
new_fields = current_fields + ['story_insights']
update_subscriptions(ig_account_id, page_token, new_fields)
```

### 2.4. Remover Subscrições

**Endpoint:** `DELETE /{instagram-business-account-id}/subscribed_apps`

```python
def unsubscribe_webhooks(ig_account_id, page_access_token):
    """
    Remove TODAS as subscrições de webhook
    """
    url = f"https://graph.facebook.com/v18.0/{ig_account_id}/subscribed_apps"

    params = {
        'access_token': page_access_token
    }

    response = requests.delete(url, params=params)

    if response.status_code == 200:
        print("✅ Subscrições removidas")
        return True
    else:
        print(f"❌ Erro: {response.json()}")
        return False
```

---

## 🔑 OBTENDO TOKENS NECESSÁRIOS

### Page Access Token (Necessário para API)

**Método 1: Via Graph API Explorer**

1. Acesse: https://developers.facebook.com/tools/explorer/
2. Selecione seu App
3. Selecione **User Token** → Clique em **Get Token**
4. Selecione a página do Instagram conectada
5. Copie o token gerado

**Método 2: Via API**

```python
def get_page_access_token(user_access_token, page_id):
    """
    Obtém Page Access Token a partir de User Token
    """
    url = f"https://graph.facebook.com/v18.0/{page_id}"

    params = {
        'fields': 'access_token',
        'access_token': user_access_token
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'access_token' in data:
        return data['access_token']
    else:
        print(f"Erro: {data}")
        return None
```

### Instagram Business Account ID

**Método 1: Via Graph API Explorer**

```bash
GET /me/accounts?fields=instagram_business_account
```

**Método 2: Via API**

```python
def get_instagram_account_id(page_id, page_access_token):
    """
    Obtém Instagram Business Account ID da página
    """
    url = f"https://graph.facebook.com/v18.0/{page_id}"

    params = {
        'fields': 'instagram_business_account',
        'access_token': page_access_token
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'instagram_business_account' in data:
        ig_id = data['instagram_business_account']['id']
        print(f"✅ Instagram Account ID: {ig_id}")
        return ig_id
    else:
        print("❌ Nenhuma conta Instagram conectada")
        return None
```

---

## 🚀 SCRIPT COMPLETO DE CONFIGURAÇÃO

```python
#!/usr/bin/env python3
"""
Script para configurar webhooks do Instagram automaticamente
Pré-requisito: Callback URL já configurada manualmente no dashboard
"""

import requests
import sys

class InstagramWebhookConfig:
    def __init__(self, page_access_token):
        self.page_token = page_access_token
        self.base_url = "https://graph.facebook.com/v18.0"

    def get_instagram_account_id(self, page_id):
        """Obtém Instagram Business Account ID"""
        url = f"{self.base_url}/{page_id}"
        params = {
            'fields': 'instagram_business_account',
            'access_token': self.page_token
        }
        response = requests.get(url, params=params)
        data = response.json()

        if 'instagram_business_account' in data:
            return data['instagram_business_account']['id']
        else:
            raise Exception(f"Instagram account não encontrado: {data}")

    def subscribe_webhooks(self, ig_account_id, events):
        """Subscreve eventos de webhook"""
        url = f"{self.base_url}/{ig_account_id}/subscribed_apps"
        params = {
            'subscribed_fields': ','.join(events),
            'access_token': self.page_token
        }
        response = requests.post(url, params=params)

        if response.status_code == 200:
            print(f"✅ Subscrição criada: {events}")
            return True
        else:
            raise Exception(f"Erro na subscrição: {response.json()}")

    def get_subscriptions(self, ig_account_id):
        """Lista subscrições ativas"""
        url = f"{self.base_url}/{ig_account_id}/subscribed_apps"
        params = {'access_token': self.page_token}
        response = requests.get(url, params=params)
        data = response.json()

        if 'data' in data and len(data['data']) > 0:
            return data['data'][0].get('subscribed_fields', [])
        return []

    def setup_complete(self, page_id):
        """Configuração completa"""
        print("🚀 Iniciando configuração de webhooks...")

        # 1. Obter Instagram Account ID
        print("\n1️⃣ Obtendo Instagram Account ID...")
        ig_id = self.get_instagram_account_id(page_id)
        print(f"   ✅ Instagram ID: {ig_id}")

        # 2. Subscrever eventos principais
        print("\n2️⃣ Subscrevendo eventos...")
        events = [
            'messages',
            'comments',
            'mentions',
            'messaging_postbacks',
            'messaging_handover'
        ]
        self.subscribe_webhooks(ig_id, events)

        # 3. Verificar subscrições
        print("\n3️⃣ Verificando subscrições...")
        active = self.get_subscriptions(ig_id)
        print(f"   ✅ Eventos ativos: {active}")

        print("\n✅ Configuração concluída com sucesso!")
        return ig_id, active

if __name__ == "__main__":
    # Configurações
    PAGE_ACCESS_TOKEN = "EAAxxxxx..."  # Seu token
    PAGE_ID = "123456789"              # ID da página Facebook conectada

    # Executar setup
    config = InstagramWebhookConfig(PAGE_ACCESS_TOKEN)
    ig_id, events = config.setup_complete(PAGE_ID)

    print(f"\n📋 RESUMO:")
    print(f"   Instagram Account ID: {ig_id}")
    print(f"   Eventos subscritos: {', '.join(events)}")
```

---

## ⚠️ LIMITAÇÕES DA API

### ❌ O que NÃO pode ser feito via API:

1. **Configurar Callback URL** (deve ser manual no dashboard)
2. **Configurar Verify Token** (deve ser manual no dashboard)
3. **Validação inicial** (seu servidor deve responder ao GET)
4. **Adicionar produto Webhooks ao app** (deve ser manual)

### ✅ O que PODE ser feito via API:

1. **Subscrever/dessubscrever eventos**
2. **Atualizar campos subscritos**
3. **Listar subscrições ativas**
4. **Gerenciar múltiplas páginas/contas**

---

## 🔍 DEBUGGING E TESTES

### Ferramenta Oficial: Webhooks Tester

1. Acesse: https://developers.facebook.com/tools/webhooks/
2. Selecione seu App
3. Selecione objeto: **Instagram**
4. Escolha evento: **messages**, **comments**, etc
5. Clique em **Enviar para meu servidor**
6. Verifique logs do seu servidor

### Teste de Validação (GET)

```bash
# Simular validação do Instagram
curl "https://seu-dominio.com/webhooks/instagram?hub.mode=subscribe&hub.verify_token=meu_token_secreto_123&hub.challenge=teste123"

# Resposta esperada:
# teste123
```

### Teste de Webhook (POST)

```bash
# Simular webhook de mensagem
curl -X POST "https://seu-dominio.com/webhooks/instagram" \
  -H "Content-Type: application/json" \
  -d '{
    "object": "instagram",
    "entry": [{
      "id": "123",
      "time": 1234567890,
      "messaging": [{
        "sender": {"id": "456"},
        "recipient": {"id": "789"},
        "timestamp": 1234567890000,
        "message": {
          "mid": "msg_123",
          "text": "Teste"
        }
      }]
    }]
  }'
```

---

## 📊 CHECKLIST DE CONFIGURAÇÃO

### Pré-configuração (Manual)
- [ ] App criado no Meta for Developers
- [ ] Instagram Business Account conectado à página Facebook
- [ ] Produto "Webhooks" adicionado ao app
- [ ] Permissões solicitadas (`instagram_manage_messages`, `instagram_manage_comments`)

### Configuração Manual (Dashboard)
- [ ] Callback URL configurada (HTTPS)
- [ ] Verify Token configurado
- [ ] Endpoint respondendo a GET request (validação)
- [ ] Webhook validado com sucesso no dashboard

### Configuração API (Automático)
- [ ] Page Access Token obtido
- [ ] Instagram Business Account ID obtido
- [ ] Eventos subscritos via API (`subscribed_apps`)
- [ ] Subscrições verificadas e ativas

### Testes
- [ ] Webhook Tester (Meta Developer Tools)
- [ ] Mensagem de teste real (DM no Instagram)
- [ ] Comentário de teste real (em post)
- [ ] Logs verificados (webhooks recebidos)

---

## 🎯 RESUMO: PROCESSO IDEAL

```
1. MANUAL (uma vez):
   └─> Dashboard: Configurar URL + Verify Token

2. AUTOMÁTICO (repetível):
   └─> API: Subscrever eventos programaticamente

3. TESTE:
   └─> Webhook Tester + eventos reais

4. PRODUÇÃO:
   └─> Monitorar logs + métricas
```

---

**Última atualização:** 06/11/2025
**Documentação relacionada:** [DOCUMENTACAO-COMPLETA.md](./DOCUMENTACAO-COMPLETA.md)
