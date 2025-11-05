# 100M Leads - Troubleshooting

## Problema 1: Skill Não Encontra Informação

### Sintomas
- Skill retorna "não encontrei informação sobre X"
- Grep não retorna resultados
- Chunk lido não contém conceito esperado

### Causas Comuns
1. **Keyword errada:** Livro usa termo diferente do esperado
2. **Conceito implícito:** Não está explicitamente nomeado no livro
3. **Localização errada:** Conceito está em chunk diferente

### Soluções

**Solução 1: Tentar sinônimos**
```bash
# Em vez de:
Grep pattern="conversão" path=".claude/skills/books/100m-leads/chunks"

# Tentar:
Grep pattern="engaged leads|conversion|sales" path=".claude/skills/books/100m-leads/chunks"
```

**Solução 2: Buscar contexto mais amplo**
```bash
# Em vez de buscar termo específico, buscar categoria:
Grep pattern="cold outreach|cold email|cold call" path=".claude/skills/books/100m-leads/chunks"
```

**Solução 3: Consultar index primeiro**
```bash
# Ver estrutura completa:
Read file_path=".claude/skills/books/100m-leads/index.md"

# Ler chunk inteiro baseado no título:
Read file_path=".claude/skills/books/100m-leads/chunks/section_004_003.md"
```

### Exemplo

**Problema:**
```
Usuário: "Como calcular ROI de afiliados?"
Grep pattern="ROI" → Nenhum resultado (livro não usa "ROI")
```

**Solução:**
```
Grep pattern="LTGP:CAC|gross profit|return" → Encontra section_005_005.md
Lê chunk → Descobre que livro usa "LTGP:CAC ratio" em vez de "ROI"
Responde com fórmula LTGP:CAC
```

---

## Problema 2: Resposta Muito Genérica

### Sintomas
- Skill retorna conceito geral sem detalhes
- Faltam números, benchmarks, exemplos
- Usuário pede "mais específico"

### Causas Comuns
1. **Chunk errado:** Leu introdução em vez do capítulo específico
2. **Parou no overview:** Não aprofundou no conteúdo
3. **Não extraiu números:** Ignorou métricas do chunk

### Soluções

**Solução 1: Ler chunk específico, não introdução**
```bash
# ERRADO (muito genérico):
Read file_path=".claude/skills/books/100m-leads/chunks/section_004_001.md"
# (Introduction: Core Four Methods - só 338 tokens)

# CERTO (específico):
Read file_path=".claude/skills/books/100m-leads/chunks/section_004_006.md"
# (#3 Cold Outreach - 3097 tokens com detalhes)
```

**Solução 2: Extrair TODOS os números e exemplos**
```
Ao ler chunk, capturar:
- Benchmarks (%, ratios, valores)
- Histórias específicas (nomes, datas, resultados)
- Fórmulas (cálculos)
- Action Steps (fim de seções)
```

**Solução 3: Ler Part I E Part II**
```bash
# Alguns tópicos têm 2 partes:
Read file_path=".claude/skills/books/100m-leads/chunks/section_004_003.md"  # Part I
Read file_path=".claude/skills/books/100m-leads/chunks/section_004_004.md"  # Part II
```

### Exemplo

**Problema:**
```
Usuário: "Qual benchmark de cold email?"
Resposta genérica: "Cold email pode gerar leads"
```

**Solução:**
```
Ler section_004_006.md completo
Extrair números específicos:
- 30% open rate
- 10% reply rate
- 3% engagement total
- $240 for 2 shows
- 33% close rate = $360 CAC
- 10:1 return ($3600 profit)

Responder com números concretos + exemplo de cálculo
```

---

## Problema 3: Usuário Quer Aplicação Prática

### Sintomas
- Usuário diz "como aplico no MEU negócio?"
- Pergunta sobre indústria específica não no livro
- Quer adaptar framework para contexto diferente

### Causas Comuns
1. **Skill só cita livro:** Não adapta para contexto do usuário
2. **Falta ponte:** Não conecta teoria do livro com prática do usuário
3. **Exemplo muito diferente:** Livro fala de gyms, usuário tem SaaS

### Soluções

**Solução 1: Estrutura "Exemplo do livro → Exemplo aplicado"**
```
SEMPRE incluir 2 exemplos:

Exemplo do livro: [História específica Alex Hormozi]
Exemplo aplicado [Indústria do usuário]: [Adaptação]

# Template:
Exemplo do livro (Prestige Labs - Supplements para Gyms):
- Gyms vendem supplements para membros
- $200 average order
- 4000 gyms x 14 sales/month = milhões

Exemplo aplicado (SaaS de Agendamento para Clínicas):
- Clínicas vendem agendamento premium para pacientes
- R$50/mês assinatura
- 1000 clínicas x 20 pacientes/month = R$1M/mês
```

**Solução 2: Usar princípios, não cópia exata**
```
Em vez de:
"Alex usou gyms como afiliados para suplementos"

Extrair princípio:
"Encontre businesses que já têm seu público-alvo como clientes"

Aplicar:
"Se você vende [X], encontre quem já vende [Y relacionado] para mesma pessoa"
```

**Solução 3: Perguntar contexto se necessário**
```
Se usuário pergunta genérico:
"Como montar programa de afiliados?"

Skill pode perguntar:
"Para aplicar melhor, me diz: O que você vende e quem é seu cliente ideal?"

Depois adaptar os 6 steps com contexto específico
```

### Exemplo

**Problema:**
```
Usuário: "Como aplicar whisper-tease-shout no meu e-commerce?"
Skill só cita: "Livro diz whisper 4-6 weeks, tease 2-3 weeks, shout 3 days"
```

**Solução:**
```
Extrair PRINCÍPIO (não só timeline):
- Whisper = Curiosity (behind scenes)
- Tease = Value elements (what, who, when)
- Shout = CTA (bonuses, scarcity)

Aplicar ao e-commerce:

Whisper (4 semanas antes Black Friday):
- Posts Instagram mostrando "preparando algo grande"
- Fotos do estoque chegando
- Teaser "nosso maior desconto do ano"

Tease (2 semanas antes):
- Revelar categorias em desconto
- Mostrar preview de produtos
- Anunciar data/hora exata (26/11 00h)

Shout (3 dias antes):
- Countdown diário
- Bônus exclusivos primeiras 100 vendas
- Email 2x/dia
- Hora do lançamento: email every 30min

Resultado: Mesmo framework, contexto diferente
```

---

## Problema 4: Conceito Não Está no Livro

### Sintomas
- Grep retorna vazio para múltiplos sinônimos
- Index não lista tópico
- Conceito moderno (pós-2021, quando livro foi escrito)

### Causas Comuns
1. **Fora do escopo:** Livro é sobre lead generation, não [outro tópico]
2. **Termo moderno:** TikTok Ads, AI, etc podem não estar
3. **Muito específico:** Livro fala princípios, não táticas de plataforma X

### Soluções

**Solução 1: Extrair princípio análogo**
```
Usuário: "Como fazer cold DM no Instagram?"
Livro não tem "Instagram DM" explicitamente

MAS tem "Cold Direct Messages" (section_004_006.md)

Aplicar princípios de Cold Outreach:
1. Build list (Instagram scraping)
2. Personalize + Big Fast Value
3. Follow up multiple times/ways

Responder: "Livro não fala Instagram especificamente, mas princípios de Cold DM aplicam..."
```

**Solução 2: Admitir limitação + indicar recurso**
```
Ser honesto:
"$100M Leads foi escrito em 2021 e não cobre [X específico].

MAS os princípios aplicam:
- [Princípio 1 relevante]
- [Princípio 2 relevante]

Para [X específico], recomendo consultar [outro recurso se houver]"
```

**Solução 3: Combinar múltiplos conceitos**
```
Usuário: "Como fazer live launch no Instagram?"

Livro não tem "Instagram live launch" MAS tem:
- "Launches" (section_005_005.md - Whisper-Tease-Shout)
- "Post Free Content" (section_004_003.md)

Combinar:
"Livro não fala Instagram Live especificamente, mas você pode aplicar:
1. Whisper-Tease-Shout para criar hype
2. Hook-Retain-Reward para estruturar o live
3. [Detalhar como]"
```

### Exemplo

**Problema:**
```
Usuário: "Como usar ChatGPT para gerar leads?"
Grep pattern="ChatGPT|AI|automation" → Nenhum resultado
(Livro é 2021, antes do ChatGPT)
```

**Solução:**
```
Responder honestamente:
"$100M Leads (2021) não menciona ChatGPT ou AI tools.

MAS você pode aplicar os princípios:

1. COLD OUTREACH automatizado:
   - ChatGPT escreve personalization (1-3 facts about lead)
   - Gera variations da mensagem
   - Mantém princípio: Big Fast Value

2. CONTENT CREATION:
   - ChatGPT gera hooks usando 7 componentes de headlines
   - Cria lists/steps/stories
   - Você valida se reward é bom (audience decides)

3. PAID ADS:
   - Gera copy variações
   - Testa What-Who-When framework
   - Métricas humanas (LTGP:CAC)

Livro ensina ESTRATÉGIA, você escolhe FERRAMENTA (ChatGPT é ferramenta)"
```

---

## Checklist de Qualidade

Antes de responder, verificar:

- [ ] **Conceito correto?** Keyword encontrou chunk relevante?
- [ ] **Números incluídos?** Benchmarks, métricas, exemplos quantitativos?
- [ ] **Estrutura visual?** ASCII diagram, lista, tabela?
- [ ] **2 exemplos?** Livro + Aplicado ao contexto usuário?
- [ ] **Action Step?** Se chunk tem, incluir no final?
- [ ] **Fonte citada?** Mencionar qual chunk foi consultado?

Se faltou qualquer item, revisar resposta antes de enviar.

---

## Quando Escalar para Humano

Skill deve admitir limitação quando:

1. **Múltiplas buscas falharam** (tentou 3+ keywords, nenhum resultado)
2. **Conceito muito fora do escopo** (livro é leads, pergunta é vendas/CS/product)
3. **Precisa contexto visual** (usuário pede "analise meu funil" mas não há como ver)
4. **Decisão estratégica** ("qual método usar no meu caso?" - precisa análise profunda)

**Template:**
```
"Não encontrei informação específica sobre [X] no livro $100M Leads.

O que consegui relacionar:
- [Princípio A]
- [Princípio B]

Para decisão estratégica sobre seu caso específico, recomendo:
1. [Sugestão prática]
2. [Alternativa]

Quer que eu aprofunde em algum dos princípios acima?"
```
