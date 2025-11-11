"""
Análise de Leads com IA (Grok-4-fast via OpenRouter)
Substitui sistema burro de palavras-chave por análise de sentimento inteligente
"""
import json
import time
import redis
import requests
from typing import Dict, List, Optional, Any


class AnalisadorLeadIA:
    """
    Analisador de leads usando Grok-4-fast (X.AI)

    Retorna:
    - Sentimento (0-100)
    - Intenção de compra (0-100)
    - Urgência (0-100)
    - Objeções identificadas
    - Score final (0-150)
    - Classificação QUENTE/MORNO/FRIO
    - Tags inteligentes
    """

    PROMPT_ANALISE = """Você é um especialista em análise de leads imobiliários.

MENSAGEM DO CLIENTE:
"{mensagem}"

HISTÓRICO (últimas mensagens):
{contexto}

ANALISE e retorne APENAS um JSON válido (sem markdown, sem explicações):
{{
  "sentimento": 0-100,
  "intencao_compra": 0-100,
  "urgencia": 0-100,
  "objecoes": ["lista de objeções identificadas"],
  "score_final": 0-150,
  "classificacao": "QUENTE ou MORNO ou FRIO",
  "tags": ["lista de tags"],
  "justificativa": "explicação curta"
}}

CRITÉRIOS DE PONTUAÇÃO:

SENTIMENTO (0-100):
- 80-100: Muito positivo, animado, empolgado
- 60-79: Positivo, interessado
- 40-59: Neutro, informativo
- 20-39: Negativo, desinteressado
- 0-19: Muito negativo, irritado

INTENÇÃO DE COMPRA (0-100):
- 80-100: Quer agendar visita, fechar negócio, fazer proposta
- 60-79: Muito interessado, pedindo detalhes específicos
- 40-59: Interessado mas ainda avaliando opções
- 20-39: Apenas pesquisando, sem pressa
- 0-19: Só olhando, sem interesse real

URGÊNCIA (0-100):
- 80-100: Urgente, hoje, agora, imediato
- 60-79: Esta semana, nos próximos dias
- 40-59: Este mês, sem pressa definida
- 20-39: Próximo mês, futuro
- 0-19: Sem prazo, apenas pesquisando

OBJEÇÕES (lista):
- Preocupações com preço, localização, condições
- Dúvidas sobre disponibilidade
- Comparando com outras opções
- Problemas mencionados

SCORE FINAL (0-150):
- Score = (sentimento * 0.3) + (intencao_compra * 0.5) + (urgencia * 0.4)
- Max: 150 pontos

CLASSIFICAÇÃO:
- QUENTE (100+): Quer visitar/comprar, urgente, muito positivo
- MORNO (50-99): Interessado mas indeciso, avaliando
- FRIO (0-49): Só pesquisando, negativo, desinteressado

TAGS INTELIGENTES:
- Baseadas na análise (ex: "urgente", "preco_alto", "primeira_vez", "comparando_opcoes")
- Máximo 5 tags mais relevantes

Retorne APENAS o JSON, sem markdown nem explicações."""

    def __init__(self, openrouter_key: str, redis_client: Optional[redis.Redis] = None):
        """
        Inicializa analisador

        Args:
            openrouter_key: Chave API OpenRouter
            redis_client: Cliente Redis (opcional, para cache)
        """
        self.api_key = openrouter_key
        self.redis = redis_client
        self.timeout = 10  # Timeout 10s

    def analisar(self, mensagem: str, contexto: List[str] = None) -> Dict[str, Any]:
        """
        Analisa mensagem com IA e retorna análise completa

        Args:
            mensagem: Mensagem atual do cliente
            contexto: Lista de mensagens anteriores (últimas 3-5)

        Returns:
            {
                'sentimento': 0-100,
                'intencao_compra': 0-100,
                'urgencia': 0-100,
                'objecoes': [],
                'score': 0-150,
                'classificacao': 'QUENTE|MORNO|FRIO',
                'tags': [],
                'justificativa': ''
            }
        """
        # Verificar cache no Redis
        if self.redis:
            cache_key = f"analise_ia:{hash(mensagem)}"
            cached = self.redis.get(cache_key)
            if cached:
                try:
                    return json.loads(cached)
                except:
                    pass

        # Preparar contexto
        contexto_str = "Nenhum histórico disponível"
        if contexto:
            contexto_str = "\n".join([f"- {msg}" for msg in contexto[-5:]])  # Últimas 5 msgs

        # Montar prompt
        prompt = self.PROMPT_ANALISE.format(
            mensagem=mensagem,
            contexto=contexto_str
        )

        # Chamar IA
        try:
            resultado = self._chamar_ia(prompt)

            # Validar resultado
            resultado = self._validar_resultado(resultado)

            # Salvar cache (TTL 1 hora)
            if self.redis:
                self.redis.setex(cache_key, 3600, json.dumps(resultado))

            return resultado

        except Exception as e:
            print(f"⚠️ Erro na análise IA: {e}")
            # Fallback: análise básica
            return self._analise_fallback(mensagem)

    def _chamar_ia(self, prompt: str) -> Dict[str, Any]:
        """
        Chama Claude Haiku via OpenRouter

        Args:
            prompt: Prompt completo

        Returns:
            Dict com análise
        """
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "x-ai/grok-4-fast",  # Grok-4-fast - X.AI (rápido e preciso)
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,  # Baixa temperatura = mais consistente
            "max_tokens": 500
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=self.timeout
        )

        response.raise_for_status()

        # Extrair resposta
        resposta_texto = response.json()["choices"][0]["message"]["content"]

        # Limpar markdown se tiver
        resposta_texto = resposta_texto.strip()
        if resposta_texto.startswith("```json"):
            resposta_texto = resposta_texto.replace("```json", "").replace("```", "").strip()
        elif resposta_texto.startswith("```"):
            resposta_texto = resposta_texto.replace("```", "").strip()

        # Parse JSON
        return json.loads(resposta_texto)

    def _validar_resultado(self, resultado: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida e normaliza resultado da IA

        Args:
            resultado: Dict retornado pela IA

        Returns:
            Dict validado e normalizado
        """
        # Valores default
        default = {
            'sentimento': 50,
            'intencao_compra': 50,
            'urgencia': 50,
            'objecoes': [],
            'score': 50,
            'classificacao': 'MORNO',
            'tags': [],
            'justificativa': ''
        }

        # Validar campos obrigatórios
        for campo in ['sentimento', 'intencao_compra', 'urgencia', 'score']:
            if campo not in resultado:
                resultado[campo] = default[campo]
            else:
                # Garantir que está no range correto
                if campo == 'score':
                    resultado[campo] = max(0, min(150, int(resultado[campo])))
                else:
                    resultado[campo] = max(0, min(100, int(resultado[campo])))

        # Validar listas
        for campo in ['objecoes', 'tags']:
            if campo not in resultado or not isinstance(resultado[campo], list):
                resultado[campo] = default[campo]

        # Validar classificação
        if 'classificacao' not in resultado or resultado['classificacao'] not in ['QUENTE', 'MORNO', 'FRIO']:
            score = resultado['score']
            if score >= 100:
                resultado['classificacao'] = 'QUENTE'
            elif score >= 50:
                resultado['classificacao'] = 'MORNO'
            else:
                resultado['classificacao'] = 'FRIO'

        # Validar justificativa
        if 'justificativa' not in resultado:
            resultado['justificativa'] = default['justificativa']

        return resultado

    def _analise_fallback(self, mensagem: str) -> Dict[str, Any]:
        """
        Análise básica quando IA falha (fallback)

        Args:
            mensagem: Mensagem do cliente

        Returns:
            Dict com análise básica
        """
        mensagem_lower = mensagem.lower()

        # Palavras-chave básicas
        palavras_positivas = ["sim", "quero", "gostei", "ótimo", "perfeito", "excelente"]
        palavras_negativas = ["não", "nao", "caro", "longe", "pequeno", "ruim"]
        palavras_urgentes = ["urgente", "hoje", "agora", "rápido", "rapido"]
        palavras_visita = ["visitar", "agendar", "ver", "conhecer"]
        palavras_fechar = ["fechar", "proposta", "contrato", "alugar"]

        # Calcular scores básicos
        sentimento = 50
        if any(p in mensagem_lower for p in palavras_positivas):
            sentimento = 70
        elif any(p in mensagem_lower for p in palavras_negativas):
            sentimento = 30

        intencao = 50
        if any(p in mensagem_lower for p in palavras_fechar):
            intencao = 90
        elif any(p in mensagem_lower for p in palavras_visita):
            intencao = 75

        urgencia = 50
        if any(p in mensagem_lower for p in palavras_urgentes):
            urgencia = 85

        # Score final (mesmo cálculo da IA)
        score = int((sentimento * 0.3) + (intencao * 0.5) + (urgencia * 0.4))

        # Classificação
        if score >= 100:
            classificacao = "QUENTE"
        elif score >= 50:
            classificacao = "MORNO"
        else:
            classificacao = "FRIO"

        return {
            'sentimento': sentimento,
            'intencao_compra': intencao,
            'urgencia': urgencia,
            'objecoes': [],
            'score': score,
            'classificacao': classificacao,
            'tags': ['fallback'],
            'justificativa': 'Análise básica (IA indisponível)'
        }

    def analisar_historico(self, mensagens: List[str]) -> Dict[str, Any]:
        """
        Analisa histórico completo de mensagens

        Args:
            mensagens: Lista de mensagens (ordem cronológica)

        Returns:
            Dict com análise agregada
        """
        if not mensagens:
            return self._analise_fallback("")

        # Analisar última mensagem com contexto
        ultima = mensagens[-1]
        contexto = mensagens[:-1] if len(mensagens) > 1 else []

        return self.analisar(ultima, contexto)


# Teste standalone
if __name__ == "__main__":
    import sys

    # Pegar API key
    OPENROUTER_KEY = "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"

    # Criar analisador
    analisador = AnalisadorLeadIA(OPENROUTER_KEY)

    # Casos de teste
    casos_teste = [
        {
            "mensagem": "Quero agendar uma visita hoje mesmo! É urgente!",
            "contexto": ["Olá", "Tenho interesse no apartamento"]
        },
        {
            "mensagem": "Muito caro, não tenho interesse",
            "contexto": ["Quanto custa?"]
        },
        {
            "mensagem": "Tem foto do imóvel?",
            "contexto": []
        },
        {
            "mensagem": "Gostei! Quero fazer uma proposta",
            "contexto": ["Vi as fotos", "É na Savassi né?"]
        }
    ]

    print("\n🧪 TESTE ANÁLISE DE LEADS COM IA\n")
    print("=" * 60)

    for i, caso in enumerate(casos_teste, 1):
        print(f"\n📋 CASO {i}")
        print(f"Mensagem: {caso['mensagem']}")
        print(f"Contexto: {caso['contexto']}")
        print("-" * 60)

        try:
            resultado = analisador.analisar(
                caso['mensagem'],
                caso['contexto']
            )

            print(f"\n✅ RESULTADO:")
            print(f"  📊 Score: {resultado['score']}/150")
            print(f"  🔥 Classificação: {resultado['classificacao']}")
            print(f"  😊 Sentimento: {resultado['sentimento']}/100")
            print(f"  💰 Intenção Compra: {resultado['intencao_compra']}/100")
            print(f"  ⏰ Urgência: {resultado['urgencia']}/100")
            print(f"  🏷️  Tags: {', '.join(resultado['tags'])}")
            if resultado['objecoes']:
                print(f"  ⚠️  Objeções: {', '.join(resultado['objecoes'])}")
            print(f"  💭 Justificativa: {resultado['justificativa']}")

        except Exception as e:
            print(f"\n❌ ERRO: {e}")

        print("=" * 60)

    print("\n✅ Teste concluído!")
