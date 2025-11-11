#!/usr/bin/env python3
"""
🔍 SUB-AGENTE FAQ - Consulta informações dos imóveis

Responsabilidade:
- Recebe: imovel_id + pergunta do cliente
- Busca: base.txt + faq.txt
- Retorna: Texto resumido e relevante

NÃO contém lógica de conversação!
"""

from pathlib import Path


class SubAgenteFAQ:
    """Sub-agente especializado em consultar informações dos imóveis"""

    def __init__(self, imoveis_dir):
        self.imoveis_dir = Path(imoveis_dir)

    def consultar(self, imovel_id: str, pergunta: str = "") -> dict:
        """
        Consulta informações do imóvel

        Args:
            imovel_id: ID do imóvel (ex: chacara-itatiaiucu-001)
            pergunta: Pergunta específica (opcional)

        Returns:
            dict com:
            - sucesso: bool
            - dados: str (base + faq)
            - erro: str (se houver)
        """
        imovel_path = self.imoveis_dir / imovel_id

        # Verifica se existe
        if not imovel_path.exists():
            return {
                "sucesso": False,
                "dados": "",
                "erro": f"Imóvel {imovel_id} não encontrado"
            }

        # Lê FAQ.txt (único arquivo com TODAS as informações)
        faq_file = imovel_path / "FAQ.txt"
        if not faq_file.exists():
            return {
                "sucesso": False,
                "dados": "",
                "erro": f"Arquivo FAQ.txt não encontrado para {imovel_id}"
            }

        with open(faq_file, 'r', encoding='utf-8') as f:
            faq_txt = f.read().strip()

        # Retorna FAQ completo
        dados_completos = faq_txt

        # Se tem pergunta específica, adiciona contexto
        if pergunta:
            dados_completos = f"PERGUNTA DO CLIENTE: {pergunta}\n\n{dados_completos}"

        return {
            "sucesso": True,
            "dados": dados_completos,
            "erro": ""
        }


if __name__ == "__main__":
    # Teste rápido
    import sys
    sys.path.append(str(Path(__file__).parent.parent))

    faq = SubAgenteFAQ("imoveis")
    resultado = faq.consultar("chacara-itatiaiucu-001", "qual o valor?")

    if resultado['sucesso']:
        print("✅ Sucesso!")
        print("\n" + resultado['dados'][:500] + "...")
    else:
        print(f"❌ Erro: {resultado['erro']}")
