# 🍌 Nano Banana Batch Generator

Gera múltiplas imagens simultaneamente usando Nano Banana (Gemini 2.5 Flash) em modo paralelo.

## 🚀 Comando

```bash
python3 tools/generate_image_batch.py "prompt1" "prompt2" "prompt3" [--format FORMAT]
```

## 📝 Parâmetros

| Parâmetro | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `prompt1 prompt2 ...` | ✅ | Lista de prompts (múltiplos prompts separados por espaço) |
| `--format` | ❌ | Formato da imagem (PNG ou JPEG). Padrão: PNG |

## 💡 Exemplos

```bash
# Gerar 3 imagens em paralelo
python3 tools/generate_image_batch.py "gato astronauta" "cachorro pirata" "pássaro robô"

# Gerar múltiplas paisagens em JPEG
python3 tools/generate_image_batch.py "floresta tropical" "deserto ao pôr do sol" "montanhas nevadas" --format JPEG

# Gerar 4 imagens de produtos
python3 tools/generate_image_batch.py "telefone futurista" "computador minimalista" "relógio elegante" "câmera vintage"
```

## 📦 Saída

- **Local:** `~/Downloads/`
- **Nome:** `batch_[descricao]_YYYYMMDD_HHMMSS.png` (timestamp único)
- **Formato:** Portrait 2:3
- **Qualidade:** Hiper-realismo, física consciente (Gemini 2.5 Flash)

## ⚙️ Configuração

- **API:** Kie.ai (Nano Banana)
- **Key:** Configurada no script
- **Modelo:** `google/nano-banana`

## 📊 Performance

- **Tempo:** ~6s por imagem
- **Qualidade:** 5/5 (hiper-realismo)
- **Velocidade:** 60% mais rápido que geração sequencial
- **Processamento:** Paralelo (todas as tarefas criadas simultaneamente)

## 🎯 Como Funciona

O script opera em 2 fases:

1. **Fase 1 - Criação:** Cria todas as tarefas de geração simultaneamente
2. **Fase 2 - Download:** Monitora todas as tarefas em paralelo e baixa conforme concluem

Isso resulta em geração muito mais rápida que processar uma imagem por vez.

## 💡 Dicas

- Use prompts descritivos para melhores resultados
- Todas as imagens são geradas em portrait (2:3) automaticamente
- O nome do arquivo contém parte do prompt (primeiros 30 caracteres)
- PNG é recomendado para melhor qualidade
- JPEG é mais leve para web/compartilhamento
