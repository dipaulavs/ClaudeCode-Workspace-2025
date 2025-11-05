# 🔧 Como Configurar no Claude Desktop

## ✅ Já Configurado!

O arquivo de configuração foi criado automaticamente em:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

---

## 🔄 Próximos Passos

### 1️⃣ Reiniciar Claude Desktop

```
1. Feche COMPLETAMENTE o Claude Desktop
   (Cmd+Q ou Claude > Quit)

2. Abra novamente
```

### 2️⃣ Verificar Conexão

```
1. Olhe o ícone 🔌 na barra inferior do Claude

2. Clique no ícone

3. Você deve ver:
   ✅ kie-nanobanana-create (connected)
```

Se aparecer ❌ ou erro, veja a seção Troubleshooting.

---

## 🎨 Como Usar

Após reiniciar, **abra qualquer conversa** e peça:

### Exemplo 1: Criar 1 Imagem

```
Você: Gere uma imagem de um gato fofo e salve no meu computador

Claude: [usa o MCP automaticamente]
        ✅ Imagem gerada!
        📄 gato_fofo_abc.png
        📂 Salvo em ~/Downloads
```

### Exemplo 2: Criar 3 Imagens

```
Você: Gere 3 imagens:
      1. Um gato
      2. Um cachorro
      3. Uma raposa

Claude: [usa batch mode automaticamente]
        ✅ 3 imagens geradas em paralelo!
        Tempo: ~17s (vs 30s)
```

### Exemplo 3: Editar Imagem

```
Você: Pegue essa imagem [URL] e mude a cor da camisa para vermelho

Claude: [detecta modo edição automaticamente]
        ✅ Imagem editada!
        📄 mudar_cor_camisa_abc.png
```

---

## 🔍 Como Funciona Automaticamente

```
┌───────────────────────────────────────┐
│ Claude Desktop                        │
├───────────────────────────────────────┤
│ Você: "Gere uma imagem de um gato"   │
│         ↓                             │
│ Claude analisa o pedido               │
│         ↓                             │
│ Claude detecta: precisa gerar imagem  │
│         ↓                             │
│ Claude vê MCP disponível:             │
│   🔌 kie-nanobanana-create           │
│         ↓                             │
│ Claude usa automaticamente:           │
│   generate_image(                     │
│     prompt="Um gato fofo",            │
│     auto_download=True                │
│   )                                   │
│         ↓                             │
│ ✅ Imagem gerada e salva              │
└───────────────────────────────────────┘
```

**Você não precisa pedir explicitamente para usar o MCP!**

Claude detecta automaticamente quando você pede para:
- "Gere uma imagem..."
- "Crie uma imagem..."
- "Gere 5 variações..."
- "Edite essa imagem..."
- "Mude a cor para..."

---

## 📍 Localização dos Arquivos

### MCP Server

```
/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/mcp-kieai-image-gen/
├── server.py          ← Código principal
├── README.md          ← Documentação
└── ...
```

### Configuração do Claude

```
~/Library/Application Support/Claude/
└── claude_desktop_config.json  ← Config automática
```

### Imagens Geradas

```
~/Downloads/
├── gato_fofo_abc.png
├── cachorro_brincando_xyz.png
└── ...
```

---

## 🐛 Troubleshooting

### MCP não aparece no ícone 🔌

**Solução 1:** Verificar config
```bash
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Deve mostrar:
```json
{
  "mcpServers": {
    "kie-nanobanana-create": {
      "command": "/opt/homebrew/bin/python3.11",
      "args": ["/Users/felipemdepaula/.../server.py"]
    }
  }
}
```

**Solução 2:** Testar servidor manualmente
```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/mcp-kieai-image-gen
/opt/homebrew/bin/python3.11 test_simple.py
```

Deve mostrar:
```
✅ Servidor inicializado com sucesso!
📋 Ferramentas disponíveis (3):
  🔧 generate_image
  ...
```

**Solução 3:** Verificar permissões
```bash
chmod +x /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/mcp-kieai-image-gen/server.py
```

### MCP mostra erro ❌

Verifique os logs do Claude Desktop:
```
Claude > View > Developer > Toggle Developer Tools
Console tab
```

---

## ✅ Checklist

Antes de usar:

- [x] ~~MCP criado~~ ✅
- [x] ~~Config criada~~ ✅
- [ ] **Reiniciar Claude Desktop** ⚠️ FAÇA ISSO AGORA
- [ ] Verificar ícone 🔌
- [ ] Testar geração de imagem

---

## 🎉 Após Configurar

**No Claude Code (terminal):**
```
Você: Gere uma imagem de um robô fofo

Eu: [ativo o MCP kie-nanobanana-create automaticamente]
    ✅ Imagem gerada!
    📄 robo_fofo_abc.png
    📂 ~/Downloads
```

**No Claude Desktop:**
```
Você: Crie 5 variações de produto em cores diferentes

Claude: [usa batch mode]
        ✅ 5 imagens em ~20s
        📂 Todas em ~/Downloads
```

---

## 📝 Importante

**Você NÃO precisa:**
- ❌ Mencionar o nome do MCP
- ❌ Pedir explicitamente para usar MCP
- ❌ Saber Python ou código

**Apenas:**
- ✅ Peça "Gere uma imagem..."
- ✅ Claude usa automaticamente!

---

**Status:** ✅ Configurado
**Próximo passo:** Reiniciar Claude Desktop
**Depois:** Usar normalmente!
