#!/usr/bin/env python3
"""
Teste: Gerar 3 thumbnails ao mesmo tempo (batch paralelo)
"""

import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "tools"))

from edit_image_nanobanana import edit_image, wait_for_completion, download_image

# URL da foto aprovada
IMAGE_URL = "https://media.loop9.com.br/s/zn7mPtT7m8soY6f/download/boa%202.png"

# 3 prompts - Padrão aprovado com variações sutis
prompts = [
    # Variação 1: Expressão intensa focada
    """YouTube thumbnail 16:9 INTENSE DRAMATIC CINEMATIC:

LIGHTING (INTENSE DRAMATIC):
- STRONG intense blue/cyan light hitting LEFT side of face (VERY BRIGHT, #00D4FF glow)
- Deep black shadows on right side creating extreme contrast
- Volumetric light rays visible in atmosphere (HEAVY smoke/fog/mist clearly visible, cinematic depth)
- Face dramatically lit with high contrast split lighting
- One side VERY BRIGHT blue/cyan, other side deep shadow
- Similar intensity to professional movie posters

COMPOSITION: Asymmetric layout - person RIGHT 60%, text LEFT 40%

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

    # Variação 2: Expressão confiante determinada
    """YouTube thumbnail 16:9 INTENSE DRAMATIC CINEMATIC:

LIGHTING (INTENSE DRAMATIC):
- STRONG intense blue/cyan light hitting LEFT side of face (VERY BRIGHT, #00D4FF glow)
- Deep black shadows on right side creating extreme contrast
- Volumetric light rays visible in atmosphere (HEAVY smoke/fog/mist clearly visible, cinematic depth)
- Face dramatically lit with high contrast split lighting
- One side VERY BRIGHT blue/cyan, other side deep shadow
- Similar intensity to professional movie posters

COMPOSITION: Asymmetric layout - person RIGHT 60%, text LEFT 40%

PERSON MANIPULATION:
- Position on right side of frame
- Add laptop with bright screen glow
- Adjust arms/hands typing position
- Face expression: Confident determined (slight smile, looking at camera)
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

    # Variação 3: Ângulo e posição ligeiramente diferente
    """YouTube thumbnail 16:9 INTENSE DRAMATIC CINEMATIC:

LIGHTING (INTENSE DRAMATIC):
- STRONG intense blue/cyan light hitting LEFT side of face (VERY BRIGHT, #00D4FF glow)
- Deep black shadows on right side creating extreme contrast
- Volumetric light rays visible in atmosphere (HEAVY smoke/fog/mist clearly visible, cinematic depth)
- Face dramatically lit with high contrast split lighting
- One side VERY BRIGHT blue/cyan, other side deep shadow
- Similar intensity to professional movie posters

COMPOSITION: Asymmetric layout - person RIGHT 60%, text LEFT 40%

PERSON MANIPULATION:
- Position on right side of frame (slightly angled toward text)
- Add laptop with bright screen glow
- Adjust arms/hands typing position
- Face expression: Professional focused (looking slightly toward text area)
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


def create_edit_task(prompt, image_url, task_number):
    """Cria uma tarefa de edição de imagem"""
    print(f"\n[{task_number}/3] Criando tarefa...")
    task_id = edit_image(
        prompt=prompt,
        image_url=image_url,
        output_format="PNG",
        image_size="16:9",
        num_outputs=1
    )
    return {"task_id": task_id, "task_number": task_number}


def monitor_task(task_info):
    """Monitora uma tarefa até conclusão"""
    task_id = task_info["task_id"]
    task_number = task_info["task_number"]

    if not task_id:
        print(f"❌ Tarefa {task_number} falhou na criação")
        return None

    print(f"[{task_number}/3] Aguardando conclusão da tarefa {task_id}...")

    # Aguarda conclusão
    image_urls = wait_for_completion(task_id)

    if not image_urls:
        print(f"❌ Tarefa {task_number} falhou na geração")
        return None

    # Baixa imagens
    print(f"\n📥 Baixando imagens da tarefa {task_number}...")
    filepaths = []
    for url in image_urls:
        filepath = download_image(url)
        if filepath:
            filepaths.append(filepath)
            print(f"✅ Salvo: {filepath}")

    return {"task_number": task_number, "filepaths": filepaths}


print("🎬 Teste: 3 Thumbnails em Paralelo")
print("=" * 60)

# Cria as 3 tarefas
print("\n📋 Criando 3 tarefas de edição...")
tasks = []
for i, prompt in enumerate(prompts, 1):
    task = create_edit_task(prompt, IMAGE_URL, i)
    tasks.append(task)

# Monitora todas as tarefas em paralelo
print(f"\n⏳ Monitorando {len(tasks)} tarefas em paralelo...")
results = []

with ThreadPoolExecutor(max_workers=3) as executor:
    future_to_task = {executor.submit(monitor_task, task): task for task in tasks}

    for future in as_completed(future_to_task):
        result = future.result()
        if result:
            results.append(result)

# Resumo final
print(f"\n{'=' * 60}")
print(f"✅ Processo concluído!")
print(f"📊 {len(results)}/{len(tasks)} tarefas bem-sucedidas")
print(f"📂 Imagens salvas em: ~/Downloads")
