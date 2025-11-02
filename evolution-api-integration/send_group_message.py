"""
Script para enviar mensagem no grupo
"""

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME

# Inicializa a API
api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

# ID do grupo
group_id = "120363406126089260@g.us"

print("=" * 60)
print("ENVIANDO MENSAGEM NO GRUPO")
print("=" * 60)
print(f"\nGrupo ID: {group_id}")

try:
    # Enviar mensagem no grupo
    print("\nEnviando mensagem de boas-vindas...")

    response = api.send_text(
        number=group_id,
        text="🎉 *Bem-vindo ao Grupo Teste Evolution API!*\n\n✅ Este grupo foi criado automaticamente\n✅ Você é administrador\n✅ Apenas admins podem enviar mensagens\n\nGrupo configurado com sucesso via Evolution API! 🚀"
    )

    print("\n✅ MENSAGEM ENVIADA NO GRUPO COM SUCESSO!")
    print(f"\nResposta: {response}")

except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
