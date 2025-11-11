"""
Script de teste para verificar a conexão com a Evolution API
"""

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


def test_connection():
    """Testa a conexão com a API"""

    print("=" * 60)
    print("TESTE DE CONEXÃO - EVOLUTION API")
    print("=" * 60)

    try:
        # Inicializa a API
        api = EvolutionAPI(
            base_url=EVOLUTION_API_URL,
            api_key=EVOLUTION_API_KEY,
            instance_name=EVOLUTION_INSTANCE_NAME
        )

        print(f"\nURL da API: {EVOLUTION_API_URL}")
        print(f"Instância: {EVOLUTION_INSTANCE_NAME}")
        print("\nVerificando status da instância...")

        # Verifica o status
        status = api.get_instance_status()

        print("\n✅ CONEXÃO ESTABELECIDA COM SUCESSO!")
        print("\nStatus da instância:")
        print(f"  - Estado: {status.get('state', 'Desconhecido')}")
        print(f"  - Instância: {status.get('instance', 'N/A')}")

        # Informações adicionais se disponíveis
        if 'connectionStatus' in status:
            print(f"  - Status de Conexão: {status['connectionStatus']}")

        return True

    except Exception as e:
        print("\n❌ ERRO NA CONEXÃO!")
        print(f"Erro: {str(e)}")
        return False


if __name__ == "__main__":
    test_connection()
