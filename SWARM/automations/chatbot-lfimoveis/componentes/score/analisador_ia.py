"""
AnalisadorLeadIA - Análise de leads com Claude IA

Usa Claude para extrair automaticamente:
- Sentimento (positivo, neutro, negativo)
- Intenção (compra, pesquisa, dúvida)
- Urgência (alta, média, baixa)
- Score inteligente (0-100)

Com fallback seguro para palavras-chave se IA falhar.
"""
import json
import os
from typing import Dict, Any, Optional
import anthropic

class AnalisadorLeadIA:
    """
    Analisa leads usando Claude IA

    Extrai automaticamente sentimento, intenção e urgência
    Calcula score inteligente baseado em múltiplos fatores
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa analisador IA

        Args:
            api_key: Chave da API Anthropic (default: env ANTHROPIC_API_KEY)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY não configurada")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20241022"

        # Keywords fallback (se IA falhar)
        self.keywords_score = {
            "compra": 20,
            "interesse": 15,
            "imovel": 10,
            "agendar": 25,
            "visita": 20,
            "foto": 10,
            "valor": 15,
            "preco": 15,
            "urgente": 25,
            "logo": 20,
            "hoje": 15,
            "agora": 15,
            "gostei": 15,
            "legal": 10,
            "perfeito": 15,
            "nao": -10,
            "chato": -15,
            "ruin": -10,
            "caro": -5
        }

    def analisar(self, mensagem: str, contexto: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analisa mensagem com IA

        Args:
            mensagem: Texto da mensagem do cliente
            contexto: Contexto opcional (histórico, estado, etc)

        Returns:
            Dict com análise: {
                "sentimento": "positivo|neutro|negativo",
                "intenção": "compra|pesquisa|dúvida|suporte",
                "urgência": "alta|média|baixa",
                "score": 0-100,
                "confianca": 0-1,
                "razao": "string explicando decisão",
                "tags_sugeridas": ["tag1", "tag2"],
                "ia_usado": True|False
            }
        """
        try:
            # Preparar prompt com contexto
            contexto_str = ""
            if contexto:
                contexto_str = f"""
Contexto do cliente:
- Score atual: {contexto.get('score_atual', 0)}
- Histórico de interesse: {contexto.get('tem_interesse', False)}
- Já pediu fotos: {contexto.get('pediu_fotos', False)}
- Mencionou prazo: {contexto.get('mencionou_prazo', False)}
"""

            prompt = f"""
Você é um especialista em qualificação de leads imobiliários.
Analise a mensagem do cliente e retorne um JSON com análise inteligente.

{contexto_str}

MENSAGEM DO CLIENTE:
"{mensagem}"

Responda EXATAMENTE neste formato JSON (sem markdown, sem explicação):
{{
    "sentimento": "positivo|neutro|negativo",
    "intenção": "compra|pesquisa|dúvida|suporte",
    "urgência": "alta|média|baixa",
    "score": 0-100,
    "razao": "explicação breve da análise",
    "tags_sugeridas": ["tag1", "tag2"]
}}

Critérios de pontuação:
- 80-100: Cliente com intenção clara de compra, urgência alta
- 60-79: Cliente interessado, quer informações, urgência média
- 40-59: Cliente explorando opções, interesse básico
- 20-39: Cliente com dúvidas, interesse baixo
- 0-19: Cliente apenas pesquisando ou sem interesse

Analise menções de:
- Agendar visita / compra iminente → urgência ALTA, score +30
- Pedido de fotos / valores → intenção COMPRA, score +20
- Perguntas sobre características → intenção PESQUISA, score +10
- Elogios / emoções positivas → sentimento POSITIVO, score +15
- Reclamações / críticas → sentimento NEGATIVO, score -15
"""

            # Chamar Claude
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extrair resposta
            resposta_texto = response.content[0].text.strip()

            # Tentar parsear JSON
            analise = json.loads(resposta_texto)

            # Validar e completar
            resultado = {
                "sentimento": analise.get("sentimento", "neutro"),
                "intenção": analise.get("intenção", "pesquisa"),
                "urgência": analise.get("urgência", "baixa"),
                "score": int(analise.get("score", 30)),
                "confianca": 0.95,
                "razao": analise.get("razao", "Análise IA"),
                "tags_sugeridas": analise.get("tags_sugeridas", []),
                "ia_usado": True
            }

            # Garantir score válido
            resultado["score"] = max(0, min(100, resultado["score"]))

            return resultado

        except json.JSONDecodeError as e:
            print(f"⚠️ Erro ao parsear JSON da IA: {e}")
            return self._analisar_fallback(mensagem, contexto)
        except anthropic.APIError as e:
            print(f"⚠️ Erro na API Claude: {e}")
            return self._analisar_fallback(mensagem, contexto)
        except Exception as e:
            print(f"⚠️ Erro geral na análise IA: {e}")
            return self._analisar_fallback(mensagem, contexto)

    def _analisar_fallback(self, mensagem: str, contexto: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Fallback para análise por palavras-chave

        Args:
            mensagem: Texto da mensagem
            contexto: Contexto opcional

        Returns:
            Dict com análise fallback
        """
        mensagem_lower = mensagem.lower()

        # Calcular score por palavras-chave
        score = 30  # Score base

        for palavra, valor in self.keywords_score.items():
            if palavra in mensagem_lower:
                score += valor

        # Detectar sentimento
        sentimento = "neutro"
        if any(p in mensagem_lower for p in ["gostei", "legal", "perfeito", "adorei", "excelente", "ótimo"]):
            sentimento = "positivo"
            score += 10
        elif any(p in mensagem_lower for p in ["não gostei", "ruim", "chato", "caro", "decepcionado"]):
            sentimento = "negativo"
            score -= 10

        # Detectar intenção
        intenção = "pesquisa"
        if any(p in mensagem_lower for p in ["compro", "compra", "vou comprar", "estou comprando"]):
            intenção = "compra"
            score += 20
        elif any(p in mensagem_lower for p in ["dúvida", "como", "qual", "por que", "quando"]):
            intenção = "dúvida"
        elif any(p in mensagem_lower for p in ["agendar", "visita", "marcar", "horário"]):
            intenção = "compra"
            score += 15

        # Detectar urgência
        urgência = "baixa"
        if any(p in mensagem_lower for p in ["urgente", "logo", "hoje", "agora", "rápido"]):
            urgência = "alta"
            score += 15
        elif any(p in mensagem_lower for p in ["próximo", "semana", "mês"]):
            urgência = "média"
            score += 5

        # Garantir range válido
        score = max(0, min(100, score))

        return {
            "sentimento": sentimento,
            "intenção": intenção,
            "urgência": urgência,
            "score": score,
            "confianca": 0.6,  # Confiança menor (fallback)
            "razao": "Análise por palavras-chave (IA indisponível)",
            "tags_sugeridas": [],
            "ia_usado": False
        }

    def extrair_tags_contexto(self, analise: Dict[str, Any]) -> list:
        """
        Extrai tags sugeridas baseado na análise

        Args:
            analise: Resultado da análise

        Returns:
            Lista de tags
        """
        tags = analise.get("tags_sugeridas", [])

        # Adicionar tags baseadas em intenção/sentimento
        if analise.get("intenção") == "compra":
            if "interessado_compra" not in tags:
                tags.append("interessado_compra")

        if analise.get("sentimento") == "positivo":
            if "atitude_positiva" not in tags:
                tags.append("atitude_positiva")

        if analise.get("urgência") == "alta":
            if "lead_quente" not in tags:
                tags.append("lead_quente")

        return list(set(tags))  # Remove duplicatas
