"""
Sistema de Follow-ups Anti-Abandono

Recupera leads que abandonaram a conversa através de follow-ups estratégicos.

Componentes:
- SistemaFollowUp: Gerenciamento de agendamento e envio
- DetectorAbandono: Detecta tipo de abandono para personalizar follow-up
- IntegradorFollowUp: Integração com chatbot V4
"""

from .sistema_followup import SistemaFollowUp
from .tipos_abandono import DetectorAbandono
from .integrador import IntegradorFollowUp

__all__ = ['SistemaFollowUp', 'DetectorAbandono', 'IntegradorFollowUp']
