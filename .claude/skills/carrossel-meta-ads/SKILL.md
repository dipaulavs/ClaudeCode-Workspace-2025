# Carrossel Meta Ads Creator

Cria carrosséis completos para Meta Ads (nicho imóveis) com copy persuasiva + imagens artesanais.

## Quando Usar

- Usuário pede "criar carrossel Meta Ads"
- Usuário fornece dados de imóvel para anunciar
- Usuário quer gerar anúncios de carrossel para Instagram/Facebook

## Workflow Completo

### 1. Coleta de Dados

Pergunte ao usuário:
- Tipo do imóvel (ex: "Chácara 1.000m²")
- Preço total
- Entrada
- Valor da parcela mensal
- Número de parcelas
- Localização
- **Foto do imóvel (opcional):**
  - Se usuário tem foto, sugira: "Coloque a imagem em `~/Pictures/upload/` e eu faço o upload automático"
  - Execute: `python3 scripts/nextcloud/upload_rapido.py --from-local`
  - Use a URL permanente retornada

### 2. Geração de Copy (Subagente)

Use **Task tool** com `subagent_type: "general-purpose"`:

**Prompt para o subagente:**
```
Analise os exemplos de carrosséis Hormozi em REFERENCE.md desta skill.

Dados do imóvel:
[DADOS_COLETADOS]

Crie 3 opções de carrossel (slides variáveis):
1. Carrossel longo (8-10 slides) - Matemática brutal
2. Carrossel médio (5-7 slides) - Objeção principal
3. Carrossel curto (3-4 slides) - Urgência/escassez

Para cada carrossel, retorne:
- Número de slides
- Copy de cada slide (texto exato a aparecer)
- Estrutura: Hook → Credibilidade → Problema → Solução → CTA

Use metodologia Hormozi (100M Offers + 100M Leads).
```

**SEMPRE mostre automaticamente a Opção 1 COMPLETA** (todos os slides com copy detalhada).

Depois mostre **resumo rápido** das Opções 2 e 3 (só título + número de slides + estratégia em 1 linha).

Pergunte: "Aprova Opção 1?" ou "Quer ver Opção 2/3 completas?"

Se usuário pedir detalhes de 2 ou 3, aí mostre completa.

Se usuário rejeitar todas, peça feedback e repita com ajustes.

### 3. Geração de Prompts de Imagem (Subagente)

Use **Task tool** com `subagent_type: "general-purpose"`:

**Prompt para o subagente:**
```
Copy aprovada:
[COPY_ESCOLHIDA]

Template visual fixo (SEMPRE usar):
"Crie uma colagem artesanal e realista feita à mão, com aparência de trabalho escolar sobre vendas de terrenos.

Fundo de mesa de madeira clara, luz natural suave e papéis colados com sombras reais e bordas rasgadas.

Use papéis de cores diferentes (branco, amarelo e azul-claro) com escrita feita à mão em canetinhas de várias cores (vermelho, verde, preto e azul).

{CONTEUDO_DO_SLIDE}

Adicione ícones desenhados à mão: {ICONES_SUGERIDOS}

Finalize com detalhes de imperfeição realista — sombras, fita adesiva segurando o papel, traços tortos e variação de espessura da caneta, mantendo o ar de colagem artesanal autêntica."

Para cada slide da copy, gere:
1. {CONTEUDO_DO_SLIDE} - Copy formatada para visual
2. {ICONES_SUGERIDOS} - Ícones relevantes

Retorne lista estruturada:
[
  {"slide": 1, "conteudo": "...", "icones": "..."},
  {"slide": 2, "conteudo": "...", "icones": "..."},
  ...
]
```

### 4. Geração de Imagens

**IMPORTANTE:** Slide 1 (capa) será gerado em 2 versões:
- **Template 1:** Divisão Vertical (foto esquerda + texto direita)
- **Template 2:** Colagem Vertical (textos em cima + foto embaixo)

Salve os prompts em arquivo JSON temporário:
```bash
~/Downloads/carrossel_prompts_[timestamp].json
```

Execute o gerador modificado:
```bash
python3 scripts/image-generation/batch_carrossel_gpt4o.py \
  --prompts-file ~/Downloads/carrossel_prompts_[timestamp].json \
  --variants 4 \
  --image-url [URL_SE_FORNECIDA] \
  --dual-cover
```

Flag `--dual-cover` gera Slide 1 com ambos templates.

### 5. Finalização

Mostre ao usuário:
```
✅ Carrossel gerado com sucesso!

📊 Resumo:
   • Slides: N
   • Imagens: N × 4 variantes = X total
   • Localização: ~/Downloads/carrossel_slide_*.png

🎯 Próximos passos:
   1. Revisar variantes de cada slide
   2. Upload para Meta Ads Manager
   3. Criar campanha
```

## Notas Importantes

- SEMPRE use Task tool para subagentes (não tente gerar copy diretamente)
- SEMPRE aguarde aprovação do usuário após mostrar opções
- Template visual é FIXO (colagem artesanal)
- Slides 2+ não usam imagem de referência (só slide 1)
- Variantes padrão: 4 por slide

## Recursos

- **Exemplos Hormozi:** Ver REFERENCE.md
- **Casos de uso:** Ver EXAMPLES.md
- **Troubleshooting:** Ver TROUBLESHOOTING.md
