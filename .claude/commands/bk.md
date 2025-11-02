Execute um backup automático completo do workspace para o GitHub seguindo este processo:

1. **Adicionar todas as mudanças:**
   - Execute `git add .` para incluir todos os arquivos modificados/novos
   - Isso inclui código, configs, e o arquivo .env (repositório privado)

2. **Criar commit com timestamp:**
   - Gere um commit com mensagem automática formatada:
   ```
   🔄 Backup automático - [DATA/HORA]

   Alterações commitadas via comando /bk

   🤖 Generated with Claude Code
   ```
   - Use o formato de data: YYYY-MM-DD HH:MM
   - Exemplo: "2025-11-02 14:30"

3. **Enviar para GitHub:**
   - Execute `git push origin main`
   - Confirme que o push foi bem-sucedido

4. **Feedback ao usuário:**
   - Mostre quantos arquivos foram modificados
   - Exiba o hash do commit criado
   - Confirme que o backup está no GitHub
   - Mostre o link do repositório: https://github.com/dipaulavs/ClaudeCode-Workspace-2025

5. **Em caso de erro:**
   - Se houver conflitos, informe o usuário
   - Se não houver mudanças, avise "Nada para commitar, workspace já está atualizado"
   - Se houver erro no push, mostre a mensagem de erro

**IMPORTANTE:**
- Sempre execute os 3 comandos: add, commit, push
- Nunca pule etapas
- O repositório é PRIVADO, então .env é incluído
- Mantenha mensagens de commit consistentes
