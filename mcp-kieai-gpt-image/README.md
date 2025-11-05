# 🎨 MCP kie-gpt-image v1.0.0

MCP Server inteligente para **criar imagens** usando a API KIE.AI (GPT-4o Image).

## ⚡ Destaques

```
GPT-4o Image = Qualidade Premium + Flexibilidade
```

- ✅ **Modelo:** GPT-4o Image (OpenAI via KIE.AI)
- ✅ **Variações:** 1, 2 ou 4 imagens por geração (nVariants)
- ✅ **Proporções:** 1:1, 3:2, 2:3 (apenas estas 3)
- ✅ **Referências:** Até 5 imagens de referência (filesUrl)
- ✅ **Inpainting:** Edição com máscaras (maskUrl)
- ✅ **Enhancement:** Melhoria automática de prompt (isEnhance)
- ✅ **Fallback:** Troca automática para outros modelos se falhar
- ✅ Download automático para `~/Downloads`
- ✅ Nomes em **português** sem acentos

## 📋 Características

- ✅ Geração com GPT-4o Image (qualidade superior)
- ✅ Suporte a PNG (formato único)
- ✅ 3 proporções fixas (1:1, 3:2, 2:3)
- ✅ Múltiplas variações (1/2/4 por prompt)
- ✅ Imagens de referência (até 5 URLs)
- ✅ Inpainting com máscaras
- ✅ Nomes descritivos automáticos em PT-BR
- ✅ Download automático para Downloads

## 🚀 Instalação

```bash
cd mcp-kieai-gpt-image
pip install -r requirements.txt
```

## 🔑 Configuração

A API key está pré-configurada no código (`fa32b7ea4ff0e9b5acce83abe09d2b06`).

Se quiser usar outra chave, defina a variável de ambiente:

```bash
export KIEAI_API_KEY="sua-chave-aqui"
```

## 🧪 Teste Rápido

```bash
python3 test_client.py
```

## 🎯 Modos de Uso

### 1️⃣ Criar 1 Imagem Simples

```python
generate_image(
    prompt="Um gato fofo sentado em uma mesa",
    auto_download=True
)
# → gato_fofo_sentado_abc.png (~8s)
# → Retorna 1 imagem em 1:1 (padrão)
```

### 2️⃣ Criar Múltiplas Variações (1, 2 ou 4)

```python
generate_image(
    prompt="Paisagem montanhosa ao pôr do sol",
    nVariants=4,  # Gera 4 variações do mesmo prompt
    image_size="3:2",
    auto_download=True
)
# → montanha_por_sol_abc.png (4 variações)
# → ~15s total (4 imagens diferentes do mesmo conceito)
```

### 3️⃣ Usar Imagens de Referência

```python
generate_image(
    prompt="Um retrato no mesmo estilo desta imagem",
    filesUrl=[
        "https://exemplo.com/estilo1.png",
        "https://exemplo.com/estilo2.png"
    ],
    auto_download=True
)
# → retrato_mesmo_estilo_xyz.png
# → GPT-4o analisa as referências e cria algo similar
```

### 4️⃣ Inpainting com Máscaras

```python
generate_image(
    prompt="Substituir o fundo por uma praia",
    filesUrl=["https://exemplo.com/foto_original.png"],
    maskUrl="https://exemplo.com/mascara_fundo.png",
    auto_download=True
)
# → substituir_fundo_praia_def.png
# → Edita apenas a área mascarada
```

### 5️⃣ Enhancement de Prompt

```python
generate_image(
    prompt="gato",  # Prompt simples
    isEnhance=True,  # GPT-4o expande automaticamente
    auto_download=True
)
# → gato_abc.png
# → Prompt expandido: "A beautiful realistic photo of a cute cat..."
```

### 6️⃣ Fallback para Outros Modelos

```python
generate_image(
    prompt="Imagem complexa que pode falhar",
    enableFallback=True,
    fallbackModel="FLUX_MAX",  # Ou "GPT_IMAGE_1"
    auto_download=True
)
# → Se GPT-4o falhar, tenta FLUX_MAX automaticamente
```

---

## 📚 Ferramentas Disponíveis

### 1. `generate_image`

**Cria imagens** com GPT-4o Image.

**Parâmetros:**
- `prompt` (string, obrigatório): Descrição da imagem a gerar
- `image_size` (opcional): "1:1", "3:2" ou "2:3" (padrão: **"1:1"**)
- `nVariants` (opcional): 1, 2 ou 4 variações (padrão: 1)
- `filesUrl` (opcional): Array de até 5 URLs de imagens de referência
- `maskUrl` (opcional): URL da máscara para inpainting
- `isEnhance` (opcional): true/false - melhora o prompt automaticamente (padrão: false)
- `enableFallback` (opcional): true/false - permite fallback para outros modelos (padrão: false)
- `fallbackModel` (opcional): "GPT_IMAGE_1" ou "FLUX_MAX" - modelo de fallback
- `wait_for_completion` (opcional): true/false (padrão: true)
- `auto_download` (opcional): true/false (padrão: false)

**Exemplo Básico:**
```python
result = await session.call_tool(
    "generate_image",
    arguments={
        "prompt": "Um pôr do sol sobre o oceano",
        "image_size": "3:2",
        "auto_download": True
    }
)
```

**Exemplo com Variações:**
```python
result = await session.call_tool(
    "generate_image",
    arguments={
        "prompt": "Retrato de uma pessoa sorrindo",
        "nVariants": 4,  # Gera 4 versões diferentes
        "image_size": "2:3",
        "auto_download": True
    }
)
```

**Exemplo com Referência:**
```python
result = await session.call_tool(
    "generate_image",
    arguments={
        "prompt": "Uma paisagem no mesmo estilo",
        "filesUrl": ["https://exemplo.com/referencia.png"],
        "auto_download": True
    }
)
```

**Exemplo com Enhancement:**
```python
result = await session.call_tool(
    "generate_image",
    arguments={
        "prompt": "cachorro",  # Prompt simples
        "isEnhance": True,  # GPT-4o expande para algo melhor
        "auto_download": True
    }
)
```

**Resposta (sem download):**
```json
{
  "status": "success",
  "task_id": "abc123",
  "image_urls": [
    "https://tempfile.aiquickdraw.com/.../image1.png",
    "https://tempfile.aiquickdraw.com/.../image2.png"
  ],
  "cost_time": 8,
  "consume_credits": 200,
  "variants_count": 2
}
```

**Resposta (com auto_download=true):**
```json
{
  "status": "success",
  "task_id": "abc123",
  "image_urls": [
    "https://tempfile.aiquickdraw.com/.../image1.png",
    "https://tempfile.aiquickdraw.com/.../image2.png"
  ],
  "cost_time": 8,
  "consume_credits": 200,
  "variants_count": 2,
  "downloads": [
    {
      "url": "https://tempfile.aiquickdraw.com/.../image1.png",
      "path": "/Users/você/Downloads/cachorro_abc.png",
      "filename": "cachorro_abc.png"
    },
    {
      "url": "https://tempfile.aiquickdraw.com/.../image2.png",
      "path": "/Users/você/Downloads/cachorro_def.png",
      "filename": "cachorro_def.png"
    }
  ],
  "downloads_path": "/Users/você/Downloads"
}
```

### 2. `download_image`

Baixa uma imagem da URL e salva na pasta ~/Downloads.

**Parâmetros:**
- `url` (obrigatório): URL da imagem
- `filename` (opcional): Nome do arquivo customizado

**Exemplo:**
```python
result = await session.call_tool(
    "download_image",
    arguments={
        "url": "https://tempfile.aiquickdraw.com/.../image.png",
        "filename": "minha_imagem.png"  # opcional
    }
)
```

**Resposta:**
```json
{
  "status": "success",
  "message": "Imagem baixada com sucesso",
  "path": "/Users/você/Downloads/minha_imagem.png",
  "filename": "minha_imagem.png",
  "downloads_folder": "/Users/você/Downloads"
}
```

### 3. `check_task_status`

Verifica o status de uma task de geração.

**Parâmetros:**
- `task_id` (obrigatório): ID da task

**Exemplo:**
```python
result = await session.call_tool(
    "check_task_status",
    arguments={"task_id": "abc123"}
)
```

**Resposta:**
```json
{
  "task_id": "abc123",
  "state": "success",
  "image_urls": ["https://example.com/image.png"],
  "cost_time": 8,
  "consume_credits": 100
}
```

## ⚠️ Sobre os Links das Imagens

**As URLs retornadas pela API são hospedadas em `tempfile.aiquickdraw.com`**

- ✅ São os links **oficiais** da API KIE.AI
- ⚠️ Pelo nome "tempfile", podem ser **temporários**
- 💡 **Recomendação:** Use `auto_download=true` ou baixe manualmente

```
┌────────────────────────────────────────────┐
│ OPÇÕES DE ARMAZENAMENTO                   │
├────────────────────────────────────────────┤
│ 1. auto_download=true                      │
│    → Baixa automaticamente para Downloads  │
│                                            │
│ 2. download_image(url)                     │
│    → Baixa manualmente depois              │
│                                            │
│ 3. Apenas URLs                             │
│    → Pode expirar (não recomendado)        │
└────────────────────────────────────────────┘
```

## 🎯 Fluxo de Uso

```
┌─────────────────┐
│ Cliente MCP     │
└────────┬────────┘
         │
         │ generate_image(prompt, auto_download=true)
         ▼
┌─────────────────┐
│ MCP Server      │
└────────┬────────┘
         │
         │ POST /createTask
         ▼
┌─────────────────┐
│ KIE.AI API      │
└────────┬────────┘
         │
         │ Processa (2-10s)
         ▼
┌─────────────────┐
│ Imagem Gerada   │
└────────┬────────┘
         │
         │ Download automático (se solicitado)
         ▼
┌─────────────────┐
│ ~/Downloads     │
└─────────────────┘
```

## 🔧 Integração com Claude Code

Adicione ao `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "kie-gpt-image": {
      "command": "python3",
      "args": [
        "/caminho/completo/mcp-kieai-gpt-image/server.py"
      ]
    }
  }
}
```

## 📊 Proporções Disponíveis (LIMITADAS)

⚠️ **GPT-4o Image aceita apenas 3 proporções:**

| Código | Proporção | Uso Típico | Disponível? |
|--------|-----------|------------|-------------|
| 1:1    | Quadrado  | Posts Instagram/Facebook | ✅ SIM (padrão) |
| 3:2    | Paisagem  | Fotos tradicionais | ✅ SIM |
| 2:3    | Retrato   | Retratos, impressão | ✅ SIM |
| 16:9   | Paisagem  | YouTube, apresentações | ❌ NÃO |
| 9:16   | Retrato   | Stories, TikTok | ❌ NÃO |
| 4:5    | Retrato   | Stories Instagram | ❌ NÃO |

**Diferença vs NanoBanana:**
- NanoBanana: 11 proporções (1:1, 16:9, 9:16, 4:5, etc)
- GPT-4o Image: Apenas 3 proporções (1:1, 3:2, 2:3)

## 🐛 Troubleshooting

### Erro: "Module 'mcp' not found"
```bash
pip install mcp
```

### Erro: "401 Unauthorized"
Verifique se a API key está correta:
```bash
echo $KIEAI_API_KEY
```

### Timeout na geração
- Algumas imagens complexas podem demorar >60s
- Use `wait_for_completion: False` e depois `check_task_status`

## 📖 Documentação da API

Documentação completa: https://docs.kie.ai

## 🎨 Exemplos de Prompts

```python
# Fotografia realista
"A professional photo of a modern office workspace, natural lighting, clean desk"

# Arte digital
"A surreal digital painting of a floating island with waterfalls, vibrant colors"

# Ilustração
"A cute cartoon character of a smiling robot, simple design, flat colors"

# Paisagem
"A beautiful mountain landscape at sunset, dramatic clouds, reflection in lake"
```

## ⚡ Performance

- Tempo médio de geração: 5-10 segundos (1 imagem)
- Com nVariants=4: ~15-20 segundos (4 imagens)
- Custo por imagem: ~100-200 créditos (varia com nVariants)
- Timeout padrão: 60 segundos

## 🆚 GPT-4o Image vs NanoBanana

| Feature | GPT-4o Image | NanoBanana |
|---------|--------------|------------|
| **Modelo** | OpenAI GPT-4o | Google Gemini 2.5 Flash |
| **Qualidade** | ⭐⭐⭐⭐⭐ Premium | ⭐⭐⭐⭐ Ótima |
| **Proporções** | 3 (1:1, 3:2, 2:3) | 11 (todas) |
| **Variações** | ✅ 1/2/4 por prompt | ❌ Não |
| **Referências** | ✅ Até 5 imagens | ❌ Não |
| **Inpainting** | ✅ Com máscaras | ❌ Não |
| **Enhancement** | ✅ Prompt automático | ❌ Não |
| **Fallback** | ✅ Para outros modelos | ❌ Não |
| **Edição batch** | ❌ Não | ✅ 1-15 imagens |
| **Velocidade** | ~8s (1 img) | ~5s (1 img) |
| **Uso ideal** | Qualidade premium, variações | Proporções customizadas, edição batch |

**Escolha GPT-4o quando:**
- Precisa de qualidade máxima
- Quer múltiplas variações do mesmo conceito
- Precisa usar imagens de referência
- Vai fazer inpainting/edição com máscaras

**Escolha NanoBanana quando:**
- Precisa de proporções específicas (16:9, 4:5, etc)
- Vai editar múltiplas imagens em paralelo
- Quer velocidade máxima
- Precisa de mais flexibilidade em proporções

## 📝 Changelog

### v1.0.0 (2025-11-05)
- ✅ Implementação inicial com GPT-4o Image
- ✅ Suporte a nVariants (1/2/4)
- ✅ Suporte a filesUrl (referências)
- ✅ Suporte a maskUrl (inpainting)
- ✅ Suporte a isEnhance (melhoria de prompt)
- ✅ Suporte a fallback para outros modelos
- ✅ Download automático
- ✅ Nomes descritivos em português
- ✅ Documentação completa
