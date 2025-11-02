#!/usr/bin/env python3
"""
🔄 WEBHOOK MIDDLEWARE V2 - CHATWOOT + EVOLUTION API
Bot recebe webhook do CHATWOOT (não Evolution)

NOVO FLUXO:
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
with open('chatwoot_config.json', 'r') as f:
    config = json.load(f)

CHATWOOT_URL = config['chatwoot']['url']
CHATWOOT_TOKEN = config['chatwoot']['token']
ACCOUNT_ID = config['chatwoot']['account_id']
INBOX_ID = config['chatwoot']['inbox_id']

EVOLUTION_URL = config['evolution']['url']
EVOLUTION_API_KEY = config['evolution']['api_key']
EVOLUTION_INSTANCE = config['evolution']['instance']

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
            return response.json()
        else:
            log(f"⚠️  Erro ao enviar: {response.status_code}")
            return None

    except Exception as e:
        log(f"❌ Erro ao enviar mensagem: {e}")
        return None

def verificar_atendente_ativo(conversation_id):
    """
    Verifica se há atendente ativo

    Returns:
        True = Tem atendente (bot fica quieto)
        False = Sem atendente (bot responde)
    """
    try:
        url = f"{CHATWOOT_URL}/api/v1/accounts/{ACCOUNT_ID}/conversations/{conversation_id}"
        headers = {"api_access_token": CHATWOOT_TOKEN}

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            conv = response.json()

            assignee = conv.get('meta', {}).get('assignee')
            status = conv.get('status')

            if assignee and assignee.get('id'):
                log(f"👤 Atendente ativo: {assignee.get('name')}")
                conversas_com_atendente[conversation_id] = {
                    "assignee_id": assignee.get('id'),
                    "timestamp": datetime.now().isoformat()
                }
                return True

            if status == 'resolved':
                log(f"✅ Conversa resolvida - Bot liberado")
                if conversation_id in conversas_com_atendente:
                    del conversas_com_atendente[conversation_id]
                return False

            log(f"🤖 Sem atendente - Bot autorizado")
            if conversation_id in conversas_com_atendente:
                del conversas_com_atendente[conversation_id]
            return False

        return False

    except Exception as e:
        log(f"❌ Erro ao verificar atendente: {e}")
        return False

@app.route('/webhook/evolution', methods=['POST'])
def webhook_evolution():
    """
    Recebe webhook da Evolution
    Apenas cria mensagem no Chatwoot
    O Chatwoot vai disparar seu próprio webhook
    """
    try:
        data = request.json

        log("\n" + "="*80)
        log("🔔 WEBHOOK EVOLUTION → CHATWOOT")
        log("="*80)

        if data.get('event') != 'messages.upsert':
            return jsonify({"status": "ignored"})

        message_data = data.get('data', {})
        key = message_data.get('key', {})
        message = message_data.get('message', {})

        if key.get('fromMe'):
            log("⏭️  Ignorado: Mensagem enviada por mim (fromMe=true)")
            return jsonify({"status": "ignored", "reason": "from_me"})

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

        # Busca/cria contato
        contact_id = buscar_ou_criar_contato_chatwoot(numero)
        if not contact_id:
            return jsonify({"status": "error"}), 500

        # Busca/cria conversa
        conversation_id = buscar_ou_criar_conversa_chatwoot(contact_id, numero)
        if not conversation_id:
            return jsonify({"status": "error"}), 500

        # Envia para Chatwoot
        # IMPORTANTE: Chatwoot vai disparar webhook message_created
        # que será processado pela rota /webhook/chatwoot abaixo
        message_created = enviar_mensagem_chatwoot(conversation_id, mensagem_texto, "incoming")

        if message_created:
            log(f"✅ Mensagem enviada ao Chatwoot (ID: {message_created.get('id')})")
            # Salva ID para não reprocessar
            mensagens_processadas.add(message_created.get('id'))

        return jsonify({
            "status": "sent_to_chatwoot",
            "conversation_id": conversation_id,
            "info": "Chatwoot vai disparar webhook próprio"
        })

    except Exception as e:
        log(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error"}), 500

@app.route('/webhook/chatwoot', methods=['POST'])
def webhook_chatwoot():
    """
    🎯 ROTA PRINCIPAL - Recebe webhook do Chatwoot

    Aqui decidimos se bot responde ou não
    Bot recebe dados do Chatwoot (com URLs de mídia)
    """
    try:
        data = request.json

        log("\n" + "="*80)
        log("🔔 WEBHOOK CHATWOOT")
        log("="*80)

        event = data.get('event')

        # 1. Se for mensagem criada, verifica se bot deve responder
        if event == 'message_created':
            message_type = data.get('message_type')
            message_id = data.get('id')

            # Ignora se já processamos (veio da Evolution)
            if message_id in mensagens_processadas:
                log(f"⏭️  Mensagem {message_id} já processada (veio da Evolution)")
                mensagens_processadas.discard(message_id)  # Remove do cache
                return jsonify({"status": "already_processed"})

            # Só processa mensagens incoming (clientes)
            if message_type != 'incoming':
                log(f"⏭️  Ignorado: Tipo {message_type} (bot envia direto via Evolution)")

                # ✅ CORREÇÃO V3: NÃO envia outgoing para WhatsApp
                # Bot V3 já envia DIRETO via Evolution API
                # Se for atendente humano, ele responde direto no WhatsApp

                return jsonify({"status": "ignored", "reason": "bot_sends_directly"})

            # Pega dados da mensagem
            content = data.get('content')  # Pode ser None para attachments
            conversation = data.get('conversation', {})
            conversation_id = conversation.get('id')
            attachments = data.get('attachments', [])

            # Log seguro (content pode ser None)
            if content:
                log(f"💬 Mensagem: {content[:50]}...")
            else:
                log(f"💬 Mensagem: (sem texto, apenas attachments)")
            log(f"📎 Attachments: {len(attachments)}")

            # Verifica se bot deve responder
            tem_atendente = verificar_atendente_ativo(conversation_id)

            if tem_atendente:
                log(f"👤 ATENDENTE ATIVO - Bot em standby")
                return jsonify({"status": "human_handling"})

            # 🤖 BOT PODE RESPONDER!
            log(f"🤖 BOT AUTORIZADO - Enviando para chatbot...")

            # Prepara dados no formato que o bot entende
            bot_payload = {
                "conversation_id": conversation_id,
                "message_id": message_id,
                "content": content or "",  # Garante que seja string (mesmo que vazia)
                "attachments": attachments,  # URLs prontas do Chatwoot!
                "sender": {
                    "phone": conversation.get('meta', {}).get('sender', {}).get('phone_number', ''),
                    "name": conversation.get('meta', {}).get('sender', {}).get('name', '')
                },
                "chatwoot_data": data  # Dados completos para debug
            }

            # Envia para o bot V3
            try:
                bot_url = "http://localhost:5001/webhook/chatwoot"  # Bot V3
                response = requests.post(bot_url, json=bot_payload, timeout=5)

                if response.status_code == 200:
                    log(f"✅ Bot processou e respondeu!")
                    return jsonify({"status": "bot_responded"})
                else:
                    log(f"⚠️  Bot erro: {response.status_code}")
                    return jsonify({"status": "bot_error"}), 500

            except Exception as e:
                log(f"❌ Erro ao chamar bot: {e}")
                return jsonify({"status": "bot_unreachable"}), 500

        # 2. Outros eventos do Chatwoot
        elif event == 'conversation_status_changed':
            status = data.get('status')
            conversation_id = data.get('id')
            log(f"📊 Status mudou: {status}")

            if status == 'resolved':
                if conversation_id in conversas_com_atendente:
                    del conversas_com_atendente[conversation_id]
                    log(f"✅ Bot liberado para conversa {conversation_id}")

        elif event == 'assignee_changed':
            assignee = data.get('assignee')
            conversation_id = data.get('id')

            if assignee:
                log(f"👤 Atendente atribuído: {assignee.get('name')}")
                conversas_com_atendente[conversation_id] = {
                    "assignee_id": assignee.get('id'),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                log(f"🤖 Atendente removido - Bot liberado")
                if conversation_id in conversas_com_atendente:
                    del conversas_com_atendente[conversation_id]

        return jsonify({"status": "processed"})

    except Exception as e:
        log(f"❌ Erro no webhook Chatwoot: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error"}), 500

def enviar_para_whatsapp(data):
    """Envia mensagem de atendente para WhatsApp via Evolution"""
    try:
        content = data.get('content', '')
        conversation = data.get('conversation', {})
        contact = conversation.get('meta', {}).get('sender', {})

        phone = contact.get('phone_number', '').replace('+', '')

        if not phone:
            log("⚠️  Sem número de telefone")
            return jsonify({"status": "error"}), 400

        log(f"📤 Enviando para WhatsApp ({phone}): {content[:50]}...")

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
            log(f"✅ Enviado via Evolution")
            return jsonify({"status": "sent"})
        else:
            log(f"⚠️  Erro: {response.status_code}")
            return jsonify({"status": "error"}), 500

    except Exception as e:
        log(f"❌ Erro ao enviar para WhatsApp: {e}")
        return jsonify({"status": "error"}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "status": "online",
        "version": "2.0 - Bot recebe do Chatwoot",
        "conversas_com_atendente": len(conversas_com_atendente),
        "mensagens_cache": len(mensagens_processadas),
        "bot_enabled": config['bot']['enabled']
    })

if __name__ == '__main__':
    log("="*80)
    log("🔄 WEBHOOK MIDDLEWARE V2 - BOT RECEBE DO CHATWOOT")
    log("="*80)
    log(f"📥 Evolution → Chatwoot: http://localhost:5002/webhook/evolution")
    log(f"🎯 Chatwoot → Bot: http://localhost:5002/webhook/chatwoot")
    log(f"💚 Health: http://localhost:5002/health")
    log("="*80)
    log("")
    log("🎯 NOVO FLUXO:")
    log("  1. Evolution → Middleware → Cria msg no Chatwoot")
    log("  2. Chatwoot dispara webhook → Middleware")
    log("  3. Middleware verifica atendente")
    log("  4. Se liberado → Envia pro BOT (formato Chatwoot)")
    log("  5. Bot recebe URLs de mídia prontas!")
    log("")
    log("🚀 Servidor iniciando...\n")

    app.run(host='0.0.0.0', port=5002, debug=False)
