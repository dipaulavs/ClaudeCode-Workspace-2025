# Examples - Casos de Uso Reais

## Exemplo 1: Chácara com Parcelamento Direto

### Input do Usuário

```
"Quero criar um carrossel Meta Ads para uma chácara de 1.000m².

Dados:
- Preço: R$ 70.000
- Entrada: R$ 10.000
- Parcela: R$ 1.000/mês
- Prazo: 60 meses
- Localização: Itatiaiuçu, 15min do centro de BH
- Foto: https://media.loop9.com.br/s/ABC123/chacara.jpg
"
```

### Workflow da Skill

**1. Coleta de Dados:** ✅ Já fornecidos

**2. Subagente Copy gera 3 opções:**

```
Opção 1 (10 slides): Matemática Brutal
- Foco: Aluguel vs Imóvel
- Target: Público geral

Opção 2 (8 slides): Objeção Nome Sujo
- Foco: Sem banco, sem score
- Target: Pessoas com restrição

Opção 3 (5 slides): Urgência Rápida
- Foco: Escassez + Valorização
- Target: Decisor rápido
```

**3. Usuário escolhe:** Opção 1 (10 slides)

**4. Subagente Prompts gera:**

```json
[
  {
    "slide": 1,
    "conteudo": "No topo: 'VOCÊ VAI PAGAR R$ 1.000/MÊS PELOS PRÓXIMOS 5 ANOS DE QUALQUER JEITO.' Abaixo: 'A pergunta é: pra quem?' Em papel amarelo: 'Aluguel ou patrimônio? Você decide.'",
    "icones": "interrogação gigante, casinha, cifrão"
  },
  ...
]
```

**5. Geração:** 10 slides × 4 variantes = 40 imagens

**6. Output:**
```
✅ Carrossel gerado com sucesso!
📂 ~/Downloads/carrossel_slide_01_v1.png até carrossel_slide_10_v4.png
⏱️ Tempo: 6min 23s
```

---

## Exemplo 2: Apartamento em Construção

### Input do Usuário

```
"Preciso anunciar um apartamento 2 quartos, entrega em 2026.

Preço: R$ 280.000
Entrada: R$ 50.000
Parcela: R$ 1.800 durante obra + R$ 1.500 após (financiado)
Localização: Bairro Castelo, BH
Sem foto ainda (na planta)
"
```

### Adaptação da Skill

**Diferencial:** Imóvel na planta (sem foto real)

**Subagente Copy adapta:**
- Slide 1: Usa ilustração/planta (não foto real)
- Enfoque em "valorização durante obra"
- Comparação: Comprar pronto × Comprar na planta

**Opções geradas:**

```
Opção 1 (7 slides): Valorização Garantida
- Slide 1: "IMÓVEL VALORIZA 30% DURANTE A OBRA"
- Matemática: Paga R$ 280k, vale R$ 364k na entrega
- CTA: Últimas unidades

Opção 2 (6 slides): Sem Financiamento Banco
- Foco: Financiamento direto com construtora
- Objeção: "Nome sujo"

Opção 3 (5 slides): Localização Premium
- Foco: Bairro Castelo (valorização histórica)
- Comparação: Alugar vs Comprar
```

**Resultado:** 6 slides × 4 variantes = 24 imagens

---

## Exemplo 3: Lote Industrial

### Input do Usuário

```
"Carrossel para lote comercial/industrial.

Dados:
- Área: 5.000m²
- Preço: R$ 1.500.000
- Entrada: R$ 300.000
- Parcelas: R$ 20.000/mês × 60 meses
- Localização: BR-381, acesso direto
- Target: Empresários/investidores
"
```

### Adaptação da Skill

**Público diferente:** B2B (não B2C)

**Subagente Copy adapta tom:**

```
Opção 1 (8 slides): ROI Industrial
- Slide 1: "QUANTO VOCÊ PERDE PAGANDO ALUGUEL DO GALPÃO?"
- Matemática: Aluguel industrial × 5 anos = R$ 1.2M desperdiçados
- Comparação: Custo de oportunidade
- CTA: "Para empresários que querem patrimônio"

Opção 2 (6 slides): Expansão vs Aluguel
- Foco: Crescimento da empresa travado por aluguel
- Caso: Empresa que triplicou após ter imóvel próprio

Opção 3 (5 slides): Localização Estratégica
- BR-381 (logística)
- Economia em frete
- Valorização comercial
```

**Resultado:** 8 slides × 4 variantes = 32 imagens

---

## Exemplo 4: Usuário Rejeita Copy Inicial

### Fluxo com Feedback

**1. Opções geradas (primeira tentativa):**
```
Opção 1: Matemática Brutal (10 slides)
Opção 2: Nome Sujo (8 slides)
Opção 3: Urgência (5 slides)
```

**2. Usuário rejeita:**
```
"Não gostei de nenhuma. Quero algo mais focado em 'sair da cidade' e qualidade de vida, não só matemática."
```

**3. Skill reprocessa com feedback:**

Subagente Copy recebe:
- Dados originais
- Feedback: "Foco em qualidade de vida, sair da cidade"
- Exemplos Hormozi (REFERENCE.md)

**4. Novas opções geradas:**

```
Opção 1 (9 slides): Qualidade de Vida
- Slide 1: "QUANTOS ANOS DE VIDA VOCÊ PERDEU NO TRÂNSITO?"
- Comparação: 2h/dia trânsito × 5 anos = 3.650 horas (152 dias)
- Solução: Chácara 15min do trabalho
- Matemática: Mesmo preço, vida melhor

Opção 2 (7 slides): Saúde Mental
- Foco: Estresse × Natureza
- Estudos: Pessoas próximas à natureza vivem mais
- CTA: "Investimento em saúde, não só imóvel"

Opção 3 (6 slides): Família
- Slide 1: "SEUS FILHOS MERECEM QUINTAL, NÃO CONCRETO"
- Comparação emocional (não só matemática)
```

**5. Usuário aprova:** Opção 1

**Resultado:** Copy personalizada mantendo estrutura Hormozi

---

## Exemplo 5: Múltiplos Carrosséis para A/B Test

### Input do Usuário

```
"Quero testar 3 ângulos diferentes do mesmo imóvel para ver qual converte melhor."
```

### Workflow

**1. Skill pergunta:** "Quer 3 carrosséis completos ou 3 primeiros slides (hook test)?"

**2. Usuário escolhe:** "3 hooks diferentes"

**3. Subagente gera 3 hooks:**

```
Hook A (Matemática):
"VOCÊ VAI PAGAR R$ 1.000/MÊS DE QUALQUER JEITO. Pra quem?"

Hook B (Emocional):
"CANSADO DE ENRIQUECER O DONO DO IMÓVEL?"

Hook C (Urgência):
"9 UNIDADES. SEMANA QUE VEM: 4. PRÓXIMA: 0."
```

**4. Skill gera 3 variações do Slide 1 apenas**

**5. Usuário testa no Meta Ads:**
- Hook A: CTR 3.2%
- Hook B: CTR 4.1% ← **Vencedor**
- Hook C: CTR 2.8%

**6. Skill continua com Hook B:**
Gera carrossel completo usando o hook vencedor.

---

## Exemplo 6: Carrossel para Stories (Vertical)

### Input do Usuário

```
"Mesma chácara, mas quero versão para Stories (9:16)"
```

### Adaptação

**Mudança no gerador:**
```bash
python3 scripts/image-generation/batch_carrossel_gpt4o.py \
  --prompts-file ~/Downloads/carrossel_prompts.json \
  --aspect-ratio 9:16  # ← Stories
  --variants 4
```

**Copy adaptada:**
- Textos mais curtos (tela vertical menor)
- Menos elementos por slide
- CTAs mais diretos

---

## Exemplo 7: Integração com Instagram API

### Workflow Completo: Criar + Publicar

**1. Skill gera carrossel** (10 slides × 4 variantes)

**2. Usuário escolhe melhores variantes:**
```
Slide 1: v2
Slide 2: v1
Slide 3: v3
...
Slide 10: v4
```

**3. Upload para Instagram:**

```bash
python3 scripts/instagram/publish_carousel.py \
  ~/Downloads/carrossel_slide_01_v2.png \
  ~/Downloads/carrossel_slide_02_v1.png \
  ~/Downloads/carrossel_slide_03_v3.png \
  ... \
  --caption "🏡 Chácara 1.000m² | R$ 10k entrada + R$ 1k/mês | Última unidade! 👉 DM"
```

**Resultado:** Carrossel publicado automaticamente no Instagram.

---

## Lições dos Exemplos

### ✅ O que funciona:

1. **Dados completos logo no início** acelera processo
2. **Feedback específico** gera melhores resultados
3. **Testar hooks** antes do carrossel completo economiza tempo/dinheiro
4. **Matemática brutal** funciona para público amplo
5. **Objeções específicas** (nome sujo) convertem segmentado

### ❌ O que evitar:

1. **Dados incompletos:** Skill precisa perguntar muito
2. **"Quero algo diferente" sem detalhar:** Subagente não sabe o que fazer
3. **Pular aprovação da copy:** Pode gerar 40 imagens erradas
4. **Não testar variantes:** Desperdiça potencial de otimização
