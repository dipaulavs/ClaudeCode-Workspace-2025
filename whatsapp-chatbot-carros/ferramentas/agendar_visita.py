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
        # Busca carro ativo (se houver)
        carro_id = None
        try:
            carro_ativo = redis_client.get(f"carro_ativo:automaia:{cliente_numero}")
            if carro_ativo:
                carro_id = carro_ativo
        except Exception as e:
            print(f"⚠️ Erro ao buscar carro ativo: {e}")

        # Chama integrador para sugerir horários
        mensagem = integrador.sugerir_horarios(cliente_numero, carro_id)

        print(f"📅 Horários sugeridos para {cliente_numero}")
        return mensagem

    # AÇÃO: CONFIRMAR AGENDAMENTO
    elif acao == "confirmar":
        if not escolha:
            return "❌ Preciso que você escolha um dos números (1, 2 ou 3)"

        # Busca carro ativo
        carro_id = None
        try:
            carro_ativo = redis_client.get(f"carro_ativo:automaia:{cliente_numero}")
            if carro_ativo:
                carro_id = carro_ativo
        except Exception as e:
            print(f"⚠️ Erro ao buscar carro ativo: {e}")

        # Confirma agendamento
        sucesso, mensagem = integrador.confirmar_agendamento(
            cliente_numero,
            escolha,
            carro_id
        )

        if sucesso:
            print(f"✅ Agendamento confirmado para {cliente_numero}")

            # NOTIFICA VENDEDOR
            _notificar_vendedor_agendamento(
                cliente_numero,
                carro_id,
                mensagem,
                redis_client,
                config
            )
        else:
            print(f"⚠️ Erro ao agendar para {cliente_numero}")

        return mensagem

    else:
        return f"❌ Ação inválida: {acao}. Use 'sugerir' ou 'confirmar'"


def _notificar_vendedor_agendamento(
    cliente_numero: str,
    carro_id: Optional[str],
    mensagem_confirmacao: str,
    redis_client: Redis,
    config: Dict
):
    """
    Notifica vendedor sobre novo agendamento via WhatsApp

    Args:
        cliente_numero: Número do cliente
        carro_id: ID do carro de interesse
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

        # 2. BUSCA INFO DO CARRO
        info_carro = "Não definido"
        if carro_id:
            try:
                carros_dir = Path(__file__).parent.parent / "carros"
                base_file = carros_dir / carro_id / "base.txt"
                if base_file.exists():
                    with open(base_file, 'r') as f:
                        conteudo = f.read()
                        # Extrai marca e modelo
                        import re
                        marca = re.search(r'Marca:\s*(.+)', conteudo)
                        modelo = re.search(r'Modelo:\s*(.+)', conteudo)
                        ano = re.search(r'Ano:\s*(.+)', conteudo)

                        if marca and modelo:
                            info_carro = f"{marca.group(1)} {modelo.group(1)}"
                            if ano:
                                info_carro += f" {ano.group(1)}"
            except Exception as e:
                print(f"⚠️ Erro ao buscar info do carro: {e}")

        # 3. EXTRAI HORÁRIO DA MENSAGEM DE CONFIRMAÇÃO
        # Mensagem formato: "✅ *Agendado!*\n\n📅 DD/MM/YYYY às HH:MM"
        import re
        horario_match = re.search(r'📅\s*(.+?)\s*às\s*(.+)', mensagem_confirmacao)
        data_hora = "Não especificado"
        if horario_match:
            data_hora = f"{horario_match.group(1)} às {horario_match.group(2)}"

        # 4. MONTA MENSAGEM PARA VENDEDOR
        # Vendedor padrão (em produção, buscar da atribuição)
        vendedor_whatsapp = "5531999999999"  # TODO: buscar vendedor atribuído

        mensagem_vendedor = f"""
🗓️ *NOVA VISITA AGENDADA*

📱 *Cliente:* {nome_cliente or cliente_numero}
🚗 *Veículo:* {info_carro}
📊 *Score:* {score} - {classificacao}

📅 *Data/Hora:* {data_hora}

🔔 *Lembrete:* Confirme presença com cliente 1 dia antes!
        """.strip()

        # 5. ENVIA VIA EVOLUTION API
        from tools.send_message_evolution import enviar_mensagem

        resultado = enviar_mensagem(
            numero_destino=vendedor_whatsapp,
            mensagem=mensagem_vendedor
        )

        if resultado:
            print(f"✅ Vendedor notificado sobre agendamento ({cliente_numero})")
        else:
            print(f"⚠️ Falha ao notificar vendedor ({cliente_numero})")

    except Exception as e:
        print(f"❌ Erro ao notificar vendedor: {e}")


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
