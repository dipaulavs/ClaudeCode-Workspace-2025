#!/usr/bin/env python3
"""
Script para editar múltiplas thumbnails YouTube simultaneamente usando Nano Banana Edit
Cria todas as tarefas de uma vez e monitora em paralelo para máxima eficiência
"""

import requests
import time
import sys
import json
import os
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuração da API
API_KEY = "fa32b7ea4ff0e9b5acce83abe09d2b06"
BASE_URL = "https://api.kie.ai"
GENERATE_ENDPOINT = f"{BASE_URL}/api/v1/jobs/createTask"
STATUS_ENDPOINT = f"{BASE_URL}/api/v1/jobs/recordInfo"

# URL da foto base
BASE_IMAGE_URL = "https://media.loop9.com.br/s/C9WLo3EytYjNKwm/download/foto1.jpg"

# Pasta de Downloads
DOWNLOADS_PATH = str(Path.home() / "Downloads")

# Headers para autenticação
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def create_edit_task(prompt, image_url, output_format="PNG", image_size="16:9"):
    """
    Cria uma tarefa de edição de thumbnail (não aguarda conclusão)

    Args:
        prompt: Descrição da edição
        image_url: URL da imagem base
        output_format: Formato da imagem (PNG ou JPEG)
        image_size: Proporção (16:9 para YouTube)

    Returns:
        dict com task_id e prompt, ou None se erro
    """
    payload = {
        "model": "google/nano-banana-edit",
        "input": {
            "prompt": prompt,
            "image_urls": [image_url],
            "image_size": image_size,
            "output_format": output_format.lower(),
            "num_outputs": 1
        }
    }

    try:
        response = requests.post(GENERATE_ENDPOINT, headers=HEADERS, json=payload)
        response.raise_for_status()

        data = response.json()
        if data.get("code") == 200:
            task_id = data["data"]["taskId"]
            return {
                "task_id": task_id,
                "prompt": prompt,
                "status": "created"
            }
        else:
            return None

    except requests.exceptions.RequestException:
        return None


def check_task_status(task_id):
    """
    Verifica o status de uma tarefa

    Returns:
        dict com status e image_urls (se pronto)
    """
    try:
        params = {"taskId": task_id}
        response = requests.get(STATUS_ENDPOINT, headers=HEADERS, params=params)
        response.raise_for_status()

        result = response.json()
        status = result.get("data", {}).get("state")

        if status == "success":
            result_json_str = result.get("data", {}).get("resultJson", "{}")
            result_json = json.loads(result_json_str)
            return {
                "status": "success",
                "image_urls": result_json.get("resultUrls", [])
            }
        elif status == "fail":
            return {"status": "failed"}
        else:
            return {"status": "processing"}

    except Exception:
        return {"status": "error"}


def download_image(url, output_path):
    """Baixa uma imagem da URL"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return output_path
    except Exception:
        return None


def monitor_and_download(task_info, output_format="PNG"):
    """
    Monitora uma tarefa até conclusão e baixa a thumbnail

    Args:
        task_info: dict com task_id e prompt
        output_format: formato da imagem

    Returns:
        dict com resultado
    """
    task_id = task_info["task_id"]
    prompt = task_info["prompt"]

    max_wait = 300
    check_interval = 3
    start_time = time.time()

    while time.time() - start_time < max_wait:
        result = check_task_status(task_id)

        if result["status"] == "success":
            image_urls = result["image_urls"]
            if image_urls:
                url = image_urls[0]

                # Define nome do arquivo
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                # Sanitiza o prompt para nome de arquivo
                safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
                safe_prompt = safe_prompt.replace(' ', '_')

                ext = ".jpg" if output_format.upper() == "JPEG" else ".png"
                output_path = os.path.join(DOWNLOADS_PATH, f"thumbnail_{safe_prompt}_{timestamp}{ext}")

                # Baixa a imagem
                downloaded = download_image(url, output_path)

                if downloaded:
                    return {
                        "success": True,
                        "prompt": prompt,
                        "path": output_path,
                        "url": url
                    }

            return {"success": False, "prompt": prompt, "error": "No image URL"}

        elif result["status"] == "failed":
            return {"success": False, "prompt": prompt, "error": "Edit failed"}

        time.sleep(check_interval)

    return {"success": False, "prompt": prompt, "error": "Timeout"}


def edit_batch(prompts, image_url=BASE_IMAGE_URL, output_format="PNG", image_size="16:9"):
    """
    Edita múltiplas thumbnails em paralelo

    Args:
        prompts: lista de prompts
        image_url: URL da imagem base
        output_format: formato das imagens
        image_size: proporção das imagens

    Returns:
        lista de resultados
    """
    print(f"\n🎬 Gerador de Thumbnails YouTube - Nano Banana Edit")
    print(f"📝 {len(prompts)} thumbnails para gerar")
    print(f"🖼️  Formato: {output_format} | Proporção: {image_size}")
    print(f"📷 Foto base: {image_url}")
    print(f"⚡ Modo: Paralelo (todas ao mesmo tempo)\n")

    # Fase 1: Criar todas as tarefas
    print("🚀 Fase 1: Criando todas as tarefas de edição...")
    tasks = []

    for i, prompt in enumerate(prompts, 1):
        print(f"   [{i}/{len(prompts)}] {prompt[:60]}...")
        task = create_edit_task(prompt, image_url, output_format, image_size)
        if task:
            tasks.append(task)
            print(f"   ✅ Task ID: {task['task_id']}")
        else:
            print(f"   ❌ Falha ao criar tarefa")

    if not tasks:
        print("\n❌ Nenhuma tarefa foi criada com sucesso")
        return []

    print(f"\n✅ {len(tasks)} tarefas criadas com sucesso!")
    print(f"\n⏳ Fase 2: Monitorando e baixando ({len(tasks)} em paralelo)...")

    # Fase 2: Monitorar todas as tarefas em paralelo
    results = []
    completed = 0

    with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        future_to_task = {
            executor.submit(monitor_and_download, task, output_format): task
            for task in tasks
        }

        for future in as_completed(future_to_task):
            completed += 1
            result = future.result()
            results.append(result)

            if result["success"]:
                print(f"   ✅ [{completed}/{len(tasks)}] {result['prompt'][:40]}...")
                print(f"      💾 {result['path']}")
                print(f"      🔗 {result['url']}")
            else:
                print(f"   ❌ [{completed}/{len(tasks)}] {result['prompt'][:40]}...")
                print(f"      ⚠️  {result.get('error', 'Unknown error')}")

    return results


def main():
    """Função principal com suporte a argumentos ou modo teste"""

    import sys

    # Se recebeu argumentos, usa os prompts fornecidos
    if len(sys.argv) > 1:
        # Modo produção: prompts via argumentos
        prompts = []
        for arg in sys.argv[1:]:
            if arg.startswith("--"):
                # Ignora flags (para futuras expansões)
                continue
            prompts.append(arg)

        if not prompts:
            print("❌ Erro: Nenhum prompt fornecido")
            print("\nUso:")
            print('  python3 tools/batch_edit_thumbnails.py "prompt 1" "prompt 2" "prompt 3"')
            print("\nExemplo:")
            print('  python3 tools/batch_edit_thumbnails.py "$(cat prompt1.txt)" "$(cat prompt2.txt)"')
            print("\nOu execute sem argumentos para rodar modo teste com 5 prompts.")
            sys.exit(1)

        print(f"🎬 Gerador de Thumbnails YouTube - Modo Produção")
        print("="*60)

        # Gera as thumbnails
        start_time = time.time()
        results = edit_batch(prompts)
        elapsed = time.time() - start_time

        # Resumo
        print(f"\n{'='*60}")
        print(f"✨ Processamento concluído em {elapsed:.1f}s")
        print(f"{'='*60}\n")

        successful = [r for r in results if r["success"]]
        failed = [r for r in results if not r["success"]]

        print(f"✅ Sucesso: {len(successful)}/{len(results)}")
        if successful:
            for r in successful:
                print(f"   📁 {os.path.basename(r['path'])}")
                print(f"   🔗 {r['url']}\n")

        if failed:
            print(f"\n❌ Falhas: {len(failed)}")
            for r in failed:
                print(f"   ⚠️  {r['prompt'][:50]} - {r.get('error', 'Unknown')}")

        print(f"\n📂 Localização: {DOWNLOADS_PATH}")
        return 0 if not failed else 1

    # Modo teste: 5 prompts hardcoded
    print("🎬 Teste: Gerando 5 Thumbnails YouTube")
    print("="*60)

    # 5 prompts de teste baseados no template (TEXTO ESQUERDA, FOTO DIREITA)
    test_prompts = [
        """Crie uma thumbnail de tecnologia para um vídeo sobre IA.
Texto e Gráficos (no lado esquerdo da imagem): Título: Escreva "INTELIGÊNCIA ARTIFICIAL" em letras maiúsculas, com uma fonte moderna e contornada em dourado. Subtítulo: Abaixo do título, insira uma barra dourada sólida com o texto "O FUTURO AGORA" em letras maiúsculas. Data: Abaixo da barra, adicione "2025" em uma fonte branca e limpa. Selo: No canto inferior esquerdo, adicione um pequeno texto "Novo".
Foto Principal: Use a minha foto em um close-up, do peito para cima. O meu rosto deve ocupar a metade direita da imagem, com um olhar sério e direto para a câmera.
Iluminação: Aplique uma iluminação de estúdio dramática com o estilo 'split lighting'. Metade do meu rosto deve estar em sombra profunda, enquanto a outra metade é iluminada por uma luz azul-ciano fria. Se eu estiver usando óculos, adicione um reflexo laranja vibrante nas lentes.
Fundo: O fundo deve ser preto e escuro.
Estilo Geral: A imagem deve ter um clima profissional, tecnológico e de alto impacto, com uma paleta de cores focada em preto, dourado e o contraste do azul-ciano.""",

        """Crie uma thumbnail de tecnologia para um vídeo sobre produtividade.
Texto e Gráficos (no lado esquerdo da imagem): Título: Escreva "PRODUTIVIDADE 10X" em letras maiúsculas, com uma fonte moderna e contornada em dourado. Subtítulo: Abaixo do título, insira uma barra dourada sólida com o texto "MÉTODO COMPROVADO" em letras maiúsculas. Data: Abaixo da barra, adicione "06/11, quinta" em uma fonte branca e limpa. Selo: No canto inferior esquerdo, adicione um pequeno texto "Imperdível".
Foto Principal: Use a minha foto em um close-up, do peito para cima. O meu rosto deve ocupar a metade direita da imagem, com um olhar sério e direto para a câmera.
Iluminação: Aplique uma iluminação de estúdio dramática com o estilo 'split lighting'. Metade do meu rosto deve estar em sombra profunda, enquanto a outra metade é iluminada por uma luz azul-ciano fria. Se eu estiver usando óculos, adicione um reflexo laranja vibrante nas lentes.
Fundo: O fundo deve ser preto e escuro.
Estilo Geral: A imagem deve ter um clima profissional, tecnológico e de alto impacto, com uma paleta de cores focada em preto, dourado e o contraste do azul-ciano.""",

        """Crie uma thumbnail de tecnologia para um vídeo sobre empreendedorismo.
Texto e Gráficos (no lado esquerdo da imagem): Título: Escreva "EMPREENDER HOJE" em letras maiúsculas, com uma fonte moderna e contornada em dourado. Subtítulo: Abaixo do título, insira uma barra dourada sólida com o texto "DO ZERO AO MILHÃO" em letras maiúsculas. Data: Abaixo da barra, adicione "10/11, segunda | 20h" em uma fonte branca e limpa. Selo: No canto inferior esquerdo, adicione um pequeno texto "Exclusivo".
Foto Principal: Use a minha foto em um close-up, do peito para cima. O meu rosto deve ocupar a metade direita da imagem, com um olhar sério e direto para a câmera.
Iluminação: Aplique uma iluminação de estúdio dramática com o estilo 'split lighting'. Metade do meu rosto deve estar em sombra profunda, enquanto a outra metade é iluminada por uma luz azul-ciano fria. Se eu estiver usando óculos, adicione um reflexo laranja vibrante nas lentes.
Fundo: O fundo deve ser preto e escuro.
Estilo Geral: A imagem deve ter um clima profissional, tecnológico e de alto impacto, com uma paleta de cores focada em preto, dourado e o contraste do azul-ciano.""",

        """Crie uma thumbnail de tecnologia para um vídeo sobre automação.
Texto e Gráficos (no lado esquerdo da imagem): Título: Escreva "AUTOMAÇÃO TOTAL" em letras maiúsculas, com uma fonte moderna e contornada em dourado. Subtítulo: Abaixo do título, insira uma barra dourada sólida com o texto "TRABALHE MENOS" em letras maiúsculas. Data: Abaixo da barra, adicione "12/11, terça | 18h" em uma fonte branca e limpa. Selo: No canto inferior esquerdo, adicione um pequeno texto "Premium".
Foto Principal: Use a minha foto em um close-up, do peito para cima. O meu rosto deve ocupar a metade direita da imagem, com um olhar sério e direto para a câmera.
Iluminação: Aplique uma iluminação de estúdio dramática com o estilo 'split lighting'. Metade do meu rosto deve estar em sombra profunda, enquanto a outra metade é iluminada por uma luz azul-ciano fria. Se eu estiver usando óculos, adicione um reflexo laranja vibrante nas lentes.
Fundo: O fundo deve ser preto e escuro.
Estilo Geral: A imagem deve ter um clima profissional, tecnológico e de alto impacto, com uma paleta de cores focada em preto, dourado e o contraste do azul-ciano.""",

        """Crie uma thumbnail de tecnologia para um vídeo sobre marketing digital.
Texto e Gráficos (no lado esquerdo da imagem): Título: Escreva "MARKETING 3.0" em letras maiúsculas, com uma fonte moderna e contornada em dourado. Subtítulo: Abaixo do título, insira uma barra dourada sólida com o texto "VENDA MAIS ONLINE" em letras maiúsculas. Data: Abaixo da barra, adicione "15/11, sexta | 21h" em uma fonte branca e limpa. Selo: No canto inferior esquerdo, adicione um pequeno texto "Ao Vivo".
Foto Principal: Use a minha foto em um close-up, do peito para cima. O meu rosto deve ocupar a metade direita da imagem, com um olhar sério e direto para a câmera.
Iluminação: Aplique uma iluminação de estúdio dramática com o estilo 'split lighting'. Metade do meu rosto deve estar em sombra profunda, enquanto a outra metade é iluminada por uma luz azul-ciano fria. Se eu estiver usando óculos, adicione um reflexo laranja vibrante nas lentes.
Fundo: O fundo deve ser preto e escuro.
Estilo Geral: A imagem deve ter um clima profissional, tecnológico e de alto impacto, com uma paleta de cores focada em preto, dourado e o contraste do azul-ciano."""
    ]

    print("🎬 Teste: Gerando 5 Thumbnails YouTube")
    print("="*60)

    # Gera as thumbnails em lote
    start_time = time.time()
    results = edit_batch(test_prompts)
    elapsed = time.time() - start_time

    # Resumo
    print(f"\n{'='*60}")
    print(f"✨ Processamento concluído em {elapsed:.1f}s")
    print(f"{'='*60}\n")

    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    print(f"✅ Sucesso: {len(successful)}/{len(results)}")
    if successful:
        for r in successful:
            print(f"   📁 {os.path.basename(r['path'])}")
            print(f"   🔗 {r['url']}\n")

    if failed:
        print(f"\n❌ Falhas: {len(failed)}")
        for r in failed:
            print(f"   ⚠️  {r['prompt'][:50]} - {r.get('error', 'Unknown')}")

    print(f"\n📂 Localização: {DOWNLOADS_PATH}")


if __name__ == "__main__":
    main()
