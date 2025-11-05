#!/usr/bin/env python3
"""
📚 PROGRESSIVE DISCLOSURE - Carregamento Progressivo (ADAPTADO PARA CARROS)

Sistema inteligente que carrega APENAS as informações necessárias:

Estrutura de arquivos por carro:
├── base.txt           # 200 tokens (SEMPRE carrega - marca, modelo, ano, km, preço)
├── detalhes.txt       # 300 tokens (motor, opcionais, consumo)
├── faq.txt            # 500 tokens (garantia, troca, financiamento)
├── historico.txt      # 300 tokens (proprietários, acidentes, revisões)
└── financiamento.txt  # 400 tokens (planos, entrada, parcelas)

Economia: 50% tokens (700 vs 1.700)
"""

import re
from pathlib import Path
from typing import List, Dict, Optional


class ProgressiveDisclosureCarros:
    """
    Sistema de carregamento progressivo de informações de carros
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
            "keywords": [
                "motor", "potência", "potencia", "cilindrada", "cavalos", "cv", "hp",
                "opcionais", "acessórios", "acessorios", "equipamentos",
                "consumo", "km/l", "kml", "economia",
                "acabamento", "versão", "versao", "modelo"
            ]
        },
        "faq": {
            "arquivo": "faq.txt",
            "tokens_estimados": 500,
            "sempre_carregar": False,
            "keywords": [
                "garantia", "troca", "aceita", "financiamento", "banco",
                "ipva", "licenciamento", "documentação", "documentacao",
                "valor", "preço", "preco", "quanto", "custa",
                "test drive", "testar", "visita", "ver"
            ]
        },
        "historico": {
            "arquivo": "historico.txt",
            "tokens_estimados": 300,
            "sempre_carregar": False,
            "keywords": [
                "histórico", "historico", "proprietário", "proprietario", "dono", "donos",
                "acidente", "batida", "sinistro", "recuperado",
                "revisão", "revisao", "manutenção", "manutencao", "mecânica", "mecanica",
                "original", "estado", "conservação", "conservacao"
            ]
        },
        "financiamento": {
            "arquivo": "financiamento.txt",
            "tokens_estimados": 400,
            "sempre_carregar": False,
            "keywords": [
                "financiamento", "financiar", "banco", "parcela", "parcelar",
                "entrada", "sinal", "prestação", "prestacao",
                "cdc", "consórcio", "consorcio", "leasing",
                "aprovação", "aprovacao", "crédito", "credito"
            ]
        }
    }

    def __init__(self, carros_dir: Path):
        """
        Args:
            carros_dir: Diretório raiz dos carros
        """
        self.carros_dir = carros_dir

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
        for nivel, config in self.NIVEIS.items():
            if nivel == "base":
                continue  # Já incluído

            # Verifica se alguma keyword está presente
            keywords = config.get("keywords", [])
            if any(keyword in mensagem_lower for keyword in keywords):
                niveis_necessarios.append(nivel)

        return niveis_necessarios

    def carregar(self, carro_id: str, niveis: Optional[List[str]] = None) -> Dict:
        """
        Carrega informações do carro de forma progressiva

        Args:
            carro_id: ID do carro (nome da pasta)
            niveis: Lista de níveis a carregar (None = detecta automaticamente)

        Returns:
            Dict com:
                - dados: Dict {nivel: conteudo}
                - tokens: Total estimado de tokens
                - item_id: ID do carro
                - niveis_carregados: Lista de níveis carregados
        """
        carro_path = self.carros_dir / carro_id

        if not carro_path.exists():
            return {
                "erro": f"Carro '{carro_id}' não encontrado",
                "dados": {},
                "tokens": 0,
                "item_id": carro_id,
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
            arquivo_path = carro_path / config["arquivo"]

            if arquivo_path.exists():
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
            "item_id": carro_id,
            "niveis_carregados": niveis_carregados
        }

    def carregar_completo(self, carro_id: str) -> Dict:
        """
        Carrega TODOS os níveis do carro (usa máximo de tokens)

        Args:
            carro_id: ID do carro

        Returns:
            Dict com todos os dados
        """
        todos_niveis = list(self.NIVEIS.keys())
        return self.carregar(carro_id, todos_niveis)

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
            return "⚠️ Nenhuma informação disponível para este carro."

        # Monta texto formatado
        secoes = []

        # Ordem preferencial de apresentação
        ordem = ["base", "detalhes", "faq", "historico", "financiamento"]

        for nivel in ordem:
            if nivel in dados:
                # Títulos amigáveis
                titulos = {
                    "base": "INFORMAÇÕES BÁSICAS",
                    "detalhes": "DETALHES TÉCNICOS",
                    "faq": "PERGUNTAS FREQUENTES",
                    "historico": "HISTÓRICO DO VEÍCULO",
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
    print("🧪 Testando Progressive Disclosure Carros...")

    from pathlib import Path

    carros_dir = Path(__file__).parent.parent.parent / "carros"

    disclosure = ProgressiveDisclosureCarros(carros_dir)

    # Teste 1: Detectar níveis
    print("\n📋 Teste 1: Detectar níveis")
    print("-" * 50)

    mensagens_teste = [
        "Me fala sobre esse carro",
        "Qual o motor dele?",
        "Quanto custa?",
        "Aceita financiamento?",
        "Teve algum acidente?"
    ]

    for msg in mensagens_teste:
        niveis = disclosure.detectar_nivel(msg)
        print(f"'{msg}' → {niveis}")

    # Teste 2: Carregar dados
    print("\n\n📋 Teste 2: Carregar dados")
    print("-" * 50)

    # Pega primeiro carro disponível
    primeiro_carro = None
    for item in carros_dir.iterdir():
        if item.is_dir():
            primeiro_carro = item.name
            break

    if primeiro_carro:
        print(f"Carro: {primeiro_carro}")

        # Carrega só base
        dados = disclosure.carregar(primeiro_carro, ["base"])
        print(f"\n✅ Base: {dados['tokens']} tokens")

        # Carrega base + faq
        dados = disclosure.carregar(primeiro_carro, ["base", "faq"])
        print(f"✅ Base + FAQ: {dados['tokens']} tokens")

        # Carrega completo
        dados = disclosure.carregar_completo(primeiro_carro)
        print(f"✅ Completo: {dados['tokens']} tokens")

        # Formata para prompt
        print("\n📝 Formatado para prompt:")
        print("-" * 50)
        texto = disclosure.formatar_para_prompt(dados)
        print(texto[:500] + "..." if len(texto) > 500 else texto)
    else:
        print("⚠️  Nenhum carro encontrado")
