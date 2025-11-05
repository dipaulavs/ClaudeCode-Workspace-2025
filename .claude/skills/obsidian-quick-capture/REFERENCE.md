# obsidian-quick-capture - Referência Técnica

## 🏗️ Arquitetura

```
┌─────────────────────┐
│ Input (bagunçado)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Analisador NLP      │ → Extrai: entidades, ações, contexto
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Classificador Tipo  │ → Regras + Heurísticas
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Formatador Visual   │ → Templates ASCII + Markdown
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ MCP Filesystem      │ → Write() direto no vault
└─────────────────────┘
```

## 🧠 Regras de Classificação

### 1. Tarefa

**Gatilhos:**
- Verbos de ação: fazer, criar, enviar, ligar, comprar, agendar
- Deadline/prazo: "até amanhã", "essa semana", "urgente"
- Lembrete: "lembrar de", "não esquecer"

**Formato:**
```markdown
# 📋 [AÇÃO]

**Tipo:** Tarefa
**Capturado:** 2025-11-05 10:30 BR
**Status:** Pendente
**Prioridade:** [Alta|Média|Baixa]
**Deadline:** [Se houver]

---

## 🎯 Resumo Visual

┌─────────────┐
│   AÇÃO      │
│   PRINCIPAL │
└──────┬──────┘
       │
       ├─> Sub-tarefa 1
       ├─> Sub-tarefa 2
       └─> Sub-tarefa 3

---

## 📝 Detalhes

[Contexto original preservado]

---

## ✅ Checklist

- [ ] Tarefa 1
- [ ] Tarefa 2
```

### 2. Ideia

**Gatilhos:**
- Conceitos: "poderia", "seria legal", "imagine"
- Criatividade: "e se", "talvez", "poderíamos"
- Insight: "percebi que", "descobri"

**Formato:**
```markdown
# 💡 [CONCEITO PRINCIPAL]

**Tipo:** Ideia
**Capturado:** 2025-11-05 10:30 BR
**Status:** Pendente
**Potencial:** [Alto|Médio|Baixo]

---

## 🎯 Resumo Visual

       IDEIA CENTRAL
            │
    ┌───────┼───────┐
    │       │       │
 Aspecto1 Aspecto2 Aspecto3

---

## 📝 Descrição

[Ideia original expandida]

---

## 🚀 Próximos Passos

- [ ] Validar viabilidade
- [ ] Pesquisar similares
- [ ] Prototipar
```

### 3. Projeto

**Gatilhos:**
- Complexidade: múltiplas etapas, "sistema", "plataforma"
- Escopo: "preciso criar", "desenvolver", "implementar"
- Duração: "longo prazo", "meses"

**Formato:**
```markdown
# 📂 [NOME DO PROJETO]

**Tipo:** Projeto
**Capturado:** 2025-11-05 10:30 BR
**Status:** Planejamento
**Duração Estimada:** [Horas/Dias/Semanas]

---

## 🎯 Visão Geral

┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   FASE 1    │ ─> │   FASE 2    │ ─> │   FASE 3    │
└─────────────┘    └─────────────┘    └─────────────┘

---

## 📝 Escopo

[Objetivo e contexto]

---

## 🗓️ Roadmap

- [ ] Etapa 1
- [ ] Etapa 2
- [ ] Etapa 3

---

## 🔗 Recursos

- Link 1
- Link 2
```

### 4. Nota

**Gatilhos:**
- Informação: "aprendi que", "descobri", "interessante"
- Referência: URL, citação, fonte
- Conhecimento: conceito técnico, definição

**Formato:**
```markdown
# 📝 [ASSUNTO]

**Tipo:** Nota
**Capturado:** 2025-11-05 10:30 BR
**Categoria:** [Técnico|Pessoal|Trabalho|...]

---

## 🎯 Resumo Visual

┌─────────────────────┐
│  CONCEITO PRINCIPAL │
└──────────┬──────────┘
           │
     ┌─────┼─────┐
     │     │     │
  Ponto1 Ponto2 Ponto3

---

## 📝 Conteúdo

[Informação organizada]

---

## 🔗 Referências

- Fonte 1
- Fonte 2
```

## 📁 Estrutura Obsidian

**Vault Base:** `/Users/felipemdepaula/Library/Mobile Documents/iCloud~md~obsidian/Documents/Claude-code-ios`

```
Claude-code-ios/
├── 📥 INBOX/              → Entrada (processamento)
│   └── [timestamp].md
│
├── 📋 TAREFAS/            → Tarefas organizadas
│   ├── urgente/
│   ├── hoje/
│   └── semana/
│
├── 💡 IDEIAS/             → Ideias processadas
│   ├── validadas/
│   └── explorando/
│
├── 📂 PROJETOS/           → Projetos ativos
│   ├── em-andamento/
│   └── backlog/
│
└── 📝 NOTAS/              → Referências
    ├── tecnico/
    ├── pessoal/
    └── trabalho/
```

## 🔧 Integração com MCP Filesystem

```python
from datetime import datetime
import pytz

VAULT_PATH = "/Users/felipemdepaula/Library/Mobile Documents/iCloud~md~obsidian/Documents/Claude-code-ios"

class QuickCapture:
    def __init__(self):
        self.vault_path = VAULT_PATH
        self.tz_br = pytz.timezone('America/Sao_Paulo')

    def capture(self, raw_input: str):
        # 1. Classificar tipo
        tipo = self._classify(raw_input)

        # 2. Extrair metadados
        metadata = self._extract_metadata(raw_input, tipo)

        # 3. Formatar visual
        content = self._format_visual(raw_input, tipo, metadata)

        # 4. Determinar path
        relative_path = self._get_path(tipo, metadata)
        full_path = f"{self.vault_path}/{relative_path}"

        # 5. Criar nota usando Write tool
        Write(file_path=full_path, content=content)

        return relative_path

    def _classify(self, text: str) -> str:
        """Classifica tipo usando heurísticas"""
        text_lower = text.lower()

        # Tarefa
        task_verbs = ['fazer', 'criar', 'enviar', 'ligar', 'comprar', 'agendar']
        task_keywords = ['lembrar', 'não esquecer', 'urgente', 'deadline']

        # Ideia
        idea_keywords = ['poderia', 'seria legal', 'imagine', 'e se', 'talvez']

        # Projeto
        project_keywords = ['sistema', 'plataforma', 'desenvolver', 'implementar']

        # Nota
        note_keywords = ['aprendi', 'descobri', 'interessante', 'http']

        # Pontuação
        scores = {
            'tarefa': sum(1 for v in task_verbs if v in text_lower) +
                     sum(1 for k in task_keywords if k in text_lower),
            'ideia': sum(1 for k in idea_keywords if k in text_lower),
            'projeto': sum(1 for k in project_keywords if k in text_lower),
            'nota': sum(1 for k in note_keywords if k in text_lower)
        }

        return max(scores, key=scores.get) or 'nota'

    def _extract_metadata(self, text: str, tipo: str) -> dict:
        """Extrai metadados contextuais"""
        now = datetime.now(self.tz_br)

        metadata = {
            'timestamp': now.strftime('%Y-%m-%d %H:%M BR'),
            'tipo': tipo.title()
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

    def _format_visual(self, raw: str, tipo: str, meta: dict) -> str:
        """Gera formato visual com ASCII diagrams"""
        templates = {
            'tarefa': self._template_tarefa,
            'ideia': self._template_ideia,
            'projeto': self._template_projeto,
            'nota': self._template_nota
        }

        return templates[tipo](raw, meta)

    def _get_path(self, tipo: str, meta: dict) -> str:
        """Determina path no Obsidian"""
        base_paths = {
            'tarefa': '📋 TAREFAS/',
            'ideia': '💡 IDEIAS/',
            'projeto': '📂 PROJETOS/',
            'nota': '📝 NOTAS/'
        }

        # Gera nome único
        timestamp = datetime.now(self.tz_br).strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}.md"

        return base_paths[tipo] + filename
```

## 🎤 Integração com Voz

**Usar script existente:** `scripts/audio-transcription/transcribe_video.py`

```python
# Transcrever áudio
python3 scripts/audio-transcription/transcribe_video.py \
    --input audio_nota.mp3 \
    --output transcricao.txt

# Processar com skill obsidian-quick-capture
# Claude automaticamente usa Write() para criar nota no vault
```

## 📊 Formato de Saída

**Sempre incluir:**
1. ✅ Emoji visual no título
2. ✅ Metadados estruturados
3. ✅ Diagrama ASCII
4. ✅ Seções colapsáveis (se longo)
5. ✅ Links internos Obsidian `[[nota]]`
6. ✅ Tags `#tag`

## 🔄 Workflow Completo

```
1. Captura (texto/voz)
2. Classificação automática
3. Formatação visual
4. Criação no Obsidian
5. Notificação → "✅ [Tipo] capturado: [Título]"
```

## 🔗 Ver Também

- `obsidian-organizer` (skill existente)
- Claude MCP Filesystem: Read/Write tools
- Vault path: `/Users/felipemdepaula/Library/Mobile Documents/iCloud~md~obsidian/Documents/Claude-code-ios`
