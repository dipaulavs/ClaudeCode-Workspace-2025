# Orshot - Solução de Problemas

## Erro: "Invalid API Key"

### Sintoma
```
Error: Invalid API key provided
Status: 401 Unauthorized
```

### Causas Possíveis
1. API key incorreta ou expirada
2. Variável de ambiente não configurada
3. Typo no arquivo `.env`

### Soluções

**1. Verificar variável de ambiente:**
```bash
# Ver se está configurada
echo $ORSHOT_API_KEY

# Se vazio, verificar .env
cat .env | grep ORSHOT_API_KEY
```

**2. Regenerar chave:**
1. Acesse https://orshot.com/settings/api
2. Clique em "Regenerate API Key"
3. Copie a nova chave
4. Atualize no `.env`:
```bash
ORSHOT_API_KEY=os-NOVA_CHAVE_AQUI
```

**3. Testar autenticação:**
```bash
python3 scripts/orshot/list_templates.py
# Se funcionar, API key está OK
```

---

## Erro: "Template not found"

### Sintoma
```
Error: Template 'meu-template' does not exist
Status: 404 Not Found
```

### Causas Possíveis
1. Template ID incorreto (typo)
2. Template não existe (nem pré-pronto nem Studio)
3. Template foi deletado

### Soluções

**1. Listar templates disponíveis:**
```bash
python3 scripts/orshot/list_templates.py

# Output mostra todos IDs válidos:
# - open-graph-image-1
# - tweet-preview-1
# - instagram-post-1
# - certificado-conclusao (Studio)
```

**2. Verificar no Dashboard:**
- Acesse https://orshot.com/dashboard
- Aba "Templates"
- Confirme que o template existe

**3. Verificar typos comuns:**
```bash
# Errado:
--template "og-image"  # Não existe

# Certo:
--template "open-graph-image-1"
```

**4. Template customizado não aparece?**
- Verifique se foi salvo corretamente no Studio
- Espere ~30s para propagação
- Refresque cache: `python3 scripts/orshot/list_templates.py --refresh`

---

## Erro: "Missing parameter"

### Sintoma
```
Error: Required parameter 'title' is missing
Status: 400 Bad Request
```

### Causas Possíveis
1. Parâmetro obrigatório não fornecido
2. Template customizado requer campos específicos
3. Modificações incorretas no JSON

### Soluções

**1. Ver documentação do template:**
```bash
# Cada template tem modificações obrigatórias
# Consulte: https://orshot.com/templates/[template-id]
```

**2. Exemplo de modificações completas:**
```bash
# Template 'open-graph-image-1' requer:
python3 scripts/orshot/generate_image.py \
  --template "open-graph-image-1" \
  --title "Título obrigatório" \  # REQUIRED
  --subtitle "Opcional" \
  --color "#FF6B35" \
  --output "result.png"
```

**3. Para templates customizados:**
```python
# Verificar no Studio quais campos são obrigatórios
# Campos marcados com * são required

modifications = {
    "title": "...",      # Se tiver * no Studio
    "subtitle": "...",   # Opcional
    "author": "..."      # Se tiver * no Studio
}
```

**4. Testar com mínimo obrigatório:**
```bash
# Teste básico
python3 scripts/orshot/generate_image.py \
  --template "seu-template" \
  --title "Teste" \
  --output "test.png"

# Se funcionar, adicione campos opcionais gradualmente
```

---

## Erro: "Rate limit exceeded"

### Sintoma
```
Error: Rate limit exceeded. Try again in 45 seconds.
Status: 429 Too Many Requests
```

### Causas Possíveis
1. Mais de 100 requisições/minuto
2. Mais de 10.000 requisições/dia
3. Batch muito grande sem delay

### Soluções

**1. Adicionar delay entre requests:**
```bash
# Para batch grande, use --delay
python3 scripts/orshot/batch_generate.py \
  --template "certificado" \
  --data "1000_alunos.json" \
  --output-dir "certificados/" \
  --delay 0.6  # 600ms entre cada request
```

**2. Dividir batches:**
```bash
# Em vez de 1000 de uma vez:
# Batch 1: 0-500
python3 scripts/orshot/batch_generate.py --data "alunos_1_500.json"

# Aguardar 1 minuto

# Batch 2: 501-1000
python3 scripts/orshot/batch_generate.py --data "alunos_501_1000.json"
```

**3. Verificar limites no dashboard:**
- Acesse https://orshot.com/dashboard/usage
- Veja consumo atual
- Aguarde reset (mostrado no dashboard)

**4. Implementar retry automático:**
```python
import time
from orshot import OrshotClient

client = OrshotClient()

def render_with_retry(template, mods, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.render(template, mods)
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                wait_time = 60 * (attempt + 1)
                print(f"Rate limit. Aguardando {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
```

---

## Erro: "Render timeout"

### Sintoma
```
Error: Render operation timed out after 30 seconds
Status: 504 Gateway Timeout
```

### Causas Possíveis
1. Template muito complexo
2. Muitas camadas/imagens de alta resolução
3. Servidor sobrecarregado

### Soluções

**1. Simplificar template:**
- Reduza número de camadas
- Use imagens otimizadas (não RAW)
- Evite muitos efeitos (sombras, blur)

**2. Aumentar timeout no código:**
```python
from orshot import OrshotClient

client = OrshotClient(timeout=60)  # 60 segundos
```

**3. Testar em horários diferentes:**
- Evite horários de pico (9h-18h UTC-5)
- Tente madrugada/final de semana

**4. Usar formato mais simples:**
```bash
# Em vez de PDF multi-page:
--format png  # Mais rápido

# Em vez de alta resolução:
--width 1200  # Em vez de 4K
```

---

## Erro: "Invalid image URL"

### Sintoma
```
Error: Could not fetch image from URL
Status: 400 Bad Request
```

### Causas Possíveis
1. URL da imagem inacessível
2. Formato de imagem não suportado
3. URL requer autenticação

### Soluções

**1. Verificar URL:**
```bash
# Testar download manual
curl -I https://example.com/image.jpg

# Deve retornar 200 OK
# Content-Type: image/jpeg
```

**2. Formatos suportados:**
- ✅ JPG/JPEG
- ✅ PNG
- ✅ WEBP
- ✅ SVG
- ❌ GIF animado (use apenas primeiro frame)
- ❌ TIFF, BMP (converta antes)

**3. Usar URLs públicas:**
```bash
# ❌ Não funciona (autenticação):
https://drive.google.com/file/d/ABC123/view

# ✅ Funciona:
https://i.imgur.com/ABC123.jpg
https://example.com/public/image.png
```

**4. Upload local primeiro:**
```bash
# Se imagem está local, use base64:
python3 scripts/orshot/generate_image.py \
  --template "custom" \
  --image-file "/caminho/local/logo.png" \  # Em vez de URL
  --output "result.png"
```

---

## Erro: "Insufficient credits"

### Sintoma
```
Error: Insufficient credits. Current: 0, Required: 1
Status: 402 Payment Required
```

### Causas Possíveis
1. Plano gratuito esgotado (100 renders)
2. Plano pago esgotou créditos do mês
3. Pagamento pendente

### Soluções

**1. Verificar saldo:**
- Acesse https://orshot.com/dashboard/billing
- Veja "Credits Remaining"
- Veja "Next Reset" (data de renovação)

**2. Upgrade de plano:**
```
Free → Paid ($30/mês)
- 100 renders → 3.000 renders
- Aguardar aprovação pagamento (~5min)
```

**3. Comprar créditos avulsos:**
- Dashboard → Billing → "Buy Credits"
- $0.01 por render adicional

**4. Aguardar renovação mensal:**
- Planos resetam no dia 1º de cada mês
- Ou na data de aniversário da assinatura

---

## Erro: "File write permission denied"

### Sintoma
```
PermissionError: [Errno 13] Permission denied: 'output/result.png'
```

### Causas Possíveis
1. Pasta de output não existe
2. Sem permissão de escrita na pasta
3. Arquivo já aberto em outro programa

### Soluções

**1. Criar pasta de output:**
```bash
mkdir -p output/
chmod 755 output/
```

**2. Usar caminho absoluto:**
```bash
python3 scripts/orshot/generate_image.py \
  --template "og-image-1" \
  --output "/Users/user/Desktop/result.png"  # Caminho completo
```

**3. Verificar permissões:**
```bash
ls -la output/
# Se não tiver 'w' (write), corrigir:
chmod 755 output/
```

**4. Fechar arquivo se estiver aberto:**
- Feche Preview/Photoshop/etc
- Tente novamente

---

## Problema: Imagem com qualidade ruim

### Sintoma
Imagem gerada está pixelada ou com cores estranhas.

### Soluções

**1. Usar formato adequado:**
```bash
# Para texto/logos (sem degradê):
--format png

# Para fotos:
--format jpg --quality 90

# Para web (otimizado):
--format webp
```

**2. Aumentar resolução:**
```bash
python3 scripts/orshot/generate_image.py \
  --template "instagram-post-1" \
  --width 2160 \  # 2x resolução (1080 padrão)
  --height 2160 \
  --output "post-hd.png"
```

**3. Verificar template:**
- Templates com muitos efeitos podem pixelar
- Use templates simples para melhor qualidade
- Evite stretch (manter proporções originais)

---

## Suporte Adicional

### Documentação Oficial
- **Docs:** https://orshot.com/docs
- **API Reference:** https://orshot.com/docs/api
- **Status:** https://status.orshot.com

### Contato
- **Email:** support@orshot.com
- **Discord:** https://discord.gg/orshot
- **Twitter:** @OrshotAPI

### Logs Úteis

```bash
# Ver logs detalhados
python3 scripts/orshot/generate_image.py --debug --verbose

# Testar conexão
curl -H "Authorization: Bearer $ORSHOT_API_KEY" https://api.orshot.com/v1/templates

# Verificar versão SDK
pip show orshot
```
