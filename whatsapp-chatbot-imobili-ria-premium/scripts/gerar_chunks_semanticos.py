#!/usr/bin/env python3
"""
🧠 Gera chunks semânticos + embeddings para carros

Quebra documento consolidado em pedaços pequenos e relevantes
Gera embeddings OpenAI para busca vetorial
"""

from pathlib import Path
import sys
import json
import requests
import re

OPENAI_API_KEY = "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"

def quebrar_semanticamente(documento: str) -> list:
    """
    Quebra documento em chunks semânticos

    Args:
        documento: Texto completo

    Returns:
        Lista de dicts {id, titulo, conteudo}
    """
    chunks = []
    chunk_id = 1

    # Separa por seções (## TÍTULO)
    secoes = re.split(r'\n## ', documento)

    for i, secao in enumerate(secoes):
        if not secao.strip():
            continue

        # Primeira seção pode não ter ##
        if i == 0 and not secao.startswith('#'):
            continue

        # Extrai título
        linhas = secao.split('\n')
        titulo = linhas[0].strip()

        # Remove separadores
        conteudo_linhas = []
        for linha in linhas[1:]:
            if re.match(r'^-+$', linha.strip()) or re.match(r'^=+$', linha.strip()):
                continue
            conteudo_linhas.append(linha)

        conteudo = '\n'.join(conteudo_linhas).strip()

        # Se seção for FAQ, quebra por pergunta
        if 'PERGUNTAS' in titulo.upper() or 'FAQ' in titulo.upper():
            perguntas = re.split(r'\n🔹 ', conteudo)

            for pergunta in perguntas:
                if not pergunta.strip():
                    continue

                # Extrai título da pergunta
                linhas_pergunta = pergunta.split('\n')
                titulo_pergunta = linhas_pergunta[0].strip()
                resposta = '\n'.join(linhas_pergunta[1:]).strip()

                if titulo_pergunta and resposta:
                    chunks.append({
                        'id': f'chunk_{chunk_id:03d}',
                        'titulo': f'FAQ: {titulo_pergunta}',
                        'conteudo': resposta,
                        'secao_pai': titulo,
                        'tokens_estimado': len(resposta.split()) * 1.3  # ~1.3 tokens por palavra
                    })
                    chunk_id += 1

        else:
            # Seções normais - se muito grande, quebra por subtópicos
            if len(conteudo) > 1000:  # ~700 tokens
                # Tenta quebrar por bullets ou subtópicos
                subtopicos = re.split(r'\n\n', conteudo)

                for subtopico in subtopicos:
                    if not subtopico.strip():
                        continue

                    # Gera título do subtópico (primeiras palavras)
                    palavras = subtopico.split()[:5]
                    titulo_sub = ' '.join(palavras) + '...'

                    chunks.append({
                        'id': f'chunk_{chunk_id:03d}',
                        'titulo': f'{titulo} - {titulo_sub}',
                        'conteudo': subtopico.strip(),
                        'secao_pai': titulo,
                        'tokens_estimado': len(subtopico.split()) * 1.3
                    })
                    chunk_id += 1
            else:
                # Seção pequena, mantém inteira
                chunks.append({
                    'id': f'chunk_{chunk_id:03d}',
                    'titulo': titulo,
                    'conteudo': conteudo,
                    'secao_pai': titulo,
                    'tokens_estimado': len(conteudo.split()) * 1.3
                })
                chunk_id += 1

    return chunks

def gerar_embedding(texto: str) -> list:
    """
    Gera embedding usando OpenAI text-embedding-3-small

    Args:
        texto: Texto para gerar embedding

    Returns:
        Lista de floats (vetor)
    """
    url = "https://api.openai.com/v1/embeddings"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "text-embedding-3-small",
        "input": texto
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()

        data = response.json()
        return data["data"][0]["embedding"]

    except Exception as e:
        print(f"❌ Erro ao gerar embedding: {e}")
        return []

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 gerar_chunks_semanticos.py <carro_id>")
        print("Exemplo: python3 gerar_chunks_semanticos.py exemplo-carro-001")
        sys.exit(1)

    carro_id = sys.argv[1]

    carros_dir = Path(__file__).parent.parent / "carros"
    carro_dir = carros_dir / carro_id

    if not carro_dir.exists():
        print(f"❌ Carro '{carro_id}' não encontrado")
        sys.exit(1)

    # Lê documento consolidado
    doc_file = carro_dir / "documento_completo.txt"

    if not doc_file.exists():
        print(f"❌ documento_completo.txt não encontrado. Execute preparar_rag_carros.py primeiro")
        sys.exit(1)

    print(f"📖 Lendo documento de {carro_id}...")
    with open(doc_file, 'r', encoding='utf-8') as f:
        documento = f.read()

    # Quebra semanticamente
    print("\n🧠 Quebrando semanticamente...")
    chunks = quebrar_semanticamente(documento)
    print(f"   ✅ {len(chunks)} chunks criados")

    # Cria diretório chunks
    chunks_dir = carro_dir / "chunks"
    chunks_dir.mkdir(exist_ok=True)

    # Salva chunks e gera embeddings
    print("\n🔢 Gerando embeddings...")
    embeddings_data = []

    for i, chunk in enumerate(chunks, 1):
        # Salva chunk como arquivo
        chunk_file = chunks_dir / f"{chunk['id']}.md"

        with open(chunk_file, 'w', encoding='utf-8') as f:
            f.write(f"# {chunk['titulo']}\n\n")
            f.write(f"**Seção:** {chunk['secao_pai']}\n\n")
            f.write(f"---\n\n")
            f.write(chunk['conteudo'])

        # Gera embedding
        texto_embedding = f"{chunk['titulo']}\n{chunk['conteudo']}"
        embedding = gerar_embedding(texto_embedding)

        if embedding:
            embeddings_data.append({
                'id': chunk['id'],
                'titulo': chunk['titulo'],
                'secao_pai': chunk['secao_pai'],
                'tokens_estimado': chunk['tokens_estimado'],
                'embedding': embedding
            })

            print(f"   ✅ {chunk['id']}: {chunk['titulo'][:50]}... ({int(chunk['tokens_estimado'])} tokens)")

    # Salva embeddings
    embeddings_file = carro_dir / "embeddings.json"
    with open(embeddings_file, 'w', encoding='utf-8') as f:
        json.dump(embeddings_data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Processo concluído!")
    print(f"   📁 Chunks: {chunks_dir}")
    print(f"   🔢 Embeddings: {embeddings_file}")
    print(f"   📊 Total: {len(chunks)} chunks")

    # Gera índice
    print("\n📋 Gerando índice...")
    index_file = carro_dir / "index.md"

    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(f"# {carro_id} - Knowledge Base\n\n")
        f.write(f"Total de chunks: {len(chunks)}\n\n")
        f.write("## Estrutura do Documento\n\n")

        secao_atual = None
        for chunk in chunks:
            if chunk['secao_pai'] != secao_atual:
                secao_atual = chunk['secao_pai']
                f.write(f"\n### {secao_atual}\n\n")

            f.write(f"- **{chunk['id']}**: {chunk['titulo']} (~{int(chunk['tokens_estimado'])} tokens)\n")

    print(f"   ✅ Índice: {index_file}")

    print("\n🎯 Próximo passo: Integrar busca vetorial no chatbot")

if __name__ == "__main__":
    main()
