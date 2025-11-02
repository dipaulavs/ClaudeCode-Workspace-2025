"""
Teste: Enviar imagem usando URL pública
"""

from whatsapp_helper import whatsapp

# URL de uma imagem pública de teste
image_url = "https://picsum.photos/800/600"
numero = "5531980160822"

print("=" * 60)
print("ENVIANDO FOTO VIA URL")
print("=" * 60)
print(f"\nURL: {image_url}")
print(f"Para: {numero}")
print("\nEnviando...")

try:
    response = whatsapp.send_image(
        number=numero,
        image_url=image_url,
        caption="Teste de envio de imagem via URL 📸"
    )

    print("\n✅ FOTO ENVIADA COM SUCESSO!")
    print(f"\nResposta:")
    print(response)
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
