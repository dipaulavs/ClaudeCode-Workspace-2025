# ⚡ QUICK START - n8n-MCP Project

## 🚀 Início Rápido (3 passos)

### 1. Abrir o projeto no Claude Code
```bash
cd ~/Desktop/ClaudeCode-Workspace/n8n-mcp-project
claude-code
```

### 2. Verificar conexão
Você deve ver: `🔌 New MCP server found: n8n-mcp`

### 3. Começar a criar workflows!
```
Crie um chatbot simples com OpenAI
```

---

## 📝 Comandos Úteis

### Listar workflows existentes
```
Liste todos os workflows do n8n
```

### Criar workflow simples
```
Crie um workflow que [descrição]
```

### Workflow com planejamento
```
Ative o modo de planejamento. Preciso criar [descrição complexa]. Me pergunte o que você precisa saber.
```

### Ver detalhes de um workflow
```
Mostre os detalhes do workflow [nome ou ID]
```

### Atualizar workflow existente
```
Atualize o workflow [nome] para [mudanças]
```

---

## 🎯 Exemplos Práticos

### Exemplo 1: Chatbot Simples
```
Crie um chatbot com:
- OpenAI chat model (GPT-4o-mini)
- Memória simples
- Ferramenta Wikipedia
- Trigger manual de chat
```

**Resultado esperado:** Workflow funcional com 4-5 nodes

---

### Exemplo 2: Newsletter Automática
```
Modo de planejamento.

Crie uma automação de newsletter que:
1. Roda todo dia às 8h
2. Busca notícias de 3 feeds RSS sobre IA
3. Resume com OpenAI
4. Formata como email HTML
5. Envia via Gmail

O que você precisa saber?
```

**Resultado esperado:** Perguntas do Claude → Plano detalhado → Workflow com 8-12 nodes

---

### Exemplo 3: Integração com API
```
Crie um workflow que:
1. Recebe webhook com dados de novo cliente
2. Valida os dados
3. Cria registro no Airtable
4. Envia mensagem de boas-vindas no WhatsApp via Evolution API
5. Notifica equipe no Slack
```

**Resultado esperado:** Workflow de integração completo

---

## 💡 Dicas de Produtividade

### Para workflows simples
- Vá direto ao ponto, não precisa de plan mode
- Seja específico sobre integrações
- Mencione credenciais que precisa configurar

### Para workflows médios/complexos
- **SEMPRE use plan mode**
- Deixe o Claude fazer perguntas
- Forneça detalhes sobre:
  - Fontes de dados
  - Formatos esperados
  - Regras de negócio
  - Horários de execução

### Melhorando prompts
❌ Ruim: "Crie uma automação"
✅ Bom: "Crie uma automação que monitora email e salva anexos no Google Drive"
✅✅ Melhor: "Crie uma automação que: 1) Monitora Gmail para emails com tag 'faturas', 2) Extrai anexos PDF, 3) Faz upload no Google Drive em pasta específica, 4) Envia notificação no Slack"

---

## ⚠️ Avisos Importantes

### Nunca será deletado sem confirmação
O Claude Code SEMPRE vai pedir confirmação antes de deletar qualquer workflow. Esta é uma regra de segurança hard-coded.

### Credentials precisam ser configuradas
O Claude Code cria a estrutura do workflow, mas você precisa:
1. Configurar credenciais (OAuth, API keys, etc) manualmente no n8n
2. Testar o workflow
3. Ativar quando estiver pronto

### Workflows complexos não são 100%
Para workflows muito complexos (15+ nodes):
- Espere ~50-80% de conclusão
- O Claude cria a estrutura base
- Você precisa ajustar detalhes específicos
- **Isso é normal e esperado!**

---

## 🔍 Verificação de Saúde

Execute estes comandos para verificar se está tudo OK:

```bash
# Node.js instalado?
node --version
# Deve mostrar: v24.9.0 (ou superior)

# NPM instalado?
npm --version
# Deve mostrar: 11.6.0 (ou superior)

# Testar n8n-MCP
npx n8n-mcp
# Deve conectar e aguardar comandos

# Ver configuração
cat .mcp.json
# Deve mostrar suas credenciais (URL e API key)

# Ver instruções
cat claude.md
# Deve mostrar todas as instruções incluindo regra de não deletar
```

---

## 🆘 Problemas Comuns

### "MCP server not found"
**Solução:**
1. Verifique se `.mcp.json` existe nesta pasta
2. Reinicie o Claude Code
3. Certifique-se de estar na pasta correta

### "Connection refused"
**Solução:**
1. Verifique se a URL está correta: `https://n8n.loop9.com.br`
2. Teste se o n8n está online no navegador
3. Confirme que a API key é válida

### "Permission denied"
**Solução:**
1. Vá no n8n → Settings → n8n API
2. Verifique se a API key tem TODOS os scopes
3. Se necessário, crie nova API key com todos os scopes

---

## 📚 Próximos Passos

1. ✅ **Teste simples** - Crie um chatbot básico
2. ✅ **Teste médio** - Crie uma automação com 5-10 nodes
3. ✅ **Documente** - Anote workflows criados no README.md
4. ✅ **Experimente** - Crie automações do seu dia a dia
5. ✅ **Compartilhe** - Se funcionar bem, ensine sua equipe

---

## 🎓 Recursos de Aprendizado

- **Vídeo original:** https://www.youtube.com/watch?v=d3bWvva6ucw
- **Docs n8n-mcp:** https://github.com/czlonkowski/n8n-mcp
- **Plano completo:** `../N8N_MCP_IMPLEMENTATION_PLAN.md`
- **n8n Docs:** https://docs.n8n.io

---

**Última atualização:** 31/10/2025
**Status:** ✅ Configurado e pronto para uso
