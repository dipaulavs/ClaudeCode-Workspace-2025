#!/usr/bin/env python3
"""
🗓️ FERRAMENTA: AGENDAR VISITA
Consulta agenda do vendedor e agenda visitas

WORKFLOW:
1. Cliente pede pra agendar → Bot sugere horários
2. Cliente escolhe (1, 2, 3) → Bot confirma + notifica vendedor
"""

from pathlib import Path
from typing import Dict, Optional
import json
from upstash_redis import Redis


def agendar_visita_vendedor(
    acao: str,
    cliente_numero: str,
    redis_client: Redis,
    config: Dict,
    escolha: Optional[str] = None
) -> str:
    """
    Gerencia agendamento de visita com vendedor

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
        >>> agendar_visita_vendedor("sugerir", "5531999999999", redis, config)
        "Posso agendar pra:\\n1️⃣ Amanhã às 10h\\n2️⃣ Quarta às 14h..."

        # Confirmar escolha
        >>> agendar_visita_vendedor("confirmar", "5531999999999", redis, config, escolha="1")
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

    Args:
        cliente_numero: Número do cliente
        imovel_id: ID do imóvel de interesse
        mensagem_confirmacao: Mensagem de confirmação enviada ao cliente
        redis_client: Cliente Redis
        config: Config completo
    """
    try:
        # 1. BUSCA DADOS DO CLIENTE
        # Nome do cliente (se tiver no Chatwoot)
        nome_cliente = _buscar_nome_cliente(cliente_numero, config)

        # Score do cliente
        score_key = f"score:{cliente_numero}"
        score = redis_client.get(score_key) or "0"

        # Classificação
        score_int = int(score)
        if score_int >= 70:
            classificacao = "🔥 LEAD QUENTE"
        elif score_int >= 40:
            classificacao = "🌡️ Lead Morno"
        else:
            classificacao = "❄️ Lead Frio"

        # 2. BUSCA INFO DO IMÓVEL
        info_imovel = "Não definido"
        if imovel_id:
            try:
                imoveis_dir = Path(__file__).parent.parent / "imoveis"
                base_file = imoveis_dir / imovel_id / "base.txt"
                if base_file.exists():
                    with open(base_file, 'r') as f:
                        conteudo = f.read()
                        # Extrai tipo e localização
                        import re
                        tipo = re.search(r'Tipo:\s*(.+)', conteudo)
                        bairro = re.search(r'Bairro:\s*(.+)', conteudo)
                        quartos = re.search(r'Quartos:\s*(.+)', conteudo)

                        if tipo and bairro:
                            info_imovel = f"{tipo.group(1)} - {bairro.group(1)}"
                            if quartos:
                                info_imovel += f" ({quartos.group(1)} quartos)"
            except Exception as e:
                print(f"⚠️ Erro ao buscar info do imóvel: {e}")

        # 3. EXTRAI HORÁRIO DA MENSAGEM DE CONFIRMAÇÃO
        # Mensagem formato: "✅ *Agendado!*\n\n📅 DD/MM/YYYY às HH:MM"
        import re
        horario_match = re.search(r'📅\s*(.+?)\s*às\s*(.+)', mensagem_confirmacao)
        data_hora = "Não especificado"
        if horario_match:
            data_hora = f"{horario_match.group(1)} às {horario_match.group(2)}"

        # 4. MONTA MENSAGEM PARA CORRETOR
        # Corretor padrão (em produção, buscar da atribuição)
        corretor_whatsapp = "5521999999999"  # TODO: buscar corretor atribuído

        mensagem_corretor = f"""
🗓️ *NOVA VISITA AGENDADA*

📱 *Cliente:* {nome_cliente or cliente_numero}
🏠 *Imóvel:* {info_imovel}
📊 *Score:* {score} - {classificacao}

📅 *Data/Hora:* {data_hora}

🔔 *Lembrete:* Confirme presença com cliente 1 dia antes!
        """.strip()

        # 5. ENVIA VIA EVOLUTION API
        from tools.send_message_evolution import enviar_mensagem

        resultado = enviar_mensagem(
            numero_destino=corretor_whatsapp,
            mensagem=mensagem_corretor
        )

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
    resultado = agendar_visita_vendedor(
        acao="sugerir",
        cliente_numero="5531999999999",
        redis_client=redis_mock,
        config=config_mock
    )

    print(f"\n📋 Resultado:\n{resultado}")
