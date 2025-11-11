# Obsidian Organizer - Troubleshooting

## 🚨 Problemas Comuns e Soluções

---

## Problema 1: Tipo Errado Detectado

**Sintoma:**
Usuário pediu anotação mas foi criada como tarefa.

**Causa:**
Keywords ambíguas ("preciso anotar" pode ser tarefa OU anotação)

**Solução:**
```
Indicadores mais fortes:
- Tarefa: "fazer", "lembrar de", "checklist"
- Anotação: "vi", "interessante", "referência"
- Vídeo: URL YouTube SEMPRE = vídeo

Em caso de dúvida → perguntar ao usuário
```

**Exemplo correto:**
```
Ambíguo? Perguntar:

"Anotar sobre Python" - é:
1. 📋 Tarefa (fazer algo)
2. 💡 Anotação (referência)
```

---

## Problema 2: Data/Hora no Formato Errado

**Sintoma:**
Data criada como `2025-11-03 14:30` (ISO) em vez de `03/11/2025 14:30` (BR)

**Causa:**
Usar formato padrão do sistema em vez do brasileiro

**Solução:**
```bash
# ❌ Errado
date "+%Y-%m-%d %H:%M"

# ✅ Correto
date "+%d/%m/%Y %H:%M"
```

**Lembrete:**
- DD/MM/YYYY HH:MM (24h)
- Sempre formato brasileiro
- Nunca AM/PM

---

## Problema 3: Transcrição Não Colapsável

**Sintoma:**
Transcrição aparece expandida, poluindo a nota.

**Causa:**
Não usar callout colapsável ou sintaxe incorreta.

**❌ Errado:**
```markdown
## Transcrição
[texto longo]
```

**✅ Correto:**
```markdown
> [!note]- 📄 Transcrição Completa (clique para expandir)
> [texto longo]
```

**Detalhe importante:** O `-` após `[!note]` faz começar **fechado**.

---

## Problema 4: Vídeo Sem Categoria

**Sintoma:**
Vídeo criado sem categoria no frontmatter.

**Causa:**
Esquecer de preencher campo obrigatório.

**Solução:**
```yaml
# ❌ Errado
---
assistido: 03/11/2025 14:30
link: url
---

# ✅ Correto
---
assistido: 03/11/2025 14:30
categoria: tutorial
link: url
---
```

**Categorias válidas:**
notícia, tutorial, curso, aula, review, documentário, palestra

**Se usuário não informou:** Perguntar antes de criar.

---

## Problema 5: Arquivo Criado em Local Errado

**Sintoma:**
Tarefa criada em `💡 Anotações/` em vez de `📋 Tarefas/`

**Causa:**
Mapeamento incorreto de tipo → pasta

**Solução - Mapa correto:**
```
📋 Tarefas/    ← Tarefas (ações, checklist)
💡 Anotações/  ← Anotações (ideias, rascunhos)
📺 Vídeos/     ← Vídeos YouTube
```

**Nunca criar em:**
- ❌ Raiz do vault
- ❌ Pasta errada
- ❌ Templates (é só para templates)

---

## Problema 6: Nomenclatura Ruim do Arquivo

**Sintoma:**
Arquivos com nomes como `tarefa1.md`, `nota.md`, `video.md`

**Causa:**
Nome não descritivo

**❌ Evitar:**
- `tarefa1.md`
- `2025-11-03.md` (data no nome)
- `IMPORTANTE!!!.md` (excessivo)
- `temp.md`

**✅ Bom:**
- `Ligar pro cliente.md`
- `Ideia app produtividade.md`
- `Tutorial Claude Code.md`

**Regra:** Nome deve ser autoexplicativo.

---

## Problema 7: Resposta Muito Longa

**Sintoma:**
Skill responde com 5+ linhas explicando o que fez.

**Causa:**
Estilo verboso, não minimalista.

**❌ Resposta excessiva:**
```
Perfeito! Criei uma anotação incrível para você sobre
esse assunto super interessante! A anotação está
devidamente organizada e categorizada no seu sistema
minimalista do Obsidian. Você pode acessar ela no
dashboard de anotações ou diretamente na pasta...
[continua por 10 linhas]
```

**✅ Resposta minimalista:**
```
✅ Anotação criada!

💡 [Nome]
📍 💡 Anotações/
⏰ DD/MM/YYYY HH:MM
```

**Máximo:** 4-5 linhas

---

## Problema 8: Frontmatter Incompleto

**Sintoma:**
Campos obrigatórios faltando ou vazios.

**Causa:**
Não preencher todos os campos do template.

**Checklist obrigatório:**

### Tarefa
- ✅ `criada:` (data/hora BR)
- ✅ `status:` (aberta/concluída)

### Anotação
- ✅ `criada:` (data/hora BR)
- ✅ `tags: [anotacao]`

### Vídeo
- ✅ `assistido:` (data/hora BR)
- ✅ `categoria:` (valor válido)
- ✅ `link:` (URL YouTube)
- ✅ `tags: [youtube]`

---

## Problema 9: Kanban Não Atualizado

**Sintoma:**
Tarefa criada mas não aparece no Kanban.

**Causa:**
Não adicionar o link da tarefa ao arquivo `📊 Kanban.md`

**Solução:**
Adicionar manualmente ou informar que usuário pode arrastar depois.

**Formato correto no Kanban:**
```markdown
## 📥 A Fazer

- [ ] [[Nome da Tarefa]]
```

**Nota:** Skill pode criar arquivo E adicionar ao Kanban se usuário pedir explicitamente.

---

## Problema 10: Path do Vault Incorreto

**Sintoma:**
Erro ao tentar criar arquivo (file not found)

**Causa:**
Path do vault mudou ou está incorreto.

**Path correto (MCP Filesystem):**
```
/Users/felipemdepaula/Documents/Obsidian/Claude-code-ios/
```

**Método de acesso:**
- ✅ Write tool (filesystem direto via iCloud)
- ✅ Funciona mesmo com Obsidian fechado
- ❌ NÃO usa REST API do Obsidian

**Verificar:**
1. Path existe?
2. Subpastas existem? (📋 Tarefas/, 💡 Anotações/, 📺 Vídeos/)
3. Permissões corretas?
4. iCloud sincronizando?

**Teste:**
```bash
ls "/Users/felipemdepaula/Documents/Obsidian/Claude-code-ios/"
```

---

## 🔍 Debug Checklist

Antes de criar qualquer arquivo, verificar:

1. [ ] Tipo identificado corretamente?
   - Tarefa, Anotação ou Vídeo?

2. [ ] Pasta correta determinada?
   - 📋 Tarefas/, 💡 Anotações/, ou 📺 Vídeos/?

3. [ ] Frontmatter completo?
   - Todos os campos obrigatórios preenchidos?

4. [ ] Data/hora brasileira?
   - DD/MM/YYYY HH:MM?

5. [ ] Nome do arquivo descritivo?
   - Autoexplicativo sem ver conteúdo?

6. [ ] Template correto aplicado?
   - Estrutura adequada ao tipo?

7. [ ] Estilo minimalista?
   - Visual limpo, sem poluição?

8. [ ] Transcrição colapsável? (vídeos)
   - Usa `> [!note]-`?

9. [ ] Categoria válida? (vídeos)
   - Uma das categorias aceitas?

10. [ ] Resposta concisa?
    - Máx 4-5 linhas?

---

## 🆘 Quando Pedir Ajuda

**Perguntar ao usuário quando:**

1. **Ambiguidade de tipo**
   - "Anotar X" pode ser tarefa OU anotação

2. **Categoria de vídeo não informada**
   - Sempre obrigatória para vídeos

3. **Informação essencial faltando**
   - Link do vídeo não fornecido
   - Título não claro

**Não perguntar sobre:**
- Data/hora (usar atual)
- Formato (usar padrão brasileiro)
- Localização (usar mapa de pastas)

---

## 📚 Referências Rápidas

**Formato data:** `03/11/2025 14:30`
**Categorias vídeo:** notícia, tutorial, curso, aula, review, documentário, palestra
**Transcrição:** `> [!note]- 📄 Transcrição Completa (clique para expandir)`
**Vault path:** `/Users/felipemdepaula/Documents/Obsidian/Claude-code-ios/`

---

**Ver também:**
- [[SKILL.md]] - Instruções principais
- [[REFERENCE.md]] - Detalhes técnicos
- [[EXAMPLES.md]] - Casos de uso práticos
