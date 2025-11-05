"""
🎯 COMPONENTES RAG - Sistema RAG + Progressive Disclosure

Exporta:
- RAGHibrido: Busca híbrida (keywords + semântico)
- ProgressiveDisclosure: Carregamento progressivo
- IAEspecialista: IA com contexto limitado
- IntegradorRAG: Orquestrador completo
"""

from .busca_hibrida import RAGHibrido
from .progressive_disclosure import ProgressiveDisclosure
from .ia_especialista import IAEspecialista
from .integrador import IntegradorRAG

__all__ = [
    "RAGHibrido",
    "ProgressiveDisclosure",
    "IAEspecialista",
    "IntegradorRAG"
]
