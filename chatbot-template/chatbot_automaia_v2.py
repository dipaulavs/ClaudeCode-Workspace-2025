#!/usr/bin/env python3
"""
🤖 CHATBOT AUTOMAIA V2 - AGÊNCIA DE SEMINOVOS COM RAG

✅ V1 features:
  - Debounce inteligente (15s + 50s se incompleta)
  - Análise IA de completude
  - Fila no Redis
  - Timers por número
  - Resposta DIRETA via Evolution (sem loop)
  - Mensagens humanizadas e picotadas
  - Transcrição de áudios (Whisper)
  - Visão de imagens (GPT-4o)
  - Envio automático de fotos

🚀 NOVO EM V2:
  - RAG Híbrido (keywords + semântico)
  - Progressive Disclosure (economia 50% tokens)
  - IA Especialista por carro
  - Busca multi-carros escalável
"""

from flask import Flask, request, jsonify
import requests
import sys
import os
import json
import time
import re
import threading
from datetime import datetime
from upstash_redis import Redis
import tempfile
from pathlib import Path

# Importa componentes RAG
from componentes.rag.integrador_carros import IntegradorRAGCarros

app = Flask(__name__)

# Configuração OpenRouter
OPENROUTER_API_KEY = "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"

# Configuração OpenAI (para Whisper)
OPENAI_API_KEY = "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"

# Carrega config
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

# ⏳ Sistema de debounce inteligente
DEBOUNCE_SEGUNDOS = 15  # Aguarda 15 segundos após última mensagem
DEBOUNCE_ESTENDIDO = 50  # Tempo adicional se mensagem parecer incompleta
CONTEXTO_TTL = 1209600  # 14 dias

timers_ativos = {}  # {numero: Thread}
lock = threading.Lock()

# 🚀 Integrador RAG Carros
CARROS_DIR = Path(__file__).parent / "carros"
integrador_rag = None  # Será inicializado no final

def transcrever_audio(audio_url):
    """
    🎤 Transcreve áudio usando Whisper da OpenAI

    Args:
        audio_url: URL do arquivo de áudio

    Returns:
        str: Texto transcrito ou mensagem de erro
    """
    try:
        print(f"🎤 Transcrevendo áudio: {audio_url[:50]}...", flush=True)

        # Baixa o áudio
        response = requests.get(audio_url, timeout=30)

        if response.status_code != 200:
            print(f"❌ Erro ao baixar áudio: {response.status_code}", flush=True)
            return "[Erro ao baixar áudio]"

        # Salva temporariamente
        with tempfile.NamedTemporaryFile(delete=False, suffix='.ogg') as temp_file:
            temp_file.write(response.content)
            temp_path = temp_file.name

        print(f"📥 Áudio baixado: {len(response.content)} bytes", flush=True)

        # Transcreve com Whisper
        whisper_url = "https://api.openai.com/v1/audio/transcriptions"

        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }

        with open(temp_path, 'rb') as audio_file:
            files = {
                'file': ('audio.ogg', audio_file, 'audio/ogg'),
                'model': (None, 'whisper-1'),
                'language': (None, 'pt'),
                'response_format': (None, 'text')
            }

            print("🤖 Enviando para Whisper API...", flush=True)
            whisper_response = requests.post(whisper_url, headers=headers, files=files, timeout=60)

        # Remove arquivo temporário
        os.unlink(temp_path)

        if whisper_response.status_code != 200:
            print(f"❌ Erro no Whisper: {whisper_response.status_code}", flush=True)
            print(f"Resposta: {whisper_response.text}", flush=True)
            return "[Erro ao transcrever áudio]"

        transcricao = whisper_response.text.strip()
        print(f"✅ Transcrição: {transcricao[:100]}...", flush=True)

        return transcricao

    except Exception as e:
        print(f"❌ Erro na transcrição: {e}", flush=True)
        import traceback
        traceback.print_exc()
        return "[Erro ao processar áudio]"

def analisar_imagem(image_url):
    """
    👁️ Analisa imagem usando GPT-4o Vision da OpenAI

    Args:
        image_url: URL da imagem

    Returns:
        str: Descrição do que há na imagem ou mensagem de erro
    """
    try:
        print(f"👁️ Analisando imagem: {image_url[:50]}...", flush=True)

        vision_url = "https://api.openai.com/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Descreva esta imagem de forma detalhada e natural, como se estivesse conversando no WhatsApp. Se for um carro, mencione características relevantes (modelo, cor, estado). Seja breve mas informativo (2-3 frases)."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300,
            "temperature": 0.7
        }

        print("🤖 Enviando para GPT-4o Vision API...", flush=True)
        vision_response = requests.post(vision_url, headers=headers, json=payload, timeout=60)

        if vision_response.status_code != 200:
            print(f"❌ Erro no GPT-4o Vision: {vision_response.status_code}", flush=True)
            print(f"Resposta: {vision_response.text}", flush=True)
            return "[Erro ao analisar imagem]"

        resultado = vision_response.json()
        descricao = resultado['choices'][0]['message']['content'].strip()
        print(f"✅ Descrição: {descricao[:100]}...", flush=True)

        return descricao

    except Exception as e:
        print(f"❌ Erro na análise de imagem: {e}", flush=True)
        import traceback
        traceback.print_exc()
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

def analisar_completude_mensagem(mensagens):
    """
    🧠 Usa IA para analisar se mensagem está completa ou se usuário vai enviar mais

    Returns:
        True = Mensagem completa, pode responder
        False = Mensagem incompleta, aguardar mais
    """
    # Se só tem uma mensagem muito curta, provavelmente vem mais
    if len(mensagens) == 1 and len(mensagens[0]) < 10:
        print("🔍 Análise: Mensagem muito curta, aguardando mais...", flush=True)
        return False

    texto_completo = "\n".join(mensagens)

    prompt_analise = f"""Você é um analisador de completude de mensagens WhatsApp.

Analise se esta mensagem parece COMPLETA ou se o usuário provavelmente vai enviar MAIS TEXTO.

MENSAGEM RECEBIDA:
"{texto_completo}"

REGRAS:
- Se termina com "..." ou reticências → INCOMPLETA
- Se é muito curta (só "oi", "olá") → INCOMPLETA
- Se termina com vírgula → INCOMPLETA
- Se faz uma pergunta completa → COMPLETA
- Se expressa uma ideia completa → COMPLETA
- Se tem múltiplas frases coerentes → COMPLETA

Responda APENAS "COMPLETA" ou "INCOMPLETA" (uma palavra só!)"""

    try:
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/felipemdepaula/claude-code-workspace",
            "X-Title": "Chatbot Automaia - Analisador"
        }

        payload = {
            "model": "anthropic/claude-haiku-4.5",
            "messages": [{"role": "user", "content": prompt_analise}],
            "temperature": 0.3,
            "max_tokens": 10
        }

        response = requests.post(url, headers=headers, json=payload, timeout=5)
        response.raise_for_status()

        resultado = response.json()
        resposta_ia = resultado['choices'][0]['message']['content'].strip().upper()

        print(f"🔍 Análise IA: {resposta_ia}", flush=True)

        return resposta_ia.startswith("COMPLETA")

    except Exception as e:
        print(f"⚠️  Erro na análise (assumindo completa): {e}", flush=True)
        return True

def enviar_imagem_whatsapp(phone, image_url, caption=""):
    """
    📸 Envia imagem via WhatsApp usando Evolution API

    Args:
        phone: Número do destinatário
        image_url: URL pública da imagem
        caption: Legenda opcional
    """
    # Garante que a URL está corretamente encodada (espaços se tornam %20)
    from urllib.parse import quote, urlparse, urlunparse

    # Parse a URL
    parsed = urlparse(image_url)
    # Encode apenas o path (mantém o resto intacto)
    encoded_path = quote(parsed.path, safe='/')
    # Reconstrói a URL
    image_url_encoded = urlunparse((
        parsed.scheme,
        parsed.netloc,
        encoded_path,
        parsed.params,
        parsed.query,
        parsed.fragment
    ))

    print(f"\n📸 Enviando imagem para {phone}...", flush=True)
    print(f"🔗 URL encoded: {image_url_encoded[:80]}...", flush=True)
    print(f"📝 Legenda: {caption}", flush=True)

    url = f"{EVOLUTION_URL}/message/sendMedia/{EVOLUTION_INSTANCE}"

    headers = {
        "apikey": EVOLUTION_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "number": phone,
        "mediatype": "image",
        "media": image_url_encoded,  # Usa URL encodada
        "caption": caption
    }

    tentativas = 0
    max_tentativas = 2

    while tentativas < max_tentativas:
        try:
            tentativas += 1
            print(f"🔄 Tentativa {tentativas}/{max_tentativas}...", flush=True)

            response = requests.post(url, headers=headers, json=payload, timeout=60)

            print(f"📡 Status code: {response.status_code}", flush=True)

            if response.status_code in [200, 201]:
                print(f"✅ Imagem enviada com sucesso!", flush=True)
                return True
            else:
                print(f"⚠️  Erro ao enviar imagem: {response.status_code}", flush=True)
                print(f"📄 Resposta: {response.text[:300]}", flush=True)

                if tentativas < max_tentativas:
                    print(f"⏳ Aguardando 2s antes de tentar novamente...", flush=True)
                    time.sleep(2)

        except requests.exceptions.Timeout:
            print(f"⏱️ Timeout na tentativa {tentativas}", flush=True)
            if tentativas < max_tentativas:
                time.sleep(2)

        except Exception as e:
            print(f"❌ Erro na tentativa {tentativas}: {e}", flush=True)
            if tentativas < max_tentativas:
                time.sleep(2)

    print(f"❌ Falha ao enviar imagem após {max_tentativas} tentativas", flush=True)
    return False

def enviar_resposta_whatsapp(phone, mensagem_completa):
    """✅ Envia DIRETO pro WhatsApp via Evolution API (sem loop!)"""
    print(f"\n📤 Enviando resposta DIRETO pro WhatsApp ({phone})...", flush=True)

    partes = dividir_mensagem(mensagem_completa)
    print(f"📦 Mensagem dividida em {len(partes)} partes", flush=True)

    url = f"{EVOLUTION_URL}/message/sendText/{EVOLUTION_INSTANCE}"

    headers = {
        "apikey": EVOLUTION_API_KEY,
        "Content-Type": "application/json"
    }

    for i, parte in enumerate(partes, 1):
        print(f"📨 Enviando parte {i}/{len(partes)}: {parte[:50]}...", flush=True)

        payload = {
            "number": phone,
            "text": parte
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)

            if response.status_code == 200:
                print(f"✅ Parte {i} enviada!", flush=True)
            else:
                print(f"⚠️  Erro: {response.status_code}", flush=True)

        except Exception as e:
            print(f"❌ Erro: {e}", flush=True)

        # Delay entre partes (humanizado)
        if i < len(partes):
            delay = 1.5 + (len(parte) * 0.01)
            delay = min(delay, 3)
            time.sleep(delay)

    print(f"✅ {len(partes)} mensagem(ns) enviada(s)!", flush=True)

def obter_contexto_historico(numero):
    """Obtém histórico do Redis"""
    try:
        chave_contexto = f"contexto:automaia:{numero}"
        contexto = redis.get(chave_contexto)
        return json.loads(contexto) if contexto else []
    except Exception as e:
        print(f"⚠️  Erro ao obter contexto: {e}")
        return []

def salvar_contexto(numero, mensagem, tipo="user"):
    """Salva mensagem no contexto"""
    try:
        chave_contexto = f"contexto:automaia:{numero}"
        contexto = obter_contexto_historico(numero)

        contexto.append({
            "tipo": tipo,
            "mensagem": mensagem,
            "timestamp": datetime.now().isoformat()
        })

        if len(contexto) > 30:
            contexto = contexto[-30:]

        redis.setex(chave_contexto, CONTEXTO_TTL, json.dumps(contexto))
    except Exception as e:
        print(f"⚠️  Erro ao salvar contexto: {e}")

def carregar_fotos_carro(carro_id):
    """
    📸 Carrega lista de fotos de um carro

    Args:
        carro_id: ID do carro (nome da pasta)

    Returns:
        Lista de dicts com {nome, link} ou lista vazia
    """
    carro_path = CARROS_DIR / carro_id
    links_file = carro_path / "links.json"

    if not links_file.exists():
        return []

    try:
        with open(links_file, 'r', encoding='utf-8') as f:
            links_data = json.load(f)
            return links_data.get("fotos", [])
    except Exception as e:
        print(f"❌ Erro ao carregar fotos de {carro_id}: {e}", flush=True)
        return []

def processar_mensagens_agrupadas(numero):
    """
    ⏳ Processa todas as mensagens acumuladas após debounce
    Usa análise IA para decidir se aguarda mais ou responde
    """
    try:
        chave_fila = f"fila:automaia:{numero}"
        mensagens_json = redis.get(chave_fila)

        if not mensagens_json:
            return

        mensagens = json.loads(mensagens_json)

        if not mensagens:
            return

        print(f"\n🚀 Timer disparado! {len(mensagens)} mensagem(ns) de {numero}", flush=True)

        # Verifica se já aguardou tempo extra
        chave_aguardou = f"aguardou_extra:automaia:{numero}"
        ja_aguardou_extra = redis.get(chave_aguardou)

        # 🧠 ANÁLISE INTELIGENTE
        if not ja_aguardou_extra:
            print("🧠 Analisando se mensagem está completa...", flush=True)
            mensagem_completa = analisar_completude_mensagem(mensagens)

            if not mensagem_completa:
                print(f"⏳ Mensagem parece INCOMPLETA. Aguardando mais {DEBOUNCE_ESTENDIDO}s...", flush=True)

                # Marca que vai aguardar extra
                redis.setex(chave_aguardou, 90, "1")

                # Cria novo timer estendido
                with lock:
                    if numero in timers_ativos:
                        timers_ativos[numero].cancel()

                    timer = threading.Timer(
                        DEBOUNCE_ESTENDIDO,
                        processar_mensagens_agrupadas,
                        args=[numero]
                    )
                    timer.daemon = True
                    timer.start()
                    timers_ativos[numero] = timer

                return  # Aguarda mais
        else:
            print("⏰ Já aguardou tempo extra. Processando agora!", flush=True)

        # Mensagem COMPLETA - processar!
        print(f"✅ Mensagem COMPLETA! Processando...", flush=True)

        # Limpa fila e flags
        redis.delete(chave_fila)
        redis.delete(chave_aguardou)

        with lock:
            if numero in timers_ativos:
                del timers_ativos[numero]

        # Obtém contexto histórico
        contexto_historico = obter_contexto_historico(numero)

        # Agrupa mensagens
        if len(mensagens) == 1:
            contexto = mensagens[0]
        else:
            contexto = "\n".join([f"- {msg}" for msg in mensagens])
            contexto = f"Cliente enviou várias mensagens seguidas:\n{contexto}"

        # Formata contexto para RAG
        contexto_rag = []
        for msg in contexto_historico[-6:]:
            role = "assistant" if msg['tipo'] == "bot" else "user"
            contexto_rag.append({
                "role": role,
                "content": msg['mensagem']
            })

        print(f"📝 Contexto: {contexto[:150]}...", flush=True)

        # Salva mensagens do usuário
        for msg in mensagens:
            salvar_contexto(numero, msg, "user")

        # 🚀 GERA RESPOSTA COM RAG
        print("🤖 Gerando resposta com RAG...", flush=True)
        resposta = integrador_rag.processar_mensagem(numero, contexto, contexto_rag)
        print(f"✅ Resposta gerada: {resposta}", flush=True)

        # Salva resposta
        salvar_contexto(numero, resposta, "bot")

        # Envia resposta DIRETO via Evolution
        enviar_resposta_whatsapp(numero, resposta)

        print("✅ Resposta enviada!", flush=True)

    except Exception as e:
        print(f"❌ Erro ao processar: {e}", flush=True)
        import traceback
        traceback.print_exc()

def adicionar_mensagem_na_fila(numero, mensagem):
    """
    📦 Adiciona mensagem na fila Redis e inicia/reseta timer de debounce
    """
    try:
        chave_fila = f"fila:automaia:{numero}"

        # Busca fila atual
        mensagens_json = redis.get(chave_fila)
        mensagens = json.loads(mensagens_json) if mensagens_json else []

        # Adiciona nova mensagem
        mensagens.append(mensagem)

        # Salva no Redis com TTL de 90s
        redis.setex(chave_fila, 90, json.dumps(mensagens))

        # Limpa flag de "aguardou extra"
        chave_aguardou = f"aguardou_extra:automaia:{numero}"
        redis.delete(chave_aguardou)

        # Cancela timer anterior e cria novo
        with lock:
            if numero in timers_ativos:
                timers_ativos[numero].cancel()

            timer = threading.Timer(
                DEBOUNCE_SEGUNDOS,
                processar_mensagens_agrupadas,
                args=[numero]
            )
            timer.daemon = True
            timer.start()

            timers_ativos[numero] = timer

        qtd = len(mensagens)
        print(f"⏳ TIMER RESETADO: {qtd} msg na fila de {numero}, aguarda {DEBOUNCE_SEGUNDOS}s...", flush=True)

    except Exception as e:
        print(f"❌ ERRO na fila: {e}", flush=True)
        import traceback
        traceback.print_exc()

@app.route('/webhook/chatwoot', methods=['POST'])
def webhook_chatwoot():
    """
    🎯 Recebe webhook do Chatwoot (via middleware)

    ✅ V2: Adiciona na fila + RAG Híbrido
    ✅ Responde DIRETO via Evolution (sem loop)
    """
    try:
        data = request.json

        print(f"\n{'='*80}", flush=True)
        print(f"🔔 WEBHOOK CHATWOOT → BOT AUTOMAIA V2 - {datetime.now().strftime('%H:%M:%S')}", flush=True)
        print(f"{'='*80}", flush=True)

        conversation_id = data.get('conversation_id')
        message_id = data.get('message_id')
        content = data.get('content', '')
        attachments = data.get('attachments', [])
        sender = data.get('sender', {})

        phone = sender.get('phone', '').replace('+', '')
        name = sender.get('name', phone)

        print(f"📱 De: {name} ({phone})", flush=True)
        print(f"💬 Mensagem: {content[:100]}...", flush=True)
        print(f"📎 Attachments: {len(attachments)}", flush=True)

        # Processa attachments
        if attachments:
            print(f"📎 Mídias recebidas:", flush=True)
            for i, att in enumerate(attachments, 1):
                tipo = att.get('file_type', 'unknown')
                url = att.get('data_url', 'N/A')
                print(f"   {i}. Tipo: {tipo} | URL: {url[:50]}...", flush=True)

                # 🎤 Transcreve áudios automaticamente
                if tipo == 'audio':
                    print(f"🎤 Detectado áudio! Transcrevendo...", flush=True)
                    transcricao = transcrever_audio(url)

                    if transcricao and not transcricao.startswith('[Erro'):
                        content += f"\n[Áudio transcrito]: {transcricao}"
                        print(f"✅ Áudio transcrito e adicionado ao conteúdo", flush=True)
                    else:
                        content += f"\n[Usuário enviou um áudio mas não foi possível transcrever]"

                # 👁️ Analisa imagens automaticamente
                elif tipo == 'image':
                    print(f"👁️ Detectada imagem! Analisando...", flush=True)
                    descricao = analisar_imagem(url)

                    if descricao and not descricao.startswith('[Erro'):
                        content += f"\n[Imagem enviada]: {descricao}"
                        print(f"✅ Imagem analisada e adicionada ao conteúdo", flush=True)
                    else:
                        content += f"\n[Usuário enviou uma imagem mas não foi possível analisar]"

                else:
                    # Outros tipos de arquivo
                    if not content:
                        content = ""

            # Se teve arquivos não-áudio e não-imagem, menciona
            arquivos_outros = [a for a in attachments if a.get('file_type') not in ['audio', 'image']]
            if arquivos_outros:
                content += f"\n[Usuário enviou {len(arquivos_outros)} arquivo(s)]"

        # Só ignora se não tiver conteúdo E não tiver attachments
        if not content and not attachments:
            print("⏭️  Sem conteúdo e sem attachments", flush=True)
            return jsonify({"status": "ignored"})

        # Se não tem content mas tem attachments (ex: só áudio), garante que content tenha algo
        if not content:
            content = "[Mensagem sem texto]"

        # 📦 ADICIONA NA FILA (não responde imediatamente!)
        print(f"📦 Adicionando na fila com debounce...", flush=True)
        adicionar_mensagem_na_fila(phone, content)

        return jsonify({
            "status": "queued",
            "phone": phone,
            "info": f"Mensagem adicionada na fila. Aguardando {DEBOUNCE_SEGUNDOS}s para processar."
        })

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
        redis_status = "✅ conectado"
    except:
        redis_status = "❌ erro"

    with lock:
        timers_count = len(timers_ativos)

    total_carros = len(integrador_rag.rag.database) if integrador_rag else 0

    return jsonify({
        "status": "online",
        "version": "2.0 - AUTOMAIA SEMINOVOS COM RAG",
        "chatbot": "Automaia V2",
        "model": "anthropic/claude-haiku-4.5",
        "whisper": "openai/whisper-1",
        "vision": "openai/gpt-4o",
        "redis": redis_status,
        "carros": {
            "total": total_carros
        },
        "features": [
            "✅ Debounce 15s (agrupa mensagens)",
            "✅ Análise IA de completude",
            "✅ Debounce estendido 50s (se incompleta)",
            "✅ Fila no Redis",
            "✅ Timers por número",
            "✅ Resposta DIRETA via Evolution (sem loop)",
            "✅ Mensagens humanizadas e picotadas",
            "🎤 Transcrição automática de áudios (Whisper)",
            "👁️ Visão de imagens (GPT-4o)",
            "🚗 Banco de dados de carros seminovos",
            "🚀 RAG Híbrido (keywords + semântico)",
            "📚 Progressive Disclosure (economia 50% tokens)",
            "🤖 IA Especialista por carro"
        ],
        "timers_ativos": timers_count,
        "debounce_segundos": DEBOUNCE_SEGUNDOS,
        "debounce_estendido_segundos": DEBOUNCE_ESTENDIDO
    })

if __name__ == '__main__':
    print("=" * 70)
    print("🤖 CHATBOT AUTOMAIA V2 - AGÊNCIA DE SEMINOVOS COM RAG!")
    print("=" * 70)
    print("✨ Funcionalidades:")
    print("   ✅ Debounce 15s + 50s (se incompleta)")
    print("   ✅ Análise IA de completude")
    print("   ✅ Fila no Redis")
    print("   ✅ Timers por número")
    print("   ✅ Resposta DIRETA via Evolution (sem loop)")
    print("   ✅ Mensagens humanizadas")
    print("   🎤 Transcrição automática de áudios (Whisper)")
    print("   👁️ Visão de imagens (GPT-4o)")
    print("   🚗 Banco de dados de carros seminovos")
    print("   🚀 RAG Híbrido (keywords + semântico)")
    print("   📚 Progressive Disclosure (economia 50% tokens)")
    print("   🤖 IA Especialista por carro")
    print()
    print(f"🌐 Webhook: http://localhost:5003/webhook/chatwoot")
    print(f"💚 Health: http://localhost:5003/health")
    print("=" * 70)

    # Inicializa RAG
    print("\n🚀 Inicializando RAG...")
    integrador_rag = IntegradorRAGCarros(
        carros_dir=CARROS_DIR,
        openai_api_key=OPENAI_API_KEY,
        openrouter_api_key=OPENROUTER_API_KEY,
        redis_client=redis
    )

    if integrador_rag.rag.database:
        print(f"✅ {len(integrador_rag.rag.database)} carro(s) carregado(s)!")
    else:
        print("⚠️  Nenhum carro encontrado.")
        print(f"💡 Dica: Use 'python3 upload_fotos_carros.py' para adicionar carros")

    # Redis
    try:
        redis.ping()
        print("✅ Redis conectado!")
    except Exception as e:
        print(f"❌ Erro ao conectar Redis: {e}")

    print("\n🚀 Servidor iniciando...\n")

    app.run(host='0.0.0.0', port=5003, debug=False, use_reloader=False)
