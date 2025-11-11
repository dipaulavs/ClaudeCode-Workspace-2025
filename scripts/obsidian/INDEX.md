# 📚 SCRIPTS/obsidian - INDEX

Scripts para integração e automação do Obsidian vault.

## 🔄 Sincronização e Organização

### sync_kanban_status.py
**Função:** Sincroniza status das tarefas entre Kanban e frontmatter
**Uso:** `python3 sync_kanban_status.py`
**Quando:** Após criar/mover tarefas no Kanban
**Mapeia:**
- 📥 A Fazer → `status: aberta`
- 🔨 Em Andamento → `status: em_andamento`
- ✅ Concluído → `status: concluída`

### watch_kanban.sh
**Função:** Monitora Kanban e sincroniza automaticamente ao detectar mudanças
**Uso:** `./watch_kanban.sh` (manter rodando em terminal separado)
**Requer:** `fswatch` (instalar: `brew install fswatch`)
**Benefit:** Sincronização automática em tempo real

### organize_loose_notes.py
**Função:** Organiza notas soltas na raiz do vault
**Uso:** `python3 organize_loose_notes.py`
**Detecta:** Tipo de conteúdo e move para pasta correta

## 📝 Captura Rápida

### quick_note.py
**Função:** Cria anotação rápida no Obsidian
**Uso:** `python3 quick_note.py "Título" "Conteúdo"`
**Local:** `💡 Anotações/`

### adicionar_tarefa.py
**Função:** Cria tarefa e adiciona ao Kanban automaticamente
**Uso:** `python3 adicionar_tarefa.py "Título da Tarefa"`
**Local:** `📋 Tarefas/` + Kanban

### capture_idea.py
**Função:** Captura rápida de ideias
**Uso:** `python3 capture_idea.py "Minha ideia"`
**Local:** `💡 Anotações/`

### quick_capture_voice.py
**Função:** Captura de voz para texto → Obsidian
**Uso:** `python3 quick_capture_voice.py`
**Requer:** Whisper API configurado

## 📺 YouTube

### add_youtube_video.py
**Função:** Adiciona vídeo YouTube com transcrição e Canvas
**Uso:** `python3 add_youtube_video.py "https://youtube.com/..."`
**Local:** `📺 Vídeos/`

### youtube_classifier.py
**Função:** Classifica vídeos por categoria
**Uso:** `python3 youtube_classifier.py "URL"`
**Categorias:** notícia, tutorial, curso, aula, review

## 📅 Daily Notes

### create_daily.py
**Função:** Cria nota diária estruturada
**Uso:** `python3 create_daily.py`
**Local:** `📅 Daily/`

## 🔧 Gerenciamento

### manage_tasks.py
**Função:** Gerencia tarefas (criar, listar, concluir)
**Uso:** `python3 manage_tasks.py [comando]`
**Comandos:** list, create, complete, delete

### new_project.py
**Função:** Cria estrutura de novo projeto
**Uso:** `python3 new_project.py "Nome do Projeto"`
**Local:** `📂 Projetos/`

### process_note.py
**Função:** Processa nota com IA (categoriza, formata)
**Uso:** `python3 process_note.py "caminho/nota.md"`

## 🔗 Integração Claude

### claude_from_obsidian.sh
**Função:** Envia nota para Claude Code processar
**Uso:** `./claude_from_obsidian.sh "nota.md"`

### send_to_claude.sh
**Função:** Envia conteúdo para Claude via API
**Uso:** `./send_to_claude.sh "Meu texto"`

### webhook_listener.py
**Função:** Servidor webhook para receber capturas
**Uso:** `python3 webhook_listener.py`
**Porta:** 8765

### start_webhook_server.sh
**Função:** Inicia servidor webhook em background
**Uso:** `./start_webhook_server.sh`

## 🛠️ Utilitários

### obsidian_client.py
**Função:** Cliente Python para interagir com vault
**Uso:** Import em outros scripts
**Classes:** `ObsidianVault`, `Note`, `Task`

### open_note_in_vscode.sh
**Função:** Abre nota no VSCode
**Uso:** `./open_note_in_vscode.sh "nota.md"`

### quick_command.sh
**Função:** Executa comando rápido no Obsidian
**Uso:** `./quick_command.sh [comando]`

## 📖 Documentação

### README.md
**Descrição:** Documentação geral dos scripts Obsidian

### README_QUICK_CAPTURE.md
**Descrição:** Guia sistema de captura rápida

---

**Total:** 21 scripts
**Última atualização:** 11/11/2025
