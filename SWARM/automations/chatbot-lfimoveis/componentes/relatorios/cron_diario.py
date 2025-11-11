#!/usr/bin/env python3
"""
Gerador de relatório diário
Executado via cron: 0 18 * * * (18h todos os dias)
"""

import sys
import os
import json

# Adiciona diretório raiz ao path
sys.path.insert(0, '/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot')

from componentes.relatorios import GeradorRelatorio


def main():
    """Gera e envia relatório diário"""
    try:
        # Carrega config
        config_path = '/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/chatwoot_config.json'

        with open(config_path, 'r') as f:
            config = json.load(f)

        # Pega número do gestor
        numero_gestor = config.get('relatorios', {}).get('numero_gestor', '5531980160822')

        # Gera relatório
        gerador = GeradorRelatorio()
        relatorio = gerador.gerar_relatorio_diario()

        print("📊 Relatório gerado:")
        print(relatorio)
        print()

        # Envia
        sucesso = gerador.enviar_relatorio(relatorio, numero_gestor)

        if sucesso:
            print("✅ Relatório diário enviado com sucesso")
            return 0
        else:
            print("❌ Falha ao enviar relatório")
            return 1

    except Exception as e:
        print(f"❌ Erro ao gerar relatório: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
