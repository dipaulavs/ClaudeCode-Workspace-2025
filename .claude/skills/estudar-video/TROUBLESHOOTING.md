# Estudar Vídeo - Troubleshooting

## Problemas Comuns & Soluções

---

## Problema 1: Transcrição Falhou (yt-dlp error)

### Sintomas
```bash
ERROR: Unable to download video
ERROR: Video unavailable
ERROR: This video is private
```

### Causa Raiz
- Vídeo privado/removido/região bloqueada
- yt-dlp desatualizado
- Problema de rede/firewall
- URL inválida

### Solução

**Passo 1: Verificar URL do vídeo**
```bash
# Testar manualmente
yt-dlp "URL_DO_VIDEO"

# Se funcionar manual, problema é no script
# Se não funcionar, problema é no vídeo/yt-dlp
```

**Passo 2: Atualizar yt-dlp**
```bash
# yt-dlp desatualiza rápido (YouTube muda APIs)
pip install --upgrade yt-dlp

# Verificar versão
yt-dlp --version
# Deve ser 2023.3.4 ou superior
```

**Passo 3: Testar vídeo alternativo**
```bash
# URL de teste (vídeo público)
python3 scripts/extraction/transcribe_video.py \
  "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Se funcionar: Problema é o vídeo específico
# Se não funcionar: Problema é no sistema
```

**Passo 4: Verificar logs detalhados**
```bash
# Rodar com verbose
python3 scripts/extraction/transcribe_video.py "URL" --verbose

# Logs mostrarão erro específico:
# - 403: Vídeo bloqueado por região
# - 404: Vídeo não existe
# - Connection timeout: Problema de rede
```

**Workarounds:**

```bash
# Vídeo privado/bloqueado
→ Não há solução (pedir ao criador tornar público)

# Vídeo de playlist
→ Usar URL direta do vídeo, não da playlist

# Vídeo ao vivo (live stream)
→ Esperar acabar e virar VOD

# Vídeo com restrição de idade
→ yt-dlp pode pedir login (adicionar cookies)
```

---

## Problema 2: Whisper API Limit Exceeded

### Sintomas
```
Error: Rate limit exceeded for Whisper API
Status: 429 (Too Many Requests)
```

### Causa Raiz
- Limite da OpenAI: 50 requests/minuto
- Limite de cota mensal atingido
- API key inválida/revogada

### Solução

**Passo 1: Verificar cota da API**
```
1. Acessar: https://platform.openai.com/usage
2. Verificar:
   - Requests/min: Máx 50
   - Cota mensal: Depende do plano
3. Se excedeu: Aguardar reset (1 minuto) ou upgrade
```

**Passo 2: Rate limiting no script**
```python
import time

# Adicionar delay entre transcrições
time.sleep(2)  # 2 segundos entre chamadas

# Isso garante < 30 req/min (bem abaixo do limite)
```

**Passo 3: Trocar API key (se necessário)**
```bash
# .env
OPENAI_API_KEY=sk-proj-NOVA_KEY_AQUI

# Verificar nova key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer sk-proj-NOVA_KEY"
```

**Passo 4: Alternativa gratuita (local)**
```bash
# Se não quer usar API paga, rodar Whisper localmente
pip install openai-whisper

# Transcrever local (mais lento, mas grátis)
whisper video.mp3 --model base --language Portuguese
```

---

## Problema 3: Classificação de Tipo Incorreta

### Sintomas
- Vídeo é tutorial mas Claude classificou como "Outros"
- Vídeo é metodologia mas classificou como "Aula"
- Classificação genérica quando deveria ser específica

### Causa Raiz
- Transcrição ambígua/incompleta
- Vídeo mescla múltiplos tipos
- Prompt de classificação precisa ajuste
- Claude não teve contexto suficiente

### Solução

**Passo 1: Verificar transcrição**
```bash
# Ler transcrição gerada
cat "/Users/felipemdepaula/Downloads/transcription_youtube_*/transcription.txt"

# Perguntas:
# - Transcrição está completa? (sem cortes)
# - Texto faz sentido? (sem erros de reconhecimento)
# - Conteúdo é claro sobre o tipo?
```

**Passo 2: Reclassificar manualmente**
```markdown
# Abrir nota no Obsidian
vim "09 - YouTube Knowledge/Videos/Outros/[TITULO].md"

# Editar frontmatter:
---
tipo: tutorial  # Mudar de "outros" para tipo correto
---

# Mover arquivo para pasta correta
mv "Videos/Outros/[TITULO].md" "Videos/Tutoriais/[TITULO].md"
```

**Passo 3: Melhorar prompt de classificação**

Se múltiplos vídeos têm classificação errada, ajustar SKILL.md:

```markdown
# Adicionar exemplos mais claros de cada tipo

Tutorial: Passo a passo COM CÓDIGO ou comandos específicos
Metodologia: Framework ou processo SEM código específico
Aula: Conceitos teóricos, explicações de fundamentos
[...]
```

**Casos Ambíguos:**

```markdown
Vídeo: "Understanding React Hooks and Building a Todo App"
→ Primeira metade: Aula (explica conceitos)
→ Segunda metade: Tutorial (constrói app)

DECISÃO: Classificar como TUTORIAL
RAZÃO: Parte prática predomina, objetivo final é construir algo

Vídeo: "The SCRUM Framework Explained"
→ Explica processo teórico
→ Mas é processo/framework, não fundamento técnico

DECISÃO: Classificar como METODOLOGIA
RAZÃO: Foca em framework de trabalho, não código
```

---

## Problema 4: Obsidian Vault Não Encontrado

### Sintomas
```bash
Error: Vault path does not exist
FileNotFoundError: [Errno 2] No such file or directory
```

### Causa Raiz
- Caminho do vault mudou (Obsidian movido)
- iCloud Drive não sincronizado
- Permissões de acesso negadas
- Typo no caminho configurado

### Solução

**Passo 1: Verificar caminho atual**
```bash
# Caminho configurado
grep VAULT_PATH config/obsidian_config.py

# Resultado esperado:
VAULT_PATH = "/Users/felipemdepaula/Library/Mobile Documents/iCloud~md~obsidian/Documents/Claude-code-ios/"
```

**Passo 2: Testar se existe**
```bash
# Listar conteúdo do vault
ls "/Users/felipemdepaula/Library/Mobile Documents/iCloud~md~obsidian/Documents/Claude-code-ios/"

# Se erro "No such file": Vault mudou de local
# Se listar pastas: Vault existe, problema é permissão
```

**Passo 3: Encontrar vault correto**
```bash
# Procurar vault do Obsidian
find ~ -name "Claude-code-ios" -type d 2>/dev/null

# Resultado mostrará caminho real:
/Users/felipemdepaula/Library/Mobile Documents/iCloud~md~obsidian/Documents/Claude-code-ios/
```

**Passo 4: Atualizar configuração**
```python
# config/obsidian_config.py
VAULT_PATH = "/CAMINHO/CORRETO/ENCONTRADO/ACIMA/"

# Salvar e testar novamente
```

**Troubleshooting iCloud:**

```bash
# iCloud Drive não sincronizado?
# 1. Abrir Finder → iCloud Drive
# 2. Verificar se pasta Obsidian existe
# 3. Se tiver ícone de nuvem: Forçar download

# Alternativa: Mover vault para local (não iCloud)
# Obsidian → Settings → Vault → Move vault
# Escolher: /Users/felipemdepaula/Documents/Obsidian/
```

---

## Problema 5: Análise Superficial/Incompleta

### Sintomas
- Resumo muito curto (1-2 frases apenas)
- Key takeaways genéricos (sem detalhes)
- Análise não extrai insights profundos
- Parece que Claude "não entendeu" o vídeo

### Causa Raiz
- Modelo Claude errado (Haiku em vez de Sonnet)
- Prompt de análise não foi seguido
- Transcrição muito longa (excede context window)
- API timeout antes de completar

### Solução

**Passo 1: Verificar modelo usado**
```python
# scripts/obsidian/add_youtube_video.py
# Verificar qual modelo está configurado

# Ideal: claude-sonnet-4-5-20250929 (200k context)
# Evitar: claude-haiku (responde rápido mas superficial)
```

**Passo 2: Melhorar prompt de análise**

```markdown
# Adicionar instruções mais específicas:

"Analise PROFUNDAMENTE esta transcrição. Não se limite a resumir.

OBRIGATÓRIO:
- Resumo executivo: 3 parágrafos completos (não 2 frases)
- Key takeaways: 7 itens com explicação detalhada (não só bullet points)
- Análise detalhada: Seção específica com 300+ palavras
- Insights profundos: Conexões não óbvias, implicações, padrões

Exemplo de key takeaway BOM:
❌ 'Express é rápido'
✅ 'Express minimiza overhead: apenas 3 linhas criam servidor (require, app, listen), sem boilerplate de outros frameworks. Isso reduz curva de aprendizado e permite foco na lógica de negócio.'
"
```

**Passo 3: Verificar tamanho da transcrição**
```bash
# Contar tokens aproximados
wc -w transcription.txt

# Se > 150k palavras (~200k tokens): Excede context window
# Solução: Resumir transcrição primeiro OU dividir em partes
```

**Passo 4: Aumentar timeout da API**
```python
# Se análise demora muito e é cortada por timeout

import openai
openai.timeout = 120  # 2 minutos (padrão: 60s)
```

**Manual Override:**

Se análise automática falhar, fazer manual:

```markdown
1. Ler transcrição completa
2. Escrever análise manualmente no Obsidian
3. Criar nota seguindo template padrão
4. Adicionar insights que Claude perdeu
```

---

## Problema 6: Dashboard Não Atualiza Automaticamente

### Sintomas
- Novo vídeo adicionado mas não aparece no dashboard
- Contador de vídeos não aumenta
- Seção "Recentes" não mostra último vídeo

### Causa Raiz
- Script `add_youtube_video.py` não atualiza dashboard
- Dashboard usa query Dataview que falhou
- Cache do Obsidian não refresh

### Solução

**Passo 1: Verificar se dashboard existe**
```bash
# Caminho do dashboard
ls "09 - YouTube Knowledge/YouTube Dashboard.md"

# Se não existe: Criar manualmente
```

**Passo 2: Atualizar dashboard manualmente**
```markdown
# Abrir dashboard no Obsidian
# Forçar refresh: Cmd+R (Mac) ou Ctrl+R (Windows)

# Se usar Dataview plugin:
# Settings → Dataview → Refresh Interval: 1000ms
```

**Passo 3: Verificar query Dataview**
```markdown
# Dashboard deve ter queries assim:

## Recentes (Últimos 10)

```dataview
TABLE tipo, canal, duracao, rating
FROM "09 - YouTube Knowledge/Videos"
SORT data_assistido DESC
LIMIT 10
```

# Se query não funciona:
# - Verificar se Dataview plugin está instalado
# - Verificar se frontmatter das notas está correto (data_assistido existe?)
```

**Passo 4: Automatizar atualização do dashboard**

```python
# scripts/obsidian/add_youtube_video.py
# Adicionar função que atualiza dashboard após criar nota

def update_dashboard():
    dashboard_path = f"{VAULT_PATH}/09 - YouTube Knowledge/YouTube Dashboard.md"

    # Contar vídeos por tipo
    tutoriais = len(list(Path(f"{VIDEOS_PATH}/Tutoriais/").glob("*.md")))
    metodologias = len(list(Path(f"{VIDEOS_PATH}/Metodologias/").glob("*.md")))
    # ...

    # Atualizar contadores no dashboard
    # (implementação específica)
```

---

## Problema 7: Vídeo Muito Longo (> 2 horas)

### Sintomas
```
Error: Audio file too large (> 25MB)
Error: Transcription exceeded context window
```

### Causa Raiz
- Whisper API: Limite de 25MB (~3h de áudio)
- Claude context: 200k tokens (~8h de transcrição)
- Processamento demora muito (timeout)

### Solução

**Opção 1: Dividir vídeo em partes**
```bash
# Usar yt-dlp para baixar apenas parte
yt-dlp -f bestaudio \
  --postprocessor-args "-ss 00:00:00 -to 01:00:00" \
  "URL_VIDEO"

# Isso baixa apenas primeira hora
# Processar cada hora separadamente
```

**Opção 2: Transcrever local (Whisper open source)**
```bash
# Instalar Whisper local (sem limite de tamanho)
pip install openai-whisper

# Transcrever (demora mais, mas funciona)
whisper video_long.mp3 --model base --language pt
```

**Opção 3: Resumir transcrição antes de analisar**
```python
# Se transcrição é muito longa:
# 1. Dividir em chunks de 10k palavras
# 2. Resumir cada chunk com Claude
# 3. Concatenar resumos
# 4. Analisar resumo final (muito menor)
```

**Quando NÃO vale a pena:**

```markdown
Vídeo > 3 horas:
- Custo: ~$1.50 transcrição + análise
- Tempo: ~10-15 minutos processamento
- Qualidade: Análise pode ser superficial (muito conteúdo)

ALTERNATIVA:
- Assistir manual em 2x speed
- Fazer anotações enquanto assiste
- Criar nota manual no Obsidian
- Mais efetivo para vídeos longos/densos
```

---

## Quick Reference: Checklist de Problemas

| Erro | Check | Solução |
|------|-------|---------|
| `yt-dlp error` | Atualizar yt-dlp | `pip install --upgrade yt-dlp` |
| `Rate limit 429` | Cota OpenAI | Aguardar 1 min ou upgrade |
| `Vault not found` | Caminho correto | Verificar `config/obsidian_config.py` |
| `Análise superficial` | Modelo Claude | Usar Sonnet (não Haiku) |
| `Dashboard não atualiza` | Plugin Dataview | Instalar/ativar Dataview |
| `Vídeo > 2h` | Limite Whisper | Dividir em partes ou transcrever local |
| `Classificação errada` | Reclassificar | Editar frontmatter manualmente |

---

## Logs & Debug

**Ativar modo verbose:**
```bash
# Adicionar flag --verbose
python3 scripts/extraction/transcribe_video.py "URL" --verbose

# Mostra:
# - URL sendo processada
# - Caminho do arquivo de áudio
# - Resposta da API Whisper
# - Erros detalhados
```

**Verificar logs do Obsidian:**
```
Obsidian → Settings → About → Open debug console
# Erros de Dataview, plugins, etc aparecem aqui
```

**Testar componentes isolados:**
```bash
# 1. Testar download apenas
yt-dlp "URL" -o "/tmp/test.mp3"

# 2. Testar transcrição com arquivo local
python3 scripts/extraction/transcribe_video.py --file "/tmp/test.mp3"

# 3. Testar análise com transcrição existente
python3 scripts/obsidian/add_youtube_video.py \
  --transcricao "/path/to/transcription.txt"
```

---

**Related:** See `REFERENCE.md` for system architecture and `EXAMPLES.md` for analysis examples.
