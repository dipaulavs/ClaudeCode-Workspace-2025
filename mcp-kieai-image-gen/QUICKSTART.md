# ⚡ Quick Start - MCP KIE.AI Image Generator

## 🚀 Instalação em 3 Passos

### 1️⃣ Instalar Dependências

```bash
cd mcp-kieai-image-gen
chmod +x INSTALL.sh
./INSTALL.sh
```

### 2️⃣ Testar o Servidor

```bash
# Teste simples (lista ferramentas)
/opt/homebrew/bin/python3.11 test_simple.py

# Teste completo (gera uma imagem) - ~10s
/opt/homebrew/bin/python3.11 test_client.py
```

### 3️⃣ Configurar no Claude Desktop

Adicione no arquivo `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "kieai-image-gen": {
      "command": "/opt/homebrew/bin/python3.11",
      "args": [
        "/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/mcp-kieai-image-gen/server.py"
      ]
    }
  }
}
```

Reinicie o Claude Desktop.

## ✅ Verificação

Após reiniciar o Claude, você verá o ícone 🔌 na barra inferior. Clique e verifique se `kieai-image-gen` está listado e conectado.

## 🎨 Uso no Claude

```
Você: Gere uma imagem de um pôr do sol sobre o oceano com palmeiras

Claude: [usa generate_image automaticamente]
```

## 📖 Documentação Completa

Veja `README.md` para detalhes completos, exemplos e troubleshooting.

## ⚠️ Requisitos

- ✅ Python 3.10+ (já instalado: 3.11)
- ✅ API Key KIE.AI (já configurada)
- ✅ Bibliotecas: mcp, requests

## 🐛 Problemas?

### Erro: "Module 'mcp' not found"
```bash
/opt/homebrew/bin/python3.11 -m pip install mcp requests
```

### Servidor não aparece no Claude
1. Verifique o caminho no config
2. Teste: `/opt/homebrew/bin/python3.11 server.py`
3. Reinicie o Claude Desktop

### Timeout na geração
- Normal para prompts complexos
- API pode levar 5-15s
