#!/usr/bin/env python3
"""
Pega Carrossel Complete - Download e análise completa de carrosséis Instagram

Baixa todos os slides de um carrossel do Instagram e gera prompts detalhados
para recriação (versão original + versão template adaptável).

Uso:
    python3 pega_carrossel_complete.py "https://www.instagram.com/p/ABC123/"
    python3 pega_carrossel_complete.py "https://www.instagram.com/p/ABC123/" --output ~/Downloads

Autor: Claude Code
Data: 2025-01-11
"""

import sys
import os
import json
import argparse
import subprocess
import re
from pathlib import Path

# Adicionar diretório raiz ao path para importar configs
WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(WORKSPACE_ROOT))

from config.apify_config import APIFY_API_KEY

try:
    from apify_client import ApifyClient
    import requests
    from anthropic import Anthropic
except ImportError as e:
    print(f"❌ Erro: Biblioteca necessária não instalada: {e}")
    print("📦 Instale com: pip3 install apify-client requests anthropic")
    sys.exit(1)


def sanitize_folder_name(text):
    """Remove caracteres inválidos para nome de pasta"""
    # Remover caracteres especiais, manter apenas letras, números, espaços e hífens
    text = re.sub(r'[^\w\s-]', '', text)
    # Substituir espaços por underscores
    text = text.replace(' ', '_')
    # Remover múltiplos underscores
    text = re.sub(r'_+', '_', text)
    # Limitar tamanho
    return text[:50].strip('_')


def download_carrossel(instagram_url, output_dir=None):
    """
    Faz download de todos os slides de um carrossel do Instagram

    Args:
        instagram_url: URL do post do Instagram
        output_dir: Diretório de saída (padrão: ~/Downloads)

    Returns:
        dict: {
            "folder_path": caminho da pasta criada,
            "slides": lista de caminhos das imagens,
            "metadata": dados do post
        }
    """
    print(f"\n🚀 Iniciando download do carrossel...")
    print(f"🔗 URL: {instagram_url}\n")

    # Configurar cliente Apify
    client = ApifyClient(APIFY_API_KEY)
    actor = client.actor("apify/instagram-scraper")

    # Executar scraping
    run_input = {
        "directUrls": [instagram_url],
        "resultsType": "posts",
        "resultsLimit": 1,
        "addParentData": False,
    }

    print("⏳ Aguardando Apify API...")
    run = actor.call(run_input=run_input, timeout_secs=120)

    # Buscar resultados
    dataset = client.dataset(run["defaultDatasetId"])
    items = list(dataset.iterate_items())

    if not items:
        raise ValueError("❌ Nenhum resultado encontrado. Verifique a URL.")

    post = items[0]

    # Extrair informações
    username = post.get('ownerUsername', 'unknown')
    caption = post.get('caption', '')
    images = post.get('images', [])
    post_type = post.get('type', 'Unknown')

    if post_type != 'Sidecar':
        print(f"⚠️  Aviso: Post não é carrossel (tipo: {post_type})")

    print(f"✅ Dados obtidos:")
    print(f"   📱 Instagram: @{username}")
    print(f"   🖼️  Total de slides: {len(images)}")
    print(f"   📝 Legenda: {caption[:100]}...")

    # Definir nome da pasta
    # Extrair tema da legenda (primeiras palavras)
    tema_palavras = caption.split()[:3] if caption else ['carrossel']
    tema = '_'.join(tema_palavras)
    tema = sanitize_folder_name(tema)

    folder_name = f"{tema}_{username}"
    output_base = Path(output_dir) if output_dir else Path.home() / "Downloads"
    folder_path = output_base / folder_name
    folder_path.mkdir(parents=True, exist_ok=True)

    print(f"\n📁 Pasta criada: {folder_path}")

    # Download das imagens
    print(f"\n📥 Baixando {len(images)} slides...\n")

    slide_paths = []
    slide_names = get_slide_names(len(images))

    for i, (img_url, slide_name) in enumerate(zip(images, slide_names), 1):
        try:
            response = requests.get(img_url, timeout=30)
            response.raise_for_status()

            filename = f"{slide_name}.jpg"
            filepath = folder_path / filename

            with open(filepath, 'wb') as f:
                f.write(response.content)

            slide_paths.append(str(filepath))
            print(f"   ✅ {i}/{len(images)} - {filename}")

        except Exception as e:
            print(f"   ❌ Erro no slide {i}: {e}")

    # Salvar metadata
    metadata = {
        "url": instagram_url,
        "username": username,
        "caption": caption,
        "type": post_type,
        "total_slides": len(images),
        "slides": slide_paths,
        "image_urls": images
    }

    metadata_path = folder_path / "metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Metadata salva: {metadata_path}")

    return {
        "folder_path": str(folder_path),
        "slides": slide_paths,
        "metadata": metadata
    }


def get_slide_names(total_slides):
    """Gera nomes descritivos para cada slide baseado na posição"""
    if total_slides == 1:
        return ["Slide 1 - Post Unico"]

    names = []
    names.append("Slide 1 - Hook")

    # Slides do meio
    for i in range(2, total_slides):
        if total_slides <= 4:
            names.append(f"Slide {i} - Conteudo")
        else:
            names.append(f"Slide {i} - Tipo{i-1}")

    # Último slide
    names.append(f"Slide {total_slides} - CTA")

    return names


def analyze_and_generate_prompts(folder_path, slides_info):
    """
    Analisa slides e gera prompts detalhados (versão original + template)

    Args:
        folder_path: Caminho da pasta com os slides
        slides_info: Dict com metadata dos slides

    Returns:
        str: Caminho do arquivo TXT gerado
    """
    print(f"\n🔍 Analisando slides e gerando prompts...\n")

    # Configurar Claude
    anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
    if not anthropic_api_key:
        raise ValueError("❌ ANTHROPIC_API_KEY não configurada")

    client = Anthropic(api_key=anthropic_api_key)

    slides = slides_info['slides']
    username = slides_info['metadata']['username']
    total_slides = len(slides)

    # Preparar imagens para análise
    image_contents = []
    for slide_path in slides:
        with open(slide_path, 'rb') as f:
            import base64
            image_data = base64.b64encode(f.read()).decode('utf-8')
            image_contents.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image_data
                }
            })

    # Criar prompt para Claude
    analysis_prompt = f"""Analise este carrossel de {total_slides} slides do Instagram (@{username}) e crie prompts detalhados para recriação.

Para CADA slide, gere 2 versões de prompt:

1. **VERSÃO ORIGINAL** - Prompt para recriar IDÊNTICO ao original
   - Descreva cores exatas (códigos HEX quando visível)
   - Tipografia precisa (fontes, tamanhos, pesos)
   - Layout exato (posições, espaçamentos, alinhamentos)
   - Textos literais como aparecem
   - Imagens/símbolos específicos mostrados
   - Efeitos visuais (sombras, bordas, gradientes)

2. **VERSÃO TEMPLATE** - Prompt adaptável para qualquer nicho
   - Substitua textos por [TEXTO EDITÁVEL AQUI]
   - Substitua imagens/símbolos por [IMAGENS E SÍMBOLOS CORRESPONDENTES AO INPUT AQUI]
   - Substitua @{username} por @lfimoveis
   - Mantenha toda estrutura, cores, tipografia, layout
   - Inclua exemplos de adaptação para outros nichos

FORMATO DE SAÍDA:

```
═══════════════════════════════════════════════════════════════════
📊 ANÁLISE COMPLETA: CARROSSEL @{username.upper()}
═══════════════════════════════════════════════════════════════════

🎯 ESTRUTURA: {total_slides} slides
📐 FORMATO: 1080x1350px (4:5 Instagram)
🎨 ESTILO: [descrever estilo geral]
🏢 TEMA: [descrever tema/propósito]

═══════════════════════════════════════════════════════════════════

📸 SLIDE 1 - [NOME DO SLIDE]
═══════════════════════════════════════════════════════════════════

🎨 VERSÃO ORIGINAL (RECRIAÇÃO IDÊNTICA):

[Prompt detalhado para recriar exatamente como está]

---

🔄 VERSÃO TEMPLATE (ADAPTÁVEL):

[Prompt com placeholders editáveis]

EXEMPLO PARA IMÓVEIS:
[Mostrar como ficaria adaptado para @lfimoveis]

VARIÁVEIS:
- [TEXTO 1]: [descrição]
- [IMAGEM 1]: [descrição]

═══════════════════════════════════════════════════════════════════

[Repetir para todos os {total_slides} slides]

═══════════════════════════════════════════════════════════════════

📋 PALETA DE CORES IDENTIFICADA
═══════════════════════════════════════════════════════════════════

[Listar todas as cores usadas com códigos HEX]

═══════════════════════════════════════════════════════════════════

🔤 TIPOGRAFIA IDENTIFICADA
═══════════════════════════════════════════════════════════════════

[Listar fontes, tamanhos, pesos usados]

═══════════════════════════════════════════════════════════════════
FIM DA ANÁLISE
═══════════════════════════════════════════════════════════════════
```

Seja EXTREMAMENTE detalhado e preciso. Este prompt será usado para recriar o carrossel de forma idêntica."""

    # Chamar Claude API
    print("   🤖 Enviando para Claude API para análise visual...")

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=16000,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": analysis_prompt},
                *image_contents
            ]
        }]
    )

    prompts_text = message.content[0].text

    # Salvar prompts em arquivo
    output_filename = f"prompts_{total_slides}slides.txt"
    output_path = Path(folder_path) / output_filename

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(prompts_text)

    print(f"\n✅ Prompts gerados: {output_path}")
    print(f"📊 Total de caracteres: {len(prompts_text):,}")

    return str(output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Pega Carrossel Complete - Download e análise de carrosséis Instagram",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

  # Download e análise completa
  python3 pega_carrossel_complete.py "https://www.instagram.com/p/DQr4zkvjpCY/"

  # Especificar diretório de saída
  python3 pega_carrossel_complete.py "https://www.instagram.com/p/DQr4zkvjpCY/" --output ~/Desktop

Saída:
  Pasta: {tema}_{@username}/
  ├── Slide 1 - Hook.jpg
  ├── Slide 2 - Tipo1.jpg
  ├── ...
  ├── Slide N - CTA.jpg
  ├── metadata.json
  └── prompts_Nslides.txt (versão original + template)
        """
    )

    parser.add_argument('url', help='URL do post do Instagram')
    parser.add_argument('--output', '-o', help='Diretório de saída (padrão: ~/Downloads)')

    args = parser.parse_args()

    try:
        # 1. Download do carrossel
        result = download_carrossel(args.url, args.output)

        # 2. Análise e geração de prompts
        prompts_file = analyze_and_generate_prompts(
            result['folder_path'],
            result
        )

        # Resumo final
        print(f"\n" + "="*70)
        print(f"✅ PROCESSO CONCLUÍDO COM SUCESSO!")
        print(f"="*70)
        print(f"\n📁 Pasta: {result['folder_path']}")
        print(f"🖼️  Slides: {len(result['slides'])}")
        print(f"📝 Prompts: {prompts_file}")
        print(f"\n💡 Use os prompts gerados para recriar ou adaptar o carrossel!")

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
