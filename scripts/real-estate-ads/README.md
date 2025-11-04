# 🏠 Real Estate Ads - Gerador de Criativos para Imóveis

Gera criativos profissionais para anúncios de imóveis no Instagram/Meta Ads usando Nano Banana Edit (Gemini 2.5 Flash).

## 📋 O Que Faz

Transforma fotos de imóveis em criativos persuasivos para Meta Ads/Instagram com:
- ✅ Hooks chamativos (texto sobreposto)
- ✅ Aspect ratio otimizado (4:5 Feed, 9:16 Stories)
- ✅ Processamento paralelo (múltiplos criativos simultâneos)
- ✅ Design profissional automático

## 🚀 Como Usar

### Uso Básico (4 criativos para Feed)

```bash
python3 scripts/real-estate-ads/generate_ads_images.py \
  --image-url "https://media.loop9.com.br/s/ABC123/imovel.jpg" \
  "Casa com 3 quartos, piscina e área gourmet. OPORTUNIDADE ÚNICA!" \
  "Localização privilegiada! Próximo a tudo que você precisa." \
  "Investimento certeiro: chácara com potencial de valorização." \
  "Não perca! Casa dos sonhos com preço especial."
```

### Stories (9:16)

```bash
python3 scripts/real-estate-ads/generate_ads_images.py \
  --image-url "https://exemplo.com/imovel.jpg" \
  --size 9:16 \
  "Hook 1..." "Hook 2..."
```

### Formato JPEG

```bash
python3 scripts/real-estate-ads/generate_ads_images.py \
  --image-url "https://exemplo.com/imovel.jpg" \
  --format JPEG \
  "Hook 1..." "Hook 2..."
```

## 📐 Parâmetros

| Parâmetro | Descrição | Padrão |
|-----------|-----------|--------|
| `--image-url` `-u` | URL pública da foto do imóvel (obrigatório) | - |
| `--format` `-f` | Formato: PNG ou JPEG | PNG |
| `--size` `-s` | Proporção: 4:5 (Feed) ou 9:16 (Stories) | 4:5 |
| `prompts` | Lista de prompts com hooks (um por criativo) | - |

## 🎯 Aspect Ratios Disponíveis

| Formato | Uso | Dimensões |
|---------|-----|-----------|
| **4:5** | Instagram Feed (padrão) | 1080x1350 |
| **9:16** | Instagram Stories/Reels | 1080x1920 |

## ⚡ Performance

- **Tempo médio:** ~90s para 4 criativos
- **Processamento:** Paralelo (todos ao mesmo tempo)
- **Modelo:** Gemini 2.5 Flash (Nano Banana Edit)
- **Custo:** ~$0.03 por criativo

## 📂 Output

Imagens salvas em: `~/Downloads`

Nomenclatura: `ad_realestate_[prompt]_[timestamp].png`

Cada resultado inclui:
- 📁 Path local do arquivo
- 🔗 URL pública temporária

## 🧠 Integração com Hormozi-Leads

**Workflow recomendado:**

1. **Gerar hooks** com skill `hormozi-leads`:
   ```
   Input: Dados do imóvel (tipo, pontos fortes, localização)
   Output: 7 hooks persuasivos
   ```

2. **Selecionar 4 melhores hooks**

3. **Gerar criativos** com este script:
   ```bash
   python3 scripts/real-estate-ads/generate_ads_images.py \
     --image-url "[URL_DO_IMOVEL]" \
     "[HOOK_1]" "[HOOK_2]" "[HOOK_3]" "[HOOK_4]"
   ```

## 💡 Dicas para Hooks Eficazes

### ✅ FAZER:
- Usar urgência: "ÚLTIMA UNIDADE", "OFERTA LIMITADA"
- Destacar benefícios: "3 QUARTOS + PISCINA"
- Localização: "BAIRRO NOBRE", "PRÓXIMO AO SHOPPING"
- Números específicos: "R$ 450MIL", "200m²"
- CTA forte: "AGENDE SUA VISITA", "FALE AGORA"

### ❌ EVITAR:
- Textos longos (máx 2-3 linhas)
- Genérico: "Linda casa" → "Casa com área gourmet completa"
- Sem urgência/escassez
- Informações técnicas excessivas

## 🛠️ Estrutura Técnica

```
scripts/real-estate-ads/
├── generate_ads_images.py    # Wrapper simplificado (use este)
└── README.md                  # Este arquivo

tools/
└── batch_edit_ads_portrait.py # Script low-level (paralelo)
```

## 📚 Exemplos Reais

### Exemplo 1: Casa com Piscina (Feed 4:5)

```bash
python3 scripts/real-estate-ads/generate_ads_images.py \
  --image-url "https://exemplo.com/casa1.jpg" \
  "🏡 CASA DOS SONHOS | 3 quartos + piscina | Bairro Nobre" \
  "OPORTUNIDADE ÚNICA! Casa completa com área gourmet" \
  "LOCALIZAÇÃO PRIVILEGIADA | Próximo a tudo" \
  "AGENDE SUA VISITA | Fale agora: (31) 98016-0822"
```

### Exemplo 2: Chácara (Stories 9:16)

```bash
python3 scripts/real-estate-ads/generate_ads_images.py \
  --image-url "https://exemplo.com/chacara.jpg" \
  --size 9:16 \
  "🌳 CHÁCARA 5.000m² | Potencial de valorização" \
  "INVISTA CERTO | Localização estratégica"
```

### Exemplo 3: Apartamento (JPEG)

```bash
python3 scripts/real-estate-ads/generate_ads_images.py \
  --image-url "https://exemplo.com/apto.jpg" \
  --format JPEG \
  "🏢 APARTAMENTO NOVO | 2 quartos | Entrega 2025" \
  "ÚLTIMA UNIDADE | Financiamento facilitado" \
  "BAIRRO NOBRE | Vista panorâmica" \
  "FALE AGORA | (31) 98016-0822"
```

## 🔗 Recursos Relacionados

- **Skill hormozi-leads:** Gera hooks persuasivos (Core Four + Lead Getters)
- **Instagram API:** `scripts/instagram/publish_post.py` (publicar criativos)
- **Meta Ads API:** `scripts/meta-ads/create_ad.py` (criar anúncios)
- **Nextcloud Upload:** Caso precise hospedar fotos de imóveis

## ⚙️ Dependências

- Python 3.7+
- Requests
- Kie.ai API (Nano Banana)

## 📝 Notas Importantes

1. **URL pública obrigatória:** A foto do imóvel DEVE estar em URL pública acessível
2. **Aspect ratio correto:** Use 4:5 para Feed, 9:16 para Stories
3. **Qualidade da foto:** Melhor foto = melhor resultado
4. **Hooks curtos:** Máx 2-3 linhas por criativo (legibilidade)
5. **Testes A/B:** Gere 4 variações e teste performance

## 🆘 Troubleshooting

**Erro: "No image URL"**
- Verifique se a URL da foto está acessível publicamente
- Use Nextcloud upload se necessário: `scripts/nextcloud/upload_from_downloads.py`

**Timeout:**
- Normal em APIs congestionadas
- Script reprocessa automaticamente

**Imagem cortada:**
- Verifique aspect ratio da foto original
- Use 4:5 para fotos verticais/quadradas
- Use 9:16 para fotos muito verticais

## 🚧 Próximas Features (Planejado)

- [ ] Geração automática de carrossel (múltiplas fotos do imóvel)
- [ ] Integração direta com hormozi-leads (workflow único)
- [ ] Áudio blogueira (ElevenLabs TTS) para vídeos
- [ ] Templates pré-definidos (moderno, clássico, luxo)
- [ ] Skill completa `real-estate-ads-creator`

---

**Última atualização:** 2025-11-03
**Versão:** 1.0
