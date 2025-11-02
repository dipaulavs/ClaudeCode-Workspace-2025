#!/usr/bin/env python3
"""
🔄 WEBHOOK MIDDLEWARE - CHATWOOT + EVOLUTION API
Integração híbrida: Bot automático + Atendimento humano

FLUXO:
1. Evolution envia mensagem → Este middleware
2. Middleware envia para Chatwoot
3. Middleware verifica: Tem atendente ativo?
   - SIM → Bloqueia bot, deixa humano responder
   - NÃO → Permite bot responder automaticamente
4. Quando atendente assume → Bot para
5. Quando conversa é resolvida → Bot volta
"""

from flask import Flask, request, jsonify
import requests
import json
import sys
import os
from datetime import datetime

app = Flask(__name__)

# Carrega configurações
with open('chatwoot_config.json', 'r') as f:
    config = json.load(f)

CHATWOOT_URL = config['chatwoot']['url']
CHATWOOT_TOKEN = config['chatwoot']['token']
ACCOUNT_ID = config['chatwoot']['account_id']
INBOX_ID = config['chatwoot']['inbox_id']

EVOLUTION_URL = config['evolution']['url']
EVOLUTION_API_KEY = config['evolution']['api_key']
EVOLUTION_INSTANCE = config['evolution']['instance']

# Cache local de conversas com atendente
conversas_com_atendente = {}  # {numero: {conversation_id, assignee_id, timestamp}}

def log(mensagem):
    """Log com timestamp"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] {mensagem}", flush=True)

def buscar_ou_criar_contato_chatwoot(numero, nome=None):
    """
    Busca ou cria contato no Chatwoot

    Returns:
        contact_id ou None
    """
    try:
        # Busca contato existente por número
        url = f"{CHATWOOT_URL}/api/v1/accounts/{ACCOUNT_ID}/contacts/search"
        headers = {"api_access_token": CHATWOOT_TOKEN}
        params = {"q": numero}

        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            contacts = response.json().get('payload', [])

            # Se encontrou, retorna primeiro
            if contacts:
                contact_id = contacts[0]['id']
                log(f"✅ Contato encontrado: {contact_id}")
                return contact_id

        # Não encontrou → Cria novo contato
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
        else:
            log(f"⚠️  Erro ao criar contato: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        log(f"❌ Erro ao buscar/criar contato: {e}")
        return None

def buscar_ou_criar_conversa_chatwoot(contact_id, numero):
    """
    Busca conversa aberta ou cria nova

    Returns:
        conversation_id ou None
    """
    try:
        # Busca conversas abertas do contato
        url = f"{CHATWOOT_URL}/api/v1/accounts/{ACCOUNT_ID}/conversations"
        headers = {"api_access_token": CHATWOOT_TOKEN}
        params = {
            "inbox_id": INBOX_ID,
            "status": "open"  # Apenas abertas
        }

        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            conversations = response.json().get('data', {}).get('payload', [])

            # Busca conversa deste contato
            for conv in conversations:
                if conv.get('meta', {}).get('sender', {}).get('id') == contact_id:
                    conversation_id = conv['id']
                    log(f"✅ Conversa encontrada: {conversation_id}")
                    return conversation_id

        # Não encontrou → Cria nova conversa
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
        else:
            log(f"⚠️  Erro ao criar conversa: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        log(f"❌ Erro ao buscar/criar conversa: {e}")
        return None

def enviar_mensagem_chatwoot(conversation_id, mensagem, message_type="incoming"):
    """
    Envia mensagem para o Chatwoot

    Args:
        conversation_id: ID da conversa
        mensagem: Texto da mensagem
        message_type: "incoming" (cliente) ou "outgoing" (agente/bot)
    """
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

        response = requests.post(url, headers=headers, json=payload, timeout=10)

        if response.status_code in [200, 201]:
            log(f"✅ Mensagem enviada ao Chatwoot")
            return True
        else:
            log(f"⚠️  Erro ao enviar mensagem: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        log(f"❌ Erro ao enviar mensagem: {e}")
        return False

def verificar_atendente_ativo(conversation_id):
    """
    Verifica se há atendente humano ativo na conversa

    Returns:
        True = Tem atendente (bot deve ficar quieto)
        False = Sem atendente (bot pode responder)
    """
    try:
        url = f"{CHATWOOT_URL}/api/v1/accounts/{ACCOUNT_ID}/conversations/{conversation_id}"
        headers = {"api_access_token": CHATWOOT_TOKEN}

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            conv = response.json()

            # Verifica se tem assignee (atendente atribuído)
            assignee = conv.get('meta', {}).get('assignee')
            status = conv.get('status')

            if assignee and assignee.get('id'):
                log(f"👤 Atendente ativo: {assignee.get('name')} (ID: {assignee.get('id')})")
                return True

            # Se status for "resolved", bot pode voltar
            if status == 'resolved':
                log(f"✅ Conversa resolvida - Bot pode responder")
                return False

            log(f"🤖 Sem atendente - Bot pode responder")
            return False
        else:
            log(f"⚠️  Erro ao verificar atendente: {response.status_code}")
            # Em caso de erro, assume que não tem atendente
            return False

    except Exception as e:
        log(f"❌ Erro ao verificar atendente: {e}")
        return False

def deve_bot_responder(numero, conversation_id):
    """
    Lógica central: Decide se o bot deve responder ou não

    Returns:
        True = Bot responde
        False = Bot fica quieto (humano vai responder)
    """

    # 1. Verifica se configuração permite bot
    if not config['bot']['enabled']:
        log("🚫 Bot desabilitado na config")
        return False

    # 2. Verifica se há atendente ativo
    tem_atendente = verificar_atendente_ativo(conversation_id)

    if tem_atendente:
        # Atualiza cache
        conversas_com_atendente[numero] = {
            "conversation_id": conversation_id,
            "timestamp": datetime.now().isoformat()
        }
        log(f"👤 HUMANO ATIVO - Bot NÃO vai responder")
        return False
    else:
        # Remove do cache se estava lá
        if numero in conversas_com_atendente:
            del conversas_com_atendente[numero]

        log(f"🤖 BOT AUTORIZADO - Vai responder automaticamente")
        return True

@app.route('/webhook/evolution', methods=['POST'])
def webhook_evolution():
    """
    Recebe webhooks da Evolution API
    Envia para Chatwoot e decide se bot responde
    """
    try:
        data = request.json

        log("\n" + "="*80)
        log("🔔 WEBHOOK EVOLUTION → CHATWOOT")
        log("="*80)

        # Verifica se é mensagem nova
        if data.get('event') != 'messages.upsert':
            log("⏭️  Ignorado: Não é mensagem nova")
            return jsonify({"status": "ignored"})

        # Extrai dados
        message_data = data.get('data', {})
        key = message_data.get('key', {})
        message = message_data.get('message', {})

        # Ignora mensagens enviadas por mim
        if key.get('fromMe'):
            log("⏭️  Ignorado: Mensagem enviada por mim")
            return jsonify({"status": "ignored"})

        # Extrai número e texto
        remote_jid = key.get('remoteJid', '')
        numero = remote_jid.replace('@s.whatsapp.net', '')

        mensagem_texto = (
            message.get('conversation') or
            message.get('extendedTextMessage', {}).get('text') or
            ""
        )

        if not mensagem_texto:
            log("⏭️  Ignorado: Sem texto")
            return jsonify({"status": "ignored"})

        log(f"💬 MSG de {numero}: {mensagem_texto[:50]}...")

        # 1. Busca/cria contato no Chatwoot
        contact_id = buscar_ou_criar_contato_chatwoot(numero)
        if not contact_id:
            log("❌ Falha ao criar contato")
            return jsonify({"status": "error", "message": "contact_creation_failed"}), 500

        # 2. Busca/cria conversa no Chatwoot
        conversation_id = buscar_ou_criar_conversa_chatwoot(contact_id, numero)
        if not conversation_id:
            log("❌ Falha ao criar conversa")
            return jsonify({"status": "error", "message": "conversation_creation_failed"}), 500

        # 3. Envia mensagem para o Chatwoot
        sucesso = enviar_mensagem_chatwoot(conversation_id, mensagem_texto, "incoming")
        if not sucesso:
            log("⚠️  Falha ao enviar mensagem ao Chatwoot")

        # 4. DECISÃO: Bot deve responder?
        bot_deve_responder = deve_bot_responder(numero, conversation_id)

        if bot_deve_responder:
            log("🤖 ENCAMINHANDO para o BOT...")
            # Encaminha para o bot original
            try:
                bot_url = "http://localhost:5001/webhook"  # URL do chatbot_corretor.py
                response = requests.post(bot_url, json=data, timeout=5)
                log(f"✅ Bot processou: {response.status_code}")
            except Exception as e:
                log(f"⚠️  Erro ao chamar bot: {e}")
        else:
            log("👤 Atendente vai responder - Bot em standby")

        return jsonify({
            "status": "processed",
            "contact_id": contact_id,
            "conversation_id": conversation_id,
            "bot_respondeu": bot_deve_responder
        })

    except Exception as e:
        log(f"❌ Erro no webhook: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/webhook/chatwoot', methods=['POST'])
def webhook_chatwoot():
    """
    Recebe webhooks do Chatwoot
    Envia mensagens de atendentes para o WhatsApp via Evolution
    """
    try:
        data = request.json

        log("\n" + "="*80)
        log("🔔 WEBHOOK CHATWOOT → EVOLUTION")
        log("="*80)

        # Verifica se é mensagem nova de atendente
        event = data.get('event')

        if event != 'message_created':
            log(f"⏭️  Ignorado: Evento {event}")
            return jsonify({"status": "ignored"})

        message_type = data.get('message_type')

        # Só processa mensagens outgoing (de atendentes)
        if message_type != 'outgoing':
            log(f"⏭️  Ignorado: Tipo {message_type}")
            return jsonify({"status": "ignored"})

        # Extrai dados
        content = data.get('content', '')
        conversation = data.get('conversation', {})
        contact = conversation.get('meta', {}).get('sender', {})

        # Pega número do contato
        phone = contact.get('phone_number', '').replace('+', '')

        if not phone:
            log("⚠️  Sem número de telefone")
            return jsonify({"status": "error", "message": "no_phone"}), 400

        log(f"📤 Enviando para {phone}: {content[:50]}...")

        # Envia via Evolution API
        url = f"{EVOLUTION_URL}/message/sendText/{EVOLUTION_INSTANCE}"
        headers = {
            "apikey": EVOLUTION_API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "number": phone,
            "text": content
        }

        response = requests.post(url, headers=headers, json=payload, timeout=10)

        if response.status_code == 200:
            log(f"✅ Mensagem enviada via Evolution")
            return jsonify({"status": "sent"})
        else:
            log(f"⚠️  Erro Evolution: {response.status_code} - {response.text}")
            return jsonify({"status": "error", "message": response.text}), 500

    except Exception as e:
        log(f"❌ Erro no webhook Chatwoot: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "status": "online",
        "servico": "Webhook Middleware - Chatwoot + Evolution",
        "conversas_com_atendente": len(conversas_com_atendente),
        "bot_enabled": config['bot']['enabled']
    })

if __name__ == '__main__':
    log("="*80)
    log("🔄 WEBHOOK MIDDLEWARE - INTEGRAÇÃO HÍBRIDA")
    log("="*80)
    log(f"📥 Evolution → Chatwoot: http://localhost:5002/webhook/evolution")
    log(f"📤 Chatwoot → Evolution: http://localhost:5002/webhook/chatwoot")
    log(f"💚 Health: http://localhost:5002/health")
    log("="*80)
    log("")
    log("🎯 FLUXO:")
    log("  1. Evolution envia mensagem → /webhook/evolution")
    log("  2. Middleware envia para Chatwoot")
    log("  3. Verifica: Tem atendente ativo?")
    log("     👤 SIM → Humano responde (bot fica quieto)")
    log("     🤖 NÃO → Bot responde automaticamente")
    log("")
    log("🚀 Servidor iniciando...\n")

    app.run(host='0.0.0.0', port=5002, debug=False)
