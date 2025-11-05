#!/usr/bin/env python3
"""
🤖 IA ESPECIALISTA - Responde com Progressive Disclosure

Usa Claude Haiku 4.5 (mesmo modelo do bot V4)
Contexto limitado = Precisão 100%
"""

import requests
from typing import Dict, List, Optional


class IAEspecialista:
    """
    IA especialista que responde baseado em dados do Progressive Disclosure
    """

    def __init__(self, openrouter_api_key: str, model: str = "anthropic/claude-haiku-4.5"):
        """
        Args:
            openrouter_api_key: Chave API OpenRouter
            model: Modelo a usar (padrão: Claude Haiku 4.5)
        """
        self.api_key = openrouter_api_key
        self.model = model
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    def responder(
        self,
        dados_disclosure: Dict,
        mensagem_cliente: str,
        contexto: Optional[List[Dict]] = None
    ) -> str:
        """
        Gera resposta usando dados do Progressive Disclosure

        Args:
            dados_disclosure: Dict retornado por ProgressiveDisclosure.carregar()
            mensagem_cliente: Pergunta do cliente
            contexto: Histórico da conversa (opcional)

        Returns:
            Resposta da IA
        """
        # Valida dados
        if "erro" in dados_disclosure:
            return f"Desculpa, não encontrei informações sobre esse imóvel. {dados_disclosure['erro']}"

        if not dados_disclosure.get("dados"):
            return "Desculpa, não tenho informações disponíveis sobre esse imóvel no momento."

        # Monta prompt
        prompt = self._montar_prompt(dados_disclosure, mensagem_cliente, contexto)

        # Chama API
        try:
            resposta = self._chamar_api(prompt)
            return resposta

        except Exception as e:
            print(f"❌ Erro ao chamar IA: {e}", flush=True)
            return "Desculpa, tive um problema ao processar sua pergunta. Pode tentar novamente?"

    def _montar_prompt(
        self,
        dados_disclosure: Dict,
        mensagem_cliente: str,
        contexto: Optional[List[Dict]] = None
    ) -> List[Dict]:
        """
        Monta prompt para a IA

        Args:
            dados_disclosure: Dados do imóvel
            mensagem_cliente: Pergunta do cliente
            contexto: Histórico

        Returns:
            Lista de mensagens no formato OpenAI
        """
        # Formata dados do imóvel
        info_imovel = self._formatar_dados(dados_disclosure)

        # System prompt
        system_msg = {
            "role": "system",
            "content": f"""Você é um corretor de imóveis profissional atendendo via WhatsApp.

🏠 IMÓVEL ATIVO: {dados_disclosure['imóvel_id']}

📋 INFORMAÇÕES DISPONÍVEIS:
{info_imovel}

⚠️ REGRAS IMPORTANTES:
1. Responda APENAS com base nas informações acima
2. Se não souber algo, diga: "Vou consultar e te retorno! 😊"
3. Seja natural, amigável e use emojis moderadamente
4. Respostas curtas (2-3 frases)
5. Foque na pergunta específica do cliente
6. NÃO invente informações
7. NÃO mencione outros imóveis
8. Use linguagem informal de WhatsApp"""
        }

        # Mensagens
        mensagens = [system_msg]

        # Adiciona contexto (últimas 6 mensagens)
        if contexto:
            for msg in contexto[-6:]:
                mensagens.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })

        # Adiciona mensagem atual
        mensagens.append({
            "role": "user",
            "content": mensagem_cliente
        })

        return mensagens

    def _formatar_dados(self, dados_disclosure: Dict) -> str:
        """
        Formata dados do disclosure para o prompt

        Args:
            dados_disclosure: Dict com dados

        Returns:
            String formatada
        """
        dados = dados_disclosure.get("dados", {})

        if not dados:
            return "Nenhuma informação disponível."

        # Monta texto por seção
        secoes = []

        ordem = ["base", "detalhes", "faq", "legal", "financiamento"]

        for nivel in ordem:
            if nivel in dados:
                conteudo = dados[nivel]
                secoes.append(conteudo)

        return "\n\n".join(secoes)

    def _chamar_api(self, mensagens: List[Dict]) -> str:
        """
        Chama API OpenRouter

        Args:
            mensagens: Lista de mensagens

        Returns:
            Resposta da IA
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": mensagens,
            "temperature": 0.7,
            "max_tokens": 300  # Respostas curtas
        }

        response = requests.post(
            self.url,
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

    def responder_multiplos_imoveis(
        self,
        candidatos: List[Dict],
        mensagem_cliente: str
    ) -> str:
        """
        Apresenta múltiplos imóveis ao cliente (ESTÁGIO 1 do RAG)

        Args:
            candidatos: Lista de imóveis candidatos
            mensagem_cliente: Mensagem do cliente

        Returns:
            Mensagem formatada com opções
        """
        if not candidatos:
            return "Não encontrei imóveis com essas características. Pode me dar mais detalhes? 🏠"

        if len(candidatos) == 1:
            return f"Encontrei o imóvel perfeito! Vou te contar mais sobre ele. O que quer saber? 😊"

        # Múltiplos candidatos - apresenta lista
        msg = f"Achei {len(candidatos)} opções que podem te interessar! 🏠\n\n"

        for i, imovel in enumerate(candidatos, 1):
            # Monta linha resumida
            tipo = imovel.get("tipo", "imóvel")
            regiao = imovel.get("regiao", "")
            quartos = imovel.get("quartos")

            linha = f"{i}️⃣ {tipo.title()}"

            if quartos:
                linha += f" {quartos} quartos"

            if regiao:
                linha += f" - {regiao.title()}"

            msg += linha + "\n"

        msg += "\nQual te interessa mais? Me fala o número! 😊"

        return msg


if __name__ == "__main__":
    # Teste standalone
    print("🧪 Testando IA Especialista...")

    from pathlib import Path
    import sys

    # Adiciona path do progressive_disclosure
    sys.path.append(str(Path(__file__).parent))

    from progressive_disclosure import ProgressiveDisclosure

    # Config
    openrouter_key = "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"
    imoveis_dir = Path(__file__).parent.parent.parent / "imoveis"

    # Instâncias
    disclosure = ProgressiveDisclosure(imoveis_dir)
    ia = IAEspecialista(openrouter_key)

    # Pega primeiro imóvel
    primeiro_imovel = None
    for imóvel in imoveis_dir.iterdir():
        if imóvel.is_dir():
            primeiro_imovel = imóvel.name
            break

    if not primeiro_imovel:
        print("⚠️  Nenhum imóvel encontrado")
        sys.exit(1)

    print(f"Imóvel de teste: {primeiro_imovel}")

    # Teste 1: Pergunta básica (carrega só base)
    print("\n📋 Teste 1: Pergunta básica")
    print("-" * 50)

    mensagem = "Me fala sobre esse imóvel"
    niveis = disclosure.detectar_nivel(mensagem)
    dados = disclosure.carregar(primeiro_imovel, niveis)

    print(f"Níveis carregados: {niveis}")
    print(f"Tokens: {dados['tokens']}")

    resposta = ia.responder(dados, mensagem)
    print(f"\n🤖 Resposta:\n{resposta}")

    # Teste 2: Pergunta específica (carrega base + faq)
    print("\n\n📋 Teste 2: Pergunta específica")
    print("-" * 50)

    mensagem = "Qual o valor do IPTU?"
    niveis = disclosure.detectar_nivel(mensagem)
    dados = disclosure.carregar(primeiro_imovel, niveis)

    print(f"Níveis carregados: {niveis}")
    print(f"Tokens: {dados['tokens']}")

    resposta = ia.responder(dados, mensagem)
    print(f"\n🤖 Resposta:\n{resposta}")
