# Learnings - Hormozi Leads

Este arquivo registra todos os erros corrigidos e aprendizados adquiridos durante o uso desta skill.

## Objetivo

Prevenir que os mesmos erros aconteçam novamente, mantendo histórico de:
- Problemas encontrados
- Correções aplicadas
- Linhas/arquivos afetados
- Status da correção

---

## Histórico de Correções

<!-- As correções mais recentes aparecem primeiro -->

### 2025-11-08 - Reorganização estrutural da skill

**Problema:** Arquivos de referência soltos na raiz da skill (hooks-biblioteca.md, headlines-frameworks.md, etc)
**Correção:** Movidos todos arquivos de referência para `references/` seguindo padrão skill-creator2
**Arquivos reorganizados:**
- hooks-biblioteca.md → references/
- headlines-frameworks.md → references/
- ctas-persuasivos.md → references/
- retain-formulas.md → references/
- equacao-valor.md → references/
- carrosseis-instagram.md → references/
- REFERENCE.md → references/
- EXAMPLES.md → references/
- TROUBLESHOOTING.md → references/

**Status:** ✅ Corrigido

### 2025-11-08 - Adicionado sistema de auto-correção

**Problema:** Skill não tinha sistema de auto-correção e aprendizado contínuo
**Correção:** Adicionados scripts/update_skill.py, scripts/log_learning.py e LEARNINGS.md
**Status:** ✅ Corrigido
