#!/usr/bin/env python3
"""
🔍 Busca Vetorial Semântica

Substitui Progressive Disclosure por busca vetorial nos chunks
Muito mais preciso e econômico
"""

import json
import math
from pathlib import Path
import requests
from typing import List, Dict, Optional


class BuscaVetorial:
    """
    Sistema de busca vetorial para chunks semânticos
    """

    def __init__(self, carros_dir: Path, openai_api_key: str):
        """
        Args:
            carros_dir: Diretório com carros
            openai_api_key: Chave API OpenAI
        """
        self.carros_dir = carros_dir
        self.openai_api_key = openai_api_key
        self.embeddings_cache = {}  # {carro_id: embeddings_data}

    def _carregar_embeddings(self, carro_id: str) -> Optional[List[Dict]]:
        """
        Carrega embeddings de um carro

        Args:
            carro_id: ID do carro

        Returns:
            Lista de chunks com embeddings ou None
        """
        # Cache
        if carro_id in self.embeddings_cache:
            return self.embeddings_cache[carro_id]

        # Carrega do arquivo
        carro_path = self.carros_dir / carro_id
        embeddings_file = carro_path / "embeddings.json"

        if not embeddings_file.exists():
            print(f"⚠️  Embeddings não encontrados para {carro_id}", flush=True)
            print(f"   Execute: python3 scripts/gerar_chunks_semanticos.py {carro_id}", flush=True)
            return None

        try:
            with open(embeddings_file, 'r', encoding='utf-8') as f:
                embeddings_data = json.load(f)

            self.embeddings_cache[carro_id] = embeddings_data
            return embeddings_data

        except Exception as e:
            print(f"❌ Erro ao carregar embeddings: {e}", flush=True)
            return None

    def _gerar_embedding(self, texto: str) -> List[float]:
        """
        Gera embedding da query

        Args:
            texto: Texto para gerar embedding

        Returns:
            Lista de floats (vetor)
        """
        url = "https://api.openai.com/v1/embeddings"

        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
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
            print(f"❌ Erro ao gerar embedding: {e}", flush=True)
            return []

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calcula similaridade cosseno entre dois vetores

        Args:
            vec1: Primeiro vetor
            vec2: Segundo vetor

        Returns:
            Similaridade (0-1)
        """
        # Produto escalar
        dot_product = sum(a * b for a, b in zip(vec1, vec2))

        # Magnitudes
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(b * b for b in vec2))

        # Evita divisão por zero
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        return dot_product / (magnitude1 * magnitude2)

    def buscar(
        self,
        carro_id: str,
        mensagem: str,
        top_k: int = 3
    ) -> Dict:
        """
        Busca chunks mais relevantes para a mensagem

        Args:
            carro_id: ID do carro
            mensagem: Mensagem do cliente
            top_k: Quantos chunks retornar

        Returns:
            Dict com:
                - chunks: Lista dos top_k chunks mais relevantes
                - tokens_total: Total estimado de tokens
                - item_id: ID do carro
        """
        print(f"\n🔍 Busca Vetorial: {carro_id}", flush=True)
        print(f"   Query: {mensagem[:50]}...", flush=True)

        # Carrega embeddings do carro
        embeddings_data = self._carregar_embeddings(carro_id)

        if not embeddings_data:
            return {
                "erro": f"Embeddings não encontrados para {carro_id}",
                "chunks": [],
                "tokens_total": 0,
                "item_id": carro_id
            }

        # Gera embedding da mensagem
        embedding_query = self._gerar_embedding(mensagem)

        if not embedding_query:
            return {
                "erro": "Erro ao gerar embedding da query",
                "chunks": [],
                "tokens_total": 0,
                "item_id": carro_id
            }

        # Calcula similaridade com cada chunk
        resultados = []

        for chunk_data in embeddings_data:
            embedding_chunk = chunk_data['embedding']
            similaridade = self._cosine_similarity(embedding_query, embedding_chunk)

            resultados.append({
                'chunk_id': chunk_data['id'],
                'titulo': chunk_data['titulo'],
                'secao_pai': chunk_data['secao_pai'],
                'tokens_estimado': chunk_data['tokens_estimado'],
                'similaridade': similaridade
            })

        # Ordena por similaridade
        resultados.sort(key=lambda x: x['similaridade'], reverse=True)

        # Pega top_k
        top_chunks = resultados[:top_k]

        # Carrega conteúdo dos chunks selecionados
        chunks_completos = []
        tokens_total = 0
        carro_path = self.carros_dir / carro_id

        for chunk in top_chunks:
            chunk_file = carro_path / "chunks" / f"{chunk['chunk_id']}.md"

            if chunk_file.exists():
                with open(chunk_file, 'r', encoding='utf-8') as f:
                    conteudo = f.read()

                chunks_completos.append({
                    'chunk_id': chunk['chunk_id'],
                    'titulo': chunk['titulo'],
                    'secao_pai': chunk['secao_pai'],
                    'conteudo': conteudo,
                    'similaridade': chunk['similaridade'],
                    'tokens_estimado': chunk['tokens_estimado']
                })

                tokens_total += chunk['tokens_estimado']

                print(f"   ✅ {chunk['chunk_id']}: {chunk['titulo'][:40]}... (sim: {chunk['similaridade']:.3f})", flush=True)

        print(f"   💾 Total: {tokens_total:.0f} tokens", flush=True)

        return {
            "chunks": chunks_completos,
            "tokens_total": tokens_total,
            "item_id": carro_id
        }

    def formatar_para_prompt(self, resultado_busca: Dict) -> str:
        """
        Formata resultado da busca para incluir no prompt

        Args:
            resultado_busca: Dict retornado por buscar()

        Returns:
            String formatada para o prompt
        """
        if "erro" in resultado_busca:
            return f"❌ {resultado_busca['erro']}"

        chunks = resultado_busca.get("chunks", [])

        if not chunks:
            return "⚠️ Nenhuma informação relevante encontrada."

        # Monta texto formatado
        texto = ""

        for chunk in chunks:
            texto += f"## {chunk['titulo']}\n\n"
            texto += chunk['conteudo'] + "\n\n"
            texto += "---\n\n"

        # Adiciona rodapé
        tokens = resultado_busca.get("tokens_total", 0)
        rodape = f"\n_Chunks retornados: {len(chunks)} | ~{tokens:.0f} tokens_\n"

        return texto + rodape


if __name__ == "__main__":
    # Teste standalone
    print("🧪 Testando Busca Vetorial...")

    from pathlib import Path

    carros_dir = Path(__file__).parent.parent.parent / "carros"
    openai_key = "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"

    busca = BuscaVetorial(carros_dir, openai_key)

    # Teste 1: Pergunta sobre garantia
    print("\n📋 Teste 1: Pergunta sobre garantia")
    print("-" * 50)

    resultado = busca.buscar("exemplo-carro-001", "Tem garantia?", top_k=2)

    if resultado['chunks']:
        print(f"\n✅ {len(resultado['chunks'])} chunks encontrados")
        print(f"💾 {resultado['tokens_total']:.0f} tokens")

        print("\n📝 Formatado para prompt:")
        print("-" * 50)
        texto = busca.formatar_para_prompt(resultado)
        print(texto[:500] + "..." if len(texto) > 500 else texto)
