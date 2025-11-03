# 🎨 Thumbnail Creation - Criador de Thumbnails Virais para YouTube

Sistema automatizado para criar 4 variações de thumbnails virais usando suas fotos + headlines do Hormozi.

**Status:** ✅ Funcional e testado

---

## 📋 Visão Geral

Este sistema gera thumbnails profissionais para YouTube em 4 estilos virais diferentes:

1. **MrBeast Style** - Vibrante, setas, expressivo
2. **Tech Minimal** - Gradiente, profissional, clean
3. **High Contrast** - Preto/neon, glitch, cyberpunk
4. **Split Screen** - Foto + visual relacionado

**Tecnologia:** Nano Banana Edit (Gemini 2.5 Flash)

---

## 🚀 Setup Inicial (UMA VEZ)

### Passo 1: Adicionar Suas 4 Fotos

Coloque 4 fotos suas na pasta:

```
scripts/thumbnail-creation/templates/fotos/
├── foto1.jpg
├── foto2.jpg
├── foto3.jpg
└── foto4.jpg
```

**Especificações recomendadas:**
- **Resolução:** Mínimo 1920x1080 (recomendado: 4K)
- **Formato:** .jpg ou .png
- **Expressões variadas:** Neutra, sorrindo, surpreso, sério
- **Fundo:** Pode ter (será removido automaticamente)
- **Enquadramento:** Busto ou rosto close

### Passo 2: Upload para Nextcloud (URLs Permanentes)

Execute UMA VEZ para fazer upload e salvar URLs:

```bash
python3 scripts/thumbnail-creation/setup_photos.py
```

**O que faz:**
- ✅ Upload das 4 fotos para Nextcloud (URLs permanentes por 1 ano)
- ✅ Salva URLs em `photos_urls.json`
- ✅ Reutilização sem re-upload

**Output:**
```
📸 Setup de Fotos Base para Thumbnails
============================================================
✅ 4 fotos encontradas:
   1. foto1.jpg
   2. foto2.jpg
   3. foto3.jpg
   4. foto4.jpg

📤 Fazendo upload para Nextcloud (URLs permanentes)...
   ✅ 4 URLs salvas

✅ Setup Concluído!
```

---

## 🎬 Uso Regular

### Gerar Thumbnails (Após Setup)

```bash
# Uso básico
python3 scripts/thumbnail-creation/create_thumbnails.py "Sua Headline Aqui"

# Com tópico personalizado (para organizar arquivos)
python3 scripts/thumbnail-creation/create_thumbnails.py "Como IA Mudou TUDO" --topic "ia-2024"
```

**Parâmetros:**
- `headline` (obrigatório): Headline viral (vem do hormozi-leads)
- `--topic`, `-t` (opcional): Nome do tópico para organização de arquivos

**O que acontece:**
1. Escolhe aleatoriamente 1 das 4 fotos (via URL salva)
2. Gera 4 variações com estilos diferentes
3. Salva em `output/thumbnails/`

**Output:**
```
🎬 Thumbnail Creator - Gerador de Thumbnails Virais
============================================================
✅ 4 fotos disponíveis
📸 Foto escolhida aleatoriamente: foto3.jpg

📋 Headline: "Como IA Mudou TUDO"
📂 Output: /Users/.../output/thumbnails

============================================================
🎨 Estilo: MR-BEAST
============================================================
📝 Gerando thumbnail...
✅ Salvo: thumbnail_ia-2024_mr-beast.jpg

[... 3 outros estilos ...]

🎉 Geração Concluída!
============================================================

✅ 4/4 thumbnails criados com sucesso:
   • thumbnail_ia-2024_mr-beast.jpg
   • thumbnail_ia-2024_tech-minimal.jpg
   • thumbnail_ia-2024_high-contrast.jpg
   • thumbnail_ia-2024_split-screen.jpg

📂 Pasta: /Users/.../output/thumbnails
💡 Escolha a melhor thumbnail e use no seu vídeo do YouTube!
```

---

## 🎨 4 Estilos de Thumbnail

### 1. MrBeast Style
**Quando usar:** Conteúdo emocional, revelações, curiosidades

**Características:**
- Fundo: Vermelho/Amarelo vibrante
- Expressão: Muito surpresa/empolgada
- Texto: MAIÚSCULO GIGANTE
- Elementos: Setas amarelas, círculos ao redor do rosto
- Energia: MÁXIMA

**Exemplo de uso:** "Descobri o SEGREDO da IA!"

---

### 2. Tech Minimal
**Quando usar:** Conteúdo técnico, profissional, educativo

**Características:**
- Fundo: Gradiente azul escuro → roxo escuro
- Expressão: Profissional/sério
- Texto: Clean, moderno, minimalista
- Elementos: Ícones tech sutis (cérebro IA, circuitos)
- Visual: Futurista, limpo

**Exemplo de uso:** "Arquitetura do GPT-4o Explicada"

---

### 3. High Contrast
**Quando usar:** Impacto visual, anúncios, chamadas fortes

**Características:**
- Fundo: PRETO SÓLIDO
- Expressão: Qualquer
- Texto: Amarelo/verde neon BRILHANTE
- Elementos: Efeito glitch, bordas neon
- Visual: Cyberpunk, contrastes extremos

**Exemplo de uso:** "A VERDADE Sobre Claude AI"

---

### 4. Split Screen
**Quando usar:** Comparações, before/after, lado a lado

**Características:**
- Layout: Dividido verticalmente (50/50)
- Lado esquerdo: Sua foto
- Lado direito: Visual relacionado
- Texto: Centralizado entre as partes
- Visual: Dinâmico, balanceado

**Exemplo de uso:** "ChatGPT vs Claude: Qual Vence?"

---

## 📊 Casos de Uso Comuns

### Caso 1: Vídeo Tutorial sobre IA

```bash
# Headline vinda do hormozi-leads
python3 scripts/thumbnail-creation/create_thumbnails.py \
  "Como Dominar IA em 30 Dias (Método Comprovado)" \
  --topic "tutorial-ia"
```

**Melhor estilo:** Tech Minimal (profissional, educativo)

---

### Caso 2: Vídeo de Novidade/Lançamento

```bash
python3 scripts/thumbnail-creation/create_thumbnails.py \
  "NOVA IA da Google DESTRUIU o ChatGPT" \
  --topic "gemini-2024"
```

**Melhor estilo:** MrBeast ou High Contrast (impacto máximo)

---

### Caso 3: Vídeo Comparativo

```bash
python3 scripts/thumbnail-creation/create_thumbnails.py \
  "Claude vs ChatGPT: Qual É MELHOR?" \
  --topic "comparacao-ia"
```

**Melhor estilo:** Split Screen (comparação visual)

---

## 🔧 Arquivos e Estrutura

```
scripts/thumbnail-creation/
├── README.md                    # Este arquivo
├── setup_photos.py              # Setup inicial (upload fotos)
├── create_thumbnails.py         # Gerador de thumbnails
├── photos_urls.json             # URLs das fotos (gerado pelo setup)
│
└── templates/
    └── fotos/
        ├── README.md            # Instruções das fotos
        ├── foto1.jpg            # Suas 4 fotos
        ├── foto2.jpg
        ├── foto3.jpg
        └── foto4.jpg
```

**Output:**
```
output/thumbnails/
├── thumbnail_ia-2024_mr-beast.jpg
├── thumbnail_ia-2024_tech-minimal.jpg
├── thumbnail_ia-2024_high-contrast.jpg
└── thumbnail_ia-2024_split-screen.jpg
```

---

## 🔄 Integração com Workflow YouTube

Este sistema integra com:

1. **hormozi-leads skill** → Gera múltiplas headlines
2. **youtube-educator skill** → Workflow completo de produção
3. **visual-explainer skill** → Apresentações para gravação

**Workflow completo:**
```
Você: "Cria vídeo sobre Transformers"
↓
youtube-educator → Extrai conteúdo
↓
Gera roteiro didático (Claude Code)
↓
visual-explainer → Apresentação HTML
↓
Você grava vídeo
↓
hormozi-leads → 6 headlines virais
↓
Você escolhe headline favorita
↓
thumbnail-creator → 4 thumbnails virais
↓
Você escolhe thumbnail favorita
↓
Upload YouTube (FASE 2)
```

---

## 🐛 Troubleshooting

### Erro: "photos_urls.json não encontrado"

**Solução:**
```bash
python3 scripts/thumbnail-creation/setup_photos.py
```

Certifique-se de ter as 4 fotos em `templates/fotos/`

---

### Erro: "Apenas X fotos encontradas"

**Solução:**
Adicione as 4 fotos com nomes corretos:
- `foto1.jpg` (ou .png)
- `foto2.jpg` (ou .png)
- `foto3.jpg` (ou .png)
- `foto4.jpg` (ou .png)

---

### Erro ao editar imagem (Nano Banana)

**Possíveis causas:**
- URL da foto expirou (se passou 1 ano)
- Conexão com internet instável

**Solução:**
```bash
# Re-fazer upload das fotos
python3 scripts/thumbnail-creation/setup_photos.py
```

---

### Thumbnails sem qualidade

**Dicas:**
1. Use fotos de alta resolução (mínimo Full HD)
2. Iluminação boa no rosto
3. Expressões faciais marcantes
4. Teste diferentes fotos (por isso são 4)

---

## 📈 Performance e Custos

| Operação | Latência | Custo Estimado |
|----------|----------|----------------|
| Setup (4 fotos) | ~1-2min | Grátis (Nextcloud) |
| 1 thumbnail | ~20-30s | ~$0.05 |
| 4 thumbnails | ~2-3min | ~$0.20 |

**Total por vídeo:** ~$0.20 para ter 4 opções de thumbnail

---

## 💡 Dicas para Thumbnails Virais

### 1. Expressões Faciais
- **MrBeast Style:** Muito surpreso, boca aberta, olhos arregalados
- **Tech Minimal:** Sério, profissional, confiante
- **High Contrast:** Qualquer expressão (foco no contraste)
- **Split Screen:** Neutro ou levemente sorrindo

### 2. Headlines Efetivas
- Use MAIÚSCULAS para impacto
- Números funcionam ("7 Segredos", "30 Dias")
- Promessa clara ("Como Fazer X", "Aprenda Y")
- Urgência ("Antes Que Seja Tarde", "Agora")

### 3. Testes A/B
- Gere 4 thumbnails
- Teste 2-3 no YouTube (mudar após upload)
- Veja qual tem melhor CTR (Click-Through Rate)
- Use o estilo vencedor nos próximos vídeos

### 4. Consistência de Marca
- Use sempre as mesmas 4 fotos (setup)
- Escolha 1-2 estilos como padrão
- Mantenha fontes/cores similares

---

## 🔗 Documentação Relacionada

- **hormozi-leads skill:** `.claude/skills/hormozi-leads/SKILL.md`
- **youtube-educator skill:** `.claude/skills/youtube-educator/SKILL.md` (em criação)
- **visual-explainer skill:** `.claude/skills/visual-explainer/SKILL.md`
- **Nano Banana Edit:** `scripts/image-generation/README.md`

---

## 📞 Suporte

**Para adicionar novo estilo de thumbnail:**

1. Edite `create_thumbnails.py`
2. Adicione novo objeto em `THUMBNAIL_STYLES`
3. Defina `name`, `prompt_template`, `size`
4. Teste com headline real

**Para mudar proporção (não 16:9):**

Edite `size` em cada estilo:
- `1:1` - Quadrado (Instagram)
- `9:16` - Vertical (Stories)
- `16:9` - Horizontal (YouTube)

---

---

## 🆕 Template Profissional (youtube-thumbnailv2)

**Novo sistema:** Estilo único profissional para thumbnails YouTube

### Diferença dos 4 Estilos Virais

| Sistema | Templates | Estilo | Uso |
|---------|-----------|--------|-----|
| **4 Estilos Virais** | `create_thumbnails.py` | MrBeast, Tech, High Contrast, Split | Variedade de estilos |
| **Profissional v2** | `generate_youtube_thumbnails.py` | Único (dourado/azul-ciano) | Consistência de marca |

### Características do Template Profissional

- ✅ **Estilo único:** Dourado + azul-ciano + preto
- ✅ **Layout fixo:** Texto esquerda / Foto direita
- ✅ **Split lighting:** Iluminação dramática
- ✅ **5 variações:** Mesmo estilo, textos diferentes
- ✅ **Integração:** Skill youtube-thumbnailv2

### Como Usar

```bash
# Gerar 5 variações profissionais
python3 scripts/thumbnail-creation/generate_youtube_thumbnails.py \
  "prompt 1..." \
  "prompt 2..." \
  "prompt 3..." \
  "prompt 4..." \
  "prompt 5..."
```

**Documentação completa:** `.claude/skills/youtube-thumbnailv2/`

### Quando Usar Cada Sistema

**Use 4 Estilos Virais quando:**
- Quer testar estilos diferentes
- Primeiro vídeo (ainda não sabe qual estilo funciona)
- Conteúdo viral/casual

**Use Template Profissional v2 quando:**
- Já tem identidade visual definida
- Quer consistência entre vídeos
- Conteúdo profissional/técnico
- Canal estabelecido

---

**Última atualização:** 2025-11-03
**Versão:** 1.1 (+ Template Profissional v2)
**API:** Nano Banana Edit (Gemini 2.5 Flash)
**Custo:** ~$0.05/thumbnail (ambos sistemas)
