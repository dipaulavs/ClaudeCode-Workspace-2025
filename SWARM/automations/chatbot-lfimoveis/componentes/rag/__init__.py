#!/usr/bin/env python3
"""
🔍 RAG System - Componentes para busca e resposta inteligente

Componentes:
- IntegradorRAGImoveis: Pipeline completo RAG
- IAEspecialistaImoveis: IA com Progressive Disclosure
- RAGHibridoImoveis: Busca híbrida (keywords + semântico)
- BuscaVetorial: Busca por similaridade semântica
"""

from .integrador_imoveis import IntegradorRAGImoveis
from .ia_especialista_imoveis import IAEspecialistaImoveis
from .busca_hibrida_imoveis import RAGHibridoImoveis
from .busca_vetorial import BuscaVetorial

__all__ = [
    'IntegradorRAGImoveis',
    'IAEspecialistaImoveis',
    'RAGHibridoImoveis',
    'BuscaVetorial'
]
