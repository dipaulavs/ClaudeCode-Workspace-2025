#!/usr/bin/env python3
"""
🗓️ FERRAMENTA: AGENDAR VISITA
Consulta agenda do corretor e agenda visitas ao imóvel

WORKFLOW:
1. Cliente pede pra agendar → Bot sugere horários
2. Cliente escolhe (1, 2, 3) → Bot confirma + notifica corretor
"""

from pathlib import Path
from typing import Dict, Optional
import json
from upstash_redis import Redis


def agendar_visita_corretor(
    acao: str,
    cliente_numero: str,
    redis_client: Redis,
    config: Dict,
    escolha: Optional[str] = None
) -> str:
    """
    Gerencia agendamento de visita ao imóvel com corretor

    Args:
        acao: "sugerir" ou "confirmar"
        cliente_numero: Número do cliente
        redis_client: Cliente Redis
        config: Config completo (chatwoot, evolution)
        escolha: Escolha do cliente (ex: "1", "2", "3") - apenas para ação "confirmar"

    Returns:
        Mensagem formatada para WhatsApp

    Exemplos:
        # Sugerir horários
        >>> agendar_visita_corretor("sugerir", "5531999999999", redis, config)
        "Posso agendar pra:\\n1️⃣ Amanhã às 10h\\n2️⃣ Quarta às 14h..."

        # Confirmar escolha
        >>> agendar_visita_corretor("confirmar", "5531999999999", redis, config, escolha="1")
        "✅ Agendado! Amanhã às 10h..."
    """
    from componentes.escalonamento import IntegradorEscalonamento

    # Inicializa integrador
    integrador = IntegradorEscalonamento(redis_client, config)

    # AÇÃO: SUGERIR HORÁRIOS
    if acao == "sugerir":
        # Busca imóvel ativo (se houver)
        imovel_id = None
        try:
            imovel_ativo = redis_client.get(f"imovel_ativo:lfimoveis:{cliente_numero}")
            if imovel_ativo:
                imovel_id = imovel_ativo
        except Exception as e:
            print(f"⚠️ Erro ao buscar imóvel ativo: {e}")

        # Chama integrador para sugerir horários
        mensagem = integrador.sugerir_horarios(cliente_numero, imovel_id)

        print(f"📅 Horários sugeridos para {cliente_numero}")
        return mensagem

    # AÇÃO: CONFIRMAR AGENDAMENTO
    elif acao == "confirmar":
        if not escolha:
            return "❌ Preciso que você escolha um dos números (1, 2 ou 3)"

        # Busca imóvel ativo
        imovel_id = None
        try:
            imovel_ativo = redis_client.get(f"imovel_ativo:lfimoveis:{cliente_numero}")
            if imovel_ativo:
                imovel_id = imovel_ativo
        except Exception as e:
            print(f"⚠️ Erro ao buscar imóvel ativo: {e}")

        # Confirma agendamento
        sucesso, mensagem = integrador.confirmar_agendamento(
            cliente_numero,
            escolha,
            imovel_id
        )

        if sucesso:
            print(f"✅ Agendamento confirmado para {cliente_numero}")

            # NOTIFICA CORRETOR
            _notificar_corretor_agendamento(
                cliente_numero,
                imovel_id,
                mensagem,
                redis_client,
                config
            )
        else:
            print(f"⚠️ Erro ao agendar para {cliente_numero}")

        return mensagem

    else:
        return f"❌ Ação inválida: {acao}. Use 'sugerir' ou 'confirmar'"


def _notificar_corretor_agendamento(
    cliente_numero: str,
    imovel_id: Optional[str],
    mensagem_confirmacao: str,
    redis_client: Redis,
    config: Dict
):
    """
    Notifica corretor sobre novo agendamento via WhatsApp
    Envia notificação ENRIQUECIDA com: dados completos do imóvel,
    resumo da conversa gerado por IA, e score detalhado do cliente

    Args:
        cliente_numero: Número do cliente
        imovel_id: ID do imóvel de interesse
        mensagem_confirmacao: Mensagem de confirmação enviada ao cliente
        redis_client: Cliente Redis
        config: Config completo
    """
    try:
        # 1. BUSCA DADOS DO CLIENTE
        nome_cliente = _buscar_nome_cliente(cliente_numero, config)
        telefone_formatado = _formatar_telefone(cliente_numero)

        # Score do cliente
        score_key = f"score:{cliente_numero}"
        score = redis_client.get(score_key) or "0"
        score_int = int(score)

        # Classificação detalhada
        if score_int >= 70:
            classificacao = "🔥 QUENTE"
        elif score_int >= 40:
            classificacao = "🌡️ MORNO"
        else:
            classificacao = "❄️ FRIO"

        # 2. BUSCA DETALHES COMPLETOS DO IMÓVEL
        detalhes_imovel = _extrair_detalhes_imovel(imovel_id)

        # 3. EXTRAI HORÁRIO DA MENSAGEM DE CONFIRMAÇÃO
        import re
        horario_match = re.search(r'📅\s*(.+?)\s*às\s*(.+)', mensagem_confirmacao)
        data_hora = "Não especificado"
        if horario_match:
            data_hora = f"{horario_match.group(1)} às {horario_match.group(2)}"

        # 4. GERA RESUMO DA CONVERSA COM IA
        resumo_conversa = _gerar_resumo_conversa_ia(
            cliente_numero,
            redis_client,
            detalhes_imovel.get('tipo', 'imóvel')
        )

        # 5. MONTA MENSAGEM ENRIQUECIDA PARA CORRETOR
        corretor_whatsapp = "5531980160822"  # Corretor Luciano

        mensagem_corretor = f"""
🗓️ *NOVA VISITA AGENDADA*

👤 *CLIENTE*
📱 {nome_cliente or "Cliente"}
📞 {telefone_formatado}
📊 Score: {score_int} - {classificacao}

🏠 *IMÓVEL DE INTERESSE*
{detalhes_imovel['titulo']}
💰 Preço: {detalhes_imovel['preco']}
💳 Condições: {detalhes_imovel['condicoes']}

📅 *AGENDAMENTO*
{data_hora}

💬 *RESUMO DA CONVERSA*
{resumo_conversa}

🔔 *Ação:* Confirme presença 1 dia antes!
        """.strip()

        # 6. ENVIA VIA EVOLUTION API
        import requests

        evolution_url = config['evolution']['url']
        evolution_instance = config['evolution']['instance']
        evolution_api_key = config['evolution']['api_key']

        payload = {
            "number": corretor_whatsapp,
            "text": mensagem_corretor
        }

        headers = {
            "apikey": evolution_api_key,
            "Content-Type": "application/json"
        }

        url = f"{evolution_url}/message/sendText/{evolution_instance}"

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            resultado = response.status_code in [200, 201]
        except Exception as e:
            print(f"❌ Erro ao enviar notificação: {e}")
            resultado = False

        if resultado:
            print(f"✅ Corretor notificado sobre agendamento ({cliente_numero})")
        else:
            print(f"⚠️ Falha ao notificar corretor ({cliente_numero})")

    except Exception as e:
        print(f"❌ Erro ao notificar corretor: {e}")


def _buscar_nome_cliente(cliente_numero: str, config: Dict) -> Optional[str]:
    """
    Busca nome do cliente no Chatwoot

    Args:
        cliente_numero: Número do cliente
        config: Config com dados do Chatwoot

    Returns:
        Nome do cliente ou None
    """
    try:
        import requests

        chatwoot = config.get('chatwoot', {})
        api_url = chatwoot.get('url', '').rstrip('/')
        api_token = chatwoot.get('token', '')
        account_id = chatwoot.get('account_id', '')

        if not all([api_url, api_token, account_id]):
            return None

        # Busca conversas
        url = f"{api_url}/api/v1/accounts/{account_id}/conversations"
        headers = {'api_access_token': api_token}

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            conversations = response.json().get('data', {}).get('payload', [])

            for conv in conversations:
                contact = conv.get('meta', {}).get('sender', {})
                phone = contact.get('phone_number', '').replace('+', '')

                if phone == cliente_numero:
                    nome = contact.get('name', '')
                    return nome if nome else None

        return None

    except Exception as e:
        print(f"⚠️ Erro ao buscar nome no Chatwoot: {e}")
        return None


def _formatar_telefone(numero: str) -> str:
    """
    Formata número de telefone brasileiro

    Args:
        numero: Número completo (ex: 5531999999999)

    Returns:
        Número formatado (ex: +55 (31) 99999-9999)
    """
    try:
        if len(numero) >= 13:  # 5531999999999
            ddi = numero[:2]
            ddd = numero[2:4]
            parte1 = numero[4:9]
            parte2 = numero[9:]
            return f"+{ddi} ({ddd}) {parte1}-{parte2}"
        return numero
    except:
        return numero


def _extrair_detalhes_imovel(imovel_id: Optional[str]) -> Dict:
    """
    Extrai TODOS os detalhes do imóvel do base.txt

    Args:
        imovel_id: ID do imóvel

    Returns:
        Dict com: titulo, preco, condicoes, tipo, area, localizacao
    """
    detalhes = {
        'titulo': 'Imóvel não especificado',
        'preco': 'A consultar',
        'condicoes': 'A consultar',
        'tipo': 'imóvel',
        'area': '',
        'localizacao': ''
    }

    if not imovel_id:
        return detalhes

    try:
        imoveis_dir = Path(__file__).parent.parent / "imoveis"
        base_file = imoveis_dir / imovel_id / "base.txt"

        if not base_file.exists():
            return detalhes

        with open(base_file, 'r', encoding='utf-8') as f:
            conteudo = f.read()

        import re

        # Extrai título (primeira linha)
        primeira_linha = conteudo.split('\n')[0].strip()
        if primeira_linha and not primeira_linha.startswith('-'):
            detalhes['titulo'] = primeira_linha.split(' - ID:')[0]

        # Extrai tipo (ex: Chácara, Casa, Apartamento)
        tipo_match = re.search(r'^([A-ZÀÁÉÍÓÚ\s]+)', primeira_linha)
        if tipo_match:
            detalhes['tipo'] = tipo_match.group(1).strip()

        # Extrai área/tamanho
        area_match = re.search(r'Tamanho:\s*(.+)', conteudo)
        if area_match:
            detalhes['area'] = area_match.group(1).strip()

        # Extrai localização
        regiao_match = re.search(r'Região:\s*(.+)', conteudo)
        if regiao_match:
            detalhes['localizacao'] = regiao_match.group(1).strip()

        # Extrai valores
        valores_section = re.search(r'VALORES\n(.+?)(?:\n\n|\nDOCUMENTAÇÃO)', conteudo, re.DOTALL)
        if valores_section:
            valores_texto = valores_section.group(1)

            # Busca primeiro plano
            plano1 = re.search(r'Plano 1:\s*(.+)', valores_texto)
            avista = re.search(r'À vista:\s*(.+)', valores_texto)

            if plano1:
                condicao_completa = plano1.group(1).strip()
                # Extrai entrada e parcelas
                entrada_match = re.search(r'R\$\s*([\d.,k]+)', condicao_completa)
                parcelas_match = re.search(r'(\d+)x\s*R\$\s*([\d.,]+)', condicao_completa)

                if entrada_match and parcelas_match:
                    entrada = entrada_match.group(1)
                    num_parcelas = parcelas_match.group(1)
                    valor_parcela = parcelas_match.group(2)

                    detalhes['preco'] = f"Entrada: R$ {entrada} + {num_parcelas}x R$ {valor_parcela}"
                    detalhes['condicoes'] = f"R$ {entrada} de entrada + {num_parcelas} parcelas de R$ {valor_parcela}"
                else:
                    detalhes['preco'] = condicao_completa

            if avista:
                valor_avista = avista.group(1).strip()
                detalhes['preco'] += f" | À vista: {valor_avista}"

        # Monta título completo
        titulo_parts = [detalhes['tipo']]
        if detalhes['localizacao']:
            titulo_parts.append(detalhes['localizacao'])
        if detalhes['area']:
            titulo_parts.append(f"({detalhes['area']})")

        if len(titulo_parts) > 1:
            detalhes['titulo'] = ' - '.join(titulo_parts)

    except Exception as e:
        print(f"⚠️ Erro ao extrair detalhes do imóvel: {e}")

    return detalhes


def _gerar_resumo_conversa_ia(
    cliente_numero: str,
    redis_client: Redis,
    tipo_imovel: str
) -> str:
    """
    Gera resumo da conversa usando Claude Haiku via OpenRouter

    Args:
        cliente_numero: Número do cliente
        redis_client: Cliente Redis
        tipo_imovel: Tipo do imóvel (para contexto)

    Returns:
        Resumo de 3-4 linhas ou mensagem simples em caso de erro
    """
    try:
        import requests

        # Busca contexto do Redis
        contexto_key = f"contexto:imobiliaria:{cliente_numero}"
        contexto = redis_client.get(contexto_key)

        if not contexto:
            return "• Cliente demonstrou interesse no imóvel\n• Solicitou agendamento de visita"

        # Limita contexto a últimas 3000 caracteres (evitar excesso)
        contexto_limitado = contexto[-3000:] if len(contexto) > 3000 else contexto

        # Chama Claude Haiku via OpenRouter
        OPENROUTER_API_KEY = "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"

        prompt = f"""Analise esta conversa entre cliente e chatbot de imobiliária sobre um {tipo_imovel}.

CONTEXTO DA CONVERSA:
{contexto_limitado}

TAREFA: Gere um resumo ULTRA-CONCISO (máximo 300 caracteres) no formato:

• Principais dúvidas: [lista 2-3 pontos principais]
• Interesse: [o que mais chamou atenção]
• Urgência: [baixa/média/alta]

REGRAS:
- Máximo 300 caracteres TOTAL
- Formato bullet points
- Foco no que MAIS importa para o corretor
- Se não houver informação suficiente, seja genérico mas útil"""

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "anthropic/claude-3.5-haiku",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 200,
                "temperature": 0.3
            },
            timeout=15
        )

        if response.status_code == 200:
            resumo = response.json()['choices'][0]['message']['content'].strip()
            # Garante limite de 300 caracteres
            if len(resumo) > 300:
                resumo = resumo[:297] + "..."
            return resumo
        else:
            print(f"⚠️ OpenRouter erro: {response.status_code}")
            return "• Cliente demonstrou interesse no imóvel\n• Principais dúvidas não registradas\n• Urgência: média"

    except Exception as e:
        print(f"⚠️ Erro ao gerar resumo com IA: {e}")
        return "• Cliente demonstrou interesse no imóvel\n• Solicitou agendamento de visita\n• Urgência: a avaliar"


# TESTE LOCAL
if __name__ == "__main__":
    print("🗓️ Ferramenta: Agendar Visita")
    print("\nTeste 1: Sugerir horários")

    # Mock Redis
    class MockRedis:
        def __init__(self):
            self.data = {}

        def get(self, key):
            return self.data.get(key)

        def setex(self, key, ttl, value):
            self.data[key] = value

        def delete(self, key):
            if key in self.data:
                del self.data[key]

    redis_mock = MockRedis()
    config_mock = {
        'chatwoot': {'url': '', 'token': '', 'account_id': ''},
        'evolution': {'url': '', 'api_key': '', 'instance': ''}
    }

    # Teste sugerir
    resultado = agendar_visita_corretor(
        acao="sugerir",
        cliente_numero="5531999999999",
        redis_client=redis_mock,
        config=config_mock
    )

    print(f"\n📋 Resultado:\n{resultado}")


# ALIAS para compatibilidade com outros arquivos
agendar_visita_imovel = agendar_visita_corretor
