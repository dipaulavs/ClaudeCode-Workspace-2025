# 🔧 Prompt Templates - Troubleshooting

## Erro 1: Site Retorna Vazio (Carregamento Dinâmico)

### Sintoma
```
WebFetch retorna:
"Loading Components..."
"Found(0 results)"
"Optimizing data for better performance on mobile devices"
```

### Causa
- Site usa JavaScript para carregar templates dinamicamente
- WebFetch só captura HTML inicial (sem execução JS)
- Conteúdo real não aparece no fetch

### Solução

**✅ Usar GitHub como Fallback:**
```python
# Tentativa 1: Site
result = WebFetch(
    url="https://www.aitmpl.com/agents",
    prompt="List all agent templates..."
)

# Verificar se vazio
if "Loading Components" in result or "Found(0 results)" in result:
    # Tentativa 2: GitHub (sempre funciona)
    result = WebFetch(
        url="https://github.com/davila7/claude-code-templates",
        prompt="Find all templates in the repository. Extract from README or directory structure."
    )
```

**✅ Priorizar GitHub Direto (opção mais rápida):**
```python
# Ir direto para categoria no GitHub
WebFetch(
    url="https://github.com/davila7/claude-code-templates/tree/main/agents",
    prompt="List all agent templates in this directory with descriptions."
)
```

### Prevenção
- **Sempre** ter GitHub como fallback
- **Sempre** verificar se conteúdo retornado é útil
- **Considerar** usar GitHub como fonte primária (mais confiável)

---

## Erro 2: Template Não Encontrado (Busca Muito Específica)

### Sintoma
```
Usuário: "Pesquise template para análise de fraude em transações PIX"
Claude: Busca → Nenhum resultado
```

### Causa
- Template muito específico (não existe no repo)
- Keywords muito nichadas
- Categoria não mapeada corretamente

### Solução

**✅ Ampliar Busca (keywords relacionadas):**
```python
# Em vez de buscar apenas "fraude PIX"
WebFetch(
    url="https://github.com/davila7/claude-code-templates",
    prompt="Find templates related to: fraud detection, payment security, transaction analysis, financial auditing, or banking security."
)
```

**✅ Buscar em Múltiplas Categorias:**
```python
# Tentar Agents (security specialist)
agents = WebFetch(url="https://www.aitmpl.com/agents", ...)

# Tentar Skills (data analysis)
skills = WebFetch(url="https://www.aitmpl.com/skills", ...)

# Agregar resultados
```

**✅ Oferecer Criar Customizado:**
```
🔍 Nenhum template específico para "fraude PIX".

📂 Templates relacionados:
   ✅ Security Auditor Agent (pode adaptar)
   ✅ Data Analysis Skill (detectar anomalias)

💡 Recomendação:
   Quer que eu crie uma skill "pix-fraud-detector"?
   → Usaria skill-creator
   → Integraria com [API de análise]
```

### Prevenção
- **Sempre** ampliar keywords (sinônimos, termos relacionados)
- **Sempre** buscar em múltiplas categorias
- **Sempre** oferecer alternativa (criar skill)

---

## Erro 3: WebFetch Timeout (Página Pesada)

### Sintoma
```
Error: WebFetch timeout after 30 seconds
Request to https://www.aitmpl.com failed
```

### Causa
- Página muito grande (100+ templates)
- Assets pesados (imagens, JS bundles)
- Rede lenta

### Solução

**✅ Consultar Páginas Específicas:**
```python
# Em vez de página geral
WebFetch(url="https://www.aitmpl.com")  # ❌ Pode dar timeout

# Ir direto para categoria
WebFetch(url="https://www.aitmpl.com/agents")  # ✅ Menor, mais rápido
```

**✅ Usar GitHub (menor overhead):**
```python
# GitHub é mais leve (sem JS, sem assets)
WebFetch(url="https://github.com/davila7/claude-code-templates")
```

**✅ Prompt Focado (reduzir processamento):**
```python
# Prompt genérico (processa tudo)
"Analyze entire page and list everything"  # ❌ Lento

# Prompt focado (processa só necessário)
"List only agent names and descriptions, ignore navigation and footer"  # ✅ Rápido
```

### Prevenção
- **Sempre** consultar páginas específicas (não homepage)
- **Preferir** GitHub para listagens completas
- **Usar** prompts focados (extrair só o necessário)

---

## Erro 4: Categoria Errada (Mapeamento Incorreto)

### Sintoma
```
Usuário: "Busque template para validar dados antes de commit"
Claude: Busca em "Commands" → Não encontra
(Deveria buscar em "Hooks" - pre-commit validation)
```

### Causa
- Mapeamento usuário → categoria incorreto
- Keywords ambíguas ("validar" pode ser várias coisas)
- Falta de contexto

### Solução

**✅ Consultar Múltiplas Categorias:**
```python
# Se incerto, buscar em 2-3 categorias
hooks = WebFetch(url="https://www.aitmpl.com/hooks", ...)
commands = WebFetch(url="https://www.aitmpl.com/commands", ...)
skills = WebFetch(url="https://www.aitmpl.com/skills", ...)

# Apresentar todos resultados
```

**✅ Usar Tabela de Mapeamento (REFERENCE.md):**
```python
# Consultar mapeamento:
"validar dados antes de commit" → Keywords: "pre-commit", "validation", "hooks"
→ Categoria primária: Hooks
→ Categoria secundária: Commands
```

**✅ Perguntar ao Usuário (se muito ambíguo):**
```
🤔 "Validar dados" pode ser:
   1. Hook (pre-commit validation)
   2. Command (manual validation)
   3. Skill (data validation library)

Qual contexto: antes de commit, manual, ou programático?
```

### Prevenção
- **Sempre** consultar tabela de mapeamento (REFERENCE.md)
- **Se incerto** → buscar em múltiplas categorias
- **Se muito ambíguo** → perguntar ao usuário

---

## Erro 5: Resultado Duplicado (Múltiplas Fontes)

### Sintoma
```
Claude retorna:
✅ Security Auditor (de aitmpl.com)
✅ Security Auditor (de GitHub)
✅ Security Auditor Agent (variação do nome)
```

### Causa
- Consultou site + GitHub
- Nomes ligeiramente diferentes (com/sem "Agent")
- Sem deduplicação

### Solução

**✅ Deduplicate por Nome:**
```python
results = []

# Fetch de múltiplas fontes
site_results = WebFetch(url="https://www.aitmpl.com/agents", ...)
github_results = WebFetch(url="https://github.com/.../agents", ...)

# Merge e deduplicate (comparar nome normalizado)
seen = set()
for result in [site_results, github_results]:
    name_normalized = result['name'].lower().replace('agent', '').strip()
    if name_normalized not in seen:
        results.append(result)
        seen.add(name_normalized)
```

**✅ Priorizar Fonte Única:**
```python
# Opção 1: Site primeiro (melhor descrição)
result = WebFetch(url="https://www.aitmpl.com/agents", ...)
if not result or "Loading" in result:
    # Fallback para GitHub
    result = WebFetch(url="https://github.com/.../agents", ...)

# Apresentar apenas UMA fonte
```

### Prevenção
- **Preferir** fonte única (site OU GitHub, não ambos)
- **Se ambos** → deduplicate antes de apresentar
- **Indicar** fonte no output ("Fonte: GitHub" vs "Fonte: aitmpl.com")

---

## Erro 6: Prompt WebFetch Genérico Demais

### Sintoma
```
WebFetch retorna informações irrelevantes:
- Menu de navegação
- Footer
- Ads
- Pouca informação sobre templates
```

### Causa
- Prompt muito genérico ("tell me about this page")
- WebFetch processa tudo (incluindo UI elements)

### Solução

**✅ Prompt Específico e Estruturado:**
```python
# ❌ Genérico
WebFetch(
    url="https://www.aitmpl.com/agents",
    prompt="What's on this page?"
)

# ✅ Específico
WebFetch(
    url="https://www.aitmpl.com/agents",
    prompt="""
    List ONLY the agent templates available.
    For each template, extract:
    1. Template name
    2. Brief description (1 sentence)
    3. When to use (use cases)
    4. Direct link (if available)

    Ignore navigation, footer, and UI elements.
    Format as markdown table.
    """
)
```

**✅ Pedir Formato Específico:**
```python
prompt="""
Extract agent templates and format as JSON:
[
  {
    "name": "Security Auditor",
    "description": "...",
    "use_cases": ["...", "..."],
    "category": "agents"
  }
]
"""
```

### Prevenção
- **Sempre** usar prompts específicos (não genéricos)
- **Sempre** pedir formato estruturado (table, JSON, list)
- **Sempre** instruir ignorar UI elements

---

## Checklist de Debug

Quando busca não funcionar, verificar:

- [ ] **WebFetch retornou conteúdo?** (não vazio)
- [ ] **Conteúdo é útil?** (não "Loading..." ou erro)
- [ ] **Categoria correta?** (consultar mapeamento)
- [ ] **Prompt específico?** (não genérico)
- [ ] **Usou fallback?** (GitHub se site falhar)
- [ ] **Ampliou keywords?** (sinônimos, termos relacionados)
- [ ] **Ofereceu alternativa?** (criar skill customizada)

---

## Contato e Suporte

Se problema persistir:

1. **GitHub Issues:** https://github.com/davila7/claude-code-templates/issues
2. **Discord Comunidade:** [link da comunidade]
3. **Docs Oficiais:** https://docs.aitmpl.com

---

**Versão:** 1.0
**Total de Erros Documentados:** 6
