# Orshot - Documentação Técnica

## Capacidades do Orshot

### 1. Templates Pré-Prontos
- Open Graph images (1200x630)
- Tweets/posts sociais (múltiplos tamanhos)
- Screenshots de websites
- Certificados e convites
- Banners e headers

### 2. Templates Customizados (Studio)
- **Importar:** Designs do Canva/Figma
- **Criar:** No Orshot Studio (editor visual)
- **Parametrizar:** Elementos dinâmicos (textos, cores, imagens)
- **Reutilizar:** Mesmos templates com dados diferentes

### 3. Formatos Suportados

**Imagens:**
- PNG (com/sem transparência)
- JPG (compressão configurável)
- WEBP (otimizado para web)

**Documentos:**
- PDF (single-page)
- PDF (multi-page)

### 4. Tipos de Resposta

| Tipo | Uso | Vantagens |
|------|-----|-----------|
| **base64** | Embedding direto em HTML/JSON | Sem arquivos temporários |
| **binary** | Salvar arquivos localmente | Processamento posterior |
| **url** | Link direto hospedado | Compartilhamento fácil |

## Configuração

### Variáveis de Ambiente

```bash
# .env
ORSHOT_API_KEY=os-XXXXXXXXXXXXXXXX
```

### Instalação SDK

```bash
# Instalar via pip
pip install orshot

# Verificar instalação
python3 -c "import orshot; print(orshot.__version__)"
```

### Autenticação

```python
from orshot import OrshotClient

client = OrshotClient(api_key="os-XXXXXXXXXXXXXXXX")
# ou usando .env
client = OrshotClient()  # lê ORSHOT_API_KEY automaticamente
```

## Scripts Disponíveis

### `scripts/orshot/generate_image.py`

Gera imagem única a partir de template.

**Parâmetros:**
- `--template` (obrigatório): ID do template
- `--title`: Título/texto principal
- `--subtitle`: Texto secundário
- `--color`: Cor de destaque (hex)
- `--output`: Nome do arquivo de saída
- `--format`: png|jpg|webp|pdf (padrão: png)
- `--response-type`: base64|binary|url (padrão: binary)

**Exemplo:**
```bash
python3 scripts/orshot/generate_image.py \
  --template "open-graph-image-1" \
  --title "Claude Code: Automação Completa" \
  --subtitle "65+ templates prontos" \
  --color "#FF6B35" \
  --output "og-image.png"
```

### `scripts/orshot/batch_generate.py`

Gera múltiplas imagens de uma vez.

**Parâmetros:**
- `--template` (obrigatório): ID do template
- `--data` (obrigatório): Arquivo JSON com dados
- `--output-dir`: Pasta de saída (padrão: output/)
- `--format`: png|jpg|webp|pdf (padrão: png)

**Formato JSON:**
```json
[
  {
    "title": "Certificado 1",
    "name": "João Silva",
    "date": "15/01/2025"
  },
  {
    "title": "Certificado 2",
    "name": "Maria Santos",
    "date": "15/01/2025"
  }
]
```

**Exemplo:**
```bash
python3 scripts/orshot/batch_generate.py \
  --template "certificado-conclusao" \
  --data "alunos.json" \
  --output-dir "certificados/" \
  --format pdf
```

### `scripts/orshot/list_templates.py`

Lista todos templates disponíveis (pré-prontos + Studio).

**Uso:**
```bash
python3 scripts/orshot/list_templates.py

# Output:
# Templates Pré-Prontos:
#   - open-graph-image-1 (OG Image padrão)
#   - tweet-preview-1 (Tweet com preview)
#   - instagram-post-1 (Post quadrado 1080x1080)
#
# Templates do Studio:
#   - certificado-conclusao (Customizado)
#   - convite-evento (Customizado)
```

## Comparação: Orshot vs Canva

| Aspecto | Orshot | Canva API |
|---------|--------|-----------|
| **Preço** | $30/mês = 3.000 renders | $300+/mês (Enterprise) |
| **Custo/render** | $0.01 | Incluído (mas plano caro) |
| **Setup** | API key simples | OAuth complexo + aprovação |
| **Automação** | 100% via API | Limitado |
| **Templates** | Importa do Canva/Figma | Nativo apenas |
| **Teste grátis** | 100 renders | Não disponível |
| **Formatos** | PNG, JPG, WEBP, PDF | PNG, JPG, PDF |

**Veredito:** Orshot é 3x mais barato e muito mais fácil de integrar.

## Integração com Outros Sistemas

### Instagram API
```bash
# Gerar post + publicar automaticamente
python3 scripts/orshot/generate_image.py --template "instagram-post-1" --title "Novo Post" --output "post.png"
python3 scripts/instagram/publish_post.py --image "post.png" --caption "Legenda"
```

### WhatsApp (Evolution API)
```bash
# Gerar imagem + enviar
python3 scripts/orshot/generate_image.py --template "promocao" --output "promo.png"
python3 scripts/whatsapp/send_media.py --phone 5531980160822 --file "promo.png" --type image
```

### Obsidian
```bash
# Gerar e anexar em note
python3 scripts/orshot/generate_image.py --template "og-image-1" --output "~/Obsidian/Assets/cover.png"
python3 scripts/obsidian/quick_note.py --title "Projeto X" --image "cover.png"
```

### Email/Newsletter
```python
# Gerar header + enviar email
from orshot import OrshotClient

client = OrshotClient()
image_url = client.render(template="newsletter-header", response_type="url")

# Usar image_url no HTML do email
```

## Recursos Oficiais

- **Documentação:** https://orshot.com/docs
- **SDK Python:** https://pypi.org/project/orshot/
- **Templates:** https://orshot.com/templates
- **Studio:** https://orshot.com/studio (criar customizados)
- **Dashboard:** https://orshot.com/dashboard (uso e billing)
- **Support:** support@orshot.com

## Limites e Pricing

### Plano Free
- 100 renders grátis (teste)
- Todos templates pré-prontos
- API completa

### Plano Paid ($30/mês)
- 3.000 renders incluídos
- $0.01 por render adicional
- Templates customizados ilimitados (Studio)
- Suporte prioritário

### Rate Limits
- 100 requisições/minuto
- 10.000 requisições/dia
- Response time: ~2-5 segundos/imagem

## Modificações Avançadas

### Parametrização Complexa

```python
from orshot import OrshotClient

client = OrshotClient()

modifications = {
    "texts": {
        "title": "Título Customizado",
        "subtitle": "Subtítulo",
        "footer": "rodapé"
    },
    "colors": {
        "primary": "#FF6B35",
        "secondary": "#004E89",
        "background": "#F7F7F7"
    },
    "images": {
        "logo": "https://example.com/logo.png",
        "background": "https://example.com/bg.jpg"
    }
}

result = client.render(
    template="custom-template-id",
    modifications=modifications,
    format="png",
    response_type="binary"
)

with open("output.png", "wb") as f:
    f.write(result)
```

### Criando Template no Studio

1. Acesse https://orshot.com/studio
2. Importe design (Canva/Figma) ou crie do zero
3. Marque elementos dinâmicos:
   - Clique no elemento
   - "Make Dynamic"
   - Defina nome da variável
4. Salve template
5. Copie template_id
6. Use na API com modifications

## Performance

### Otimizações

- **Cache:** Orshot cacheia renders idênticos
- **CDN:** URLs hospedadas em CDN global
- **Async:** Use `batch_generate.py` para múltiplas imagens
- **Formatos:** WEBP = menor tamanho, PNG = melhor qualidade

### Benchmarks

| Operação | Tempo Médio |
|----------|-------------|
| Render simples (OG image) | 2-3s |
| Render complexo (multi-layer) | 4-6s |
| Batch 10 imagens | 15-20s |
| Batch 100 imagens | 2-3min |
