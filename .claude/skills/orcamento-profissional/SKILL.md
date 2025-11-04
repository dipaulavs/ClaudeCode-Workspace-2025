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

**Output para usuário:**
```
💰 Precificação Sugerida:

Valor Gerado (ano 1): R$ 120.000
├─ Receita nova: R$ 80.000
├─ Economia tempo: R$ 30.000
└─ Redução custos: R$ 10.000

Preço Justo (5%): R$ 6.000
ROI Cliente: 20x (R$ 120k ÷ R$ 6k)

Faixas:
• Conservador (2%): R$ 2.400
• Realista (5%): R$ 6.000
• Premium (10%): R$ 12.000
```

### Etapa 4: Gerar Apresentação HTML 📊

Invocar `visual-explainer` com template MotherDuck:

**Estrutura obrigatória (8-10 slides):**
1. **Capa** → Título + cliente
2. **Problema** → Situação atual (dor)
3. **Solução** → Transformação proposta
4. **Processos** → O que será feito (etapas técnicas)
5. **Recursos** → O que você já tem (reutilização)
6. **Timeline** → Prazo realista
7. **Investimento** → Preço + ancoragem
8. **ROI Matemático** → Cenários conservador/realista/otimista
9. **Garantias** → O que está incluso
10. **CTA** → Próximos passos

**Features:**
- Dark mode (MotherDuck: beige + yellow)
- Navegação teclado (setas, F fullscreen)
- Barra de progresso
- Standalone HTML (funciona offline)

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
