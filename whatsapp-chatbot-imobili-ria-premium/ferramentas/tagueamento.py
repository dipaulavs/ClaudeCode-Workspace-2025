#!/usr/bin/env python3
"""
🔧 FERRAMENTA: Tagueamento Chatwoot + Redis

Marca cliente como interessado em carro específico:
1. Cria tag no Chatwoot (ex: "interessado_gol_2020")
2. Salva carro ativo no Redis
"""

import requests
import json
from typing import Dict, Optional
from pathlib import Path


def taguear_cliente(
    numero_cliente: str,
    carro_id: str,
    redis_client,
    chatwoot_config: Dict
) -> Dict:
    """
    Tageia cliente no Chatwoot e marca carro ativo no Redis

    Args:
        numero_cliente: Número do cliente (ex: "5531986549366")
        carro_id: ID do carro (ex: "gol-2020-001")
        redis_client: Cliente Redis (upstash_redis.Redis)
        chatwoot_config: Dict com config Chatwoot

    Returns:
        Dict com:
            - sucesso: bool
            - tag_criada: str
            - redis_salvo: bool
            - erro: str (se houver)
    """
    resultado = {
        "sucesso": False,
        "tag_criada": "",
        "redis_salvo": False,
        "erro": ""
    }

    # 1. SALVA NO REDIS (prioridade - funciona offline)
    try:
        chave_redis = f"carro_ativo:automaia:{numero_cliente}"
        redis_client.setex(chave_redis, 86400, carro_id)  # 24h TTL
        resultado["redis_salvo"] = True
        print(f"✅ Redis: Carro ativo salvo ({carro_id})", flush=True)
    except Exception as e:
        resultado["erro"] += f"Erro Redis: {e}\n"
        print(f"⚠️ Erro ao salvar no Redis: {e}", flush=True)

    # 2. CRIA TAG NO CHATWOOT (melhor esforço)
    try:
        # Formata nome da tag
        tag_nome = f"interessado_{carro_id}".replace("-", "_")

        # Busca conversa do cliente
        conversation_id = _buscar_conversation_id(numero_cliente, chatwoot_config)

        if not conversation_id:
            resultado["erro"] += "Conversa não encontrada no Chatwoot\n"
            print(f"⚠️ Conversa não encontrada para {numero_cliente}", flush=True)
        else:
            # Adiciona tag na conversa
            sucesso_tag = _adicionar_tag_conversa(
                conversation_id,
                tag_nome,
                chatwoot_config
            )

            if sucesso_tag:
                resultado["tag_criada"] = tag_nome
                print(f"✅ Chatwoot: Tag '{tag_nome}' adicionada", flush=True)
            else:
                resultado["erro"] += "Falha ao adicionar tag no Chatwoot\n"
                print(f"⚠️ Falha ao adicionar tag no Chatwoot", flush=True)

    except Exception as e:
        resultado["erro"] += f"Erro Chatwoot: {e}\n"
        print(f"⚠️ Erro no Chatwoot: {e}", flush=True)

    # Se Redis salvou, consideramos sucesso (tag é opcional)
    if resultado["redis_salvo"]:
        resultado["sucesso"] = True

    return resultado


def obter_carro_ativo(numero_cliente: str, redis_client) -> Optional[str]:
    """
    Obtém carro ativo do cliente no Redis

    Args:
        numero_cliente: Número do cliente
        redis_client: Cliente Redis

    Returns:
        carro_id ou None
    """
    try:
        chave_redis = f"carro_ativo:automaia:{numero_cliente}"
        carro_id = redis_client.get(chave_redis)

        if carro_id:
            # Upstash Redis já retorna string decodificada
            return carro_id if isinstance(carro_id, str) else carro_id.decode()

        return None

    except Exception as e:
        print(f"⚠️ Erro ao obter carro ativo: {e}", flush=True)
        return None


def limpar_carro_ativo(numero_cliente: str, redis_client) -> bool:
    """
    Limpa carro ativo do cliente (útil para reset)

    Args:
        numero_cliente: Número do cliente
        redis_client: Cliente Redis

    Returns:
        bool (sucesso)
    """
    try:
        chave_redis = f"carro_ativo:automaia:{numero_cliente}"
        redis_client.delete(chave_redis)
        print(f"✅ Carro ativo limpo para {numero_cliente}", flush=True)
        return True
    except Exception as e:
        print(f"⚠️ Erro ao limpar carro ativo: {e}", flush=True)
        return False


def _buscar_conversation_id(numero_cliente: str, chatwoot_config: Dict) -> Optional[int]:
    """Busca ID da conversa do cliente no Chatwoot"""
    try:
        # Busca contato
        url = f"{chatwoot_config['url']}/api/v1/accounts/{chatwoot_config['account_id']}/contacts/search"
        headers = {"api_access_token": chatwoot_config['token']}
        params = {"q": numero_cliente}

        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code != 200:
            return None

        contacts = response.json().get('payload', [])
        if not contacts:
            return None

        contact_id = contacts[0]['id']

        # Busca conversas abertas do contato
        url = f"{chatwoot_config['url']}/api/v1/accounts/{chatwoot_config['account_id']}/conversations"
        params = {"inbox_id": chatwoot_config['inbox_id'], "status": "open"}

        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code != 200:
            return None

        conversations = response.json().get('data', {}).get('payload', [])

        for conv in conversations:
            if conv.get('meta', {}).get('sender', {}).get('id') == contact_id:
                return conv['id']

        return None

    except Exception as e:
        print(f"⚠️ Erro ao buscar conversation_id: {e}", flush=True)
        return None


def _adicionar_tag_conversa(conversation_id: int, tag_nome: str, chatwoot_config: Dict) -> bool:
    """Adiciona tag em uma conversa do Chatwoot"""
    try:
        url = f"{chatwoot_config['url']}/api/v1/accounts/{chatwoot_config['account_id']}/conversations/{conversation_id}/labels"

        headers = {
            "api_access_token": chatwoot_config['token'],
            "Content-Type": "application/json"
        }

        payload = {"labels": [tag_nome]}

        response = requests.post(url, headers=headers, json=payload, timeout=10)

        return response.status_code in [200, 201]

    except Exception as e:
        print(f"⚠️ Erro ao adicionar tag: {e}", flush=True)
        return False


if __name__ == "__main__":
    # Teste standalone
    print("🧪 Testando tagueamento.py...\n")

    from upstash_redis import Redis

    # Carrega config
    config_path = Path(__file__).parent.parent / "chatwoot_config_automaia.json"

    if not config_path.exists():
        print("❌ Arquivo chatwoot_config_automaia.json não encontrado")
        exit(1)

    with open(config_path, 'r') as f:
        config = json.load(f)

    # Redis
    redis = Redis(
        url="https://legible-collie-9537.upstash.io",
        token="ASVBAAImcDFiOTlmYTM1MTdkNzg0MWU3OTI5YmU4N2RmZmU5ZmJkZnAxOTUzNw"
    )

    # Teste
    numero_teste = "5531999999999"
    carro_teste = "gol-2020-001"

    print(f"📋 Teste: Taguear {numero_teste} com {carro_teste}")
    print("-" * 50)

    resultado = taguear_cliente(
        numero_teste,
        carro_teste,
        redis,
        config['chatwoot']
    )

    print(f"\n✅ Resultado:")
    print(f"   Sucesso: {resultado['sucesso']}")
    print(f"   Tag criada: {resultado['tag_criada']}")
    print(f"   Redis salvo: {resultado['redis_salvo']}")
    if resultado['erro']:
        print(f"   Erros: {resultado['erro']}")

    # Teste obter carro ativo
    print(f"\n📋 Teste: Obter carro ativo")
    print("-" * 50)

    carro_ativo = obter_carro_ativo(numero_teste, redis)
    print(f"   Carro ativo: {carro_ativo}")

    # Limpa
    print(f"\n📋 Teste: Limpar carro ativo")
    print("-" * 50)

    sucesso = limpar_carro_ativo(numero_teste, redis)
    print(f"   Limpo: {sucesso}")
