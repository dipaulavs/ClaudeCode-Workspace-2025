#!/usr/bin/env python3
"""
Script para adicionar vídeos do YouTube ao Obsidian Knowledge Base
COM CLASSIFICAÇÃO AUTOMÁTICA POR IA

Uso:
    # Adicionar vídeo com URL (classificação automática)
    python3 scripts/obsidian/add_youtube_video.py "https://youtu.be/VIDEO_ID"

    # Com transcrição
    python3 scripts/obsidian/add_youtube_video.py "URL" --transcricao "caminho/arquivo.txt"

    # Com categoria manual (sobrescreve IA)
    python3 scripts/obsidian/add_youtube_video.py "URL" \
        --categoria "IA & Automação" \
        --rating 5 \
        --duracao "45min"

    # Forçar tipo específico
    python3 scripts/obsidian/add_youtube_video.py "URL" --tipo tutorial
"""

import sys
import os
import re
from pathlib import Path
from datetime import datetime
import argparse

# Adicionar path do config
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'config'))
sys.path.insert(0, str(Path(__file__).parent))

try:
    from obsidian_config import OBSIDIAN_VAULT_PATH, DISPLAY_DATE_FORMAT
except ImportError:
    print("❌ Erro: obsidian_config.py não encontrado!")
    sys.exit(1)

try:
    from youtube_classifier import YouTubeClassifier
except ImportError:
    print("⚠️  Aviso: youtube_classifier.py não encontrado. Classificação desabilitada.")
    YouTubeClassifier = None


# Caminhos
VAULT_PATH = Path(OBSIDIAN_VAULT_PATH)
VIDEOS_BASE_PATH = VAULT_PATH / "09 - YouTube Knowledge" / "Videos"
TRANSCRICOES_PATH = VAULT_PATH / "09 - YouTube Knowledge" / "Transcricoes"
TEMPLATE_PATH = VAULT_PATH / "05 - Templates" / "template-youtube-video.md"


def extract_video_id(url: str) -> str:
    """Extrai ID do vídeo da URL"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]+)',
        r'youtube\.com\/embed\/([a-zA-Z0-9_-]+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def get_rating_stars(rating: int) -> str:
    """Converte número em estrelas"""
    if rating < 1 or rating > 5:
        rating = 3
    return "⭐" * rating


def create_video_note(
    url: str,
    titulo: str = "",
    canal: str = "",
    categoria: str = "",
    duracao: str = "",
    rating: int = 5,
    transcricao_file: str = None,
    tipo: str = None  # novo: tipo forçado (tutorial, metodologia, aula, etc)
):
    """Cria nota do vídeo no Obsidian com classificação automática"""

    video_id = extract_video_id(url)
    if not video_id:
        print(f"❌ URL inválida: {url}")
        return

    # Data atual
    today = datetime.now().strftime(DISPLAY_DATE_FORMAT)  # Para exibição no conteúdo
    today_filename = datetime.now().strftime("%Y-%m-%d")  # Para nome do arquivo

    # Se não tem título, usar ID temporário
    if not titulo:
        titulo = f"Video {video_id}"

    # 🤖 CLASSIFICAÇÃO AUTOMÁTICA POR IA
    tipo_pasta = "Outros"  # default
    classificacao_info = ""

    if tipo:
        # Tipo manual fornecido
        tipos_validos = {
            "tutorial": "Tutoriais",
            "metodologia": "Metodologias",
            "aula": "Aulas",
            "noticia": "Noticias",
            "review": "Reviews",
            "outros": "Outros"
        }
        tipo_pasta = tipos_validos.get(tipo.lower(), "Outros")
        classificacao_info = f"🏷️  Tipo (manual): {tipo_pasta}"
    elif YouTubeClassifier and titulo:
        # Usar IA para classificar
        print(f"\n🤖 Classificando vídeo com IA...")
        try:
            classifier = YouTubeClassifier()
            result = classifier.classify(titulo, canal)

            tipo_pasta = result['pasta']
            classificacao_info = f"""🏷️  Tipo (IA): {tipo_pasta}
   📊 Confiança: {result['confianca']:.0%}
   💡 Razão: {result['razao']}"""

        except Exception as e:
            print(f"⚠️  Erro na classificação: {e}")
            print(f"   Usando pasta padrão: Outros")
            classificacao_info = "🏷️  Tipo: Outros (fallback)"
    else:
        classificacao_info = "🏷️  Tipo: Outros (sem classificação)"

    # Determinar pasta de destino
    VIDEOS_PATH = VIDEOS_BASE_PATH / tipo_pasta

    # Ler transcrição se fornecida
    transcricao_content = ""
    if transcricao_file and Path(transcricao_file).exists():
        with open(transcricao_file, 'r', encoding='utf-8') as f:
            transcricao_content = f.read()

        # Salvar cópia da transcrição
        transcricao_dest = TRANSCRICOES_PATH / f"{video_id}.txt"
        transcricao_dest.write_text(transcricao_content, encoding='utf-8')
        print(f"   💾 Transcrição salva: {transcricao_dest.name}")

    # Criar conteúdo da nota
    rating_stars = get_rating_stars(rating)

    content = f"""---
tipo: youtube-video
titulo: "{titulo}"
url: {url}
canal: {canal}
duracao: {duracao}
data_assistido: {today}
categoria: {categoria}
rating: {rating_stars}
status: 🟡 assistindo
tags:
  - youtube
  - video
  - {categoria.lower().replace(' ', '-') if categoria else 'geral'}
aplicavel: true
implementado: false
---

# 🎬 {titulo}

> **Canal:** {canal} | **Duração:** {duracao} | **Assistido em:** {today}
> **URL:** [Assistir no YouTube]({url})

---

## 📊 Metadados

| Campo | Valor |
|-------|-------|
| **Categoria** | `= this.categoria` |
| **Rating** | `= this.rating` |
| **Status** | `= this.status` |
| **Aplicável?** | `= this.aplicavel` |
| **Já Implementei?** | `= this.implementado` |

---

## 🎯 Objetivo do Vídeo

[Preencher: O que este vídeo ensina/apresenta?]

---

## 📝 Resumo Executivo

1. **Ponto principal 1:**
2. **Ponto principal 2:**
3. **Ponto principal 3:**

---

## 🗂️ Tópicos Abordados

### 1. [Nome do Tópico]
- Subtópico

### 2. [Nome do Tópico]
- Subtópico

---

## ⚙️ Passo a Passo (Se Tutorial)

### Passo 1: [Título]

- [ ] Ação 1
- [ ] Ação 2

**Código:**
```python
# Cole código aqui
```

### Passo 2: [Título]

- [ ] Ação 1

---

## 💡 Insights e Aprendizados

### 🔑 Key Takeaways

1. **Insight 1:**
2. **Insight 2:**
3. **Insight 3:**

### 💭 Minhas Reflexões

[Suas anotações pessoais]

---

## 🔗 Recursos Mencionados

### Ferramentas
- [Nome](url) - Descrição

### Links Úteis
- [Documentação](url)

---

## 🎯 Aplicação Prática

### Como vou usar isso?

[Descreva como você planeja aplicar]

### Projetos onde posso implementar:

- [ ] [[Projeto 1]]

---

## 📊 Transcrição Completa

<details>
<summary><b>📜 Clique para expandir transcrição</b></summary>

### Transcrição Automática

```
{transcricao_content if transcricao_content else '[Cole aqui a transcrição do vídeo]'}
```

</details>

---

## 🏷️ Tags e Categorização

**Tags principais:**
`#{categoria.lower().replace(' ', '-') if categoria else 'geral'}` `#youtube` `#aprendizado`

**Palavras-chave para busca:**
{titulo.lower()} {canal.lower() if canal else ''}

---

## 🔄 Próximos Passos

- [ ] Revisar este conteúdo em 1 semana
- [ ] Implementar em projeto
- [ ] Criar teste prático

---

**Criado em:** {today}
**Última atualização:** {today}
**Video ID:** {video_id}
"""

    # Nome do arquivo (usar formato compatível com filesystem)
    filename = f"{today_filename} - {titulo.replace('/', '-').replace(':', '-')}.md"
    filepath = VIDEOS_PATH / filename

    # Criar pasta se não existir
    VIDEOS_PATH.mkdir(parents=True, exist_ok=True)

    # Salvar arquivo
    filepath.write_text(content, encoding='utf-8')

    # Retornar informações para exibição
    return {
        'filepath': filepath,
        'titulo': titulo,
        'canal': canal,
        'categoria': categoria,
        'duracao': duracao,
        'rating_stars': rating_stars,
        'tipo_pasta': tipo_pasta,
        'classificacao_info': classificacao_info,
        'url': url,
        'video_id': video_id
    }


def update_dashboard_quick_links(filepath: Path):
    """Atualiza tabela de histórico no dashboard"""
    dashboard_path = VAULT_PATH / "09 - YouTube Knowledge" / "YouTube Dashboard.md"

    if not dashboard_path.exists():
        return

    # Ler dashboard
    dashboard_content = dashboard_path.read_text(encoding='utf-8')

    # Buscar últimos 15 vídeos
    videos_path = VIDEOS_BASE_PATH
    all_videos = []

    for video_file in videos_path.rglob("*.md"):
        if video_file.stem not in ["YouTube Dashboard", "README", "Por Rating", "Por Categoria", "Por Tipo", "COMO USAR", "✅ PRONTO - LINKS CLICÁVEIS"]:
            all_videos.append(video_file)

    # Ordenar por data de modificação (mais recentes primeiro)
    all_videos.sort(key=lambda x: x.stat().st_mtime, reverse=True)

    # Pegar apenas os 15 mais recentes
    recent_videos = all_videos[:15]

    # Criar linhas da tabela
    table_rows = []

    for video in recent_videos:
        try:
            content = video.read_text(encoding='utf-8')

            # Extrair rating
            rating_match = re.search(r'rating:\s*(.+)', content)
            rating = rating_match.group(1).strip() if rating_match else "⭐"

            # Extrair categoria
            categoria_match = re.search(r'categoria:\s*(.+)', content)
            categoria = categoria_match.group(1).strip() if categoria_match else "-"

            # Extrair duração
            duracao_match = re.search(r'duracao:\s*(.+)', content)
            duracao = duracao_match.group(1).strip() if duracao_match else "-"

            # Criar linha da tabela
            table_rows.append(f"| [[{video.stem}]] | {rating} | {categoria} | {duracao} |")

        except Exception:
            table_rows.append(f"| [[{video.stem}]] | ⭐ | - | - |")

    # Montar tabela completa
    table_content = "\n".join(table_rows)

    # Padrão regex para encontrar e substituir a tabela
    pattern = r"(\| 📹 Vídeo \| ⭐ Rating \| 📂 Categoria \| ⏱️ Duração \|\n\|----------|-----------|--------------|------------\|\n)(?:\| \[\[.*?\]\] \| .*? \| .*? \| .*? \|\n?)+"

    replacement = f"\\1{table_content}\n"

    # Substituir tabela
    dashboard_content = re.sub(pattern, replacement, dashboard_content)

    # Salvar dashboard atualizado
    dashboard_path.write_text(dashboard_content, encoding='utf-8')


def print_video_summary(video_data: dict):
    """Imprime resumo formatado e bonito do vídeo estudado"""

    filepath = video_data['filepath']
    titulo = video_data['titulo']
    canal = video_data['canal']
    categoria = video_data['categoria']
    duracao = video_data['duracao']
    rating_stars = video_data['rating_stars']
    tipo_pasta = video_data['tipo_pasta']
    url = video_data['url']

    # Nome do arquivo para link obsidian
    filename_without_ext = filepath.stem

    print("\n" + "="*70)
    print("✅ VÍDEO ESTUDADO E SALVO COM SUCESSO!")
    print("="*70)

    print(f"\n📂 **LOCALIZAÇÃO NO OBSIDIAN:**")
    print(f"   {filepath.relative_to(VAULT_PATH)}")

    print(f"\n🎬 **INFORMAÇÕES DO VÍDEO:**")
    print(f"   Título: {titulo}")
    if canal:
        print(f"   Canal: {canal}")
    if categoria:
        print(f"   Categoria: {categoria}")
    if duracao:
        print(f"   Duração: {duracao}")
    print(f"   Rating: {rating_stars}")
    print(f"   Tipo: {tipo_pasta}")

    print(f"\n🔗 **LINKS RÁPIDOS:**")
    print(f"   📊 Dashboard: obsidian://open?vault=Claude-code-ios&file=09%20-%20YouTube%20Knowledge/YouTube%20Dashboard")
    print(f"   📹 Ver resumo: obsidian://open?vault=Claude-code-ios&file=09%20-%20YouTube%20Knowledge/Videos/{tipo_pasta}/{filename_without_ext}")
    print(f"   🎥 Assistir no YouTube: {url}")

    print(f"\n💡 **PRÓXIMOS PASSOS:**")
    print(f"   1. Abrir o dashboard do Obsidian: [[YouTube Dashboard]]")
    print(f"   2. Ler o resumo completo: [[{filename_without_ext}]]")
    print(f"   3. Marcar insights importantes no arquivo")
    print(f"   4. Aplicar aprendizados em seus projetos")

    print("\n" + "="*70)
    print("🎯 ACESSO RÁPIDO AO RESUMO:")
    print("="*70)
    print(f"\nPara abrir no Obsidian, clique em:")
    print(f"   [[{filename_without_ext}]]")
    print(f"\nOu busque por: {titulo[:50]}...")
    print("\n" + "="*70 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Adicionar vídeos do YouTube ao Obsidian Knowledge Base (com IA)'
    )

    parser.add_argument('url', help='URL do vídeo do YouTube')
    parser.add_argument('--titulo', default='', help='Título do vídeo')
    parser.add_argument('--canal', default='', help='Nome do canal')
    parser.add_argument('--categoria', default='', help='Categoria (IA, Programação, Marketing, etc)')
    parser.add_argument('--duracao', default='', help='Duração (ex: 45min)')
    parser.add_argument('--rating', type=int, default=5, help='Rating de 1 a 5 estrelas')
    parser.add_argument('--transcricao', help='Caminho do arquivo de transcrição')
    parser.add_argument('--tipo', help='Tipo do vídeo (tutorial|metodologia|aula|noticia|review|outros)')

    args = parser.parse_args()

    # Criar pastas base se não existirem
    VIDEOS_BASE_PATH.mkdir(parents=True, exist_ok=True)
    TRANSCRICOES_PATH.mkdir(parents=True, exist_ok=True)

    # Criar nota do vídeo
    video_data = create_video_note(
        url=args.url,
        titulo=args.titulo,
        canal=args.canal,
        categoria=args.categoria,
        duracao=args.duracao,
        rating=args.rating,
        transcricao_file=args.transcricao,
        tipo=args.tipo
    )

    # Exibir resumo formatado
    if video_data:
        # Atualizar links rápidos no dashboard
        try:
            update_dashboard_quick_links(video_data['filepath'])
        except Exception as e:
            print(f"⚠️  Aviso: Não foi possível atualizar dashboard ({e})")

        print_video_summary(video_data)


if __name__ == '__main__':
    main()
