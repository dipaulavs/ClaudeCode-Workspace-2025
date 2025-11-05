#!/usr/bin/env python3
"""
🔄 WEBHOOK MIDDLEWARE AUTOMAIA - CHATWOOT + EVOLUTION API
Bot recebe webhook do CHATWOOT (não Evolution)

FLUXO:
1. Evolution envia mensagem → Middleware
2. Middleware cria mensagem no Chatwoot
3. Chatwoot dispara webhook message_created → Middleware
4. Middleware verifica: Bot deve responder?
   - SIM → Envia para bot (formato Chatwoot com URLs de mídia)
   - NÃO → Atendente responde
5. Bot responde → Evolution → Cliente
"""

from flask import Flask, request, jsonify
import requests
import json
import sys
import os
from datetime import datetime

app = Flask(__name__)

# Carrega configurações
with open('chatwoot_config_automaia.json', 'r') as f:
    config = json.load(f)

CHATWOOT_URL = config['chatwoot']['url']
CHATWOOT_TOKEN = config['chatwoot']['token']
ACCOUNT_ID = config['chatwoot']['account_id']
INBOX_ID = config['chatwoot']['inbox_id']

EVOLUTION_URL = config['evolution']['url']
EVOLUTION_API_KEY = config['evolution']['api_key']
EVOLUTION_INSTANCE = config['evolution']['instance']

# URL do bot
BOT_WEBHOOK_URL = "http://localhost:5003/webhook/chatwoot"

# 🔒 FILTRO DE NÚMERO - SOMENTE ESTE NÚMERO SERÁ ATENDIDO
# Aceita com ou sem o 9 extra (Evolution API pode enviar em formatos diferentes)
NUMEROS_PERMITIDOS = ["5531986549366", "553186549366"]

# Cache de conversas
conversas_com_atendente = {}  # {conversation_id: {assignee_id, timestamp}}
mensagens_processadas = set()  # Evita processar mesma mensagem 2x

def log(mensagem):
    """Log com timestamp"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] {mensagem}", flush=True)

def buscar_ou_criar_contato_chatwoot(numero, nome=None):
    """Busca ou cria contato no Chatwoot"""
    try:
        # Busca contato existente
        url = f"{CHATWOOT_URL}/api/v1/accounts/{ACCOUNT_ID}/contacts/search"
        headers = {"api_access_token": CHATWOOT_TOKEN}
        params = {"q": numero}

        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            contacts = response.json().get('payload', [])
            if contacts:
                contact_id = contacts[0]['id']
                log(f"✅ Contato encontrado: {contact_id}")
                return contact_id

        # Cria novo contato
        log(f"📝 Criando novo contato para {numero}")
        url = f"{CHATWOOT_URL}/api/v1/accounts/{ACCOUNT_ID}/contacts"
        headers = {
            "api_access_token": CHATWOOT_TOKEN,
            "Content-Type": "application/json"
        }

        payload = {
            "inbox_id": INBOX_ID,
            "name": nome or numero,
            "phone_number": f"+{numero}",
            "identifier": numero
        }

        response = requests.post(url, headers=headers, json=payload, timeout=10)

        if response.status_code in [200, 201]:
            contact = response.json().get('payload', {}).get('contact', {})
            contact_id = contact.get('id')
            log(f"✅ Contato criado: {contact_id}")
            return contact_id

        log(f"⚠️  Erro ao criar contato: {response.status_code}")
        return None

    except Exception as e:
        log(f"❌ Erro ao buscar/criar contato: {e}")
        return None

def buscar_ou_criar_conversa_chatwoot(contact_id, numero):
    """Busca conversa aberta ou cria nova"""
    try:
        # Busca conversas abertas do contato
        url = f"{CHATWOOT_URL}/api/v1/accounts/{ACCOUNT_ID}/conversations"
        headers = {"api_access_token": CHATWOOT_TOKEN}
        params = {"inbox_id": INBOX_ID, "status": "open"}

        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            conversations = response.json().get('data', {}).get('payload', [])

            for conv in conversations:
                if conv.get('meta', {}).get('sender', {}).get('id') == contact_id:
                    conversation_id = conv['id']
                    log(f"✅ Conversa encontrada: {conversation_id}")
                    return conversation_id

        # Cria nova conversa
        log(f"📝 Criando nova conversa para contato {contact_id}")
        url = f"{CHATWOOT_URL}/api/v1/accounts/{ACCOUNT_ID}/conversations"
        headers = {
            "api_access_token": CHATWOOT_TOKEN,
            "Content-Type": "application/json"
        }

        payload = {
            "inbox_id": INBOX_ID,
            "contact_id": contact_id,
            "status": "open"
        }

        response = requests.post(url, headers=headers, json=payload, timeout=10)

        if response.status_code in [200, 201]:
            conversation_id = response.json().get('id')
            log(f"✅ Conversa criada: {conversation_id}")
            return conversation_id

        log(f"⚠️  Erro ao criar conversa: {response.status_code}")
        return None

    except Exception as e:
        log(f"❌ Erro ao buscar/criar conversa: {e}")
        return None

def enviar_mensagem_chatwoot(conversation_id, mensagem, message_type="incoming", attachments=None):
    """Envia mensagem para o Chatwoot"""
    try:
        url = f"{CHATWOOT_URL}/api/v1/accounts/{ACCOUNT_ID}/conversations/{conversation_id}/messages"

        headers = {
            "api_access_token": CHATWOOT_TOKEN,
            "Content-Type": "application/json"
        }

        payload = {
            "content": mensagem,
            "message_type": message_type,
            "private": False
        }

        if attachments:
            payload["attachments"] = attachments

        response = requests.post(url, headers=headers, json=payload, timeout=10)

        if response.status_code in [200, 201]:
            log(f"✅ Mensagem enviada ao Chatwoot")
            return True

        log(f"⚠️  Erro ao enviar mensagem: {response.status_code}")
        return False

    except Exception as e:
        log(f"❌ Erro ao enviar mensagem: {e}")
        return False

def verificar_atendente_ativo(conversation_id):
    """Verifica se há atendente atribuído à conversa"""
    try:
        url = f"{CHATWOOT_URL}/api/v1/accounts/{ACCOUNT_ID}/conversations/{conversation_id}"
        headers = {"api_access_token": CHATWOOT_TOKEN}

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            assignee_id = data.get('meta', {}).get('assignee', {}).get('id')

            if assignee_id:
                log(f"👤 Atendente ativo: {assignee_id}")
                return True

        return False

    except Exception as e:
        log(f"❌ Erro ao verificar atendente: {e}")
        return False

@app.route('/webhook/evolution', methods=['POST'])
def webhook_evolution():
    """
    Recebe mensagens da Evolution API e cria no Chatwoot
    """
    try:
        data = request.json

        log(f"\n{'='*80}")
        log(f"📱 WEBHOOK EVOLUTION → MIDDLEWARE AUTOMAIA")
        log(f"{'='*80}")

        event = data.get('event')

        if event != 'messages.upsert':
            log(f"⏭️  Evento ignorado: {event}")
            return jsonify({"status": "ignored"})

        message_data = data.get('data', {})
        key = message_data.get('key', {})
        message = message_data.get('message', {})

        # Ignora mensagens do próprio bot
        if key.get('fromMe'):
            log("⏭️  Mensagem enviada pelo bot, ignorando")
            return jsonify({"status": "ignored"})

        # Extrai dados
        numero = key.get('remoteJid', '').replace('@s.whatsapp.net', '')
        push_name = message_data.get('pushName', numero)

        # 🔒 FILTRO DE NÚMERO - Aceita apenas números permitidos
        if numero not in NUMEROS_PERMITIDOS:
            log(f"🚫 Número {numero} não autorizado. Ignorando mensagem.")
            return jsonify({"status": "ignored", "reason": "numero_nao_autorizado"})

        # Extrai conteúdo
        conversation = message.get('conversation', '')
        extended = message.get('extendedTextMessage', {}).get('text', '')
        content = conversation or extended

        log(f"📱 De: {push_name} ({numero})")
        log(f"💬 Mensagem: {content[:100]}...")

        # Processa mídias
        attachments_data = []

        # Imagem
        if 'imageMessage' in message:
            image_url = message['imageMessage'].get('url')
            if image_url:
                attachments_data.append({
                    "file_type": "image",
                    "data_url": image_url
                })
                log(f"🖼️  Imagem detectada")

        # Áudio
        if 'audioMessage' in message:
            audio_url = message['audioMessage'].get('url')
            if audio_url:
                attachments_data.append({
                    "file_type": "audio",
                    "data_url": audio_url
                })
                log(f"🎤 Áudio detectado")

        # Vídeo
        if 'videoMessage' in message:
            video_url = message['videoMessage'].get('url')
            if video_url:
                attachments_data.append({
                    "file_type": "video",
                    "data_url": video_url
                })
                log(f"🎬 Vídeo detectado")

        # Busca ou cria contato
        contact_id = buscar_ou_criar_contato_chatwoot(numero, push_name)
        if not contact_id:
            return jsonify({"status": "error", "message": "Falha ao criar contato"}), 500

        # Busca ou cria conversa
        conversation_id = buscar_ou_criar_conversa_chatwoot(contact_id, numero)
        if not conversation_id:
            return jsonify({"status": "error", "message": "Falha ao criar conversa"}), 500

        # Envia mensagem ao Chatwoot
        enviar_mensagem_chatwoot(conversation_id, content or "[Mídia]", "incoming", attachments_data)

        return jsonify({"status": "success", "conversation_id": conversation_id})

    except Exception as e:
        log(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/webhook/chatwoot', methods=['POST'])
def webhook_chatwoot():
    """
    Recebe webhooks do Chatwoot e decide: Bot ou Atendente?
    """
    try:
        data = request.json

        log(f"\n{'='*80}")
        log(f"🔔 WEBHOOK CHATWOOT → MIDDLEWARE AUTOMAIA")
        log(f"{'='*80}")

        event = data.get('event')

        # Só processa message_created
        if event != 'message_created':
            log(f"⏭️  Evento ignorado: {event}")
            return jsonify({"status": "ignored"})

        message_type = data.get('message_type')
        conversation_id = data.get('conversation', {}).get('id')
        message_id = data.get('id')

        # Ignora mensagens do bot
        if message_type == 'outgoing':
            log("⏭️  Mensagem outgoing (do bot), ignorando")
            return jsonify({"status": "ignored"})

        # Evita processar mensagem duplicada
        if message_id in mensagens_processadas:
            log(f"⏭️  Mensagem {message_id} já processada")
            return jsonify({"status": "already_processed"})

        mensagens_processadas.add(message_id)

        # Limita tamanho do cache (últimas 1000)
        if len(mensagens_processadas) > 1000:
            mensagens_processadas.clear()

        log(f"📝 Conversation ID: {conversation_id}")
        log(f"📝 Message ID: {message_id}")

        # Verifica se tem atendente ativo
        tem_atendente = verificar_atendente_ativo(conversation_id)

        if tem_atendente:
            log("👤 Atendente ativo → Bot NÃO responde")
            return jsonify({"status": "handled_by_agent"})

        # SEM atendente → BOT RESPONDE
        log("🤖 Sem atendente → Enviando para BOT")

        # Formata payload para o bot
        sender = data.get('sender', {})
        content = data.get('content', '')
        attachments = data.get('attachments', [])

        bot_payload = {
            "conversation_id": conversation_id,
            "message_id": message_id,
            "content": content,
            "attachments": attachments,
            "sender": {
                "phone": sender.get('phone_number', '').replace('+', ''),
                "name": sender.get('name', '')
            }
        }

        # Envia para bot
        try:
            response = requests.post(BOT_WEBHOOK_URL, json=bot_payload, timeout=30)

            if response.status_code == 200:
                log("✅ Mensagem enviada ao bot com sucesso")
                return jsonify({"status": "sent_to_bot"})
            else:
                log(f"⚠️  Erro ao enviar ao bot: {response.status_code}")
                return jsonify({"status": "error", "message": "Falha ao enviar ao bot"}), 500

        except Exception as e:
            log(f"❌ Erro ao enviar ao bot: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500

    except Exception as e:
        log(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "status": "online",
        "service": "Middleware Automaia",
        "version": "1.0",
        "chatwoot": CHATWOOT_URL,
        "evolution_instance": EVOLUTION_INSTANCE,
        "bot_url": BOT_WEBHOOK_URL
    })

if __name__ == '__main__':
    print("=" * 70)
    print("🔄 WEBHOOK MIDDLEWARE AUTOMAIA V1")
    print("=" * 70)
    print(f"🌐 Evolution Webhook: http://localhost:5004/webhook/evolution")
    print(f"🌐 Chatwoot Webhook: http://localhost:5004/webhook/chatwoot")
    print(f"💚 Health: http://localhost:5004/health")
    print(f"🤖 Bot URL: {BOT_WEBHOOK_URL}")
    print("=" * 70)

    app.run(host='0.0.0.0', port=5004, debug=False, use_reloader=False)
