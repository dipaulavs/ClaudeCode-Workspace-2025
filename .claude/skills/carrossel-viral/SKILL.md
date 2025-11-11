---
name: carrossel-viral
description: Criar carrosséis virais para redes sociais com copy Hormozi + visual artesanal. Auto-invoca quando usuário pedir carrossel, slides, posts Instagram/LinkedIn, ou conteúdo viral. Workflow completo - copy (3 versões) + prompt visual colagem + geração em batch + organização de pasta.
---

# Carrossel Viral

## Overview

Criar carrosséis extremamente virais para Meta Ads, Instagram e LinkedIn com metodologia Hormozi (hooks, objeções, matemática brutal) e visual de colagem artesanal feita à mão. Workflow completo automatizado: copy → prompts visuais → geração paralela → organização de arquivos.

**Auto-invocação:** Quando usuário pedir carrossel, slides, posts redes sociais, ou conteúdo viral.

## Workflow Completo

```
Usuário pede carrossel
↓
1. Perguntar tema (se não fornecido)
↓
2. ANÁLISE ESTRATÉGICA (avatar, dor, objeção, matemática, urgência)
↓
3. Invocar hormozi-copywriter COM análise (prompt consultor)
↓
4. Usuário escolhe versão preferida (1, 2 ou 3)
↓
5. Gerar prompts visuais (colagem artesanal + copy escolhida)
↓
6. Executar batch_carrossel_gpt4o.py (geração paralela)
↓
7. Criar pasta organizada com slides nomeados
↓
8. Entregar carrossel pronto
```

## Step 1: Coletar Tema

**Se tema NÃO fornecido:**

Perguntar ao usuário: "Qual o tema/nicho do carrossel?"

**Exemplos de temas:**
- Venda de terrenos
- Curso de inglês
- SaaS para startups
- Emagrecer sem academia
- Investimentos para iniciantes

## Step 2: Gerar Copy com Hormozi-Copywriter

**OBRIGATÓRIO:** Invocar skill `hormozi-copywriter` com análise estratégica completa do negócio.

**NUNCA usar prompt simples.** Sempre fazer análise de mercado primeiro e direcionar hormozi-copywriter como consultor estratégico.

### Análise Estratégica do Nicho

**ANTES de invocar hormozi-copywriter, analisar:**

1. **Avatar específico:**
   - Quem é exatamente? (idade, situação, contexto)
   - Qual a dor mais íntima? (pain of silence)
   - O que já tentou e falhou?

2. **Objeção principal:**
   - Qual a desculpa #1 pra não comprar?
   - Por que essa objeção existe?
   - Como Hormozi destruiria ela?

3. **Dream Outcome:**
   - Resultado específico e mensurável
   - Timeline realista
   - Prova social que valida

4. **Contradição poderosa:**
   - O que o mercado diz vs realidade
   - Esforço alto/resultado baixo → mudança pequena/resultado massivo
   - Qual crença quebrar?

5. **Matemática brutal:**
   - Qual comparação numérica usar?
   - Custo de não agir (quantificado)
   - ROI tangível

6. **Urgência real:**
   - Por que AGORA e não depois?
   - Qual escassez usar? (real, não fake)

### Prompt Estratégico para Hormozi-Copywriter

```bash
# Invocar hormozi-copywriter
Skill(command="hormozi-copywriter")
```

**Template do prompt (adaptar ao nicho):**

```
Você é Alex Hormozi analisando o negócio de [NICHO].

CONTEXTO DO MERCADO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Avatar: [descrição específica - ex: "mulher 28-35 anos, 1 filho pequeno,
        ganhou 18kg na gravidez, voltou ao trabalho há 6 meses, tenta
        emagrecer desde que o bebê nasceu"]

Dor principal: [pain of silence - ex: "não cabe mais nas roupas de antes,
               evita fotos com o filho, marido parou de elogiar, se sente
               invisível"]

Tentativas anteriores: [o que já tentou - ex: "3 nutricionistas diferentes,
                       academia 2x (cancelou por falta de tempo), dieta do
                       YouTube, chás detox, jejum intermitente"]

Objeção #1: [a maior - ex: "não tenho tempo, bebê mama de 3 em 3 horas,
            trabalho integral, não consigo ir pra academia"]

Dream Outcome: [específico - ex: "perder os 18kg em 90 dias, voltar a
               usar jeans 38, marido elogiar de novo, ter energia pra
               brincar com o filho"]

ANÁLISE HORMOZI:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Contradição ideal: [ex: "Fiz 240 horas de academia em 8 meses. Perdi 2kg.
                   Mudei UMA coisa em casa. Perdi 18kg em 90 dias."]

Matemática brutal: [ex: "Academia: R$ 120/mês x 8 meses = R$ 960 gastos.
                   Resultado: 2kg. Meu método: R$ 297 total. Resultado: 18kg."]

Objeção a destruir: [ex: "Você NÃO precisa de tempo. Precisa de MÉTODO.
                    15min/dia > 2h de academia errada."]

Urgência real: [ex: "Seu filho vai lembrar da mãe cansada ou da mãe
               que brincava com ele? Cada dia sem energia é um dia
               perdido que não volta."]

TAREFA:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Com essa análise estratégica, crie 3 versões de carrossel viral (7-10 slides).

Cada versão deve:
- Hook diferente (usando contradição específica)
- Destruir objeção #1 de forma única
- Mostrar matemática brutal com números reais
- CTA que gera ação IMEDIATA

Estrutura obrigatória:
[Slide 1] Hook com contradição
[Slide 2] Credibilidade (casos reais, números)
[Slide 3] Objeção (validar a dor)
[Slide 4] Reframe da objeção (destruir crença)
[Slide 5] Matemática brutal (comparação numérica)
[Slide 6] Prova (antes/depois, depoimentos)
[Slide 7] Solução (método específico)
[Slide 8] Garantia/risco reverso
[Slide 9] Urgência real
[Slide 10] CTA forte

NÃO crie copy genérica. Use a análise acima para copy CIRÚRGICA.

Formato de retorno:
VERSÃO 1: [Nome estratégico - ex: "Contradição Tempo"]
[Slide 1] ...
[Slide 2] ...

VERSÃO 2: [Nome estratégico - ex: "Matemática Brutal Academia"]
[Slide 1] ...
[Slide 2] ...

VERSÃO 3: [Nome estratégico - ex: "Objeção Marido"]
[Slide 1] ...
[Slide 2] ...
```

**Apresentar 3 versões ao usuário:**

```
🎯 3 VERSÕES DE COPY GERADAS:

VERSÃO 1: [Nome descritivo]
[Preview do hook]

VERSÃO 2: [Nome descritivo]
[Preview do hook]

VERSÃO 3: [Nome descritivo]
[Preview do hook]

Qual versão você prefere? (1, 2 ou 3)
```

**Aguardar escolha do usuário.**

## Step 3: Gerar Prompts Visuais (Colagem Artesanal)

**Após usuário escolher versão da copy:**

Para cada slide da copy escolhida, gerar um prompt visual usando o template abaixo.

### Template Visual Fixo (SEMPRE usar)

```
Crie uma colagem artesanal e realista feita à mão, com aparência de trabalho escolar sobre [tema].

Fundo de mesa de madeira clara, luz natural suave e papéis colados com sombras reais e bordas rasgadas.

Use papéis de cores diferentes (branco, amarelo e azul-claro) com escrita feita à mão em canetinhas de várias cores (vermelho, verde, preto e azul).

{CONTEUDO_DO_SLIDE}

Adicione ícones desenhados à mão: {ICONES_SUGERIDOS}

Finalize com detalhes de imperfeição realista — sombras, fita adesiva segurando o papel, traços tortos e variação de espessura da caneta, mantendo o ar de colagem artesanal autêntica.
```

### Gerar Prompts para Todos os Slides

**Para cada slide da copy escolhida:**

1. **{CONTEUDO_DO_SLIDE}**: Copy formatada para visual (quebras de linha, destaques, listas)
2. **{ICONES_SUGERIDOS}**: Ícones relevantes ao conteúdo (ex: "interrogação, casinha, cifrão")

**REGRA ESPECIAL - Slide 1:**

O primeiro slide DEVE ter uma foto representando o assunto (ex: imóvel, produto, pessoa) estilo recortado mantendo o estilo do prompt.

Exemplo de prompt Slide 1:

```
Crie uma colagem artesanal e realista feita à mão, com aparência de trabalho escolar sobre vendas de imóveis.

Fundo de mesa de madeira clara, luz natural suave e papéis colados com sombras reais e bordas rasgadas.

Use papéis de cores diferentes (branco, amarelo e azul-claro) com escrita feita à mão em canetinhas de várias cores (vermelho, verde, preto e azul).

LAYOUT DIVIDIDO VERTICAL:

Lado esquerdo: Foto recortada de um imóvel/terreno colada na madeira (estilo scrapbook)

Lado direito: Papéis coloridos com escrita à mão:
"VOCÊ VAI PAGAR R$ 1.000/MÊS PELOS PRÓXIMOS 5 ANOS DE QUALQUER JEITO."
"A pergunta é: pra quem?"
"Aluguel ou patrimônio? Você decide."

Rodapé centralizado: Setinha desenhada (→) com texto: "Deslize para continuar ➜"

Adicione ícones desenhados à mão: interrogação, casinha, cifrão

Finalize com detalhes de imperfeição realista — sombras, fita adesiva segurando o papel, traços tortos e variação de espessura da caneta, mantendo o ar de colagem artesanal autêntica.
```

### Retornar Lista Estruturada

**Formato de retorno:**

```json
[
  {
    "slide": 1,
    "conteudo": "LAYOUT DIVIDIDO VERTICAL:\n\nLado esquerdo: Foto recortada...",
    "icones": "interrogação, casinha, cifrão"
  },
  {
    "slide": 2,
    "conteudo": "No topo: 'Levei 23 famílias...'",
    "icones": "grid com 23 casinhas, check verde"
  },
  ...
]
```

**Salvar JSON temporariamente:**

```bash
# Salvar prompts em JSON para o script batch
echo '[...]' > /tmp/carrossel_prompts.json
```

## Step 4: Gerar Slides em Batch (Paralelo)

**Executar script de geração em paralelo:**

```bash
python3 /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/SCRIPTS/image-generation/batch_carrossel_gpt4o.py \
  --prompts-file /tmp/carrossel_prompts.json \
  --variants 4 \
  --yes
```

**Parâmetros:**
- `--prompts-file`: JSON com prompts de todos os slides
- `--variants`: Número de variantes por slide (padrão: 4)
- `--yes`: Pular confirmação manual

**Características do script:**
- Gera TODOS os slides em paralelo (máxima velocidade)
- 4 variantes por slide (escolher melhor depois)
- Salva em `~/Downloads/carrossel_slide_01_v1.png`, `carrossel_slide_01_v2.png`, etc.

## Step 5: Organizar Pasta Final

**Após geração completa:**

1. Criar pasta com nome adequado:

```bash
cd ~/Downloads
mkdir "carrossel_[tema]_$(date +%Y%m%d)"
```

2. Mover slides para pasta organizada:

```bash
# Renomear slides com nomes descritivos
mv carrossel_slide_01_v1.png "carrossel_[tema]_$(date +%Y%m%d)/slide_1_hook_v1.png"
mv carrossel_slide_02_v1.png "carrossel_[tema]_$(date +%Y%m%d)/slide_2_credibilidade_v1.png"
# ... etc para todos os slides
```

3. Criar README.txt na pasta:

```bash
cat > "carrossel_[tema]_$(date +%Y%m%d)/README.txt" << EOF
CARROSSEL VIRAL - [TEMA]
Data: $(date +%Y-%m-%d)

Slides:
1. Hook
2. Credibilidade
3. Problema
4. Solução
5. Matemática
6. Objeção
7. CTA

Cada slide tem 4 variantes (_v1, _v2, _v3, _v4).
Escolher melhor variante de cada antes de publicar.

Copy completa salva em: copy.txt
EOF
```

4. Salvar copy escolhida:

```bash
cat > "carrossel_[tema]_$(date +%Y%m%d)/copy.txt" << EOF
[Copy completa da versão escolhida]
EOF
```

## Step 6: Entregar ao Usuário

**Resumo final:**

```
✅ Carrossel pronto!

📂 Local: ~/Downloads/carrossel_[tema]_[data]/
📊 Slides: 10 slides × 4 variantes = 40 imagens
🎨 Visual: Colagem artesanal Hormozi
📝 Copy: Versão [X] escolhida

Próximos passos:
1. Abrir pasta e revisar slides
2. Escolher melhor variante de cada slide
3. Upload para Meta Ads / Instagram / LinkedIn
```

## Exemplo Completo

**User:** "Preciso de um carrossel viral pra vender terrenos"

**Assistant:**

1️⃣ Tema identificado: Venda de terrenos

2️⃣ Fazendo análise estratégica do negócio...

```
ANÁLISE HORMOZI - VENDA DE TERRENOS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Avatar: Pessoa 25-40 anos, pagando aluguel R$ 800-1.200/mês,
        cansada de "jogar dinheiro fora", quer patrimônio mas
        banco negou financiamento (score baixo/sem comprovante renda)

Dor principal: Paga aluguel há 5+ anos, nunca sobra pra entrada,
               vê preços subindo, sente que nunca vai ter casa própria,
               família cobra ("até quando vão morar de aluguel?")

Tentativas anteriores: Foi em 3 bancos, todos negaram. Tentou juntar
                       entrada mas sempre aparece imprevisto. Viu
                       terrenos que gostava ficarem 30% mais caros.

Objeção #1: "Não tenho entrada" / "Nome sujo, banco não aprova"

Dream Outcome: Ter terreno próprio em 60 dias, parar de pagar aluguel,
               construir aos poucos, deixar patrimônio pros filhos

Contradição: "Fui em 3 bancos. Todos negaram. Desisti. Cliente me
             mostrou que EU NUNCA PRECISEI de banco. Comprei em 48h."

Matemática brutal: "Aluguel: R$ 1.000/mês x 60 meses = R$ 60.000 gastos.
                   Patrimônio: R$ 0. Terreno: R$ 10k entrada + 60x R$ 1.000
                   = R$ 70k investidos. Patrimônio: R$ 120k+"

Objeção a destruir: "Você NÃO precisa de banco. Banco = juros, burocracia,
                    humilhação. Aqui = entrada + parcelas FIXAS, sem juros."

Urgência real: "Segunda-feira: 17 lotes. Hoje: 9 lotes. Preço sobe
               semana que vem. Cada mês esperando = mais caro."
```

3️⃣ Invocando hormozi-copywriter com análise estratégica...

```
🎯 3 VERSÕES DE COPY GERADAS:

VERSÃO 1: Contradição Banco (foco: destruir necessidade de aprovação)
"FUI EM 3 BANCOS. TODOS NEGARAM. DESISTI. 6 MESES DEPOIS..."

VERSÃO 2: Matemática Brutal Aluguel (foco: comparação numérica)
"VOCÊ VAI PAGAR R$ 1.000/MÊS PELOS PRÓXIMOS 5 ANOS DE QUALQUER JEITO..."

VERSÃO 3: Urgência Preço (foco: custo de procrastinação)
"HÁ 2 ANOS TERRENO CUSTAVA R$ 40K. HOJE R$ 70K. DAQUI 2 ANOS..."

Qual versão você prefere? (1, 2 ou 3)
```

**User:** "1"

3️⃣ Versão 1 escolhida. Gerando prompts visuais...

```json
[
  {"slide": 1, "conteudo": "LAYOUT DIVIDIDO...", "icones": "..."},
  {"slide": 2, "conteudo": "...", "icones": "..."},
  ...
]
```

4️⃣ Executando geração em batch (paralelo)...

```bash
python3 batch_carrossel_gpt4o.py --prompts-file /tmp/carrossel_prompts.json --variants 4 --yes
```

5️⃣ Organizando pasta final...

```bash
mkdir ~/Downloads/carrossel_terrenos_20250107
mv carrossel_slide_*.png ~/Downloads/carrossel_terrenos_20250107/
```

6️⃣ Pronto!

```
✅ Carrossel pronto!

📂 Local: ~/Downloads/carrossel_terrenos_20250107/
📊 Slides: 10 slides × 4 variantes = 40 imagens
🎨 Visual: Colagem artesanal Hormozi
📝 Copy: Versão 1 (Matemática Brutal)

Próximos passos:
1. Abrir pasta e revisar slides
2. Escolher melhor variante de cada slide
3. Upload para Meta Ads
```

## Resources

### scripts/

**Script batch de geração:**
- `batch_carrossel_gpt4o.py` - Já existe em `/SCRIPTS/image-generation/`
- Gera todos os slides em paralelo
- Suporta 4-10 variantes por slide
- Usa GPT-4o Image Generation

### references/

**Não necessário** - Hormozi copywriter já tem referências próprias.

### assets/

**Não necessário** - Visual é gerado dinamicamente pelo script.

## Workflow Decision Tree

```
Usuário pede carrossel
    │
    ├─> Tema fornecido?
    │   NO → Perguntar tema
    │   YES → Continuar
    │
    ├─> ANÁLISE ESTRATÉGICA DO NEGÓCIO
    │   ├─> Avatar específico (idade, situação, contexto)
    │   ├─> Dor principal (pain of silence)
    │   ├─> Tentativas anteriores (o que já tentou)
    │   ├─> Objeção #1 (maior desculpa)
    │   ├─> Dream Outcome (resultado + timeline)
    │   ├─> Contradição (esforço alto→baixo vs resultado baixo→alto)
    │   ├─> Matemática brutal (comparação numérica)
    │   └─> Urgência real (por que AGORA)
    │
    ├─> Invocar hormozi-copywriter COM ANÁLISE ESTRATÉGICA
    │   ├─> Prompt como consultor (não genérico)
    │   ├─> Contexto completo do negócio
    │   ├─> Direções táticas de Hormozi
    │   └─> Gerar 3 versões de copy (cada com abordagem única)
    │
    ├─> Apresentar 3 versões ao usuário
    │   → Usuário escolhe (1, 2 ou 3)
    │
    ├─> Gerar prompts visuais
    │   → Para cada slide da copy escolhida
    │   → Template colagem artesanal
    │   → Slide 1 tem foto recortada
    │   → Salvar JSON temporário
    │
    ├─> Executar batch_carrossel_gpt4o.py
    │   → --prompts-file /tmp/carrossel_prompts.json
    │   → --variants 4
    │   → --yes (auto-confirmar)
    │   → Geração 100% paralela
    │
    ├─> Organizar pasta final
    │   → Criar pasta com nome adequado
    │   → Renomear slides descritivamente
    │   → Criar README.txt
    │   → Salvar copy escolhida + análise estratégica
    │
    └─> Entregar ao usuário
        → Resumo final
        → Próximos passos
```

## Auto-Correção de Erros

Esta skill possui sistema de auto-correção automático integrado.

**Quando um erro ocorrer:**

1. **Detecção automática:** Erro é detectado imediatamente
2. **Invocação do fix-skill:** Skill fix-skill é chamada automaticamente (sem intervenção manual)
3. **Análise e correção:** fix-skill analisa o erro, corrige SKILL.md
4. **Registro:** Erro é registrado em LEARNINGS.md para histórico
5. **Retry:** Operação é tentada novamente automaticamente
6. **Prevenção:** Mesmo erro nunca mais acontece

**Fluxo de auto-correção:**

```
Erro detectado
↓
fix-skill auto-invocada
↓
SKILL.md corrigido
↓
LEARNINGS.md atualizado
↓
Retry automático
↓
✅ Sucesso!
```

**Sem intervenção necessária:** O usuário não precisa pedir "/fix-skill", acontece automaticamente.

**Histórico:** Todos os erros corrigidos ficam registrados em `LEARNINGS.md` desta skill.
