#!/usr/bin/env python3
"""
🔍 RAG HÍBRIDO - Busca Keywords + Semântico (ADAPTADO PARA IMÓVEIS)

Pipeline:
1. Filtro Keywords: 50 imóveis → 10 candidatos (rápido, zero custo)
2. Ranking Semântico: 10 → TOP 3 (embeddings OpenAI)

Custo: ~$0.0001 por busca
"""

import re
import json
import math
from pathlib import Path
import requests
from typing import List, Dict, Optional


class RAGHibridoImoveis:
    """
    Sistema de busca híbrida para imóveis
    """

    def __init__(self, imoveis_dir: Path, openai_api_key: str):
        """
        Args:
            imoveis_dir: Diretório com dados dos imóveis
            openai_api_key: Chave API OpenAI (para embeddings)
        """
        self.imoveis_dir = imoveis_dir
        self.openai_api_key = openai_api_key
        self.database = self._carregar_database()

    def _carregar_database(self) -> List[Dict]:
        """
        Carrega todos os imóveis do diretório

        Returns:
            Lista de dicts com dados dos imóveis
        """
        imoveis = []

        if not self.imoveis_dir.exists():
            return []

        for imovel_dir in self.imoveis_dir.iterdir():
            if not imovel_dir.is_dir():
                continue

            # Lê arquivo base.txt
            base_file = imovel_dir / "base.txt"

            if not base_file.exists():
                continue

            with open(base_file, 'r', encoding='utf-8') as f:
                conteudo = f.read().strip()

            # Extrai metadados do conteúdo
            imovel = {
                "id": imovel_dir.name,
                "path": str(imovel_dir),
                "conteudo_base": conteudo,
                "tipo": self._extrair_tipo(conteudo),
                "bairro": self._extrair_bairro(conteudo),
                "cidade": self._extrair_cidade(conteudo),
                "quartos": self._extrair_quartos(conteudo),
                "banheiros": self._extrair_banheiros(conteudo),
                "vagas": self._extrair_vagas(conteudo),
                "area": self._extrair_area(conteudo),
                "preco": self._extrair_preco(conteudo),
                "tipo_negocio": self._extrair_tipo_negocio(conteudo)
            }

            imoveis.append(imovel)

        return imoveis

    def _extrair_tipo(self, texto: str) -> Optional[str]:
        """Extrai tipo do imóvel"""
        texto_lower = texto.lower()

        # Lista de tipos comuns
        tipos = [
            "casa", "apartamento", "apto", "cobertura", "kitnet", "quitinete",
            "studio", "sobrado", "chácara", "sítio", "sitio", "fazenda",
            "terreno", "lote", "galpão", "galpao", "sala comercial", "loja",
            "prédio", "predio"
        ]

        for tipo in tipos:
            if tipo in texto_lower:
                # Normaliza nomes
                if tipo in ["apto"]:
                    return "apartamento"
                if tipo in ["quitinete"]:
                    return "kitnet"
                if tipo in ["sitio"]:
                    return "sítio"
                if tipo in ["galpao"]:
                    return "galpão"
                if tipo in ["predio"]:
                    return "prédio"
                return tipo

        return None

    def _extrair_bairro(self, texto: str) -> Optional[str]:
        """Extrai bairro do imóvel"""
        # Padrões: "Bairro: Centro", "no Centro", "em Centro"
        match = re.search(r'(?:bairro[:\s]+|no\s+bairro\s+|em\s+)([A-ZÀ-Ú][a-zà-ú\s]+?)(?:\s*[-,\.\n]|$)', texto)
        if match:
            return match.group(1).strip()

        return None

    def _extrair_cidade(self, texto: str) -> Optional[str]:
        """Extrai cidade do imóvel"""
        # Padrões: "Cidade: Poços de Caldas", "em Poços de Caldas"
        match = re.search(r'(?:cidade[:\s]+|em\s+)([A-ZÀ-Ú][a-zà-ú\s]+?)(?:\s*[-,\.\n]|$)', texto)
        if match:
            return match.group(1).strip()

        return None

    def _extrair_quartos(self, texto: str) -> Optional[int]:
        """Extrai número de quartos"""
        # Padrões: "3 quartos", "3 qts", "3Q"
        match = re.search(r'(\d+)\s*(?:quartos?|qts?|q\b)', texto.lower())
        if match:
            return int(match.group(1))

        return None

    def _extrair_banheiros(self, texto: str) -> Optional[int]:
        """Extrai número de banheiros"""
        # Padrões: "2 banheiros", "2 bwc"
        match = re.search(r'(\d+)\s*(?:banheiros?|bwc|wc)', texto.lower())
        if match:
            return int(match.group(1))

        return None

    def _extrair_vagas(self, texto: str) -> Optional[int]:
        """Extrai número de vagas"""
        # Padrões: "2 vagas", "2 garagens"
        match = re.search(r'(\d+)\s*(?:vagas?|garagens?)', texto.lower())
        if match:
            return int(match.group(1))

        return None

    def _extrair_area(self, texto: str) -> Optional[float]:
        """Extrai área em m²"""
        # Padrões: "120m²", "120 m2", "120m2"
        match = re.search(r'(\d+(?:[\.,]\d+)?)\s*m[²2]', texto.lower())
        if match:
            area_str = match.group(1).replace(',', '.')
            return float(area_str)

        return None

    def _extrair_preco(self, texto: str) -> Optional[int]:
        """Extrai preço"""
        # Padrões: "R$ 450.000", "R$450000", "450.000,00"
        match = re.search(r'R\$\s*(\d+(?:\.\d{3})*(?:,\d{2})?)', texto)
        if match:
            preco_str = match.group(1).replace('.', '').replace(',', '.')
            return int(float(preco_str))

        return None

    def _extrair_tipo_negocio(self, texto: str) -> Optional[str]:
        """Extrai tipo de negócio (venda/aluguel)"""
        texto_lower = texto.lower()

        if any(palavra in texto_lower for palavra in ["venda", "vende-se", "à venda", "a venda"]):
            return "venda"
        elif any(palavra in texto_lower for palavra in ["aluguel", "aluga-se", "locação", "locacao"]):
            return "aluguel"

        return None

    def filtrar_keywords(self, mensagem: str) -> List[Dict]:
        """
        Filtro rápido por keywords (zero custo)

        Args:
            mensagem: Mensagem do cliente

        Returns:
            Lista de candidatos (máx 10)
        """
        # Extrai filtros da mensagem
        tipo_buscado = self._extrair_tipo(mensagem)
        bairro_buscado = self._extrair_bairro(mensagem)
        cidade_buscada = self._extrair_cidade(mensagem)
        quartos_buscados = self._extrair_quartos(mensagem)
        preco_max = self._extrair_preco_maximo(mensagem)
        tipo_negocio_buscado = self._extrair_tipo_negocio(mensagem)

        # Calcula score para cada imóvel
        candidatos = []

        for imovel in self.database:
            score = 0

            # Tipo (peso 30)
            if tipo_buscado and imovel["tipo"] == tipo_buscado:
                score += 30

            # Bairro (peso 25)
            if bairro_buscado and imovel["bairro"]:
                if bairro_buscado.lower() in imovel["bairro"].lower():
                    score += 25

            # Cidade (peso 20)
            if cidade_buscada and imovel["cidade"]:
                if cidade_buscada.lower() in imovel["cidade"].lower():
                    score += 20

            # Quartos (peso 15)
            if quartos_buscados and imovel["quartos"]:
                diff_quartos = abs(imovel["quartos"] - quartos_buscados)
                if diff_quartos == 0:
                    score += 15
                elif diff_quartos == 1:
                    score += 8

            # Preço (peso 25)
            if preco_max and imovel["preco"]:
                if imovel["preco"] <= preco_max:
                    score += 25
                    # Bonus se for bem abaixo do orçamento
                    if imovel["preco"] <= preco_max * 0.8:
                        score += 5

            # Tipo de negócio (peso 15)
            if tipo_negocio_buscado and imovel["tipo_negocio"] == tipo_negocio_buscado:
                score += 15

            # Threshold mínimo
            if score >= 20 or len(self.database) <= 3:  # Se tem poucos imóveis, inclui todos
                candidatos.append({
                    "score": score,
                    "imovel": imovel
                })

        # Ordena por score
        candidatos.sort(key=lambda x: x["score"], reverse=True)

        # Retorna top 10
        return [c["imovel"] for c in candidatos[:10]]

    def _extrair_preco_maximo(self, mensagem: str) -> Optional[int]:
        """Extrai preço máximo da mensagem"""
        msg_lower = mensagem.lower()

        # Padrões: "até 500000", "máximo 500 mil", "até R$ 500.000"
        match = re.search(r'(?:até|max|máximo|maximo)\s*(?:r\$\s*)?(\d+(?:\.\d{3})*)', msg_lower)
        if match:
            preco_str = match.group(1).replace('.', '')
            return int(preco_str)

        # Padrão: "R$ 500000"
        match = re.search(r'r\$\s*(\d+(?:\.\d{3})*)', msg_lower)
        if match:
            preco_str = match.group(1).replace('.', '')
            return int(preco_str)

        return None

    def ranking_semantico(self, mensagem: str, candidatos: List[Dict]) -> List[Dict]:
        """
        Ranking semântico usando embeddings OpenAI

        Args:
            mensagem: Mensagem do cliente
            candidatos: Lista de candidatos do filtro keywords

        Returns:
            TOP 3 candidatos ranqueados
        """
        if len(candidatos) <= 3:
            return candidatos

        # Gera embedding da mensagem
        embedding_msg = self._gerar_embedding(mensagem)

        # Calcula similaridade para cada candidato
        resultados = []

        for imovel in candidatos:
            # Gera embedding do conteúdo base
            embedding_imovel = self._gerar_embedding(imovel["conteudo_base"])

            # Calcula similaridade cosseno
            similaridade = self._cosine_similarity(embedding_msg, embedding_imovel)

            resultados.append({
                "similaridade": similaridade,
                "imovel": imovel
            })

        # Ordena por similaridade
        resultados.sort(key=lambda x: x["similaridade"], reverse=True)

        # Retorna top 3
        return [r["imovel"] for r in resultados[:3]]

    def _gerar_embedding(self, texto: str) -> List[float]:
        """
        Gera embedding usando OpenAI text-embedding-3-small

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
            return [0.0] * 1536  # Retorna vetor zero em caso de erro

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

    def buscar(self, mensagem: str) -> List[Dict]:
        """
        Busca híbrida completa: keywords → semântico

        Args:
            mensagem: Mensagem do cliente

        Returns:
            TOP 3 imóveis mais relevantes
        """
        print(f"🔍 RAG Híbrido Imóveis: Iniciando busca...", flush=True)
        print(f"   Database: {len(self.database)} imóveis", flush=True)

        # PASSO 1: Filtro keywords
        candidatos = self.filtrar_keywords(mensagem)
        print(f"   Filtro keywords: {len(candidatos)} candidatos", flush=True)

        if len(candidatos) == 0:
            print(f"   ⚠️  Nenhum candidato encontrado", flush=True)
            return []

        # PASSO 2: Ranking semântico (se necessário)
        if len(candidatos) > 3:
            top_3 = self.ranking_semantico(mensagem, candidatos)
            print(f"   Ranking semântico: TOP 3 selecionados", flush=True)
        else:
            top_3 = candidatos
            print(f"   Ranking semântico: Não necessário ({len(candidatos)} <= 3)", flush=True)

        print(f"✅ RAG Híbrido Imóveis: {len(top_3)} imóveis retornados", flush=True)
        return top_3
