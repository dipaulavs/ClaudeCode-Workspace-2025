# Templates Visuais - Biblioteca Completa

Referência detalhada dos templates visuais validados para criação de carrosséis.

## Templates Disponíveis

### 1. Template Colagem Artesanal

**Localização:** `biblioteca de prompts/Templates Carrosseis/carrossel-colagem-artesanal.md`

**Características:**
- Estilo: Trabalho escolar feito à mão
- Aparência: Papéis colados, canetinhas coloridas, mesa de madeira
- Melhor uso: Storytelling emocional, autenticidade, nicho imóveis

**Estrutura Visual:**
- Fundo: Mesa de madeira clara com luz natural
- Papéis: Branco, amarelo claro, azul claro, papel pardo
- Canetas: Vermelho (erros/objeções), verde (soluções), preto (principal), azul (complementar)
- Elementos: Sombras reais, bordas rasgadas, fita adesiva, imperfeições artesanais

**Dimensões:**
- Tamanho: 1080x1350px (4:5 Instagram)
- Proporção GPT-4o: 2:3 (portrait)

**Variáveis Substituíveis:**
- `{CONTEUDO_ESPECIFICO}`: Texto principal do slide
- `{ICONES}`: Ícones desenhados à mão

**Exemplo de Prompt:**
```
Crie uma colagem artesanal e realista feita à mão, com aparência de trabalho escolar sobre vendas de terrenos.

Fundo de mesa de madeira clara, luz natural suave e papéis colados com sombras reais e bordas rasgadas.

Use papéis de cores diferentes (branco, amarelo e azul-claro) com escrita feita à mão em canetinhas de várias cores (vermelho, verde, preto e azul).

No topo, escreva à mão em letras grandes e coloridas: "ONTEM fechei 3 LOTES em 47 MINUTOS"

Adicione ícones desenhados à mão: um relógio, uma casinha simples, e uma nota de dinheiro com um check verde

Finalize com detalhes de imperfeição realista — sombras, fita adesiva segurando o papel, traços tortos e variação de espessura da caneta, mantendo o ar de colagem artesanal autêntica.
```

---

### 2. Template Educacional ABSM

**Localização:** `biblioteca de prompts/Templates Carrosseis/carrossel estilo ABSM/template_carrossel_educacional_6slides.txt`

**Características:**
- Estilo: Minimalista elegante tipo revista editorial
- Aparência: Badge sticker ondulado, mockups Instagram, fotografia lifestyle
- Melhor uso: Conteúdo educacional, estabelecer autoridade

**Estrutura Visual:**
- Slide 1: Foto top-down lifestyle + badge sticker ondulado branco com sombra
- Slides 2-5: Fundos variados (bege claro, marrom médio/escuro) + mockups ou fotos
- Slide 6: CTA minimalista com hierarquia tipográfica em cor marca

**Badge Sticker (Slide 1):**
- Formato: Shape irregular com bordas onduladas (não retangular)
- Cor: Branco puro (#FFFFFF)
- Sombra: Offset Y 8-12px, Blur 20-30px, Opacidade 15-20%
- Tipografia: Serifada (linha 1 cor marca) + Sans-serif (linhas 2-3 preto)

**Paleta de Cores:**
- Slide 1: Fundo escuro natural (foto)
- Slide 2: #EAE3D8 (bege claro)
- Slide 3: #8B7355 (marrom médio)
- Slide 4: #6B5444 (marrom escuro)
- Slide 5: #F5F1EB (bege muito claro)
- Slide 6: #E8E3D8 (bege claro)
- Cor destaque: #8B5A3C (terracota)

**Variáveis Substituíveis:**
- `[IMAGENS E SÍMBOLOS]`: 3-4 objetos icônicos do nicho
- `[TEXTO EDITÁVEL]`: Títulos e descrições personalizadas
- `@lfimoveis`: Trocar por nome da marca

**Exemplo de Prompt Slide 1:**
```
Fotografia top-down (visão de cima) de uma mesa com iluminação natural difusa e suave. Chaves, plantas arquitetônicas, maquete de apartamento, café.

Composição simétrica, fundo de mesa de madeira escura, profundidade de campo rasa (f/2.8), tons quentes (4500K-5500K).

Sobreposição centralizada:

CABEÇALHO (topo): "@lfimoveis | 99" - Fonte serifada fina, marrom escuro (#4A3428), 28-32px, letras espaçadas, 120px do topo

BADGE CENTRAL (sticker ondulado):
- Shape irregular com bordas onduladas (estilo adesivo colado)
- Branco (#FFFFFF), sombra suave (Y=10px, blur=25px, opacity=18%)
- Padding interno 40-50px horizontal x 30-40px vertical

TEXTO DENTRO DO BADGE (3 linhas centralizadas):
Linha 1: "Estratégias" - Serifada terracota (#8B5A3C), 56-64px, SemiBold
Linha 2: "que vendem" - Sans-serif preta, 52-60px, Regular
Linha 3: "imóveis mais rápido" - Sans-serif preta, 52-60px, Regular
```

---

### 3. Template Texto Tipo Adesivo

**Localização:** `biblioteca de prompts/Templates Carrosseis/carrossel texto tipo adesivo/prompt template carrossel.txt`

**Características:**
- Estilo: Tipografia display vintage com efeito sticker em 3 camadas
- Aparência: Layout Bento Box, paletas de cores profissionais
- Melhor uso: Listas, tutoriais visuais, paletas de cores, dicas rápidas

**Estrutura Visual:**
- Slide 1 (Capa): Foto do nicho + título com efeito sticker triple-layer
- Slides 2-6: Layout Bento Box com cartões de cor arredondados
- Slide 7 (CTA): Foto com overlay + CTA elegante

**Efeito Sticker Triple-Layer:**
1. Fill/Preenchimento: Creme claro (#F5EFE0)
2. Stroke interno: Preto (#1A1A1A) 2-3px
3. Stroke externo: Branco (#FFFFFF) 8-12px (efeito adesivo recortado)

**Tipografia:**
- Fonte: Display serif vintage estilo Cooper Black/Souvenir Bold
- Peso: Extra Bold com alto contraste
- Largura: Extended/Wide
- Kerning: Tight/apertado
- Serifas: Bracketed arredondadas estilo anos 70

**Variáveis Substituíveis:**
- `[IMAGENS E SÍMBOLOS]`: Foto do ambiente/produto do nicho
- `[TEXTO EDITÁVEL]`: Títulos, nomes de cores, CTAs

**Exemplo de Prompt Capa:**
```
Design editorial moderno de carrossel Instagram. Fundo: foto real de estabelecimento (cafeteria moderna, luz natural).

Layout: título centralizado vertical ocupando 60% da altura com EFEITO STICKER/ADESIVO em 3 camadas:

TIPOGRAFIA STICKER:
- Fonte: Display serif vintage Cooper Black/Souvenir Bold com swash ornamentais
- Extra Bold, caracteres largos (Extended)
- Kerning tight, serifas bracketed arredondadas anos 70
- "R" inicial com floreio/swash dramático

CAMADAS DO EFEITO (dentro para fora):
1. FILL: Creme claro (#F5EFE0)
2. STROKE INTERNO: Preto (#1A1A1A) 2-3px
3. STROKE EXTERNO: Branco (#FFFFFF) 8-12px

TEXTO: "ROUBE MINHAS PALETAS DE CORES"

Abaixo: "hello" em script cursivo manuscrito fino (#2D2D2D), tamanho pequeno, sem efeito sticker.

Rodapé: "@lfimoveis" em serifada branca simples, centralizado.

Composição balanceada, hierarquia visual forte, estética clean editorial.
```

---

### 4. Template Antes e Depois

**Localização:** `biblioteca de prompts/Templates Carrosseis/carrossel_estrelato estilo antes e depois/template_carrossel_minimalista_beige_8slides.txt`

**Características:**
- Estilo: Comparações lado a lado minimalistas
- Aparência: Split screen, cores neutras beige, tipografia limpa
- Melhor uso: Transformações, provas de resultados, comparações visuais

**Estrutura Visual:**
- Layout: Divisão vertical 50/50 ou assimétrico
- Cores: Tons beige neutros (#EAE3D8, #F5F1EB, #D4C4B7)
- Tipografia: Serifada elegante para títulos + Sans-serif clean para corpo
- Elementos: Linhas divisórias, badges/labels, setas direcionais

**Variáveis Substituíveis:**
- `[ANTES]`: Foto/descrição do estado inicial
- `[DEPOIS]`: Foto/descrição do estado final
- `[MÉTRICA]`: Números de transformação

**Exemplo de Prompt Comparação:**
```
Design de carrossel minimalista comparativo, fundo bege claro (#EAE3D8).

Layout split screen vertical dividido ao meio por linha preta fina.

LADO ESQUERDO (ANTES):
- Fundo levemente mais escuro (#D4C4B7)
- Badge superior: "ANTES" em serifada preta, fundo branco arredondado
- Foto/descrição: [Estado inicial problemático]
- Métricas negativas em vermelho (#D32F2F)

LADO DIREITO (DEPOIS):
- Fundo levemente mais claro (#F5F1EB)
- Badge superior: "DEPOIS" em serifada preta, fundo branco arredondado
- Foto/descrição: [Estado final transformado]
- Métricas positivas em verde (#388E3C)

Centro: Seta grande apontando da esquerda para direita, cor marca.

Rodapé centralizado: "@lfimoveis" em serifada pequena.

Composição equilibrada, contraste claro entre antes/depois, hierarquia visual marcante.
```

---

## Seleção Automática de Template

**Critérios:**

```
Conteúdo educacional/informativo
    └─> Template ABSM ou Texto Adesivo

Conteúdo de venda/oferta
    └─> Template Colagem Artesanal

Comparação/prova/transformação
    └─> Template Antes e Depois

Lista/paleta/tutorial visual
    └─> Template Texto Adesivo
```

## Adaptação por Nicho

### Imóveis
- Templates recomendados: ABSM, Colagem Artesanal
- Objetos Slide 1: Chaves, plantas, maquete, café
- Cores: Tons terrosos, beige, marrom, terracota
- Emojis: 🏡 🔑 🏢 📍

### Gastronomia
- Templates recomendados: Texto Adesivo, ABSM
- Objetos Slide 1: Pratos gourmet, talheres elegantes, ingredientes frescos
- Cores: Quentes, apetitosas, âmbar, dourado
- Emojis: 🍕 🍔 ☕ 🍰

### Fitness
- Templates recomendados: Antes e Depois, ABSM
- Objetos Slide 1: Tênis, garrafa d'água, halteres, smartwatch
- Cores: Energéticas, vibrantes, azul, verde, laranja
- Emojis: 💪 🏋️ 🥗 ⏱️

### Moda
- Templates recomendados: Texto Adesivo, ABSM
- Objetos Slide 1: Roupas, acessórios, tecidos, café
- Cores: Elegantes, pastel, preto/branco, rosa
- Emojis: 👗 👠 💄 ✨

### Educação
- Templates recomendados: ABSM, Texto Adesivo
- Objetos Slide 1: Livros, notebook, café, óculos
- Cores: Profissionais, azul, verde, bege
- Emojis: 📚 🎓 💡 🚀

## Especificações Técnicas Universais

**Dimensões:**
- 1080x1350px (4:5 Instagram/Facebook)
- Proporção GPT-4o: 2:3 (portrait)
- Resolução: 72-300 DPI
- Formato: JPG (qualidade 90%) ou PNG

**Tipografia:**
- Cabeçalho: 24-32px
- Título principal: 56-64px (serifada) / 52-60px (sans-serif)
- Corpo/descrição: 36-48px
- Legendas: 28-36px
- Kerning/tracking: +80 (letras espaçadas)

**Espaçamento:**
- Mínimo entre elementos: 40px
- Margens: 80px laterais, 100px superior/inferior
- Padding interno badges: 40-50px horizontal x 30-40px vertical

**Sombras (para badges/stickers):**
- Offset Y: 8-12px
- Blur: 20-30px
- Opacidade: 15-20%
- Cor: Preto (#000000)

## Referências Adicionais

**Localização dos templates originais:**
```
/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/biblioteca de prompts/Templates Carrosseis/
├── carrossel-colagem-artesanal.md
├── carrossel estilo ABSM/
│   └── template_carrossel_educacional_6slides.txt
├── carrossel texto tipo adesivo/
│   ├── prompt template carrossel.txt
│   └── post_01_caption.txt
└── carrossel_estrelato estilo antes e depois/
    └── template_carrossel_minimalista_beige_8slides.txt
```

**Para consultar detalhes completos:**
Use a ferramenta Read para ler o arquivo do template específico.
