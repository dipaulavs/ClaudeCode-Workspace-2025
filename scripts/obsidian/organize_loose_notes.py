#!/usr/bin/env python3
"""
Organiza notas soltas do Obsidian
Identifica tipo, formata visualmente e move para pasta correta
"""

import sys
from pathlib import Path
from datetime import datetime
import re

# Adicionar path do config
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'config'))

from obsidian_config import OBSIDIAN_VAULT_PATH, FOLDERS, ensure_folder_exists


class NoteOrganizer:
    """Organiza notas soltas automaticamente"""

    def __init__(self):
        self.vault_path = OBSIDIAN_VAULT_PATH

    def identify_type(self, content):
        """
        Identifica tipo da nota por conteúdo

        Returns:
            tuple: (tipo, pasta_destino, emoji)
        """
        content_lower = content.lower()

        # Palavras-chave por tipo
        keywords = {
            "tarefa": {
                "words": ["fazer", "lembrar", "deadline", "urgente", "tarefa", "fazer:",
                         "todo", "preciso", "devo", "tenho que"],
                "folder": "inbox",
                "emoji": "📋"
            },
            "ideia": {
                "words": ["ideia", "conceito", "insight", "possibilidade", "poderia",
                         "talvez", "pensei", "que tal", "e se"],
                "folder": "ideas",
                "emoji": "💡"
            },
            "projeto": {
                "words": ["projeto", "etapas", "fases", "implementar", "desenvolver",
                         "plano", "roadmap", "milestone"],
                "folder": "projects",
                "emoji": "📂"
            }
        }

        # Contar matches por tipo
        scores = {}
        for note_type, config in keywords.items():
            score = sum(1 for word in config["words"] if word in content_lower)
            scores[note_type] = score

        # Se tem matches, retornar maior score
        if max(scores.values()) > 0:
            best_type = max(scores, key=scores.get)
            config = keywords[best_type]
            return best_type.capitalize(), config["folder"], config["emoji"]

        # Default: nota de conhecimento
        return "Nota", "knowledge", "📝"

    def format_visual(self, title, content, note_type, emoji):
        """
        Formata nota com template visual ASCII

        Args:
            title: Título da nota
            content: Conteúdo original
            note_type: Tipo identificado
            emoji: Emoji do tipo

        Returns:
            str: Nota formatada
        """
        now = datetime.now()
        date_br = now.strftime("%d/%m/%Y")
        time_br = now.strftime("%H:%M")

        # Status baseado no tipo
        status_map = {
            "Tarefa": "Pendente",
            "Ideia": "Em Análise",
            "Projeto": "Planejamento",
            "Nota": "Arquivado"
        }
        status = status_map.get(note_type, "Pendente")

        # Criar diagrama ASCII baseado no tipo
        if note_type == "Tarefa":
            diagram = """┌─────────────┐
│   CAPTURA   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  ANÁLISE    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   AÇÃO ⚡   │
└─────────────┘"""
        elif note_type == "Ideia":
            diagram = """┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   INSIGHT   │ → │  VALIDAR    │ → │  EXECUTAR   │
└─────────────┘    └─────────────┘    └─────────────┘"""
        elif note_type == "Projeto":
            diagram = """┌─────────────┐
│ PLANEJAR 📋 │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ EXECUTAR ⚙️  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ CONCLUIR ✅ │
└─────────────┘"""
        else:  # Nota
            diagram = """┌─────────────┐
│  CONTEÚDO   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ CONHECIMENTO│
└─────────────┘"""

        # Extrair possíveis próximos passos do conteúdo
        lines = content.split('\n')
        next_steps = []
        for line in lines:
            # Procurar por linhas que parecem ações
            if any(word in line.lower() for word in ['fazer', 'criar', 'implementar', 'testar', 'validar']):
                next_steps.append(f"- [ ] {line.strip('- ').strip()}")

        if not next_steps:
            next_steps = ["- [ ] Revisar conteúdo", "- [ ] Definir próximos passos"]

        # Montar nota formatada
        formatted = f"""# {emoji} {title}

**Tipo:** {note_type}
**Capturado:** {date_br} {time_br}
**Status:** {status}

---

## 🎯 Resumo Visual

{diagram}

---

## 📝 Conteúdo Original

{content.strip()}

---

## ✅ Próximos Passos

{chr(10).join(next_steps[:5])}

---

_Organizado automaticamente por obsidian-quick-capture_
"""

        return formatted

    def list_loose_notes(self):
        """
        Lista notas soltas (inbox ou raiz)

        Returns:
            list: Lista de paths de notas
        """
        try:
            inbox_folder = self.vault_path / FOLDERS["inbox"]

            loose_notes = []

            # Notas no inbox
            if inbox_folder.exists():
                for note_file in inbox_folder.glob("*.md"):
                    # Ignorar templates e daily notes
                    if not any(skip in note_file.name for skip in ["Template", "Daily"]):
                        loose_notes.append(note_file)

            # Notas na raiz do vault
            for note_file in self.vault_path.glob("*.md"):
                # Ignorar templates e daily notes
                if not any(skip in note_file.name for skip in ["Template", "Daily"]):
                    loose_notes.append(note_file)

            return loose_notes

        except Exception as e:
            print(f"❌ Erro ao listar notas: {e}")
            return []

    def organize_note(self, note_path: Path):
        """
        Organiza uma nota específica

        Args:
            note_path: Path da nota a organizar

        Returns:
            dict: Resultado da organização
        """
        try:
            # Ler nota
            content = note_path.read_text(encoding='utf-8')

            if not content or len(content.strip()) < 10:
                return {"status": "skipped", "reason": "Conteúdo muito curto"}

            # Extrair título (primeira linha com # ou nome do arquivo)
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip()
                # Remover título do conteúdo
                content = re.sub(r'^#\s+.+$', '', content, count=1, flags=re.MULTILINE).strip()
            else:
                title = note_path.stem

            # Identificar tipo
            note_type, dest_folder_key, emoji = self.identify_type(content)

            # Formatar visualmente
            formatted_content = self.format_visual(title, content, note_type, emoji)

            # Gerar novo nome de arquivo
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            new_filename = f"{title[:50]} - {timestamp}.md"  # Limitar tamanho

            # Criar nota organizada na pasta correta
            dest_folder = ensure_folder_exists(dest_folder_key)
            dest_path = dest_folder / new_filename
            dest_path.write_text(formatted_content, encoding='utf-8')

            # Deletar nota original (apenas se não for a mesma pasta)
            if note_path.parent != dest_folder:
                note_path.unlink()

            return {
                "status": "success",
                "original": str(note_path),
                "new_path": str(dest_path),
                "type": note_type,
                "emoji": emoji
            }

        except Exception as e:
            return {
                "status": "error",
                "note": str(note_path),
                "error": str(e)
            }

    def organize_all(self):
        """
        Organiza todas as notas soltas

        Returns:
            dict: Estatísticas da organização
        """
        print("🔍 Buscando notas soltas...")
        loose_notes = self.list_loose_notes()

        if not loose_notes:
            print("✅ Nenhuma nota solta encontrada!")
            return {"total": 0, "organized": 0}

        print(f"\n📋 Encontradas {len(loose_notes)} nota(s) solta(s)\n")

        results = []
        for note_path in loose_notes:
            print(f"📝 Organizando: {note_path.name}")
            result = self.organize_note(note_path)
            results.append(result)

            if result["status"] == "success":
                print(f"   ✅ {result['emoji']} Tipo: {result['type']}")
                print(f"   📍 Destino: {Path(result['new_path']).relative_to(Path.home())}\n")
            elif result["status"] == "skipped":
                print(f"   ⏭️  Pulado: {result['reason']}\n")
            else:
                print(f"   ❌ Erro: {result.get('error', 'Desconhecido')}\n")

        # Estatísticas
        organized = sum(1 for r in results if r["status"] == "success")

        print("=" * 60)
        print(f"✅ Organização concluída!")
        print(f"   Total: {len(loose_notes)} | Organizadas: {organized}")
        print("=" * 60)

        return {
            "total": len(loose_notes),
            "organized": organized,
            "results": results
        }


def main():
    """Função principal"""
    organizer = NoteOrganizer()

    print("✅ Pronto para organizar notas!\n")

    # Organizar todas
    organizer.organize_all()

    return 0


if __name__ == "__main__":
    sys.exit(main())
