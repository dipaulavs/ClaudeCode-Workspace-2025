# 💼 Exemplos de Orçamentos Profissionais

## Índice

1. [Exemplo 1: Automação WhatsApp para Imobiliária](#exemplo-1-automação-whatsapp-para-imobiliária)
2. [Exemplo 2: Sistema de Leads com Meta Ads](#exemplo-2-sistema-de-leads-com-meta-ads)
3. [Exemplo 3: Automação Instagram para Infoproduto](#exemplo-3-automação-instagram-para-infoproduto)

---

## Exemplo 1: Automação WhatsApp para Imobiliária

### Input do Usuário

```
Usuário: "Preciso fazer um orçamento para automatizar WhatsApp de uma imobiliária.
Cliente recebe 200+ mensagens/dia, perde vendas por demora na resposta."
```

### Etapa 1: Coleta de Dados

**Claude pergunta:**
```
Para criar o orçamento ideal, preciso entender:

1. **Projeto:** Automação completa ou chatbot inteligente?
2. **Cliente:** Imobiliária (quantos corretores? quantos imóveis?)
3. **Problema atual:** Perda de quantos leads/mês? Tempo gasto por lead?
4. **Resultado esperado:** Taxa de resposta? Conversão? Economia de tempo?
5. **Processos necessários:** Respostas automáticas? Qualificação? Integração CRM?
```

**Usuário responde:**
```
- Imobiliária com 5 corretores, 100 imóveis ativos
- Perdem ~30 leads/mês por demora (conversão 10% = 3 vendas/mês perdidas)
- Ticket médio: R$ 300k (comissão 5% = R$ 15k por venda)
- Corretores gastam 3h/dia respondendo perguntas repetitivas
- Quer: chatbot + qualificação + agendamento automático
```

### Etapa 2: Mapear Recursos

**Claude analisa:**
```
📦 Recursos Disponíveis:

Reutilizáveis (✅):
  • scripts/whatsapp/send_message.py (envios)
  • scripts/whatsapp/send_media.py (fotos de imóveis)
  • whatsapp-chatbot/ (V4 produção, Claude Haiku)
  • scripts/scheduling/ (agendamento de visitas)

Ajustes (🟡):
  • whatsapp-chatbot/chatbot_v4.py (adaptar para imobiliária)
    - Criar intents específicos (preço, localização, visita)
    - Integrar banco de dados de imóveis
    - Configurar qualificação de leads
  • scripts/scheduling/ (adaptar para agendamento de visitas)

Criar (🔴):
  • Integração CRM do cliente (se tiver)
  • Dashboard de leads qualificados

Esforço Total:
  ✅ 60% pronto (chatbot base + envios + agendamento)
  🟡 30% adaptação (4-6h config + prompts)
  🔴 10% novo (2h integração CRM simples)
```

### Etapa 3: Calcular Preço

**Claude calcula:**
```
💰 Valor Gerado (Ano 1):

1. Vendas Recuperadas:
   - Leads perdidos/mês: 30
   - Taxa conversão: 10%
   - Vendas recuperadas/mês: 3
   - Comissão por venda: R$ 15.000
   - Total/mês: R$ 45.000
   - Total/ano: R$ 540.000

2. Tempo Economizado:
   - Corretores: 5
   - Horas economizadas/dia/corretor: 3h
   - Valor/hora (custo oportunidade): R$ 100
   - Economia/dia: 5 × 3h × R$ 100 = R$ 1.500
   - Economia/mês: R$ 45.000 (22 dias úteis)
   - Economia/ano: R$ 540.000

Valor Total Gerado: R$ 1.080.000/ano

Precificação (5% do valor):
  • R$ 54.000 (ideal, mas pode assustar)

Precificação Ajustada (2% do valor):
  • R$ 21.600 (mais palatável)
  • ROI cliente: 50x (R$ 1.080k ÷ R$ 21.6k)

Faixas:
  • Conservador (1%): R$ 10.800
  • Realista (2%): R$ 21.600 ⭐
  • Premium (3%): R$ 32.400
```

**Recomendação:** R$ 21.600 (ou 3x R$ 7.200)

### Etapa 4: Apresentação HTML

**Claude gera:**
```
📊 Gerando apresentação: orcamento_imobiliaria_chatbot.html

Slides:
1. Capa → "Automação WhatsApp Inteligente"
2. Problema → "30 leads/mês perdidos = R$ 45k/mês perdidos"
3. Solução → "Chatbot + Qualificação + Agendamento"
4. Processos → "Lead chega → Bot responde → Qualifica → Agenda → Corretor fecha"
5. Recursos → "60% pronto (chatbot V4) + 30% adaptação + 10% novo"
6. Timeline → "4 semanas (config + testes + treinamento)"
7. Investimento → "R$ 21.600 (3x R$ 7.200)"
8. ROI → Cenários 30x / 50x / 100x
9. Garantias → "Suporte 60 dias, treinamento incluído"
10. CTA → "Aprovação → Início em 5 dias → Entrega em 4 semanas"
```

### Etapa 5: Ancoragem

**Slide 7 (Investimento):**
```html
<h2>Investimento</h2>
<p class="price">R$ 21.600 (ou 3x R$ 7.200)</p>

<h3>Comparações Realistas:</h3>
<ul>
  <li>❌ Perder 3 vendas/mês = R$ 45.000/mês perdidos</li>
  <li>✅ Investir R$ 21.600 = Recuperar R$ 540.000/ano</li>
  <li>📊 Vs Contratar assistente CLT = R$ 36.000/ano (economia de R$ 14k)</li>
  <li>⏰ Vs Tempo dos corretores = 3.300h/ano economizadas</li>
</ul>

<p><strong>Retorno do investimento:</strong> Em 14 dias 🚀</p>
```

**Slide 8 (ROI):**
```html
<h2>Projeção de Resultados (Ano 1)</h2>

<div class="scenarios">
  <div class="conservative">
    <h3>🟢 Conservador (30x)</h3>
    <p>Premissa: 50% eficiência</p>
    <p>Vendas recuperadas: 18/ano</p>
    <p>Retorno: R$ 270.000 + R$ 270.000 (tempo)</p>
    <p><strong>Total: R$ 540.000</strong></p>
    <p>Investimento: R$ 21.600</p>
    <p><strong>ROI: 25x</strong></p>
  </div>

  <div class="realistic">
    <h3>🟡 Realista (50x) ⭐</h3>
    <p>Premissa: 100% eficiência</p>
    <p>Vendas recuperadas: 36/ano</p>
    <p>Retorno: R$ 540.000 + R$ 540.000 (tempo)</p>
    <p><strong>Total: R$ 1.080.000</strong></p>
    <p>Investimento: R$ 21.600</p>
    <p><strong>ROI: 50x</strong></p>
  </div>

  <div class="optimistic">
    <h3>🔵 Otimista (100x)</h3>
    <p>Premissa: 150% eficiência (melhora processos)</p>
    <p>Vendas recuperadas: 54/ano</p>
    <p>Retorno: R$ 810.000 + R$ 810.000 (tempo)</p>
    <p><strong>Total: R$ 1.620.000</strong></p>
    <p>Investimento: R$ 21.600</p>
    <p><strong>ROI: 75x</strong></p>
  </div>
</div>
```

### Output Final

```
✅ Orçamento Profissional Criado!

📊 Apresentação: orcamento_imobiliaria_chatbot.html
💰 Preço sugerido: R$ 21.600 (3x R$ 7.200)
🎯 ROI cliente: 50x (R$ 1.080.000 ÷ R$ 21.600)

📦 Análise de recursos:
  • 60% reutilizável (chatbot V4 + scripts)
  • 30% adaptação (intents + prompts)
  • 10% desenvolvimento novo (integração)

⏱️ Prazo: 4 semanas
🚀 Payback: 14 dias

Boa sorte na apresentação! 🎬
```

---

## Exemplo 2: Sistema de Leads com Meta Ads

### Input do Usuário

```
Usuário: "Quanto cobrar para criar sistema completo de geração de leads
com Meta Ads para dentista? Campanha + landing page + CRM."
```

### Etapa 1: Coleta de Dados

**Claude pergunta:**
```
Para orçar corretamente:

1. **Escopo:** Criação única ou gestão mensal recorrente?
2. **Cliente:** Dentista (quantas cadeiras? cidade?)
3. **Problema:** Lead caro? Pouco volume? Baixa conversão?
4. **Meta:** Quantos leads/mês? Taxa de conversão esperada? Ticket médio?
5. **Budget Ads:** Quanto cliente investe/mês em anúncios?
```

**Usuário responde:**
```
- Criação inicial do sistema (não gestão mensal)
- Dentista com 3 cadeiras em BH, foco em implantes
- Hoje depende de indicação, quer escalar
- Meta: 30 leads qualificados/mês (taxa conversão 20% = 6 pacientes/mês)
- Ticket médio implante: R$ 8.000 (margem 40% = R$ 3.200/paciente)
- Budget ads: R$ 3.000/mês (R$ 100/lead)
```

### Etapa 2: Mapear Recursos

```
📦 Recursos Disponíveis:

Reutilizáveis (✅):
  • scripts/meta-ads/create_campaign.py
  • scripts/meta-ads/create_ad.py
  • scripts/image-generation/batch_generate.py (criativos)
  • skills/hormozi-leads (copy persuasivo)
  • skills/website-cloner (landing page profissional)

Ajustes (🟡):
  • Adaptar scripts Meta Ads (público-alvo: "implante dentário BH")
  • Configurar pixel + conversões
  • Criar 5-10 variações de anúncios (A/B test)

Criar (🔴):
  • Landing page customizada (HTML/CSS ou Unbounce)
  • Integração CRM simples (Google Sheets ou Notion)
  • Formulário de qualificação (Tally/Typeform)

Esforço Total:
  ✅ 40% pronto
  🟡 40% adaptação (8-10h)
  🔴 20% novo (4-5h)
```

### Etapa 3: Calcular Preço

```
💰 Valor Gerado (Ano 1):

1. Receita Nova:
   - Leads/mês: 30
   - Taxa conversão: 20%
   - Pacientes/mês: 6
   - Ticket médio: R$ 8.000
   - Receita/mês: R$ 48.000
   - Receita/ano: R$ 576.000

2. Lucro Líquido:
   - Margem: 40%
   - Lucro/mês: R$ 19.200
   - Lucro/ano: R$ 230.400

3. Custo de Ads (descontar):
   - R$ 3.000/mês × 12 = R$ 36.000/ano

Lucro Líquido Real: R$ 194.400/ano

Precificação (5% do lucro líquido):
  • R$ 9.720

Precificação Arredondada:
  • R$ 10.000 ⭐
  • ROI cliente: 19.4x (R$ 194k ÷ R$ 10k)

Faixas:
  • Conservador (3%): R$ 6.000
  • Realista (5%): R$ 10.000 ⭐
  • Premium (8%): R$ 15.000
```

### Etapa 4: Apresentação HTML

**Destaques dos slides:**

**Slide 7 (Investimento):**
```
R$ 10.000 (ou 2x R$ 5.000)

Comparações:
• Investimento ads ano 1: R$ 36.000
• Investimento sistema: R$ 10.000
• Total: R$ 46.000

• Retorno esperado: R$ 576.000
• ROI combinado: 12.5x
```

**Slide 8 (ROI):**
```
Cenário Conservador (10x):
- 50% da meta (15 leads/mês, 3 pacientes)
- Receita: R$ 288k/ano
- Custo ads: R$ 36k
- Investimento sistema: R$ 10k
- Lucro: R$ 242k
- ROI: 24x

Cenário Realista (20x):
- 100% da meta (30 leads/mês, 6 pacientes)
- Receita: R$ 576k/ano
- Lucro: R$ 530k
- ROI: 53x

Cenário Otimista (30x):
- 150% da meta (45 leads/mês, 9 pacientes)
- Receita: R$ 864k/ano
- Lucro: R$ 808k
- ROI: 80x
```

### Output Final

```
✅ Orçamento Criado: Sistema de Leads Meta Ads

💰 Preço: R$ 10.000 (2x R$ 5.000)
🎯 ROI: 19.4x no cenário realista
📦 Inclui: Campanhas + Landing Page + CRM + Criativos
⏱️ Prazo: 3 semanas
🚀 Payback: 5 dias (0.2 pacientes)
```

---

## Exemplo 3: Automação Instagram para Infoproduto

### Input do Usuário

```
Usuário: "Orçamento para automatizar Instagram de infoprodutor.
Quer postar 2x/dia (carrosséis educativos) sem esforço manual."
```

### Etapa 1: Coleta de Dados

**Claude pergunta:**
```
1. **Infoproduto:** Qual nicho? Ticket? Faturamento atual?
2. **Problema:** Falta de tempo? Falta de criatividade? Inconsistência?
3. **Meta:** Aumentar seguidores? Aumentar vendas? Autoridade?
4. **Conteúdo:** Ele cria roteiros ou quer 100% automatizado?
5. **Frequência:** 2x/dia = 60 posts/mês. Aceita IA ou quer curadoria?
```

**Usuário responde:**
```
- Infoprodutor de marketing digital (ticket R$ 1.997)
- Fatura R$ 50k/mês (25 vendas/mês)
- Problema: posta manual, leva 2h/dia, inconsistente
- Meta: aumentar de 10k para 30k seguidores em 6 meses (+ vendas)
- Conteúdo: quer 80% automatizado (IA) + 20% revisão dele
- Aceita IA gerando carrosséis desde que fique profissional
```

### Etapa 2: Mapear Recursos

```
📦 Recursos Disponíveis:

Reutilizáveis (✅):
  • scripts/instagram/publish_carousel.py
  • scripts/image-generation/batch_generate.py
  • skills/hormozi-leads (hooks + headlines + copy)
  • skills/carrossel-meta-ads (estrutura 10 slides adaptável)
  • scripts/scheduling/ (agendamento automático)

Ajustes (🟡):
  • Criar workflow: Grok (pesquisa temas) → Claude (roteiro) → batch images (slides) → publish
  • Configurar cron job (2x/dia: 8h e 18h)
  • Criar banco de temas (100+ ideias pré-aprovadas)

Criar (🔴):
  • Script orquestrador (pipeline completo)
  • Sistema de aprovação (Telegram bot para revisar antes de postar)
  • Dashboard Notion (planejamento semanal)

Esforço Total:
  ✅ 50% pronto
  🟡 30% adaptação (6h)
  🔴 20% novo (4h)
```

### Etapa 3: Calcular Preço

```
💰 Valor Gerado (Ano 1):

1. Tempo Economizado:
   - Tempo atual: 2h/dia
   - Dias úteis/ano: 250
   - Total horas: 500h/ano
   - Valor/hora (custo oportunidade): R$ 200 (ele fatura R$ 50k/mês)
   - Valor tempo: R$ 100.000/ano

2. Crescimento de Seguidores → Vendas:
   - Hoje: 10k seguidores, 25 vendas/mês (taxa 0.25%)
   - Meta: 30k seguidores, 75 vendas/mês (mesmo taxa)
   - Aumento vendas: 50 vendas/mês
   - Ticket: R$ 1.997
   - Receita adicional/mês: R$ 99.850
   - Receita adicional/ano: R$ 1.198.200

Valor Total: R$ 1.298.200/ano

Precificação (2% - conservadora porque crescimento depende de variáveis):
  • R$ 25.964

Precificação Arredondada:
  • R$ 25.000 (ou 5x R$ 5.000) ⭐
  • ROI cliente: 51.9x

Faixas:
  • Conservador (1%): R$ 13.000
  • Realista (2%): R$ 25.000 ⭐
  • Premium (3%): R$ 38.000
```

### Etapa 4: Apresentação HTML

**Destaques:**

**Slide 7 (Investimento):**
```
R$ 25.000 (5x R$ 5.000)

Por que vale?
• Economiza 500h/ano = R$ 100.000
• Gera 50 vendas/mês adicionais = R$ 1.198.200/ano
• Total valor: R$ 1.298.200

Comparações:
• Vs Contratar social media: R$ 3.500/mês × 12 = R$ 42.000/ano
• Vs Fazer manual: 500h/ano perdidas (R$ 100k oportunidade)
• Vs Agência: R$ 8.000/mês × 12 = R$ 96.000/ano

Payback: 9 dias (0.5 vendas)
```

**Slide 8 (ROI):**
```
Conservador (20x):
- 50% crescimento (10k → 20k seguidores)
- 25 vendas/mês adicionais
- Receita adicional: R$ 599k/ano
- Tempo economizado: R$ 100k/ano
- Total: R$ 699k
- ROI: 28x

Realista (50x):
- 100% crescimento (10k → 30k)
- 50 vendas/mês adicionais
- Total: R$ 1.298k
- ROI: 52x

Otimista (100x):
- 200% crescimento (10k → 50k)
- 100 vendas/mês adicionais
- Total: R$ 2.596k
- ROI: 104x
```

### Output Final

```
✅ Orçamento: Automação Instagram 100%

💰 Preço: R$ 25.000 (5x R$ 5.000)
🎯 ROI: 52x no cenário realista
📦 Inclui: Pipeline IA + Agendamento + Aprovação Telegram + Dashboard
⏱️ Prazo: 2 semanas
🚀 Payback: 9 dias

🎬 Apresentação: orcamento_instagram_automacao.html
```

---

## Padrões Identificados

**Todos os 3 exemplos seguem:**

1. ✅ **Precificação por valor** (não por hora)
2. ✅ **ROI mínimo 3x** (na verdade 20x+)
3. ✅ **Mapeamento de recursos** (reutilizar 40-60%)
4. ✅ **3 cenários** (conservador/realista/otimista)
5. ✅ **Ancoragens realistas** (vs CLT, vs manual, vs não fazer)
6. ✅ **Payback rápido** (9-14 dias)
7. ✅ **Apresentação profissional** (template MotherDuck)

---

**Próximos passos:** Testar skill com seu caso real!
