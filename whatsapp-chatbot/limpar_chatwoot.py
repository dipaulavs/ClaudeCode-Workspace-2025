#!/usr/bin/env python3
"""
🧹 Script de Limpeza Completa do Chatwoot

Deleta:
- Todas conversas de todas inboxes
- Inboxes inúteis (mantém apenas LF IMOVEIS ID 40)
"""

import requests
import json
import time

# Carregar config
with open('chatwoot_config.json', 'r') as f:
    config = json.load(f)

url = config['chatwoot']['url']
token = config['chatwoot']['token']
account_id = config['chatwoot']['account_id']

headers = {'api_access_token': token}

print("🧹 LIMPEZA COMPLETA DO CHATWOOT")
print("=" * 80)

# 1. DELETAR TODAS AS CONVERSAS
print("\n📋 FASE 1: Deletando todas conversas...")
print("-" * 80)

# Buscar todas inboxes
inboxes_response = requests.get(
    f'{url}/api/v1/accounts/{account_id}/inboxes',
    headers=headers
)

if not inboxes_response.ok:
    print(f"❌ Erro ao buscar inboxes: {inboxes_response.status_code}")
    exit(1)

inboxes = inboxes_response.json()['payload']
total_conversas_deletadas = 0

for inbox in inboxes:
    inbox_id = inbox['id']
    inbox_name = inbox['name']

    print(f"\n📬 Processando inbox: {inbox_name} (ID {inbox_id})")

    # Buscar todas conversas dessa inbox
    conv_response = requests.get(
        f'{url}/api/v1/accounts/{account_id}/conversations',
        params={'inbox_id': inbox_id, 'status': 'all'},
        headers=headers
    )

    if not conv_response.ok:
        print(f"   ⚠️  Erro ao buscar conversas: {conv_response.status_code}")
        continue

    conversations = conv_response.json()['data']['payload']

    if not conversations:
        print(f"   ✓ Nenhuma conversa para deletar")
        continue

    print(f"   Encontradas {len(conversations)} conversas para deletar...")

    # Deletar cada conversa
    for i, conv in enumerate(conversations, 1):
        conv_id = conv['id']

        # Tentar deletar (pode não ter endpoint direto, então vamos resolver)
        # API do Chatwoot não tem DELETE conversation, então vamos RESOLVER todas
        resolve_response = requests.post(
            f'{url}/api/v1/accounts/{account_id}/conversations/{conv_id}/toggle_status',
            headers=headers
        )

        if resolve_response.ok:
            print(f"   ✓ Conversa {i}/{len(conversations)} resolvida (ID {conv_id})")
            total_conversas_deletadas += 1
        else:
            print(f"   ✗ Erro ao resolver conversa {conv_id}: {resolve_response.status_code}")

        # Rate limit (evitar sobrecarga)
        time.sleep(0.1)

print(f"\n✅ Total de conversas resolvidas: {total_conversas_deletadas}")

# 2. DELETAR INBOXES INÚTEIS
print("\n📬 FASE 2: Deletando inboxes inúteis...")
print("-" * 80)

INBOXES_PARA_DELETAR = [37, 38, 39, 41]  # TESTEBOX, POWERPOINT, PLENUM, LF IMOVEIS2
INBOX_MANTER = 40  # LF IMOVEIS

for inbox_id in INBOXES_PARA_DELETAR:
    # Buscar nome da inbox
    inbox_info = next((ib for ib in inboxes if ib['id'] == inbox_id), None)

    if not inbox_info:
        print(f"⚠️  Inbox {inbox_id} não encontrada")
        continue

    inbox_name = inbox_info['name']

    print(f"\n🗑️  Deletando inbox: {inbox_name} (ID {inbox_id})")

    delete_response = requests.delete(
        f'{url}/api/v1/accounts/{account_id}/inboxes/{inbox_id}',
        headers=headers
    )

    if delete_response.ok:
        print(f"   ✅ Inbox deletada com sucesso!")
    else:
        print(f"   ❌ Erro ao deletar: {delete_response.status_code}")
        print(f"   Resposta: {delete_response.text}")

# 3. VERIFICAÇÃO FINAL
print("\n" + "=" * 80)
print("📊 VERIFICAÇÃO FINAL")
print("=" * 80)

# Buscar inboxes restantes
final_response = requests.get(
    f'{url}/api/v1/accounts/{account_id}/inboxes',
    headers=headers
)

if final_response.ok:
    remaining_inboxes = final_response.json()['payload']

    print(f"\n📬 Inboxes restantes: {len(remaining_inboxes)}")

    for inbox in remaining_inboxes:
        print(f"   • {inbox['name']} (ID {inbox['id']})")

    if len(remaining_inboxes) == 1 and remaining_inboxes[0]['id'] == INBOX_MANTER:
        print(f"\n✅ LIMPEZA CONCLUÍDA COM SUCESSO!")
        print(f"   Apenas LF IMOVEIS (ID {INBOX_MANTER}) está ativa")
    else:
        print(f"\n⚠️  ATENÇÃO: Mais de uma inbox ainda existe")
else:
    print(f"❌ Erro ao verificar inboxes finais: {final_response.status_code}")

print("\n" + "=" * 80)
print("🎉 PROCESSO FINALIZADO")
