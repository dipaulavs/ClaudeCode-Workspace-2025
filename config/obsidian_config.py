"""
Configuração para integração com Obsidian via acesso direto ao filesystem
"""

from pathlib import Path

# ============================================
# CONFIGURAÇÃO DO VAULT
# ============================================

# Caminho do vault (acesso direto ao filesystem)
OBSIDIAN_VAULT_PATH = Path("/Users/felipemdepaula/Documents/Obsidian/Claude-code-ios")

# ============================================
# ESTRUTURA DE PASTAS
# ============================================

FOLDERS = {
    "inbox": "00 - Inbox",
    "projects": "01 - Projetos",
    "ideas": "02 - Ideias",
    "knowledge": "03 - Conhecimento",
    "automations": "04 - Automações",
    "templates": "05 - Templates",
    "daily": "06 - Daily Notes",
    "resources": "07 - Recursos",
    "youtube": "09 - YouTube Knowledge",
    "youtube_videos": "09 - YouTube Knowledge/Videos",
    "youtube_transcricoes": "09 - YouTube Knowledge/Transcricoes",
    # Nova estrutura organizada para vídeos
    "videos": "📺 Vídeos",
    "videos_canvas": "📺 Vídeos/.canvas",
    "videos_assets": "📺 Vídeos/.assets"
}

# Estrutura de tipos de vídeos (classificação automática por IA)
VIDEO_TYPES = {
    "tutorial": "Tutoriais",          # Passo a passo prático
    "metodologia": "Metodologias",    # Frameworks, processos
    "aula": "Aulas",                  # Conteúdo educacional teórico
    "noticia": "Noticias",            # Novidades, lançamentos
    "review": "Reviews",              # Análises de ferramentas/produtos
    "outros": "Outros"                # Não se encaixa nas categorias
}

# ============================================
# CONFIGURAÇÕES DE DAILY NOTES
# ============================================

# Formato de data para daily notes (nome do arquivo - compatibilidade Obsidian)
DAILY_NOTE_FORMAT = "%Y-%m-%d"  # Ex: 2025-11-02

# Formato de data para exibição (padrão brasileiro)
DISPLAY_DATE_FORMAT = "%d/%m/%Y"  # Ex: 02/11/2025

# ============================================
# FUNÇÕES AUXILIARES
# ============================================

def get_folder_path(folder_key: str) -> Path:
    """Retorna caminho completo de uma pasta"""
    folder_name = FOLDERS.get(folder_key, folder_key)
    return OBSIDIAN_VAULT_PATH / folder_name

def ensure_folder_exists(folder_key: str) -> Path:
    """Garante que a pasta existe, criando se necessário"""
    folder_path = get_folder_path(folder_key)
    folder_path.mkdir(parents=True, exist_ok=True)
    return folder_path
