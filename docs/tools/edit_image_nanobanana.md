# ✏️ Nano Banana Image Editor

Edita imagens existentes usando IA (Gemini 2.5 Flash Image Preview) com processamento inteligente.

## 🚀 Comando

```bash
python3 tools/edit_image_nanobanana.py caminho/da/imagem.jpg "prompt de edição" [opções]
```

**OU usar URL diretamente:**

```bash
python3 tools/edit_image_nanobanana.py --url https://exemplo.com/imagem.jpg "prompt de edição" [opções]
```

## 📝 Parâmetros

| Parâmetro | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `image_source` | ✅ | Caminho da imagem local (se não usar --url) |
| `prompt` | ✅ | Descrição da edição a ser feita |
| `--url` | ❌ | URL da imagem (alternativa ao caminho local) |
| `--format` | ❌ | Formato de saída (PNG ou JPEG). Padrão: PNG |
| `--size` | ❌ | Proporção da imagem. Padrão: auto |
| `--expire-days` | ❌ | Dias até expiração do link Nextcloud. Padrão: 1 |

## 🎨 Proporções Disponíveis (--size)

- `1:1` - Quadrado
- `2:3` - Portrait
- `3:2` - Landscape
- `3:4` - Portrait moderado
- `4:3` - Landscape moderado
- `4:5` - Portrait vertical
- `5:4` - Landscape horizontal
- `9:16` - Vertical (Stories)
- `16:9` - Horizontal (Widescreen)
- `21:9` - Ultra-wide
- `auto` - Detecta automaticamente (padrão)

## 💡 Exemplos

```bash
# Adicionar elementos à imagem
python3 tools/edit_image_nanobanana.py foto.jpg "adicionar flores coloridas no fundo"

# Remover objeto
python3 tools/edit_image_nanobanana.py imagem.png "remover o cachorro da foto"

# Mudar cores/estilo
python3 tools/edit_image_nanobanana.py retrato.jpg "tornar preto e branco com efeito vintage"

# Editar com proporção específica
python3 tools/edit_image_nanobanana.py paisagem.jpg "adicionar pôr do sol dramático" --size 16:9

# Usar URL diretamente
python3 tools/edit_image_nanobanana.py --url https://exemplo.com/foto.jpg "adicionar óculos de sol na pessoa"

# Salvar como JPEG
python3 tools/edit_image_nanobanana.py foto.png "adicionar fundo desfocado" --format JPEG

# Edição com link de 7 dias
python3 tools/edit_image_nanobanana.py imagem.jpg "trocar cor do carro para vermelho" --expire-days 7
```

## 📦 Saída

- **Local:** `~/Downloads/`
- **Nome:**
  - 1 imagem: `nanobanana_edited_YYYYMMDD_HHMMSS.png`
  - Múltiplas: `nanobanana_edited_YYYYMMDD_HHMMSS_v1.png`, `v2.png`, etc.
- **Formato:** Configurável (PNG ou JPEG)
- **Proporção:** Configurável ou auto-detectada

## ⚙️ Configuração

- **API:** Kie.ai (Nano Banana Edit)
- **Key:** Configurada no script
- **Modelo:** `google/nano-banana-edit`
- **Upload:** Nextcloud (automático para imagens locais)

## 📊 Performance

- **Tempo:** 18-26s (inclui upload + processamento)
- **Qualidade:** 5/5 (edições realistas)
- **Upload automático:** Sim (para arquivos locais)
- **Suporte a URLs:** Sim (pula upload)

## 🎯 Como Funciona

Para **imagens locais:**
1. Upload automático para Nextcloud (gera URL temporária)
2. Envia URL + prompt para API de edição
3. Aguarda processamento (IA edita a imagem)
4. Baixa resultado editado para Downloads

Para **URLs externas:**
1. Usa URL fornecida diretamente
2. Envia para API de edição
3. Aguarda processamento
4. Baixa resultado editado

## 💡 Casos de Uso

### Adição de Elementos
```bash
# Adicionar objetos
python3 tools/edit_image_nanobanana.py foto.jpg "adicionar chapéu na pessoa"

# Adicionar efeitos
python3 tools/edit_image_nanobanana.py paisagem.jpg "adicionar névoa e raios de luz"
```

### Remoção de Elementos
```bash
# Remover objetos
python3 tools/edit_image_nanobanana.py foto.jpg "remover texto da imagem"

# Limpar fundo
python3 tools/edit_image_nanobanana.py produto.png "remover fundo, deixar apenas o produto"
```

### Modificações de Estilo
```bash
# Filtros artísticos
python3 tools/edit_image_nanobanana.py foto.jpg "transformar em aquarela"

# Ajustes de cor
python3 tools/edit_image_nanobanana.py imagem.jpg "aumentar saturação e contraste"
```

### Transformações
```bash
# Mudar tempo/clima
python3 tools/edit_image_nanobanana.py paisagem.jpg "transformar em cena noturna com lua cheia"

# Substituir elementos
python3 tools/edit_image_nanobanana.py sala.jpg "trocar sofá por um sofá moderno azul"
```

## 🛡️ Segurança

- Upload via Nextcloud com links temporários
- Expiração padrão: 1 dia (configurável)
- Links públicos mas únicos/não-guessable
- Imagens locais não ficam permanentemente hospedadas

## 🆚 Quando Usar

**Use Nano Banana Edit quando:**
- Precisar modificar imagens existentes
- Quiser adicionar/remover elementos
- Necessitar mudar estilos/cores
- Tiver foto base para trabalhar

**Use geradores (GPT-4o/Nano Banana) quando:**
- Criar imagens do zero
- Não tiver imagem de referência
- Precisar apenas de prompt
