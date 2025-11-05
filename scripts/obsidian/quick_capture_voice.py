#!/usr/bin/env python3
"""
🎤 Captura Rápida por Voz → Obsidian
Grava áudio, transcreve e organiza automaticamente
"""

import sys
import os
import argparse
from datetime import datetime
from pathlib import Path
import pytz

# Adicionar paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'config'))

from obsidian_config import OBSIDIAN_VAULT_PATH, FOLDERS, ensure_folder_exists


class VoiceQuickCapture:
    def __init__(self):
        self.vault_path = OBSIDIAN_VAULT_PATH
        self.tz_br = pytz.timezone('America/Sao_Paulo')

    def capture_from_audio(self, audio_path: str) -> str:
        """
        Processa áudio → transcrição → nota organizada

        Fluxo:
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │  Áudio   │ ─> │Transcrição─> │ Obsidian │
        └──────────┘    └──────────┘    └──────────┘
        """
        print("🎤 Transcrevendo áudio...")

        # 1. Transcrever com Whisper
        transcription = self._transcribe(audio_path)
        print(f"✅ Transcrição: {transcription[:100]}...")

        # 2. Processar como texto
        return self.capture_from_text(transcription, source="voz")

    def capture_from_text(self, text: str, source: str = "texto") -> str:
        """
        Processa texto → classificação → formatação → Obsidian
        """
        print("🧠 Identificando tipo...")

        # 1. Classificar
        tipo = self._classify(text)
        print(f"✅ Tipo: {tipo.upper()}")

        # 2. Extrair metadados
        metadata = self._extract_metadata(text, tipo, source)

        # 3. Formatar visual
        content = self._format_visual(text, tipo, metadata)

        # 4. Determinar path
        folder_key, filename = self._get_path(tipo, metadata)

        # 5. Criar nota no Obsidian
        folder_path = ensure_folder_exists(folder_key)
        filepath = folder_path / filename

        print(f"💾 Salvando em: {filepath.relative_to(Path.home())}")
        filepath.write_text(content, encoding='utf-8')

        print(f"\n✅ Capturado com sucesso!")
        print(f"📂 Local: {filepath.relative_to(Path.home())}")
        print(f"🔷 Tipo: {tipo.title()}")

        return str(filepath)

    def _transcribe(self, audio_path: str) -> str:
        """Transcreve áudio usando Whisper"""
        import whisper

        # Carregar modelo
        model = whisper.load_model("base")

        # Transcrever
        result = model.transcribe(audio_path, language="pt")

        return result["text"].strip()

    def _classify(self, text: str) -> str:
        """Classifica tipo usando heurísticas"""
        text_lower = text.lower()

        # Pontuações
        scores = {
            'tarefa': 0,
            'ideia': 0,
            'projeto': 0,
            'nota': 0
        }

        # TAREFA
        task_patterns = [
            'preciso', 'fazer', 'criar', 'enviar', 'ligar', 'comprar',
            'agendar', 'lembrar', 'não esquecer', 'urgente', 'deadline'
        ]
        scores['tarefa'] = sum(1 for p in task_patterns if p in text_lower)

        # IDEIA
        idea_patterns = [
            'e se', 'poderia', 'seria legal', 'imagine', 'talvez',
            'poderíamos', 'ideia', 'insight'
        ]
        scores['ideia'] = sum(1 for p in idea_patterns if p in text_lower)

        # PROJETO
        project_patterns = [
            'sistema', 'plataforma', 'desenvolver', 'implementar',
            'projeto', 'múltiplas', 'componentes', 'fases'
        ]
        scores['projeto'] = sum(1 for p in project_patterns if p in text_lower)

        # NOTA
        note_patterns = [
            'aprendi', 'descobri', 'interessante', 'http',
            'artigo', 'referência', 'estudo'
        ]
        scores['nota'] = sum(1 for p in note_patterns if p in text_lower)

        # Retornar maior score (ou 'nota' como default)
        return max(scores, key=scores.get) or 'nota'

    def _extract_metadata(self, text: str, tipo: str, source: str) -> dict:
        """Extrai metadados contextuais"""
        now = datetime.now(self.tz_br)

        metadata = {
            'timestamp': now.strftime('%Y-%m-%d %H:%M BR'),
            'tipo': tipo.title(),
            'source': '🎤' if source == 'voz' else '⌨️'
        }

        # Extras por tipo
        if tipo == 'tarefa':
            metadata['status'] = 'Pendente'
            metadata['prioridade'] = self._detect_priority(text)
        elif tipo == 'ideia':
            metadata['status'] = 'Pendente'
            metadata['potencial'] = 'Médio'
        elif tipo == 'projeto':
            metadata['status'] = 'Planejamento'

        return metadata

    def _detect_priority(self, text: str) -> str:
        """Detecta prioridade da tarefa"""
        text_lower = text.lower()

        if any(p in text_lower for p in ['urgente', 'imediato', 'agora']):
            return 'Alta ⚠️'
        elif any(p in text_lower for p in ['importante', 'prioridade']):
            return 'Média'
        else:
            return 'Baixa'

    def _format_visual(self, raw: str, tipo: str, meta: dict) -> str:
        """Gera formato visual com ASCII diagrams"""

        # Título limpo (primeiras 5-10 palavras)
        words = raw.split()
        title = ' '.join(words[:8])
        if len(words) > 8:
            title += '...'

        # Emoji por tipo
        emojis = {
            'tarefa': '📋',
            'ideia': '💡',
            'projeto': '📂',
            'nota': '📝'
        }
        emoji = emojis[tipo]

        # Template base
        content = f"""# {emoji} {title.title()}

**Tipo:** {meta['tipo']}
**Capturado:** {meta['timestamp']} {meta['source']}
**Status:** {meta.get('status', 'Pendente')}
"""

        # Adicionar extras por tipo
        if tipo == 'tarefa':
            content += f"**Prioridade:** {meta['prioridade']}\n"

        content += "\n---\n\n"

        # Diagrama visual
        content += "## 🎯 Resumo Visual\n\n```\n"
        content += self._generate_diagram(raw, tipo)
        content += "\n```\n\n---\n\n"

        # Conteúdo original
        content += "## 📝 Detalhes\n\n"
        content += f"**Captura original:**\n> {raw}\n\n"

        # Próximos passos
        content += "---\n\n## ✅ Próximos Passos\n\n"
        content += "- [ ] Revisar e refinar\n"
        content += "- [ ] Definir ações\n"

        return content

    def _generate_diagram(self, text: str, tipo: str) -> str:
        """Gera diagrama ASCII simples"""
        # Título do box central
        title = tipo.upper()
        width = max(len(title) + 4, 20)
        border = "─" * (width - 2)

        diagram = f"""┌{border}┐
│ {title.center(width-2)} │
└{'─' * (width - 2)}┘"""

        return diagram

    def _get_path(self, tipo: str, meta: dict) -> tuple:
        """Determina path no Obsidian"""
        # Mapear tipo para folder key
        folder_map = {
            'tarefa': 'inbox',
            'ideia': 'ideas',
            'projeto': 'projects',
            'nota': 'knowledge'
        }

        folder_key = folder_map.get(tipo, 'inbox')

        # Nome do arquivo (timestamp)
        now = datetime.now(self.tz_br)
        filename = now.strftime('%Y%m%d_%H%M%S') + '.md'

        return folder_key, filename


def main():
    parser = argparse.ArgumentParser(
        description='🎤 Captura rápida por voz → Obsidian'
    )

    parser.add_argument(
        '--audio',
        type=str,
        help='Path para arquivo de áudio (mp3, m4a, wav)'
    )

    parser.add_argument(
        '--text',
        type=str,
        help='Texto direto (sem áudio)'
    )

    args = parser.parse_args()

    capturer = VoiceQuickCapture()

    if args.audio:
        if not os.path.exists(args.audio):
            print(f"❌ Arquivo não encontrado: {args.audio}")
            sys.exit(1)

        capturer.capture_from_audio(args.audio)

    elif args.text:
        capturer.capture_from_text(args.text)

    else:
        print("❌ Forneça --audio ou --text")
        print("\nExemplos:")
        print("  python3 quick_capture_voice.py --audio nota.mp3")
        print("  python3 quick_capture_voice.py --text 'minha ideia'")
        sys.exit(1)


if __name__ == '__main__':
    main()
