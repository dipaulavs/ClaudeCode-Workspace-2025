# 🔧 Troubleshooting - Orçamento Profissional

## Problemas Comuns e Soluções

### Problema 1: "Cliente achou caro demais"

**Sintomas:**
- Cliente rejeita proposta dizendo "está muito caro"
- Compara com freelancers baratos
- Não entende o valor

**Causas:**
1. ❌ Ancoragem mal feita (faltou comparações realistas)
2. ❌ ROI não ficou claro na apresentação
3. ❌ Cliente não entendeu o resultado/transformação
4. ❌ Preço apresentado sem contexto

**Soluções:**

**1. Reforçar Ancoragem:**
```
Antes (ruim):
"O projeto custa R$ 10.000"

Depois (bom):
"O projeto custa R$ 10.000, que é:
• 23% do custo de contratar CLT (R$ 42.000/ano)
• O equivalente a 0.5 vendas (você terá 50+ vendas/ano com isso)
• O investimento se paga em 9 dias"
```

**2. Quebrar Preço em Componentes:**
```html
<h2>Detalhamento do Investimento</h2>
<ul>
  <li>Setup inicial: R$ 3.000</li>
  <li>Desenvolvimento: R$ 5.000</li>
  <li>Treinamento: R$ 1.000</li>
  <li>Suporte 60 dias: R$ 1.000</li>
  <li><strong>Total: R$ 10.000</strong></li>
</ul>
```

**3. Oferecer Parcelamento:**
```
R$ 10.000 → 3x R$ 3.333 (sem juros)
ou
R$ 10.000 → 5x R$ 2.000 (sem juros)

"Menos que o custo de 1 freelancer/mês (R$ 3.500)"
```

**4. Criar Comparação Direta:**
```
Opção A (não fazer):
• Continuar perdendo R$ 45k/mês
• Total perdido em 12 meses: R$ 540k

Opção B (investir R$ 10k):
• Recuperar R$ 45k/mês
• Retorno em 12 meses: R$ 540k
• ROI: 54x

Qual faz mais sentido? 🤔
```

---

### Problema 2: "Cliente não tem dados concretos"

**Sintomas:**
- Cliente não sabe faturamento exato
- Não sabe quantos leads perde
- Não sabe valor/hora do tempo dele

**Causas:**
1. ❌ Negócio desorganizado (normal em PMEs)
2. ❌ Perguntas muito técnicas
3. ❌ Não sabe estimar custo de oportunidade

**Soluções:**

**1. Usar Benchmarks do Setor:**
```python
# Se cliente é dentista implante e não sabe ticket médio
ticket_medio_mercado = 8000  # R$ (pesquisa Google)
margem_setor = 0.40          # 40% (padrão odontologia)

# Calcular conservadoramente
lucro_por_paciente = ticket_medio_mercado * margem_setor
# R$ 3.200 por paciente
```

**Fontes de benchmarks:**
- SEBRAE (relatórios setoriais)
- Google Trends + pesquisa "preço médio [serviço]"
- Concorrentes (análise de mercado)
- Associações de classe

**2. Simplificar Perguntas:**
```
Antes (técnico):
"Qual seu CAC e LTGP:CAC ratio atual?"

Depois (simples):
"Quantos clientes novos você tem por mês?"
"Quanto cada cliente gasta, em média?"
"Quantos clientes você perde por não atender rápido?"
```

**3. Usar Estimativas Conservadoras:**
```
Se cliente não sabe quantos leads perde:

Estimativa conservadora:
• Recebe 200 mensagens/dia
• 50% são leads reais (100/dia)
• 10% não são respondidos rápido (10/dia)
• Taxa conversão: 10%
• Leads perdidos/dia: 1 lead

Total/mês: ~30 leads perdidos
```

**4. Criar Cenário "Pior Caso":**
```
Não sabemos os números exatos, então vamos calcular
o PIOR cenário possível:

• Se você ganhar apenas 10% do projetado
• Se você economizar apenas 1h/dia (não 3h)
• Se converter apenas 5% (não 10%)

Mesmo assim:
• Retorno: R$ 54.000/ano
• Investimento: R$ 10.000
• ROI: 5.4x

Ou seja, mesmo no PIOR caso, você ganha 5x o investimento.
```

---

### Problema 3: "Skill não encontrou recursos suficientes"

**Sintomas:**
- Análise retorna 80%+ "criar do zero" (🔴)
- Poucos scripts/skills reutilizáveis
- Esforço muito alto

**Causas:**
1. ❌ Projeto fora do escopo usual (ex: hardware, IoT)
2. ❌ API/integração proprietária do cliente
3. ❌ Tecnologia não suportada no workspace

**Soluções:**

**1. Reavaliar Escopo:**
```
Se projeto é 80% desenvolvimento novo:

Opção A (boa): Recomendar solução existente no mercado
"Para isso, recomendo usar [Zapier/Make/n8n] que já tem
integração pronta. Economiza R$ 20k de desenvolvimento."

Opção B (realista): Cobrar por desenvolvimento customizado
"Como 80% é desenvolvimento novo, o preço será baseado
em horas (não valor), estimado em R$ 30k."
```

**2. Buscar APIs de Terceiros:**
```
Em vez de criar integração do zero:

Antes:
• Integrar API proprietária Cliente (20h dev)

Depois:
• Usar Zapier/Make como middleware (2h config)
• Cliente paga R$ 30/mês (Zapier)
• Você economiza 18h de desenvolvimento
```

**3. Modularizar Projeto:**
```
Quebrar projeto em fases:

Fase 1 (Reutilizável 80%): R$ 6.000
• Automação WhatsApp básica
• Usando chatbot V4 existente

Fase 2 (Reutilizável 40%): R$ 12.000
• Integração CRM proprietário
• Desenvolvimento customizado

Total: R$ 18.000
Cliente pode aprovar Fase 1 primeiro.
```

---

### Problema 4: "ROI ficou muito alto, parece irreal"

**Sintomas:**
- ROI de 50x, 100x, 200x
- Cliente desconfia que é exagero
- Números parecem "bons demais"

**Causas:**
1. ❌ Valor gerado muito grande (ex: recuperar R$ 500k/ano)
2. ❌ Preço muito baixo (ex: cobrando só R$ 5k)
3. ✅ ROI realmente é alto (você está cobrando pouco!)

**Soluções:**

**1. Aumentar Preço (Sério!):**
```
Se ROI é 100x, você está cobrando 1% do valor.
Isso é MUITO baixo.

Antes: R$ 5.000 (ROI 100x) ← Parece irreal
Depois: R$ 25.000 (ROI 20x) ← Mais crível

Cliente vai respeitar mais um ROI de 20x do que 100x.
```

**2. Mostrar Fontes de Dados:**
```html
<h3>Premissas (Dados Reais)</h3>
<ul>
  <li>Ticket médio: R$ 8.000 (fonte: cliente informou)</li>
  <li>Taxa conversão: 10% (fonte: benchmark SEBRAE odontologia)</li>
  <li>Leads perdidos: 30/mês (fonte: estimativa conservadora cliente)</li>
  <li>Margem: 40% (fonte: padrão setor odontológico)</li>
</ul>

<p>Todas premissas são conservadoras e baseadas em dados reais.</p>
```

**3. Usar Cenário Conservador como Padrão:**
```
Não apresentar ROI otimista (100x) como principal.

Destacar cenário CONSERVADOR:
"Mesmo se você atingir apenas 30% do resultado esperado,
o ROI será de 15x. Difícil não dar certo."
```

**4. Quebrar em Pequenas Vitórias:**
```
Em vez de:
"Você vai ganhar R$ 500k no ano"

Use:
"Nos primeiros 30 dias, você deve recuperar 3 vendas (R$ 24k).
Isso já paga o investimento 2x. O resto do ano é lucro."
```

---

### Problema 5: "Cliente quer pagar por hora, não por valor"

**Sintomas:**
- Cliente insiste em "quanto você cobra por hora?"
- Quer contrato CLT ou PJ mensal
- Não entende precificação por valor

**Causas:**
1. ❌ Cliente habituado a contratar freelancers/CLTs
2. ❌ Não entende diferença entre commodity e solução estratégica
3. ❌ Quer "controle" sobre suas horas

**Soluções:**

**1. Educar sobre Diferença:**
```
"Entendo que você está acostumado a pagar por hora.
Mas veja a diferença:

Freelancer por hora (R$ 100/h):
• Quanto mais rápido faz, menos ganha
• Incentivo: demorar mais
• Risco todo seu (e se não funcionar?)

Solução por valor (R$ 10.000 fixo):
• Quanto mais rápido entrego, melhor para mim
• Incentivo: máxima eficiência
• Risco compartilhado (garanto resultado)

O que faz mais sentido para você?"
```

**2. Converter Valor em "Hora Equivalente":**
```
Se cliente insiste:

"Ok, se você quer pensar em horas:
• Projeto: R$ 10.000
• Estimativa: 50 horas
• 'Taxa equivalente': R$ 200/h

Mas você NÃO paga por hora. Você paga resultado fixo.
Se eu terminar em 30h (porque reutilizo 60% de código pronto),
você NÃO paga menos. E se demorar 70h, você NÃO paga mais.

Preço fixo: R$ 10.000, independente de horas."
```

**3. Oferecer Retainer (Mensal) se Fizer Sentido:**
```
Se cliente quer relacionamento longo:

Opção A (Projeto único): R$ 10.000
• Entrega em 4 semanas
• Suporte 60 dias

Opção B (Retainer): R$ 3.000/mês (mínimo 6 meses)
• Inclui: automação + melhorias contínuas + suporte
• Total 6 meses: R$ 18.000
• Mais caro, mas cliente tem suporte contínuo
```

---

### Problema 6: "Apresentação HTML não abre ou quebra"

**Sintomas:**
- Arquivo HTML não abre no navegador
- Slides desformatados
- Responsividade quebrada

**Causas:**
1. ❌ Template MotherDuck corrompido
2. ❌ CSS inline com erro de sintaxe
3. ❌ Conteúdo com caracteres especiais (', ")

**Soluções:**

**1. Validar HTML antes de entregar:**
```bash
# Abrir HTML no navegador via terminal
open orcamento_cliente.html

# Se não abrir, checar erros de sintaxe
# Buscar por: aspas não fechadas, tags não fechadas
```

**2. Usar Template Base (Fallback):**
```
Se template MotherDuck falhar:

Usar template simples (notion-style.html):
• Mais robusto
• Menos dependências
• Sempre funciona
```

**3. Escapar Caracteres Especiais:**
```python
# Ao injetar conteúdo no HTML
import html

texto_usuario = "Cliente disse: 'isso é ótimo'"
texto_seguro = html.escape(texto_usuario)
# Resultado: Cliente disse: &#x27;isso é ótimo&#x27;
```

**4. Testar Responsividade:**
```
Antes de entregar, testar em:
• Desktop (Chrome, Safari, Firefox)
• Mobile (iPhone, Android)
• Tablet (iPad)

Redimensionar janela do navegador para checar breakpoints.
```

---

## Checklist de Prevenção

**Antes de entregar orçamento, verificar:**

- [ ] ROI entre 3x e 30x (nem baixo nem alto demais)
- [ ] 3 cenários apresentados (conservador/realista/otimista)
- [ ] Ancoragens realistas (vs CLT, vs manual, vs não fazer)
- [ ] Fontes de dados mencionadas (não "inventei")
- [ ] Preço baseado em VALOR (não tempo)
- [ ] HTML abre corretamente (testar antes)
- [ ] Slides responsivos (testar mobile)
- [ ] Timeline realista (não promessa impossível)
- [ ] Garantias claras (o que está incluso)
- [ ] CTA com próximos passos

---

## Quando NÃO Usar Esta Skill

**Evitar usar se:**

1. ❌ Projeto é 100% commodity (usar preço de mercado)
2. ❌ Cliente quer freela por hora (educar primeiro ou recusar)
3. ❌ Escopo é vago demais (pedir mais detalhes antes)
4. ❌ Cliente não tem budget mínimo (qualificar antes)
5. ❌ Projeto fora do escopo técnico (80%+ desenvolvimento novo)

---

## Recursos Adicionais

- **Voltar ao workflow:** Ver [SKILL.md](SKILL.md)
- **Metodologia completa:** Ver [REFERENCE.md](REFERENCE.md)
- **Exemplos práticos:** Ver [EXAMPLES.md](EXAMPLES.md)

---

**Versão:** 1.0
**Última atualização:** 2025-11-04
