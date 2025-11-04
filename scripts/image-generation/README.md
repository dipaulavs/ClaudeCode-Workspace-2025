# 🎨 Image Generation Templates - APIs de IA

Scripts prontos para geração e edição de imagens com múltiplas APIs de IA.

**Status:** ✅ **Todos funcionais e testados**

**URLs Públicas:** ✅ Todas as imagens geradas retornam URLs públicas que podem ser usadas diretamente (ex: WhatsApp)

---

## 📋 Templates Disponíveis (4 templates)

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

### 3. batch_generate.py - Geração em Lote

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

### 4. edit_nanobanana.py - Editar Imagem

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

### 5. batch_carrossel_gpt4o.py - Carrosséis Meta Ads (Hormozi)

Gera carrosséis completos para Meta Ads no estilo Alex Hormozi para nicho de imóveis.
**Visual:** Colagem artesanal feita à mão | **Geração:** 100% paralela | **Output:** 4 variantes por slide

#### Uso:

```bash
# Modo interativo (recomendado)
python3 scripts/image-generation/batch_carrossel_gpt4o.py

# Modo teste (3 slides para validar visual)
python3 scripts/image-generation/batch_carrossel_gpt4o.py --limit 3

# Carrossel 1 completo (10 slides - Matemática Brutal)
python3 scripts/image-generation/batch_carrossel_gpt4o.py \
  --tipo "Chácara 1.000m²" \
  --preco "70000" \
  --entrada "10000" \
  --parcela "1000" \
  --parcelas "60" \
  --localizacao "Itatiaiuçu, 15min do centro" \
  --carrossel 1 \
  --image-url "https://exemplo.com/foto-imovel.jpg"

# Carrossel 2 completo (8 slides - Objeção Nome Sujo)
python3 scripts/image-generation/batch_carrossel_gpt4o.py \
  --tipo "Apartamento 3 quartos" \
  --preco "450000" \
  --entrada "50000" \
  --parcela "2500" \
  --parcelas "120" \
  --localizacao "Savassi, BH" \
  --carrossel 2 \
  --image-url "https://exemplo.com/apto.jpg"
```

#### Parâmetros:
- `--tipo` (obrigatório): Tipo do imóvel (ex: "Chácara 1.000m²", "Apartamento 3 quartos")
- `--preco` (obrigatório): Preço total do imóvel (ex: 70000)
- `--entrada` (obrigatório): Valor da entrada (ex: 10000)
- `--parcela` (obrigatório): Valor da parcela mensal (ex: 1000)
- `--parcelas` (obrigatório): Número de parcelas (ex: 60)
- `--localizacao` (obrigatório): Localização do imóvel (ex: "Itatiaiuçu, 15min do centro")
- `--carrossel` (opcional): Tipo de carrossel [1|2|3] (padrão: 1)
  - **1** = Matemática Brutal (10 slides)
  - **2** = Objeção Nome Sujo (8 slides)
  - **3** = Custo de Não Agir (7 slides - em breve)
- `--image-url` (opcional): URL da imagem do imóvel (usado apenas no slide 1)
- `--limit` (opcional): Limitar número de slides para teste (ex: --limit 3)

#### Características:
- **Metodologia:** Alex Hormozi (100M Offers + 100M Leads)
- **Visual:** Colagem artesanal feita à mão (papéis coloridos, canetinhas, sombras reais)
- **Geração:** 100% paralela (ThreadPoolExecutor)
- **Variantes:** 4 por slide (escolher melhor depois)
- **Formato:** Portrait 2:3 (ideal para Meta Ads)
- **Slide 1:** Usa imagem de referência do imóvel (`filesUrl`)
- **Slides 2-10:** Apenas prompt (visual de colagem)
- **Salvamento:** `~/Downloads/carrossel_slide_01_v1.png`, `carrossel_slide_01_v2.png`, etc.
- **Tempo:** ~5-7 minutos para carrossel completo (10 slides × 4 variantes = 40 imagens)

#### Templates de Slide de Capa:

**📍 Localização:** `scripts/image-generation/templates/slide_capa_templates.json`

**Template 1: Divisão Vertical - Foto + Texto**
- **Layout:** Dividido em duas metades verticais (50% cada)
- **Lado Esquerdo:** Foto limpa do imóvel (sem texto ou overlay)
- **Lado Direito:** Colagem artesanal com hook e textos
- **Parte Inferior:** Setinha "Deslize para continuar ➜" (apenas Slide 1)
- **Quando usar:** Ideal para mostrar produto + hook simultaneamente. Bom para first impression.

**Template 2: Colagem Vertical - Textos em Cima + Foto Embaixo**
- **Layout:** Vertical de cima para baixo (60% textos + 40% foto)
- **Parte Superior:** Colagem artesanal completa com hook/objeção
- **Parte Inferior:** Foto do imóvel (limpa ou só com preço destacado)
- **Rodapé:** Setinha "Deslize para continuar ➜" (apenas Slide 1)
- **Quando usar:** Ideal para hooks emocionais/objeções. Textos ganham mais destaque, foto prova credibilidade.

**Como reutilizar:**
1. Ver templates disponíveis: `cat scripts/image-generation/templates/slide_capa_templates.json`
2. Copiar `prompt_base` do template desejado
3. Substituir `{CONTEUDO_TEXTO}` pelo hook/copy específica
4. (Template 2) Substituir `{PRECO_DESTAQUE}` por valor opcional sobre a foto
5. Usar com `--image-url` para incluir foto do imóvel

#### Estrutura dos Carrosséis:

**Carrossel 1 - Matemática Brutal (10 slides):**
1. Hook - "Você VAI pagar R$ X/mês de qualquer jeito"
2. Credibilidade - "23 famílias de aluguel para dona de terra"
3. Opção 1: Aluguel (perdas)
4. Opção 2: Imóvel (ganhos)
5. Comparação lado a lado
6. Objeção: "Nome sujo"
7. Sem juros (economia R$ 70k)
8. Value stack (tudo incluso)
9. Recap + Custo de não agir
10. CTA urgente

**Carrossel 2 - Objeção Nome Sujo (8 slides):**
1. Hook - "Não consigo comprar, nome sujo"
2. Reframe - "NO BANCO. Aqui não tem banco"
3. Casos reais (João, Maria, Carlos)
4. O que eles tinham em comum
5. Matemática (aluguel vs imóvel)
6. Sem banco = Sem barreiras
7. Dignidade (empatia)
8. CTA qualificado

#### Exemplo de Output:
```
✅ Slides gerados com sucesso: 10/10
🖼️  Total de imagens geradas: 40 (10 slides × 4 variantes)
⏱️  Tempo total: 324.5s (32.5s por slide)
📂 ~/Downloads/carrossel_slide_01_v1.png ... carrossel_slide_10_v4.png
```

#### Quando Usar:
- Criar anúncios de imóveis para Meta Ads (Facebook/Instagram)
- Precisa de copy persuasivo estilo Hormozi
- Quer testar múltiplas variações visuais (4 por slide)
- Visual diferenciado (colagem artesanal) vs templates genéricos

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

### 3. Conteúdo em Massa para Blog
```bash
# Gerar múltiplas imagens de uma vez
python3 scripts/image-generation/batch_generate.py \
  "ilustração de marketing digital" \
  "conceito de inteligência artificial" \
  "equipe trabalhando em escritório moderno" \
  "gráfico de crescimento de vendas" \
  --api nanobanana
```

### 4. Edição de Fotos de Produtos
```bash
# Remover fundo
python3 scripts/image-generation/edit_nanobanana.py produto.jpg "remover fundo, manter apenas o produto" --format PNG

# Mudar ambiente
python3 scripts/image-generation/edit_nanobanana.py tenis.jpg "colocar tênis em ambiente de academia moderna" --size 3:4
```

---

## 📊 Comparação de APIs

| Característica | GPT-4o | Nano Banana |
|----------------|--------|-------------|
| **Latência** | ~20-30s | ~15-25s |
| **Custo** | Médio | Baixo |
| **Qualidade** | Alta | Alta |
| **Variações** | 1, 2 ou 4 | 1 |
| **Formato** | Portrait (2:3) | Portrait (2:3) |
| **Refinamento** | Sim (opcional) | Não |
| **Edição** | Não | Sim |
| **URL Pública** | ✅ Sim | ✅ Sim |
| **Melhor para** | Posts versáteis | Volume/Custo |

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

### Verificar instalação:
```bash
# Testar GPT-4o
python3 scripts/image-generation/generate_gpt4o.py "teste rápido" --variants 1

# Testar Nano Banana
python3 scripts/image-generation/generate_nanobanana.py "teste rápido"
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
| "Gerar várias imagens" | `batch_generate.py` |
| "Editar imagem" / "Modificar foto" | `edit_nanobanana.py` |
| "Gerar múltiplas variações" | `generate_gpt4o.py --variants N` |

#### Escolha da API por contexto:

- **Versátil (padrão):** GPT-4o
- **Velocidade/Custo:** Nano Banana
- **Volume:** `batch_generate.py` com Nano Banana
- **Edição:** Sempre `edit_nanobanana.py`
- **URL Pública:** Todas as APIs retornam URLs diretas

---

## 🐛 Troubleshooting

### Erro: "Módulo não encontrado"
```bash
# Verifique se está executando do diretório raiz do workspace
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace
python3 scripts/image-generation/generate_gpt4o.py "teste"
```

### Erro: "Task failed" ou "Timeout"
- **GPT-4o/Nano Banana:** Verifique conexão com internet
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
- **Produção:** GPT-4o (melhor qualidade e variações)
- **Múltiplas opções:** GPT-4o com `--variants 4`
- **URL Pública:** Ambas retornam URLs diretas para uso em WhatsApp/outros

### 3. Formatos e tamanhos:
- **Instagram Post:** Portrait (2:3) - GPT-4o ou Nano Banana
- **Stories/Reels:** Portrait (2:3) - GPT-4o ou Nano Banana

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
| Edição Nano Banana | ~20-30s | ~$0.05 |
| Batch (10 imagens Nano) | ~2-3min | ~$0.40 |

*Custos aproximados, podem variar conforme plano da API*

**Vantagem URLs Públicas:** Imagens podem ser usadas diretamente sem upload adicional para Nextcloud/outros serviços

---

## 📞 Suporte

**Docs principais:**
- Este arquivo: `scripts/image-generation/README.md`
- Índice geral: `docs/tools/INDEX.md`
- CLAUDE.md: Instruções para agente

**Ferramentas base (em `tools/`):**
- `generate_image.py` (GPT-4o)
- `generate_image_nanobanana.py` (Nano Banana)
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

**Última atualização:** 2025-11-02
**Versão:** 1.1
**APIs:** Kie.ai (GPT-4o, Nano Banana)
**Templates:** 4 (GPT-4o, Nano Banana, Batch, Edit)
