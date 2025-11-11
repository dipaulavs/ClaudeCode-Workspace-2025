# Learnings - Obsidian Organizer

Registro de correções e aprendizados para prevenir erros recorrentes.

## 2025-11-11 - Sistema de Organização Completo

### 📋 Correções Implementadas

1. **Title Case nos Filenames** - Usar "Nome da Tarefa" (não "nome-da-tarefa")
2. **Campo `criada:`** - Usar `criada:` (não `created:`)
3. **Status inicial** - Sempre `status: aberta` para novas tarefas
4. **Integração Kanban** - Adicionar automaticamente em `## aberta`
5. **Dashboard queries** - Sempre excluir `file.name != "📊 Kanban"`

### 🎯 Workflow Correto

```
1. Analyze content type
2. Generate Title Case filename
3. Get datetime (DD/MM/YYYY HH:mm)
4. Load template
5. Fill with criada: and status: aberta
6. Write file
7. Add to Kanban (## aberta section)
8. Confirm to user
```

### ✅ Checklist Obrigatório

- [ ] Title Case filename
- [ ] criada: DD/MM/YYYY HH:mm
- [ ] status: aberta (if task)
- [ ] Added to Kanban (if task)
- [ ] Confirmation sent

---
**Atualizado:** 11/11/2025
