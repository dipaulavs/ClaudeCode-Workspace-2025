# 🎨 GPT-4o Image Generator

Gera imagens usando GPT-4o via Kie.ai (portrait 2:3).

## 🚀 Comando

```bash
python3 tools/generate_image.py "prompt" [--variants 1|2|4] [--enhance]
```

## 📝 Parâmetros

| Parâmetro | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `prompt` | ✅ | Descrição da imagem em português ou inglês |
| `--variants` | ❌ | Número de variações (1, 2 ou 4). Padrão: 1 |
| `--enhance` | ❌ | Refina prompt automaticamente via IA |

## 💡 Exemplos

```bash
# Básico
python3 tools/generate_image.py "mulher cyberpunk com óculos neon"

# Com variações
python3 tools/generate_image.py "pôr do sol nas montanhas" --variants 4

# Com refinamento de prompt
python3 tools/generate_image.py "gato astronauta" --enhance
```

## 📦 Saída

- **Local:** `~/Downloads/`
- **Nome:** `descricao_do_conteudo_xyz1.png` (português, código aleatório)
- **Formato:** Portrait 2:3

## ⚙️ Config

- **API:** Kie.ai (GPT-4o)
- **Key:** Configurada no script
