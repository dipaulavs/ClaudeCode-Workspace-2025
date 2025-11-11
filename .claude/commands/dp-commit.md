---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git diff:*), Bash(git log:*)
argument-hint: [message]
description: Commit rápido e inteligente estilo Felipe
---

# 🚀 DP Commit

Criar commit bem formatado: $ARGUMENTS

## Estado Atual

- Status: !`git status --porcelain`
- Branch: !`git branch --show-current`
- Staged: !`git diff --cached --stat`
- Unstaged: !`git diff --stat`
- Commits recentes: !`git log --oneline -5`

## Fluxo

1. Verificar arquivos staged com `git status`
2. Se nenhum staged → `git add .` automaticamente
3. Analisar `git diff` para entender mudanças
4. Criar mensagem com emoji + conventional commit

## Formato Commit

```
<emoji> <tipo>: <descrição>
```

**Tipos mais usados:**
- ✨ `feat`: Nova feature
- 🐛 `fix`: Bug fix
- 📝 `docs`: Documentação
- 💄 `style`: Formatação/UI
- ♻️ `refactor`: Refatoração
- ⚡️ `perf`: Performance
- ✅ `test`: Testes
- 🔧 `chore`: Config/tooling
- 🚀 `deploy`: Deploy/CI
- 🗑️ `remove`: Remover código
- 🔒️ `security`: Segurança
- 🚑️ `hotfix`: Fix crítico
- 🎨 `improve`: Melhorias estrutura
- 🔥 `cleanup`: Limpeza código

## Exemplos

✅ Bons commits:
- ✨ feat: adicionar sistema agendamento visitas
- 🐛 fix: corrigir memory leak no webhook
- 📝 docs: atualizar README com instruções deploy
- ♻️ refactor: simplificar lógica score leads
- 🚑️ hotfix: corrigir falha crítica autenticação
- 🎨 improve: reorganizar estrutura componentes RAG
- 🔥 cleanup: remover código legado inutilizado
- 🚀 deploy: configurar Docker + Traefik SWARM

## Regras

- **Imperativo**: "adicionar" não "adicionado"
- **Conciso**: Primeira linha < 72 chars
- **Atômico**: 1 commit = 1 propósito
- **Português**: Mensagens em PT-BR
- **Direto**: Sem contexto óbvio

## Nota

Se múltiplas mudanças não relacionadas forem detectadas, vou sugerir split em commits separados.
