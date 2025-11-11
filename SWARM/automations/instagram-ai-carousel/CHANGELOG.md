# Changelog - Instagram AI Carousel

## v2.0 - Carrossel Artesanal (06/11/2025)

### ✨ Novas Funcionalidades

**Estilo Visual Atualizado:**
- Template de colagem artesanal (papéis à mão, canetinhas coloridas)
- Baseado na skill `carrossel-meta-ads`
- Ícones desenhados à mão gerados via IA
- Visual autêntico e imperfeit o (sombras, fita adesiva, traços tortos)

**Workflow Otimizado:**
- Geração de ícones contextual por slide
- Prompts salvos em JSON estruturado
- Pronto para integração com `batch_carrossel_gpt4o.py`
- 4 variantes por slide (produção)

### 🔧 Estrutura Técnica

**Agentes:**
1. **Agente 1 (Pesquisa)** - OpenRouter Haiku
2. **Agente 2 (Hormozi Copy)** - OpenRouter Haiku
3. **Agente 3 (PDF)** - OpenRouter Haiku
4. **Agente 4 (Ícones)** - OpenRouter Haiku (novo!)
5. **Auto-Healing** - Claude API Sonnet

**Template Visual:**
```
Colagem artesanal em mesa de madeira
├── Papéis coloridos (branco, amarelo, azul-claro)
├── Escrita à mão (canetinhas vermelho, verde, preto, azul)
├── Ícones desenhados contextuais
└── Imperfeições realistas (sombras, fita, traços tortos)
```

### 📊 Outputs

**Arquivos Gerados:**
- `hormozi_[timestamp].json` - Copy completo
- `carrossel_prompts_[timestamp].json` - Prompts para imagens
- `content_[timestamp].pdf` - Guia expandido
- `slide_[timestamp]_[N].txt` - Prompts individuais

**Próximos Passos (Produção):**
```bash
# Gerar imagens reais (4 variantes cada)
python3 scripts/image-generation/batch_carrossel_gpt4o.py \
  --prompts-file output/carrossel_prompts_[timestamp].json \
  --variants 4 \
  --output-dir output/
```

### 🎯 Exemplo de Prompt Gerado

```
Crie uma colagem artesanal e realista feita à mão, com aparência
de trabalho escolar sobre vendas de terrenos.

Fundo de mesa de madeira clara, luz natural suave e papéis colados
com sombras reais e bordas rasgadas.

Use papéis de cores diferentes (branco, amarelo e azul-claro) com
escrita feita à mão em canetinhas de várias cores.

[CONTEÚDO DO SLIDE]

Adicione ícones desenhados à mão: 🧠, 💡, 🤖

Finalize com detalhes de imperfeição realista — sombras, fita
adesiva, traços tortos e variação de espessura da caneta.
```

---

## v1.0 - Workflow Base (06/11/2025)

### Funcionalidades Iniciais

- Workflow completo 5 etapas
- Auto-healing via Claude API
- OpenRouter para agentes
- Retry automático (3x)
- Logs estruturados
- Estado salvo em JSON

---

**Última atualização:** 06/11/2025 00:35
**Status:** ✅ Testado e funcional
**Próximo:** Deploy VPS
