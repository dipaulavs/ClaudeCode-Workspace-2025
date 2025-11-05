#!/usr/bin/env python3
"""
🔍 RAG HÍBRIDO - Busca Keywords + Semântico (ADAPTADO PARA CARROS)

Pipeline:
1. Filtro Keywords: 50 carros → 10 candidatos (rápido, zero custo)
2. Ranking Semântico: 10 → TOP 3 (embeddings OpenAI)

Custo: ~$0.0001 por busca
"""

import re
import json
import math
from pathlib import Path
import requests
from typing import List, Dict, Optional


class RAGHibridoCarros:
    """
    Sistema de busca híbrida para carros seminovos
    """

    def __init__(self, carros_dir: Path, openai_api_key: str):
        """
        Args:
            carros_dir: Diretório com dados dos carros
            openai_api_key: Chave API OpenAI (para embeddings)
        """
        self.carros_dir = carros_dir
        self.openai_api_key = openai_api_key
        self.database = self._carregar_database()

    def _carregar_database(self) -> List[Dict]:
        """
        Carrega todos os carros do diretório

        Returns:
            Lista de dicts com dados dos carros
        """
        carros = []

        if not self.carros_dir.exists():
            return []

        for carro_dir in self.carros_dir.iterdir():
            if not carro_dir.is_dir():
                continue

            # Lê arquivo base.txt
            base_file = carro_dir / "base.txt"

            if not base_file.exists():
                continue

            with open(base_file, 'r', encoding='utf-8') as f:
                conteudo = f.read().strip()

            # Extrai metadados do conteúdo
            carro = {
                "id": carro_dir.name,
                "path": str(carro_dir),
                "conteudo_base": conteudo,
                "marca": self._extrair_marca(conteudo),
                "modelo": self._extrair_modelo(conteudo),
                "ano": self._extrair_ano(conteudo),
                "km": self._extrair_km(conteudo),
                "preco": self._extrair_preco(conteudo),
                "combustivel": self._extrair_combustivel(conteudo),
                "cambio": self._extrair_cambio(conteudo)
            }

            carros.append(carro)

        return carros

    def _extrair_marca(self, texto: str) -> Optional[str]:
        """Extrai marca do carro"""
        texto_lower = texto.lower()

        # Lista de marcas comuns
        marcas = [
            "volkswagen", "vw", "fiat", "chevrolet", "ford", "honda", "toyota",
            "hyundai", "nissan", "renault", "peugeot", "citroën", "citroen",
            "jeep", "mercedes", "bmw", "audi", "volvo", "land rover",
            "mitsubishi", "kia", "suzuki", "caoa chery", "chery"
        ]

        for marca in marcas:
            if marca in texto_lower:
                # Normaliza nomes
                if marca in ["vw"]:
                    return "volkswagen"
                if marca in ["citroen"]:
                    return "citroën"
                if marca in ["chery"]:
                    return "caoa chery"
                return marca

        return None

    def _extrair_modelo(self, texto: str) -> Optional[str]:
        """Extrai modelo do carro"""
        # Padrão: primeira linha geralmente tem marca + modelo
        primeira_linha = texto.split('\n')[0].lower()

        # Remove emojis e caracteres especiais
        primeira_linha = re.sub(r'[^\w\s.-]', '', primeira_linha)

        # Remove marca conhecida da linha
        marca = self._extrair_marca(texto)
        if marca:
            primeira_linha = primeira_linha.replace(marca, '')

        # Remove números (ano, versão)
        palavras = primeira_linha.split()
        palavras_modelo = []

        for palavra in palavras:
            # Ignora números puros e versões (1.0, 2.0, etc)
            if not re.match(r'^\d', palavra):
                palavras_modelo.append(palavra)

        if palavras_modelo:
            # Pega até 2 primeiras palavras (ex: "gol 1.0" → "gol")
            return ' '.join(palavras_modelo[:2]).strip()

        return None

    def _extrair_ano(self, texto: str) -> Optional[int]:
        """Extrai ano do carro"""
        # Padrões: "2020", "Ano: 2020"
        match = re.search(r'\b(20\d{2})\b', texto)
        if match:
            ano = int(match.group(1))
            # Valida (entre 2000 e 2025)
            if 2000 <= ano <= 2025:
                return ano

        return None

    def _extrair_km(self, texto: str) -> Optional[int]:
        """Extrai kilometragem"""
        # Padrões: "35.000 km", "35000km", "35 mil km"
        match = re.search(r'(\d+(?:\.\d{3})*)\s*(?:km|mil\s*km|quilômetros)', texto.lower())
        if match:
            km_str = match.group(1).replace('.', '')
            return int(km_str)

        return None

    def _extrair_preco(self, texto: str) -> Optional[int]:
        """Extrai preço"""
        # Padrões: "R$ 45.000", "R$45000", "45.000,00"
        match = re.search(r'R\$\s*(\d+(?:\.\d{3})*(?:,\d{2})?)', texto)
        if match:
            preco_str = match.group(1).replace('.', '').replace(',', '.')
            return int(float(preco_str))

        return None

    def _extrair_combustivel(self, texto: str) -> Optional[str]:
        """Extrai tipo de combustível"""
        texto_lower = texto.lower()

        if "flex" in texto_lower:
            return "flex"
        elif "gasolina" in texto_lower:
            return "gasolina"
        elif any(palavra in texto_lower for palavra in ["diesel", "óleo diesel"]):
            return "diesel"
        elif any(palavra in texto_lower for palavra in ["elétrico", "eletrico", "híbrido", "hibrido"]):
            return "híbrido/elétrico"

        return None

    def _extrair_cambio(self, texto: str) -> Optional[str]:
        """Extrai tipo de câmbio"""
        texto_lower = texto.lower()

        if any(palavra in texto_lower for palavra in ["automático", "automatico", "cvt", "dct"]):
            return "automático"
        elif "manual" in texto_lower:
            return "manual"

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
        marca_buscada = self._extrair_marca(mensagem)
        modelo_buscado = self._extrair_modelo(mensagem)
        ano_buscado = self._extrair_ano(mensagem)
        km_max = self._extrair_km_maximo(mensagem)
        preco_max = self._extrair_preco_maximo(mensagem)
        combustivel_buscado = self._extrair_combustivel(mensagem)
        cambio_buscado = self._extrair_cambio(mensagem)

        # Calcula score para cada carro
        candidatos = []

        for carro in self.database:
            score = 0

            # Marca (peso 30)
            if marca_buscada and carro["marca"] == marca_buscada:
                score += 30

            # Modelo (peso 25)
            if modelo_buscado and carro["modelo"]:
                # Match parcial (ex: "gol" em "gol 1.0")
                if modelo_buscado.lower() in carro["modelo"].lower():
                    score += 25

            # Ano (peso 20)
            if ano_buscado and carro["ano"]:
                # Prefere ano exato, mas aceita próximos
                diff_ano = abs(carro["ano"] - ano_buscado)
                if diff_ano == 0:
                    score += 20
                elif diff_ano <= 2:
                    score += 10

            # KM (peso 15)
            if km_max and carro["km"]:
                if carro["km"] <= km_max:
                    score += 15
                    # Bonus se for bem abaixo
                    if carro["km"] <= km_max * 0.7:
                        score += 5

            # Preço (peso 20)
            if preco_max and carro["preco"]:
                if carro["preco"] <= preco_max:
                    score += 20
                    # Bonus se for bem abaixo do orçamento
                    if carro["preco"] <= preco_max * 0.8:
                        score += 5

            # Combustível (peso 10)
            if combustivel_buscado and carro["combustivel"] == combustivel_buscado:
                score += 10

            # Câmbio (peso 10)
            if cambio_buscado and carro["cambio"] == cambio_buscado:
                score += 10

            # Threshold mínimo
            if score >= 20 or len(self.database) <= 3:  # Se tem poucos carros, inclui todos
                candidatos.append({
                    "score": score,
                    "carro": carro
                })

        # Ordena por score
        candidatos.sort(key=lambda x: x["score"], reverse=True)

        # Retorna top 10
        return [c["carro"] for c in candidatos[:10]]

    def _extrair_km_maximo(self, mensagem: str) -> Optional[int]:
        """Extrai kilometragem máxima da mensagem"""
        msg_lower = mensagem.lower()

        # Padrões: "até 50000 km", "máximo 50 mil km"
        match = re.search(r'(?:até|max|máximo|maximo)\s*(\d+(?:\.\d{3})*)\s*(?:km|mil)', msg_lower)
        if match:
            km_str = match.group(1).replace('.', '')
            return int(km_str)

        return None

    def _extrair_preco_maximo(self, mensagem: str) -> Optional[int]:
        """Extrai preço máximo da mensagem"""
        msg_lower = mensagem.lower()

        # Padrões: "até 50000", "máximo 50 mil", "até R$ 50.000"
        match = re.search(r'(?:até|max|máximo|maximo)\s*(?:r\$\s*)?(\d+(?:\.\d{3})*)', msg_lower)
        if match:
            preco_str = match.group(1).replace('.', '')
            return int(preco_str)

        # Padrão: "R$ 50000"
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

        for carro in candidatos:
            # Gera embedding do conteúdo base
            embedding_carro = self._gerar_embedding(carro["conteudo_base"])

            # Calcula similaridade cosseno
            similaridade = self._cosine_similarity(embedding_msg, embedding_carro)

            resultados.append({
                "similaridade": similaridade,
                "carro": carro
            })

        # Ordena por similaridade
        resultados.sort(key=lambda x: x["similaridade"], reverse=True)

        # Retorna top 3
        return [r["carro"] for r in resultados[:3]]

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
            TOP 3 carros mais relevantes
        """
        print(f"🔍 RAG Híbrido Carros: Iniciando busca...", flush=True)
        print(f"   Database: {len(self.database)} carros", flush=True)

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

        print(f"✅ RAG Híbrido Carros: {len(top_3)} carros retornados", flush=True)
        return top_3


if __name__ == "__main__":
    # Teste standalone
    print("🧪 Testando RAG Híbrido Carros...")

    from pathlib import Path

    carros_dir = Path(__file__).parent.parent.parent / "carros"
    openai_key = "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"

    rag = RAGHibridoCarros(carros_dir, openai_key)

    mensagem = "Volkswagen Gol 2020 até 50 mil"
    resultados = rag.buscar(mensagem)

    print(f"\n📋 Resultados ({len(resultados)}):")
    for i, carro in enumerate(resultados, 1):
        print(f"{i}. {carro['id']} - {carro['marca']} {carro['modelo']} {carro['ano']} - R$ {carro['preco']}")
