# 🎬 Scripts de Geração de Vídeos - Sora 2

Templates prontos e testados para geração de vídeos usando **Sora 2 (OpenAI)** via API Kie.ai.

## 📋 Índice

- [Templates Disponíveis](#-templates-disponíveis)
- [Uso Rápido](#-uso-rápido)
- [Configuração](#-configuração)
- [Opções e Parâmetros](#-opções-e-parâmetros)
- [Exemplos Práticos](#-exemplos-práticos)
- [Comparação de Performance](#-comparação-de-performance)
- [Troubleshooting](#-troubleshooting)

---

## 🛠️ Templates Disponíveis

### 1. `generate_sora.py` - Vídeo Único
Gera **1 vídeo** com Sora 2.

**Quando usar:**
- ✅ Gerar apenas 1 vídeo
- ✅ Testar prompts rapidamente
- ✅ Vídeos individuais com foco em qualidade

**Tempo estimado:** 2-5 minutos

### 2. `batch_generate.py` - Vídeos em Lote
Gera **2+ vídeos simultaneamente** em paralelo.

**Quando usar:**
- ✅ Gerar 2 ou mais vídeos
- ✅ Máxima eficiência (todos em paralelo)
- ✅ Criar variações de um mesmo conceito

**Tempo estimado:** 2-5 minutos (mesmo para múltiplos vídeos!)

### 3. `edit_json2video.py` - Edição via JSON
Cria e edita vídeos programaticamente usando **JSON2Video API**.

**Quando usar:**
- ✅ Criar vídeos complexos (múltiplas scenes, elementos)
- ✅ Adicionar legendas automáticas
- ✅ Criar audiogramas (podcast visual)
- ✅ Voice-over com ElevenLabs
- ✅ Templates reutilizáveis com variáveis
- ✅ Slideshows com transições

**Tempo estimado:** 1-5 minutos (renderização cloud)

**Documentação completa:** `.claude/skills/json2video/SKILL.md`

---

## ⚡ Uso Rápido

### Vídeo Único

```bash
# Básico
python3 scripts/video-generation/generate_sora.py "seu prompt aqui"

# Com proporção específica
python3 scripts/video-generation/generate_sora.py "paisagem montanha" --aspect landscape

# Portrait (vertical - Stories/Reels)
python3 scripts/video-generation/generate_sora.py "modelo desfilando" --aspect portrait

# Quadrado (posts Instagram)
python3 scripts/video-generation/generate_sora.py "logo animado" --aspect square
```

### Vídeos em Lote (2+)

```bash
# Múltiplos vídeos
python3 scripts/video-generation/batch_generate.py "gato brincando" "cachorro correndo" "pássaro voando"

# Com proporção específica
python3 scripts/video-generation/batch_generate.py "cena 1" "cena 2" "cena 3" --aspect landscape

# Variações de um conceito
python3 scripts/video-generation/batch_generate.py \
  "café sendo servido - close up" \
  "café sendo servido - plano aberto" \
  "café sendo servido - câmera lenta"
```

### Edição via JSON (JSON2Video)

```bash
# Criar vídeo a partir de JSON
python3 scripts/video-generation/edit_json2video.py video.json

# Output customizado
python3 scripts/video-generation/edit_json2video.py video.json --output ~/Desktop/result.mp4

# Verificar status de renderização
python3 scripts/video-generation/edit_json2video.py --status PROJECT_ID

# Ver exemplos de JSON
python3 scripts/video-generation/edit_json2video.py --examples
```

**Estrutura JSON mínima:**
```json
{
  "scenes": [
    {
      "elements": [
        {
          "type": "text",
          "text": "Hello World"
        }
      ]
    }
  ]
}
```

**Configuração necessária:**
```bash
export JSON2VIDEO_API_KEY='sua_api_key'
```

Obtenha API key em: https://json2video.com/dashboard

---

## 🔧 Configuração

### Pré-requisitos

1. **API Key configurada** em `tools/generate_video_sora.py`:
   ```python
   API_KEY = "sua-api-key-kie-ai"
   ```

2. **Dependências instaladas**:
   ```bash
   pip3 install --user requests
   ```

### Localização dos Vídeos

Todos os vídeos são salvos automaticamente em:
```
~/Downloads/
```

**Formato dos nomes:**
- Vídeo único: `sora_video_20251102_103045.mp4`
- Lote: `batch_sora_gato_brincando_20251102_103045.mp4`

---

## ⚙️ Opções e Parâmetros

### Proporções Disponíveis (`--aspect`)

| Proporção | Uso Ideal | Exemplo |
|-----------|-----------|---------|
| `portrait` (padrão) | Stories, Reels, TikTok | 9:16 vertical |
| `landscape` | YouTube, TV | 16:9 horizontal |
| `square` | Posts Instagram | 1:1 quadrado |

### Marca d'água (`--watermark`)

Por padrão, a marca d'água é **removida automaticamente**.

Para **manter a marca d'água**:
```bash
python3 scripts/video-generation/generate_sora.py "prompt" --watermark
```

---

## 🎯 Exemplos Práticos

### 1. Conteúdo para Redes Sociais

```bash
# Stories/Reels (vertical)
python3 scripts/video-generation/generate_sora.py \
  "pessoa tomando café pela manhã, luz natural, câmera lenta" \
  --aspect portrait

# YouTube (horizontal)
python3 scripts/video-generation/generate_sora.py \
  "timelapse de cidade ao anoitecer" \
  --aspect landscape

# Post Instagram (quadrado)
python3 scripts/video-generation/generate_sora.py \
  "produto sendo aberto, unboxing, close up" \
  --aspect square
```

### 2. Geração em Lote (Eficiente)

```bash
# Criar 3 variações de produtos
python3 scripts/video-generation/batch_generate.py \
  "tênis esportivo girando 360 graus, fundo branco" \
  "tênis esportivo close no solado" \
  "tênis esportivo em movimento, corrida" \
  --aspect square

# Diferentes ângulos da mesma cena
python3 scripts/video-generation/batch_generate.py \
  "praia ao pôr do sol - plano geral" \
  "praia ao pôr do sol - close nas ondas" \
  "praia ao pôr do sol - câmera aérea" \
  --aspect landscape
```

### 3. Animações e Efeitos

```bash
# Câmera lenta
python3 scripts/video-generation/generate_sora.py \
  "gotas de água caindo em super slow motion, fundo preto"

# Movimento dramático
python3 scripts/video-generation/generate_sora.py \
  "cortina sendo aberta revelando paisagem, movimento cinematográfico"

# Texto animado
python3 scripts/video-generation/generate_sora.py \
  "logo aparecendo com partículas de luz, fundo escuro, elegante"
```

---

## 📊 Comparação de Performance

| Cenário | Método Antigo | Batch (Novo) | Economia |
|---------|---------------|--------------|----------|
| 1 vídeo | 3 min | 3 min | 0% |
| 2 vídeos | 6 min (sequencial) | 3 min (paralelo) | **50%** |
| 3 vídeos | 9 min (sequencial) | 3 min (paralelo) | **67%** |
| 5 vídeos | 15 min (sequencial) | 5 min (paralelo) | **67%** |

**🚨 REGRA CRÍTICA:**
- **1 vídeo** → use `generate_sora.py`
- **2+ vídeos** → SEMPRE use `batch_generate.py` (paralelo!)

---

## 🎨 Dicas de Prompts

### Estrutura Ideal

```
[Sujeito] + [Ação] + [Contexto] + [Estilo/Movimento]
```

**Exemplos:**
- ✅ "Gato persa brincando com novelo de lã, sala iluminada, câmera lenta"
- ✅ "Barista preparando café latte art, close nas mãos, movimento fluido"
- ✅ "Drone sobrevoando floresta tropical, amanhecer, movimento cinematográfico"

### Palavras-chave Úteis

**Movimento:**
- `câmera lenta`, `slow motion`, `timelapse`
- `movimento cinematográfico`, `dolly zoom`
- `rotação 360 graus`, `zoom in`, `zoom out`

**Iluminação:**
- `luz natural`, `golden hour`, `pôr do sol`
- `luz neon`, `fundo escuro`, `contraluz`

**Estilo:**
- `cinematográfico`, `profissional`, `comercial`
- `minimalista`, `vibrante`, `dramático`

---

## 🔍 Troubleshooting

### Vídeo não gera (timeout)

```bash
# Verifique se API está funcionando
curl -X POST https://api.kie.ai/api/v1/jobs/createTask \
  -H "Authorization: Bearer sua-api-key" \
  -H "Content-Type: application/json" \
  -d '{"model": "sora-2-text-to-video", "input": {"prompt": "test"}}'
```

**Solução:** Vídeos podem levar até 10 minutos. O timeout padrão é 10 min.

### Erro de API Key

```
❌ Erro: 401 Unauthorized
```

**Solução:** Verifique se a API Key está correta em `tools/generate_video_sora.py`:17

### Vídeo de baixa qualidade

**Solução:** Refine o prompt com mais detalhes:
- ❌ "gato brincando"
- ✅ "gato persa brincando com novelo de lã vermelha, sala iluminada por luz natural, close up, câmera lenta, profissional"

### Download falha

```
❌ Erro ao baixar vídeo
```

**Solução:**
1. Verifique conexão de internet
2. Vídeo pode estar temporariamente indisponível
3. Execute novamente após alguns segundos

---

## 📂 Estrutura dos Arquivos

```
scripts/video-generation/
├── README.md              # Esta documentação
├── generate_sora.py       # Template vídeo único (Sora 2)
├── batch_generate.py      # Template vídeos em lote (Sora 2)
└── edit_json2video.py     # Template edição via JSON (JSON2Video)

tools/
├── generate_video_sora.py       # Ferramenta base (vídeo único)
├── generate_video_batch_sora.py # Ferramenta base (lote)
└── json2video_api.py            # Ferramenta base (JSON2Video API)

.claude/skills/json2video/
├── SKILL.md               # Instruções principais
├── REFERENCE.md           # Documentação técnica completa
├── EXAMPLES.md            # Casos de uso (7 exemplos)
└── TROUBLESHOOTING.md     # Erros comuns e soluções
```

---

## 🚀 Próximos Passos

1. **Teste com 1 vídeo** para validar setup:
   ```bash
   python3 scripts/video-generation/generate_sora.py "teste vídeo simples"
   ```

2. **Teste batch** com 2 vídeos:
   ```bash
   python3 scripts/video-generation/batch_generate.py "teste 1" "teste 2"
   ```

3. **Use em produção** para seus projetos!

---

## 📞 Suporte

**Ferramentas base:**
- `tools/generate_video_sora.py`
- `tools/generate_video_batch_sora.py`
- `tools/json2video_api.py`

**Docs relacionada:**
- `.claude/skills/json2video/SKILL.md` (JSON2Video completo)
- `.claude/skills/json2video/EXAMPLES.md` (7 exemplos práticos)
- `.claude/skills/json2video/REFERENCE.md` (API técnica)
- `CLAUDE.md` (configuração geral)

**API Kie.ai (Sora 2):**
- Base URL: `https://api.kie.ai`
- Modelo: `sora-2-text-to-video`
- Duração: ~15 segundos por vídeo

**API JSON2Video:**
- Base URL: `https://api.json2video.com/v2`
- Docs: `https://json2video.com/docs/v2/`
- Dashboard: `https://json2video.com/dashboard`

---

**Última atualização:** 2025-11-04
**Versão:** 2.0 (+ JSON2Video API)
