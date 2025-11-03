#!/usr/bin/env python3
"""
Teste: Gerar 2 thumbnails de teste
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))

from edit_image_nanobanana import edit_image, wait_for_completion, download_image

# URL da foto
IMAGE_URL = "https://media.loop9.com.br/s/zn7mPtT7m8soY6f/download/boa%202.png"

# 2 prompts - PADRÃO APROVADO EXATO (a thumb que o usuário gostou)
prompts = [
    # Variação 1: EXATAMENTE o padrão aprovado
    """YouTube thumbnail 16:9 INTENSE DRAMATIC CINEMATIC:

LIGHTING (INTENSE DRAMATIC):
- STRONG intense blue/cyan light hitting LEFT side of face (VERY BRIGHT, #00D4FF glow)
- Deep black shadows on right side creating extreme contrast
- Volumetric light rays visible in atmosphere (HEAVY smoke/fog/mist clearly visible, cinematic depth)
- Face dramatically lit with high contrast split lighting
- One side VERY BRIGHT blue/cyan, other side deep shadow
- Similar intensity to professional movie posters

COMPOSITION: Asymmetric layout - person RIGHT 50%, text LEFT 50%

PERSON MANIPULATION:
- Position on right side of frame
- Add laptop with bright screen glow
- Adjust arms/hands typing position
- Face expression: Intense focused (dramatic)
- Show upper body in dark professional attire
- Strong rim lighting creating edge glow

BACKGROUND: Pure pitch black with HEAVY blue/cyan atmospheric smoke/fog/haze visible throughout (cinematic movie poster style, volumetric lighting, dramatic mist/fog clearly visible, not subtle)

LEFT SIDE - HARMONIZED TYPOGRAPHY (PT-BR):
- 'DE R$60/MÊS' in GOLDEN YELLOW (#FFD700) bold with dark outline (complementary to cyan lighting)
- 'PARA R$0' HUGE in bright ORANGE/AMBER (#FF8C00) with glow effect (warm complement)
- 'SEM PERDER ARQUIVOS' in WHITE with dark shadow
- Faded cloud icons with red X marks

COLOR HARMONY:
- Text colors (yellow/orange/gold) complement the blue/cyan face lighting
- High contrast for readability
- Professional color theory applied

STYLE: CINEMATIC MOVIE POSTER aesthetic - intense dramatic like professional film posters, heavy volumetric fog/smoke visible, atmospheric depth, strong lighting, harmonized color palette, viral YouTube thumbnail quality""",

    # Variação 2: Mesmo padrão, leve variação na expressão
    """YouTube thumbnail 16:9 INTENSE DRAMATIC CINEMATIC:

LIGHTING (INTENSE DRAMATIC):
- STRONG intense blue/cyan light hitting LEFT side of face (VERY BRIGHT, #00D4FF glow)
- Deep black shadows on right side creating extreme contrast
- Volumetric light rays visible in atmosphere (HEAVY smoke/fog/mist clearly visible, cinematic depth)
- Face dramatically lit with high contrast split lighting
- One side VERY BRIGHT blue/cyan, other side deep shadow
- Similar intensity to professional movie posters

COMPOSITION: Asymmetric layout - person RIGHT 50%, text LEFT 50%

PERSON MANIPULATION:
- Position on right side of frame
- Add laptop with bright screen glow
- Adjust arms/hands typing position
- Face expression: Confident determined (slight variation from first)
- Show upper body in dark professional attire
- Strong rim lighting creating edge glow

BACKGROUND: Pure pitch black with HEAVY blue/cyan atmospheric smoke/fog/haze visible throughout (cinematic movie poster style, volumetric lighting, dramatic mist/fog clearly visible, not subtle)

LEFT SIDE - HARMONIZED TYPOGRAPHY (PT-BR):
- 'DE R$60/MÊS' in GOLDEN YELLOW (#FFD700) bold with dark outline (complementary to cyan lighting)
- 'PARA R$0' HUGE in bright ORANGE/AMBER (#FF8C00) with glow effect (warm complement)
- 'SEM PERDER ARQUIVOS' in WHITE with dark shadow
- Faded cloud icons with red X marks

COLOR HARMONY:
- Text colors (yellow/orange/gold) complement the blue/cyan face lighting
- High contrast for readability
- Professional color theory applied

STYLE: CINEMATIC MOVIE POSTER aesthetic - intense dramatic like professional film posters, heavy volumetric fog/smoke visible, atmospheric depth, strong lighting, harmonized color palette, viral YouTube thumbnail quality"""
]

print("🎬 Teste: 2 Thumbnails")
print("=" * 60)

# Gera as 2 imagens
for i, prompt in enumerate(prompts, 1):
    print(f"\n[{i}/2] Gerando thumbnail...")

    # Cria tarefa
    task_id = edit_image(
        prompt=prompt,
        image_url=IMAGE_URL,
        output_format="PNG",
        image_size="16:9",
        num_outputs=1
    )

    if not task_id:
        print(f"❌ Falha na tarefa {i}")
        continue

    # Aguarda conclusão
    image_urls = wait_for_completion(task_id)

    if not image_urls:
        print(f"❌ Falha ao gerar thumbnail {i}")
        continue

    # Baixa
    print(f"\n📥 Baixando thumbnail {i}...")
    for url in image_urls:
        filepath = download_image(url)
        if filepath:
            print(f"✅ Salvo: {filepath}")

print(f"\n✅ Processo concluído!")
print(f"📂 ~/Downloads")
