# 🎨 Template Visual: Carrossel Colagem Artesanal

## 📋 Descrição

Template de prompt visual para gerar slides de carrossel no estilo **colagem artesanal feita à mão** - aparência de trabalho escolar sobre vendas de terrenos/imóveis.

---

## 🎯 Prompt Base

```
Crie uma colagem artesanal e realista feita à mão, com aparência de trabalho escolar sobre vendas de terrenos.

Fundo de mesa de madeira clara, luz natural suave e papéis colados com sombras reais e bordas rasgadas.

Use papéis de cores diferentes (branco, amarelo e azul-claro) com escrita feita à mão em canetinhas de várias cores (vermelho, verde, preto e azul).

{CONTEUDO_ESPECIFICO}

Adicione ícones desenhados à mão: {ICONES}

Finalize com detalhes de imperfeição realista — sombras, fita adesiva segurando o papel, traços tortos e variação de espessura da caneta, mantendo o ar de colagem artesanal autêntica.
```

---

## 🔧 Variáveis Disponíveis

### `{CONTEUDO_ESPECIFICO}`
Conteúdo principal do slide (textos, números, comparações)

**Exemplo:**
```
No topo, escreva à mão em letras grandes e coloridas: "ONTEM fechei 3 LOTES em 47 MINUTOS"

Abaixo, desenhe três pequenos recortes com ❌ e ✅ feitos com canetinha:
❌ Nome sujo
❌ Sem entrada grande
✅ Queriam terra própria

Logo depois, em destaque sobre um pedaço de papel pardo colado:
"R$ 10 mil resolve. Não precisa de banco."
```

### `{ICONES}`
Ícones/desenhos à mão que devem aparecer

**Exemplo:**
```
um relógio, uma casinha simples, e uma nota de dinheiro com um check verde
```

---

## 📐 Especificações Visuais

### Dimensões
- **Tamanho:** 1080x1350px (4:5 - formato Instagram/Facebook carrossel)
- **Proporção GPT-4o:** 2:3 (portrait)

### Cores de Papel
- Branco (principal)
- Amarelo claro (destaques)
- Azul claro (informações secundárias)
- Papel pardo/kraft (CTAs e valores importantes)

### Canetas
- **Vermelho:** Erros, perdas, objeções (❌)
- **Verde:** Soluções, checks, ganhos (✅)
- **Preto:** Texto principal
- **Azul:** Informações complementares

### Fontes (Manuscrito)
- Letras grandes: 80-120pt equivalente
- Corpo de texto: 28-40pt equivalente
- Números importantes: 100pt+ (sempre em destaque)

### Elementos Visuais
- Sombras reais dos papéis
- Bordas rasgadas (não cortadas retas)
- Fita adesiva transparente segurando os papéis
- Traços tortos e imperfeitos
- Variação de espessura da caneta
- Fundo: mesa de madeira clara com luz natural

---

## 📝 Exemplos de Uso

### Slide 1 (Capa com Imagem)
```
{CONTEUDO_ESPECIFICO} =
No topo, escreva à mão em letras grandes e coloridas: "ONTEM fechei 3 LOTES em 47 MINUTOS"

Abaixo, desenhe três pequenos recortes com ❌ e ✅ feitos com canetinha:
❌ Nome sujo
❌ Sem entrada grande
✅ Queriam terra própria

Logo depois, em destaque sobre um pedaço de papel pardo colado:
"R$ 10 mil resolve. Não precisa de banco."

{ICONES} = um relógio, uma casinha simples, e uma nota de dinheiro com um check verde
```

### Slide 2 (Comparação)
```
{CONTEUDO_ESPECIFICO} =
No topo: "MESMA DOR MENSAL | RESULTADOS OPOSTOS"

Divida o papel ao meio com uma linha vertical desenhada:

LADO ESQUERDO (fundo vermelho claro):
ALUGUEL
R$ 1.000/mês
5 anos = R$ 60.000
❌ Zero patrimônio

LADO DIREITO (fundo verde claro):
CHÁCARA
R$ 1.000/mês
5 anos = R$ 70.000
✅ Terra valendo R$ 150k

{ICONES} = seta pra baixo em vermelho (lado esquerdo), seta pra cima em verde (lado direito)
```

### Slide 3 (Objeção)
```
{CONTEUDO_ESPECIFICO} =
No topo, em letras grandes vermelhas entre aspas:
"MEU NOME TÁ SUJO"

Abaixo, em preto:
Você não consegue comprar NO BANCO.

Aqui não tem banco.

Liste com X's vermelhos:
❌ Sem consulta SPC
❌ Sem consulta Serasa
❌ Sem aprovação de crédito

E checks verdes:
✅ Você tem R$ 10k?
✅ Você paga R$ 1k/mês?

Em destaque: "Pronto. É sua."

{ICONES} = banco riscado com X vermelho, casinha com check verde
```

### Slide 4 (Matemática)
```
{CONTEUDO_ESPECIFICO} =
No topo: "BANCO vs DIRETO"

Em papel branco:
🏦 COMPRANDO PELO BANCO:
Terreno: R$ 70.000
Juros (5 anos): R$ 70.000
TOTAL: R$ 140.000

Em papel verde:
🤝 COMPRANDO DIRETO:
Terreno: R$ 70.000
Juros: R$ 0
TOTAL: R$ 70.000

Em destaque em papel pardo:
"ECONOMIA: R$ 70.000"

Abaixo: "Metade do preço. Mesma terra."

{ICONES} = calculadora desenhada, nota de R$ 70k com seta pra baixo
```

### Slide 10 (CTA)
```
{CONTEUDO_ESPECIFICO} =
No topo: "ÚLTIMA COISA:"

Segunda-feira: 17 lotes
Hoje: 9 lotes

Preço sobe R$ 5k semana que vem.

Em destaque: "Não é pressão. É realidade."

Você decide:
→ Continuar pagando aluguel
→ ou ter patrimônio

Em papel amarelo grande:
👉 CHAMA NO WHATSAPP AGORA

Manda: "TENHO R$ 10K"

{ICONES} = relógio urgente, WhatsApp logo desenhado, seta apontando pro CTA
```

---

## 🚀 Uso com GPT-4o

### Com Imagem de Referência (Slide 1)
```bash
python3 scripts/image-generation/batch_carrossel_gpt4o.py \
  --image-url "https://media.loop9.com.br/s/qpj8XHWcZs4Jjo9/download/PHOTO-2025-10-10-09-11-05.jpg" \
  --slide 1
```

### Apenas Texto (Slides 2-10)
```bash
python3 scripts/image-generation/batch_carrossel_gpt4o.py \
  --slides 2-10
```

---

## 📊 Estrutura de Carrosséis Hormozi

### Carrossel 1: Matemática Brutal (10 slides)
1. Hook - "Você VAI pagar R$ 1.000/mês"
2. Credibilidade - "23 famílias de aluguel pra dona de terra"
3. Opção 1: Aluguel (perdas)
4. Opção 2: Chácara (ganhos)
5. Comparação lado a lado
6. Objeção: "Nome sujo"
7. Sem juros (economia R$ 70k)
8. Value stack (tudo incluso)
9. Recap + Custo de não agir
10. CTA urgente

### Carrossel 2: Objeção "Nome Sujo" (8 slides)
1. Hook - "Não consigo comprar, nome sujo"
2. Reframe - "NO BANCO. Aqui não tem banco"
3. Casos reais (João, Maria, Carlos)
4. O que eles tinham em comum
5. Matemática (aluguel vs chácara)
6. Sem banco = Sem barreiras
7. Dignidade (empatia)
8. CTA qualificado

### Carrossel 3: Custo de Não Agir (7 slides)
1. Hook - "Você perde R$ 3.000/mês"
2. Perda #1: Aluguel
3. Perda #2: Valorização
4. Perda #3: Inflação
5. Total perdido (R$ 192k em 5 anos)
6. A alternativa (ganhar R$ 180k)
7. CTA urgência máxima

---

## 🎨 Paleta de Cores

**Fundo:**
- Mesa de madeira clara: #D4A574
- Luz natural: Branco suave com sombras

**Papéis:**
- Branco: #FFFFFF
- Amarelo: #FFF9C4
- Azul claro: #BBDEFB
- Papel pardo: #C4A77D

**Canetas:**
- Vermelho: #D32F2F
- Verde: #388E3C
- Preto: #212121
- Azul: #1976D2

---

**Versão:** 1.0
**Data:** 2025-11-03
**Uso:** Carrosséis Meta Ads para nicho de imóveis
