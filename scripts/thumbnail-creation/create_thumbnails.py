#!/usr/bin/env python3
"""
Template: Criar Thumbnails Virais para YouTube

Gera 4 variações de thumbnail viral usando sua foto + headline do Hormozi.
Usa a foto configurada (via URL Nextcloud salva).

Uso:
    python3 scripts/thumbnail-creation/create_thumbnails.py "Como Transformers Revolucionaram IA"
    python3 scripts/thumbnail-creation/create_thumbnails.py "O Segredo da IA Que Ninguém Conta" --topic "inteligencia-artificial"
"""

import sys
import argparse
import json
from pathlib import Path

# Adiciona o diretório tools ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))

from edit_image_nanobanana import edit_image, wait_for_completion
import requests


# 4 Estilos de Thumbnail Viral
THUMBNAIL_STYLES = [
    {
        "name": "mr-beast",
        "prompt_template": """Criar thumbnail estilo MrBeast vibrante:
- Fundo: Vermelho e amarelo INTENSO e vibrante
- Pessoa: Expressão muito surpresa/empolgada
- Texto GIGANTE em maiúsculo: "{headline}"
- Adicionar setas amarelas apontando para a pessoa
- Círculos amarelos ao redor do rosto
- Estilo: Energia máxima, cores saturadas
- Proporção: 16:9 (YouTube thumbnail)
- Remover qualquer fundo original, aplicar o fundo novo""",
        "size": "16:9"
    },
    {
        "name": "tech-minimal",
        "prompt_template": """Criar thumbnail tech minimalista profissional:
- Fundo: Gradiente azul escuro (#1a1f3a) para roxo escuro (#2d1b4e)
- Pessoa: Posição esquerda, look profissional/sério
- Texto clean e moderno: "{headline}"
- Adicionar ícones tech sutis (cérebro IA, circuitos, chip)
- Estilo: Minimalista, limpo, futurista
- Cores: Azul neon, roxo, branco
- Proporção: 16:9 (YouTube thumbnail)
- Remover fundo original, aplicar gradiente""",
        "size": "16:9"
    },
    {
        "name": "high-contrast",
        "prompt_template": """Criar thumbnail de alto contraste neon:
- Fundo: PRETO SÓLIDO absoluto (#000000)
- Pessoa: Recorte sem fundo, centralizada
- Texto em AMARELO NEON ou VERDE LIMÃO brilhante: "{headline}"
- Adicionar efeito glitch/neon ao redor da pessoa
- Bordas com brilho neon (rosa, ciano, amarelo)
- Estilo: Cyberpunk, futurista, neon vibrante
- Proporção: 16:9 (YouTube thumbnail)
- Contraste máximo entre preto e cores neon""",
        "size": "16:9"
    },
    {
        "name": "split-screen",
        "prompt_template": """Criar thumbnail split-screen dinâmico:
- Dividir em duas metades verticais
- LADO ESQUERDO: Pessoa (rosto/busto)
- LADO DIREITO: Visual relacionado ao tema (ex: diagrama IA, código, gráficos tech)
- Texto centralizado entre as duas partes: "{headline}"
- Linha divisória neon (azul ou amarelo) no centro
- Fundo de cada lado: Cores complementares (ex: azul vs laranja)
- Estilo: Dinâmico, balanceado, profissional
- Proporção: 16:9 (YouTube thumbnail)
- Remover fundo original da pessoa""",
        "size": "16:9"
    }
]


def load_photo_urls():
    """Carrega URLs das fotos do arquivo de configuração"""

    script_dir = Path(__file__).resolve().parent
    config_file = script_dir / "photos_urls.json"

    if not config_file.exists():
        print("❌ Erro: Arquivo photos_urls.json não encontrado!")
        print("\n📸 Execute o setup primeiro:")
        print("   python3 scripts/thumbnail-creation/setup_photos.py")
        print("\n   Isso fará upload das suas 4 fotos e salvará as URLs.")
        sys.exit(1)

    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_photo_url(photo_urls):
    """Retorna a URL da foto configurada"""

    # Sempre usa foto1 (única foto configurada)
    chosen_data = photo_urls['foto1']

    print(f"📸 Usando foto: {chosen_data['filename']}")
    return chosen_data['url']


def create_thumbnail_variation(photo_url, headline, style, output_dir, topic="video"):
    """Cria uma variação de thumbnail usando Nano Banana Edit"""

    print(f"\n{'='*60}")
    print(f"🎨 Estilo: {style['name'].upper()}")
    print(f"{'='*60}")

    try:
        # Monta o prompt com a headline
        edit_prompt = style['prompt_template'].format(headline=headline)

        print(f"📝 Gerando thumbnail...")

        # Edita com Nano Banana (usando URL já salva)
        task_id = edit_image(
            prompt=edit_prompt,
            image_url=photo_url,
            output_format='JPEG',
            image_size=style['size']
        )

        if not task_id:
            print(f"❌ Falha ao criar thumbnail {style['name']}")
            return None

        # Aguarda conclusão
        image_urls = wait_for_completion(task_id)

        if not image_urls:
            print(f"❌ Falha ao gerar thumbnail {style['name']}")
            return None

        # Baixa a thumbnail gerada
        print(f"📥 Baixando thumbnail...")

        # Salva com nome descritivo
        output_filename = f"thumbnail_{topic}_{style['name']}.jpg"
        output_path = Path(output_dir) / output_filename

        # Download direto para pasta de output
        response = requests.get(image_urls[0], timeout=30)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            f.write(response.content)

        print(f"✅ Salvo: {output_path}")
        return str(output_path)

    except Exception as e:
        print(f"❌ Erro ao criar thumbnail {style['name']}: {e}")
        return None


def main():
    """Função principal"""

    parser = argparse.ArgumentParser(
        description='Criar 4 variações de thumbnail viral para YouTube',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
    # Criar thumbnails com headline
    python3 scripts/thumbnail-creation/create_thumbnails.py "Como IA Mudou TUDO"

    # Com tópico personalizado (para nome dos arquivos)
    python3 scripts/thumbnail-creation/create_thumbnails.py "Transformers Explicado" --topic "transformers-ia"

Características:
    - Escolhe aleatoriamente 1 das 4 fotos (URLs salvas)
    - Gera 4 estilos virais: MrBeast, Tech Minimal, High Contrast, Split Screen
    - Salva em output/thumbnails/
    - Formato: JPEG 16:9 (ideal para YouTube)

Setup inicial necessário:
    python3 scripts/thumbnail-creation/setup_photos.py
        """
    )

    parser.add_argument('headline',
                        help='Headline viral (do hormozi-leads)')
    parser.add_argument('--topic', '-t', default='video',
                        help='Tópico do vídeo (para nome dos arquivos). Ex: "transformers-ia"')

    args = parser.parse_args()

    print("🎬 Thumbnail Creator - Gerador de Thumbnails Virais")
    print("=" * 60)

    # Carrega URL da foto
    photo_urls = load_photo_urls()
    print(f"✅ Foto carregada")

    # Usa foto configurada (via URL)
    photo_url = get_photo_url(photo_urls)

    # Diretório de output
    output_dir = Path.home() / "Desktop" / "ClaudeCode-Workspace" / "output" / "thumbnails"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n📋 Headline: \"{args.headline}\"")
    print(f"📂 Output: {output_dir}")

    # Gera 4 variações
    results = []
    for style in THUMBNAIL_STYLES:
        result = create_thumbnail_variation(
            photo_url=photo_url,
            headline=args.headline,
            style=style,
            output_dir=output_dir,
            topic=args.topic
        )
        if result:
            results.append(result)

    # Resumo final
    print("\n" + "=" * 60)
    print("🎉 Geração Concluída!")
    print("=" * 60)
    print(f"\n✅ {len(results)}/4 thumbnails criados com sucesso:")
    for path in results:
        print(f"   • {Path(path).name}")

    print(f"\n📂 Pasta: {output_dir}")
    print("\n💡 Escolha a melhor thumbnail e use no seu vídeo do YouTube!")

    return 0 if len(results) == 4 else 1


if __name__ == "__main__":
    sys.exit(main())
