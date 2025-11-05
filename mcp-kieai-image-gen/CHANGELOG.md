# 📋 Changelog - MCP KIE.AI Image Generator

## 🎉 v2.0.0 (2025-11-05) - Melhorias Inteligentes

### ✨ Novas Funcionalidades

#### 1. 📝 Nomes de Arquivo Descritivos Automáticos

**Antes:**
```
image_1762352617073_t6wzla_1x1_1024x1024.png
```

**Depois:**
```
fox_sitting_top_e4q.png
cat_sleeping_soft_z4h.png
robot_big_eyes_x9k.png
```

**Como funciona:**
- Extrai palavras-chave do prompt
- Remove palavras comuns (the, a, cute, beautiful, etc)
- Pega 2-3 palavras principais
- Adiciona código aleatório de 3 caracteres
- Limita a 30 caracteres

**Exemplos:**

| Prompt | Nome do Arquivo |
|--------|----------------|
| "A cute fox sitting on top of a wooden table" | `fox_sitting_top_abc.png` |
| "A cat sleeping on a soft pillow" | `cat_sleeping_soft_xyz.png` |
| "A beautiful sunset over the ocean" | `sunset_ocean_def.png` |
| "A futuristic city with neon lights" | `futuristic_city_neon_ghi.png` |

#### 2. 📐 Proporção 4:5 Como Padrão

**Antes:** Padrão era 1:1 (quadrado)

**Depois:** Padrão é 4:5 (vertical/retrato)

**Por quê?**
- ✅ Ideal para stories (Instagram, TikTok)
- ✅ Melhor para retratos
- ✅ Formato mais versátil
- ✅ Ocupa mais espaço em feeds verticais

**Dimensões reais:** 896 x 1152 pixels (proporção ~4:5)

**Ainda pode mudar:**
```python
# Usar outra proporção quando quiser
generate_image(
    prompt="...",
    image_size="16:9"  # paisagem
)
```

---

## 📊 Comparação Antes vs Depois

### Antes (v1.0.0)

```python
result = generate_image("A fox on a table", auto_download=True)

# Resultado:
{
  "downloads": [{
    "filename": "image_1762352617073_t6wzla_1x1_1024x1024.png",
    "path": "~/Downloads/image_1762352617073_t6wzla_1x1_1024x1024.png"
  }]
}
```

**Problemas:**
- ❌ Nome do arquivo não diz nada sobre a imagem
- ❌ Difícil de encontrar depois
- ❌ Proporção 1:1 pode não ser ideal

### Depois (v2.0.0)

```python
result = generate_image("A fox on a table", auto_download=True)

# Resultado:
{
  "downloads": [{
    "filename": "fox_table_e4q.png",
    "path": "~/Downloads/fox_table_e4q.png"
  }]
}
```

**Melhorias:**
- ✅ Nome descritivo e curto
- ✅ Fácil de encontrar e identificar
- ✅ Proporção 4:5 (vertical) por padrão

---

## 🎯 Como os Nomes São Gerados

### Passo a Passo

```
Prompt: "A cute fox sitting on top of a wooden table, photorealistic"
           ↓
1. Remove pontuação e lowercase
   "a cute fox sitting on top of a wooden table photorealistic"
           ↓
2. Remove stopwords (a, cute, on, of, photorealistic)
   "fox sitting top wooden table"
           ↓
3. Pega primeiras 2-3 palavras
   "fox sitting top"
           ↓
4. Adiciona código aleatório (3 chars)
   "fox_sitting_top_e4q"
           ↓
5. Adiciona extensão
   "fox_sitting_top_e4q.png"
```

### Stopwords Removidas

Palavras que não ajudam a identificar a imagem:
- Artigos: a, an, the
- Preposições: in, on, at, of, for, with
- Verbos auxiliares: is, are, was, were, be
- Qualificadores genéricos: cute, beautiful, nice, pretty
- Técnicos: digital, art, photorealistic, lighting

---

## 📐 Proporções Disponíveis

| Proporção | Uso | Dimensões* | Padrão? |
|-----------|-----|------------|---------|
| 4:5 | Stories, Retratos | 896 x 1152 | ✅ SIM |
| 1:1 | Posts quadrados | 1024 x 1024 | ❌ |
| 16:9 | Paisagem, YouTube | 1024 x 576 | ❌ |
| 9:16 | Stories verticais | 576 x 1024 | ❌ |
| 3:4 | Fotos tradicionais | 768 x 1024 | ❌ |

\* Dimensões aproximadas (a API pode ajustar)

---

## 🔧 Configuração

### Usar Padrões (Recomendado)

```python
# Usa 4:5 + nome descritivo automaticamente
result = generate_image(
    prompt="A cat sleeping",
    auto_download=True
)
# → cat_sleeping_abc.png (896x1152)
```

### Customizar Proporção

```python
# Força 16:9 (paisagem)
result = generate_image(
    prompt="A mountain landscape",
    image_size="16:9",
    auto_download=True
)
# → mountain_landscape_xyz.png (1024x576)
```

### Customizar Nome

```python
# Baixa depois com nome personalizado
result = generate_image(prompt="A sunset")
url = result["image_urls"][0]

download_image(url, filename="meu_por_do_sol.png")
# → meu_por_do_sol.png
```

---

## ✅ Testes Realizados

### Teste 1: Nome Descritivo
```bash
Prompt: "A fox sitting on top of a wooden table"
Resultado: fox_sitting_top_e4q.png ✅
```

### Teste 2: Proporção Padrão
```bash
Proporção solicitada: (não especificada)
Proporção gerada: 896 x 1152 (4:5) ✅
```

### Teste 3: Download Automático
```bash
auto_download: True
Arquivo salvo: ~/Downloads/fox_sitting_top_e4q.png ✅
Tamanho: 1.5 MB ✅
```

---

## 📦 Arquivos Modificados

```
mcp-kieai-image-gen/
├── server.py                    # ✅ Atualizado
│   ├── create_descriptive_filename()  # NOVO
│   ├── download_image()               # Melhorado
│   └── image_size default = "4:5"     # Alterado
├── test_improvements.py         # ✅ NOVO
├── CHANGELOG.md                 # ✅ NOVO
└── README.md                    # (precisa atualizar)
```

---

## 🐛 Possíveis Problemas

### Nome muito genérico
**Problema:** Prompt só tem stopwords
**Solução:** Usa as primeiras 2 palavras do prompt

**Exemplo:**
```python
# Prompt ruim
"A beautiful cute nice image"
# Nome: beautiful_cute_abc.png

# Prompt bom
"Mountain sunset landscape"
# Nome: mountain_sunset_landscape_xyz.png
```

### Código aleatório duplicado (raro)
**Probabilidade:** ~1 em 46.656 (36³)
**Solução:** Código tem 3 caracteres aleatórios
**Impacto:** Mínimo (arquivo seria sobrescrito)

---

## 🚀 Próximas Melhorias (Futuro)

- [ ] Detecção automática de idioma do prompt
- [ ] Tradução de nomes para português
- [ ] Suporte a múltiplas resoluções
- [ ] Cache de imagens geradas
- [ ] Batch generation otimizado

---

**Versão:** 2.0.0
**Data:** 2025-11-05
**Status:** ✅ Produção
