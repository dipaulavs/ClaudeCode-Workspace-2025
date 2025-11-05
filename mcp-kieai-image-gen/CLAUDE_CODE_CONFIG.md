# ⚡ Configuração para Claude Code

## ✅ Status

```
MCP adicionado com sucesso!

Nome: kie-nanobanana-create
Tipo: stdio (local)
Config: ~/.claude.json (projeto local)
```

---

## 🔍 Verificar Status

No Claude Code (este terminal), digite:

```
/mcp
```

Deve mostrar:
```
🔌 kie-nanobanana-create (connected)
```

---

## 🎨 Como Usar Agora

**Opção 1: Uso Direto (Recomendado)**

Basta pedir normalmente:

```
Você: Gere uma imagem de um gato fofo e salve no meu computador
```

Eu vou detectar automaticamente e usar o MCP!

**Opção 2: Comando /mcp (Manual)**

```
/mcp use kie-nanobanana-create
```

Depois:
```
Você: Gere uma imagem...
```

---

## 📍 Onde Está Configurado

### Claude Code (Terminal)
```
~/.claude.json
  └─ mcpServers
      └─ kie-nanobanana-create ✅
```

### Claude Desktop (App)
```
~/Library/Application Support/Claude/claude_desktop_config.json
  └─ mcpServers
      └─ kie-nanobanana-create ✅
```

**Ambos configurados!** ✅

---

## 🚀 Teste Rápido

Digite no Claude Code:

```
Gere uma imagem de um robô fofo
```

Eu vou:
1. Detectar que você quer gerar imagem
2. Ver que tenho o MCP disponível
3. Usar automaticamente
4. Salvar em ~/Downloads

**Você não precisa fazer nada especial!**

---

## 🔄 Diferenças

### Claude Desktop
- ✅ Auto-ativo em TODAS as conversas
- ✅ Ícone 🔌 visível
- ✅ Gerenciamento visual

### Claude Code (Terminal)
- ✅ Auto-ativo APÓS configurar
- ✅ Comando `/mcp` para status
- ✅ Mais leve e rápido

---

## 📊 Configuração Atual

```json
{
  "mcpServers": {
    "kie-nanobanana-create": {
      "type": "stdio",
      "command": "/opt/homebrew/bin/python3.11",
      "args": [
        "/Users/.../mcp-kieai-image-gen/server.py"
      ]
    }
  }
}
```

---

## ✅ Checklist

- [x] MCP criado e testado
- [x] Adicionado ao Claude Code
- [x] Adicionado ao Claude Desktop
- [ ] **Testar agora** - peça para gerar uma imagem!

---

**Status:** ✅ Configurado no Claude Code
**Próximo:** Teste pedindo "Gere uma imagem..."
