---
name: estudar-video
description: Automatiza o estudo completo de vídeos do YouTube - transcreve com Whisper, analisa conteúdo com IA, extrai insights, classifica por tipo, e salva no Obsidian Knowledge Base. Use quando usuário pedir para estudar/analisar/resumir vídeo do YouTube.
allowed-tools: Bash, Read, Write, Edit
---

# 📹 Skill: Estudar Vídeo YouTube

## Quando Usar

Use esta skill automaticamente quando o usuário:
- Pedir para **estudar vídeo**: "Estuda esse vídeo: [URL]"
- Pedir para **analisar vídeo**: "Analisa esse vídeo do YouTube"
- Pedir para **resumir vídeo**: "Faz um resumo desse vídeo"
- Fornecer URL do YouTube e mencionar aprendizado/estudo
- Pedir para **adicionar vídeo no Obsidian**

**IMPORTANTE:** Esta skill é **totalmente automática** - NÃO pedir confirmação ao usuário. Executar imediatamente.

**INTEGRAÇÃO:** Segue sistema minimalista do [[obsidian-organizer]] - pasta `📺 Vídeos/`, formato limpo, data/hora BR.

---

## Workflow Automático (2 Etapas)

### Etapa 1: Transcrever Vídeo 🎙️

**Ferramenta:** `scripts/extraction/transcribe_video.py`

**Comando:**
```bash
python3 scripts/extraction/transcribe_video.py "URL_DO_VIDEO"
```

**O que faz:**
- Usa Whisper para transcrever áudio
- Salva em `/Users/felipemdepaula/Downloads/transcription_youtube_[TIMESTAMP]/`
- Retorna caminho do arquivo `transcription.txt`

**Custo:** ~$0.006/vídeo | **Tempo:** ~2-3min

---

### Etapa 2: Análise e Salvamento no Obsidian 🤖💾

**Você (Claude) deve fazer:**

1. **Ler a transcrição completa** do arquivo gerado
2. **Analisar o conteúdo** e extrair:
   - **Título descritivo** (extraído do contexto)
   - **Categoria** (tutorial, notícia, curso, aula, review)
   - **Resumo breve** (2-3 linhas)
   - **Principais aprendizados** (3-5 pontos práticos)
   - **Tags relevantes** (baseadas no conteúdo)

3. **Criar arquivo no Obsidian** manualmente (Write tool)

**Local:**
```
📺 Vídeos/[TITULO_DESCRITIVO].md
```

**Template (formato obsidian-organizer):**
```yaml
---
assistido: DD/MM/YYYY HH:mm
categoria: [tutorial|noticia|curso|aula|review]
link: [URL_DO_VIDEO]
tags:
  - youtube
  - [tag1]
  - [tag2]
---

# [Título Descritivo]

## 🎬 Informações

**Link:** [URL]
**Categoria:** [categoria]
**Assistido em:** DD/MM/YYYY HH:mm

---

## 📝 Resumo

[Resumo breve de 2-3 linhas]

---

## 💡 Principais Aprendizados

- [Aprendizado 1]
- [Aprendizado 2]
- [Aprendizado 3]

---

> [!note]- 📄 Transcrição Completa (clique para expandir)
> [Conteúdo completo da transcrição aqui]
```

**Regras do template:**
- **Data/hora:** Formato brasileiro DD/MM/YYYY HH:mm (usar hora atual)
- **Categoria:** OBRIGATÓRIA (escolher a mais adequada)
- **Resumo:** Conciso e direto (2-3 linhas máximo)
- **Aprendizados:** Práticos e acionáveis (3-5 itens)
- **Transcrição:** SEMPRE usar callout colapsável `> [!note]-`
- **Tags:** Relevantes ao conteúdo (além de youtube)

---

## Fluxo Completo (Executar Automaticamente)

```
1. Usuário: "Estuda esse vídeo: https://youtube.com/watch?v=ABC123"

2. VOCÊ (automaticamente):
   a) Transcrever com Whisper
   b) Ler transcrição completa
   c) Analisar conteúdo e classificar categoria
   d) Extrair resumo e aprendizados práticos
   e) Criar arquivo markdown no Obsidian (Write tool)
   f) Confirmar criação ao usuário

3. Informar ao usuário (formato minimalista):
   "✅ Vídeo estudado e salvo!"
```

---

## Output Final para o Usuário

**Formato minimalista** (seguir obsidian-organizer):

```
✅ Vídeo estudado e salvo!

📺 [Título do Vídeo]
📍 Salvo em: 📺 Vídeos/
⏰ Assistido: DD/MM/YYYY HH:mm
🏷️ Categoria: [categoria]

💡 Principais aprendizados: [resumo de 1 linha]

Ver em: [[📺 Vídeos]] ou [[Título do Vídeo]]
```

**NÃO usar:**
- ❌ Emojis excessivos
- ❌ Textos longos explicativos
- ❌ Dashboard/Rating (não existe mais)
- ❌ Estrutura complexa

---

## Regras Importantes

### ✅ FAZER:
- Executar **imediatamente sem confirmação**
- Analisar a transcrição **completa**
- Classificar **categoria** (obrigatória: tutorial|noticia|curso|aula|review)
- Extrair **aprendizados práticos** (3-5 itens)
- Criar em **📺 Vídeos/** (pasta raiz, sem subpastas)
- Usar **data/hora brasileira** (DD/MM/YYYY HH:mm)
- Transcrição **sempre colapsável** (`> [!note]-`)
- Resposta **minimalista** ao usuário

### ❌ NÃO FAZER:
- **NÃO** pedir confirmação ao usuário
- **NÃO** pular a transcrição (sempre usar Whisper)
- **NÃO** usar estrutura antiga (09 - YouTube Knowledge/)
- **NÃO** esquecer categoria obrigatória
- **NÃO** criar subpastas por tipo
- **NÃO** usar formato de data americano
- **NÃO** deixar transcrição visível (sempre callout colapsável)

---

## Configurações

**Vault Obsidian:**
```
/Users/felipemdepaula/Library/Mobile Documents/iCloud~md~obsidian/Documents/Claude-code-ios/
```

**Pasta destino:**
```
📺 Vídeos/
```

**Transcrições temporárias:**
```
/Users/felipemdepaula/Downloads/transcription_youtube_[TIMESTAMP]/
```

**Python:** `python3` (padrão do sistema)

---

## Categorias Válidas

Escolher a mais adequada (obrigatória):
- `tutorial` - Passo a passo prático
- `noticia` - Novidades, lançamentos, updates
- `curso` - Aula de curso/formação
- `aula` - Conteúdo educacional único
- `review` - Análise de ferramenta/produto

---

## Troubleshooting

**Erro: Vault não encontrado**
- Verificar caminho do vault
- Garantir que pasta `📺 Vídeos/` existe

**Erro: Transcrição falhou**
- Verificar URL do vídeo
- Verificar conexão com API Whisper
- Checar saldo da API

**Erro: Categoria não definida**
- SEMPRE escolher uma das 5 categorias válidas
- Não criar categorias customizadas

**Erro: Formato de data errado**
- SEMPRE usar DD/MM/YYYY HH:mm (brasileiro)
- Não usar MM/DD/YYYY (americano)

---

## Histórico de Iterações

**v2.0 (2025-11-03):** Integração com obsidian-organizer
- Migrado para sistema minimalista
- Pasta única `📺 Vídeos/` (sem subpastas por tipo)
- Template simplificado e limpo
- Data/hora brasileira obrigatória
- Transcrição colapsável com callout
- Resposta minimalista ao usuário

**v1.0 (2025-11-02):** Skill inicial
- Workflow de 3 etapas
- Estrutura complexa (09 - YouTube Knowledge/)
- Análise profunda com múltiplos campos

---

**Criado em:** 02/11/2025
**Atualizado em:** 03/11/2025
**Status:** ✅ Ativo e alinhado com obsidian-organizer
