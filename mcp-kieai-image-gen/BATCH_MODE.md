# ⚡ Batch Mode - Geração Paralela

## 🎯 O Que É?

**Geração em Lote Paralela** = Criar **múltiplas imagens AO MESMO TEMPO**, não uma por uma.

```
MODO FILA (LENTO):
Imagem 1 → Aguarda → Imagem 2 → Aguarda → Imagem 3
   10s       10s        10s        10s       10s
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 30 segundos ❌


MODO PARALELO (RÁPIDO):
Imagem 1 ┐
Imagem 2 ├─→ Todas ao mesmo tempo
Imagem 3 ┘
   10s
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: ~12 segundos ✅ (1.9x mais rápido!)
```

---

## 🚀 Como Funciona

### Fase 1: Criação das Tasks (Rápido ~1s cada)

```
POST task_1 → task_id_1  ┐
POST task_2 → task_id_2  ├─→ Cria TODAS primeiro
POST task_3 → task_id_3  ┘
    ~3 segundos total
```

### Fase 2: Polling Paralelo (Assíncrono)

```
query(task_1) ┐
query(task_2) ├─→ Aguarda TODAS ao mesmo tempo
query(task_3) ┘
     ~10 segundos (todas juntas)
```

### Total

```
Fase 1 + Fase 2 = ~13s
vs
Sequencial = 3×10s = ~30s

Economia: 17s (57% mais rápido!)
```

---

## 📊 Capacidade

```
┌────────────────────────────────────────┐
│ LIMITES                                │
├────────────────────────────────────────┤
│ Mínimo: 1 imagem                       │
│ Máximo: 15 imagens                     │
│ Recomendado: 3-5 imagens              │
└────────────────────────────────────────┘
```

**Por que 15?**
- ✅ Limite seguro para não sobrecarregar a API
- ✅ Tempo de resposta razoável (~15-20s)
- ✅ Uso controlado de créditos

---

## 🎨 Exemplos de Uso

### 1 Imagem (Modo Normal)

```python
generate_image(
    prompt="Um gato fofo",
    auto_download=True
)
```

### 3 Imagens (Modo Batch)

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

### 10 Imagens (Batch Grande)

```python
generate_image(
    prompts=[
        "A cute fox in the forest",
        "A cat sleeping peacefully",
        "A dog running on the beach",
        "A bird flying in the sky",
        "A rabbit eating a carrot",
        "A lion roaring in the savanna",
        "A dolphin jumping in the ocean",
        "A butterfly on a flower",
        "A wolf howling at the moon",
        "A panda eating bamboo"
    ],
    auto_download=True
)
```

---

## 📈 Performance

### Teste Real: 3 Imagens

| Métrica | Valor |
|---------|-------|
| Tempo sequencial (estimado) | ~32s |
| Tempo paralelo (real) | 17s |
| Aceleração | 1.9x mais rápido |
| Economia | 15s (47%) |

### Projeção: 10 Imagens

| Métrica | Valor |
|---------|-------|
| Tempo sequencial | ~100s (1min 40s) |
| Tempo paralelo | ~15-20s |
| Aceleração | ~5-6x mais rápido |
| Economia | ~80s (80%!) |

### Projeção: 15 Imagens

| Métrica | Valor |
|---------|-------|
| Tempo sequencial | ~150s (2min 30s) |
| Tempo paralelo | ~20-25s |
| Aceleração | ~6-7x mais rápido |
| Economia | ~125s (83%!) |

---

## 🔍 Resposta do Batch Mode

```json
{
  "mode": "batch_parallel",
  "total": 3,
  "successful": 3,
  "failed": 0,
  "total_time": 32,
  "results": [
    {
      "status": "success",
      "prompt": "Um gato fofo",
      "task_id": "abc123",
      "image_urls": ["https://..."],
      "cost_time": 10,
      "downloads": [{
        "filename": "gato_fofo_xyz.png",
        "path": "/Users/você/Downloads/gato_fofo_xyz.png"
      }]
    },
    {
      "status": "success",
      "prompt": "Um cachorro brincando",
      ...
    },
    ...
  ]
}
```

---

## 🎯 Casos de Uso

### 📱 Posts para Redes Sociais

Gere 5 variações de uma vez:

```python
prompts=[
    "Social media post about coffee - minimalist style",
    "Social media post about coffee - colorful style",
    "Social media post about coffee - dark moody style",
    "Social media post about coffee - bright morning style",
    "Social media post about coffee - vintage style"
]
```

**Resultado:** 5 opções em ~15s (vs ~50s sequencial)

### 🎨 Variações de Design

Teste múltiplos estilos:

```python
prompts=[
    "Logo for tech startup - modern minimalist",
    "Logo for tech startup - geometric shapes",
    "Logo for tech startup - gradient colorful"
]
```

### 📚 Ilustrações para Apresentação

Gere todas as imagens de uma vez:

```python
prompts=[
    "Introduction slide background - professional",
    "Data visualization background - charts",
    "Team collaboration illustration",
    "Success celebration illustration",
    "Future vision illustration - innovation"
]
```

---

## ⚙️ Como Detecta Single vs Batch

```python
# Server detecta automaticamente:

# Se recebe "prompt" → Modo Single
arguments = {"prompt": "Um gato"}

# Se recebe "prompts" → Modo Batch Paralelo
arguments = {"prompts": ["Gato", "Cachorro", "Raposa"]}
```

**Você não precisa fazer nada diferente!** O servidor escolhe automaticamente.

---

## 💡 Dicas de Performance

### ✅ Boas Práticas

```python
# Use batch para 2+ imagens
prompts=["Imagem 1", "Imagem 2", "Imagem 3"]

# Sempre use auto_download=True
auto_download=True

# Prefira 3-5 imagens por lote
# (melhor custo-benefício)
```

### ❌ Evite

```python
# NÃO faça loop manual (lento!)
for prompt in prompts:
    generate_image(prompt=prompt)  # ❌ Uma por vez

# Use batch em vez disso:
generate_image(prompts=prompts)  # ✅ Todas juntas
```

---

## 🧪 Testes Realizados

```
✅ 3 imagens em paralelo: 17s (vs 32s)
✅ Nomes em português funcionando
✅ Downloads automáticos funcionando
✅ Proporção 4:5 padrão aplicada
✅ asyncio.sleep (não bloqueante) ✅
```

---

## 🎉 Vantagens

| Aspecto | Single | Batch Paralelo |
|---------|--------|----------------|
| 1 imagem | 10s | 10s (igual) |
| 3 imagens | 30s | ~17s (1.9x) |
| 10 imagens | 100s | ~20s (5x) |
| 15 imagens | 150s | ~25s (6x) |

**Quanto mais imagens, maior a economia!**

---

## 🚀 Próximos Testes

Rode:
```bash
/opt/homebrew/bin/python3.11 test_batch_10.py
```

Para testar 10 imagens em paralelo e ver a economia real de tempo!

---

**Versão:** 2.1.0 (Batch Parallel)
**Limite:** 1-15 imagens
**Método:** asyncio.gather + async sleep
