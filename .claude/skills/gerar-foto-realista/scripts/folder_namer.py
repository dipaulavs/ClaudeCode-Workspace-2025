#!/usr/bin/env python3
"""
Folder Namer - Gera nomes inteligentes para pastas de batch

Cria nomes resumidos e descritivos baseados no prompt.
Formato: {resumo}_{count}_fotos/
"""

import sys
import re
import os
import requests

# Configuração OpenRouter
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "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")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """Você é um gerador de nomes de pastas.

Receba um prompt de imagem e retorne um nome curto e descritivo para pasta.

REGRAS:
1. Máximo 3 palavras
2. Remover artigos (o, a, de, em, com, etc)
3. Usar underscore (_) entre palavras
4. Tudo minúsculo
5. Sem acentos
6. Sem caracteres especiais
7. Substantivos mais importantes

EXEMPLOS:

Input: "golden retriever sentado em quintal com grama verde, luz natural..."
Output: cachorro_quintal

Input: "carro sedan prata estacionado em rua urbana residencial..."
Output: carro_rua

Input: "prato de comida caseira em mesa de madeira clara..."
Output: comida_mesa

Input: "paisagem de montanha com neve ao pôr do sol..."
Output: montanha_neve

Input: "pessoa correndo na praia ao amanhecer..."
Output: corrida_praia

IMPORTANTE: Retorne APENAS o nome da pasta, sem explicações."""


def slugify(text: str) -> str:
    """Remove acentos e caracteres especiais"""
    # Remove acentos
    import unicodedata
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')

    # Remove caracteres especiais
    text = re.sub(r'[^a-z0-9_]', '_', text.lower())

    # Remove underscores duplicados
    text = re.sub(r'_+', '_', text)

    # Remove underscores no início/fim
    text = text.strip('_')

    return text


def create_folder_name(prompt: str, count: int) -> str:
    """
    Gera nome inteligente para pasta de batch

    Args:
        prompt: Prompt completo da imagem
        count: Quantidade de fotos

    Returns:
        Nome da pasta (ex: "cachorro_quintal_5_fotos")
    """

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/felipemdepaula",
                "X-Title": "Gerar Foto Realista - Folder Namer"
            },
            json={
                "model": "anthropic/claude-3.5-haiku",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.5,
                "max_tokens": 50
            },
            timeout=15
        )

        response.raise_for_status()
        data = response.json()

        base_name = data["choices"][0]["message"]["content"].strip()
        base_name = slugify(base_name)

    except Exception as e:
        print(f"⚠️  Erro ao gerar nome: {e}. Usando fallback.", file=sys.stderr)
        # Fallback: pegar primeiras 2 palavras do prompt
        words = re.findall(r'\b\w+\b', prompt.lower())
        base_name = '_'.join(words[:2])
        base_name = slugify(base_name)

    # Adiciona quantidade
    folder_name = f"{base_name}_{count}_fotos"

    return folder_name


def main():
    """CLI para testar o folder namer"""

    if len(sys.argv) < 3:
        print("Uso: python3 folder_namer.py 'prompt' <quantidade>")
        print("\nExemplos:")
        print('  python3 folder_namer.py "cachorro em quintal" 5')
        print('  python3 folder_namer.py "carro na rua" 3')
        print('  python3 folder_namer.py "comida na mesa" 10')
        sys.exit(1)

    prompt = sys.argv[1]
    count = int(sys.argv[2])

    print(f"📝 Prompt: {prompt}")
    print(f"🔢 Quantidade: {count}")
    print(f"🤖 Gerando nome...\n")

    folder_name = create_folder_name(prompt, count)

    print(f"📁 Nome da pasta: {folder_name}")

    return folder_name


if __name__ == "__main__":
    main()
