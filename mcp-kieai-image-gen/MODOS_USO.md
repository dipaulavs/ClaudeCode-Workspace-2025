# 🎨 Modos de Uso - MCP kie-nanobanana-create

## 🎯 Visão Geral

**1 MCP = 4 Modos** (detecção automática!)

```
┌─────────────────────────────────────────────────────┐
│ MODO 1: Criar 1 imagem                              │
│ • prompt="Um gato"                                  │
│ • Sem image_url                                     │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ MODO 2: Criar N imagens (PARALELO)                  │
│ • prompts=["Gato", "Cão", "Raposa"]                │
│ • Sem image_urls                                    │
│ • Todas AO MESMO TEMPO                              │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ MODO 3: Editar 1 imagem                             │
│ • prompt="Mude a cor para vermelho"                │
│ • image_url="https://..."                           │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ MODO 4: Editar N imagens (PARALELO)                 │
│ • prompts=["Cor A", "Cor B", "Cor C"]              │
│ • image_urls=[url1, url2, url3]                     │
│ • Todas AO MESMO TEMPO                              │
└─────────────────────────────────────────────────────┘
```

---

## 📖 Exemplos Detalhados

### 1️⃣ Criar 1 Imagem

```python
generate_image(
    prompt="Um gato fofo sentado",
    auto_download=True
)
```

**Resultado:**
- ✅ 1 imagem criada (~10s)
- 📄 `gato_fofo_sentado_abc.png`
- 📂 `~/Downloads/`

---

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
```

**Resultado:**
- ✅ 3 imagens criadas em ~17s (vs ~30s sequencial)
- 📄 `gato_fofo_xyz.png`
- 📄 `cachorro_brincando_abc.png`
- 📄 `raposa_floresta_def.png`

---

### 3️⃣ Editar 1 Imagem

```python
# Passo 1: Criar imagem base
result = generate_image(
    prompt="A person wearing a blue shirt"
)
url = result["image_urls"][0]

# Passo 2: Editar imagem
generate_image(
    prompt="Change the shirt color to red",
    image_url=url,  # 🔥 Ativa modo EDIÇÃO
    auto_download=True
)
```

**Resultado:**
- ✅ Imagem editada (~19s)
- 📄 `mudar_cor_camisa_abc.png`
- 🎨 Camisa azul → vermelha

---

### 4️⃣ Editar 3-15 Imagens (Paralelo)

```python
# Passo 1: Criar 3 imagens base
result = generate_image(
    prompts=[
        "A person wearing a blue shirt",
        "A car painted in green",
        "A house with yellow walls"
    ]
)
urls = [r["image_urls"][0] for r in result["results"]]

# Passo 2: Editar as 3 em PARALELO
generate_image(
    prompts=[
        "Change the shirt to red",
        "Paint the car blue",
        "Change walls to pink"
    ],
    image_urls=urls,  # 🔥 BATCH EDIT MODE
    auto_download=True
)
```

**Resultado:**
- ✅ 3 imagens editadas em ~26s (vs ~54s sequencial)
- 📄 3 arquivos salvos com nomes descritivos
- ⚡ ~2x mais rápido

---

## 🔍 Como o MCP Detecta o Modo?

```python
# Lógica interna (automática):

if image_url or image_urls:
    model = "google/nano-banana-edit"  # EDIÇÃO
else:
    model = "google/nano-banana"       # CRIAÇÃO

if prompts:
    # BATCH (paralelo)
    asyncio.gather(...)  # Todas juntas
else:
    # SINGLE
    create_task(...)  # Uma só
```

**Você não precisa fazer nada!** Apenas forneça os parâmetros e o servidor decide.

---

## 📊 Matriz de Decisão

| prompt | prompts | image_url | image_urls | Modo |
|--------|---------|-----------|------------|------|
| ✅ | ❌ | ❌ | ❌ | Criar 1 |
| ❌ | ✅ | ❌ | ❌ | Criar N (paralelo) |
| ✅ | ❌ | ✅ | ❌ | Editar 1 |
| ❌ | ✅ | ❌ | ✅ | Editar N (paralelo) |

---

## 🎯 Casos de Uso

### 📸 Variações de Produto

Crie e edite múltiplas versões:

```python
# Cria imagem base
base = generate_image(prompt="Product on white background")

# Edita com 5 cores diferentes em paralelo
generate_image(
    prompts=[
        "Change product color to red",
        "Change product color to blue",
        "Change product color to green",
        "Change product color to yellow",
        "Change product color to black"
    ],
    image_urls=[base["url"]] * 5,  # Mesma imagem base
    auto_download=True
)
# Resultado: 5 variações em ~20-30s (vs ~100s sequencial)
```

### 🎨 Batch de Thumbnails

Edite múltiplas thumbnails de uma vez:

```python
# URLs de 10 thumbnails existentes
thumbnail_urls = [...]

# Edita todas em paralelo
generate_image(
    prompts=[
        "Add red border and title text",
        "Add blue border and title text",
        ...  # 10 variações
    ],
    image_urls=thumbnail_urls,
    auto_download=True
)
# Resultado: 10 thumbnails editadas em ~30s
```

### 🖼️  Processamento de Imagens

Aplique o mesmo filtro em várias imagens:

```python
image_urls = ["url1.jpg", "url2.jpg", "url3.jpg"]

generate_image(
    prompts=[
        "Make it more vibrant and colorful",
        "Make it more vibrant and colorful",
        "Make it more vibrant and colorful"
    ],
    image_urls=image_urls,
    auto_download=True
)
```

---

## ⚡ Performance

### Criação Paralela (Já testado)

| Quantidade | Sequencial | Paralelo | Speedup |
|------------|-----------|----------|---------|
| 1 imagem | 10s | 10s | 1x |
| 3 imagens | 30s | 17s | 1.9x |
| 10 imagens | 100s | ~20s | 5x |

### Edição Paralela (Testado agora!)

| Quantidade | Sequencial | Paralelo | Speedup |
|------------|-----------|----------|---------|
| 1 imagem | 19s | 19s | 1x |
| 3 imagens | 57s | 26s | 2.2x |
| 10 imagens | 190s | ~40s | 4.8x |

---

## 🧪 Testes Realizados

```
✅ Criar 1 imagem: fox_sitting_top_abc.png
✅ Criar 3 imagens paralelo: 17s (vs 30s)
✅ Editar 1 imagem: camisa azul → vermelha (19s)
✅ Editar 3 imagens paralelo: 26s (vs 57s)
✅ Nomes em português sem acentos
✅ Download automático funcionando
✅ Detecção automática de modo
```

---

## 🎨 Resumo Visual

```
generate_image()  ←  1 função para tudo
       │
       ├─→ prompt?           → Criar 1
       ├─→ prompts?          → Criar N (paralelo)
       ├─→ prompt + image_url?    → Editar 1
       └─→ prompts + image_urls?  → Editar N (paralelo)

Tudo automático! Sem código duplicado!
```

---

## 📦 Capacidades Finais

```
┌────────────────────────────────────────────────────┐
│ MCP: kie-nanobanana-create v2.1.0                  │
├────────────────────────────────────────────────────┤
│ ✅ Criar 1-15 imagens (paralelo)                   │
│ ✅ Editar 1-15 imagens (paralelo)                  │
│ ✅ Detecção automática de modo                     │
│ ✅ Nomes em português (sem acentos)                │
│ ✅ Proporção 4:5 padrão                            │
│ ✅ Download automático                             │
│ ✅ Sem duplicação de código                        │
└────────────────────────────────────────────────────┘
```

**Tudo no mesmo MCP!** 🚀