"""
Script para enviar mensagem de teste
"""

from whatsapp_helper import whatsapp

# Enviar mensagem de boa tarde
numero = "5531980160822"
mensagem = "Boa tarde! 😊"

print("=" * 60)
print("ENVIANDO MENSAGEM DE TESTE")
print("=" * 60)
print(f"\nNúmero: {numero}")
print(f"Mensagem: {mensagem}")
print("\nEnviando...")

try:
    response = whatsapp.send_message(numero, mensagem)
    print("\n✅ MENSAGEM ENVIADA COM SUCESSO!")
    print(f"\nResposta da API:")
    print(response)
except Exception as e:
    print(f"\n❌ ERRO: {e}")
