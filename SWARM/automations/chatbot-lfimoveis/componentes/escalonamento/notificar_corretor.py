"""Notifica corretor Luciano sobre agendamentos"""
import requests

CORRETOR_WHATSAPP = "5531980160822"
EVOLUTION_URL = "https://evolution.loop9.com.br"
EVOLUTION_API_KEY = "178e43e1c4f459527e7008e57e378e1c"
EVOLUTION_INSTANCE = "lfimoveis"

def notificar_corretor(cliente_nome, cliente_numero, data_hora, imovel):
    """Envia notificação para o corretor via WhatsApp"""
    mensagem = f"""
🔔 *NOVA VISITA AGENDADA*

👤 Cliente: {cliente_nome}
📱 Telefone: {cliente_numero}
📅 Data/Hora: {data_hora}
🏡 Imóvel: {imovel}

_Mensagem automática do Bot LF Imóveis_
"""

    url = f"{EVOLUTION_URL}/message/sendText/{EVOLUTION_INSTANCE}"
    headers = {"apikey": EVOLUTION_API_KEY}
    data = {
        "number": CORRETOR_WHATSAPP,
        "text": mensagem
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro ao notificar corretor: {e}")
        return False
