# Troubleshooting - Problemas Comuns

## Erro: Subagente não retorna copy estruturada

### Sintoma
```
Subagente retorna texto corrido sem estrutura de slides clara
```

### Causa
Prompt vago ou sem exemplo de formato

### Solução
No prompt do Task, adicione:
```
IMPORTANTE: Retorne no formato:

SLIDE 1:
Copy: [texto exato]
Ícones: [lista]

SLIDE 2:
Copy: [texto exato]
Ícones: [lista]
...
```

---

## Erro: Copy gerada não segue estilo Hormozi

### Sintoma
- Copy genérica ("linda chácara", "ótima oportunidade")
- Sem números específicos
- Sem matemática brutal

### Causa
Subagente não leu REFERENCE.md corretamente

### Solução
No prompt do Task, reforce:
```
OBRIGATÓRIO seguir metodologia Hormozi em REFERENCE.md:
- Números específicos (não "muitas", mas "23 famílias")
- Matemática brutal (comparação lado a lado)
- Destruir objeções com fatos
- Urgência/escassez real
```

---

## Erro: Usuário rejeita todas as 3 opções

### Sintoma
Nenhuma das opções geradas agrada o usuário

### Causa
Skill não capturou "voz" ou ângulo desejado

### Solução
1. Pergunte especificamente:
   ```
   "Qual ângulo você quer enfatizar?"
   - Matemática (números/comparação)
   - Emocional (família/qualidade de vida)
   - Urgência (escassez/preço subindo)
   - Objeção (nome sujo/sem entrada)
   ```

2. Peça exemplos:
   ```
   "Tem algum anúncio/carrossel que você gostou? Me passa o link."
   ```

3. Reprocesse com contexto adicional

---

## Erro: Imagens geradas não seguem estilo artesanal

### Sintoma
Imagens muito "digitais" ou "profissionais demais"

### Causa
Prompt visual não está sendo aplicado corretamente

### Solução
Verifique se subagente de prompts usou template EXATO:
```
"Crie uma colagem artesanal e realista feita à mão..."
```

Se persistir, adicione no final de cada prompt:
```
"IMPORTANTE: Deve parecer feito à mão com canetinhas e papéis colados, NÃO design digital."
```

---

## Erro: Timeout na geração de imagens

### Sintoma
```
❌ Slide X: Timeout
```

### Causa
API Kie.ai congestionada ou prompt muito complexo

### Solução
1. **Reprocessar apenas slides com falha:**
   ```bash
   # Identifique slides que falharam
   # Gere apenas esses (use --slides 3,5,7)
   ```

2. **Simplificar prompt:**
   - Menos elementos por slide
   - Descrições mais diretas

3. **Aumentar timeout:**
   Em `batch_carrossel_gpt4o.py`:
   ```python
   max_wait = 300  # Aumentar para 600
   ```

---

## Erro: Arquivo JSON de prompts mal formatado

### Sintoma
```
❌ Erro ao ler prompts-file: JSON decode error
```

### Causa
Subagente retornou texto em vez de JSON válido

### Solução
No prompt do subagente de imagens, reforce:
```
RETORNE APENAS JSON VÁLIDO, sem texto antes/depois:

[
  {"slide": 1, "conteudo": "...", "icones": "..."},
  {"slide": 2, "conteudo": "...", "icones": "..."}
]

NÃO adicione explicações, só o JSON puro.
```

---

## Erro: Slide 1 sem imagem de referência

### Sintoma
Slide 1 não usa foto do imóvel mesmo usuário tendo fornecido URL

### Causa
URL não passou corretamente para o gerador

### Solução
Verifique comando final:
```bash
python3 scripts/image-generation/batch_carrossel_gpt4o.py \
  --prompts-file ~/Downloads/carrossel_prompts.json \
  --image-url "https://exemplo.com/foto.jpg"  # ← Deve estar aqui
  --variants 4
```

---

## Erro: Variantes muito parecidas

### Sintoma
4 variantes de um slide são quase idênticas

### Causa
GPT-4o Image gerando pouca diversidade

### Solução
1. **Adicionar variação no prompt:**
   ```
   Subagente de imagens deve adicionar ao final:
   "Varie: posição dos papéis, cores predominantes, tamanho dos elementos."
   ```

2. **Aumentar número de variantes:**
   ```bash
   --variants 8  # Em vez de 4
   ```

3. **Gerar em 2 lotes:**
   - Lote 1: --variants 4
   - Ajustar prompt
   - Lote 2: --variants 4 (prompts levemente modificados)

---

## Erro: Copy muito longa para visual

### Sintoma
Texto não cabe no slide, fica ilegível

### Causa
Subagente gerou copy muito extensa

### Solução
No prompt de copy, adicione:
```
LIMITE DE TEXTO POR SLIDE:
- Título: Máx 12 palavras
- Corpo: Máx 40 palavras
- Listas: Máx 6 itens

Visual é colagem artesanal à mão, texto muito longo fica ilegível.
```

---

## Erro: CTA fraco no último slide

### Sintoma
Último slide sem urgência/escassez, CTA genérico

### Causa
Subagente não aplicou princípios Hormozi no final

### Solução
No prompt de copy, reforce para último slide:
```
SLIDE FINAL (CTA):
- Urgência REAL: "Restam X unidades" (número específico)
- Escassez: "Preço sobe em Y dias"
- CTA direto: "Chama no WhatsApp AGORA: (31) 98016-0822"
- Qualificação: "Não é pra todo mundo. SE VOCÊ tem R$ X..."
```

---

## Erro: Skill não ativa automaticamente

### Sintoma
Usuário diz "criar carrossel Meta Ads" mas skill não inicia

### Causa
Frase não corresponde aos gatilhos da skill

### Solução
**Frases que devem ativar:**
- "criar carrossel Meta Ads"
- "gerar anúncio carrossel Instagram"
- "preciso carrossel para Facebook Ads"
- "quero anunciar [imóvel] em carrossel"

Se não ativar, invoque manualmente:
```
/skills carrossel-meta-ads
```

---

## Erro: Processo muito lento

### Sintoma
Todo workflow leva mais de 20 minutos

### Causa
Subagentes rodando sequencialmente

### Solução
Não há como paralelizar subagentes (copy → prompts → imagens é sequencial).

**Otimizações possíveis:**
1. **Aprovar copy mais rápido** (não pedir múltiplas revisões)
2. **Reduzir variantes** (--variants 2 em vez de 4)
3. **Testar com --limit 3** antes de gerar completo

---

## Perguntas Frequentes

### "Posso usar para outros nichos?"

Sim. Adapte exemplos em REFERENCE.md para:
- Carros
- Infoprodutos
- Serviços
- SaaS

### "Preciso de 3 opções sempre?"

Não. Modifique SKILL.md para gerar 1 ou 5 opções se preferir.

### "Posso gerar sem foto do imóvel?"

Sim. Deixe `--image-url` vazio. Todos slides usarão só copy.

### "Posso editar copy manualmente após aprovação?"

Sim. Edite JSON antes de gerar:
```bash
nano ~/Downloads/carrossel_prompts_[timestamp].json
```

### "Como adiciono música/áudio nos slides?"

Skill gera só imagens. Para vídeo com áudio:
1. Gere imagens (esta skill)
2. Use `scripts/video-generation/` para compilar
3. Adicione áudio com `scripts/audio-generation/`
