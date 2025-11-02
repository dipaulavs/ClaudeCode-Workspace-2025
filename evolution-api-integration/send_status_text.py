"""
Script para enviar status de texto
"""

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME

# Inicializa a API
api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

print("=" * 60)
print("ENVIANDO STATUS DE TEXTO")
print("=" * 60)
print("\nEnviando status de texto...")

try:
    # Envia status de texto
    response = api.send_status(
        content="Olá! Este é um status de texto enviado via Evolution API! 🚀",
        type="text",
        background_color="#FF5733",  # Cor laranja
        font=2,  # NORICAN_REGULAR
        all_contacts=False,
        status_jid_list=["5531980160822"]
    )

    print("\n✅ STATUS DE TEXTO PUBLICADO COM SUCESSO!")
    print(f"\nResposta da API:")
    print(response)
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
