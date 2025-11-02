"""
Script para enviar foto como status (corrigido)
"""

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME
import base64

# Inicializa a API
api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

# Caminho da imagem
image_path = "/Users/felipemdepaula/Downloads/Claude Code Chat.png"

print("=" * 60)
print("ENVIANDO FOTO COMO STATUS")
print("=" * 60)
print(f"\nArquivo: {image_path}")
print("\nConvertendo para base64 e enviando...")

try:
    # Lê e converte a imagem para base64
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
        image_url = f"data:image/png;base64,{image_data}"

    # Envia como status com lista de contatos
    response = api.send_status(
        content=image_url,
        type="image",
        status_jid_list=["5531980160822"]  # Seu número na lista
    )

    print("\n✅ STATUS PUBLICADO COM SUCESSO!")
    print(f"\nResposta da API:")
    print(response)
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
