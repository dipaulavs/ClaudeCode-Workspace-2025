"""
Script para enviar status com imagem (corrigido)
"""

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME

# Inicializa a API
api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

# URL da imagem
image_url = "https://picsum.photos/800/600"

print("=" * 60)
print("ENVIANDO STATUS COM IMAGEM")
print("=" * 60)
print(f"\nURL: {image_url}")
print("\nEnviando status...")

try:
    # Envia como status com allContacts=False e lista específica
    response = api.send_status(
        content=image_url,
        type="image",
        all_contacts=False,  # Envia apenas para a lista abaixo
        status_jid_list=["5531980160822"],  # Seu número
        caption="Status enviado via Evolution API! 🚀"
    )

    print("\n✅ STATUS PUBLICADO COM SUCESSO!")
    print(f"\nResposta da API:")
    print(response)
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
