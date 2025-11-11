"""
Componente de Score, Tags e Origem

Sistema completo de qualificação de leads para Chatbot WhatsApp V4
Com análise IA via Claude
"""
from .sistema_score import SistemaScore
from .sistema_tags import SistemaTags
from .deteccao_origem import DeteccaoOrigem
from .integrador import IntegradorScore
from .analisador_ia import AnalisadorLeadIA

__all__ = [
    "SistemaScore",
    "SistemaTags",
    "DeteccaoOrigem",
    "IntegradorScore",
    "AnalisadorLeadIA"
]
