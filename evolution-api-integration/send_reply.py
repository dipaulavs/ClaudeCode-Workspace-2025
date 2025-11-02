"""
Script para responder a mensagem anterior
"""

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME

# Inicializa a API
api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

# Dados da resposta
numero = "5531980160822"
message_id = "3EB0F92BACE4D8DDDB7CE9B94D5B9C610DFBF521"  # ID da mensagem anterior
mensagem_resposta = "Como você está? Espero que esteja tudo bem! 😊"

print("=" * 60)
print("RESPONDENDO MENSAGEM ANTERIOR")
print("=" * 60)
print(f"\nNúmero: {numero}")
print(f"ID da mensagem original: {message_id}")
print(f"Resposta: {mensagem_resposta}")
print("\nEnviando resposta...")

try:
    response = api.send_reply(
        number=numero,
        text=mensagem_resposta,
        message_id=message_id
    )
    print("\n✅ RESPOSTA ENVIADA COM SUCESSO!")
    print(f"\nResposta da API:")
    print(response)
except Exception as e:
    print(f"\n❌ ERRO: {e}")
