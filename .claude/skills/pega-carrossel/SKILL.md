---
name: pega-carrossel
description: Download automático de carrosséis do Instagram com análise visual e geração de prompts detalhados para recriação idêntica ou adaptação para outros nichos. Auto-invoca quando usuário pedir para baixar/pegar/analisar carrossel do Instagram.
---

# Pega Carrossel

Faz download completo de carrosséis do Instagram, organiza slides com nomenclatura descritiva e gera prompts de IA detalhados para recriação (versão original idêntica + versão template adaptável para qualquer nicho).

## Quando Usar

AUTO-INVOCAR esta skill quando o usuário:
- Fornecer URL de carrossel do Instagram para download
- Pedir para "pegar/baixar esse carrossel"
- Solicitar análise de carrossel para recriação
- Querer criar template baseado em carrossel existente
- Mencionar "adaptar carrossel para outro nicho"

Exemplos de gatilhos:
- "Pega esse carrossel: https://www.instagram.com/p/ABC123/"
- "Baixa as imagens desse post e analisa"
- "Quero recriar esse carrossel para imóveis"
- "Faz download desse carrossel e me dá os prompts"

## Como Usar

### Workflow Completo

Quando a skill é invocada, executar o processo em 3 etapas:

#### 1. Executar Script Principal

```bash
python3 scripts/pega_carrossel_complete.py "URL_DO_INSTAGRAM"
```

Opcionalmente especificar diretório de saída:

```bash
python3 scripts/pega_carrossel_complete.py "URL" --output ~/Desktop
```

#### 2. Aguardar Conclusão

O script executa automaticamente:
1. Download via Apify API do Instagram
2. Organização em pasta `{tema}_{@username}/`
3. Nomenclatura descritiva dos slides (Hook, Tipo1, Tipo2, ..., CTA)
4. Análise visual com Claude API
5. Geração de prompts (versão original + template)

#### 3. Apresentar Resultados

Após conclusão, informar ao usuário:

```
✅ Carrossel baixado e analisado!

📁 Pasta: ~/Downloads/{tema}_{@username}/
🖼️  Slides: {N} slides
📝 Prompts: prompts_{N}slides.txt

O arquivo de prompts contém:
- ✅ Versão original (recriação idêntica)
- ✅ Versão template (adaptável para qualquer nicho)
- ✅ Paleta de cores identificada
- ✅ Tipografia identificada
- ✅ Exemplos de adaptação para outros nichos
```

## Estrutura de Saída

Para cada carrossel baixado, a estrutura gerada é:

```
{tema}_{@username}/
├── Slide 1 - Hook.jpg              # Capa atrativa
├── Slide 2 - Tipo1.jpg             # Conteúdo 1
├── Slide 3 - Tipo2.jpg             # Conteúdo 2
├── ...
├── Slide N - CTA.jpg               # Call-to-action final
├── metadata.json                    # Dados do post
└── prompts_{N}slides.txt           # Prompts detalhados
```

### Nomenclatura Automática de Slides

A skill aplica nomenclatura inteligente baseada na quantidade de slides:

- **1 slide**: "Slide 1 - Post Unico"
- **2 slides**: "Hook" → "CTA"
- **3 slides**: "Hook" → "Conteudo" → "CTA"
- **4 slides**: "Hook" → "Conteudo1" → "Conteudo2" → "CTA"
- **5+ slides**: "Hook" → "Tipo1" → "Tipo2" → ... → "CTA"

Padrões completos estão em `assets/slide_naming_patterns.json`.

## Conteúdo dos Prompts Gerados

O arquivo `prompts_{N}slides.txt` contém para CADA slide:

### Versão Original (Recriação Idêntica)

Prompt extremamente detalhado com:
- Cores exatas (códigos HEX)
- Tipografia precisa (fontes, tamanhos, pesos, kerning)
- Layout exato (posições, espaçamentos, margens)
- Textos literais como aparecem na imagem
- Imagens/símbolos específicos descritos em detalhes
- Efeitos visuais (sombras, bordas, gradientes, opacidades)
- Composição fotográfica (iluminação, ângulo, profundidade)

### Versão Template (Adaptável)

Prompt estruturado para adaptação com:
- Textos substituídos por `[TEXTO EDITÁVEL AQUI]`
- Imagens substituídas por `[IMAGENS E SÍMBOLOS CORRESPONDENTES AO INPUT AQUI]`
- `@username` substituído por `@lfimoveis` (template padrão)
- Toda estrutura visual preservada
- Exemplos de adaptação para outros nichos (imóveis, gastronomia, fitness, moda, educação)
- Checklist de personalização
- Variáveis documentadas

### Informações Adicionais

- **Paleta de cores completa** (todos os HEX usados)
- **Tipografia identificada** (fontes, hierarquia)
- **Especificações técnicas** (dimensões, DPI, formatos)
- **Dicas de recriação** por tipo de ferramenta (Figma, Canva, Photoshop)

## Dependências

### APIs Necessárias

1. **Apify API** - Download de posts do Instagram
   - Configurada em: `config/apify_config.py`
   - Actor usado: `apify/instagram-scraper`

2. **Anthropic Claude API** - Análise visual e geração de prompts
   - Variável de ambiente: `ANTHROPIC_API_KEY`
   - Model usado: `claude-sonnet-4-20250514`

### Bibliotecas Python

```bash
pip3 install apify-client requests anthropic
```

## Troubleshooting

### Erro: "APIFY_API_KEY não configurada"

Verificar se a chave existe em `config/apify_config.py`:

```python
APIFY_API_KEY = "apify_api_..."
```

### Erro: "ANTHROPIC_API_KEY não configurada"

Configurar variável de ambiente:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Erro: "Nenhum resultado encontrado"

Verificar se:
- URL está correta e acessível
- Post não foi deletado ou tornado privado
- Post é público (Instagram Scraper só acessa posts públicos)

### Prompts incompletos ou imprecisos

Aumentar `max_tokens` em `scripts/pega_carrossel_complete.py`:

```python
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=20000,  # Aumentar se necessário
    ...
)
```

### Pasta com nome estranho

O nome da pasta é baseado nas primeiras palavras da legenda. Se a legenda estiver vazia ou com caracteres especiais, ajustar manualmente após download ou editar função `sanitize_folder_name()`.

## Exemplos de Uso

### Exemplo 1: Download Simples

```bash
python3 scripts/pega_carrossel_complete.py "https://www.instagram.com/p/DQr4zkvjpCY/"
```

**Saída:**
```
~/Downloads/Qual_desses_tipos_absm/
├── Slide 1 - Hook.jpg
├── Slide 2 - Tipo1.jpg
├── Slide 3 - Tipo2.jpg
├── Slide 4 - Tipo3.jpg
├── Slide 5 - Tipo4.jpg
├── Slide 6 - CTA.jpg
├── metadata.json
└── prompts_6slides.txt
```

### Exemplo 2: Especificar Diretório

```bash
python3 scripts/pega_carrossel_complete.py \
    "https://www.instagram.com/p/ABC123/" \
    --output ~/Desktop/carrosseis
```

### Exemplo 3: Uso via Skill (Auto-Invocação)

**Usuário diz:**
> "Pega esse carrossel: https://www.instagram.com/p/DQr4zkvjpCY/"

**Claude executa:**
1. Auto-invoca skill `pega-carrossel`
2. Executa `python3 scripts/pega_carrossel_complete.py "URL"`
3. Aguarda conclusão
4. Apresenta resultados organizados ao usuário

## Limitações

- **Posts privados**: Não é possível baixar posts de contas privadas
- **Posts deletados**: URLs de posts deletados retornam erro
- **Limite de slides**: Funciona com qualquer quantidade, mas >10 slides pode levar mais tempo
- **Análise visual**: Qualidade depende da resolução das imagens do Instagram (máx 1080px)
- **Custo**: Cada execução consome créditos Apify + tokens Claude API

## Auto-Correção

Esta skill inclui sistema de auto-correção. Quando um erro ocorrer:

```bash
# 1. Corrigir SKILL.md
python3 scripts/update_skill.py "texto_antigo" "texto_novo"

# 2. Registrar aprendizado
python3 scripts/log_learning.py "descrição_erro" "correção_aplicada" "SKILL.md:linha"
```

Todos os erros corrigidos são registrados em `LEARNINGS.md` para prevenir recorrência.
