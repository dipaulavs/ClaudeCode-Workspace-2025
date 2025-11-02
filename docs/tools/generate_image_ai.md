# 🎨 DALL-E 3 Image Generator

Gera imagens usando DALL-E 3 oficial da OpenAI com prompt revisado automaticamente.

## 🚀 Comando

```bash
python3 tools/generate_image_ai.py "prompt" [opções]
```

## 📝 Parâmetros

| Parâmetro | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `prompt` | ✅ | Descrição da imagem a ser gerada |
| `--size` | ❌ | Tamanho da imagem. Padrão: 1024x1024 |
| `--quality` | ❌ | Qualidade (standard ou hd). Padrão: standard |
| `--output` | ❌ | Diretório de saída. Padrão: ~/Downloads |
| `--api-key` | ❌ | OpenAI API Key (ou use variável de ambiente) |

## 📐 Tamanhos Disponíveis (--size)

- `1024x1024` - Quadrado (padrão)
- `1792x1024` - Landscape (horizontal)
- `1024x1792` - Portrait (vertical)

## ✨ Qualidades Disponíveis (--quality)

- `standard` - Qualidade padrão, mais rápido (padrão)
- `hd` - Alta definição, mais detalhado

## 💡 Exemplos

```bash
# Geração básica (quadrado)
python3 tools/generate_image_ai.py "gato astronauta flutuando no espaço"

# Landscape (horizontal)
python3 tools/generate_image_ai.py "paisagem montanhosa ao pôr do sol" --size 1792x1024

# Portrait (vertical)
python3 tools/generate_image_ai.py "retrato de mulher elegante" --size 1024x1792

# Alta qualidade
python3 tools/generate_image_ai.py "cidade cyberpunk à noite" --quality hd

# Landscape HD
python3 tools/generate_image_ai.py "floresta mágica com luzes" --size 1792x1024 --quality hd

# Diretório customizado
python3 tools/generate_image_ai.py "logo minimalista" --output ~/Projetos/logos

# Com API key explícita
python3 tools/generate_image_ai.py "arte abstrata" --api-key sk-proj-xxxxx
```

## 📦 Saída

- **Local:** `~/Downloads/` (ou diretório especificado)
- **Nome:** `ai_generated_YYYYMMDD_HHMMSS.png`
- **Formato:** PNG (sempre)
- **Tamanho:** Varia por resolução (média 200-500 KB)

## ⚙️ Configuração

### Variável de Ambiente (Recomendado)

```bash
# Adicionar ao ~/.bashrc ou ~/.zshrc
export OPENAI_API_KEY='sk-proj-xxxxxxxxxxxx'

# Ou definir temporariamente
export OPENAI_API_KEY='sk-proj-xxxxxxxxxxxx'
python3 tools/generate_image_ai.py "imagem"
```

### Via Parâmetro

```bash
python3 tools/generate_image_ai.py "imagem" --api-key sk-proj-xxxxxxxxxxxx
```

## 📊 Performance

- **Tempo:** Varia (geralmente 10-30s)
- **Qualidade:** Máxima (DALL-E 3 oficial)
- **Prompt revisado:** Sim (IA melhora seu prompt automaticamente)
- **Limite:** 1 imagem por requisição

## 🎯 Funcionalidades Especiais

### Prompt Revisado

A IA da OpenAI automaticamente refina seu prompt para gerar melhores resultados:

```
📝 Seu prompt: "gato astronauta"

📝 Prompt revisado pela IA:
"A realistic depiction of a feline astronaut, adorned in a
detailed spacesuit complete with helmet, floating gracefully
in the cosmic void filled with distant stars and nebulae."
```

O prompt revisado é exibido no console após a geração.

### Tamanhos Otimizados

- **1024x1024:** Ideal para posts quadrados, logos, ícones
- **1792x1024:** Perfeito para banners, headers, capas
- **1024x1792:** Ótimo para stories, reels, posts verticais

### Qualidade HD

O modo `--quality hd` gera:
- Mais detalhes e texturas
- Melhor resolução de elementos pequenos
- Cores mais ricas
- Tempo de processamento um pouco maior

## 💡 Dicas de Uso

### Prompts Efetivos

```bash
# ✅ BOM - Específico e descritivo
python3 tools/generate_image_ai.py "retrato fotorrealista de uma mulher de 30 anos, cabelos castanhos, sorriso suave, iluminação natural, fundo desfocado"

# ❌ RUIM - Vago demais
python3 tools/generate_image_ai.py "mulher bonita"
```

### Casos de Uso

**Marketing/Branding:**
```bash
python3 tools/generate_image_ai.py "logo minimalista para empresa de tecnologia, azul e branco, clean" --size 1024x1024 --quality hd
```

**Social Media:**
```bash
python3 tools/generate_image_ai.py "post motivacional, amanhecer nas montanhas, cores vibrantes" --size 1024x1024
```

**Banners/Headers:**
```bash
python3 tools/generate_image_ai.py "banner futurista para site tech, roxo e preto, elementos digitais" --size 1792x1024 --quality hd
```

**Stories/Reels:**
```bash
python3 tools/generate_image_ai.py "fundo abstrato colorido para story de produto" --size 1024x1792
```

## 🆚 Comparação com Outras Ferramentas

| Aspecto | DALL-E 3 | GPT-4o Image | Nano Banana |
|---------|----------|--------------|-------------|
| Qualidade | Máxima | 10/10 | 5/5 |
| Velocidade | 10-30s | 10-15s | 6s |
| Tamanhos | 3 opções | 2:3 fixo | 2:3 fixo |
| Qualidade HD | Sim | Não | Não |
| Variações | Não | Sim (1-4) | Não |
| Prompt Revisado | Sim | Opcional | Não |
| API | OpenAI oficial | Kie.ai | Kie.ai |
| Custo | Pago (OpenAI) | Incluído Kie | Incluído Kie |
| Uso ideal | Profissional | Lote/Variações | Rápido |

## 🔑 Obtendo API Key

1. Acesse: https://platform.openai.com/api-keys
2. Faça login ou crie conta
3. Clique em "Create new secret key"
4. Copie a key (começa com `sk-proj-`)
5. Configure como variável de ambiente

## ⚠️ Erros Comuns

### API Key não encontrada
```bash
❌ OPENAI_API_KEY não encontrada!
💡 Configure: export OPENAI_API_KEY='sua-chave'
```

**Solução:**
```bash
export OPENAI_API_KEY='sk-proj-xxxxxxxxxxxx'
```

### Erro 401 (Unauthorized)
- Verifique se a API key está correta
- Confirme que tem créditos na conta OpenAI

### Erro 429 (Rate Limit)
- Aguarde alguns segundos entre requisições
- Verifique limites da sua conta OpenAI

## 📖 Recursos Adicionais

- **Docs OpenAI:** https://platform.openai.com/docs/guides/images
- **Pricing:** https://openai.com/pricing
- **Best Practices:** Use prompts detalhados e específicos para melhores resultados
