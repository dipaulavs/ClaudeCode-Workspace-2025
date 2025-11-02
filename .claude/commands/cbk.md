Liste o histórico completo de backups do repositório e ofereça opções para restaurar versões anteriores.

**Execute as seguintes ações:**

1. **Mostrar histórico de commits (últimos 20 backups):**
   - Execute: `git log --oneline --graph --decorate -20`
   - Mostre em formato de tabela legível:
     - Hash do commit (curto)
     - Data/hora
     - Mensagem do commit
   - Use também: `git log --pretty=format:"%h - %ar - %s" -20` para formato mais limpo

2. **Estatísticas úteis:**
   - Total de commits: `git rev-list --count HEAD`
   - Último backup: `git log -1 --pretty=format:"%h - %ar - %s"`
   - Tamanho do repositório: `git count-objects -vH`

3. **Mostrar o que mudou no último commit:**
   - Execute: `git show --stat HEAD`
   - Liste arquivos modificados/adicionados/removidos

4. **Perguntar ao usuário o que ele quer fazer:**
   - Opção 1: Ver detalhes de um commit específico
   - Opção 2: Ver diferenças entre commits
   - Opção 3: Restaurar arquivo específico de versão antiga
   - Opção 4: Restaurar projeto inteiro para versão antiga (criar branch)
   - Opção 5: Apenas visualizar (sem ação)

5. **Se usuário escolher restaurar:**

   **Para arquivo específico:**
   - Perguntar: qual commit? (hash)
   - Perguntar: qual arquivo? (caminho)
   - Executar: `git checkout HASH -- caminho/arquivo`
   - Confirmar restauração

   **Para projeto inteiro (SEGURO - cria branch):**
   - Perguntar: qual commit? (hash)
   - Criar branch de segurança: `git checkout -b backup-restore-TIMESTAMP HASH`
   - Avisar: "Branch criada! Para voltar ao main: git checkout main"
   - Mostrar diferenças: `git diff main`

6. **Comandos úteis adicionais a mostrar:**
   ```bash
   # Ver mudanças de um commit específico
   git show HASH

   # Ver arquivos alterados entre duas versões
   git diff HASH1 HASH2 --name-only

   # Ver conteúdo de arquivo em versão específica (sem restaurar)
   git show HASH:caminho/arquivo.py

   # Criar branch de backup antes de restaurar
   git checkout -b backup-seguro
   ```

7. **Avisos importantes:**
   - ⚠️ Sempre fazer backup atual antes de restaurar (`/bk`)
   - ⚠️ Restaurar projeto inteiro cria nova branch (segurança)
   - ⚠️ Para restaurar arquivo: não precisa branch
   - ℹ️ Nada é perdido permanentemente no Git

**Formato de saída recomendado:**

```
📦 HISTÓRICO DE BACKUPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Estatísticas:
  • Total de backups: X commits
  • Último backup: há X horas
  • Tamanho: X MB

🕐 Últimos 20 backups:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hash    | Quando          | Descrição
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
8d3ff87 | há 5 minutos    | 🔄 Backup automático - 2025-11-02 09:11
6ba7dd2 | há 10 minutos   | 🚀 Backup completo ClaudeCode Workspace 2025
...

📝 Último backup incluiu:
  • 2 arquivos modificados
  • +39 linhas adicionadas

❓ O que você quer fazer?
  1️⃣ Ver detalhes de um commit
  2️⃣ Comparar duas versões
  3️⃣ Restaurar arquivo específico
  4️⃣ Restaurar projeto inteiro (cria branch)
  5️⃣ Apenas visualizar (nada)
```

**IMPORTANTE:**
- Sempre criar backup atual ANTES de qualquer restauração
- Para restauração completa, SEMPRE criar branch (segurança)
- Explicar cada passo ao usuário
- Confirmar ações destrutivas
