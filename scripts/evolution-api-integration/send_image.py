"""
Script para enviar foto como mensagem
"""

from whatsapp_helper import whatsapp

# Caminho da imagem
image_path = "/Users/felipemdepaula/Downloads/Claude Code Chat.png"
numero = "5531980160822"

print("=" * 60)
print("ENVIANDO FOTO")
print("=" * 60)
print(f"\nArquivo: {image_path}")
print(f"Para: {numero}")
print("\nEnviando...")

try:
    response = whatsapp.send_image(
        number=numero,
        image_url=image_path,
        caption="Aqui está a foto mais recente dos seus Downloads! 📸"
    )

    print("\n✅ FOTO ENVIADA COM SUCESSO!")
    print(f"\nResposta:")
    print(response)
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
