# Workflow: Headline to Image

**Objetivo:** Gerar imagens com headlines virais automaticamente

## Input Necessário
- Nicho/tema para as headlines
- Quantidade de imagens desejadas (padrão: 3)

## Etapas do Workflow

### 1. Gerar Headlines Virais
**Ferramenta:** Agente OpenRouter `agente-1201-[youtube-headline]`

**Ação:**
```bash
python3 tools/agent_openrouter.py "agente-1201-[youtube-headline]" "Crie [QUANTIDADE] headlines super virais para o nicho de [NICHO]. As headlines devem ser extremamente persuasivas e otimizadas para alto CTR."
```

**Output:** Lista de headlines numeradas

---

### 2. Gerar Prompts de Imagem
**Ferramenta:** Agente local `imagem-colada`

**Ação:**
- Ativar o agente imagem-colada
- Passar as headlines geradas no passo 1
- Solicitar criação de prompts individuais para cada headline

**Input para o agente:**
```
Ative o agente imagem-colada e crie prompts de imagem para as seguintes headlines:

1. [HEADLINE 1]
2. [HEADLINE 2]
3. [HEADLINE 3]

Gere um prompt individual e detalhado para cada headline, otimizado para Nano Banana.
```

**Output:** 3 prompts completos e prontos para uso

---

### 3. Gerar Imagens
**Ferramenta:** Nano Banana (generate_image_nanobanana.py)

**Ação:**
Para cada prompt gerado, executar:
```bash
python3 tools/generate_image_nanobanana.py "PROMPT_1" --format PNG
python3 tools/generate_image_nanobanana.py "PROMPT_2" --format PNG
python3 tools/generate_image_nanobanana.py "PROMPT_3" --format PNG
```

**Alternativa (Batch - mais rápido):**
```bash
python3 tools/generate_image_batch.py "PROMPT_1" "PROMPT_2" "PROMPT_3" --format PNG
```

**Output:** Imagens salvas em `~/Downloads` com timestamp

---

## Exemplo Completo

**Input do Usuário:**
```
Ative o workflow headline-to-image para o nicho de mixagem e masterização de áudio, gerando 3 imagens.
```

**Execução:**

1. **Headlines geradas:**
   - "Por que SUA mixagem soa AMADORA (e como consertar em 5 minutos)"
   - "O SEGREDO que engenheiros ESCONDEM sobre masterização profissional"
   - "Ela mixou esse beat em 10 minutos (resultado CHOCANTE)"

2. **Prompts criados:**
   - Prompt 1: Professional music studio photography, centered bold text "POR QUE SUA MIXAGEM SOA AMADORA", mixing console background...
   - Prompt 2: 3D rendered scene, metallic text "O SEGREDO QUE ENGENHEIROS ESCONDEM", audio waveforms...
   - Prompt 3: Minimalist design, bold text "ELA MIXOU ESSE BEAT EM 10 MINUTOS", gradient background...

3. **Imagens geradas:**
   - `~/Downloads/nanobanana_20250130_143022.png`
   - `~/Downloads/nanobanana_20250130_143045.png`
   - `~/Downloads/nanobanana_20250130_143108.png`

---

## Notas

- Todas as imagens são geradas em formato portrait 2:3
- O processo todo leva aproximadamente 3-5 minutos
- Use `--format JPEG` se precisar de arquivos menores
- Para mais imagens, ajuste a quantidade no input inicial
