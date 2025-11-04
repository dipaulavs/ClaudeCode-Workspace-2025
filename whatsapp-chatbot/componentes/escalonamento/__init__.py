"""
Componente de Escalonamento Inteligente
Sistema completo: detecção → atribuição → notificação → agendamento
"""

from componentes.escalonamento.triggers import DetectorEscalonamento
from componentes.escalonamento.consulta_agenda import ConsultaAgenda
from componentes.escalonamento.chatwoot_integration import ChatwootEscalonamento
from componentes.escalonamento.notificacao import NotificadorCorretor
from componentes.escalonamento.integrador import IntegradorEscalonamento

__all__ = [
    'DetectorEscalonamento',
    'ConsultaAgenda',
    'ChatwootEscalonamento',
    'NotificadorCorretor',
    'IntegradorEscalonamento'
]
