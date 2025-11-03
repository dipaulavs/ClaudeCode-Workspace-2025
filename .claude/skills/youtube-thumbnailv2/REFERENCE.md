# YouTube Thumbnail - Anatomia Detalhada

Documentação técnica completa do template de thumbnails.

---

## 🎨 Estrutura Visual

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  [TEXTO LADO ESQUERDO]    [FOTO LADO DIREITO]  │
│                                                 │
│  ┌──────────────────┐     ┌──────────────────┐ │
│  │ TÍTULO DOURADO   │     │  CLOSE-UP        │ │
│  │ ════════════     │     │  PEITO PRA CIMA  │ │
│  │ Subtítulo        │     │  SPLIT LIGHTING  │ │
│  │ Data/Hora        │     │  REFLEXO LARANJA │ │
│  │ [Selo]           │     │  (óculos)        │ │
│  └──────────────────┘     └──────────────────┘ │
│                                                 │
│  FUNDO: PRETO ESCURO                            │
│  PALETA: Preto, Dourado, Azul-Ciano             │
└─────────────────────────────────────────────────┘
```

---

## 📋 Seções do Template (em ordem)

### 1. Introdução (Linha 1)

```
Crie uma thumbnail de tecnologia para um vídeo sobre {{TEMA}}.
```

**Propósito:** Define contexto e assunto geral

**Variável:**
- `{{TEMA}}` → Assunto do vídeo (1-3 palavras)

**Exemplos:**
- "IA"
- "produtividade"
- "empreendedorismo"
- "marketing digital"
- "automação"

**Impacto:** BAIXO (IA usa para contexto geral)

---

### 2. Texto e Gráficos (Linhas 2-5)

```
Texto e Gráficos (no lado esquerdo da imagem):
  Título: Escreva "{{TÍTULO}}" em letras maiúsculas, com uma fonte moderna e contornada em dourado.
  Subtítulo: Abaixo do título, insira uma barra dourada sólida com o texto "{{SUBTÍTULO}}" em letras maiúsculas.
  Data: Abaixo da barra, adicione "{{DATA}}" em uma fonte branca e limpa.
  Selo: No canto inferior esquerdo, adicione um pequeno texto "{{SELO}}".
```

**Propósito:** Define todo o conteúdo textual da thumbnail

#### 2.1 Título (Linha 2) - **CLICKBAIT CURTO OBRIGATÓRIO**

**Variável:** `{{TÍTULO}}`
**Características:**
- ✅ **Máximo ABSOLUTO: 20 caracteres** (conta espaços!)
- ✅ Letras MAIÚSCULAS OBRIGATÓRIO
- ✅ Estilo CLICKBAIT (curiosidade/urgência/resultado)
- ✅ Fonte moderna + contorno dourado
- ✅ Posição: Topo do lado esquerdo
- ✅ Tamanho: Grande (destaque principal)

**Diretrizes RÍGIDAS:**
- ⚠️ **Contar caracteres SEMPRE** antes de usar
- ⚠️ Se headline original > 20 chars → EXTRAIR ESSÊNCIA
- Usar números quando possível ("10X", "48%", "7 DIAS")
- Evitar artigos (o, a, de, para)
- Aplicar frameworks clickbait (ver seção abaixo)

**✅ Exemplos CLICKBAIT CURTOS:**
| Texto | Chars | Framework |
|-------|-------|-----------|
| "SUPERA GPT-5" | 12 | Comparação |
| "48% MAIS RÁPIDO" | 15 | Resultado |
| "MUDOU TUDO" | 10 | Transformação |
| "NINGUÉM TE CONTA" | 16 | Segredo |
| "10X MAIS RÁPIDO" | 15 | Número |
| "PARE DE USAR X" | 14 | Negação |
| "EM 90 SEGUNDOS" | 13 | Tempo |
| "ISSO FUNCIONA" | 13 | Validação |

**❌ Exemplos ERRADOS:**
- ❌ "Como usar inteligência artificial" (39 chars - MUITO LONGO)
- ❌ "Deep Agent Desktop supera GPT-5" (32 chars - MUITO LONGO)
- ❌ "dicas de produtividade" (22 chars + minúsculas)
- ❌ "IA" (2 chars - muito curto, sem impacto)

#### 2.2 Subtítulo (Linha 3) - **GANCHO IMPACTO OBRIGATÓRIO**

**Variável:** `{{SUBTÍTULO}}`
**Características:**
- ✅ **Máximo ABSOLUTO: 25 caracteres** (conta espaços!)
- ✅ Dentro de barra dourada sólida
- ✅ Letras MAIÚSCULAS OBRIGATÓRIO
- ✅ Estilo CLICKBAIT (complementa título)
- ✅ Posição: Abaixo do título
- ✅ Tamanho: Médio

**Diretrizes RÍGIDAS:**
- ⚠️ **Contar caracteres SEMPRE** antes de usar
- Foco em benefício/resultado/transformação
- Criar urgência, curiosidade ou promessa
- Complementar o título (não repetir)
- Usar gatilhos emocionais

**✅ Exemplos GANCHO CURTO:**
| Texto | Chars | Gatilho |
|-------|-------|---------|
| "Testei Por 30 Dias" | 18 | Prova/Tempo |
| "Resultado Chocante" | 18 | Curiosidade |
| "Ninguém Te Conta" | 16 | Segredo |
| "DO ZERO AO MILHÃO" | 17 | Transformação |
| "EM 90 SEGUNDOS" | 13 | Velocidade |
| "FUNCIONA SEMPRE" | 15 | Garantia |
| "SEM GASTAR NADA" | 15 | Benefício |
| "MÉTODO COMPROVADO" | 17 | Validação |

**❌ Exemplos ERRADOS:**
- ❌ "Veja como fazer isso funcionar para você" (43 chars - MUITO LONGO)
- ❌ "Aprenda as melhores técnicas" (29 chars - MUITO LONGO)
- ❌ "aprenda" (minúsculas + genérico)
- ❌ "Clique aqui" (call to action genérico)

#### 2.3 Data (Linha 4)

**Variável:** `{{DATA}}`
**Características:**
- Fonte branca e limpa
- Posição: Abaixo da barra dourada
- Tamanho: Pequeno

**Diretrizes:**
- Formato brasileiro: DD/MM
- Incluir dia da semana (opcional)
- Incluir horário (opcional)
- Pode ser só ano para conteúdo atemporal

**Formatos aceitos:**
- ✅ "05/11, quarta"
- ✅ "10/11, segunda | 20h"
- ✅ "2025"
- ✅ "12/11, terça | 18h"
- ✅ "" (vazio, se não aplicável)

#### 2.4 Selo (Linha 5)

**Variável:** `{{SELO}}`
**Características:**
- Texto pequeno
- Posição: Canto inferior esquerdo
- Badge/etiqueta de destaque

**Diretrizes:**
- 1-2 palavras máximo
- Criar senso de exclusividade/urgência

**Opções recomendadas:**

| Selo | Quando Usar |
|------|-------------|
| **Novo** | Lançamentos, conteúdo recente |
| **Ao Vivo** | Lives, transmissões, webinars |
| **Exclusivo** | Conteúdo premium, membros |
| **Imperdível** | Eventos importantes, datas especiais |
| **Premium** | Conteúdo pago, cursos |
| **Grátis** | Oferta gratuita, freebies |
| **Urgente** | Prazo limitado, promoções |
| **Bônus** | Conteúdo adicional, extras |

---

### 3. Foto Principal (Linhas 6-7)

```
Foto Principal: Use a minha foto em um close-up, do peito para cima. O meu rosto deve ocupar a metade direita da imagem, com um olhar sério e direto para a câmera.
```

**Propósito:** Define posicionamento e enquadramento da foto

**🔒 FIXO - NUNCA MODIFICAR:**
- ✅ Close-up (peito para cima)
- ✅ Lado direito da imagem
- ✅ Olhar sério e direto
- ✅ Ocupa metade direita

**Características técnicas:**
- Foto base: URL Nextcloud
- Resolução original mantida
- IA aplica edições sobre a foto

---

### 4. Iluminação (Linhas 8-9)

```
Iluminação: Aplique uma iluminação de estúdio dramática com o estilo 'split lighting'. Metade do meu rosto deve estar em sombra profunda, enquanto a outra metade é iluminada por uma luz azul-ciano fria. Se eu estiver usando óculos, adicione um reflexo laranja vibrante nas lentes.
```

**Propósito:** Define mood e estética profissional

**🔒 FIXO - NUNCA MODIFICAR:**
- ✅ Split lighting (metade sombra, metade luz)
- ✅ Sombra profunda
- ✅ Luz azul-ciano fria
- ✅ Reflexo laranja nos óculos

**Características técnicas:**
- Contraste alto
- Dramaticidade
- Assinatura visual reconhecível

---

### 5. Fundo (Linha 10)

```
Fundo: O fundo deve ser preto e escuro.
```

**Propósito:** Maximizar contraste e foco

**🔒 FIXO - NUNCA MODIFICAR:**
- ✅ Preto e escuro
- ✅ Sem distrações

---

### 6. Estilo Geral (Linha 11)

```
Estilo Geral: A imagem deve ter um clima profissional, tecnológico e de alto impacto, com uma paleta de cores focada em preto, dourado e o contraste do azul-ciano.
```

**Propósito:** Define identidade visual consistente

**🔒 FIXO - NUNCA MODIFICAR:**
- ✅ Clima profissional
- ✅ Tecnológico
- ✅ Alto impacto
- ✅ Paleta: preto, dourado, azul-ciano

---

## 🎯 Hierarquia de Impacto Visual

**Ordem de atenção do espectador:**

1. **TÍTULO** (80% impacto) → Primeira coisa que chama atenção
2. **FOTO** (70% impacto) → Conexão humana
3. **SUBTÍTULO** (60% impacto) → Reforça promessa
4. **DATA** (20% impacto) → Contexto temporal
5. **SELO** (30% impacto) → Urgência/exclusividade

---

## 🧪 Variações Recomendadas

### Para Gerar 5 Thumbnails Diferentes:

**Estratégia:** Variar ângulos/promessas mantendo tema central

**Exemplo: Vídeo sobre "Produtividade"**

| # | Título | Subtítulo | Ângulo |
|---|--------|-----------|--------|
| 1 | PRODUTIVIDADE 10X | MÉTODO COMPROVADO | Resultado quantificado |
| 2 | TRABALHE MENOS | GANHE MAIS TEMPO | Benefício direto |
| 3 | ROTINA PERFEITA | PRODUTIVO DE VERDADE | Transformação |
| 4 | FOCO TOTAL | ELIMINE DISTRAÇÕES | Problema → Solução |
| 5 | SISTEMA SIMPLES | 3 PASSOS APENAS | Facilidade |

---

## 🎨 Teoria das Cores

### Paleta Fixa (NÃO modificar)

| Cor | Uso | Psicologia |
|-----|-----|------------|
| **Preto** | Fundo, base | Elegância, profissionalismo |
| **Dourado** | Texto principal, barra | Luxo, valor, exclusividade |
| **Azul-Ciano** | Iluminação | Tecnologia, modernidade, confiança |
| **Laranja** | Reflexo óculos | Energia, contraste quente |
| **Branco** | Data | Clareza, legibilidade |

**Contraste:** Alto contraste garante legibilidade mesmo em miniaturas pequenas (thumbnails no feed do YouTube).

---

## 📐 Proporções e Resolução

- **Proporção:** 16:9 (padrão YouTube)
- **Resolução gerada:** 1024x576px
- **Tamanho de arquivo:** ~300-500KB PNG
- **Qualidade:** Alta (Nano Banana Edit)

**Nota:** YouTube aceita até 2MB e recomenda 1280x720px, mas 1024x576px é suficiente e processa mais rápido.

---

## 🔥 Frameworks de CLICKBAIT para Thumbnails

### 6 Frameworks Comprovados (≤20 caracteres)

#### 1. RESULTADO CHOCANTE (Números)
**Fórmula:** `[NÚMERO] + [MÉTRICA] + [COMPARAÇÃO]`
**Exemplos:**
- "48% NO SWEBENCH"
- "10X MAIS RÁPIDO"
- "R$50K EM 7 DIAS"
- "3X MELHOR"

#### 2. COMPARAÇÃO DIRETA (VS)
**Fórmula:** `[SUPERA/MELHOR] + [REFERÊNCIA]`
**Exemplos:**
- "SUPERA GPT-5"
- "MELHOR QUE CLAUDE"
- "VENCE CHATGPT"
- "DESTROI CURSOR"

#### 3. EXCLUSIVIDADE/SEGREDO
**Fórmula:** `[NINGUÉM/SÓ] + [VERBO] + [BENEFÍCIO]`
**Exemplos:**
- "NINGUÉM TE CONTA"
- "SEGREDO REVELADO"
- "SÓ AQUI VOCÊ VÊ"
- "JAMAIS DIVULGADO"

#### 4. TEMPO/URGÊNCIA
**Fórmula:** `[EM] + [TEMPO CURTO]`
**Exemplos:**
- "EM 90 SEGUNDOS"
- "TESTEI 30 DIAS"
- "7 DIAS APENAS"
- "ÚLTIMA CHANCE"

#### 5. TRANSFORMAÇÃO
**Fórmula:** `[MUDOU/VIROU] + [TUDO/JOGO]`
**Exemplos:**
- "MUDOU TUDO"
- "VIROU O JOGO"
- "ANTES E DEPOIS"
- "TRANSFORMAÇÃO"

#### 6. NEGAÇÃO/CONTRÁRIO
**Fórmula:** `[PARE/NÃO] + [AÇÃO COMUM]`
**Exemplos:**
- "PARE DE USAR X"
- "NÃO FAÇA ISSO"
- "ESQUECE GPT-4"
- "NUNCA MAIS USE"

### Checklist de Validação CLICKBAIT

Antes de gerar thumbnails, validar:
- [ ] Título tem ≤20 caracteres? (contar no editor)
- [ ] Subtítulo tem ≤25 caracteres? (contar no editor)
- [ ] Ambos em MAIÚSCULAS?
- [ ] Tem número/dado específico?
- [ ] Gera curiosidade/urgência/exclusividade?
- [ ] É clickbait HONESTO? (não engana o espectador)
- [ ] Complementam um ao outro? (título + subtítulo)

---

## 💡 Boas Práticas

### ✅ FAZER:
- **SEMPRE contar caracteres antes de usar**
- Usar números específicos (10X, 48%, 7 DIAS)
- Criar contraste emocional (problema vs solução)
- Focar em resultado/transformação ESPECÍFICO
- Aplicar frameworks clickbait consistentemente
- Testar legibilidade em tamanho pequeno
- Manter consistência visual entre vídeos

### ❌ NÃO FAZER:
- ❌ **Textos longos (>20 título, >25 subtítulo)**
- ❌ **Usar headline original diretamente sem extrair essência**
- ❌ Minúsculas (sempre MAIÚSCULAS)
- ❌ Textos genéricos ("Aprenda", "Descubra")
- ❌ Múltiplas fontes (manter moderna + dourado)
- ❌ Mudar paleta de cores
- ❌ Mudar layout (texto esquerda / foto direita)

---

## 🔗 Recursos Relacionados

- **SKILL.md** → Workflow completo
- **EXAMPLES.md** → 5 casos reais
- **TROUBLESHOOTING.md** → Resolver erros
- **hormozi-leads skill** → Gerar headlines persuasivas
