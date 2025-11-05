#!/usr/bin/env python3
"""
📱 GERAR QR CODE - Evolution API Automaia
Gera QR Code para conectar WhatsApp da instância Automaia
"""

import requests
import json
import sys
import base64
from pathlib import Path

def carregar_config():
    """Carrega configurações do arquivo JSON"""
    config_file = Path(__file__).parent / "chatwoot_config_automaia.json"

    if not config_file.exists():
        print("❌ Erro: chatwoot_config_automaia.json não encontrado!")
        print("\n💡 Crie o arquivo primeiro:")
        print("   cp chatwoot_config_automaia.json.template chatwoot_config_automaia.json")
        sys.exit(1)

    with open(config_file, 'r') as f:
        return json.load(f)

def criar_instancia(evolution_url, api_key, instance_name):
    """Cria nova instância no Evolution API"""
    print(f"\n🔄 Criando instância '{instance_name}'...")

    url = f"{evolution_url}/instance/create"

    headers = {
        "apikey": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "instanceName": instance_name,
        "qrcode": True,
        "integration": "WHATSAPP-BAILEYS"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code in [200, 201]:
            print("✅ Instância criada com sucesso!")
            return True
        elif response.status_code == 409:
            print("⚠️  Instância já existe")
            return True
        else:
            print(f"⚠️  Erro ao criar instância: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def conectar_instancia(evolution_url, api_key, instance_name):
    """Conecta instância e obtém QR Code"""
    print(f"\n🔗 Conectando instância '{instance_name}'...")

    url = f"{evolution_url}/instance/connect/{instance_name}"

    headers = {
        "apikey": api_key
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"❌ Erro ao conectar: {response.status_code}")
            print(f"Resposta: {response.text}")
            return None

    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

def salvar_qrcode_imagem(base64_data, output_path):
    """Salva QR Code como imagem PNG"""
    try:
        # Remove prefixo "data:image/png;base64," se existir
        if ',' in base64_data:
            base64_data = base64_data.split(',')[1]

        # Decodifica base64
        image_data = base64.b64decode(base64_data)

        # Salva arquivo
        with open(output_path, 'wb') as f:
            f.write(image_data)

        return True

    except Exception as e:
        print(f"❌ Erro ao salvar imagem: {e}")
        return False

def verificar_status(evolution_url, api_key, instance_name):
    """Verifica status da conexão"""
    url = f"{evolution_url}/instance/connectionState/{instance_name}"

    headers = {
        "apikey": api_key
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            state = data.get('instance', {}).get('state')
            return state
        return None

    except Exception as e:
        return None

def main():
    print("=" * 70)
    print("📱 GERAR QR CODE - EVOLUTION API AUTOMAIA")
    print("=" * 70)

    # Carrega config
    config = carregar_config()

    evolution_url = config['evolution']['url']
    api_key = config['evolution']['api_key']
    instance_name = config['evolution']['instance']

    print(f"\n📡 Servidor: {evolution_url}")
    print(f"📱 Instância: {instance_name}")

    # Verifica status atual
    print(f"\n🔍 Verificando status...")
    status = verificar_status(evolution_url, api_key, instance_name)

    if status == 'open':
        print("✅ WhatsApp já está conectado!")
        print("\n💡 Não precisa escanear QR Code novamente.")
        return

    # Tenta criar instância (se não existir)
    criar_instancia(evolution_url, api_key, instance_name)

    # Conecta e obtém QR Code
    result = conectar_instancia(evolution_url, api_key, instance_name)

    if not result:
        print("\n❌ Falha ao gerar QR Code")
        print("\n🆘 Possíveis soluções:")
        print("   1. Verificar se Evolution API está online")
        print("   2. Verificar se API Key está correta")
        print("   3. Tentar deletar a instância e criar novamente")
        print("\n💡 Comando para deletar:")
        print(f"   curl -X DELETE '{evolution_url}/instance/delete/{instance_name}' \\")
        print(f"     -H 'apikey: {api_key}'")
        return

    # Extrai dados do QR Code
    qrcode_data = result.get('qrcode', {})

    if not qrcode_data:
        print("⚠️  QR Code não disponível na resposta")
        print(f"Resposta completa: {json.dumps(result, indent=2)}")
        return

    # Tenta pegar base64
    base64_qr = None

    if isinstance(qrcode_data, dict):
        base64_qr = qrcode_data.get('base64') or qrcode_data.get('pairingCode')
    elif isinstance(qrcode_data, str):
        base64_qr = qrcode_data

    if base64_qr and ('base64' in base64_qr or base64_qr.startswith('iVBOR')):
        # É uma imagem base64
        output_file = Path(__file__).parent / "qrcode_automaia.png"

        print(f"\n💾 Salvando QR Code como imagem...")

        if salvar_qrcode_imagem(base64_qr, output_file):
            print(f"✅ QR Code salvo em: {output_file}")
            print()
            print("=" * 70)
            print("📲 COMO ESCANEAR:")
            print("=" * 70)
            print(f"1. Abra o arquivo: {output_file}")
            print("2. No WhatsApp: ⋮ (3 pontos) → Aparelhos conectados")
            print("3. Toque em 'Conectar um aparelho'")
            print("4. Escaneie o QR Code da imagem")
            print()
            print("⏳ Aguarde alguns segundos após escanear...")
            print("=" * 70)

            # Tenta abrir automaticamente
            import subprocess
            import platform

            try:
                if platform.system() == 'Darwin':  # macOS
                    subprocess.run(['open', str(output_file)])
                    print("\n✅ Imagem aberta automaticamente!")
                elif platform.system() == 'Linux':
                    subprocess.run(['xdg-open', str(output_file)])
                    print("\n✅ Imagem aberta automaticamente!")
            except:
                pass

        else:
            print(f"❌ Falha ao salvar imagem")

    else:
        # É um código texto (pairing code)
        print("\n" + "=" * 70)
        print("📱 CÓDIGO DE PAREAMENTO:")
        print("=" * 70)
        print()
        print(f"   {qrcode_data}")
        print()
        print("=" * 70)
        print("📲 COMO USAR:")
        print("=" * 70)
        print("1. Abra o WhatsApp no celular")
        print("2. Toque em ⋮ (3 pontos) → Aparelhos conectados")
        print("3. Toque em 'Conectar usando número do telefone'")
        print("4. Digite o código acima")
        print()
        print("⏳ Aguarde alguns segundos após digitar...")
        print("=" * 70)

if __name__ == '__main__':
    main()
