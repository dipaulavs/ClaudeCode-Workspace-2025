---
description: Busca notas soltas → identifica automaticamente → organiza visualmente no local correto
---

# Comando: /notas

**Ação automática:**
1. Buscar notas soltas/bagunçadas no Obsidian
2. Identificar tipo de cada uma (tarefa/ideia/nota/projeto)
3. Formatar visualmente (ASCII boxes/fluxos)
4. Mover para local correto
5. Deletar originais bagunçados

---

## 🎯 Fluxo

```
NOTAS SOLTAS
     │
     ▼
IDENTIFICAR
     │
  ┌──┴──┐
  │     │
TIPOS  LOCAL
  │     │
  └──┬──┘
     │
     ▼
ORGANIZAR
```

---

## 📋 Instruções para Claude

**Sistema:** Acesso direto via MCP filesystem (Obsidian não precisa estar aberto)

**Você DEVE:**

1. **Buscar notas soltas via MCP:**
   - Raiz do vault (sem pasta)
   - Nome genérico ("Sem título", "Untitled", "Nova nota")
   - Criadas hoje ou últimas 24h
   - Usar ferramentas MCP: `list_vault_notes` + `read_note`

2. **Para cada nota encontrada:**
   - Ler conteúdo completo via MCP
   - Identificar tipo usando skill `obsidian-quick-capture`
   - Formatar visual (diagramas ASCII)
   - Determinar pasta destino

3. **Estrutura de destino:**
   - `📋 Tarefas/` → Tarefas/ações/lembretes
   - `💡 Anotações/` → Ideias/insights
   - `📝 Notas/` → Notas de registro/referência (criar se não existir)
   - `📂 Projetos/` → Projetos complexos (criar se não existir)
   - `📺 Vídeos/` → Relacionado a vídeos YouTube

4. **Executar via MCP:**
   - Criar nota formatada no local correto (`create_note`)
   - Deletar nota original bagunçada (`delete_note`)
   - Reportar: "✅ [N] notas organizadas"

5. **Formato visual obrigatório:**
   - Emoji no título
   - Metadados estruturados
   - Diagrama ASCII
   - Próximos passos

---

## 🚨 IMPORTANTE

- **NUNCA** deixar tarefa em `💡 Anotações/`
- **SEMPRE** validar tipo antes de mover
- **SEMPRE** preservar conteúdo original
- **SEMPRE** usar formato visual consistente
- **MCP filesystem:** Operações diretas no vault, sem necessidade de Obsidian aberto

---

## 📊 Relatório Final

Ao terminar, mostrar:

```
✅ NOTAS ORGANIZADAS

📋 Tarefas: [N]
💡 Ideias: [N]
📝 Notas: [N]
📂 Projetos: [N]

Detalhes:
- [Título] → [Local]
- [Título] → [Local]
```
