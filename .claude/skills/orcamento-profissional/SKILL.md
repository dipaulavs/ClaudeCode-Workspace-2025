# 💼 Orçamento Profissional - Propostas com Valor e Apresentação

## Quando Usar

Automaticamente quando usuário:
- "Preciso fazer um orçamento para cliente"
- "Quanto cobrar por [projeto]?"
- "Cria proposta/apresentação para [serviço]"
- "Precificar projeto de [automação/sistema/etc]"

**Objetivo:** Gerar orçamentos baseados em VALOR (não tempo), com análise de recursos e apresentação profissional.

---

## Workflow Automático (5 Etapas)

### Etapa 1: Coletar Dados do Projeto 📋

Perguntar ao usuário:
1. **Projeto/Serviço:** O que será entregue?
2. **Cliente:** Segmento/nicho (contexto)
3. **Problema atual:** O que cliente sofre hoje?
4. **Resultado esperado:** Qual transformação/ganho?
5. **Processos necessários:** Quais etapas técnicas?

### Etapa 2: Mapear Recursos Disponíveis 🔍

Análise automática:
1. **Buscar scripts reutilizáveis** → `scripts/` (67+ templates)
2. **Buscar skills aplicáveis** → `.claude/skills/` (19 skills)
3. **Identificar ferramentas** → `tools/` (40+ ferramentas)
4. **Calcular esforço:**
   - ✅ Verde: 100% reutilizável (configuração apenas)
   - 🟡 Amarelo: 50-80% reutilizável (ajustes necessários)
   - 🔴 Vermelho: <50% reutilizável (desenvolvimento novo)

Apresentar ao usuário:
```
📦 Recursos Mapeados:

Reutilizáveis (✅):
  • scripts/whatsapp/send_message.py
  • skills/hormozi-leads

Ajustes (🟡):
  • scripts/meta-ads/create_campaign.py (adaptar para produto)

Criar (🔴):
  • Integração customizada API X
```

### Etapa 3: Calcular Preço Baseado em Valor 💰

Usar metodologia de precificação por resultado (ver [REFERENCE.md](REFERENCE.md)):

**Fórmula Master:**
```
Preço Justo = 2-10% do Valor Gerado no Primeiro Ano
```

**Perguntas estratégicas:**
1. Quanto cliente GANHA com isso? (receita, economia, tempo)
2. Quanto cliente PERDE sem isso? (oportunidade, risco)
3. Qual ROI esperado? (conservador: 3x, realista: 5x, otimista: 10x)

**SEMPRE aplicar Valores Quebrados + Ancoragem:**

**Técnica de Preços Psicológicos:**
1. **Calcular preço base** (ex: R$ 6.000)
2. **Criar ancoragem alta** → Tabela +30-40% (ex: R$ 8.391)
3. **Aplicar descontos nomeados** → Parceria + Combo
4. **Valor final quebrado** → Terminar em 7 ou 9 (ex: R$ 5.997)

**Output para usuário:**
```
💰 Precificação Sugerida (com Ancoragem):

TABELA EMPRESAS PADRÃO: R$ 8.391
├─ Desconto parceria: -R$ 1.200
├─ Desconto combo: -R$ 1.194
└─ INVESTIMENTO CLIENTE: R$ 5.997/mês ⭐

Economia: 28% (R$ 2.394)
ROI Cliente: 20x

Valores quebrados aplicados:
• Tabela:  R$ 8.391 (ancoragem alta)
• Final:   R$ 5.997 (parece "R$ 5 mil")
• Setup:   R$ 1.497 (consistência)
```

### Etapa 4: Gerar Apresentação HTML 📊

Usar template interativo padrão: `templates/proposta-orcamento/template_proposta_interativa.html`

**Estrutura padrão (9 slides com animações progressivas):**
1. **Capa** → Título + cliente
2. **Situação Atual** → 4 problemas (revelam progressivamente)
3. **Solução Proposta** → 6 serviços (revelam progressivamente)
4. **Como Funciona** → Fluxo + Diferenciais
5. **Timeline** → Prazo realista (10 dias úteis padrão)
6. **Investimento Detalhado** → Tabela progressiva (10 steps!)
7. **Comparação Mercado** → Economia vs concorrentes
8. **O Que Está Incluso** → Detalhamento
9. **Próximos Passos** → CTA

**Features do template:**
- ✅ Animações progressivas (itens aparecem ao clicar)
- ✅ Design MotherDuck (beige + yellow + dark gray)
- ✅ Navegação teclado (→, F fullscreen)
- ✅ Indicador de progresso "(3/6)"
- ✅ Hints dinâmicos ("Clique para revelar")
- ✅ Slide Investimento em 10 steps (quadrado amarelo por último!)
- ✅ 100% responsivo e standalone

**Documentação completa:** `templates/proposta-orcamento/README.md`

### Etapa 5: Ancoragem Realista 🎯

Aplicar frameworks `hormozi-leads` (Equação de Valor):

**Slide "Investimento" deve incluir:**
```
💰 Investimento: R$ 6.000

Comparações Realistas:
├─ Vs Contratar CLT (R$ 3.500/mês): Economia de R$ 36.000/ano
├─ Vs Fazer manual (80h/mês): Libera 960h/ano = R$ 48.000
└─ Vs Perder oportunidade: Deixa de ganhar R$ 80.000/ano

Retorno: Paga em 27 dias 📈
```

**Slide "ROI Matemático":**
```
Cenários de Resultado (ano 1):

🟢 Conservador (3x):
   Investimento: R$ 6.000
   Retorno: R$ 18.000
   Lucro: R$ 12.000

🟡 Realista (5x):
   Investimento: R$ 6.000
   Retorno: R$ 30.000
   Lucro: R$ 24.000

🔵 Otimista (10x):
   Investimento: R$ 6.000
   Retorno: R$ 60.000
   Lucro: R$ 54.000
```

**NUNCA exagerar:** Usar dados reais, pesquisas, benchmarks do mercado.

---

## Output Final para Usuário

```
✅ Orçamento Profissional Criado!

📊 Apresentação: orcamento_[cliente]_[projeto].html
💰 Preço sugerido: R$ 6.000 (ROI 20x)
🎯 Ancoragem: Vs CLT, Vs Manual, Vs Oportunidade

🎬 Próximos passos:
  1. Abrir HTML no navegador (F = fullscreen)
  2. Revisar slides (setas ← →)
  3. Agendar videochamada com cliente
  4. Apresentar com confiança!

Boa sorte! 🚀
```

---

## Regras de Ouro

### ✅ SEMPRE:
- Precificar por VALOR (não por tempo/hora)
- Mapear recursos existentes ANTES de estimar
- Calcular ROI realista (não exagerar)
- Usar template MotherDuck (visual-explainer)
- Criar ancoragens matemáticas (comparações)
- Mostrar 3 cenários (conservador/realista/otimista)

### ❌ NUNCA:
- Cobrar por hora (mentalidade CLT)
- Ignorar scripts/skills disponíveis
- Exagerar ROI (manter realismo)
- Criar apresentação feia/genérica
- Esquecer slide de garantias
- Deixar preço sem contexto (sempre ancorar)

---

## Documentação Adicional

- **Metodologia completa de precificação:** Ver [REFERENCE.md](REFERENCE.md)
- **Exemplos de orçamentos reais:** Ver [EXAMPLES.md](EXAMPLES.md)
- **Problemas comuns:** Ver [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Skill Type:** Model-invoked (ativação automática)
**Output:** HTML standalone + resumo precificação
**Versão:** 1.0
