#!/usr/bin/env python3
"""Gerador de Imagens com IA usando OpenAI DALL-E"""
import os, sys, requests, json, argparse
from datetime import datetime

class AIImageGenerator:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            print("❌ OPENAI_API_KEY não encontrada!")
            print("💡 Configure: export OPENAI_API_KEY='sua-chave'")
            sys.exit(1)

        self.api_url = "https://api.openai.com/v1/images/generations"

    def generate_image(self, prompt, size="1024x1024", quality="standard", output_dir=None):
        """Gera imagem usando DALL-E 3"""
        print("🎨 GERANDO IMAGEM COM IA")
        print("=" * 60)
        print(f"📝 Prompt: {prompt}")
        print(f"📐 Tamanho: {size}")
        print(f"✨ Qualidade: {quality}")
        print("=" * 60)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "dall-e-3",
            "prompt": prompt,
            "n": 1,
            "size": size,
            "quality": quality
        }

        try:
            print("\n⏳ Gerando imagem...")
            resp = requests.post(self.api_url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()

            image_url = data['data'][0]['url']
            revised_prompt = data['data'][0].get('revised_prompt', prompt)

            print(f"✅ Imagem gerada!")
            print(f"📸 URL: {image_url[:50]}...")
            print(f"📝 Prompt revisado: {revised_prompt[:100]}...")

            # Baixar imagem
            print("\n⬇️  Baixando imagem...")
            img_response = requests.get(image_url)
            img_response.raise_for_status()

            # Salvar arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ai_generated_{timestamp}.png"

            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                filepath = os.path.join(output_dir, filename)
            else:
                filepath = os.path.join(os.path.expanduser("~/Downloads"), filename)

            with open(filepath, 'wb') as f:
                f.write(img_response.content)

            print(f"✅ Imagem salva: {filepath}")
            print(f"💾 Tamanho: {len(img_response.content) / 1024:.2f} KB")

            return filepath

        except requests.exceptions.HTTPError as e:
            print(f"❌ Erro na API: {e}")
            if hasattr(e.response, 'text'):
                print(f"Detalhes: {e.response.text}")
            return None
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(description="Gerador de Imagens com IA (DALL-E 3)")
    parser.add_argument("prompt", help="Descrição da imagem a ser gerada")
    parser.add_argument("--size", default="1024x1024", choices=["1024x1024", "1792x1024", "1024x1792"])
    parser.add_argument("--quality", default="standard", choices=["standard", "hd"])
    parser.add_argument("--output", help="Diretório de saída (padrão: ~/Downloads)")
    parser.add_argument("--api-key", help="OpenAI API Key (ou use OPENAI_API_KEY env var)")

    args = parser.parse_args()

    generator = AIImageGenerator(api_key=args.api_key)
    filepath = generator.generate_image(
        prompt=args.prompt,
        size=args.size,
        quality=args.quality,
        output_dir=args.output
    )

    if filepath:
        print(f"\n✅ Sucesso! Use este arquivo: {filepath}")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
