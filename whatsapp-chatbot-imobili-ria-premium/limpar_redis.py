#!/usr/bin/env python3
"""
🧹 LIMPAR REDIS - Remove todos os dados do Upstash Redis
"""

from upstash_redis import Redis

# Credenciais Upstash
redis = Redis(
    url="https://legible-collie-9537.upstash.io",
    token="ASVBAAImcDFiOTlmYTM1MTdkNzg0MWU3OTI5YmU4N2RmZmU5ZmJkZnAxOTUzNw"
)

def limpar_redis():
    """Limpa todos os dados do Redis"""
    print("\n🧹 LIMPANDO REDIS...")
    print("=" * 60)

    try:
        # Conta chaves antes
        keys_antes = redis.dbsize()
        print(f"\n📊 Chaves antes: {keys_antes}")

        # Limpa tudo
        redis.flushdb()

        # Verifica
        keys_depois = redis.dbsize()
        print(f"📊 Chaves depois: {keys_depois}")

        print("\n✅ Redis limpo com sucesso!")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\n❌ Erro ao limpar Redis: {e}")
        return False


if __name__ == '__main__':
    limpar_redis()
