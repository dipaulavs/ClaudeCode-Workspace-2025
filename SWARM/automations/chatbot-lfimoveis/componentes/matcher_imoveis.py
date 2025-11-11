#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 MATCHER DE IMÓVEIS - Identificação Automática com IA

Responsabilidade:
- Analisa mensagem do cliente usando Grok-4-fast
- Faz matching semântico inteligente (não só keywords)
- Retorna top 3 matches com scores e justificativas
- Fallback: busca simples se IA falhar

INTERFACE OBRIGATÓRIA:
┌─────────────────────────────────────┐
│  encontrar_melhor_match(            │
│      mensagem: str,                 │
│      contexto_cliente: list         │
│  ) -> dict                          │
└─────────────────────────────────────┘

Returns:
{
    'sucesso': True/False,
    'imovel_id': 1,
    'slug': 'chacara-itatiaiucu-001',
    'score_match': 95,
    'confianca': 'alta'|'media'|'baixa',
    'motivo': 'Chácara 1000m² região BH conforme pedido',
    'alternativas': [...]  # Top 3
}

Autor: Claude Code
Data: 2025-11-05
"""

import json
import os
import time
import re
from pathlib import Path
from typing import Optional, Dict, Any, List
import requests
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()


class MatcherImoveis:
    """
    Sub-agente especializado em identificar qual imóvel o cliente quer

    Usa Grok-4-fast (OpenRouter) para matching semântico inteligente
    Fallback: busca simples por keywords se IA falhar
    """

    def __init__(
        self,
        imoveis_dir: str = None,
        redis_client=None,
        openrouter_key: str = None,
        timeout: int = 15
    ):
        """
        Inicializa matcher

        Args:
            imoveis_dir: Diretório com os imóveis (default: ../imoveis)
            redis_client: Cliente Redis para cache (opcional)
            openrouter_key: Chave OpenRouter (default: variável ambiente)
            timeout: Timeout para chamadas IA em segundos (default: 15s)
        """
        # Caminhos
        self.base_dir = Path(__file__).parent.parent
        self.imoveis_dir = Path(imoveis_dir) if imoveis_dir else self.base_dir / "imoveis"
        self.indice_path = self.imoveis_dir / "INDICE.json"

        # Redis (opcional)
        self.redis = redis_client

        # API
        self.api_key = openrouter_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY não encontrada no .env")

        self.timeout = timeout
        self.modelo = "x-ai/grok-4-fast"  # Modelo rápido e eficiente
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"

        # Carrega índice de imóveis
        self.indice = self._carregar_indice()

        print(f"✅ Matcher de imóveis carregado - {len(self.indice.get('imoveis', []))} disponíveis", flush=True)

    def _carregar_indice(self) -> Dict:
        """Carrega índice de imóveis do arquivo INDICE.json"""
        try:
            if not self.indice_path.exists():
                raise FileNotFoundError(f"INDICE.json não encontrado em: {self.indice_path}")

            with open(self.indice_path, 'r', encoding='utf-8') as f:
                indice = json.load(f)

            # Validação básica
            if 'imoveis' not in indice:
                raise ValueError("INDICE.json inválido: falta campo 'imoveis'")

            return indice

        except Exception as e:
            print(f"❌ ERRO ao carregar índice: {e}", flush=True)
            return {"imoveis": []}


    def _chamar_grok(self, prompt: str) -> Optional[Dict]:
        """
        Chama Grok-4-fast via OpenRouter para análise semântica

        Args:
            prompt: Prompt estruturado para matching

        Returns:
            Resposta parseada do modelo (JSON) ou None se falhar
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/felipemdepaula/whatsapp-chatbot-lfimoveis",
                "X-Title": "LFImóveis Matcher"
            }

            payload = {
                "model": self.modelo,
                "messages": [
                    {
                        "role": "system",
                        "content": "Você é um especialista em matching imobiliário. Retorne SEMPRE JSON válido."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3,  # Mais determinístico para matching
                "max_tokens": 1000,
                "response_format": {"type": "json_object"}
            }

            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()

            result = response.json()
            content = result['choices'][0]['message']['content']

            # Parse JSON da resposta
            return json.loads(content)

        except requests.exceptions.Timeout:
            print(f"⚠️ Timeout após {self.timeout}s", flush=True)
            return None

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Erro HTTP: {e}", flush=True)
            return None

        except json.JSONDecodeError as e:
            print(f"⚠️ Erro ao parsear JSON: {e}", flush=True)
            return None

        except Exception as e:
            print(f"⚠️ Erro inesperado: {e}", flush=True)
            return None

    def _fallback_busca_simples(self, mensagem: str) -> List[Dict]:
        """
        Fallback: busca simples por keywords se IA falhar

        Args:
            mensagem: Mensagem do cliente (normalizada)

        Returns:
            Lista de matches encontrados (top 3)
        """
        print("⚠️ Usando fallback: busca por keywords", flush=True)

        # Normaliza mensagem
        msg_lower = mensagem.lower()
        msg_normalizada = (
            msg_lower
            .replace('á', 'a').replace('é', 'e').replace('í', 'i')
            .replace('ó', 'o').replace('ú', 'u').replace('ã', 'a')
            .replace('õ', 'o').replace('ç', 'c')
        )

        matches = []

        for imovel in self.indice.get('imoveis', []):
            score = 0
            motivos = []

            # Verifica tipo
            tipo = imovel.get('tipo', '').lower()
            if tipo in msg_normalizada:
                score += 30
                motivos.append(f"tipo: {tipo}")

            # Verifica cidade/região
            cidade = imovel.get('cidade', '').lower()
            regiao = imovel.get('regiao_metropolitana', '').lower()

            if cidade in msg_normalizada:
                score += 25
                motivos.append(f"cidade: {cidade}")

            if regiao in msg_normalizada or 'bh' in msg_normalizada:
                score += 20
                motivos.append(f"região: {regiao}")

            # Verifica características-chave
            caracteristicas = imovel.get('caracteristicas_chave', [])
            for caract in caracteristicas:
                caract_normalizada = caract.lower().replace('ç', 'c').replace('ã', 'a')

                # Busca termos específicos
                if 'poco' in msg_normalizada and 'poco' in caract_normalizada:
                    score += 15
                    motivos.append("tem poço artesiano")

                if 'agua' in msg_normalizada and 'artesiano' in caract_normalizada:
                    score += 15
                    motivos.append("água própria")

                if 'sem juros' in msg_normalizada and 'sem juros' in caract_normalizada:
                    score += 10
                    motivos.append("sem juros")

            # Verifica área
            area = imovel.get('area_m2', 0)
            if re.search(r'\b\d{3,5}\s*m', msg_normalizada):
                area_match = re.search(r'\b(\d{3,5})\s*m', msg_normalizada)
                if area_match:
                    area_desejada = int(area_match.group(1))
                    if abs(area - area_desejada) / area_desejada <= 0.3:
                        score += 15
                        motivos.append(f"área próxima: {area}m²")

            # Adiciona match se tiver score mínimo
            if score >= 20:
                matches.append({
                    "id": imovel.get('id'),
                    "slug": imovel.get('slug'),
                    "score": score,
                    "motivo": f"{imovel.get('titulo', 'Imóvel')} - {', '.join(motivos)}"
                })

        # Ordena por score (maior primeiro)
        matches.sort(key=lambda x: x['score'], reverse=True)

        return matches[:3]  # Top 3


    def encontrar_melhor_match(
        self,
        mensagem: str,
        contexto_cliente: List[str] = None
    ) -> Dict[str, Any]:
        """
        Encontra imóvel que melhor corresponde ao pedido do cliente

        Args:
            mensagem: Mensagem atual do cliente
            contexto_cliente: Mensagens anteriores da conversa (opcional)

        Returns:
            {
                'sucesso': True/False,
                'imovel_id': 1,
                'slug': 'chacara-itatiaiucu-001',
                'score_match': 95,
                'confianca': 'alta|media|baixa',
                'motivo': 'Chácara 1000m² região BH conforme pedido',
                'caracteristicas_extraidas': {...},
                'alternativas': [...]  # Top 3
            }
        """
        print(f"🔍 Analisando: '{mensagem[:80]}...'", flush=True)

        # Validações
        if not mensagem or len(mensagem.strip()) < 3:
            return {
                'sucesso': False,
                'erro': 'Mensagem muito curta para análise',
                'alternativas': []
            }

        if not self.indice.get('imoveis'):
            return {
                'sucesso': False,
                'erro': 'Nenhum imóvel disponível no catálogo',
                'alternativas': []
            }

        # Monta contexto da conversa
        contexto_str = ""
        if contexto_cliente and len(contexto_cliente) > 0:
            contexto_str = "\n".join(contexto_cliente[-3:])

        # Monta prompt estruturado para Grok
        prompt = f"""Você é especialista em matching imobiliário. Analise o pedido e encontre o melhor imóvel.

PEDIDO DO CLIENTE:
"{mensagem}"

CONTEXTO CONVERSA (últimas mensagens):
{contexto_str if contexto_str else 'Primeira mensagem do cliente'}

CATÁLOGO DISPONÍVEL ({self.indice.get('total_imoveis', 0)} imóveis):
{json.dumps(self.indice.get('imoveis', []), indent=2, ensure_ascii=False)}

ANALISE e retorne JSON com esta ESTRUTURA EXATA:
{{
  "matches": [
    {{
      "id": <id_imovel_numerico>,
      "score": <0-100>,
      "motivo": "descrição breve por que atende"
    }}
  ],
  "melhor_match_id": <id_do_melhor>,
  "confianca": <0-100>,
  "caracteristicas_extraidas": {{
    "tipo": "chacara|apartamento|casa|terreno",
    "area_desejada": <numero_ou_null>,
    "cidade": "string_ou_null",
    "preco_max": <numero_ou_null>,
    "caracteristicas_importantes": ["lista", "de", "features"]
  }}
}}

CRITÉRIOS DE SCORING:
- Score 80-100: Match perfeito (tipo + localização + características)
- Score 50-79: Match parcial (alguns critérios atendidos)
- Score 0-49: Match fraco (sugerir apenas se único disponível)

REGRAS:
- Retorne SEMPRE os 3 melhores matches (ou todos disponíveis se menos de 3)
- Score deve ser número inteiro 0-100
- Confiança baseada em clareza do pedido
- Se cliente só cumprimentar/perguntar geral: confiança < 30
"""

        # Tenta análise com IA
        start_time = time.time()
        resultado_ia = self._chamar_grok(prompt)
        tempo_ia = time.time() - start_time

        # Fallback se IA falhar
        if not resultado_ia:
            print(f"⚠️ IA falhou após {tempo_ia:.1f}s, usando fallback", flush=True)
            matches_fallback = self._fallback_busca_simples(mensagem)

            if not matches_fallback:
                return {
                    'sucesso': False,
                    'erro': 'Nenhum imóvel corresponde aos critérios',
                    'sugestao': 'Tente descrever: tipo, localização, tamanho ou características',
                    'alternativas': []
                }

            # Retorna resultado do fallback
            melhor = matches_fallback[0]
            return {
                'sucesso': True,
                'metodo': 'fallback_keywords',
                'imovel_id': melhor['id'],
                'slug': melhor['slug'],
                'score_match': melhor['score'],
                'confianca': 'baixa',
                'motivo': melhor['motivo'],
                'alternativas': matches_fallback,
                'tempo_processamento_s': tempo_ia
            }

        # Processa resultado da IA
        print(f"✅ IA respondeu em {tempo_ia:.1f}s", flush=True)

        try:
            matches = resultado_ia.get('matches', [])
            melhor_id = resultado_ia.get('melhor_match_id')
            confianca_num = resultado_ia.get('confianca', 0)
            caracteristicas = resultado_ia.get('caracteristicas_extraidas', {})

            if not matches or not melhor_id:
                print("⚠️ IA não retornou matches, tentando fallback", flush=True)
                matches_fallback = self._fallback_busca_simples(mensagem)

                if not matches_fallback:
                    return {
                        'sucesso': False,
                        'erro': 'Nenhum imóvel corresponde aos critérios',
                        'alternativas': []
                    }

                melhor = matches_fallback[0]
                return {
                    'sucesso': True,
                    'metodo': 'fallback_keywords',
                    'imovel_id': melhor['id'],
                    'slug': melhor['slug'],
                    'score_match': melhor['score'],
                    'confianca': 'baixa',
                    'motivo': melhor['motivo'],
                    'alternativas': matches_fallback,
                    'tempo_processamento_s': tempo_ia
                }

            # Encontra dados completos do melhor match
            melhor_match = next(
                (m for m in matches if m.get('id') == melhor_id),
                matches[0] if matches else None
            )

            if not melhor_match:
                return {
                    'sucesso': False,
                    'erro': 'Erro ao processar resultado da IA',
                    'alternativas': []
                }

            # Encontra slug do imóvel
            imovel_completo = next(
                (im for im in self.indice.get('imoveis', []) if im.get('id') == melhor_id),
                None
            )

            # Classifica confiança
            if confianca_num >= 80:
                confianca = 'alta'
            elif confianca_num >= 50:
                confianca = 'media'
            else:
                confianca = 'baixa'

            # Retorna resultado estruturado
            return {
                'sucesso': True,
                'metodo': 'ia_grok4fast',
                'imovel_id': melhor_id,
                'slug': imovel_completo.get('slug') if imovel_completo else None,
                'score_match': melhor_match.get('score', 0),
                'confianca': confianca,
                'confianca_numerica': confianca_num,
                'motivo': melhor_match.get('motivo', 'Match identificado'),
                'caracteristicas_extraidas': caracteristicas,
                'alternativas': matches[:3],
                'tempo_processamento_s': tempo_ia,
                'modelo_usado': self.modelo
            }

        except Exception as e:
            print(f"❌ Erro ao processar resultado IA: {e}", flush=True)

            # Último recurso: fallback
            matches_fallback = self._fallback_busca_simples(mensagem)

            if not matches_fallback:
                return {
                    'sucesso': False,
                    'erro': f'Erro ao processar: {str(e)}',
                    'alternativas': []
                }

            melhor = matches_fallback[0]
            return {
                'sucesso': True,
                'metodo': 'fallback_erro',
                'imovel_id': melhor['id'],
                'slug': melhor['slug'],
                'score_match': melhor['score'],
                'confianca': 'baixa',
                'motivo': melhor['motivo'],
                'alternativas': matches_fallback,
                'erro_original': str(e)
            }



# ========== EXEMPLO DE USO ==========

if __name__ == "__main__":
    print("=" * 80)
    print("🧪 TESTE: Matcher de Imóveis com IA (Grok-4-fast)")
    print("=" * 80)

    try:
        # Inicializa matcher
        print("\n[1/3] Inicializando matcher...")
        matcher = MatcherImoveis()

        # Testes com diferentes mensagens
        testes = [
            {
                "mensagem": "Quero uma chácara perto de BH com água própria",
                "descricao": "Pedido específico com características"
            },
            {
                "mensagem": "Procuro terreno 1000m2 Itatiaiucu",
                "descricao": "Busca por localização + área"
            },
            {
                "mensagem": "Tem alguma chácara barata sem juros?",
                "descricao": "Busca por condições de pagamento"
            },
            {
                "mensagem": "Olá, bom dia!",
                "descricao": "Mensagem genérica (sem intenção clara)"
            }
        ]

        print(f"\n[2/3] Executando {len(testes)} testes...\n")

        for i, teste in enumerate(testes, 1):
            print(f"\n{'='*80}")
            print(f"TESTE {i}/{len(testes)}: {teste['descricao']}")
            print(f"Mensagem: \"{teste['mensagem']}\"")
            print(f"{'='*80}")

            resultado = matcher.encontrar_melhor_match(teste['mensagem'])

            print(f"\n📊 RESULTADO:")
            print(json.dumps(resultado, indent=2, ensure_ascii=False))

            # Análise do resultado
            if resultado.get('sucesso'):
                print(f"\n✅ Match encontrado!")
                print(f"   Imóvel: {resultado.get('slug')}")
                print(f"   Score: {resultado.get('score_match')}")
                print(f"   Confiança: {resultado.get('confianca')}")
                print(f"   Método: {resultado.get('metodo')}")
                print(f"   Tempo: {resultado.get('tempo_processamento_s', 0):.2f}s")
            else:
                print(f"\n❌ Nenhum match encontrado")
                print(f"   Erro: {resultado.get('erro')}")

            # Delay entre testes (rate limiting)
            if i < len(testes):
                print(f"\n⏳ Aguardando 3s antes do próximo teste...")
                time.sleep(3)

        print(f"\n{'='*80}")
        print("✅ [3/3] Testes concluídos!")
        print(f"{'='*80}\n")

    except KeyboardInterrupt:
        print("\n\n⚠️ Testes interrompidos pelo usuário")

    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
