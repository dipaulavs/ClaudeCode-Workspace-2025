#!/usr/bin/env python3.11
"""
Script: Daily AI News - Resumo automático de novidades sobre IA

Busca no Twitter notícias sobre OpenAI, Claude/Anthropic e Gemini/Google,
cria resumo detalhado, salva no Obsidian e envia via WhatsApp.

Uso:
    python3.11 scripts/scheduling/daily_ai_news.py
    python3.11 scripts/scheduling/daily_ai_news.py --phone 5531980160822
    python3.11 scripts/scheduling/daily_ai_news.py --no-whatsapp  # Apenas Obsidian
"""

import sys
import os
from datetime import datetime
import argparse
import requests
import urllib3

# Desabilitar warnings SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configurações (hardcoded para evitar conflitos de import)
XAI_API_KEY = "xai-h66b4L5bInRmreYlmM1JLQRjDEzTm7xPzqEI6W82NV83OuULANLGq28isee1tTUIIcBehpHzFhpOjf3r"
OBSIDIAN_API_URL = "https://127.0.0.1:27124"
OBSIDIAN_API_KEY = os.getenv("OBSIDIAN_API_KEY", "")
EVOLUTION_API_URL = "https://evolution.loop9.com.br"
EVOLUTION_API_KEY = "178e43e1c4f459527e7008e57e378e1c"
EVOLUTION_INSTANCE_NAME = "lfimoveis"

# Adiciona path para xAI SDK
workspace_root = os.path.join(os.path.dirname(__file__), '../..')
sys.path.insert(0, workspace_root)

from xai_sdk import Client
from xai_sdk.chat import user
from xai_sdk.search import SearchParameters, x_source


def buscar_twitter_ai_news(empresa: str, max_results: int = 10):
    """
    Busca notícias recentes sobre empresa de IA no Twitter

    Args:
        empresa: Nome da empresa (OpenAI, Anthropic, Google)
        max_results: Número máximo de posts

    Returns:
        dict: Resultado da busca com content, citations e num_sources_used
    """
    client = Client(api_key=XAI_API_KEY)

    # Configura fonte do Twitter
    x_src = x_source()

    # Configura parâmetros de busca
    search_params = SearchParameters(
        mode="on",
        max_search_results=max_results,
        return_citations=True,
        sources=[x_src]
    )

    # Query otimizada para cada empresa
    queries = {
        'OpenAI': 'OpenAI OR ChatGPT OR GPT-4 OR GPT-5 OR Sam Altman news announcement launch',
        'Anthropic': 'Anthropic OR Claude OR Claude 4 OR Claude Sonnet news announcement',
        'Google': 'Google AI OR Gemini OR Gemini 2 OR DeepMind news announcement launch'
    }

    query = queries.get(empresa, empresa)

    # Cria chat e realiza busca
    chat = client.chat.create(
        model="grok-4-fast",
        search_parameters=search_params
    )

    chat.append(user(f"Liste as principais novidades e anúncios recentes sobre {empresa} baseado nos posts do Twitter. Seja objetivo e direto."))
    response = chat.sample()

    return {
        'content': response.content,
        'citations': response.citations if hasattr(response, 'citations') else [],
        'num_sources_used': response.usage.num_sources_used if hasattr(response.usage, 'num_sources_used') else 0
    }


def criar_resumo_consolidado(resultados: dict):
    """
    Cria resumo consolidado das notícias usando Grok

    Args:
        resultados: Dict com resultados de OpenAI, Anthropic e Google

    Returns:
        str: Resumo formatado em markdown
    """
    client = Client(api_key=XAI_API_KEY)

    # Prepara contexto para análise
    contexto = f"""
Analise as seguintes notícias sobre empresas de IA e crie um resumo detalhado:

## OPENAI
{resultados['OpenAI']['content']}

## ANTHROPIC (CLAUDE)
{resultados['Anthropic']['content']}

## GOOGLE (GEMINI)
{resultados['Google']['content']}

Crie um resumo ESTRUTURADO em português com:
1. **Resumo Executivo** (2-3 linhas do mais importante)
2. **OpenAI**: principais novidades (bullet points)
3. **Anthropic/Claude**: principais novidades (bullet points)
4. **Google/Gemini**: principais novidades (bullet points)
5. **Análise**: tendências e insights (2-3 parágrafos)

Use markdown. Seja objetivo mas detalhado. Destaque anúncios importantes.
"""

    chat = client.chat.create(model="grok-4-fast")
    chat.append(user(contexto))
    response = chat.sample()

    return response.content


def salvar_obsidian(resumo: str, resultados: dict, workspace_root: str = None):
    """
    Salva resumo no Obsidian via API

    Args:
        resumo: Texto do resumo
        resultados: Dict com resultados das buscas
        workspace_root: Caminho raiz do workspace (para fallback)

    Returns:
        str: Nome do arquivo criado
    """
    if workspace_root is None:
        workspace_root = os.path.join(os.path.dirname(__file__), '../..')

    # Gera nome do arquivo
    data_hoje = datetime.now().strftime('%Y-%m-%d')
    filename = f"AI News - {data_hoje}"

    # Cria conteúdo completo
    conteudo = f"""# 🤖 AI News - {datetime.now().strftime('%d/%m/%Y')}

{resumo}

---

## 📊 Fontes Consultadas

### OpenAI ({resultados['OpenAI']['num_sources_used']} posts)
"""

    # Adiciona citações OpenAI
    for i, citation in enumerate(resultados['OpenAI']['citations'][:5], 1):
        conteudo += f"{i}. {citation}\n"

    conteudo += f"\n### Anthropic ({resultados['Anthropic']['num_sources_used']} posts)\n"

    # Adiciona citações Anthropic
    for i, citation in enumerate(resultados['Anthropic']['citations'][:5], 1):
        conteudo += f"{i}. {citation}\n"

    conteudo += f"\n### Google ({resultados['Google']['num_sources_used']} posts)\n"

    # Adiciona citações Google
    for i, citation in enumerate(resultados['Google']['citations'][:5], 1):
        conteudo += f"{i}. {citation}\n"

    conteudo += f"""

---
**Gerado em:** {datetime.now().strftime('%d/%m/%Y às %H:%M')}
**Script:** daily_ai_news.py
**Tags:** #ai #news #automation
"""

    # Tenta salvar via API do Obsidian (com fallback para arquivo local)
    filepath = f"00 - Inbox/{filename}.md"

    try:
        headers = {
            "Authorization": f"Bearer {OBSIDIAN_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "path": filepath,
            "content": conteudo
        }

        response = requests.put(
            f"{OBSIDIAN_API_URL}/vault/{filepath}",
            headers=headers,
            json=data,
            verify=False,
            timeout=5
        )

        response.raise_for_status()
        print(f"✅ Nota salva no Obsidian: {filename}.md")

    except Exception as e:
        # Fallback: salvar em arquivo local
        print(f"⚠️  Obsidian não disponível ({e})")
        print(f"💾 Salvando em arquivo local...")

        local_path = os.path.join(workspace_root, "output", "ai-news")
        os.makedirs(local_path, exist_ok=True)

        arquivo_local = os.path.join(local_path, f"{filename}.md")
        with open(arquivo_local, 'w', encoding='utf-8') as f:
            f.write(conteudo)

        print(f"✅ Nota salva localmente: {arquivo_local}")

    return filename


def enviar_whatsapp(resumo: str, phone: str):
    """
    Envia resumo via WhatsApp usando Evolution API

    Args:
        resumo: Texto do resumo
        phone: Número do destinatário
    """
    # Prepara mensagem (versão resumida para WhatsApp)
    hoje = datetime.now().strftime('%d/%m/%Y')
    mensagem = f"""🤖 *AI News - {hoje}*

{resumo}

_Resumo completo salvo no Obsidian_"""

    # Envia via Evolution API
    url = f"{EVOLUTION_API_URL}/message/sendText/{EVOLUTION_INSTANCE_NAME}"

    headers = {
        "apikey": EVOLUTION_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "number": phone,
        "text": mensagem
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    print(f"✅ Resumo enviado para WhatsApp: {phone}")
    return response.json()


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Buscar e resumir notícias de IA')
    parser.add_argument(
        '--phone',
        default='5531980160822',
        help='Número WhatsApp (padrão: 5531980160822)'
    )
    parser.add_argument(
        '--no-whatsapp',
        action='store_true',
        help='Não enviar WhatsApp (apenas Obsidian)'
    )
    parser.add_argument(
        '--max-posts',
        type=int,
        default=10,
        help='Máximo de posts por empresa (padrão: 10)'
    )

    args = parser.parse_args()

    print("=" * 80)
    print("🤖 AI NEWS DIGEST - Resumo Diário de Inteligência Artificial")
    print("=" * 80)
    print(f"\n📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")

    try:
        # 1. Buscar notícias no Twitter
        print("🐦 Buscando notícias no Twitter...\n")

        resultados = {}
        empresas = ['OpenAI', 'Anthropic', 'Google']

        for empresa in empresas:
            print(f"  → {empresa}...", end=' ')
            resultados[empresa] = buscar_twitter_ai_news(empresa, args.max_posts)
            print(f"✓ ({resultados[empresa]['num_sources_used']} posts)")

        print(f"\n✅ {sum(r['num_sources_used'] for r in resultados.values())} posts consultados no total\n")

        # 2. Criar resumo consolidado
        print("📝 Criando resumo consolidado com Grok...\n")
        resumo = criar_resumo_consolidado(resultados)
        print("✅ Resumo criado\n")

        # 3. Salvar no Obsidian
        print("💾 Salvando no Obsidian...\n")
        filename = salvar_obsidian(resumo, resultados)

        # 4. Enviar WhatsApp
        if not args.no_whatsapp:
            print(f"\n📤 Enviando para WhatsApp ({args.phone})...\n")
            enviar_whatsapp(resumo, args.phone)

        # Resumo final
        print("\n" + "=" * 80)
        print("✅ TAREFA CONCLUÍDA COM SUCESSO!")
        print("=" * 80)
        print(f"\n📂 Nota Obsidian: {filename}.md")
        if not args.no_whatsapp:
            print(f"📱 WhatsApp enviado para: {args.phone}")
        print()

    except Exception as e:
        print(f"\n❌ Erro ao executar tarefa: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
