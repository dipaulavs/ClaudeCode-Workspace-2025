#!/usr/bin/env python3.11
"""
Simula conversa natural sobre show do Gusttavo Lima
"""
import sys
import time
import random

# Adiciona o diretório ao path para importar o módulo
sys.path.insert(0, '/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/evolution-api-integration')

from whatsapp_helper import whatsapp

# Número de destino
numero = "5531980160822"

# Mensagens para enviar (simulando jovem conversando)
mensagens = [
    "e aiii mano",
    "ce ta sabendo do show do gusttavo lima??",
    "vai ser na sexta q vem",
    "o nelito vai",
    "ele ja comprou ingresso inclusive kkkkk",
    "ta mto animado",
    "ce devia ir tbm",
    "vai ser mto dahora"
]

print(f"🎵 Iniciando conversa sobre o show do Gusttavo Lima...")
print(f"📱 Enviando para: {numero}\n")

try:
    for i, msg in enumerate(mensagens, 1):
        # Envia a mensagem
        print(f"[{i}/{len(mensagens)}] Enviando: {msg}")
        resultado = whatsapp.send_message(numero, msg)

        if resultado.get('status') == 'success':
            print(f"✅ Enviada com sucesso!")
        else:
            print(f"❌ Erro ao enviar: {resultado.get('message', 'Erro desconhecido')}")

        # Pausa natural entre mensagens (2-5 segundos)
        if i < len(mensagens):
            pausa = random.uniform(2, 5)
            print(f"⏳ Aguardando {pausa:.1f}s...\n")
            time.sleep(pausa)

    print("\n✨ Conversa finalizada!")
    print(f"📊 Total de mensagens enviadas: {len(mensagens)}")

except KeyboardInterrupt:
    print("\n\n⚠️ Envio interrompido pelo usuário")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Erro: {e}")
    sys.exit(1)
