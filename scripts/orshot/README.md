# 🎨 Orshot - Automação de Design e Imagens

Scripts para gerar designs profissionais usando Orshot API - alternativa mais barata e poderosa ao Canva para automação.

## 📋 Visão Geral

Orshot permite criar imagens personalizadas em escala usando templates + dados. Perfeito para:
- Posts de redes sociais em massa
- Certificados personalizados
- Convites de eventos
- Open Graph images para blogs
- Marketing visual automatizado

## 🚀 Quick Start

### 1. Instalação

```bash
# Instalar dependências
pip install orshot pillow python-dotenv

# Adicionar API key no .env
echo "ORSHOT_API_KEY=os-XXXXXXXXXXXXXXXX" >> .env
```

### 2. Gerar Primeira Imagem

```bash
python3 scripts/orshot/generate_image.py \
  --template open-graph-image-1 \
  --title "Claude Code: AI Development Assistant"
```

## 📂 Scripts Disponíveis

### `generate_image.py` - Geração Única

Gera uma imagem a partir de template.

**Uso básico:**
```bash
# Template pré-pronto
python3 scripts/orshot/generate_image.py \
  --template open-graph-image-1 \
  --title "Meu Título"

# Template customizado (Studio)
python3 scripts/orshot/generate_image.py \
  --template custom-post-123 \
  --data '{"title":"Lançamento","color":"#FF6B6B","date":"10/Jan"}'

# Especificar formato
python3 scripts/orshot/generate_image.py \
  --template tweet-image-1 \
  --title "Hello World" \
  --format webp \
  --output post.webp
```

**Argumentos:**
- `--template, -t`: ID do template (obrigatório)
- `--title`: Texto principal (atalho simples)
- `--data, -d`: JSON completo com todas modificações
- `--format, -f`: Formato (png, jpg, webp, pdf) - padrão: png
- `--output, -o`: Caminho de saída (opcional)
- `--verbose, -v`: Modo detalhado

---

### `batch_generate.py` - Geração em Lote

Gera múltiplas imagens de uma vez (JSON ou CSV).

**Uso básico:**
```bash
# Gerar 50 certificados
python3 scripts/orshot/batch_generate.py \
  --template certificate-1 \
  --data alunos.json \
  --output certificados/

# Gerar posts de produtos (CSV)
python3 scripts/orshot/batch_generate.py \
  --template product-post \
  --data produtos.csv \
  --format webp \
  --limit 100
```

**Formato dos dados:**

**JSON:**
```json
[
  {
    "title": "João Silva",
    "course": "Python Avançado",
    "date": "10/01/2025"
  },
  {
    "title": "Maria Santos",
    "course": "Python Avançado",
    "date": "10/01/2025"
  }
]
```

**CSV:**
```csv
title,course,date
João Silva,Python Avançado,10/01/2025
Maria Santos,Python Avançado,10/01/2025
```

**Argumentos:**
- `--template, -t`: ID do template (obrigatório)
- `--data, -d`: Arquivo .json ou .csv (obrigatório)
- `--output, -o`: Diretório de saída (padrão: orshot_batch)
- `--format, -f`: Formato (png, jpg, webp, pdf)
- `--limit, -l`: Limitar quantidade
- `--verbose, -v`: Modo detalhado

---

### `list_templates.py` - Listar Templates

Lista templates disponíveis (pré-prontos + Studio).

**Uso:**
```bash
# Listar todos
python3 scripts/orshot/list_templates.py

# Buscar por termo
python3 scripts/orshot/list_templates.py --search certificate

# Ver apenas Studio
python3 scripts/orshot/list_templates.py --studio-only
```

## 🎨 Templates Pré-Prontos

| Template ID | Descrição | Parâmetros |
|-------------|-----------|------------|
| `open-graph-image-1` | OG image para blogs (1200x630) | title, description, image |
| `tweet-image-1` | Post estilo Twitter/X | title, author, date |
| `instagram-post-1` | Post Instagram (1080x1080) | title, description, image |
| `certificate-1` | Certificado genérico | name, course, date |
| `website-screenshot` | Screenshot de website | websiteUrl, fullCapture, delay |

**Dica:** Use `list_templates.py` para ver lista completa atualizada.

## 🎯 Templates Customizados (Studio)

### Criar no Orshot Studio

1. Acesse: https://orshot.com/studio
2. Crie design customizado
3. Parametrize elementos (textos, cores, imagens)
4. Copie o **Template ID**
5. Use nos scripts

### Importar do Canva

1. Abra seu design no Canva
2. Copie todo conteúdo (Ctrl+A, Ctrl+C)
3. No Orshot Studio: Ctrl+V
4. Parametrize e salve
5. Use o Template ID

### Exemplo de Uso

```bash
# Usar template Studio customizado
python3 scripts/orshot/generate_image.py \
  --template template-abc123xyz \
  --data '{"headline":"Novidade!","price":"R$ 99","color":"#FF6B6B"}'
```

## 📊 Exemplos Práticos

### Exemplo 1: Certificados em Massa

**1. Criar CSV de alunos:**
```csv
name,course,date,instructor
João Silva,Python Avançado,10/01/2025,Prof. Maria
Ana Santos,Python Avançado,10/01/2025,Prof. Maria
Carlos Souza,Python Avançado,10/01/2025,Prof. Maria
```

**2. Gerar certificados:**
```bash
python3 scripts/orshot/batch_generate.py \
  --template certificate-1 \
  --data alunos.csv \
  --output certificados/ \
  --format pdf
```

**Resultado:** 3 PDFs em `certificados/001_João_Silva.pdf`, etc.

---

### Exemplo 2: Posts Instagram de Produtos

**1. Criar JSON de produtos:**
```json
[
  {"title": "Tênis Nike", "price": "R$ 299", "image": "https://..."},
  {"title": "Camisa Adidas", "price": "R$ 89", "image": "https://..."}
]
```

**2. Gerar posts:**
```bash
python3 scripts/orshot/batch_generate.py \
  --template produto-instagram \
  --data produtos.json \
  --format jpg
```

---

### Exemplo 3: Open Graph para Blog Posts

```bash
python3 scripts/orshot/generate_image.py \
  --template open-graph-image-1 \
  --data '{"title":"Como usar Orshot API","description":"Tutorial completo"}' \
  --output blog/og-image.png
```

## 💰 Preços e Limites

| Plano | Preço/mês | Renders | Custo/render |
|-------|-----------|---------|--------------|
| Free (teste) | $0 | 100 | Grátis |
| Indie | $30 | 3.000 | $0.01 |
| Growth | ~$60 | 10.000 | $0.006 |
| Enterprise | Custom | 100.000+ | $0.003 |

**Teste grátis:** 100 renders sem cartão de crédito
**Site:** https://orshot.com/pricing

## 🔧 Configuração Avançada

### Variáveis de Ambiente (.env)

```bash
# API Key (obrigatório)
ORSHOT_API_KEY=os-XXXXXXXXXXXXXXXX

# Configurações opcionais
ORSHOT_DEFAULT_FORMAT=png
ORSHOT_DEFAULT_OUTPUT_DIR=orshot_output
```

### Formatos Suportados

- **PNG:** Padrão, sem perda, transparência
- **JPG/JPEG:** Menor tamanho, sem transparência
- **WEBP:** Moderno, menor que JPG, transparência
- **PDF:** Para certificados/documentos

## 🧠 Claude Skill (Automática)

Esta integração tem uma **Claude Skill** que ativa automaticamente quando você pede para criar designs:

```
Usuário: "Crie um post Instagram sobre Claude Code"
Claude: [Skill orshot-design ativa automaticamente]
        → Usa generate_image.py
        → Gera imagem
        → Mostra resultado
```

**Skill:** `.claude/skills/orshot/SKILL.md`

## 🔗 Integrações Disponíveis

### Publicar Automaticamente

```bash
# Gerar + publicar Instagram
python3 scripts/orshot/generate_image.py --template post-ig --title "Novidade"
python3 scripts/instagram/publish_post.py --image orshot_post-ig_Novidade.png

# Gerar + enviar WhatsApp
python3 scripts/orshot/generate_image.py --template promo --title "50% OFF"
python3 scripts/whatsapp/send_media.py --phone 5531999999999 --file promo.png
```

### n8n/Zapier/Make

Orshot tem integrações nativas:
- n8n node oficial
- Zapier integration
- Make (Integromat)
- Airtable

**Docs:** https://orshot.com/docs/integrations

## 🆚 Comparação

### Orshot vs Canva API

| Aspecto | Orshot | Canva API |
|---------|--------|-----------|
| **Preço** | $30/mês = 3.000 renders | $300+/mês (Enterprise) |
| **Setup** | API key simples | OAuth + Enterprise account |
| **Automação** | 100% via API/Python | Limitado (só Autofill) |
| **Templates** | Importa do Canva | Nativo apenas |
| **Custo/render** | $0.01 | Ilimitado* (plano caro) |
| **Free tier** | 100 renders teste | Trial curto |

### Orshot vs Outros

| Serviço | Preço | Renders | Custo/render |
|---------|-------|---------|--------------|
| **Orshot** | $30 | 3.000 | $0.01 ✅ |
| Templated | $29 | 1.000 | $0.029 |
| Placid | $39 | 2.500 | $0.0156 |
| Bannerbear | $49 | 1.000 | $0.049 |
| RenderForm | $19 | 1.000 | $0.019 |

**Melhor custo/benefício:** Orshot 🏆

## 📚 Recursos

- **Documentação oficial:** https://orshot.com/docs
- **SDK Python:** https://pypi.org/project/orshot/
- **API Reference:** https://orshot.com/docs/api-reference
- **Templates:** https://orshot.com/templates
- **Studio (criar customizados):** https://orshot.com/studio
- **Pricing:** https://orshot.com/pricing

## ❓ Troubleshooting

### Erro: "Invalid API Key"
```bash
# Verifique .env
cat .env | grep ORSHOT

# Regenere chave em:
# https://orshot.com/settings/api
```

### Erro: "Template not found"
```bash
# Liste templates disponíveis
python3 scripts/orshot/list_templates.py

# Verifique se ID está correto
```

### Erro: "Missing parameter"
```bash
# Cada template tem parâmetros obrigatórios
# Use --data com todos os campos necessários

# Ver docs do template em:
# https://orshot.com/docs/templates/TEMPLATE_ID
```

### Imagem muito grande
```bash
# Use WebP (menor que PNG)
--format webp

# Ou JPG
--format jpg
```

## 🎓 Tutoriais

### Tutorial 1: Primeiro Design
1. Instale: `pip install orshot pillow`
2. Configure: Adicione ORSHOT_API_KEY no .env
3. Teste: `python3 scripts/orshot/list_templates.py`
4. Gere: `python3 scripts/orshot/generate_image.py --template open-graph-image-1 --title "Teste"`

### Tutorial 2: Certificados em Massa
1. Crie `alunos.csv` com: name,course,date
2. Execute: `python3 scripts/orshot/batch_generate.py --template certificate-1 --data alunos.csv`
3. Veja resultados em: `orshot_batch/`

### Tutorial 3: Template Customizado
1. Acesse: https://orshot.com/studio
2. Crie design ou importe do Canva
3. Parametrize elementos (clique → "Make dynamic")
4. Copie Template ID
5. Use nos scripts com `--template SEU_ID`

---

**Status:** ✅ Pronto para uso
**Última atualização:** 2025-01-11
**Total de templates:** 5+ pré-prontos + ilimitados Studio
