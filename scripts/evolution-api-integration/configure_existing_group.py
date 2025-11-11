"""
Script para configurar grupo existente
"""

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME
import time

# Inicializa a API
api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

# ID do grupo criado
group_id = "120363406126089260@g.us"
numero = "5531980160822"

print("=" * 60)
print("CONFIGURANDO GRUPO EXISTENTE")
print("=" * 60)
print(f"\nGrupo ID: {group_id}")

try:
    # 1. Promover o participante a administrador
    print(f"\n1. Promovendo {numero} a administrador...")
    promote_response = api.promote_participant(
        group_id=group_id,
        participants=[numero]
    )
    print(f"✅ Promovido a administrador!")
    print(f"Resposta: {promote_response}")

    # Aguarda um pouco
    time.sleep(2)

    # 2. Configurar grupo para apenas admins enviarem mensagens
    print("\n2. Configurando grupo para apenas admins enviarem mensagens...")

    endpoint = f"/group/updateSetting/{api.instance_name}"
    settings_data = {
        "groupJid": group_id,
        "action": "announcement"  # announcement = apenas admins podem enviar
    }

    settings_response = api._make_request('PUT', endpoint, settings_data)
    print(f"✅ Grupo configurado para apenas admins!")
    print(f"Resposta: {settings_response}")

    print("\n" + "=" * 60)
    print("✅ GRUPO CONFIGURADO COM SUCESSO!")
    print("=" * 60)
    print(f"\nResumo:")
    print(f"  - ID: {group_id}")
    print(f"  - Admin: {numero}")
    print(f"  - Configuração: Apenas admins podem enviar mensagens")

except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
