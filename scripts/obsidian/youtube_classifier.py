#!/usr/bin/env python3
"""
Classificador de Vídeos do YouTube usando IA (Grok 4 Fast via OpenRouter)

Detecta automaticamente o tipo de conteúdo:
- Tutorial (passo a passo prático)
- Metodologia (frameworks, processos)
- Aula (conteúdo educacional teórico)
- Notícia (novidades, lançamentos)
- Review (análise de ferramentas/produtos)
- Outros (quando não se encaixa)
"""

import os
import sys
import json
import requests
from pathlib import Path

# Carregar .env
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent.parent / '.env'
    load_dotenv(env_path)
except ImportError:
    env_path = Path(__file__).parent.parent.parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value


class YouTubeClassifier:
    """Classificador de vídeos usando Grok 4 Fast via OpenRouter"""

    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY não encontrada no .env")

        self.api_endpoint = "https://openrouter.ai/api/v1/chat/completions"
        # Usar Grok 4 Fast da xAI (rápido e econômico)
        self.model = os.getenv("YOUTUBE_CLASSIFIER_MODEL", "x-ai/grok-4-fast")

        # Categorias possíveis
        self.categories = {
            "tutorial": "Tutoriais",
            "metodologia": "Metodologias",
            "aula": "Aulas",
            "noticia": "Noticias",
            "review": "Reviews",
            "outros": "Outros"
        }

    def classify(self, titulo: str, canal: str = "", descricao: str = "") -> dict:
        """
        Classifica o vídeo usando IA

        Args:
            titulo: Título do vídeo
            canal: Nome do canal (opcional)
            descricao: Descrição do vídeo (opcional)

        Returns:
            dict: {
                "categoria": "tutorial|metodologia|aula|noticia|review|outros",
                "pasta": "Tutoriais|Metodologias|Aulas|Noticias|Reviews|Outros",
                "confianca": 0.95,
                "razao": "Explicação da classificação"
            }
        """

        # Prompt para classificação
        prompt = f"""Você é um classificador de vídeos do YouTube. Analise as informações abaixo e classifique o vídeo em UMA das seguintes categorias:

**CATEGORIAS:**
1. **tutorial** - Vídeos passo a passo práticos, "como fazer", guias de implementação
2. **metodologia** - Frameworks, processos, sistemas, metodologias (ex: GTD, PARA, Second Brain)
3. **aula** - Conteúdo educacional teórico, explicações de conceitos, palestras
4. **noticia** - Novidades, lançamentos, anúncios, atualizações de produtos/tecnologias
5. **review** - Análises de ferramentas, produtos, comparações, opiniões
6. **outros** - Qualquer conteúdo que não se encaixa nas categorias acima

**INFORMAÇÕES DO VÍDEO:**
Título: {titulo}
{f"Canal: {canal}" if canal else ""}
{f"Descrição: {descricao[:500]}" if descricao else ""}

**INSTRUÇÕES:**
- Seja objetivo e preciso
- Escolha APENAS UMA categoria
- Base sua decisão principalmente no TÍTULO
- Se houver dúvida entre duas categorias, escolha a mais específica

**RESPONDA EM JSON:**
{{
    "categoria": "tutorial|metodologia|aula|noticia|review|outros",
    "confianca": 0.0-1.0,
    "razao": "Breve explicação (máx 50 palavras)"
}}
"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://claude-code-workspace.com",
            "X-Title": "Claude Code Workspace - YouTube Classifier"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,  # Baixa temperatura para classificação consistente
            "max_tokens": 500
        }

        try:
            response = requests.post(
                self.api_endpoint,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()

            result = response.json()
            content = result['choices'][0]['message']['content']

            # Extrair JSON da resposta
            # Tentar encontrar JSON na resposta (às vezes vem com texto extra)
            json_start = content.find('{')
            json_end = content.rfind('}') + 1

            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                classification = json.loads(json_str)
            else:
                classification = json.loads(content)

            # Validar categoria
            categoria = classification.get("categoria", "outros").lower()
            if categoria not in self.categories:
                categoria = "outros"

            return {
                "categoria": categoria,
                "pasta": self.categories[categoria],
                "confianca": classification.get("confianca", 0.8),
                "razao": classification.get("razao", "Classificação automática")
            }

        except requests.exceptions.RequestException as e:
            print(f"⚠️  Erro na API OpenRouter: {e}")
            return self._fallback_classification(titulo)

        except (json.JSONDecodeError, KeyError, IndexError) as e:
            print(f"⚠️  Erro ao processar resposta: {e}")
            return self._fallback_classification(titulo)

    def _fallback_classification(self, titulo: str) -> dict:
        """Classificação fallback baseada em palavras-chave se API falhar"""

        titulo_lower = titulo.lower()

        # Regras simples baseadas em palavras-chave
        if any(word in titulo_lower for word in ["como", "tutorial", "passo a passo", "guia", "aprenda"]):
            return {
                "categoria": "tutorial",
                "pasta": "Tutoriais",
                "confianca": 0.6,
                "razao": "Classificação por palavras-chave (fallback)"
            }

        if any(word in titulo_lower for word in ["metodologia", "framework", "sistema", "processo", "método"]):
            return {
                "categoria": "metodologia",
                "pasta": "Metodologias",
                "confianca": 0.6,
                "razao": "Classificação por palavras-chave (fallback)"
            }

        if any(word in titulo_lower for word in ["aula", "curso", "palestra", "explicando", "entendendo"]):
            return {
                "categoria": "aula",
                "pasta": "Aulas",
                "confianca": 0.6,
                "razao": "Classificação por palavras-chave (fallback)"
            }

        if any(word in titulo_lower for word in ["lançamento", "novo", "novidade", "anúncio", "atualização"]):
            return {
                "categoria": "noticia",
                "pasta": "Noticias",
                "confianca": 0.6,
                "razao": "Classificação por palavras-chave (fallback)"
            }

        if any(word in titulo_lower for word in ["review", "análise", "comparação", "vale a pena", "opinião"]):
            return {
                "categoria": "review",
                "pasta": "Reviews",
                "confianca": 0.6,
                "razao": "Classificação por palavras-chave (fallback)"
            }

        # Default
        return {
            "categoria": "outros",
            "pasta": "Outros",
            "confianca": 0.5,
            "razao": "Não foi possível determinar categoria específica"
        }


def main():
    """Teste do classificador"""
    if len(sys.argv) < 2:
        print("Uso: python3 youtube_classifier.py '<título>' ['<canal>'] ['<descrição>']")
        sys.exit(1)

    titulo = sys.argv[1]
    canal = sys.argv[2] if len(sys.argv) > 2 else ""
    descricao = sys.argv[3] if len(sys.argv) > 3 else ""

    classifier = YouTubeClassifier()
    print(f"\n🔍 Classificando vídeo...")
    print(f"   Título: {titulo}")
    if canal:
        print(f"   Canal: {canal}")

    result = classifier.classify(titulo, canal, descricao)

    print(f"\n✅ Classificação:")
    print(f"   📂 Categoria: {result['categoria']}")
    print(f"   📁 Pasta: {result['pasta']}")
    print(f"   📊 Confiança: {result['confianca']:.0%}")
    print(f"   💡 Razão: {result['razao']}\n")


if __name__ == "__main__":
    main()
