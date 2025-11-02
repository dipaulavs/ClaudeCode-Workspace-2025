# Orshot - Exemplos Práticos

## Exemplo 1: Post Instagram

### Cenário
Criar um post Instagram promocional sobre Claude Code.

### Solicitação do Usuário
```
"Crie um post Instagram sobre Claude Code"
```

### Workflow da Skill

**1. Análise:**
- Tipo: Post Instagram (1080x1080)
- Conteúdo: Claude Code
- Estilo: Moderno e profissional

**2. Execução:**
```bash
python3 scripts/orshot/generate_image.py \
  --template "instagram-post-1" \
  --title "Claude Code" \
  --subtitle "65+ templates de automação prontos" \
  --color "#FF6B35" \
  --output "post-claude-code.png"
```

**3. Resultado:**
- Imagem PNG 1080x1080 salva
- Preview mostrado ao usuário
- Pronto para publicar

**4. Publicação (opcional):**
```bash
python3 scripts/instagram/publish_post.py \
  --image "post-claude-code.png" \
  --caption "Automatize tudo com Claude Code! 🚀"
```

---

## Exemplo 2: Certificados em Massa

### Cenário
Gerar 50 certificados de conclusão para alunos de um curso.

### Solicitação do Usuário
```
"Gere certificados para esses 50 alunos" [fornece planilha]
```

### Workflow da Skill

**1. Análise:**
- Tipo: Certificados PDF
- Quantidade: 50
- Dados: Nome + Data

**2. Preparação dos Dados:**
```json
// alunos.json
[
  {
    "name": "João Silva",
    "course": "Python Avançado",
    "date": "15/01/2025",
    "instructor": "Prof. Maria Santos"
  },
  {
    "name": "Ana Costa",
    "course": "Python Avançado",
    "date": "15/01/2025",
    "instructor": "Prof. Maria Santos"
  }
  // ... mais 48 alunos
]
```

**3. Execução:**
```bash
python3 scripts/orshot/batch_generate.py \
  --template "certificado-conclusao" \
  --data "alunos.json" \
  --output-dir "certificados/" \
  --format pdf
```

**4. Resultado:**
- 50 PDFs gerados em ~2min
- Salvos em `certificados/`
- Nomes: certificado_joao_silva.pdf, certificado_ana_costa.pdf, etc.
- Custo: 50 × $0.01 = $0.50

---

## Exemplo 3: Open Graph Image

### Cenário
Criar Open Graph image para post de blog.

### Solicitação do Usuário
```
"Crie OG image para meu blog post sobre Claude Skills"
```

### Workflow da Skill

**1. Análise:**
- Tipo: OG Image (1200x630)
- Título: "Claude Skills"
- Descrição: Resumo do post

**2. Execução:**
```bash
python3 scripts/orshot/generate_image.py \
  --template "open-graph-image-1" \
  --title "Claude Skills: Superpoderes para IA" \
  --subtitle "8 capacidades modulares model-invoked" \
  --color "#8B5CF6" \
  --output "og-claude-skills.png" \
  --format png
```

**3. Resultado:**
- PNG 1200x630 salvo
- Otimizado para compartilhamento social
- Pronto para meta tag `og:image`

**4. Uso no HTML:**
```html
<meta property="og:image" content="https://meusite.com/og-claude-skills.png">
<meta property="twitter:image" content="https://meusite.com/og-claude-skills.png">
```

---

## Exemplo 4: Tweet com Preview

### Cenário
Criar preview visual para tweet de lançamento.

### Solicitação do Usuário
```
"Crie uma imagem para anunciar o lançamento do meu produto no Twitter"
```

### Workflow da Skill

**1. Análise:**
- Tipo: Twitter image (1200x675)
- Conteúdo: Anúncio de lançamento
- CTA: Link no tweet

**2. Execução:**
```bash
python3 scripts/orshot/generate_image.py \
  --template "tweet-preview-1" \
  --title "🚀 Lançamento Oficial!" \
  --subtitle "ClaudeCode Workspace está no ar" \
  --color "#1DA1F2" \
  --output "tweet-lancamento.png"
```

**3. Resultado:**
- PNG 1200x675 salvo
- Formato otimizado para Twitter
- Texto legível em mobile

**4. Tweet (via API ou manual):**
```bash
# Opcional: postar via Twitter API
python3 scripts/twitter/post_tweet.py \
  --text "Finalmente chegou! 🎉 ClaudeCode Workspace com 65+ templates prontos. Link: https://..." \
  --image "tweet-lancamento.png"
```

---

## Exemplo 5: Convites Personalizados

### Cenário
Criar 20 convites digitais para evento corporativo.

### Solicitação do Usuário
```
"Crie convites personalizados para os convidados VIP do evento"
```

### Workflow da Skill

**1. Análise:**
- Tipo: Convites digitais
- Quantidade: 20
- Personalização: Nome do convidado

**2. Dados:**
```json
// convidados.json
[
  {
    "name": "Dr. Carlos Lima",
    "title": "CEO TechCorp",
    "table": "Mesa 1"
  },
  {
    "name": "Dra. Paula Mendes",
    "title": "Diretora Innovation Co",
    "table": "Mesa 1"
  }
  // ... mais 18 convidados
]
```

**3. Execução:**
```bash
python3 scripts/orshot/batch_generate.py \
  --template "convite-evento-vip" \
  --data "convidados.json" \
  --output-dir "convites/" \
  --format png
```

**4. Distribuição (WhatsApp):**
```bash
# Enviar cada convite via WhatsApp
python3 scripts/whatsapp/send_media.py \
  --phone 5531999999999 \
  --file "convites/convite_carlos_lima.png" \
  --caption "Dr. Carlos, confirme sua presença! 🎉"
```

---

## Exemplo 6: Story Instagram Diário

### Cenário
Automatizar criação de story diário com frase motivacional.

### Solicitação do Usuário
```
"Crie um story Instagram com frase motivacional do dia"
```

### Workflow da Skill

**1. Análise:**
- Tipo: Instagram Story (1080x1920)
- Conteúdo: Frase motivacional
- Frequência: Diário

**2. Execução:**
```bash
# Pode combinar com API de frases ou lista pré-definida
python3 scripts/orshot/generate_image.py \
  --template "instagram-story-quote" \
  --title "Frase do Dia" \
  --subtitle "O sucesso é a soma de pequenos esforços repetidos dia após dia." \
  --color "#FF6B35" \
  --output "story-$(date +%Y%m%d).png"
```

**3. Publicação automática:**
```bash
python3 scripts/instagram/publish_story.py \
  --image "story-20250115.png"
```

**4. Automação (cron job):**
```bash
# Executar todo dia às 8h
0 8 * * * cd /caminho/workspace && python3 scripts/orshot/generate_image.py ... && python3 scripts/instagram/publish_story.py ...
```

---

## Exemplo 7: Thumbnails YouTube em Lote

### Cenário
Criar 10 thumbnails padronizados para série de vídeos.

### Solicitação do Usuário
```
"Crie thumbnails para minha série de 10 vídeos sobre Python"
```

### Workflow da Skill

**1. Dados:**
```json
// videos.json
[
  {"episode": "01", "title": "Introdução ao Python", "topic": "Basics"},
  {"episode": "02", "title": "Variáveis e Tipos", "topic": "Basics"},
  {"episode": "03", "title": "Estruturas de Controle", "topic": "Intermediate"}
  // ... mais 7 vídeos
]
```

**2. Execução:**
```bash
python3 scripts/orshot/batch_generate.py \
  --template "youtube-thumbnail-series" \
  --data "videos.json" \
  --output-dir "thumbnails/" \
  --format jpg
```

**3. Resultado:**
- 10 JPGs (1280x720) gerados
- Design consistente (branding)
- Prontos para upload no YouTube
- Custo: 10 × $0.01 = $0.10

---

## Exemplo 8: Banner LinkedIn Sazonal

### Cenário
Atualizar banner do LinkedIn para campanha de fim de ano.

### Solicitação do Usuário
```
"Crie um banner LinkedIn para minha campanha de Black Friday"
```

### Workflow da Skill

**1. Execução:**
```bash
python3 scripts/orshot/generate_image.py \
  --template "linkedin-banner-promo" \
  --title "Black Friday: 50% OFF" \
  --subtitle "Todos os planos de automação" \
  --color "#000000" \
  --output "linkedin-banner-blackfriday.png"
```

**2. Resultado:**
- PNG 1584x396 (tamanho LinkedIn)
- Design profissional
- Pronto para upload manual ou via API

---

## Dicas para Melhores Resultados

### Escolha de Templates
- **Genérico:** Use templates pré-prontos para rapidez
- **Branding:** Crie template customizado no Studio para consistência
- **Teste:** Gere 2-3 variações e escolha a melhor

### Textos
- **Curtos:** Máximo 60 caracteres para títulos
- **Legíveis:** Evite fontes muito pequenas
- **Hierarquia:** Título > Subtítulo > Footer

### Cores
- **Contraste:** Texto escuro em fundo claro (ou vice-versa)
- **Branding:** Use paleta da marca
- **Hex:** Sempre usar códigos hex (#FF6B35)

### Formatos
- **Web/Social:** PNG (transparência) ou JPG (menor tamanho)
- **Impressão:** PDF (melhor qualidade)
- **Performance:** WEBP (otimizado)
