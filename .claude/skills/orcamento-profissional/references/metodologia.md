# 📚 Orçamento Profissional - Documentação Técnica Completa

## Índice

1. [Metodologia de Precificação](#metodologia-de-precificação)
2. [Análise de Recursos](#análise-de-recursos)
3. [Cálculo de ROI](#cálculo-de-roi)
4. [Estrutura de Apresentação](#estrutura-de-apresentação)
5. [Frameworks de Ancoragem](#frameworks-de-ancoragem)
6. [Valores Quebrados (Preços Psicológicos)](#valores-quebrados-preços-psicológicos)
7. [Fórmulas e Cálculos](#fórmulas-e-cálculos)

---

## Metodologia de Precificação

### Filosofia: Valor vs Tempo

**❌ Mentalidade CLT (Evitar):**
```
Preço = Horas × Valor/Hora
Exemplo: 40h × R$ 150/h = R$ 6.000
```
**Problema:** Penaliza eficiência. Quanto mais rápido você é, menos ganha.

**✅ Mentalidade Valor (Usar):**
```
Preço = % do Valor Gerado
Exemplo: 5% de R$ 120.000/ano = R$ 6.000
```
**Vantagem:** Alinhado com resultado do cliente. Quanto mais valor gera, mais pode cobrar.

---

### Fórmula Master de Precificação

```
Preço Justo = (Valor Gerado no Ano 1) × (2% a 10%)

Onde:
- 2% = Projetos commoditizados, baixa complexidade
- 5% = Projetos personalizados, média complexidade (PADRÃO)
- 10% = Projetos estratégicos, alta complexidade/risco
```

**Regra de ROI Mínimo:** Cliente deve ter ROI de **pelo menos 3x** no primeiro ano.

---

### Componentes do Valor Gerado

**1. Receita Nova (Direta):**
- Vendas aumentadas
- Novos canais de receita
- Conversão melhorada

**2. Economia de Custos:**
- Redução de despesas operacionais
- Eliminação de ferramentas/serviços
- Otimização de processos

**3. Valor do Tempo (Indireto):**
```
Tempo Economizado (horas/mês) × Valor/Hora do Cliente
Exemplo: 80h/mês × R$ 50/h = R$ 4.000/mês = R$ 48.000/ano
```

**4. Custo de Oportunidade:**
- O que cliente PERDE por não ter isso?
- Vendas perdidas
- Clientes perdidos
- Posicionamento de mercado

**Fórmula Completa:**
```
Valor Total = Receita Nova + Economia + Valor Tempo + Custo Oportunidade
```

---

## Análise de Recursos

### Categorização de Esforço

**✅ Verde (0-20% esforço):**
- Script pronto, apenas configurar
- Skill existente, apenas invocar
- API já integrada, apenas usar

**Exemplo:**
```python
# scripts/whatsapp/send_message.py (Verde)
# Apenas configurar: phone, message
# Esforço: 5min de config
```

**🟡 Amarelo (20-50% esforço):**
- Script existente, precisa adaptar lógica
- Skill existente, precisa customizar
- API integrada, precisa novos endpoints

**Exemplo:**
```python
# scripts/meta-ads/create_campaign.py (Amarelo)
# Adaptar: objetivo, público, criativos customizados
# Esforço: 2-4h de adaptação
```

**🔴 Vermelho (50-100% esforço):**
- Nenhum script similar
- Skill nova necessária
- API nova para integrar
- Lógica complexa do zero

**Exemplo:**
```python
# Integração API customizada do cliente (Vermelho)
# Criar: autenticação, endpoints, error handling
# Esforço: 8-20h de desenvolvimento
```

---

### Mapeamento Automático

**Comandos para mapear recursos:**

```bash
# Buscar scripts relacionados
grep -r "palavra-chave" scripts/*/README.md

# Listar skills disponíveis
ls -la .claude/skills/

# Buscar ferramentas low-level
ls tools/ | grep "palavra-chave"
```

**Output esperado:**
```
📦 Recursos Disponíveis:

Categoria: WhatsApp
├─ ✅ send_message.py (pronto)
├─ ✅ send_media.py (pronto)
└─ 🟡 create_group.py (adaptar nomes)

Categoria: Imagens
├─ ✅ generate_nanobanana.py (pronto)
└─ ✅ batch_generate.py (pronto)

Categoria: Skills
├─ ✅ hormozi-leads (copy persuasivo)
└─ ✅ visual-explainer (apresentação)

Criar do Zero:
└─ 🔴 Integração API XYZ (20h estimadas)
```

---

## Cálculo de ROI

### Framework de 3 Cenários

**Sempre apresentar 3 cenários realistas:**

**1. Conservador (Pessimista, 3x ROI):**
- Usa dados mínimos garantidos
- Assume adoção lenta
- Margens conservadoras

**2. Realista (Esperado, 5x ROI):**
- Usa benchmarks de mercado
- Assume adoção normal
- Margens medianas

**3. Otimista (Melhor caso, 10x ROI):**
- Usa máximo observado no setor
- Assume adoção rápida
- Margens otimistas (mas não fantasiosas)

---

### Template de Cálculo

```markdown
## ROI Projetado (Ano 1)

### Cenário Conservador (3x)
**Premissas:**
- Receita nova: R$ 10.000/mês × 12 = R$ 120.000
- Economia tempo: 40h/mês × R$ 50/h × 12 = R$ 24.000
- Redução custos: R$ 1.000/mês × 12 = R$ 12.000

**Total Valor:** R$ 156.000
**Investimento:** R$ 6.000
**ROI:** 26x (R$ 156k ÷ R$ 6k)

### Cenário Realista (5x)
[mesma estrutura]

### Cenário Otimista (10x)
[mesma estrutura]
```

---

### Fontes de Dados para ROI

**1. Benchmarks de Mercado:**
- Relatórios setoriais (McKinsey, Gartner)
- Estudos de caso públicos
- Dados de concorrentes

**2. Dados do Cliente:**
- Faturamento atual
- Custos operacionais
- Tempo gasto em processos manuais

**3. Estimativas Conservadoras:**
- Se não tem dados → usar limites inferiores
- NUNCA inventar números sem base
- Sempre explicar premissas

---

## Estrutura de Apresentação

### Slides Obrigatórios (10 slides)

**Slide 1: Capa**
```html
<h1>Proposta: [Nome do Projeto]</h1>
<h2>Para: [Nome do Cliente]</h2>
<p>Por: [Seu Nome/Empresa]</p>
<p>Data: [DD/MM/YYYY]</p>
```

**Slide 2: Problema (Situação Atual)**
```html
<h2>Situação Atual</h2>
<ul>
  <li>❌ [Dor 1 específica]</li>
  <li>❌ [Dor 2 específica]</li>
  <li>❌ [Dor 3 específica]</li>
</ul>
<p><strong>Custo dessa situação:</strong> R$ [valor]/mês</p>
```

**Slide 3: Solução (Transformação)**
```html
<h2>Solução Proposta</h2>
<p>[Descrição em 2-3 linhas do que será entregue]</p>
<ul>
  <li>✅ [Benefício 1]</li>
  <li>✅ [Benefício 2]</li>
  <li>✅ [Benefício 3]</li>
</ul>
```

**Slide 4: Processos (Como será feito)**
```html
<h2>Como Funciona</h2>
<div class="process-flow">
  <div>1. [Etapa 1]</div> →
  <div>2. [Etapa 2]</div> →
  <div>3. [Etapa 3]</div> →
  <div>✅ Resultado</div>
</div>
```

**Slide 5: Recursos (O que já existe)**
```html
<h2>Recursos Utilizados</h2>
<div class="resources">
  <div class="green">✅ Reutilizáveis (80%)</div>
  <div class="yellow">🟡 Adaptações (15%)</div>
  <div class="red">🔴 Desenvolvimento (5%)</div>
</div>
<p><strong>Vantagem:</strong> Velocidade e confiabilidade comprovadas</p>
```

**Slide 6: Timeline**
```html
<h2>Cronograma</h2>
<ul>
  <li>Semana 1-2: [Fase 1]</li>
  <li>Semana 3-4: [Fase 2]</li>
  <li>Semana 5-6: [Fase 3]</li>
  <li>Semana 7: Testes e ajustes</li>
  <li>Semana 8: Entrega final</li>
</ul>
<p><strong>Prazo total:</strong> 8 semanas</p>
```

**Slide 7: Investimento (Preço + Ancoragem)**
```html
<h2>Investimento</h2>
<p class="price">R$ 6.000</p>

<h3>Comparações Realistas:</h3>
<ul>
  <li>Vs Contratar CLT: Economia de R$ 36.000/ano</li>
  <li>Vs Fazer manual: Libera 960h/ano</li>
  <li>Vs Não fazer: Deixa de ganhar R$ 80.000/ano</li>
</ul>

<p><strong>Retorno do investimento:</strong> Em 27 dias</p>
```

**Slide 8: ROI Matemático (3 Cenários)**
```html
<h2>Projeção de Resultados (Ano 1)</h2>
<div class="scenarios">
  <div class="conservative">
    <h3>🟢 Conservador (3x)</h3>
    <p>Investimento: R$ 6.000</p>
    <p>Retorno: R$ 18.000</p>
    <p>Lucro: R$ 12.000</p>
  </div>
  <div class="realistic">
    <h3>🟡 Realista (5x)</h3>
    <p>Investimento: R$ 6.000</p>
    <p>Retorno: R$ 30.000</p>
    <p>Lucro: R$ 24.000</p>
  </div>
  <div class="optimistic">
    <h3>🔵 Otimista (10x)</h3>
    <p>Investimento: R$ 6.000</p>
    <p>Retorno: R$ 60.000</p>
    <p>Lucro: R$ 54.000</p>
  </div>
</div>
```

**Slide 9: Garantias (O que está incluso)**
```html
<h2>O Que Está Incluso</h2>
<ul>
  <li>✅ [Entregável 1]</li>
  <li>✅ [Entregável 2]</li>
  <li>✅ [Entregável 3]</li>
  <li>✅ Suporte de 30 dias</li>
  <li>✅ Documentação completa</li>
  <li>✅ Treinamento da equipe</li>
</ul>
```

**Slide 10: CTA (Próximos Passos)**
```html
<h2>Próximos Passos</h2>
<ol>
  <li>Você aprova a proposta</li>
  <li>Assinamos contrato</li>
  <li>Pagamento: [forma de pagamento]</li>
  <li>Início em [data]</li>
  <li>Entrega em [data]</li>
</ol>
<p><strong>Dúvidas?</strong> [email/telefone]</p>
```

---

## Frameworks de Ancoragem

### Tipos de Ancoragem

**1. Ancoragem por Comparação:**
```
R$ 6.000 (seu preço)
vs
R$ 3.500/mês CLT = R$ 42.000/ano (economia de R$ 36k)
```

**2. Ancoragem por Tempo:**
```
Investimento: R$ 6.000
Resultado esperado: R$ 30.000/ano
Payback: 2.4 meses (73 dias)
```

**3. Ancoragem por Oportunidade:**
```
Custo de não fazer:
- Perda de R$ 5.000/mês = R$ 60.000/ano
- Investir R$ 6.000 evita perder R$ 60.000
```

**4. Ancoragem por Divisão:**
```
R$ 6.000 total
= R$ 500/mês (parcelado 12x)
= R$ 16,67/dia
= Menos que 2 cafés/dia
```

---

### Equação de Valor (Hormozi)

**Fórmula:**
```
Valor Percebido = (Dream Outcome × Perceived Likelihood)
                  ÷ (Time Delay × Effort & Sacrifice)
```

**Como aplicar em orçamentos:**

**Aumentar numerador:**
- **Dream Outcome:** "Você vai ganhar R$ 30k/ano"
- **Perceived Likelihood:** "Usando ferramentas já testadas (67 templates)"

**Diminuir denominador:**
- **Time Delay:** "Entrega em 8 semanas (não 6 meses)"
- **Effort & Sacrifice:** "Zero esforço da sua equipe, fazemos tudo"

---

## Valores Quebrados (Preços Psicológicos)

### Fundamento: Percepção de Preço

**Cérebro processa preços da esquerda para direita:**

```
R$ 3.500 → "Três mil e quinhentos"
R$ 3.497 → "Três mil e..." (cérebro arredonda para baixo)
```

**Resultado:** R$ 3.497 parece significativamente mais barato que R$ 3.500, mesmo sendo diferença de R$ 3.

---

### Regra dos Dígitos Mágicos

**SEMPRE terminar preços em:**
- **7** → R$ 1.497, R$ 3.497, R$ 5.997
- **9** → R$ 1.499, R$ 3.499, R$ 5.999

**NUNCA terminar em:**
- **0** → R$ 1.500, R$ 3.500 (parece "redondo", caro)
- **5** → R$ 1.495, R$ 3.495 (sem impacto psicológico)

---

### Técnica Completa (4 Passos)

#### **Passo 1: Calcular Preço Base**
```python
# Preço justo baseado em valor
preco_base = 3500  # R$
```

#### **Passo 2: Criar Ancoragem Alta (+35-40%)**
```python
# Adicionar 35-40% para criar "tabela empresas"
ancoragem = preco_base * 1.37  # 37% maior
# R$ 3.500 × 1.37 = R$ 4.795

# Aplicar valor quebrado na ancoragem
ancoragem_quebrada = 4791  # R$ (arredondar para terminar em 1, 7 ou 9)
```

#### **Passo 3: Calcular Descontos Nomeados**
```python
# Total de desconto = diferença entre ancoragem e preço desejado
desconto_total = ancoragem_quebrada - preco_base  # R$ 1.291

# Dividir em 2 descontos nomeados (psicologia)
desconto_1 = 800  # "Desconto parceria estratégica"
desconto_2 = desconto_total - desconto_1  # R$ 491 → arredondar para 494
```

#### **Passo 4: Valor Final Quebrado**
```python
# Aplicar descontos e ajustar para valor quebrado
preco_final = ancoragem_quebrada - desconto_1 - desconto_2
# R$ 4.791 - R$ 800 - R$ 494 = R$ 3.497 ✅

# Garantir que termina em 7 ou 9
if preco_final % 10 not in [7, 9]:
    preco_final = (preco_final // 10) * 10 + 7
```

---

### Exemplo Prático Completo

**Cenário:** Projeto vale R$ 3.500/mês (preço base justo)

**Aplicando técnica:**

```
1. Preço base: R$ 3.500

2. Ancoragem (+37%): R$ 4.795 → R$ 4.791 (quebrado)

3. Descontos nomeados:
   - Desconto parceria: -R$ 800
   - Desconto combo: -R$ 494

4. Valor final: R$ 4.791 - R$ 1.294 = R$ 3.497 ✅
```

**Apresentação ao cliente:**
```html
<h2>Investimento</h2>

<div class="regular-price">
  <p class="strikethrough">Tabela empresas: R$ 4.791/mês</p>
</div>

<div class="discounts">
  <p>✅ Desconto parceria estratégica: -R$ 800</p>
  <p>✅ Desconto combo completo: -R$ 494</p>
</div>

<div class="final-price">
  <h3>Investimento para [Cliente]:</h3>
  <p class="big-price">R$ 3.497/mês</p>
  <p class="small">Economia de R$ 1.294/mês (27%)</p>
</div>
```

---

### Tabela de Conversão Rápida

| Preço Base | Ancoragem (+37%) | Desconto Total | Preço Final Quebrado |
|------------|------------------|----------------|----------------------|
| R$ 1.000 | R$ 1.397 | R$ 400 | R$ 997 |
| R$ 1.500 | R$ 2.097 | R$ 600 | R$ 1.497 |
| R$ 2.000 | R$ 2.797 | R$ 800 | R$ 1.997 |
| R$ 2.500 | R$ 3.497 | R$ 1.000 | R$ 2.497 |
| R$ 3.000 | R$ 4.197 | R$ 1.200 | R$ 2.997 |
| R$ 3.500 | R$ 4.891 | R$ 1.394 | R$ 3.497 |
| R$ 4.000 | R$ 5.591 | R$ 1.594 | R$ 3.997 |
| R$ 5.000 | R$ 6.991 | R$ 1.994 | R$ 4.997 |
| R$ 6.000 | R$ 8.391 | R$ 2.394 | R$ 5.997 |
| R$ 8.000 | R$ 11.191 | R$ 3.194 | R$ 7.997 |
| R$ 10.000 | R$ 13.991 | R$ 3.994 | R$ 9.997 |

---

### Nomes de Descontos Persuasivos

**Use descontos nomeados (psicologia de exclusividade):**

**Opções de nomenclatura:**

1. **"Desconto Parceria Estratégica"**
   - Quando: Cliente grande, potencial de case
   - Mensagem: "Você é especial para nós"

2. **"Desconto Primeiro Cliente Setor"**
   - Quando: Primeiro cliente no nicho dele
   - Mensagem: "Você é pioneiro"

3. **"Desconto Combo Completo"**
   - Quando: Contrata múltiplos serviços
   - Mensagem: "Você é inteligente (comprou junto)"

4. **"Desconto Lançamento"**
   - Quando: Serviço novo que você oferece
   - Mensagem: "Pegou a oportunidade"

5. **"Desconto Pagamento à Vista"**
   - Quando: Cliente paga adiantado
   - Mensagem: "Você facilita nosso fluxo"

**SEMPRE use 2 descontos** (não 1, não 3):
- 1 desconto = parece simples demais
- 2 descontos = percepção de "muito desconto"
- 3+ descontos = cliente desconfia

---

### Setup Inicial (One-Time) Também Quebrado

**Consistência é chave:**

```
Se mensalidade: R$ 3.497
Então setup: R$ 1.497 (não R$ 1.500)

Se mensalidade: R$ 5.997
Então setup: R$ 1.997 (não R$ 2.000)
```

**Regra:** Setup = ~40-50% da primeira mensalidade, sempre quebrado.

---

### Impacto Real (Estudos)

**Pesquisas mostram:**
- Preços terminados em 9: +15-20% conversão vs preços redondos
- Preços terminados em 7: +10-15% conversão vs preços redondos
- Ancoragem alta: +30-50% aceitação vs sem ancoragem

**Fontes:**
- MIT Study on Pricing Psychology (2003)
- Journal of Consumer Research (2005)
- Priceless: The Myth of Fair Value (William Poundstone, 2010)

---

### Quando NÃO Usar Valores Quebrados

**Exceções (usar valores redondos):**

1. ❌ **Produtos premium de luxo**
   - Ex: Rolex cobra R$ 50.000 (não R$ 49.997)
   - Razão: Preço redondo = exclusividade

2. ❌ **B2B enterprise (>R$ 50k/mês)**
   - Ex: Consultoria estratégica R$ 80.000/mês
   - Razão: Valores altos, quebrado parece "pequeno"

3. ❌ **Doações/Caridade**
   - Ex: Doar R$ 100 (não R$ 97)
   - Razão: Generosidade não combina com "truque"

**Para 99% dos casos (incluindo PMEs, B2B médio), SEMPRE usar valores quebrados.**

---

## Fórmulas e Cálculos

### Valor do Tempo

```python
# Calcular valor do tempo economizado
horas_economizadas_mes = 80  # horas
valor_hora_cliente = 50      # R$/hora
meses_ano = 12

valor_tempo_ano = horas_economizadas_mes * valor_hora_cliente * meses_ano
# Resultado: R$ 48.000/ano
```

### Payback Period

```python
# Tempo para recuperar investimento
investimento = 6000          # R$
retorno_mensal = 2500        # R$/mês

payback_meses = investimento / retorno_mensal
payback_dias = payback_meses * 30
# Resultado: 2.4 meses (72 dias)
```

### ROI Percentage

```python
# Retorno sobre investimento (%)
investimento = 6000          # R$
retorno_total = 30000        # R$

roi_percentual = ((retorno_total - investimento) / investimento) * 100
# Resultado: 400% ROI (5x)
```

### Economia vs CLT

```python
# Comparação com contratação CLT
salario_clt_mes = 3500       # R$
encargos_percentual = 80     # %
custo_real_mes = salario_clt_mes * (1 + encargos_percentual/100)
custo_real_ano = custo_real_mes * 12

investimento_projeto = 6000  # R$

economia_ano1 = custo_real_ano - investimento_projeto
# Resultado: R$ 69.600 (custo CLT) - R$ 6.000 = R$ 63.600 economia
```

---

## Checklist de Qualidade

**Antes de apresentar orçamento, verificar:**

- [ ] Preço baseado em VALOR (não tempo)?
- [ ] ROI mínimo de 3x no cenário conservador?
- [ ] Recursos existentes mapeados e apresentados?
- [ ] 3 cenários de ROI (conservador/realista/otimista)?
- [ ] Ancoragens realistas (não exageradas)?
- [ ] Fontes de dados mencionadas?
- [ ] Timeline realista (não promessa impossível)?
- [ ] Garantias e entregáveis claros?
- [ ] CTA com próximos passos?
- [ ] Apresentação HTML profissional (MotherDuck)?

---

## Referências

- **Alex Hormozi - $100M Offers:** Metodologia de precificação por valor
- **Blair Enns - Pricing Creativity:** Framework de value-based pricing
- **Alan Weiss - Value-Based Fees:** Cálculo de ROI e ancoragem
- **Visual Explainer Skill:** Template MotherDuck para apresentações
- **Hormozi Leads Skill:** Equação de Valor e frameworks persuasivos

---

**Versão:** 1.0
**Última atualização:** 2025-11-04
