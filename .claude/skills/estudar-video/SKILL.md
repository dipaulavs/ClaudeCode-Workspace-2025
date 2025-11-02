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

---

## Workflow Automático (3 Etapas)

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

### Etapa 2: Análise Completa com IA 🤖

**Você (Claude) deve fazer:**

1. **Ler a transcrição completa** do arquivo gerado
2. **Analisar profundamente** o conteúdo
3. **Classificar o tipo** do vídeo:
   - **Tutorial:** Passo a passo prático com código/comandos
   - **Metodologia:** Frameworks, processos, sistemas
   - **Aula:** Conteúdo educacional teórico
   - **Noticia:** Novidades, lançamentos, updates
   - **Review:** Análises de ferramentas/produtos
   - **Outros:** Não se encaixa nas categorias acima

4. **Extrair informações:**
   - **Resumo executivo** (2-3 parágrafos)
   - **Key takeaways** (5-7 pontos principais)
   - **Análise personalizada** baseada no tipo:
     - Tutorial → Passo a passo detalhado
     - Metodologia → Frameworks e conceitos
     - Aula → Conceitos e teoria
     - Review → Prós, contras, alternativas
   - **Recursos mencionados** (ferramentas, links, código)
   - **Aplicações práticas**

**Diretrizes de análise:**
- Seja **detalhado e completo**
- Foque no **valor prático**
- Organize de forma **escaneável**
- Use **exemplos concretos**
- Identifique **ações aplicáveis**

---

### Etapa 3: Salvar no Obsidian 💾

**Ferramenta:** `scripts/obsidian/add_youtube_video.py`

**Comando:**
```bash
python3 scripts/obsidian/add_youtube_video.py "URL" \
  --titulo "TITULO_EXTRAIDO" \
  --canal "NOME_DO_CANAL" \
  --categoria "CATEGORIA_IDENTIFICADA" \
  --duracao "XXmin" \
  --rating 5 \
  --tipo "TIPO_CLASSIFICADO" \
  --transcricao "/caminho/para/transcription.txt"
```

**Parâmetros importantes:**
- `--tipo`: Use o tipo classificado na Etapa 2 (tutorial|metodologia|aula|noticia|review|outros)
- `--categoria`: Tema principal (IA & Automação, Programação, Marketing, etc)
- `--rating`: Sempre 5 (padrão para vídeos estudados)
- `--transcricao`: Caminho do arquivo gerado na Etapa 1

**Estrutura no Obsidian:**
```
09 - YouTube Knowledge/
├── Videos/
│   └── [TIPO]/
│       └── 2025-11-02 - [TITULO].md
└── Transcricoes/
    └── [VIDEO_ID].txt
```

---

## Fluxo Completo (Executar Automaticamente)

```
1. Usuário: "Estuda esse vídeo: https://youtube.com/watch?v=ABC123"

2. VOCÊ (automaticamente):
   a) Transcrever com Whisper
   b) Ler transcrição completa
   c) Analisar e classificar
   d) Extrair insights
   e) Salvar no Obsidian com análise completa
   f) Atualizar dashboard automaticamente

3. Informar ao usuário:
   "✅ Vídeo estudado! Análise completa salva no Obsidian."
```

---

## Output Final para o Usuário

Após completar todas as etapas, mostrar:

```
✅ Vídeo estudado e analisado completamente!

📊 Resumo da Análise
🎬 Vídeo: [TITULO]
👤 Canal: [CANAL]
⏱️ Duração: [DURACAO]
📂 Tipo: [TIPO]
⭐ Rating: 5/5

🎯 Principais Aprendizados
[Listar 3-5 key takeaways principais]

📂 Localização no Obsidian
- Dashboard: [[YouTube Dashboard]]
- Resumo completo: [[TITULO_DO_VIDEO]]

💡 Próximo passo sugerido: [sugestão relevante baseada no conteúdo]
```

---

## Regras Importantes

### ✅ FAZER:
- Executar **imediatamente sem confirmação**
- Analisar a transcrição **completa** (não resumir)
- Classificar **automaticamente** o tipo do vídeo
- Extrair **insights profundos e práticos**
- Salvar no **vault correto** do Obsidian
- Atualizar **dashboard automaticamente**

### ❌ NÃO FAZER:
- **NÃO** pedir confirmação ao usuário
- **NÃO** pular a transcrição (sempre usar Whisper)
- **NÃO** resumir superficialmente
- **NÃO** esquecer de classificar o tipo
- **NÃO** salvar no vault errado

---

## Configurações

**Vault Obsidian:**
```
/Users/felipemdepaula/Library/Mobile Documents/iCloud~md~obsidian/Documents/Claude-code-ios/
```

**Transcrições temporárias:**
```
/Users/felipemdepaula/Downloads/transcription_youtube_[TIMESTAMP]/
```

**Python:** `python3` (padrão do sistema)

---

## Troubleshooting

**Erro: Vault não encontrado**
- Verificar caminho em `config/obsidian_config.py`
- Garantir que Obsidian está aberto

**Erro: Transcrição falhou**
- Verificar URL do vídeo
- Checar se yt-dlp está instalado
- Verificar conexão com API Whisper

**Erro: Classificação incorreta**
- Na próxima iteração, corrigir com feedback
- Atualizar skill (Etapa E - Enhance)

---

## Histórico de Iterações

**v1.0 (2025-11-02):** Skill inicial criada
- Workflow de 3 etapas definido
- Classificação automática por tipo
- Análise profunda com IA
- Salvamento automático no Obsidian

**Próximas melhorias (Etapa E):**
- [ ] Testar com diferentes tipos de vídeo
- [ ] Refinar classificação automática
- [ ] Ajustar profundidade da análise
- [ ] Adicionar edge cases encontrados

---

**Criado em:** 02/11/2025
**Framework usado:** MASTER (aplicado na prática!)
**Status:** ✅ Pronto para uso e iteração
