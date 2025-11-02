"""
Utilitário para carregar arquivos .md como instruções de agentes CrewAI
"""
import os
from pathlib import Path
from typing import Optional


class MDLoader:
    """
    Carrega arquivos markdown (.md) e os converte em instruções para agentes CrewAI
    """

    def __init__(self, base_path: Optional[str] = None):
        """
        Args:
            base_path: Caminho base para buscar arquivos .md
                      Se None, usa a pasta 'agentes' do workspace
        """
        if base_path is None:
            # Pega o caminho do workspace (2 níveis acima)
            current_dir = Path(__file__).parent.parent.parent
            self.base_path = current_dir / "agentes"
        else:
            self.base_path = Path(base_path)

    def load_md(self, file_path: str) -> str:
        """
        Carrega o conteúdo de um arquivo .md

        Args:
            file_path: Caminho relativo ao base_path ou caminho absoluto

        Returns:
            Conteúdo do arquivo como string

        Raises:
            FileNotFoundError: Se o arquivo não existir
        """
        # Tenta primeiro como caminho absoluto
        full_path = Path(file_path)

        # Se não for absoluto, concatena com base_path
        if not full_path.is_absolute():
            full_path = self.base_path / file_path

        if not full_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {full_path}")

        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return content

    def load_agent_instructions(self, agent_folder: str, file_name: str = "SKILL.md") -> str:
        """
        Carrega instruções de um agente específico

        Args:
            agent_folder: Nome da pasta do agente (ex: "ganchos-hormozi")
            file_name: Nome do arquivo (padrão: "SKILL.md")

        Returns:
            Conteúdo do arquivo como string
        """
        file_path = f"{agent_folder}/{file_name}"
        return self.load_md(file_path)

    def load_multiple_files(self, file_paths: list[str], separator: str = "\n\n---\n\n") -> str:
        """
        Carrega múltiplos arquivos .md e os concatena

        Args:
            file_paths: Lista de caminhos de arquivos
            separator: Separador entre arquivos (padrão: linha horizontal markdown)

        Returns:
            Conteúdo concatenado de todos os arquivos
        """
        contents = []

        for file_path in file_paths:
            try:
                content = self.load_md(file_path)
                contents.append(content)
            except FileNotFoundError as e:
                print(f"⚠️  Aviso: {e}")
                continue

        return separator.join(contents)

    def list_available_agents(self) -> list[str]:
        """
        Lista todas as pastas de agentes disponíveis

        Returns:
            Lista com nomes das pastas de agentes
        """
        if not self.base_path.exists():
            return []

        # Pega apenas diretórios
        agents = [
            d.name for d in self.base_path.iterdir()
            if d.is_dir() and not d.name.startswith('.')
        ]

        return sorted(agents)

    def get_agent_files(self, agent_folder: str) -> list[str]:
        """
        Lista todos os arquivos .md de um agente

        Args:
            agent_folder: Nome da pasta do agente

        Returns:
            Lista com nomes dos arquivos .md
        """
        agent_path = self.base_path / agent_folder

        if not agent_path.exists():
            return []

        # Pega apenas arquivos .md
        md_files = [
            f.name for f in agent_path.iterdir()
            if f.is_file() and f.suffix == '.md'
        ]

        return sorted(md_files)


# Função auxiliar para uso rápido
def load_agent_md(agent_folder: str, file_name: str = "SKILL.md") -> str:
    """
    Atalho para carregar instruções de um agente

    Exemplo:
        instructions = load_agent_md("ganchos-hormozi", "SKILL.md")
    """
    loader = MDLoader()
    return loader.load_agent_instructions(agent_folder, file_name)


# Exemplo de uso
if __name__ == "__main__":
    loader = MDLoader()

    print("🤖 Agentes disponíveis:")
    agents = loader.list_available_agents()
    for agent in agents:
        print(f"   - {agent}")
        files = loader.get_agent_files(agent)
        for file in files:
            print(f"      └─ {file}")

    print("\n📄 Carregando exemplo (ganchos-hormozi):")
    try:
        content = loader.load_agent_instructions("ganchos-hormozi")
        print(f"✅ Carregado! {len(content)} caracteres")
        print(f"Primeiras 200 chars:\n{content[:200]}...")
    except FileNotFoundError as e:
        print(f"❌ Erro: {e}")
