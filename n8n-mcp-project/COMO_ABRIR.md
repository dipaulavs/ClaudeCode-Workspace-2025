# 🚪 Como Abrir o Projeto n8n-MCP

## Método 1: Via Terminal (Recomendado)

```bash
cd ~/Desktop/ClaudeCode-Workspace/n8n-mcp-project
claude-code
```

---

## Método 2: Via Claude Code Desktop

1. Abra o Claude Code
2. Use o comando: `File > Open Folder`
3. Navegue até: `~/Desktop/ClaudeCode-Workspace/n8n-mcp-project`
4. Selecione a pasta e clique "Open"

---

## ✅ Verificação de Sucesso

Quando abrir o projeto corretamente, você deve ver:

```
🔌 New MCP server found: n8n-mcp
```

Se não aparecer, reinicie o Claude Code.

---

## 🎯 Primeiro Teste Recomendado

Após abrir o projeto, execute este teste:

```
Crie um chatbot simples com:
- OpenAI GPT-4o-mini
- Memória simples
- Wikipedia tool
- Manual chat trigger
```

Se funcionar, você está pronto! 🎉

---

## 📚 Próximos Passos

1. ✅ Leia o `QUICK_START.md` para comandos úteis
2. ✅ Consulte o `README.md` para estrutura do projeto
3. ✅ Documente workflows criados no `WORKFLOWS_LOG.md`
4. ✅ Experimente criar suas próprias automações!

---

## 🆘 Problemas?

Se o MCP server não conectar:

```bash
# 1. Verificar Node.js
node --version

# 2. Testar n8n-mcp diretamente
npx n8n-mcp

# 3. Verificar configuração
cat .mcp.json

# 4. Reiniciar Claude Code
```

---

**Instância n8n:** https://n8n.loop9.com.br
**Status:** ✅ Configurado e pronto
