"""
Componente de Score, Tags e Origem

Sistema completo de qualificação de leads para Chatbot WhatsApp V4
"""
from .sistema_score import SistemaScore
from .sistema_tags import SistemaTags
from .deteccao_origem import DeteccaoOrigem
from .integrador import IntegradorScore

__all__ = [
    "SistemaScore",
    "SistemaTags",
    "DeteccaoOrigem",
    "IntegradorScore"
]
