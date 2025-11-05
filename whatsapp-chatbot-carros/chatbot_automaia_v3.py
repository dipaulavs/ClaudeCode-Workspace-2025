#!/usr/bin/env python3
"""
🤖 CHATBOT AUTOMAIA V3 - AGENTE PRINCIPAL COM FERRAMENTAS

Arquitetura simples baseada em N8N:
- Agente Principal (personalidade editável)
- 3 Ferramentas especializadas:
  1. lista_carros - Lista carros disponíveis
  2. consulta_faq - Busca respostas no FAQ do carro ativo
  3. taguear_cliente - Tageia no Chatwoot + Redis

✅ Features mantidas:
  - Debounce inteligente (15s + 50s)
  - Transcrição de áudios (Whisper)
  - Visão de imagens (GPT-4o)
  - Contexto Redis (14 dias)
"""

from flask import Flask, request, jsonify
import requests
import json
import time
import re
import threading
from datetime import datetime
from upstash_redis import Redis
from pathlib import Path
import tempfile
import os

# Importa ferramentas
import sys
sys.path.append(str(Path(__file__).parent / "ferramentas"))

from lista_carros import listar_carros_disponiveis, formatar_lista_para_mensagem
from consulta_faq import consultar_faq_carro
from tagueamento import taguear_cliente, obter_carro_ativo

app = Flask(__name__)

# Configuração
OPENROUTER_API_KEY = "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"
OPENAI_API_KEY = "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"

# Carrega config Chatwoot/Evolution
with open('chatwoot_config_automaia.json', 'r') as f:
    config = json.load(f)

CHATWOOT_URL = config['chatwoot']['url']
CHATWOOT_TOKEN = config['chatwoot']['token']
ACCOUNT_ID = config['chatwoot']['account_id']
EVOLUTION_URL = config['evolution']['url']
EVOLUTION_API_KEY = config['evolution']['api_key']
EVOLUTION_INSTANCE = config['evolution']['instance']

# Redis
redis = Redis(
    url="https://legible-collie-9537.upstash.io",
    token="ASVBAAImcDFiOTlmYTM1MTdkNzg0MWU3OTI5YmU4N2RmZmU5ZmJkZnAxOTUzNw"
)

# Debounce
DEBOUNCE_SEGUNDOS = 15
DEBOUNCE_ESTENDIDO = 50
CONTEXTO_TTL = 1209600  # 14 dias

timers_ativos = {}
lock = threading.Lock()

# Path dos carros
CARROS_DIR = Path(__file__).parent / "carros"
PERSONALIDADE_FILE = Path(__file__).parent / "personalidade.txt"


def carregar_personalidade() -> str:
    """Carrega arquivo personalidade.txt (editável ao vivo)"""
    try:
        with open(PERSONALIDADE_FILE, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"⚠️ Erro ao carregar personalidade: {e}", flush=True)
        return "Você é vendedor da Automaia, agência de carros seminovos. Seja amigável e prestativo."


def transcrever_audio(audio_url):
    """Transcreve áudio usando Whisper"""
    try:
        print(f"🎤 Transcrevendo áudio...", flush=True)
        response = requests.get(audio_url, timeout=30)

        if response.status_code != 200:
            return "[Erro ao baixar áudio]"

        with tempfile.NamedTemporaryFile(delete=False, suffix='.ogg') as temp_file:
            temp_file.write(response.content)
            temp_path = temp_file.name

        whisper_url = "https://api.openai.com/v1/audio/transcriptions"
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}

        with open(temp_path, 'rb') as audio_file:
            files = {
                'file': ('audio.ogg', audio_file, 'audio/ogg'),
                'model': (None, 'whisper-1'),
                'language': (None, 'pt'),
                'response_format': (None, 'text')
            }
            whisper_response = requests.post(whisper_url, headers=headers, files=files, timeout=60)

        os.unlink(temp_path)

        if whisper_response.status_code != 200:
            return "[Erro ao transcrever áudio]"

        transcricao = whisper_response.text.strip()
        print(f"✅ Transcrição: {transcricao[:100]}...", flush=True)
        return transcricao

    except Exception as e:
        print(f"❌ Erro na transcrição: {e}", flush=True)
        return "[Erro ao processar áudio]"


def analisar_imagem(image_url):
    """Analisa imagem usando GPT-4o Vision"""
    try:
        print(f"👁️ Analisando imagem...", flush=True)
        vision_url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gpt-4o",
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "text", "text": "Descreva esta imagem de forma detalhada (2-3 frases). Se for um carro, mencione características."},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }],
            "max_tokens": 300
        }

        vision_response = requests.post(vision_url, headers=headers, json=payload, timeout=60)

        if vision_response.status_code != 200:
            return "[Erro ao analisar imagem]"

        resultado = vision_response.json()
        descricao = resultado['choices'][0]['message']['content'].strip()
        print(f"✅ Descrição: {descricao[:100]}...", flush=True)
        return descricao

    except Exception as e:
        print(f"❌ Erro na análise: {e}", flush=True)
        return "[Erro ao processar imagem]"


def dividir_mensagem(texto):
    """Divide mensagem em partes menores (humanizado)"""
    texto = texto.strip()
    partes = []

    for linha in texto.split('\n'):
        linha = linha.strip()
        if not linha:
            continue

        if len(linha) <= 100:
            partes.append(linha)
        else:
            frases = re.split(r'([.!?]+\s+)', linha)
            frase_atual = ""

            for i, frase in enumerate(frases):
                frase_atual += frase

                if re.match(r'[.!?]+\s+', frase):
                    continue

                if len(frase_atual) > 80 or i == len(frases) - 1:
                    if frase_atual.strip():
                        partes.append(frase_atual.strip())
                    frase_atual = ""

    return partes


def enviar_resposta_whatsapp(phone, mensagem_completa):
    """Envia resposta via Evolution API"""
    print(f"\n📤 Enviando resposta para {phone}...", flush=True)

    partes = dividir_mensagem(mensagem_completa)
    url = f"{EVOLUTION_URL}/message/sendText/{EVOLUTION_INSTANCE}"
    headers = {
        "apikey": EVOLUTION_API_KEY,
        "Content-Type": "application/json"
    }

    for i, parte in enumerate(partes, 1):
        payload = {"number": phone, "text": parte}

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                print(f"✅ Parte {i} enviada", flush=True)
        except Exception as e:
            print(f"❌ Erro parte {i}: {e}", flush=True)

        if i < len(partes):
            delay = 1.5 + (len(parte) * 0.01)
            time.sleep(min(delay, 3))


def obter_contexto_historico(numero):
    """Obtém histórico do Redis"""
    try:
        chave = f"contexto:automaia:{numero}"
        contexto = redis.get(chave)
        return json.loads(contexto) if contexto else []
    except:
        return []


def salvar_contexto(numero, mensagem, tipo="user"):
    """Salva mensagem no contexto"""
    try:
        chave = f"contexto:automaia:{numero}"
        contexto = obter_contexto_historico(numero)

        contexto.append({
            "tipo": tipo,
            "mensagem": mensagem,
            "timestamp": datetime.now().isoformat()
        })

        if len(contexto) > 30:
            contexto = contexto[-30:]

        redis.setex(chave, CONTEXTO_TTL, json.dumps(contexto))
    except Exception as e:
        print(f"⚠️ Erro ao salvar contexto: {e}")


def gerar_resposta_com_ferramentas(numero, mensagem, contexto_historico):
    """
    Agente Principal com 3 ferramentas
    Usa Claude com function calling
    """
    print(f"\n🤖 Agente Principal processando...", flush=True)

    # Carrega personalidade (ao vivo!)
    personalidade = carregar_personalidade()

    # Verifica carro ativo
    carro_ativo = obter_carro_ativo(numero, redis)
    print(f"   Carro ativo: {carro_ativo if carro_ativo else 'Nenhum'}", flush=True)

    # Monta contexto
    mensagens = []

    # System prompt com personalidade + ferramentas
    system_prompt = f"""{personalidade}

🔧 FERRAMENTAS OBRIGATÓRIAS:

Você tem 3 ferramentas. SEMPRE use a ferramenta correta - NUNCA invente informações!

1. **lista_carros** - Lista carros disponíveis
2. **consulta_faq** - Consulta FAQ do carro ativo
3. **taguear_cliente** - Marca cliente interessado em carro

{"🚗 CARRO ATIVO: " + carro_ativo if carro_ativo else "❌ SEM CARRO ATIVO"}

⚠️ REGRAS OBRIGATÓRIAS (NUNCA QUEBRE):

📋 **LISTA DE CARROS:**
Cliente pergunta: "quais carros tem?", "me mostra", "o que tem?", "tenho X reais"
→ SEMPRE use lista_carros
→ NUNCA responda sem usar a ferramenta
→ NUNCA invente carros que não existem

❓ **PERGUNTAS SOBRE CARRO:**
Cliente pergunta: "preço", "garantia", "aceita troca", "qual motor"
→ SE tem carro ativo: SEMPRE use consulta_faq
→ SE NÃO tem carro ativo: Pergunte qual carro interessa PRIMEIRO

🏷️ **ESCOLHA DE CARRO:**
Cliente diz: "quero o Gol", "me fala do HB20", "interessado no Civic"
→ SEMPRE use taguear_cliente PRIMEIRO
→ Depois pode usar consulta_faq para responder

📌 **EXEMPLOS PRÁTICOS:**

Cliente: "Quais carros vocês tem?"
Você: [USA lista_carros] → Adapta resposta ao tom

Cliente: "Quanto custa o Gol?"
Você (SEM carro ativo): [USA lista_carros para confirmar] → [USA taguear_cliente com gol-2020-001] → [USA consulta_faq com "preço"]

Cliente: "Aceita troca?" (COM carro ativo: gol-2020-001)
Você: [USA consulta_faq com "troca"]

🚨 NUNCA FAÇA ISSO:
❌ Responder sobre carros sem usar lista_carros
❌ Responder detalhes sem usar consulta_faq
❌ Esquecer de taguear quando cliente escolhe carro
❌ Inventar informações (preço, garantia, etc)

✅ SEMPRE FAÇA ISSO:
✓ Use ferramenta ANTES de responder
✓ Adapte resposta da ferramenta ao seu tom
✓ Seja natural e amigável na resposta final
"""

    mensagens.append({"role": "system", "content": system_prompt})

    # Adiciona histórico (últimas 6 msgs)
    for msg in contexto_historico[-6:]:
        role = "assistant" if msg['tipo'] == "bot" else "user"
        mensagens.append({"role": role, "content": msg['mensagem']})

    # Mensagem atual
    mensagens.append({"role": "user", "content": mensagem})

    # Define ferramentas no formato OpenAI
    tools = [
        {
            "type": "function",
            "function": {
                "name": "lista_carros",
                "description": "Lista todos os carros disponíveis na loja com marca, modelo, ano e preço",
                "parameters": {"type": "object", "properties": {}}
            }
        },
        {
            "type": "function",
            "function": {
                "name": "consulta_faq",
                "description": "Consulta FAQ do carro ativo para responder perguntas específicas",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pergunta": {
                            "type": "string",
                            "description": "Pergunta do cliente (opcional)"
                        }
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "taguear_cliente",
                "description": "Marca cliente como interessado em um carro específico",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "carro_id": {
                            "type": "string",
                            "description": "ID do carro (formato: marca-modelo-ano-001)"
                        }
                    },
                    "required": ["carro_id"]
                }
            }
        }
    ]

    # Chama Claude com function calling
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "anthropic/claude-haiku-4.5",
            "messages": mensagens,
            "tools": tools,
            "temperature": 0.9,
            "max_tokens": 500
        }

        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        resultado = response.json()
        message = resultado['choices'][0]['message']

        # Verifica se chamou ferramenta
        if message.get('tool_calls'):
            tool_call = message['tool_calls'][0]
            function_name = tool_call['function']['name']
            function_args = json.loads(tool_call['function']['arguments'])

            print(f"   🔧 Ferramenta: {function_name}", flush=True)
            print(f"   📋 Args: {function_args}", flush=True)

            # Executa ferramenta
            if function_name == "lista_carros":
                carros = listar_carros_disponiveis(CARROS_DIR)
                resultado_ferramenta = formatar_lista_para_mensagem(carros)

            elif function_name == "consulta_faq":
                if not carro_ativo:
                    resultado_ferramenta = "ERRO: Cliente não tem carro ativo. Use lista_carros primeiro."
                else:
                    pergunta = function_args.get('pergunta', '')
                    resultado = consultar_faq_carro(carro_ativo, pergunta, CARROS_DIR)
                    if resultado['sucesso']:
                        resultado_ferramenta = f"{resultado['base']}\n\n{resultado['faq']}"
                    else:
                        resultado_ferramenta = resultado['erro']

            elif function_name == "taguear_cliente":
                carro_id = function_args['carro_id']
                resultado_tag = taguear_cliente(numero, carro_id, redis, config['chatwoot'])
                if resultado_tag['sucesso']:
                    resultado_ferramenta = f"✅ Cliente marcado como interessado em {carro_id}"
                else:
                    resultado_ferramenta = f"⚠️ Erro ao taguear: {resultado_tag['erro']}"

            # Adiciona resultado da ferramenta ao contexto
            mensagens.append(message)
            mensagens.append({
                "role": "tool",
                "tool_call_id": tool_call['id'],
                "content": resultado_ferramenta
            })

            # Claude processa resultado e gera resposta final
            payload['messages'] = mensagens
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            resultado = response.json()

        # Resposta final
        resposta = resultado['choices'][0]['message']['content'].strip()
        print(f"   ✅ Resposta gerada ({len(resposta)} chars)", flush=True)
        return resposta

    except Exception as e:
        print(f"❌ Erro no Agente: {e}", flush=True)
        import traceback
        traceback.print_exc()
        return "Desculpa, tive um problema. Pode repetir sua pergunta? 😊"


def analisar_completude_mensagem(mensagens):
    """Usa IA para analisar se mensagem está completa"""
    if len(mensagens) == 1 and len(mensagens[0]) < 10:
        return False

    texto_completo = "\n".join(mensagens)
    prompt = f"""Analise se esta mensagem WhatsApp está COMPLETA ou INCOMPLETA.

MENSAGEM: "{texto_completo}"

REGRAS:
- "..." ou reticências → INCOMPLETA
- Muito curta (só "oi") → INCOMPLETA
- Termina com vírgula → INCOMPLETA
- Pergunta completa → COMPLETA
- Ideia completa → COMPLETA

Responda APENAS "COMPLETA" ou "INCOMPLETA"."""

    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "anthropic/claude-haiku-4.5",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 10
        }

        response = requests.post(url, headers=headers, json=payload, timeout=5)
        response.raise_for_status()
        resultado = response.json()
        resposta_ia = resultado['choices'][0]['message']['content'].strip().upper()

        print(f"🔍 Análise: {resposta_ia}", flush=True)
        return resposta_ia.startswith("COMPLETA")

    except:
        return True


def processar_mensagens_agrupadas(numero):
    """Processa mensagens após debounce"""
    try:
        chave_fila = f"fila:automaia:{numero}"
        mensagens_json = redis.get(chave_fila)

        if not mensagens_json:
            return

        mensagens = json.loads(mensagens_json)

        if not mensagens:
            return

        print(f"\n🚀 Timer disparado! {len(mensagens)} mensagem(ns) de {numero}", flush=True)

        # Análise de completude
        chave_aguardou = f"aguardou_extra:automaia:{numero}"
        ja_aguardou_extra = redis.get(chave_aguardou)

        if not ja_aguardou_extra:
            mensagem_completa = analisar_completude_mensagem(mensagens)

            if not mensagem_completa:
                print(f"⏳ INCOMPLETA. Aguardando +{DEBOUNCE_ESTENDIDO}s...", flush=True)
                redis.setex(chave_aguardou, 90, "1")

                with lock:
                    if numero in timers_ativos:
                        timers_ativos[numero].cancel()

                    timer = threading.Timer(DEBOUNCE_ESTENDIDO, processar_mensagens_agrupadas, args=[numero])
                    timer.daemon = True
                    timer.start()
                    timers_ativos[numero] = timer

                return

        # Limpa fila
        redis.delete(chave_fila)
        redis.delete(chave_aguardou)

        with lock:
            if numero in timers_ativos:
                del timers_ativos[numero]

        # Agrupa mensagens
        contexto = "\n".join(mensagens) if len(mensagens) > 1 else mensagens[0]
        contexto_historico = obter_contexto_historico(numero)

        # Salva mensagens
        for msg in mensagens:
            salvar_contexto(numero, msg, "user")

        # Gera resposta COM FERRAMENTAS
        resposta = gerar_resposta_com_ferramentas(numero, contexto, contexto_historico)

        # Salva resposta
        salvar_contexto(numero, resposta, "bot")

        # Envia via Evolution
        enviar_resposta_whatsapp(numero, resposta)
        print("✅ Resposta enviada!", flush=True)

    except Exception as e:
        print(f"❌ Erro ao processar: {e}", flush=True)
        import traceback
        traceback.print_exc()


def adicionar_mensagem_na_fila(numero, mensagem):
    """Adiciona mensagem na fila com debounce"""
    try:
        chave_fila = f"fila:automaia:{numero}"
        mensagens_json = redis.get(chave_fila)
        mensagens = json.loads(mensagens_json) if mensagens_json else []

        mensagens.append(mensagem)
        redis.setex(chave_fila, 90, json.dumps(mensagens))

        chave_aguardou = f"aguardou_extra:automaia:{numero}"
        redis.delete(chave_aguardou)

        with lock:
            if numero in timers_ativos:
                timers_ativos[numero].cancel()

            timer = threading.Timer(DEBOUNCE_SEGUNDOS, processar_mensagens_agrupadas, args=[numero])
            timer.daemon = True
            timer.start()
            timers_ativos[numero] = timer

        print(f"⏳ TIMER: {len(mensagens)} msg, aguarda {DEBOUNCE_SEGUNDOS}s", flush=True)

    except Exception as e:
        print(f"❌ ERRO fila: {e}", flush=True)


@app.route('/webhook/chatwoot', methods=['POST'])
def webhook_chatwoot():
    """Recebe webhook do Chatwoot"""
    try:
        data = request.json
        print(f"\n{'='*80}", flush=True)
        print(f"🔔 WEBHOOK CHATWOOT → BOT V3 - {datetime.now().strftime('%H:%M:%S')}", flush=True)
        print(f"{'='*80}", flush=True)

        content = data.get('content', '')
        attachments = data.get('attachments', [])
        sender = data.get('sender', {})
        phone = sender.get('phone', '').replace('+', '')

        print(f"📱 De: {sender.get('name', phone)} ({phone})", flush=True)
        print(f"💬 Mensagem: {content[:100]}...", flush=True)

        # Processa attachments
        if attachments:
            for att in attachments:
                tipo = att.get('file_type')
                url = att.get('data_url')

                if tipo == 'audio':
                    transcricao = transcrever_audio(url)
                    if not transcricao.startswith('[Erro'):
                        content += f"\n[Áudio]: {transcricao}"

                elif tipo == 'image':
                    descricao = analisar_imagem(url)
                    if not descricao.startswith('[Erro'):
                        content += f"\n[Imagem]: {descricao}"

        if not content:
            return jsonify({"status": "ignored"})

        # Adiciona na fila
        adicionar_mensagem_na_fila(phone, content)

        return jsonify({"status": "queued"})

    except Exception as e:
        print(f"❌ Erro: {e}", flush=True)
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    try:
        redis.ping()
        redis_status = "✅"
    except:
        redis_status = "❌"

    with lock:
        timers_count = len(timers_ativos)

    # Conta carros
    carros = listar_carros_disponiveis(CARROS_DIR)

    return jsonify({
        "status": "online",
        "version": "3.0 - AGENTE PRINCIPAL COM FERRAMENTAS",
        "model": "anthropic/claude-haiku-4.5",
        "redis": redis_status,
        "carros": len(carros),
        "timers_ativos": timers_count,
        "features": [
            "✅ Agente Principal (personalidade editável)",
            "✅ 3 Ferramentas (lista_carros, consulta_faq, tagueamento)",
            "✅ Debounce 15s + 50s",
            "✅ Transcrição áudios (Whisper)",
            "✅ Visão imagens (GPT-4o)",
            "✅ Contexto Redis (14 dias)",
            "✅ Tagueamento Chatwoot"
        ]
    })


if __name__ == '__main__':
    print("=" * 70)
    print("🤖 CHATBOT AUTOMAIA V3 - AGENTE PRINCIPAL")
    print("=" * 70)
    print("✨ Arquitetura:")
    print("   ✅ Agente Principal (personalidade.txt)")
    print("   ✅ 3 Ferramentas especializadas")
    print("   ✅ Debounce inteligente")
    print("   ✅ Transcrição + Visão")
    print()
    print(f"🌐 Webhook: http://localhost:5003/webhook/chatwoot")
    print(f"💚 Health: http://localhost:5003/health")
    print("=" * 70)

    # Testa personalidade
    print("\n📝 Carregando personalidade...")
    pers = carregar_personalidade()
    print(f"✅ {len(pers)} chars carregados\n")

    # Testa carros
    carros = listar_carros_disponiveis(CARROS_DIR)
    print(f"🚗 {len(carros)} carros disponíveis")

    # Redis
    try:
        redis.ping()
        print("✅ Redis conectado!")
    except Exception as e:
        print(f"❌ Erro Redis: {e}")

    print("\n🚀 Servidor iniciando...\n")
    app.run(host='0.0.0.0', port=5003, debug=False, use_reloader=False)
