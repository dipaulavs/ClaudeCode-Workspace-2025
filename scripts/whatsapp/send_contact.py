#!/usr/bin/env python3
"""
Template: Enviar contato via WhatsApp

Uso:
    python3 scripts/whatsapp/send_contact.py --phone 5531980160822 --contact-number 5511999999999 --name "João Silva" --organization "Empresa XYZ" --email "joao@example.com"
    python3 scripts/whatsapp/send_contact.py --phone 5531980160822 --contact-number 5511999999999 --name "Maria Santos"
"""

import sys
import argparse
from pathlib import Path

# Adiciona paths necessários
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "evolution-api-integration"))

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


def send_contact(phone: str, contact_number: str, full_name: str, organization: str = "", email: str = ""):
    """Envia contato via WhatsApp"""

    # Inicializa API
    api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

    # Envia contato
    response = api.send_contact(
        number=phone,
        contact_number=contact_number,
        full_name=full_name,
        organization=organization,
        email=email
    )

    return response


def main():
    parser = argparse.ArgumentParser(description='Enviar contato WhatsApp')
    parser.add_argument('--phone', '-p', required=True, help='Número com DDI (ex: 5531980160822)')
    parser.add_argument('--contact-number', '-c', required=True, help='Número do contato a enviar (ex: 5511999999999)')
    parser.add_argument('--name', '-n', required=True, help='Nome completo do contato')
    parser.add_argument('--organization', '-o', default="", help='Empresa/Organização')
    parser.add_argument('--email', '-e', default="", help='E-mail do contato')

    args = parser.parse_args()

    print(f"👤 Enviando contato para {args.phone}...")
    print(f"   Nome: {args.name}")
    print(f"   Número: {args.contact_number}")

    try:
        response = send_contact(args.phone, args.contact_number, args.name, args.organization, args.email)
        message_id = response.get('key', {}).get('id', 'N/A')
        print(f"✅ Contato enviado com sucesso!")
        print(f"   Message ID: {message_id}")
        return response
    except Exception as e:
        print(f"❌ Erro ao enviar contato: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
