#!/usr/bin/env python3
"""
🔄 MIGRAÇÃO DE IMÓVEIS - Estrutura Antiga → Progressive Disclosure

Converte estrutura atual:
├── descricao.txt
├── localizacao.txt
└── faq.txt

Para nova estrutura:
├── base.txt           # 200 tokens (descrição básica + localização)
├── detalhes.txt       # 300 tokens (metragem, características técnicas)
├── faq.txt            # 500 tokens (preço, IPTU, pet - mantém arquivo)
├── legal.txt          # 300 tokens (documentação - se tiver)
└── financiamento.txt  # 400 tokens (financiamento - se tiver)
"""

import re
from pathlib import Path
from typing import Dict, Optional


class MigradorImoveis:
    """
    Migra estrutura antiga de imóveis para Progressive Disclosure
    """

    def __init__(self, imoveis_dir: Path, dry_run: bool = False):
        """
        Args:
            imoveis_dir: Diretório raiz dos imóveis
            dry_run: Se True, não salva arquivos (apenas mostra o que faria)
        """
        self.imoveis_dir = imoveis_dir
        self.dry_run = dry_run

    def migrar_todos(self):
        """
        Migra todos os imóveis do diretório
        """
        if not self.imoveis_dir.exists():
            print(f"❌ Diretório não existe: {self.imoveis_dir}")
            return

        imoveis = [d for d in self.imoveis_dir.iterdir() if d.is_dir()]

        print(f"🔄 Migrando {len(imoveis)} imóveis...")
        print(f"   Dry run: {self.dry_run}")
        print()

        for imovel_dir in imoveis:
            self.migrar_imovel(imovel_dir)

        print(f"\n✅ Migração concluída!")

    def migrar_imovel(self, imovel_dir: Path):
        """
        Migra um único imóvel

        Args:
            imovel_dir: Diretório do imóvel
        """
        imovel_id = imovel_dir.name
        print(f"📦 {imovel_id}")

        # Lê arquivos existentes
        descricao = self._ler_arquivo(imovel_dir / "descricao.txt")
        localizacao = self._ler_arquivo(imovel_dir / "localizacao.txt")
        faq = self._ler_arquivo(imovel_dir / "faq.txt")
        informacoes = self._ler_arquivo(imovel_dir / "informacoes.txt")  # Alguns imóveis podem ter

        # Se não tem nenhum conteúdo, pula
        if not any([descricao, localizacao, faq, informacoes]):
            print(f"   ⚠️  Sem conteúdo para migrar")
            return

        # Separa conteúdo por categorias
        categorizado = self._categorizar_conteudo(descricao, localizacao, faq, informacoes)

        # Cria novos arquivos
        arquivos_criados = []

        # base.txt (sempre cria)
        if categorizado["base"]:
            base_path = imovel_dir / "base.txt"
            self._salvar_arquivo(base_path, categorizado["base"])
            arquivos_criados.append("base.txt")

        # detalhes.txt (se tiver conteúdo técnico)
        if categorizado["detalhes"]:
            detalhes_path = imovel_dir / "detalhes.txt"
            self._salvar_arquivo(detalhes_path, categorizado["detalhes"])
            arquivos_criados.append("detalhes.txt")

        # faq.txt (mantém se já existe)
        if faq:
            faq_path = imovel_dir / "faq.txt"
            # Já existe, não precisa recriar
            arquivos_criados.append("faq.txt (mantido)")
        elif categorizado["faq"]:
            faq_path = imovel_dir / "faq.txt"
            self._salvar_arquivo(faq_path, categorizado["faq"])
            arquivos_criados.append("faq.txt")

        # legal.txt (se tiver info legal)
        if categorizado["legal"]:
            legal_path = imovel_dir / "legal.txt"
            self._salvar_arquivo(legal_path, categorizado["legal"])
            arquivos_criados.append("legal.txt")

        # financiamento.txt (se tiver info de financiamento)
        if categorizado["financiamento"]:
            financiamento_path = imovel_dir / "financiamento.txt"
            self._salvar_arquivo(financiamento_path, categorizado["financiamento"])
            arquivos_criados.append("financiamento.txt")

        print(f"   ✅ Criados: {', '.join(arquivos_criados)}")

    def _categorizar_conteudo(
        self,
        descricao: Optional[str],
        localizacao: Optional[str],
        faq: Optional[str],
        informacoes: Optional[str]
    ) -> Dict[str, str]:
        """
        Categoriza conteúdo nos 5 níveis do Progressive Disclosure

        Args:
            descricao: Conteúdo de descricao.txt
            localizacao: Conteúdo de localizacao.txt
            faq: Conteúdo de faq.txt
            informacoes: Conteúdo de informacoes.txt

        Returns:
            Dict com conteúdo categorizado por nível
        """
        # Junta tudo para análise
        texto_completo = "\n\n".join(filter(None, [descricao, localizacao, informacoes]))

        categorizado = {
            "base": "",
            "detalhes": "",
            "faq": "",
            "legal": "",
            "financiamento": ""
        }

        # === BASE ===
        # Descrição resumida + localização
        base_partes = []

        if descricao:
            # Pega primeiras linhas da descrição (resumo)
            linhas = descricao.strip().split('\n')
            resumo = []

            for linha in linhas[:10]:  # Primeiras 10 linhas
                linha = linha.strip()
                if linha and not linha.startswith('#'):
                    resumo.append(linha)

            if resumo:
                base_partes.append('\n'.join(resumo))

        if localizacao:
            base_partes.append(f"\n📍 LOCALIZAÇÃO\n{localizacao.strip()}")

        categorizado["base"] = '\n\n'.join(base_partes)

        # === DETALHES ===
        # Extrai informações técnicas (m², dimensões, etc)
        detalhes = self._extrair_detalhes_tecnicos(texto_completo)
        if detalhes:
            categorizado["detalhes"] = detalhes

        # === FAQ ===
        # Se já tem arquivo FAQ separado, não precisa recriar
        # Mas se tiver perguntas no texto, extrai
        if not faq:
            faq_extraido = self._extrair_faq(texto_completo)
            if faq_extraido:
                categorizado["faq"] = faq_extraido

        # === LEGAL ===
        # Extrai informações legais/documentação
        legal = self._extrair_info_legal(texto_completo)
        if legal:
            categorizado["legal"] = legal

        # === FINANCIAMENTO ===
        # Extrai informações de financiamento
        financiamento = self._extrair_info_financiamento(texto_completo)
        if financiamento:
            categorizado["financiamento"] = financiamento

        return categorizado

    def _extrair_detalhes_tecnicos(self, texto: str) -> Optional[str]:
        """Extrai detalhes técnicos (metragem, dimensões)"""
        linhas_detalhes = []

        for linha in texto.split('\n'):
            linha_lower = linha.lower()

            # Detecta linhas com info técnica
            keywords = ["m²", "m2", "metros", "área", "metragem", "dimensões", "tamanho"]

            if any(kw in linha_lower for kw in keywords):
                linhas_detalhes.append(linha.strip())

        if linhas_detalhes:
            return "📐 DETALHES TÉCNICOS\n\n" + '\n'.join(linhas_detalhes)

        return None

    def _extrair_faq(self, texto: str) -> Optional[str]:
        """Extrai perguntas e respostas do texto"""
        # Procura por padrões de FAQ
        linhas = texto.split('\n')
        faq_linhas = []
        capturando = False

        for linha in linhas:
            linha_limpa = linha.strip()

            # Detecta início de seção FAQ
            if any(x in linha_limpa.lower() for x in ["faq", "perguntas", "frequentes", "dúvidas"]):
                capturando = True
                faq_linhas.append(linha_limpa)
                continue

            # Detecta pergunta (linha com ?)
            if '?' in linha_limpa or linha_limpa.endswith(':'):
                capturando = True
                faq_linhas.append(linha_limpa)
                continue

            # Se está capturando, adiciona linha
            if capturando and linha_limpa:
                faq_linhas.append(linha_limpa)

        if faq_linhas:
            return '\n'.join(faq_linhas)

        return None

    def _extrair_info_legal(self, texto: str) -> Optional[str]:
        """Extrai informações legais/documentação"""
        linhas_legal = []

        for linha in texto.split('\n'):
            linha_lower = linha.lower()

            keywords = ["documentação", "escritura", "certidão", "registro", "regularizado", "documentos"]

            if any(kw in linha_lower for kw in keywords):
                linhas_legal.append(linha.strip())

        if linhas_legal:
            return "📄 DOCUMENTAÇÃO\n\n" + '\n'.join(linhas_legal)

        return None

    def _extrair_info_financiamento(self, texto: str) -> Optional[str]:
        """Extrai informações de financiamento"""
        linhas_financ = []

        for linha in texto.split('\n'):
            linha_lower = linha.lower()

            keywords = ["financiamento", "banco", "parcela", "fgts", "entrada", "financiar"]

            if any(kw in linha_lower for kw in keywords):
                linhas_financ.append(linha.strip())

        if linhas_financ:
            return "💰 FINANCIAMENTO\n\n" + '\n'.join(linhas_financ)

        return None

    def _ler_arquivo(self, path: Path) -> Optional[str]:
        """Lê arquivo de texto"""
        if not path.exists():
            return None

        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            print(f"   ⚠️  Erro ao ler {path.name}: {e}")
            return None

    def _salvar_arquivo(self, path: Path, conteudo: str):
        """Salva arquivo (ou mostra conteúdo se dry_run)"""
        if self.dry_run:
            print(f"\n   [DRY RUN] Criaria {path.name}:")
            print(f"   {conteudo[:100]}...")
            return

        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(conteudo)
        except Exception as e:
            print(f"   ❌ Erro ao salvar {path.name}: {e}")


def main():
    """
    Executa migração
    """
    import sys

    print("🔄 MIGRADOR DE IMÓVEIS - Progressive Disclosure")
    print("=" * 60)

    # Detecta diretório de imóveis
    script_dir = Path(__file__).parent
    imoveis_dir = script_dir.parent.parent / "imoveis"

    if not imoveis_dir.exists():
        print(f"❌ Diretório não encontrado: {imoveis_dir}")
        sys.exit(1)

    print(f"📁 Diretório: {imoveis_dir}")
    print()

    # Pergunta confirmação
    resposta = input("Deseja fazer migração? (s/N/dry-run): ").lower().strip()

    if resposta == 'dry-run':
        print("\n🔍 Modo DRY RUN (não salva arquivos)")
        migrador = MigradorImoveis(imoveis_dir, dry_run=True)
        migrador.migrar_todos()

    elif resposta == 's':
        print("\n✅ Iniciando migração REAL...")
        migrador = MigradorImoveis(imoveis_dir, dry_run=False)
        migrador.migrar_todos()

    else:
        print("\n❌ Migração cancelada")


if __name__ == "__main__":
    main()
