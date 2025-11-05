#!/usr/bin/env python3
"""
📚 PROGRESSIVE DISCLOSURE - Carregamento Progressivo

Sistema inteligente que carrega APENAS as informações necessárias:

Estrutura de arquivos por imóvel:
├── base.txt           # 200 tokens (SEMPRE carrega)
├── detalhes.txt       # 300 tokens (metragem, área, m²)
├── faq.txt            # 500 tokens (preço, IPTU, pet)
├── legal.txt          # 300 tokens (documentação)
└── financiamento.txt  # 400 tokens (financiamento)

Economia: 50% tokens (700 vs 1.700)
"""

import re
from pathlib import Path
from typing import List, Dict, Optional


class ProgressiveDisclosure:
    """
    Sistema de carregamento progressivo de informações
    """

    # Configuração dos níveis
    NIVEIS = {
        "base": {
            "arquivo": "base.txt",
            "tokens_estimados": 200,
            "sempre_carregar": True,
            "keywords": []
        },
        "detalhes": {
            "arquivo": "detalhes.txt",
            "tokens_estimados": 300,
            "sempre_carregar": False,
            "keywords": ["metragem", "área", "area", "tamanho", "m2", "m²", "metros", "dimensões", "dimensoes"]
        },
        "faq": {
            "arquivo": "faq.txt",
            "tokens_estimados": 500,
            "sempre_carregar": False,
            "keywords": ["valor", "preço", "preco", "iptu", "condomínio", "condominio", "pet", "cachorro", "gato", "animal", "quanto", "custa"]
        },
        "legal": {
            "arquivo": "legal.txt",
            "tokens_estimados": 300,
            "sempre_carregar": False,
            "keywords": ["documentação", "documentacao", "escritura", "certidão", "certidao", "registro", "documento", "papel", "papelada"]
        },
        "financiamento": {
            "arquivo": "financiamento.txt",
            "tokens_estimados": 400,
            "sempre_carregar": False,
            "keywords": ["financiamento", "banco", "parcela", "fgts", "financiar", "entrada", "prestação", "prestacao", "caixa"]
        }
    }

    def __init__(self, imoveis_dir: Path):
        """
        Args:
            imoveis_dir: Diretório raiz dos imóveis
        """
        self.imoveis_dir = imoveis_dir

    def detectar_nivel(self, mensagem: str) -> List[str]:
        """
        Detecta quais níveis de informação carregar baseado na mensagem

        Args:
            mensagem: Mensagem do cliente

        Returns:
            Lista de níveis necessários (ex: ["base", "faq"])
        """
        niveis_necessarios = ["base"]  # Base sempre é carregado

        mensagem_lower = mensagem.lower()

        # Verifica cada nível
        for nivel, config in self.NIVEIS.imóvels():
            if nivel == "base":
                continue  # Já incluído

            # Verifica se alguma keyword está presente
            keywords = config.get("keywords", [])
            if any(keyword in mensagem_lower for keyword in keywords):
                niveis_necessarios.append(nivel)

        return niveis_necessarios

    def carregar(self, imovel_id: str, niveis: Optional[List[str]] = None) -> Dict:
        """
        Carrega informações do imóvel de forma progressiva

        Args:
            imovel_id: ID do imóvel (nome da pasta)
            niveis: Lista de níveis a carregar (None = detecta automaticamente)

        Returns:
            Dict com:
                - dados: Dict {nivel: conteudo}
                - tokens: Total estimado de tokens
                - imóvel_id: ID do imóvel
                - niveis_carregados: Lista de níveis carregados
        """
        imovel_path = self.imoveis_dir / imovel_id

        if not imovel_path.exists():
            return {
                "erro": f"Imóvel '{imovel_id}' não encontrado",
                "dados": {},
                "tokens": 0,
                "imóvel_id": imovel_id,
                "niveis_carregados": []
            }

        # Se níveis não foram especificados, carrega apenas base
        if niveis is None:
            niveis = ["base"]

        dados = {}
        tokens_total = 0
        niveis_carregados = []

        for nivel in niveis:
            if nivel not in self.NIVEIS:
                continue

            config = self.NIVEIS[nivel]
            arquivo_path = imovel_path / config["arquivo"]

            # Se arquivo não existe, tenta fallback
            if not arquivo_path.exists():
                arquivo_path = self._tentar_fallback(imovel_path, nivel)

            if arquivo_path and arquivo_path.exists():
                try:
                    with open(arquivo_path, 'r', encoding='utf-8') as f:
                        conteudo = f.read().strip()

                    if conteudo:  # Só adiciona se tiver conteúdo
                        dados[nivel] = conteudo
                        tokens_total += config["tokens_estimados"]
                        niveis_carregados.append(nivel)

                except Exception as e:
                    print(f"⚠️  Erro ao ler {arquivo_path}: {e}", flush=True)

        return {
            "dados": dados,
            "tokens": tokens_total,
            "imóvel_id": imovel_id,
            "niveis_carregados": niveis_carregados
        }

    def _tentar_fallback(self, imovel_path: Path, nivel: str) -> Optional[Path]:
        """
        Tenta encontrar arquivo alternativo quando o arquivo do nível não existe

        Args:
            imovel_path: Path do imóvel
            nivel: Nome do nível

        Returns:
            Path do arquivo alternativo ou None
        """
        # Mapeamento de fallbacks
        fallbacks = {
            "base": ["descricao.txt", "informacoes.txt"],
            "faq": ["faq.txt", "perguntas.txt"],
            "detalhes": ["detalhes.txt", "caracteristicas.txt"],
            "legal": ["legal.txt", "documentacao.txt"],
            "financiamento": ["financiamento.txt", "pagamento.txt"]
        }

        if nivel not in fallbacks:
            return None

        for fallback_name in fallbacks[nivel]:
            fallback_path = imovel_path / fallback_name
            if fallback_path.exists():
                return fallback_path

        return None

    def carregar_completo(self, imovel_id: str) -> Dict:
        """
        Carrega TODOS os níveis do imóvel (usa máximo de tokens)

        Args:
            imovel_id: ID do imóvel

        Returns:
            Dict com todos os dados
        """
        todos_niveis = list(self.NIVEIS.keys())
        return self.carregar(imovel_id, todos_niveis)

    def estimar_tokens(self, niveis: List[str]) -> int:
        """
        Estima total de tokens para uma lista de níveis

        Args:
            niveis: Lista de níveis

        Returns:
            Total estimado de tokens
        """
        total = 0
        for nivel in niveis:
            if nivel in self.NIVEIS:
                total += self.NIVEIS[nivel]["tokens_estimados"]
        return total

    def formatar_para_prompt(self, dados_carregados: Dict) -> str:
        """
        Formata dados carregados para incluir no prompt da IA

        Args:
            dados_carregados: Dict retornado por carregar()

        Returns:
            String formatada para o prompt
        """
        if "erro" in dados_carregados:
            return f"❌ {dados_carregados['erro']}"

        dados = dados_carregados["dados"]
        if not dados:
            return "⚠️ Nenhuma informação disponível para este imóvel."

        # Monta texto formatado
        secoes = []

        # Ordem preferencial de apresentação
        ordem = ["base", "detalhes", "faq", "legal", "financiamento"]

        for nivel in ordem:
            if nivel in dados:
                # Títulos amigáveis
                titulos = {
                    "base": "INFORMAÇÕES BÁSICAS",
                    "detalhes": "DETALHES TÉCNICOS",
                    "faq": "PERGUNTAS FREQUENTES",
                    "legal": "DOCUMENTAÇÃO",
                    "financiamento": "FINANCIAMENTO"
                }

                titulo = titulos.get(nivel, nivel.upper())
                conteudo = dados[nivel]

                secoes.append(f"## {titulo}\n\n{conteudo}")

        # Adiciona metadados
        texto_final = "\n\n".join(secoes)

        # Adiciona rodapé com info de tokens
        tokens = dados_carregados.get("tokens", 0)
        niveis_carregados = dados_carregados.get("niveis_carregados", [])

        rodape = f"\n\n---\n_Níveis carregados: {', '.join(niveis_carregados)} | ~{tokens} tokens_"

        return texto_final + rodape


if __name__ == "__main__":
    # Teste standalone
    print("🧪 Testando Progressive Disclosure...")

    from pathlib import Path

    imoveis_dir = Path(__file__).parent.parent.parent / "imoveis"

    disclosure = ProgressiveDisclosure(imoveis_dir)

    # Teste 1: Detectar níveis
    print("\n📋 Teste 1: Detectar níveis")
    print("-" * 50)

    mensagens_teste = [
        "Me fala sobre esse imóvel",
        "Qual o valor do IPTU?",
        "Qual a metragem?",
        "Aceita financiamento?",
        "Tem documentação regularizada?"
    ]

    for msg in mensagens_teste:
        niveis = disclosure.detectar_nivel(msg)
        print(f"'{msg}' → {niveis}")

    # Teste 2: Carregar dados
    print("\n\n📋 Teste 2: Carregar dados")
    print("-" * 50)

    # Pega primeiro imóvel disponível
    primeiro_imovel = None
    for imóvel in imoveis_dir.iterdir():
        if imóvel.is_dir():
            primeiro_imovel = imóvel.name
            break

    if primeiro_imovel:
        print(f"Imóvel: {primeiro_imovel}")

        # Carrega só base
        dados = disclosure.carregar(primeiro_imovel, ["base"])
        print(f"\n✅ Base: {dados['tokens']} tokens")

        # Carrega base + faq
        dados = disclosure.carregar(primeiro_imovel, ["base", "faq"])
        print(f"✅ Base + FAQ: {dados['tokens']} tokens")

        # Carrega completo
        dados = disclosure.carregar_completo(primeiro_imovel)
        print(f"✅ Completo: {dados['tokens']} tokens")

        # Formata para prompt
        print("\n📝 Formatado para prompt:")
        print("-" * 50)
        texto = disclosure.formatar_para_prompt(dados)
        print(texto[:500] + "..." if len(texto) > 500 else texto)
    else:
        print("⚠️  Nenhum imóvel encontrado")
