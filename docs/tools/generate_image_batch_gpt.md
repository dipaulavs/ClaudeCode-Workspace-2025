# 🎨 GPT-4o Batch Generator

Gera múltiplas imagens simultaneamente usando GPT-4o via Kie.ai em modo paralelo, com suporte a variações.

## 🚀 Comando

```bash
python3 tools/generate_image_batch_gpt.py "prompt1" "prompt2" "prompt3" [opções]
```

## 📝 Parâmetros

| Parâmetro | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `prompt1 prompt2 ...` | ✅ | Lista de prompts (múltiplos prompts separados por espaço) |
| `--variants` | ❌ | Número de variações por prompt (1, 2 ou 4). Padrão: 1 |
| `--enhance` | ❌ | Ativa refinamento automático do prompt via IA |

## 💡 Exemplos

```bash
# Gerar 3 imagens diferentes
python3 tools/generate_image_batch_gpt.py "gato astronauta" "cachorro pirata" "pássaro robô"

# Gerar 2 prompts com 2 variações cada (total: 4 imagens)
python3 tools/generate_image_batch_gpt.py "paisagem montanhosa" "cidade futurista" --variants 2

# Gerar com refinamento de prompt
python3 tools/generate_image_batch_gpt.py "arte abstrata" "retrato realista" --enhance

# Gerar múltiplas variações com refinamento (2 prompts × 4 variações = 8 imagens)
python3 tools/generate_image_batch_gpt.py "logo minimalista" "banner moderno" --variants 4 --enhance
```

## 📦 Saída

- **Local:** `~/Downloads/`
- **Nome:**
  - 1 variação: `batch_gpt_[descricao]_YYYYMMDD_HHMMSS.png`
  - Múltiplas: `batch_gpt_[descricao]_YYYYMMDD_HHMMSS_v1.png`, `v2.png`, etc.
- **Formato:** Portrait 2:3
- **Qualidade:** Máxima (GPT-4o Image)

## ⚙️ Configuração

- **API:** Kie.ai (GPT-4o Image)
- **Key:** Configurada no script
- **Endpoint:** `/api/v1/gpt4o-image/generate`

## 📊 Performance

- **Tempo:** 10-15s por imagem (em paralelo)
- **Qualidade:** 10/10 (qualidade superior)
- **Processamento:** Paralelo (todas as tarefas criadas simultaneamente)
- **Variações:** Suporta 1, 2 ou 4 variações por prompt

## 🎯 Como Funciona

O script opera em 2 fases otimizadas:

1. **Fase 1 - Criação:** Cria todas as tarefas de geração simultaneamente
2. **Fase 2 - Download:** Monitora todas as tarefas em paralelo e baixa conforme concluem

### Exemplo de Escala:

- **1 prompt, 4 variações:** 4 imagens em ~15s
- **3 prompts, 2 variações:** 6 imagens em ~15s
- **4 prompts, 1 variação:** 4 imagens em ~15s

Todas processadas em paralelo para máxima eficiência.

## 💡 Dicas

- Use `--variants 4` para explorar diferentes interpretações do mesmo prompt
- `--enhance` melhora automaticamente prompts vagos ou curtos
- GPT-4o gera imagens mais detalhadas e precisas que Nano Banana
- Ideal para trabalhos profissionais e alta qualidade
- O nome do arquivo contém parte do prompt (primeiros 30 caracteres)

## 🆚 Comparação com Nano Banana

| Aspecto | GPT-4o Batch | Nano Banana Batch |
|---------|--------------|-------------------|
| Qualidade | 10/10 | 5/5 |
| Velocidade | 10-15s/img | 6s/img |
| Variações | Sim (1, 2, 4) | Não |
| Enhance | Sim | Não |
| Custo | Incluído API | Incluído API |
| Uso | Profissional | Rápido/Casual |
