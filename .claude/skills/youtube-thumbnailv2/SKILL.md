# YouTube Thumbnail Generator v2

Gera 5 thumbnails profissionais para YouTube usando Nano Banana Edit em paralelo.

## 🎯 Quando Usar

**Ativação automática quando usuário disser:**
- "crie uma thumbnail"
- "thumbnail do youtube"
- "miniatura do vídeo"
- "capa para o vídeo"

## 📋 Workflow (5 Passos)

1. **Receber input do usuário:**
   - Headline do vídeo
   - Resumo breve do conteúdo

2. **⚠️ TRANSFORMAR em CLICKBAIT CURTO (OBRIGATÓRIO):**
   - **NUNCA usar headline longa diretamente**
   - Extrair ESSÊNCIA em máx 20 caracteres
   - Criar 5 variações clickbait diferentes
   - Aplicar frameworks: Resultado/Comparação/Segredo/Urgência/Transformação/Negação
   - Validar checklist antes de prosseguir

3. **Gerar 5 variações criativas:**
   - Usar o template base (abaixo)
   - Variar: título CURTO, subtítulo CURTO, data/hora, selo
   - Manter: estrutura, iluminação, paleta de cores

4. **Preparar prompts:**
   - Copiar template completo 5 vezes
   - Substituir apenas as partes marcadas com {{VARIÁVEL}}
   - **IMPORTANTE:** Validar que título tem ≤20 chars e subtítulo ≤25 chars
   - Manter resto idêntico

5. **Executar script batch:**
   - Script: `tools/batch_edit_thumbnails.py`
   - Gera 5 thumbnails simultaneamente (90-120s)

6. **Retornar ao usuário:**
   - 5 URLs públicas das thumbnails
   - Caminhos dos arquivos salvos em ~/Downloads
   - Preview visual (se possível)
   - **Mostrar os textos usados** (para validação)

---

## 🔧 Recursos Prontos

| Recurso | Valor/Caminho |
|---------|---------------|
| **Script principal** | `scripts/thumbnail-creation/generate_youtube_thumbnails.py` |
| **Script low-level** | `tools/batch_edit_thumbnails.py` |
| **Foto base** | `https://media.loop9.com.br/s/C9WLo3EytYjNKwm/download/foto1.jpg` |
| **Proporção** | 16:9 (YouTube) - 1024x576px |
| **Formato** | PNG |
| **Tempo** | ~90s para 5 thumbnails |

---

## 📝 Template de Prompt (COPIAR E MODIFICAR)

```
Crie uma thumbnail de tecnologia para um vídeo sobre {{TEMA}}.
Texto e Gráficos (no lado esquerdo da imagem): Título: Escreva "{{TÍTULO}}" em letras MAIÚSCULAS GRANDES (fonte moderna, negrito, contornada em dourado). IMPORTANTE: O título deve ser CURTO (máximo 20 caracteres) e IMPACTANTE. Subtítulo: Abaixo do título, insira uma barra dourada sólida com o texto "{{SUBTÍTULO}}" em letras MAIÚSCULAS (máximo 25 caracteres). Data: Abaixo da barra, adicione "{{DATA}}" em uma fonte branca e limpa. Selo: No canto inferior esquerdo, adicione um pequeno texto "{{SELO}}" em MAIÚSCULAS.
Foto Principal: Use a minha foto em um close-up, do peito para cima. O meu rosto deve ocupar a metade direita da imagem, com um olhar sério e direto para a câmera.
Iluminação: Aplique uma iluminação de estúdio dramática com o estilo 'split lighting'. Metade do meu rosto deve estar em sombra profunda, enquanto a outra metade é iluminada por uma luz azul-ciano fria. Se eu estiver usando óculos, adicione um reflexo laranja vibrante nas lentes.
Fundo: O fundo deve ser preto e escuro.
Estilo Geral: A imagem deve ter um clima profissional, tecnológico e de alto impacto, com uma paleta de cores focada em preto, dourado e o contraste do azul-ciano.
```

**⚠️ VALIDAÇÃO OBRIGATÓRIA antes de usar:**
- {{TÍTULO}} tem ≤20 caracteres? (contar espaços)
- {{SUBTÍTULO}} tem ≤25 caracteres? (contar espaços)
- Ambos estão em MAIÚSCULAS?
- São clickbait que chamam atenção?

---

## ⚡ Partes VARIÁVEIS (MODIFICAR apenas estas)

| Variável | Descrição | Limites | Exemplos CLICKBAIT |
|----------|-----------|---------|---------------------|
| `{{TEMA}}` | Assunto do vídeo | 1-3 palavras | "IA", "ChatGPT", "produtividade" |
| `{{TÍTULO}}` | **CLICKBAIT CURTO** | **Máx 20 caracteres** | "ISSO MUDOU TUDO", "SUPERA GPT-5", "48% MAIS RÁPIDO" |
| `{{SUBTÍTULO}}` | **GANCHO IMPACTO** | **Máx 25 caracteres** | "Ninguém Te Conta", "Testei Por 30 Dias", "Resultado Chocante" |
| `{{DATA}}` | Data/hora (opcional) | 8-15 caracteres | "05/11, quarta", "10/11 \| 20h" |
| `{{SELO}}` | Badge urgência | 1-2 palavras | "NOVO", "AO VIVO", "GRÁTIS", "ÚLTIMA CHANCE" |

### 💡 Regras de CLICKBAIT (OBRIGATÓRIO)

**✅ SEMPRE FAZER:**
- **CURTO:** Máx 20 chars no título, 25 no subtítulo
- **MAIÚSCULAS:** Sempre em CAPS (gera impacto visual)
- **NÚMEROS:** Use quando possível ("48%", "10X", "7 DIAS")
- **GATILHOS:** Curiosidade/urgência/exclusividade/resultado
- **ESPECIFICIDADE:** "SUPERA GPT-5" > "Melhor que IA"
- **CONTRASTE:** "X vs Y", "ANTES/DEPOIS", "ISSO vs AQUILO"

**❌ NUNCA FAZER:**
- ❌ Textos longos (>25 caracteres ficam ilegíveis)
- ❌ Frases completas (thumbnail não é artigo)
- ❌ Minúsculas (sem impacto visual)
- ❌ Genérico ("Aprenda", "Descubra" sem contexto)
- ❌ Abstrato ("Sucesso", "Inovação" sem especificidade)

### 🎯 Frameworks de CLICKBAIT para Thumbnails

**1. RESULTADO CHOCANTE (números):**
- "48.75% NO SWEBENCH"
- "10X MAIS RÁPIDO"
- "R$50K EM 7 DIAS"

**2. COMPARAÇÃO DIRETA (vs):**
- "SUPERA GPT-5"
- "MELHOR QUE CLAUDE"
- "ISSO vs AQUILO"

**3. EXCLUSIVIDADE/SEGREDO:**
- "NINGUÉM TE CONTA"
- "SEGREDO REVELADO"
- "SÓ AQUI VOCÊ VÊ"

**4. TEMPO/URGÊNCIA:**
- "EM 90 SEGUNDOS"
- "TESTEI POR 30 DIAS"
- "ÚLTIMA CHANCE"

**5. TRANSFORMAÇÃO:**
- "MUDOU TUDO"
- "VIROU O JOGO"
- "ANTES E DEPOIS"

**6. NEGAÇÃO/CONTRÁRIO:**
- "PARE DE USAR X"
- "NÃO FAÇA ISSO"
- "ESQUECE GPT-4"

### 📏 Checklist de Validação

Antes de gerar thumbnails, verificar:
- [ ] Título tem ≤20 caracteres?
- [ ] Subtítulo tem ≤25 caracteres?
- [ ] Está em MAIÚSCULAS?
- [ ] Tem número/dado específico?
- [ ] Gera curiosidade/urgência?
- [ ] É clickbait sem ser enganoso?

**Para {{SELO}}:**
- Novo → lançamentos
- Ao Vivo → transmissões
- Exclusivo → conteúdo premium
- Imperdível → eventos importantes
- Premium → conteúdo pago

---

## 🔒 Partes FIXAS (NUNCA modificar)

✅ **Manter sempre idêntico:**
- Layout: Texto esquerda / Foto direita
- Foto: Close-up, peito para cima, lado direito
- Iluminação: Split lighting (sombra + azul-ciano)
- Reflexo: Laranja nos óculos
- Fundo: Preto e escuro
- Paleta: Preto, dourado, azul-ciano
- Fonte: Moderna, contornada em dourado
- Barra: Dourada sólida
- Estilo: Profissional, tecnológico, alto impacto

---

## 🚀 Como Executar

### Método 1: Via script principal (produção)

```bash
# Gerar 5 thumbnails com prompts customizados
python3 scripts/thumbnail-creation/generate_youtube_thumbnails.py \
  "prompt 1 completo..." \
  "prompt 2 completo..." \
  "prompt 3 completo..." \
  "prompt 4 completo..." \
  "prompt 5 completo..."
```

**Uso pela skill:**
1. Receber headline + resumo do usuário
2. Gerar 5 prompts (substituir variáveis do template)
3. Executar script passando os 5 prompts como argumentos
4. Retornar URLs + paths ao usuário

### Método 2: Modo teste (desenvolvimento)

```bash
# Rodar com 5 prompts hardcoded para teste
python3 tools/batch_edit_thumbnails.py
```

**Nota:** Usa prompts de exemplo. Útil para testar API/configuração.

---

## 📊 Output Esperado

Após execução bem-sucedida:

```
✅ Sucesso: 5/5
   📁 thumbnail_[nome]_[timestamp].png
   🔗 https://tempfile.aiquickdraw.com/workers/nano/image_[id].png

📂 Localização: ~/Downloads
```

**Cada thumbnail inclui:**
- Foto profissional editada (sua foto)
- Texto persuasivo (lado esquerdo)
- Layout profissional YouTube
- Resolução 1024x576 (16:9)

---

## ⚙️ Detalhes Técnicos

- **API:** Kie.ai (Nano Banana Edit)
- **Modelo:** google/nano-banana-edit (Gemini 2.5 Flash)
- **Processamento:** Paralelo (5 tasks simultâneas)
- **Timeout:** 300s por thumbnail
- **Custo:** ~$0.03 por thumbnail (5 = $0.15)

---

## 📚 Próximos Passos

- Ver `REFERENCE.md` para anatomia detalhada do template
- Ver `EXAMPLES.md` para 5 casos reais completos
- Ver `TROUBLESHOOTING.md` se encontrar erros
