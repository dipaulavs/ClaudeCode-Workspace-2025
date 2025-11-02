#!/usr/bin/env python3
"""
Script para enviar resumo completo das funcionalidades para WhatsApp
"""

import sys
sys.path.append('/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/evolution-api-integration')

from whatsapp_helper import whatsapp

# Número de destino
NUMERO_DESTINO = "5531980160822"

# Resumo completo das funcionalidades
RESUMO = """🤖 *RESUMO COMPLETO - CLAUDE CODE WORKSPACE*

📌 *VISÃO GERAL*
Workspace com ferramentas de IA pré-configuradas para automação, criação de conteúdo e análise de dados.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 *SISTEMA DE AGENTES*

*1. Agentes Especializados (.md)*
• especificidade33 - Conteúdos virais Instagram com 33 formatos
• Uso: "Ative o agente [nome] para [tarefa]"

*2. Agentes via OpenRouter*
• copywriter-vendas - Copy persuasivo
• analista-negocios - Análise estratégica
• Modelos: Claude Haiku/Sonnet 4.5, GPT-4o/5, Gemini 2.5 Pro, Grok 4
• Comando: python3 tools/agent_openrouter.py <agente> "input"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔄 *WORKFLOWS*
Automações completas que executam múltiplas etapas

• headline-to-image - Gera imagens com headlines virais
• Uso: "Ative o workflow [nome] para [input]"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤝 *CREWAI (MULTI-AGENTES)*
Sistema de agentes colaborativos com feedback loops

• Processo Hierarchical com Manager automático
• Agentes delegam e revisam trabalho entre si
• Integrado com OpenRouter (Claude Sonnet 4.5)
• Exemplo: crews/copywriter_crew.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔄 *N8N-MCP (NOVO!)*
Automação de workflows via linguagem natural

• Instância: https://n8n.loop9.com.br
• 3000+ templates pré-configurados
• Cria chatbots, automações, pipelines de dados
• Integração com centenas de serviços (APIs, webhooks, etc.)
• Modo de planejamento para workflows complexos
• Ferramentas: list_nodes, create_workflow, update_workflow, list_templates
• ⚠️ Segurança: NUNCA deleta workflows sem confirmação

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🛠️ *FERRAMENTAS DISPONÍVEIS*

*🎨 GERAÇÃO DE IMAGENS*
• GPT-4o Image (Kie.ai) - Portrait 2:3, variações, refinamento
• Nano Banana (Gemini 2.5 Flash) - Hiper-realismo, física consciente
• Editor Nano Banana - Edição de imagens existentes

*🎵 GERAÇÃO DE ÁUDIO*
• ElevenLabs TTS - 70+ idiomas, múltiplos modelos
• Vozes: Michele, felipe
• Formatos: mp3_low, medium, high, ultra, pcm

*🎬 GERAÇÃO DE VÍDEOS*
• Sora 2 (OpenAI via Kie.ai) - ~15s, portrait/landscape/square
• Processamento paralelo em batch

*📥 EXTRAÇÃO DE CONTEÚDO*
• Transcrição Universal - YouTube, TikTok, Instagram, LinkedIn, X/Twitter
• Instagram Posts/Carrosséis - Extrai imagens e legendas
• Instagram Reels Transcrição - Transcreve áudio automaticamente
• TikTok Transcrição - Transcreve vídeos do TikTok
• Web Scraping - Extrai documentação/sites em Markdown

*📱 INSTAGRAM API*
• Publicação de Posts, Carrosséis, Reels, Stories
• Gerenciamento de Comentários - Lista, responde, oculta, deleta
• Insights/Métricas - Estatísticas de conta e posts
• Direct Messages (DMs) - Lista conversas, responde mensagens
• ⚠️ Requer permissões especiais para DMs

*📢 META ADS API*
• Campanhas - Criar, listar, atualizar, deletar
• Ad Sets - Gerenciar conjuntos de anúncios
• Anúncios - Criar e gerenciar ads
• Criativos - Criar criativos (imagens, vídeos, textos)
• Insights/Métricas - Impressões, cliques, gastos, CPC, CPM, CTR
• Upload de Imagens - Para uso em criativos
• Campanhas Regionais com Raio - Targeting por latitude/longitude

*💬 WHATSAPP (EVOLUTION API)*
• Enviar: mensagens, imagens, vídeos, documentos, áudio
• Grupos: criar, listar, adicionar/remover membros, promover admins
• Recursos: enquetes, localização, menções, status
• Helper simplificado: whatsapp_helper.py

*🔍 BUSCA EM TEMPO REAL*
• xAI Live Search (Grok) - Web, Twitter/X, News
• Máximo 5 fontes, citações incluídas
• Notícias em tempo real, tendências

*📤 UPLOAD DE IMAGENS*
• Nextcloud - media.loop9.com.br
• Links públicos diretos (.jpg)
• Expiração configurável

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 *DOCUMENTAÇÃO DE APIS*

*Meta Ads API v24.0*
• Documentação completa (77 páginas)
• Autenticação, campanhas, ad sets, ads, creatives
• Exemplos práticos em cURL
• Best practices e troubleshooting

*Instagram API*
• Documentação completa (77 páginas, 548KB)
• Autenticação, publicação, moderação, DMs
• Insights, webhooks
• Guias completos e referências

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 *QUICK START*
bash setup.sh  # Setup inicial

Todos os arquivos salvos em ~/Downloads com timestamp automático.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 *ESTRUTURA DO PROJETO*
• agentes/ - Agentes especializados
• crewai/ - Multi-agentes colaborativos
• docs/ - Documentação de APIs
• evolution-api-integration/ - Automação WhatsApp
• n8n-mcp-project/ - Workflows n8n via MCP
• tools/ - Scripts Python de IA
• config/ - Configurações
• workflows/ - Workflows automatizados

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ *PRINCIPAIS DIFERENCIAIS*
• Integração completa de múltiplas IAs (Claude, GPT, Gemini, Grok)
• Automação WhatsApp via Evolution API
• Publicação automática Instagram/Facebook
• Gerenciamento completo de Meta Ads
• n8n-MCP para workflows complexos
• Sistema de agentes colaborativos (CrewAI)
• Documentações completas de APIs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 *DOCUMENTAÇÃO*
README.md completo na raiz do projeto
Documentações específicas em cada pasta

*Atualizado em:* 31/10/2025"""

def main():
    """Envia o resumo para WhatsApp"""
    print("=" * 60)
    print("ENVIANDO RESUMO PARA WHATSAPP")
    print("=" * 60)
    print(f"\nNúmero destino: {NUMERO_DESTINO}")
    print(f"\nTamanho da mensagem: {len(RESUMO)} caracteres")

    try:
        # Verifica status
        print("\n1. Verificando status da conexão...")
        whatsapp.check_status()

        # Envia mensagem
        print("\n2. Enviando resumo completo...")
        response = whatsapp.send_message(NUMERO_DESTINO, RESUMO)

        print("\n" + "=" * 60)
        print("✅ RESUMO ENVIADO COM SUCESSO!")
        print("=" * 60)
        print(f"\nResposta da API:")
        print(response)

    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ ERRO AO ENVIAR RESUMO")
        print("=" * 60)
        print(f"\nErro: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
