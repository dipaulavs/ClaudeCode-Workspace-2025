#!/usr/bin/env python3
"""Meta Ads - Upload de Imagens"""
import requests, sys, os, json, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import meta_ads_config as config

class MetaAdsImageUploader:
    def __init__(self):
        if not config.validate_config():
            sys.exit(1)
        self.access_token = config.ACCESS_TOKEN
        self.ad_account_id = config.AD_ACCOUNT_ID

    def upload_image(self, image_path):
        """Faz upload de uma imagem e retorna o hash"""
        print(f"📤 FAZENDO UPLOAD DA IMAGEM")
        print("=" * 60)
        print(f"📁 Arquivo: {os.path.basename(image_path)}")

        if not os.path.exists(image_path):
            print(f"❌ Erro: Arquivo não encontrado: {image_path}")
            return None

        url = f"{config.BASE_URL}/{self.ad_account_id}/adimages"

        try:
            with open(image_path, 'rb') as f:
                files = {'file': f}
                params = {'access_token': self.access_token}

                resp = requests.post(url, params=params, files=files)
                resp.raise_for_status()
                data = resp.json()

                # A resposta vem no formato: {"images": {"filename.jpg": {"hash": "xxx"}}}
                images = data.get('images', {})
                if images:
                    first_image = list(images.values())[0]
                    image_hash = first_image.get('hash')
                    print(f"✅ Upload concluído!")
                    print(f"🔑 Hash: {image_hash}")
                    return image_hash
                else:
                    print("❌ Erro: Resposta inesperada da API")
                    print(json.dumps(data, indent=2))
                    return None

        except Exception as e:
            print(f"❌ Erro ao fazer upload: {e}")
            if hasattr(e, 'response'):
                print(e.response.text)
            return None

def main():
    parser = argparse.ArgumentParser(description="Meta Ads - Upload de Imagens")
    parser.add_argument("image_path", help="Caminho da imagem para upload")

    args = parser.parse_args()

    uploader = MetaAdsImageUploader()
    image_hash = uploader.upload_image(args.image_path)

    if image_hash:
        print(f"\n✅ Use este hash no criativo: {image_hash}")

if __name__ == "__main__":
    main()
