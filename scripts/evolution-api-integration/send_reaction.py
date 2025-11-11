"""
Script para reagir a uma mensagem
"""

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME

# Inicializa a API
api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

# Dados da reação
numero = "5531980160822"
message_id = "3EB0404D20F5761B2B9E4763C6AFDA7ACE1CF03D"  # ID da última mensagem
reacao = "🚀"  # Emoji de foguete

print("=" * 60)
print("REAGINDO À MENSAGEM")
print("=" * 60)
print(f"\nNúmero: {numero}")
print(f"ID da mensagem: {message_id}")
print(f"Reação: {reacao}")
print("\nEnviando reação...")

try:
    response = api.send_reaction(
        number=numero,
        key=message_id,
        reaction=reacao
    )
    print(f"\n✅ REAÇÃO {reacao} ENVIADA COM SUCESSO!")
    print(f"\nResposta da API:")
    print(response)
except Exception as e:
    print(f"\n❌ ERRO: {e}")
