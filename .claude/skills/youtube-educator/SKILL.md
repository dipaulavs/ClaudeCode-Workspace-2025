# 🎬 YouTube Educator - Produção Completa de Vídeos Educativos

## Quando Usar (Model-Invoked)

**Ativa automaticamente quando usuário pedir:**
- "Cria vídeo sobre [assunto]"
- "Quero fazer vídeo do YouTube de [tema]"
- "Prepara apresentação para gravar vídeo sobre [X]"

**Propósito:** Automatizar produção de vídeos educativos (roteiro → gravação → metadados → thumbnails).

---

## Workflow Automático (7 Etapas)

### 1. Extração de Conteúdo 🔍
- Busca em: xAI Search + YouTube + Twitter/X
- Consolida contexto rico sobre tema
- Output: Material estruturado para roteiro

### 2. Roteiro Didático 📝
- **EU (Claude Code)** analiso e crio roteiro
- Estrutura: Conceito + Analogia + Exemplo + Notas
- 6-8 slides conteúdo + Resumo + CTA
- Salva: `roteiro_[tema].md`

### 3. Apresentação HTML 🎨
- CHAMA: visual-explainer skill
- Template: notion-interativo.html (dark mode)
- Output: `apresentacao_[tema].html` (abre automaticamente)

### 4. Você Grava 🎥
- Fullscreen (F) + gravação de tela
- Navegar com setas ← →
- Seguir notas do roteiro

### 5. Headlines Virais 📊
- CHAMA: hormozi-leads skill
- Output: 6-8 headlines (ângulos diferentes)
- Você escolhe favorita

### 6. Thumbnails 🎨
- CHAMA: thumbnail-creator
- Input: Headline escolhida
- Output: 4 thumbnails (MrBeast, Tech Minimal, High Contrast, Split Screen)
- Você escolhe favorita

### 7. Nota Obsidian 📋
- Rastreamento completo da produção
- Pasta: `09 - YouTube Production/`
- Checklist, links, status

---

## Output Final

✅ **Roteiro** → `roteiro_[tema].md`
✅ **Apresentação** → `apresentacao_[tema].html`
✅ **Headlines** → 6-8 opções
✅ **Thumbnails** → 4 estilos
✅ **Nota rastreamento** → Obsidian

**Pronto para edição e upload!**

---

## Setup Inicial (UMA VEZ)

**Thumbnails:**
```bash
# 1. Adicionar 4 fotos em:
scripts/thumbnail-creation/templates/fotos/

# 2. Executar setup
python3 scripts/thumbnail-creation/setup_photos.py
```

**Pronto!** Tudo mais já está configurado.

---

## Documentação Completa

- **Specs técnicas + Integração:** [REFERENCE.md](REFERENCE.md)
- **Casos de uso (4 exemplos):** [EXAMPLES.md](EXAMPLES.md)
- **Erros comuns (8 problemas):** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Skill Type:** Model-invoked (auto-ativa)
**FASE:** 1 (Pré-gravação + Metadados)
**Versão:** 1.0
