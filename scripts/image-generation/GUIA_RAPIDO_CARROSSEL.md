# 🚀 Guia Rápido - Carrossel Meta Ads (Hormozi)

**Script:** `batch_carrossel_gpt4o.py`
**Objetivo:** Gerar carrosséis completos para Meta Ads no estilo Alex Hormozi (nicho de imóveis)

---

## ⚡ Uso Rápido

### 1. Workflow Interativo (RECOMENDADO) 🌟
```bash
python3 scripts/image-generation/workflow_carrossel_interativo.py
```
**Fluxo completo:**
1. ✅ INPUT → Coleta dados do imóvel
2. ✅ PREVIEW → Mostra copy dos 3 carrosséis
3. ✅ ESCOLHA → Você seleciona qual usar
4. ✅ GERAÇÃO → Cria imagens em paralelo

**Por quê usar:** Interface guiada, visualiza previews antes de gerar

---

### 2. Teste Rápido (3 slides)
```bash
python3 scripts/image-generation/batch_carrossel_gpt4o.py --limit 3
```
**Tempo:** ~2 minutos | **Output:** 12 imagens (3 slides × 4 variantes padrão)

**Com mais variantes:**
```bash
python3 scripts/image-generation/batch_carrossel_gpt4o.py --limit 3 --variants 8
```
**Tempo:** ~3-4 minutos | **Output:** 24 imagens (3 slides × 8 variantes)

---

### 3. Carrossel Completo (Linha de Comando)

**Carrossel 1 - Matemática Brutal (10 slides):**
```bash
python3 scripts/image-generation/batch_carrossel_gpt4o.py \
  --tipo "Chácara 1.000m²" \
  --preco "70000" \
  --entrada "10000" \
  --parcela "1000" \
  --parcelas "60" \
  --localizacao "Itatiaiuçu, 15min do centro" \
  --carrossel 1 \
  --image-url "https://media.loop9.com.br/s/XXXXXXX/download/foto.jpg"
```
**Tempo:** ~5-7 minutos | **Output:** 40 imagens (10 slides × 4 variantes padrão)

**Com 8 variantes por slide:**
```bash
# Adicione --variants 8 ao comando acima
--variants 8
```
**Tempo:** ~10-14 minutos | **Output:** 80 imagens (10 slides × 8 variantes)

**Carrossel 2 - Objeção Nome Sujo (8 slides):**
```bash
python3 scripts/image-generation/batch_carrossel_gpt4o.py \
  --tipo "Apartamento 3 quartos" \
  --preco "450000" \
  --entrada "50000" \
  --parcela "2500" \
  --parcelas "120" \
  --localizacao "Savassi, BH" \
  --carrossel 2 \
  --image-url "https://media.loop9.com.br/s/XXXXXXX/download/apto.jpg"
```
**Tempo:** ~4-6 minutos | **Output:** 32 imagens (8 slides × 4 variantes padrão)

**Com 10 variantes por slide (máximo):**
```bash
# Adicione --variants 10 ao comando acima
--variants 10
```
**Tempo:** ~10-13 minutos | **Output:** 80 imagens (8 slides × 10 variantes)

---

## 📊 Tipos de Carrossel

| Tipo | Nome | Slides | Melhor Para |
|------|------|--------|-------------|
| **1** | Matemática Brutal | 10 | Público geral, primeira campanha |
| **2** | Objeção Nome Sujo | 8 | Pessoas com restrição de crédito |
| **3** | Custo de Não Agir | 7 | Indecisos, procrastinadores (em breve) |

---

## 🎨 Visual Gerado

**Estilo:** Colagem artesanal feita à mão
- Papéis coloridos (branco, amarelo, azul-claro)
- Canetinhas de cores (vermelho, verde, preto, azul)
- Sombras reais, bordas rasgadas, fita adesiva
- Traços tortos e variação de espessura

**Formato:** Portrait 2:3 (ideal para Meta Ads)

---

## 📂 Output

**Localização:** `~/Downloads`

**Nomenclatura:**
```
carrossel_slide_01_v1.png  (Slide 1, Variante 1)
carrossel_slide_01_v2.png  (Slide 1, Variante 2)
carrossel_slide_01_v3.png  (Slide 1, Variante 3)
carrossel_slide_01_v4.png  (Slide 1, Variante 4)
...
carrossel_slide_01_vN.png  (Slide 1, Variante N - até v10 no máximo)
carrossel_slide_02_v1.png  (Slide 2, Variante 1)
...
carrossel_slide_10_vN.png  (Slide 10, última variante)
```

**Exemplo com --variants 8:**
- 10 slides × 8 variantes = 80 imagens
- Arquivos: `carrossel_slide_01_v1.png` até `carrossel_slide_10_v8.png`

---

## 🔧 Parâmetros

| Parâmetro | Obrigatório | Exemplo | Descrição |
|-----------|-------------|---------|-----------|
| `--tipo` | ✅ | "Chácara 1.000m²" | Tipo do imóvel |
| `--preco` | ✅ | "70000" | Preço total |
| `--entrada` | ✅ | "10000" | Valor da entrada |
| `--parcela` | ✅ | "1000" | Valor da parcela mensal |
| `--parcelas` | ✅ | "60" | Número de parcelas |
| `--localizacao` | ✅ | "Itatiaiuçu, 15min do centro" | Localização |
| `--carrossel` | ❌ | 1 | Tipo (1, 2 ou 3). Padrão: 1 |
| `--image-url` | ❌ | "https://..." | Imagem do imóvel (só slide 1) |
| `--variants` | ❌ | 8 | Variantes por slide (4-10). Padrão: 4 |
| `--limit` | ❌ | 3 | Limitar slides (para teste) |

---

## 💡 Dicas

### ✅ Sempre use imagem do imóvel
```bash
--image-url "https://media.loop9.com.br/s/XXXXXXX/download/foto.jpg"
```
- O slide 1 fica muito melhor com a foto real do imóvel
- Slides 2-10 usam apenas o visual de colagem

### ✅ Teste antes de rodar completo
```bash
--limit 3
```
- Valida visual em ~2 minutos
- Ajuste prompt se necessário antes de gerar todos

### ✅ Escolha o número ideal de variantes
```bash
--variants 4   # Rápido, econômico (padrão)
--variants 6   # Equilíbrio custo/opções
--variants 8   # Mais diversidade visual
--variants 10  # Máxima variedade (mais caro/lento)
```
- **4 variantes:** Ideal para a maioria dos casos
- **6-8 variantes:** Quando quer mais opções para escolher
- **10 variantes:** Quando precisa testar muitas variações ou A/B test intensivo

### ✅ Escolha melhor variante
- Cada slide gera múltiplas versões (4-10 conforme escolhido)
- Escolha a melhor variante de cada slide
- Use no Meta Ads

---

## 📈 Estrutura do Carrossel 1 (Matemática Brutal)

1. **Hook** - "Você VAI pagar R$ X/mês de qualquer jeito"
2. **Credibilidade** - "23 famílias de aluguel para dona de terra"
3. **Opção 1: Aluguel** - Perdas e desperdício
4. **Opção 2: Imóvel** - Ganhos e patrimônio
5. **Comparação** - Lado a lado (vermelho vs verde)
6. **Objeção** - "Nome sujo" → Sem banco resolve
7. **Sem Juros** - Economia de R$ 70k
8. **Value Stack** - Tudo que está incluso
9. **Recap** - Recapitulação + Custo de não agir
10. **CTA** - Urgência + WhatsApp

---

## 📈 Estrutura do Carrossel 2 (Objeção Nome Sujo)

1. **Hook** - "Não consigo comprar, nome sujo"
2. **Reframe** - "NO BANCO. Aqui não tem banco"
3. **Casos Reais** - João, Maria, Carlos (todos compraram)
4. **Comum** - O que eles tinham (R$ 10k + vontade)
5. **Matemática** - Aluguel vs Imóvel
6. **Sem Barreiras** - Lista completa de X's (sem SPC, Serasa...)
7. **Dignidade** - Empatia sem pena
8. **CTA** - Qualificação dura + urgência

---

## 🎯 Próximos Passos

Após gerar o carrossel:

1. ✅ Revisar todas as variantes de cada slide (4-10 dependendo do --variants escolhido)
2. ✅ Escolher a melhor variante por slide
3. ✅ Fazer upload para Meta Ads
4. ✅ Criar campanha no Facebook Ads Manager
5. ✅ Testar diferentes combinações (A/B test)

💡 **Dica:** Com mais variantes, você pode criar múltiplos carrosséis diferentes para A/B testing

---

## 🔗 Documentação Completa

- **README:** `scripts/image-generation/README.md`
- **Template Visual:** `biblioteca de prompts/Templates Visuais/carrossel-colagem-artesanal.md`
- **Exemplos Hormozi:** `biblioteca de prompts/Exemplos - Hormozi META ADS [Imoveis]/carrossel/`

---

**Versão:** 1.0
**Data:** 2025-11-03
**Nicho:** Imóveis (adaptável para outros nichos)
