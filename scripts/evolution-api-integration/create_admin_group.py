"""
Script para criar grupo com configurações específicas
"""

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME
import time

# Inicializa a API
api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

# Número a adicionar
numero = "5531980160822"

print("=" * 60)
print("CRIANDO GRUPO COM CONFIGURAÇÕES")
print("=" * 60)

try:
    # 1. Criar o grupo
    print("\n1. Criando grupo...")
    grupo = api.create_group(
        subject="Grupo Teste Evolution API",
        participants=[numero],
        description="Grupo de teste criado via Evolution API"
    )

    group_id = grupo.get('id') or grupo.get('groupJid')
    print(f"✅ Grupo criado!")
    print(f"   ID: {group_id}")
    print(f"   Nome: {grupo.get('subject', 'N/A')}")

    # Aguarda um pouco para garantir que o grupo foi criado
    time.sleep(2)

    # 2. Promover o participante a administrador
    print(f"\n2. Promovendo {numero} a administrador...")
    promote_response = api.promote_participant(
        group_id=group_id,
        participants=[numero]
    )
    print(f"✅ Promovido a administrador!")

    # Aguarda um pouco
    time.sleep(2)

    # 3. Configurar grupo para apenas admins enviarem mensagens
    print("\n3. Configurando grupo para apenas admins enviarem mensagens...")

    # Vou fazer a requisição direta para configurar as permissões do grupo
    endpoint = f"/group/updateSetting/{api.instance_name}"
    settings_data = {
        "groupJid": group_id,
        "action": "announcement"  # announcement = apenas admins podem enviar
    }

    settings_response = api._make_request('PUT', endpoint, settings_data)
    print(f"✅ Grupo configurado para apenas admins!")

    print("\n" + "=" * 60)
    print("✅ GRUPO CRIADO E CONFIGURADO COM SUCESSO!")
    print("=" * 60)
    print(f"\nResumo:")
    print(f"  - Nome: Grupo Teste Evolution API")
    print(f"  - ID: {group_id}")
    print(f"  - Participante: {numero}")
    print(f"  - Status: Administrador")
    print(f"  - Configuração: Apenas admins podem enviar mensagens")

except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
