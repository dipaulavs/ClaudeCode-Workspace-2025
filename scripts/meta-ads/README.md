# 🎯 Templates Meta Ads

Scripts templates reutilizáveis para automação Meta Ads via CLI.

## 📋 Templates Disponíveis

| Template | Funcionalidade | Status |
|----------|----------------|--------|
| `create_campaign.py` | Criar campanha | ✅ Pronto |
| `create_adset.py` | Criar ad set | ✅ Pronto |
| `create_ad.py` | Criar anúncio completo | ✅ Pronto |
| `get_insights.py` | Obter métricas | ✅ Pronto |

## 🚀 Quick Start

### 1. Criar Campanha
```bash
python3 scripts/meta-ads/create_campaign.py --name "Minha Campanha" --objective OUTCOME_TRAFFIC
```

### 2. Criar Ad Set
```bash
python3 scripts/meta-ads/create_adset.py --campaign-id 123456789 --name "Ad Set Brasil"
```

### 3. Criar Anúncio
```bash
python3 scripts/meta-ads/create_ad.py --adset-id 987654321 --name "Anúncio Casa" --message "Casa linda!" --link "https://site.com" --image "foto.jpg"
```

### 4. Obter Métricas
```bash
python3 scripts/meta-ads/get_insights.py --id 123456789 --level campaign
```

---

## 📚 Documentação Detalhada

### create_campaign.py

Cria campanha Meta Ads de forma simplificada.

**Argumentos obrigatórios:**
- `--name` / `-n`: Nome da campanha
- `--objective` / `-o`: Objetivo da campanha

**Argumentos opcionais:**
- `--daily-budget` / `-d`: Orçamento diário em USD (padrão: 10.0)
- `--status` / `-s`: Status (ACTIVE, PAUSED - padrão: PAUSED)
- `--special-category` / `-c`: Categoria especial (HOUSING, CREDIT, EMPLOYMENT, NONE - padrão: NONE)

**Objetivos disponíveis:**
- `OUTCOME_TRAFFIC`: Gerar tráfego
- `OUTCOME_LEADS`: Gerar leads
- `OUTCOME_SALES`: Gerar vendas
- `OUTCOME_AWARENESS`: Gerar reconhecimento
- `OUTCOME_ENGAGEMENT`: Gerar engajamento

**Exemplos:**
```bash
# Campanha básica (pausada, $10/dia)
python3 scripts/meta-ads/create_campaign.py -n "Campanha Teste" -o OUTCOME_TRAFFIC

# Campanha com orçamento customizado
python3 scripts/meta-ads/create_campaign.py -n "Black Friday" -o OUTCOME_SALES -d 50.0

# Campanha para imóveis (HOUSING)
python3 scripts/meta-ads/create_campaign.py -n "Venda Casa" -o OUTCOME_LEADS -c HOUSING

# Campanha ativa imediatamente
python3 scripts/meta-ads/create_campaign.py -n "Lançamento" -o OUTCOME_TRAFFIC -s ACTIVE
```

**Output esperado:**
```
📢 Criando campanha 'Minha Campanha' [HOUSING]...
   Objetivo: OUTCOME_LEADS
   Orçamento: $15.0/dia
   Status: PAUSED

✅ Campanha criada com sucesso!
   Campaign ID: 123456789
   Nome: Minha Campanha
   Status: PAUSED

💡 Para ativar: python3 tools/meta_ads_campaigns.py update 123456789 --status ACTIVE
```

---

### create_adset.py

Cria ad set com targeting básico.

**Argumentos obrigatórios:**
- `--campaign-id` / `-c`: ID da campanha pai
- `--name` / `-n`: Nome do ad set

**Argumentos opcionais:**
- `--daily-budget` / `-d`: Orçamento diário em USD (usar se campanha não tiver orçamento)
- `--optimization-goal` / `-g`: Meta de otimização (padrão: LINK_CLICKS)
- `--country` / `-co`: País de targeting (padrão: BR)
- `--age-min` / `-amin`: Idade mínima (padrão: 25)
- `--age-max` / `-amax`: Idade máxima (padrão: 55)
- `--status` / `-s`: Status (padrão: PAUSED)

**Metas de otimização:**
- `LINK_CLICKS`: Cliques no link
- `IMPRESSIONS`: Impressões
- `REACH`: Alcance
- `LANDING_PAGE_VIEWS`: Visualizações da página

**Exemplos:**
```bash
# Ad set básico (orçamento da campanha)
python3 scripts/meta-ads/create_adset.py -c 123456789 -n "Ad Set Brasil"

# Ad set com orçamento próprio
python3 scripts/meta-ads/create_adset.py -c 123456789 -n "Ad Set SP" -d 20.0

# Ad set com targeting customizado
python3 scripts/meta-ads/create_adset.py -c 123456789 -n "Ad Set 30-60" -amin 30 -amax 60

# Ad set para EUA
python3 scripts/meta-ads/create_adset.py -c 123456789 -n "Ad Set USA" -co US

# Ad set otimizado para alcance
python3 scripts/meta-ads/create_adset.py -c 123456789 -n "Ad Set Reach" -g REACH
```

**Output esperado:**
```
🎯 Criando ad set 'Ad Set Brasil'...
   Campaign ID: 123456789
   Targeting: BR, 25-55 anos
   Orçamento: Orçamento da campanha
   Status: PAUSED

✅ Ad set criado com sucesso!
   Ad Set ID: 987654321
   Nome: Ad Set Brasil
   Status: PAUSED

💡 Próximo passo: Criar anúncio com python3 scripts/meta-ads/create_ad.py --adset-id 987654321
```

---

### create_ad.py

Cria anúncio completo (upload imagem + criativo + ad).

**Argumentos obrigatórios:**
- `--adset-id` / `-a`: ID do ad set pai
- `--name` / `-n`: Nome do anúncio
- `--message` / `-m`: Texto do anúncio
- `--link` / `-l`: URL de destino
- `--image` / `-i`: Caminho da imagem

**Argumentos opcionais:**
- `--cta` / `-c`: Call to action (padrão: LEARN_MORE)
- `--status` / `-s`: Status (padrão: PAUSED)

**CTAs disponíveis:**
- `LEARN_MORE`: Saiba mais
- `SHOP_NOW`: Compre agora
- `SIGN_UP`: Inscreva-se
- `DOWNLOAD`: Baixar
- `GET_QUOTE`: Solicitar orçamento
- `CONTACT_US`: Entre em contato
- `APPLY_NOW`: Candidate-se

**Exemplos:**
```bash
# Anúncio básico
python3 scripts/meta-ads/create_ad.py \
  -a 987654321 \
  -n "Anúncio Casa Centro" \
  -m "Casa linda de 3 quartos no centro!" \
  -l "https://lfimoveis.com.br/casa" \
  -i "casa.jpg"

# Anúncio com CTA "Compre agora"
python3 scripts/meta-ads/create_ad.py \
  -a 987 -n "Ad Promoção" \
  -m "50% OFF!" \
  -l "https://loja.com" \
  -i "promo.jpg" \
  -c SHOP_NOW

# Anúncio ativo imediatamente
python3 scripts/meta-ads/create_ad.py \
  -a 987 -n "Ad Casa" \
  -m "Conheça!" \
  -l "https://site.com" \
  -i "casa.jpg" \
  -s ACTIVE
```

**Output esperado:**
```
📢 Criando anúncio 'Anúncio Casa Centro'...
   Ad Set ID: 987654321
   Mensagem: Casa linda de 3 quartos no centro!
   Link: https://lfimoveis.com.br/casa
   Imagem: casa.jpg
   CTA: LEARN_MORE
   📤 Fazendo upload da imagem...
   🎨 Criando criativo...
   📢 Criando anúncio...

✅ Anúncio criado com sucesso!
   Ad ID: 111222333
   Creative ID: 444555666
   Image Hash: abc123xyz...
   Status: PAUSED

💡 Para ativar: python3 tools/meta_ads_ads.py update 111222333 --status ACTIVE
```

---

### get_insights.py

Obtém métricas de campanhas, ad sets ou anúncios.

**Argumentos obrigatórios:**
- `--id` / `-i`: ID do objeto (campanha/adset/ad)
- `--level` / `-l`: Nível (campaign, adset, ad)

**Argumentos opcionais:**
- `--period` / `-p`: Período (padrão: last_7d)
- `--breakdown` / `-b`: Dimensão para quebra (opcional)
- `--export` / `-e`: Nome do arquivo para exportar (opcional)

**Períodos disponíveis:**
- `today`: Hoje
- `yesterday`: Ontem
- `last_7d`: Últimos 7 dias
- `last_30d`: Últimos 30 dias
- `lifetime`: Desde o início

**Breakdowns disponíveis:**
- `age`: Por faixa etária
- `gender`: Por gênero
- `country`: Por país
- `region`: Por região
- `placement`: Por posicionamento

**Exemplos:**
```bash
# Métricas de campanha (últimos 7 dias)
python3 scripts/meta-ads/get_insights.py -i 123456789 -l campaign

# Métricas de adset (últimos 30 dias)
python3 scripts/meta-ads/get_insights.py -i 987654321 -l adset -p last_30d

# Métricas com exportação
python3 scripts/meta-ads/get_insights.py -i 123 -l campaign -e relatorio.json

# Métricas por idade
python3 scripts/meta-ads/get_insights.py -i 123 -l ad -b age

# Métricas de hoje por país
python3 scripts/meta-ads/get_insights.py -i 456 -l campaign -p today -b country
```

**Output esperado:**
```
📊 Buscando métricas por age...
   ID: 123456789
   Nível: campaign
   Período: last_7d

✅ Métricas obtidas com sucesso!
   Total de registros: 3

   📈 Registro 1:
      Impressões: 15234
      Cliques: 456
      Alcance: 12000
      Gasto: $45.67
      CPC: $0.10
      CTR: 2.99%

   📈 Registro 2:
      ...

💾 Dados exportados para: relatorio.json
```

---

## 🔄 Workflow Completo

**Criar campanha completa do zero:**

```bash
# 1. Criar campanha
python3 scripts/meta-ads/create_campaign.py \
  -n "Campanha Imóveis BH" \
  -o OUTCOME_LEADS \
  -d 30.0 \
  -c HOUSING
# Output: Campaign ID: 123456789

# 2. Criar ad set
python3 scripts/meta-ads/create_adset.py \
  -c 123456789 \
  -n "Ad Set BH 30-60" \
  -amin 30 \
  -amax 60
# Output: Ad Set ID: 987654321

# 3. Criar anúncio
python3 scripts/meta-ads/create_ad.py \
  -a 987654321 \
  -n "Anúncio Casa Luxo" \
  -m "Casa de luxo com piscina em BH!" \
  -l "https://lfimoveis.com.br/casa123" \
  -i "casa_luxo.jpg" \
  -c GET_QUOTE
# Output: Ad ID: 111222333

# 4. Ativar campanha
python3 tools/meta_ads_campaigns.py update 123456789 --status ACTIVE

# 5. Monitorar performance
python3 scripts/meta-ads/get_insights.py -i 123456789 -l campaign -p today
```

---

## 🛠️ Requisitos

### Configuração:
- Access Token válido em `config/meta_ads_config.py`
- Ad Account ID configurado
- Page ID configurado

### Dependências:
- Python 3.9+
- requests
- tools/meta_ads_*.py (ferramentas base)

---

## ⚠️ Notas Importantes

### Special Ad Categories:
- **HOUSING/CREDIT/EMPLOYMENT**: NÃO suportam targeting por raio (custom_locations)
- Para usar raio geográfico, use `--special-category NONE`
- Para essas categorias, use targeting por cidade/país completo

### Orçamento:
- Pode ser definido na **campanha** OU no **ad set**, não em ambos
- Se campanha tiver orçamento, ad set não deve ter
- Valores são em USD, convertidos automaticamente para centavos

### Status:
- Todos os templates criam objetos com `status=PAUSED` por segurança
- Use `--status ACTIVE` para criar já ativo
- Ou use ferramentas em `tools/` para ativar depois

### Imagens:
- Formatos suportados: JPG, PNG
- Tamanho recomendado: 1200x628px (proporção 1.91:1)
- Peso máximo: 30MB

---

## 📞 Suporte

**Ferramentas base (CRUD completo):**
- `tools/meta_ads_campaigns.py` (list, create, update, delete)
- `tools/meta_ads_adsets.py` (list, create, update)
- `tools/meta_ads_ads.py` (list, create, update)
- `tools/meta_ads_creatives.py` (list, create)
- `tools/meta_ads_insights.py` (get, export)
- `tools/meta_ads_upload_image.py` (upload)

**Documentação:**
- Meta Ads API: `docs/meta-ads-api/META_ADS_API_DOCUMENTATION.md`
- Configuração: `config/meta_ads_config.py`

**Última atualização:** 2025-11-01
