# 🎨 MCP kie-nanobanana-create v2.1.0

MCP Server inteligente para **criar e editar imagens** usando a API KIE.AI (NanoBanana - Gemini 2.5 Flash).

## ⚡ Destaques

```
1 MCP = 4 Modos Automáticos
```

- ✅ **Criar** 1-15 imagens (paralelo quando N > 1)
- ✅ **Editar** 1-15 imagens (paralelo quando N > 1)
- ✅ Detecção automática de modo (criar vs editar)
- ✅ Nomes em **português** sem acentos
- ✅ Download automático para `~/Downloads`
- ✅ Proporção **4:5** padrão (stories/retratos)
- ✅ **Até 6x mais rápido** com geração paralela

## 📋 Características

- ✅ Geração e edição com NanoBanana (Gemini 2.5 Flash)
- ✅ Suporte a múltiplos formatos (PNG, JPEG)
- ✅ Múltiplas proporções (1:1, 16:9, 4:5, etc)
- ✅ Geração/edição paralela (até 15 imagens simultâneas)
- ✅ Nomes descritivos automáticos em PT-BR
- ✅ Download automático para Downloads

## 🚀 Instalação

```bash
cd mcp-kieai-image-gen
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

## 🎯 4 Modos de Uso (Detecção Automática)

### 1️⃣ Criar 1 Imagem

```python
generate_image(
    prompt="Um gato fofo",
    auto_download=True
)
# → gato_fofo_abc.png (~10s)
```

### 2️⃣ Criar 3-15 Imagens (Paralelo)

```python
generate_image(
    prompts=[
        "Um gato fofo",
        "Um cachorro brincando",
        "Uma raposa na floresta"
    ],
    auto_download=True
)
# → 3 imagens em ~17s (vs 30s = 1.8x mais rápido!)
```

### 3️⃣ Editar 1 Imagem

```python
generate_image(
    prompt="Mude a cor da camisa para vermelho",
    image_url="https://tempfile.aiquickdraw.com/.../imagem.png",
    auto_download=True
)
# → mudar_cor_camisa_abc.png (~19s)
```

### 4️⃣ Editar 3-15 Imagens (Paralelo)

```python
generate_image(
    prompts=[
        "Cor vermelha",
        "Cor azul",
        "Cor verde"
    ],
    image_urls=[
        "https://.../img1.png",
        "https://.../img2.png",
        "https://.../img3.png"
    ],
    auto_download=True
)
# → 3 edições em ~26s (vs 57s = 2.2x mais rápido!)
```

---

## 📚 Ferramentas Disponíveis

### 1. `generate_image`

**Cria OU edita imagens** com NanoBanana (detecção automática).

**Parâmetros:**
- `prompt` (string): Para criar/editar 1 imagem. Use este OU `prompts`.
- `prompts` (array): Para criar/editar 2-15 imagens em PARALELO. Use este OU `prompt`.
- `image_url` (string, opcional): URL da imagem a editar (modo EDIÇÃO). Use com `prompt`.
- `image_urls` (array, opcional): URLs das imagens a editar (modo EDIÇÃO batch). Use com `prompts` (mesmo tamanho).
- `output_format` (opcional): "png" ou "jpeg" (padrão: "png")
- `image_size` (opcional): "1:1", "16:9", "4:5", etc (padrão: **"4:5"**)
- `wait_for_completion` (opcional): true/false (padrão: true)
- `auto_download` (opcional): true/false (padrão: false)

**Exemplo:**
```python
# Sem download automático (apenas URLs)
result = await session.call_tool(
    "generate_image",
    arguments={
        "prompt": "A beautiful sunset over the ocean",
        "output_format": "png",
        "image_size": "16:9",
        "wait_for_completion": True
    }
)

# COM download automático ⚡
result = await session.call_tool(
    "generate_image",
    arguments={
        "prompt": "A beautiful sunset over the ocean",
        "auto_download": True  # 🔥 Baixa direto para Downloads
    }
)
```

**Resposta (sem download):**
```json
{
  "status": "success",
  "task_id": "abc123",
  "image_urls": ["https://tempfile.aiquickdraw.com/.../image.png"],
  "cost_time": 8,
  "consume_credits": 100
}
```

**Resposta (com auto_download=true):**
```json
{
  "status": "success",
  "task_id": "abc123",
  "image_urls": ["https://tempfile.aiquickdraw.com/.../image.png"],
  "cost_time": 8,
  "consume_credits": 100,
  "downloads": [
    {
      "url": "https://tempfile.aiquickdraw.com/.../image.png",
      "path": "/Users/você/Downloads/image_xxx.png",
      "filename": "image_xxx.png"
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
    "kieai-image-gen": {
      "command": "python3",
      "args": [
        "/caminho/completo/mcp-kieai-image-gen/server.py"
      ]
    }
  }
}
```

## 📊 Proporções Disponíveis

| Código | Proporção | Uso Típico |
|--------|-----------|------------|
| 1:1    | Quadrado  | Posts Instagram/Facebook |
| 16:9   | Paisagem  | YouTube, apresentações |
| 9:16   | Retrato   | Stories, TikTok |
| 4:3    | Paisagem  | Apresentações clássicas |
| 3:4    | Retrato   | Impressão |
| 21:9   | Ultralarga| Cinema, banners |

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

- Tempo médio de geração: 5-10 segundos
- Custo por imagem: ~100 créditos
- Timeout padrão: 60 segundos

## 📝 Changelog

### v1.0.0 (2025-11-05)
- ✅ Implementação inicial
- ✅ Suporte a generate_image
- ✅ Suporte a check_task_status
- ✅ Polling automático com timeout
- ✅ Documentação completa
