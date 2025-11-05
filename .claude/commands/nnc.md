---
description: Criar nova nota solta usando obsidian-quick-capture
---

# Nova Nota Solta

**Sistema:** Acesso direto via MCP filesystem (Obsidian não precisa estar aberto)

**Ação obrigatória:** Ativar skill `obsidian-quick-capture` para processar nova nota.

**Fluxo:**
1. Ativar skill `obsidian-quick-capture`
2. Aguardar instruções do usuário sobre o conteúdo da nota
3. Skill processa e organiza automaticamente via MCP
4. Nota criada diretamente no vault usando ferramentas MCP

**IMPORTANTE:**
- Sempre usar skill `obsidian-quick-capture`, nunca criar manualmente
- MCP permite criação direta de notas sem Obsidian aberto
