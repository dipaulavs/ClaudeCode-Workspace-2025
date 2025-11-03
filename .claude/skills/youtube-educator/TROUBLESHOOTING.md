# YouTube Educator - Troubleshooting

## Erro 1: "photos_urls.json não encontrado"

### Sintoma
```
❌ Erro: Arquivo photos_urls.json não encontrado!

📸 Execute o setup primeiro:
   python3 scripts/thumbnail-creation/setup_photos.py
```

### Causa
Tentou criar thumbnails sem ter feito setup das fotos.

### Solução
```bash
# 1. Adicionar 4 fotos em:
scripts/thumbnail-creation/templates/fotos/
# foto1.jpg, foto2.jpg, foto3.jpg, foto4.jpg

# 2. Executar setup (UMA VEZ)
python3 scripts/thumbnail-creation/setup_photos.py

# 3. Tentar novamente
# Skill vai funcionar normalmente
```

### Prevenção
O setup só precisa ser feito UMA VEZ. As URLs das fotos ficam salvas permanentemente (1 ano).

---

## Erro 2: xAI Search requer Python 3.11+

### Sintoma
```bash
python3 scripts/search/xai_web.py "tema"
# Erro: SyntaxError ou módulo incompatível
```

### Causa
Scripts xAI usam Python 3.11+ (tipo hints modernos).

### Solução
```bash
# Verificar versão instalada
python3.11 --version

# Se não tiver, instalar:
# macOS (Homebrew)
brew install python@3.11

# Usar python3.11 explicitamente
python3.11 scripts/search/xai_web.py "tema"
```

### Alternativa
Pular extração xAI e usar apenas YouTube + Twitter:
```
Skill pergunta: "Buscar em quais fontes?"
Você: "YouTube e Twitter apenas"
```

---

## Erro 3: Apresentação HTML não abre automaticamente

### Sintoma
Apresentação gerada mas navegador não abre.

### Causa
Sistema operacional bloqueia abertura automática ou navegador padrão não configurado.

### Solução
```bash
# Abrir manualmente (macOS)
open apresentacao_[tema].html

# Abrir manualmente (Linux)
xdg-open apresentacao_[tema].html

# Abrir manualmente (Windows)
start apresentacao_[tema].html
```

### Prevenção
Configurar navegador padrão no sistema operacional.

---

## Erro 4: hormozi-leads não gera headlines suficientes

### Sintoma
Recebe apenas 3-4 headlines em vez de 6-8.

### Causa
Contexto insuficiente fornecido (assunto muito genérico).

### Solução
Fornecer mais detalhes ao usuário quando skill perguntar:
- **Assunto específico:** "Transformers em IA" > "IA"
- **Avatar claro:** "Desenvolvedores Python iniciantes" > "Programadores"
- **Objetivo:** "Explicar conceito técnico de forma simples" > "Ensinar"

hormozi-leads precisa de contexto rico para gerar variações.

---

## Erro 5: Thumbnails ficaram ruins/genéricas

### Sintoma
Thumbnails geradas não têm a qualidade esperada.

### Causa Comum
Fotos base com baixa qualidade ou iluminação ruim.

### Solução
**Melhorar fotos base:**
1. Usar fotos em alta resolução (mínimo Full HD)
2. Boa iluminação no rosto
3. Expressões faciais marcantes
4. Fundo limpo (será removido de qualquer forma)

**Re-fazer setup:**
```bash
# Substituir fotos em templates/fotos/
# Rodar setup novamente
python3 scripts/thumbnail-creation/setup_photos.py
# Aceitar refazer upload
```

### Dica
Tire múltiplas fotos com diferentes expressões e escolha as 4 melhores antes do setup.

---

## Erro 6: Nota Obsidian não foi criada

### Sintoma
Workflow completo mas nota não aparece em Obsidian.

### Causa
Pasta `09 - YouTube Production/` não existe no vault Obsidian.

### Solução
```bash
# Verificar caminho do vault Obsidian
# Criar pasta manualmente
mkdir -p "/caminho/do/vault/09 - YouTube Production"

# Ou atualizar config em:
scripts/obsidian/quick_note.py
# Modificar OBSIDIAN_VAULT_PATH
```

### Alternativa
Skill salva nota em `output/obsidian-notes/` como fallback.

---

## Erro 7: Vídeo muito longo (>15min)

### Sintoma
Roteiro gerou 12+ slides, vídeo ficou longo demais.

### Causa
Tema muito amplo ou conteúdo extraído muito denso.

### Solução
**Antes de gerar roteiro:**
```
Skill pergunta: "Quantos slides deseja?"
Você: "6 slides" (em vez do padrão 8)
```

**Ou pedir foco:**
```
"Cria vídeo sobre Transformers focando APENAS em self-attention"
```

Limitar escopo = vídeos mais curtos e focados.

---

## Erro 8: Claude Code não ativou youtube-educator automaticamente

### Sintoma
Disse "Cria vídeo sobre X" mas skill não ativou.

### Causa
Frase não matchou os triggers da skill.

### Solução
**Frases que ativam:**
- ✅ "Cria vídeo sobre [tema]"
- ✅ "Quero fazer vídeo do YouTube de [tema]"
- ✅ "Prepara apresentação para gravar vídeo sobre [tema]"
- ✅ "Cria conteúdo YouTube sobre [tema]"

**Frases que NÃO ativam:**
- ❌ "Me ajuda com YouTube" (muito genérico)
- ❌ "Ideias para vídeo" (não é criação)

**Forçar ativação:**
```
"Ativa skill youtube-educator para criar vídeo sobre [tema]"
```

---

## Problema Comum: Workflow incompleto

### Sintoma
Skill parou em alguma etapa e não completou.

### Causa
Erro em algum script intermediário.

### Solução
**Ver logs:**
```bash
# Verificar último arquivo gerado
ls -lt roteiro_* apresentacao_* output/thumbnails/

# Identificar onde parou e continuar manualmente
```

**Etapas manuais de fallback:**
```bash
# Se parou após roteiro:
python3 scripts/visual-explainer/generate.py --roteiro roteiro_tema.md

# Se parou antes de thumbnails:
python3 scripts/thumbnail-creation/create_thumbnails.py "Headline" --topic tema
```

---

## Debug Geral

### Verificar Dependências
```bash
# Python 3.11 (xAI)
python3.11 --version

# APIs configuradas
cat config/apis.env | grep -E "XAI_API_KEY|OPENAI_API_KEY|KIE_API_KEY"

# Scripts funcionais
python3 scripts/image-generation/generate_nanobanana.py "teste"
```

### Verificar Setup Thumbnails
```bash
# URLs salvas
cat scripts/thumbnail-creation/photos_urls.json

# Fotos na pasta
ls scripts/thumbnail-creation/templates/fotos/
```

### Verificar Obsidian
```bash
# Vault existe
ls ~/Documents/Obsidian\ Vault/

# Pasta Production existe
ls ~/Documents/Obsidian\ Vault/09\ -\ YouTube\ Production/
```

---

## Logs Úteis

**Durante execução, verificar outputs:**
- Extração: xAI/YouTube/Twitter exibem URLs encontradas
- Roteiro: Claude Code mostra número de slides
- visual-explainer: Confirma template usado
- hormozi-leads: Lista headlines geradas
- thumbnail-creator: Mostra foto escolhida aleatoriamente

**Se algo falhar, procurar:**
```
❌ [mensagem de erro específica]
```

E verificar seção correspondente acima.

---

**Última atualização:** 2025-11-03
**Versão:** 1.0
