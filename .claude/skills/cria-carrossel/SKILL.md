---
name: cria-carrossel
description: Automatizar criação completa de carrosséis e reels para redes sociais com copy Hormozi, imagens em batch e organização profissional. Auto-invoca quando usuário pedir para criar carrossel, reels, post Instagram/LinkedIn, ou conteúdo visual viral.
---

# Cria Carrossel

## Overview

Automatiza criação completa de carrosséis virais e reels para redes sociais, desde a copy até geração de imagens em batch, com frameworks Hormozi e templates visuais validados. Produz conteúdo pronto para publicar com legenda, hashtags e arquivos organizados.

## Workflow Decision Tree

```
Usuário solicita carrossel/reels
    ↓
1. Coletar informações básicas
    ↓
2. Definir/criar copy ────> Skills: hormozi-exercito-viral | exercito-hormozi-ads
    ↓
3. Personalização visual (opcional)
    ↓
4. Escolher estilo CTA
    ↓
5. Referência visual (opcional) ────> Skill: pega-carrossel
    ↓
6. Gerar conteúdo
    ├─> CARROSSEL ────> openai-gpt-image (batch)
    └─> REELS ────> hormozi-copywriter + google-gemini-tts
    ↓
7. Organizar output profissional
    ↓
8. Finalizar com legenda + hashtags ────> Skill: hormozi-copywriter
```

## Step 1: Coletar Informações Básicas

Perguntar ao usuário em mensagem única e concisa:

**Inputs necessários:**
1. **Nicho/tema:** O que quer vender ou comunicar?
2. **Formato:** Carrossel ou reels?
3. **Copy existente:** Já tem copy pronta? Se NÃO, perguntar se é:
   - Conteúdo de valor (educacional) → Skill `hormozi-exercito-viral`
   - Conteúdo de venda (oferta/produto) → Skill `exercito-hormozi-ads`

**Formato da pergunta:**
```
Preciso de algumas informações:

1. Qual o nicho/tema? O que quer vender ou comunicar?
2. Formato: carrossel ou reels?
3. Já tem a copy? Se não, é conteúdo educacional ou de venda?
```

## Step 2: Definir/Criar Copy

### Se usuário JÁ tem copy:
- Prosseguir para Step 3

### Se usuário NÃO tem copy:

**Para conteúdo EDUCACIONAL (valor):**
```bash
# Invocar skill hormozi-exercito-viral
Skill: hormozi-exercito-viral
```
Aguardar copy gerada pela skill antes de prosseguir.

**Para conteúdo de VENDA:**
```bash
# Invocar skill exercito-hormozi-ads
Skill: exercito-hormozi-ads
```
Aguardar copy gerada pela skill antes de prosseguir.

## Step 3: Personalização Visual (Opcional)

Perguntar se usuário quer adicionar foto personalizada na capa:

**Pergunta:**
```
Quer adicionar alguma foto personalizada na capa do carrossel?
Se sim, envie o link da imagem.

Se não tiver link, posso te ajudar a subir a imagem no Nextcloud para gerar a URL.
```

### Upload Nextcloud (se necessário):

**Script disponível:** `scripts/nextcloud_upload.py`

```bash
python3 scripts/nextcloud_upload.py --file <caminho_local> --folder <pasta_destino>
```

Output: URL pública da imagem para usar nos prompts visuais.

## Step 4: Escolher Estilo CTA

Perguntar estilo de call-to-action:

**Pergunta:**
```
Qual estilo de CTA você prefere?

1. Palavra-chave nos comentários (ex: "Comente LISTA")
2. Click no botão WhatsApp
3. Chame na DM
```

Adaptar último slide do carrossel ou CTA do reels com base na escolha.

## Step 5: Referência Visual (Opcional)

Perguntar se usuário tem referência visual para copiar:

**Pergunta:**
```
Tem algum carrossel de referência que quer copiar o estilo visual?
Se sim, me envie o link do Instagram.
```

### Se SIM - Usar Skill pega-carrossel:

```bash
# Invocar skill pega-carrossel
Skill: pega-carrossel
```

A skill irá:
1. Baixar o carrossel do Instagram
2. Analisar visualmente cada slide
3. Gerar prompts detalhados para recriar estilo idêntico
4. Retornar prompts prontos para usar

Aguardar prompts gerados antes de prosseguir para Step 6.

### Se NÃO - Usar Templates da Biblioteca:

**Templates disponíveis em:**
```
biblioteca de prompts/Templates Carrosseis/
```

**Templates validados:**

1. **Colagem Artesanal** (`carrossel-colagem-artesanal.md`)
   - Estilo: Trabalho escolar feito à mão
   - Uso: Storytelling emocional, autenticidade
   - Prompts: Papéis colados, canetinhas coloridas, mesa de madeira

2. **Educacional ABSM** (`carrossel estilo ABSM/template_carrossel_educacional_6slides.txt`)
   - Estilo: Minimalista elegante tipo revista
   - Uso: Conteúdo educacional, autoridade
   - Prompts: Badge sticker ondulado, mockups Instagram, fotografia lifestyle

3. **Texto Tipo Adesivo** (`carrossel texto tipo adesivo/prompt template carrossel.txt`)
   - Estilo: Tipografia display com efeito sticker vintage
   - Uso: Paletas de cores, listas, tutoriais visuais
   - Prompts: Triple-layer sticker effect, layout Bento Box

4. **Antes e Depois** (`carrossel_estrelato estilo antes e depois/template_carrossel_minimalista_beige_8slides.txt`)
   - Estilo: Comparações lado a lado minimalistas
   - Uso: Transformações, resultados, provas
   - Prompts: Split screen, cores neutras beige

**Seleção automática:**
- Conteúdo educacional → Template ABSM ou Texto Adesivo
- Venda/oferta → Template Colagem Artesanal
- Comparação/prova → Template Antes e Depois

## Step 6: Gerar Conteúdo

### Se formato = CARROSSEL:

**Usar Skill openai-gpt-image para batch:**

```bash
# Invocar skill openai-gpt-image
Skill: openai-gpt-image
```

**Processo:**
1. Montar lista de prompts (1 por slide)
2. Se usuário forneceu foto personalizada, incluir no prompt do Slide 1
3. Aplicar template visual escolhido em todos os slides
4. Gerar imagens em batch (1-20 imagens simultâneas)

**Exemplo de invocação:**
```python
# Dentro da skill openai-gpt-image
prompts = [
    "Slide 1 - Gancho: [PROMPT_VISUAL_TEMPLATE] + [COPY_GANCHO]",
    "Slide 2 - Conteúdo: [PROMPT_VISUAL_TEMPLATE] + [COPY_SLIDE_2]",
    ...
    "Slide N - CTA: [PROMPT_VISUAL_TEMPLATE] + [COPY_CTA]"
]

# Skill gera todas as imagens em paralelo
```

### Se formato = REELS:

**Etapa 6.1 - Criar Roteiro (Skill hormozi-copywriter):**

```bash
# Invocar skill hormozi-copywriter
Skill: hormozi-copywriter
```

**Instrução para a skill:**
```
Escreva um roteiro de 15 segundos para uma blogueira com +50M seguidores.
Tema: [TEMA_DO_USUARIO]
Tom: Direto, pessoal, comunicação com [PUBLICO_ALVO]
Estrutura: Hook (3s) → Corpo (9s) → CTA (3s)
```

**Etapa 6.2 - Gerar Áudio (Skill google-gemini-tts):**

```bash
# Invocar skill google-gemini-tts
Skill: google-gemini-tts
```

**Instrução para a skill:**
```
Gere áudio natural estilo conversa casual:
Texto: [ROTEIRO_GERADO]
Voz: Feminina jovem brasileira (tom amigável)
Duração: ~15 segundos
```

## Step 7: Organizar Output Profissional

Criar estrutura de pastas organizada:

**Estrutura obrigatória:**
```
output/carrossel-{tema}-{data}/
├── Slide 1 - Gancho.png
├── Slide 2 - [nome-descritivo].png
├── Slide 3 - [nome-descritivo].png
├── ...
├── Slide N - CTA.png
├── links.txt
└── legenda-hashtags.txt
```

### Arquivo `links.txt`:

**Formato:**
```
Slide 1 - Gancho
https://url-da-imagem-1.png

Slide 2 - [Nome]
https://url-da-imagem-2.png

...

Slide N - CTA
https://url-da-imagem-N.png
```

**Se imagens NÃO retornarem URLs automaticamente:**

Usar script de upload Nextcloud:

```bash
# Upload de todas as imagens geradas
for file in output/carrossel-{tema}-{data}/*.png; do
    python3 scripts/nextcloud_upload.py --file "$file" --folder "carrosseis/{tema}"
done
```

Atualizar `links.txt` com URLs retornadas.

## Step 8: Finalizar com Legenda + Hashtags

**Invocar Skill hormozi-copywriter:**

```bash
# Invocar skill hormozi-copywriter
Skill: hormozi-copywriter
```

**Instrução para a skill:**
```
Escreva legenda viral + hashtags para Instagram/LinkedIn:

Tema: [TEMA_DO_CARROSSEL]
Copy dos slides: [RESUMO_DA_COPY]
CTA escolhido: [ESTILO_CTA]

Formato:
- 3-5 linhas de legenda pessoal/orgânica (tom Hormozi)
- Call-to-action integrado naturalmente
- 15-25 hashtags estratégicas (mix de alto/médio/baixo volume)
```

**Salvar em:** `output/carrossel-{tema}-{data}/legenda-hashtags.txt`

**Formato do arquivo:**
```txt
=== LEGENDA ===

[Legenda viral gerada pela skill]

=== HASHTAGS ===

#hashtag1 #hashtag2 #hashtag3 ...

=== CTA ===

[CTA específico do estilo escolhido]
```

## Resources

### scripts/

**nextcloud_upload.py** - Upload de imagens para Nextcloud e geração de URLs públicas

```bash
python3 scripts/nextcloud_upload.py --file <caminho> --folder <pasta>
```

### references/

**templates_visuais.md** - Biblioteca completa de templates de carrossel com prompts validados

Contém:
- Template Colagem Artesanal
- Template ABSM Educacional
- Template Texto Adesivo
- Template Antes e Depois
- Especificações técnicas (dimensões, cores, tipografia)
- Exemplos de uso por nicho

## Fluxograma Completo (Resumo)

```
Input usuário
    ↓
┌─────────────────────────────────────┐
│ 1. Coletar: nicho, formato, copy    │
└─────────────────────────────────────┘
    ↓
    ├─> Tem copy? ──NO──> Invocar:
    │                     - hormozi-exercito-viral (educacional)
    │                     - exercito-hormozi-ads (venda)
    └─> YES ──> Prosseguir
    ↓
┌─────────────────────────────────────┐
│ 2. Foto personalizada? (opcional)   │
│    YES → Upload Nextcloud → URL     │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. Escolher estilo CTA               │
│    - Palavra-chave comentários       │
│    - WhatsApp                        │
│    - DM                              │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. Tem referência visual?            │
│    YES → pega-carrossel              │
│    NO → Templates biblioteca         │
└─────────────────────────────────────┘
    ↓
    ├─> CARROSSEL ──> openai-gpt-image (batch)
    │                 └─> N slides em paralelo
    │
    └─> REELS ──> hormozi-copywriter (roteiro)
                  └─> google-gemini-tts (áudio)
    ↓
┌─────────────────────────────────────┐
│ 5. Organizar output                  │
│    - Pasta com slides nomeados       │
│    - links.txt com URLs              │
│    - Upload Nextcloud (se precisar)  │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 6. Gerar legenda + hashtags          │
│    hormozi-copywriter                │
│    └─> legenda-hashtags.txt          │
└─────────────────────────────────────┘
    ↓
✅ Output pronto para publicar
```

## Outputs Finais

**Para CARROSSEL:**
```
📁 output/carrossel-{tema}-{data}/
   ├── Slide 1 - Gancho.png
   ├── Slide 2 - [nome].png
   ├── ...
   ├── Slide N - CTA.png
   ├── links.txt
   └── legenda-hashtags.txt
```

**Para REELS:**
```
📁 output/reels-{tema}-{data}/
   ├── roteiro.txt
   ├── audio.mp3
   ├── legenda-hashtags.txt
   └── instrucoes-edicao.txt
```

## Notas Importantes

1. **Batch Generation:** SEMPRE usar geração em batch para múltiplas imagens (mais eficiente)
2. **Skills Sequenciais:** Aguardar output de cada skill antes de prosseguir (não usar placeholders)
3. **Organização:** Nunca entregar arquivos soltos - sempre estrutura de pasta completa
4. **URLs:** Se skill de imagem não retornar URLs, usar script Nextcloud obrigatoriamente
5. **Copy Hormozi:** Priorizar skills Hormozi para copy (nunca criar copy genérica manualmente)

## Auto-Correction System

Esta skill inclui sistema automático de correção de erros.

### Como Funciona

Quando um script ou comando falhar:

1. **Detectar erro** - Identificar o que deu errado
2. **Corrigir automaticamente** - Atualizar código/instruções
3. **Registrar aprendizado** - Salvar em LEARNINGS.md
4. **Prevenir recorrência** - Mesmo erro não acontece novamente

### Scripts Disponíveis

```bash
# Corrigir problema no SKILL.md
python3 scripts/update_skill.py <texto_antigo> <texto_novo>

# Registrar aprendizado
python3 scripts/log_learning.py <descrição_erro> <descrição_correção> [linha]
```

### Exemplo de Uso

```bash
# 1. Corrigir erro no SKILL.md
python3 scripts/update_skill.py \
    "python3 gerar_imagem.py --prompt" \
    "python3 gerar_imagem.py"

# 2. Registrar o aprendizado
python3 scripts/log_learning.py \
    "Flag --prompt não reconhecida" \
    "Removida flag --prompt, usar argumento posicional" \
    "SKILL.md:150"
```

### LEARNINGS.md

Todas as correções são registradas automaticamente:

```markdown
### 2025-01-10 - Flag --prompt não reconhecida

**Problema:** Script não aceita flag --prompt
**Correção:** Removida flag, usar argumento posicional
**Linha afetada:** SKILL.md:150
**Status:** ✅ Corrigido
```

Isso cria histórico de melhorias e garante que erros não se repitam.
