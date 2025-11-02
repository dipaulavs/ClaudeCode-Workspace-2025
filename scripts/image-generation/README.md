# 🎨 Image Generation Templates - APIs de IA

Scripts prontos para geração e edição de imagens com múltiplas APIs de IA.

**Status:** ✅ **Todos funcionais e testados**

---

## 📋 Templates Disponíveis

### 1. generate_gpt4o.py - Gerar Imagem com GPT-4o

Gera imagens usando GPT-4o Image Generation via Kie.ai API.

#### Uso:
```bash
# Gerar imagem simples
python3 scripts/image-generation/generate_gpt4o.py "astronauta gato no espaço"

# Gerar múltiplas variações
python3 scripts/image-generation/generate_gpt4o.py "logo minimalista empresa tech" --variants 2

# Gerar com refinamento de prompt
python3 scripts/image-generation/generate_gpt4o.py "paisagem montanhosa realista" --enhance

# Múltiplas variações + refinamento
python3 scripts/image-generation/generate_gpt4o.py "retrato profissional" --variants 4 --enhance
```

#### Parâmetros:
- `prompt` (obrigatório): Descrição da imagem a ser gerada
- `--variants`, `-v` (opcional): Número de variações [1|2|4] (padrão: 1)
- `--enhance`, `-e` (opcional): Ativa refinamento automático do prompt

#### Características:
- Formato: Portrait (2:3)
- Salvamento: Automático em ~/Downloads
- Nomes: Descritivos em português
- Latência: ~20-30 segundos

---

### 2. generate_nanobanana.py - Gerar Imagem com Nano Banana

Gera imagens usando Nano Banana (Gemini 2.5 Flash Image Preview) via Kie.ai API.

#### Uso:
```bash
# Gerar imagem em PNG (padrão)
python3 scripts/image-generation/generate_nanobanana.py "gato fofo em jardim japonês"

# Gerar em JPEG
python3 scripts/image-generation/generate_nanobanana.py "logo empresa startup" --format JPEG

# Arte abstrata
python3 scripts/image-generation/generate_nanobanana.py "arte abstrata colorida minimalista"
```

#### Parâmetros:
- `prompt` (obrigatório): Descrição da imagem a ser gerada
- `--format`, `-f` (opcional): Formato da imagem [PNG|JPEG] (padrão: PNG)

#### Características:
- Modelo: Gemini 2.5 Flash
- Formato: Portrait (2:3)
- Salvamento: Automático em ~/Downloads
- Nomes: Descritivos em português
- Latência: ~15-25 segundos
- Custo: Mais econômico que GPT-4o

---

### 3. generate_dalle3.py - Gerar Imagem com DALL-E 3

Gera imagens usando DALL-E 3 via OpenAI API.

#### Uso:
```bash
# Gerar imagem quadrada
python3 scripts/image-generation/generate_dalle3.py "astronauta surfando na lua"

# Gerar em landscape
python3 scripts/image-generation/generate_dalle3.py "paisagem futurista" --size 1792x1024

# Gerar em portrait
python3 scripts/image-generation/generate_dalle3.py "retrato elegante" --size 1024x1792

# Gerar em alta qualidade
python3 scripts/image-generation/generate_dalle3.py "arte detalhada premium" --quality hd
```

#### Parâmetros:
- `prompt` (obrigatório): Descrição da imagem a ser gerada
- `--size`, `-s` (opcional): Tamanho [1024x1024|1792x1024|1024x1792] (padrão: 1024x1024)
- `--quality`, `-q` (opcional): Qualidade [standard|hd] (padrão: standard)

#### Características:
- Modelo: DALL-E 3 (OpenAI)
- Formatos: Quadrado, Landscape, Portrait
- Qualidades: Standard ou HD
- Prompt revisado automaticamente pela API
- Salvamento: Automático em ~/Downloads
- Requer: OPENAI_API_KEY configurada

---

### 4. batch_generate.py - Geração em Lote

Gera múltiplas imagens de uma vez usando diferentes APIs.

#### Uso:
```bash
# Gerar múltiplas imagens com GPT-4o (padrão)
python3 scripts/image-generation/batch_generate.py "gato" "cachorro" "pássaro"

# GPT-4o com múltiplas variações
python3 scripts/image-generation/batch_generate.py "logo A" "logo B" "logo C" --variants 2

# Nano Banana (mais econômico)
python3 scripts/image-generation/batch_generate.py --api nanobanana "arte 1" "arte 2" "arte 3"

# Nano Banana em JPEG
python3 scripts/image-generation/batch_generate.py --api nanobanana "foto 1" "foto 2" --format JPEG
```

#### Parâmetros:
- `prompts` (obrigatório): Lista de prompts separados por espaço
- `--api`, `-a` (opcional): API a usar [gpt4o|nanobanana] (padrão: gpt4o)
- `--variants`, `-v` (opcional): Variações por prompt (apenas GPT-4o) (padrão: 1)
- `--format`, `-f` (opcional): Formato [PNG|JPEG] (apenas Nano Banana) (padrão: PNG)

#### Características:
- Geração paralela eficiente
- Relatório de sucessos/falhas
- Salvamento automático em ~/Downloads
- Nomes descritivos para cada imagem

---

### 5. edit_nanobanana.py - Editar Imagem

Edita imagens existentes usando Nano Banana Edit (Gemini 2.5 Flash).

#### Uso:
```bash
# Editar imagem local
python3 scripts/image-generation/edit_nanobanana.py foto.jpg "remover fundo"

# Editar com URL
python3 scripts/image-generation/edit_nanobanana.py --url https://exemplo.com/img.jpg "adicionar chapéu"

# Editar com formato e proporção específicos
python3 scripts/image-generation/edit_nanobanana.py imagem.png "mudar cor para azul" --format JPEG --size 16:9

# Transformações criativas
python3 scripts/image-generation/edit_nanobanana.py retrato.jpg "transformar em estilo cartoon" --size 1:1
```

#### Parâmetros:
- `image` (obrigatório se não usar --url): Caminho da imagem local
- `prompt` (obrigatório): Descrição da edição a ser aplicada
- `--url`, `-u` (opcional): URL da imagem (alternativa ao arquivo local)
- `--format`, `-f` (opcional): Formato [PNG|JPEG] (padrão: PNG)
- `--size`, `-s` (opcional): Proporção [1:1|9:16|16:9|3:4|4:3|3:2|2:3|5:4|4:5|21:9|auto] (padrão: auto)

#### Características:
- Modelo: Gemini 2.5 Flash (Nano Banana Edit)
- Suporte a imagens locais ou URLs
- Upload automático para Nextcloud (imagens locais)
- Múltiplas proporções de saída
- Salvamento automático em ~/Downloads

---

## 🎯 Casos de Uso Comuns

### 1. Post para Instagram (Portrait)
```bash
# GPT-4o com refinamento
python3 scripts/image-generation/generate_gpt4o.py "mulher jovem sorrindo em café moderno, iluminação natural, estilo lifestyle" --enhance

# Nano Banana (mais rápido)
python3 scripts/image-generation/generate_nanobanana.py "paisagem urbana ao pôr do sol, cores vibrantes"
```

### 2. Logos e Branding
```bash
# Gerar múltiplas opções
python3 scripts/image-generation/generate_gpt4o.py "logo minimalista para startup de tecnologia, azul e branco" --variants 4

# Editar logo existente
python3 scripts/image-generation/edit_nanobanana.py logo.png "mudar cor para verde, manter design" --size 1:1
```

### 3. Banners para Web (Landscape)
```bash
# DALL-E 3 em landscape
python3 scripts/image-generation/generate_dalle3.py "banner de site moderno com espaço para texto" --size 1792x1024 --quality hd
```

### 4. Conteúdo em Massa para Blog
```bash
# Gerar múltiplas imagens de uma vez
python3 scripts/image-generation/batch_generate.py \
  "ilustração de marketing digital" \
  "conceito de inteligência artificial" \
  "equipe trabalhando em escritório moderno" \
  "gráfico de crescimento de vendas" \
  --api nanobanana
```

### 5. Edição de Fotos de Produtos
```bash
# Remover fundo
python3 scripts/image-generation/edit_nanobanana.py produto.jpg "remover fundo, manter apenas o produto" --format PNG

# Mudar ambiente
python3 scripts/image-generation/edit_nanobanana.py tenis.jpg "colocar tênis em ambiente de academia moderna" --size 3:4
```

---

## 📊 Comparação de APIs

| Característica | GPT-4o | Nano Banana | DALL-E 3 |
|----------------|--------|-------------|----------|
| **Latência** | ~20-30s | ~15-25s | ~20-30s |
| **Custo** | Médio | Baixo | Alto |
| **Qualidade** | Alta | Alta | Muito Alta |
| **Variações** | 1, 2 ou 4 | 1 | 1 |
| **Formato** | Portrait (2:3) | Portrait (2:3) | Quadrado, Landscape, Portrait |
| **Refinamento** | Sim (opcional) | Não | Sim (automático) |
| **Edição** | Não | Sim | Não |
| **Melhor para** | Posts rápidos | Volume/Custo | Arte premium |

---

## 🔧 Configuração

### Pré-requisitos:

1. **Python 3.9+**
   ```bash
   python3 --version
   ```

2. **Dependências instaladas**
   ```bash
   pip3 install requests
   ```

3. **APIs configuradas**

   **GPT-4o e Nano Banana (Kie.ai):**
   - API Key já configurada em `tools/generate_image.py` e `tools/generate_image_nanobanana.py`
   - Não requer configuração adicional

   **DALL-E 3 (OpenAI):**
   ```bash
   export OPENAI_API_KEY='sua-chave-aqui'
   # ou adicione ao ~/.zshrc ou ~/.bashrc
   ```

### Verificar instalação:
```bash
# Testar GPT-4o
python3 scripts/image-generation/generate_gpt4o.py "teste rápido" --variants 1

# Testar Nano Banana
python3 scripts/image-generation/generate_nanobanana.py "teste rápido"

# Testar DALL-E 3 (requer API key)
python3 scripts/image-generation/generate_dalle3.py "teste rápido"
```

---

## 📖 Integração com Claude Code

### Para o Agente Claude Code:

Quando o usuário pedir geração de imagens, **SEMPRE use estes templates** ao invés de criar scripts novos.

#### Exemplos de comandos do usuário:

**❌ NÃO fazer:**
```
Usuário: "Gere uma imagem de gato astronauta"
Agente: Cria novo script test_image.py → Executa → Descarta
```

**✅ FAZER:**
```
Usuário: "Gere uma imagem de gato astronauta"
Agente: python3 scripts/image-generation/generate_gpt4o.py "gato astronauta no espaço"
```

#### Mapeamento de comandos:

| Pedido do usuário | Template a usar |
|-------------------|-----------------|
| "Gerar imagem" / "Criar imagem" | `generate_gpt4o.py` (padrão) |
| "Gerar imagem rápida/barata" | `generate_nanobanana.py` |
| "Gerar com DALL-E" | `generate_dalle3.py` |
| "Gerar várias imagens" | `batch_generate.py` |
| "Editar imagem" / "Modificar foto" | `edit_nanobanana.py` |
| "Gerar múltiplas variações" | `generate_gpt4o.py --variants N` |
| "Gerar logo/banner" (quadrado) | `generate_dalle3.py --size 1024x1024` |
| "Banner horizontal" | `generate_dalle3.py --size 1792x1024` |

#### Escolha da API por contexto:

- **Qualidade máxima:** DALL-E 3 com `--quality hd`
- **Velocidade/Custo:** Nano Banana
- **Versátil (padrão):** GPT-4o
- **Volume:** `batch_generate.py` com Nano Banana
- **Edição:** Sempre `edit_nanobanana.py`

---

## 🐛 Troubleshooting

### Erro: "Módulo não encontrado"
```bash
# Verifique se está executando do diretório raiz do workspace
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace
python3 scripts/image-generation/generate_gpt4o.py "teste"
```

### Erro: "OPENAI_API_KEY não encontrada" (DALL-E 3)
```bash
# Configure a variável de ambiente
export OPENAI_API_KEY='sua-chave-openai'

# Para tornar permanente (macOS/Linux)
echo 'export OPENAI_API_KEY="sua-chave-openai"' >> ~/.zshrc
source ~/.zshrc
```

### Erro: "Task failed" ou "Timeout"
- **GPT-4o/Nano Banana:** Verifique conexão com internet
- **DALL-E 3:** Verifique créditos da API OpenAI
- Tente novamente após alguns segundos
- Simplifique o prompt se muito complexo

### Imagem não foi gerada
- Verifique logs no terminal para detalhes do erro
- Confirme que ~/Downloads existe e tem permissão de escrita
- Para edição: verifique se o arquivo de entrada existe

### Upload falha (edit_nanobanana com arquivo local)
```bash
# Verifique se o script de upload existe
ls -la tools/upload_to_nextcloud.py

# Use URL direta se upload falhar
python3 scripts/image-generation/edit_nanobanana.py --url "https://url-da-imagem.com/img.jpg" "edição"
```

---

## 📊 Logs e Monitoramento

Todos os scripts exibem output em tempo real com emojis:

```
🎨 = Iniciando geração
📝 = Prompt recebido
⏳ = Aguardando API
✅ = Sucesso
❌ = Erro
📥 = Baixando imagem
💾 = Imagem salva
📂 = Pasta de destino
🍌 = Nano Banana
```

---

## 💡 Dicas de Uso

### 1. Prompts eficientes:
- **Seja específico:** "mulher jovem sorrindo em café moderno" > "pessoa feliz"
- **Inclua detalhes:** "iluminação natural, cores vibrantes, alta qualidade"
- **Estilos:** "estilo fotográfico", "arte digital", "minimalista", "realista"

### 2. Escolha da API:
- **Teste rápido:** Nano Banana (mais rápido e barato)
- **Produção:** GPT-4o ou DALL-E 3 (melhor qualidade)
- **Múltiplas opções:** GPT-4o com `--variants 4`

### 3. Formatos e tamanhos:
- **Instagram Post:** Portrait (2:3) - GPT-4o ou Nano Banana
- **Instagram Story:** Portrait (9:16) - DALL-E 3 `--size 1024x1792`
- **Banner Web:** Landscape (16:9) - DALL-E 3 `--size 1792x1024`
- **Logo/Avatar:** Quadrado (1:1) - DALL-E 3 `--size 1024x1024`

### 4. Edição de imagens:
- **Fundo:** "remover fundo", "trocar fundo para [descrição]"
- **Estilo:** "transformar em estilo cartoon", "aplicar filtro vintage"
- **Objetos:** "adicionar [objeto]", "remover [objeto]"
- **Cores:** "mudar cor para [cor]", "tornar mais vibrante"

---

## 🔄 Próximas Funcionalidades

- [ ] `upscale_image.py` - Aumentar resolução de imagens
- [ ] `style_transfer.py` - Transferência de estilo artístico
- [ ] `background_remove.py` - Remoção de fundo especializada
- [ ] `batch_edit.py` - Edição em lote
- [ ] `compare_apis.py` - Comparar resultado de múltiplas APIs
- [ ] Suporte a mais proporções (21:9 ultra-wide)
- [ ] Integração com Meta Ads para upload direto

---

## 📈 Performance e Custos

| Operação | Latência | Custo Estimado |
|----------|----------|----------------|
| GPT-4o (1 imagem) | ~20-30s | ~$0.08 |
| GPT-4o (4 variações) | ~30-40s | ~$0.32 |
| Nano Banana (1 imagem) | ~15-25s | ~$0.04 |
| DALL-E 3 standard | ~20-30s | ~$0.04 |
| DALL-E 3 HD | ~30-40s | ~$0.08 |
| Edição Nano Banana | ~20-30s | ~$0.05 |
| Batch (10 imagens Nano) | ~2-3min | ~$0.40 |

*Custos aproximados, podem variar conforme plano da API*

---

## 📞 Suporte

**Docs principais:**
- Este arquivo: `scripts/image-generation/README.md`
- Índice geral: `docs/tools/INDEX.md`
- CLAUDE.md: Instruções para agente

**Ferramentas base (em `tools/`):**
- `generate_image.py` (GPT-4o)
- `generate_image_nanobanana.py` (Nano Banana)
- `generate_image_ai.py` (DALL-E 3)
- `edit_image_nanobanana.py` (Edição)
- `generate_image_batch.py` (Batch Nano Banana)
- `generate_image_batch_gpt.py` (Batch GPT-4o)

**Para adicionar novo template:**
1. Crie script em `scripts/image-generation/`
2. Use `scripts/common/template_base.py` como base
3. Importe ferramenta de `tools/` via `sys.path.insert()`
4. Atualize este README.md
5. Teste com prompts variados

---

**Última atualização:** 2025-11-01
**Versão:** 1.0
**APIs:** Kie.ai (GPT-4o, Nano Banana) + OpenAI (DALL-E 3)
