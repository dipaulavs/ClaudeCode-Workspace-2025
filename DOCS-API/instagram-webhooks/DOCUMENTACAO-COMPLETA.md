# 📘 Documentação Completa: Instagram Webhooks API

**Fonte:** Meta for Developers - Instagram Platform
**URL:** https://developers.facebook.com/docs/graph-api/webhooks/reference/instagram
**Data de extração:** 06/11/2025
**Versão da API:** Graph API (atual)

---

## 📚 ÍNDICE

1. [Visão Geral](#visão-geral)
2. [Configuração Inicial](#configuração-inicial)
3. [Eventos Disponíveis](#eventos-disponíveis)
4. [Estruturas de Dados](#estruturas-de-dados)
5. [Exemplos de Payloads](#exemplos-de-payloads)
6. [Fluxo de Implementação](#fluxo-de-implementação)

---

## 🎯 VISÃO GERAL

### O que são Instagram Webhooks?

Webhooks do Instagram são notificações em tempo real enviadas pelo Instagram para seu servidor quando eventos específicos ocorrem (mensagens, comentários, menções, etc).

### Como Funcionam

```
┌─────────────────┐
│  Usuário age    │
│  (mensagem,     │
│   comentário)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Instagram      │
│  detecta evento │
└────────┬────────┘
         │
         ▼ (POST HTTP)
┌─────────────────┐
│  Seu Webhook    │ ← Você recebe payload JSON
│  (sua URL)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Você processa  │
│  e responde     │
└─────────────────┘
```

---

## ⚙️ CONFIGURAÇÃO INICIAL

### 1. Pré-requisitos

- App criado no Meta for Developers
- Instagram Business Account ou Creator Account
- Servidor HTTPS público (webhook URL)
- Permissões necessárias:
  - `instagram_manage_messages` (para mensagens)
  - `instagram_manage_comments` (para comentários)

### 2. Configurar Webhook URL

**Local:** Meta App Dashboard > Produtos > Webhooks

**Campos obrigatórios:**
- **Callback URL:** `https://seu-dominio.com/webhooks/instagram`
- **Verify Token:** Token secreto (você define)

**Validação inicial (GET request):**
```python
# Instagram envia GET para validar sua URL
def validate_webhook(request):
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == 'subscribe' and token == SEU_VERIFY_TOKEN:
        return challenge, 200
    return 'Erro', 403
```

### 3. Subscrever Eventos

**Eventos disponíveis para subscrição:**
- `messages` - Mensagens diretas
- `comments` - Comentários em posts
- `live_comments` - Comentários em lives
- `mentions` - Menções (@seu_usuario)
- `story_insights` - Métricas de stories
- `message_reactions` - Reações em mensagens
- `message_edit` - Edições de mensagens
- `messaging_seen` - Status de leitura
- `messaging_postbacks` - Respostas de botões
- `messaging_referral` - Referências de origem
- `messaging_handover` - Transferência de controle

---

## 📡 EVENTOS DISPONÍVEIS

### 1. **messages** (PRIORIDADE ALTA)

**Quando dispara:** Alguém envia mensagem direta para seu perfil

**Estrutura do Payload:**

```json
{
  "object": "instagram",
  "entry": [
    {
      "id": "INSTAGRAM_BUSINESS_ACCOUNT_ID",
      "time": 1692048000,
      "messaging": [
        {
          "sender": {
            "id": "USER_INSTAGRAM_SCOPED_ID"
          },
          "recipient": {
            "id": "YOUR_INSTAGRAM_SCOPED_ID"
          },
          "timestamp": 1692048000000,
          "message": {
            "mid": "MESSAGE_ID",
            "text": "Olá! Quanto custa?",
            "attachments": [
              {
                "type": "image",
                "payload": {
                  "url": "https://..."
                }
              }
            ],
            "reply_to": {
              "story": {
                "url": "STORY_URL",
                "id": "STORY_ID"
              }
            }
          }
        }
      ]
    }
  ]
}
```

**Campos importantes:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `sender.id` | string | ID do remetente (Instagram-scoped) |
| `recipient.id` | string | ID do destinatário (você) |
| `timestamp` | integer | Timestamp em milissegundos |
| `message.mid` | string | ID único da mensagem |
| `message.text` | string | Texto da mensagem |
| `message.attachments` | array | Fotos, vídeos, etc |
| `message.reply_to` | object | Se é resposta a story/mensagem |

**Tipos de attachments:**
- `image` - Fotos
- `video` - Vídeos
- `audio` - Áudios
- `file` - Arquivos
- `template` - Templates de resposta rápida

---

### 2. **comments** (PRIORIDADE ALTA)

**Quando dispara:** Alguém comenta em seu post

**Estrutura do Payload:**

```json
{
  "object": "instagram",
  "entry": [
    {
      "id": "INSTAGRAM_BUSINESS_ACCOUNT_ID",
      "time": 1692048000,
      "changes": [
        {
          "field": "comments",
          "value": {
            "from": {
              "id": "USER_INSTAGRAM_SCOPED_ID",
              "username": "joaosilva"
            },
            "media": {
              "id": "MEDIA_ID",
              "media_product_type": "FEED"
            },
            "id": "COMMENT_ID",
            "text": "Produto incrível! Onde compro?",
            "parent_id": null
          }
        }
      ]
    }
  ]
}
```

**Campos importantes:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `from.id` | string | ID do usuário que comentou |
| `from.username` | string | Username do usuário |
| `media.id` | string | ID do post comentado |
| `media.media_product_type` | string | Tipo: FEED, REELS, IGTV |
| `id` | string | ID do comentário |
| `text` | string | Texto do comentário |
| `parent_id` | string | Se for resposta a outro comentário |

**Tipos de media_product_type:**
- `FEED` - Post normal
- `REELS` - Reels
- `IGTV` - IGTV (descontinuado)
- `AD` - Anúncio

---

### 3. **live_comments** (PRIORIDADE MÉDIA)

**Quando dispara:** Comentário em live video

**Estrutura:** Idêntica a `comments`, mas em lives

---

### 4. **mentions** (PRIORIDADE MÉDIA)

**Quando dispara:** Alguém te @menciona em comentário ou caption

**Estrutura do Payload:**

```json
{
  "object": "instagram",
  "entry": [
    {
      "id": "INSTAGRAM_BUSINESS_ACCOUNT_ID",
      "time": 1692048000,
      "changes": [
        {
          "field": "mentions",
          "value": {
            "media_id": "MEDIA_ID_WHERE_MENTIONED",
            "comment_id": "COMMENT_ID_WITH_MENTION"
          }
        }
      ]
    }
  ]
}
```

**Nota:** Você precisa fazer request adicional na Graph API para obter detalhes do comentário/caption.

---

### 5. **message_reactions** (PRIORIDADE BAIXA)

**Quando dispara:** Alguém reage a uma mensagem com emoji

**Estrutura do Payload:**

```json
{
  "object": "instagram",
  "entry": [
    {
      "id": "INSTAGRAM_BUSINESS_ACCOUNT_ID",
      "time": 1692048000,
      "messaging": [
        {
          "sender": {
            "id": "USER_ID"
          },
          "recipient": {
            "id": "YOUR_ID"
          },
          "timestamp": 1692048000000,
          "reaction": {
            "mid": "MESSAGE_ID_REACTED_TO",
            "action": "react",
            "reaction": "love",
            "emoji": "❤️"
          }
        }
      ]
    }
  ]
}
```

**Valores de `action`:**
- `react` - Adicionou reação
- `unreact` - Removeu reação

**Valores de `reaction`:**
- `love` - ❤️
- `wow` - 😮
- `haha` - 😂
- `sad` - 😢
- `angry` - 😠
- `like` - 👍

---

### 6. **messaging_seen** (PRIORIDADE BAIXA)

**Quando dispara:** Alguém visualizou sua mensagem

**Estrutura do Payload:**

```json
{
  "object": "instagram",
  "entry": [
    {
      "id": "INSTAGRAM_BUSINESS_ACCOUNT_ID",
      "time": 1692048000,
      "messaging": [
        {
          "sender": {
            "id": "USER_ID"
          },
          "recipient": {
            "id": "YOUR_ID"
          },
          "timestamp": 1692048000000,
          "read": {
            "mid": "MESSAGE_ID_READ"
          }
        }
      ]
    }
  ]
}
```

---

### 7. **story_insights** (PRIORIDADE BAIXA)

**Quando dispara:** Story expira (24h depois)

**Estrutura do Payload:**

```json
{
  "object": "instagram",
  "entry": [
    {
      "id": "INSTAGRAM_BUSINESS_ACCOUNT_ID",
      "time": 1692048000,
      "changes": [
        {
          "field": "story_insights",
          "value": {
            "media_id": "STORY_MEDIA_ID",
            "impressions": 1523,
            "reach": 1200,
            "taps_forward": 45,
            "taps_back": 12,
            "exits": 8,
            "replies": 23
          }
        }
      ]
    }
  ]
}
```

**Nota:** Métricas com menos de 5 contagens retornam `-1` por privacidade.

---

### 8. **messaging_postbacks** (PRIORIDADE MÉDIA)

**Quando dispara:** Usuário clica em botão de resposta rápida

**Estrutura do Payload:**

```json
{
  "object": "instagram",
  "entry": [
    {
      "id": "INSTAGRAM_BUSINESS_ACCOUNT_ID",
      "time": 1692048000,
      "messaging": [
        {
          "sender": {
            "id": "USER_ID"
          },
          "recipient": {
            "id": "YOUR_ID"
          },
          "timestamp": 1692048000000,
          "postback": {
            "mid": "MESSAGE_ID",
            "title": "Ver Preços",
            "payload": "VIEW_PRICES_ACTION"
          }
        }
      ]
    }
  ]
}
```

---

### 9. **messaging_handover** (PRIORIDADE ALTA - BOT/HUMANO)

**Quando dispara:** Transferência de controle entre bot e humano

**Estrutura do Payload:**

```json
{
  "object": "instagram",
  "entry": [
    {
      "id": "INSTAGRAM_BUSINESS_ACCOUNT_ID",
      "time": 1692048000,
      "messaging": [
        {
          "sender": {
            "id": "USER_ID"
          },
          "recipient": {
            "id": "YOUR_ID"
          },
          "timestamp": 1692048000000,
          "pass_thread_control": {
            "previous_owner_app_id": "BOT_APP_ID",
            "new_owner_app_id": "INBOX_APP_ID",
            "metadata": "Cliente solicitou atendimento humano"
          }
        }
      ]
    }
  ]
}
```

**Tipos de handover:**
- `pass_thread_control` - Passar controle
- `take_thread_control` - Tomar controle
- `request_thread_control` - Solicitar controle

---

## 🏗️ ESTRUTURAS DE DADOS

### IDName

```json
{
  "id": "string" // Instagram-scoped ID
}
```

### IGCommentFromUser

```json
{
  "id": "numeric_string",
  "username": "string",
  "self_ig_scoped_id": "numeric_string"
}
```

### IGCommentMedia

```json
{
  "id": "numeric_string",
  "media_product_type": "string", // FEED, REELS, AD
  "ad_id": "numeric_string", // se for ad
  "ad_title": "string", // se for ad
  "original_media_id": "numeric_string"
}
```

### FBInstagramMessageAttachmentData

```json
{
  "type": "string", // image, video, audio, file, template
  "payload": {
    "url": "string",
    "ig_post_media_id": "numeric_string", // se for post
    "generic": {} // se for template
  }
}
```

---

## 🔄 FLUXO DE IMPLEMENTAÇÃO

### Fluxo Completo: Receber e Responder Mensagem

```
1. RECEBER WEBHOOK
   ├─> Validar signature (X-Hub-Signature-256)
   ├─> Parse JSON payload
   └─> Identificar evento (messages/comments)

2. PROCESSAR EVENTO
   ├─> Extrair sender_id
   ├─> Extrair conteúdo (text/attachments)
   ├─> Armazenar contexto (opcional)
   └─> Gerar resposta (IA/regras)

3. ENVIAR RESPOSTA
   ├─> POST para Graph API
   ├─> Endpoint: /{recipient_id}/messages
   └─> Payload com resposta

4. MONITORAR
   ├─> Log de webhooks
   ├─> Métricas de resposta
   └─> Tratamento de erros
```

### Exemplo de Código Python (Flask)

```python
import hashlib
import hmac
import json
from flask import Flask, request

app = Flask(__name__)

# Configuração
APP_SECRET = "seu_app_secret"
VERIFY_TOKEN = "seu_verify_token"
PAGE_ACCESS_TOKEN = "seu_page_access_token"

@app.route('/webhooks/instagram', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Validação inicial do webhook
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200
        return 'Erro', 403

    elif request.method == 'POST':
        # Validar signature
        signature = request.headers.get('X-Hub-Signature-256', '')
        expected_signature = 'sha256=' + hmac.new(
            APP_SECRET.encode(),
            request.data,
            hashlib.sha256
        ).hexdigest()

        if signature != expected_signature:
            return 'Assinatura inválida', 403

        # Processar payload
        data = request.json

        if data.get('object') == 'instagram':
            for entry in data.get('entry', []):
                # Processar mensagens
                if 'messaging' in entry:
                    for messaging_event in entry['messaging']:
                        if 'message' in messaging_event:
                            handle_message(messaging_event)

                # Processar comentários
                if 'changes' in entry:
                    for change in entry['changes']:
                        if change['field'] == 'comments':
                            handle_comment(change['value'])

        return 'OK', 200

def handle_message(event):
    sender_id = event['sender']['id']
    message_text = event.get('message', {}).get('text', '')

    print(f"Mensagem de {sender_id}: {message_text}")

    # Gerar resposta (aqui você colocaria sua lógica/IA)
    response_text = f"Recebi sua mensagem: {message_text}"

    # Enviar resposta via Graph API
    send_message(sender_id, response_text)

def handle_comment(comment_data):
    comment_id = comment_data['id']
    comment_text = comment_data['text']
    commenter_username = comment_data['from']['username']

    print(f"Comentário de @{commenter_username}: {comment_text}")

    # Responder comentário via Graph API
    reply_to_comment(comment_id, "Obrigado pelo comentário!")

def send_message(recipient_id, message_text):
    import requests

    url = f"https://graph.facebook.com/v18.0/me/messages"
    headers = {'Content-Type': 'application/json'}
    payload = {
        'recipient': {'id': recipient_id},
        'message': {'text': message_text},
        'access_token': PAGE_ACCESS_TOKEN
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def reply_to_comment(comment_id, reply_text):
    import requests

    url = f"https://graph.facebook.com/v18.0/{comment_id}/replies"
    params = {
        'message': reply_text,
        'access_token': PAGE_ACCESS_TOKEN
    }

    response = requests.post(url, params=params)
    return response.json()

if __name__ == '__main__':
    app.run(port=8080)
```

---

## 🔐 SEGURANÇA

### Validação de Signature

Todo webhook do Instagram inclui header `X-Hub-Signature-256` para validar autenticidade:

```python
def verify_webhook_signature(payload, signature):
    expected_signature = 'sha256=' + hmac.new(
        APP_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected_signature)
```

### HTTPS Obrigatório

- Webhook URL **DEVE** ser HTTPS
- Certificado SSL válido
- Porta 443 (padrão HTTPS)

---

## ⚠️ LIMITAÇÕES E BOAS PRÁTICAS

### Rate Limits

- **Webhooks recebidos:** Ilimitado
- **Envio de mensagens:**
  - Resposta a mensagem recebida: 24h para responder
  - Mensagem proativa: Requer Message Template aprovado

### Boas Práticas

1. **Responda rápido (< 20s):** Instagram espera resposta HTTP 200 em até 20 segundos
2. **Processe async:** Retorne 200 imediatamente, processe em background
3. **Trate duplicatas:** Mesma mensagem pode ser enviada 2x (use `mid` como idempotência)
4. **Log tudo:** Armazene payloads para debug
5. **Retry logic:** Implemente retry para chamadas à Graph API

### Exemplo de Processamento Assíncrono

```python
from threading import Thread

@app.route('/webhooks/instagram', methods=['POST'])
def webhook():
    data = request.json

    # Retorna 200 imediatamente
    Thread(target=process_webhook, args=(data,)).start()
    return 'OK', 200

def process_webhook(data):
    # Processa em background
    # Pode demorar quanto precisar
    pass
```

---

## 📊 TABELA RESUMO: EVENTOS

| Evento | Prioridade | Quando Dispara | Campo JSON | Use Case |
|--------|-----------|----------------|-----------|----------|
| **messages** | 🔴 Alta | Mensagem direta recebida | `messaging.message` | Chatbot, atendimento |
| **comments** | 🔴 Alta | Comentário em post | `changes.comments` | Moderação, resposta |
| **live_comments** | 🟡 Média | Comentário em live | `changes.live_comments` | Interação ao vivo |
| **mentions** | 🟡 Média | @mencionado | `changes.mentions` | Brand monitoring |
| **message_reactions** | 🟢 Baixa | Reação em mensagem | `messaging.reaction` | Analytics |
| **messaging_seen** | 🟢 Baixa | Mensagem lida | `messaging.read` | Status de leitura |
| **story_insights** | 🟢 Baixa | Story expira | `changes.story_insights` | Métricas |
| **messaging_postbacks** | 🟡 Média | Clique em botão | `messaging.postback` | Fluxos interativos |
| **messaging_handover** | 🔴 Alta | Bot ↔ Humano | `messaging.pass_thread_control` | Escalação |

---

## 🎓 RECURSOS ADICIONAIS

### Links Oficiais

- **Documentação completa:** https://developers.facebook.com/docs/graph-api/webhooks/reference/instagram
- **Graph API Explorer:** https://developers.facebook.com/tools/explorer/
- **Webhook Tester:** https://developers.facebook.com/tools/webhooks/
- **App Dashboard:** https://developers.facebook.com/apps/

### Ferramentas Úteis

- **ngrok:** Para testar webhooks localmente
- **RequestBin:** Para debug de payloads
- **Postman:** Para testar Graph API

---

## 📝 CHECKLIST DE IMPLEMENTAÇÃO

- [ ] App criado no Meta for Developers
- [ ] Instagram Business/Creator Account conectado
- [ ] Webhook URL configurada (HTTPS)
- [ ] Verify token definido
- [ ] Eventos subscritos (messages, comments)
- [ ] Permissões solicitadas e aprovadas
- [ ] Validação de signature implementada
- [ ] Processamento assíncrono implementado
- [ ] Logs e monitoramento configurados
- [ ] Testes realizados com Webhook Tester
- [ ] Rate limiting implementado
- [ ] Tratamento de erros robusto
- [ ] Retry logic para Graph API
- [ ] Documentação interna criada

---

**Última atualização:** 06/11/2025
**Mantido por:** Claude Code Workspace
**Webscraping original:** [./webscraping-original/](./webscraping-original/)
