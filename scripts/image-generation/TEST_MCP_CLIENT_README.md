# MCP Image Generation Client Test

Cliente Python assíncrono para testar o MCP (Model Context Protocol) server de image generation.

## Arquivos

- **`test_mcp_client.py`** - Cliente de teste principal com 6 testes
- **`mcp-server/server_simple.py`** - Servidor MCP simplificado (funcional)
- **`mcp-server/server.py`** - Servidor MCP completo com SDK oficial (em desenvolvimento)

## Estrutura do Cliente

### Classe: `ImageGenMCPClient`

```python
cliente = ImageGenMCPClient(server_script_path)
await cliente.conectar()
resultado = await cliente.chamar_ferramenta(nome, parametros)
await cliente.desconectar()
```

**Métodos:**

- `conectar()` - Inicia servidor MCP via subprocess e envia handshake de inicialização
- `desconectar()` - Encerra servidor MCP gracefully
- `chamar_ferramenta(nome, parametros)` - Chama ferramenta via JSON-RPC 2.0
- `listar_ferramentas()` - Retorna lista de ferramentas disponíveis

### Context Manager

```python
async with conectar_mcp(server_path) as cliente:
    resultado = await cliente.chamar_ferramenta("generate_image", {...})
```

## Ferramentas Disponíveis

### 1. `generate_image`

Gera uma imagem usando a API especificada.

```python
await cliente.chamar_ferramenta("generate_image", {
    "prompt": "gato astronauta no espaço",
    "api": "nanobanana",  # ou "gpt4o", "sora"
    "quality": "standard"  # ou "high"
})
```

**Resposta:**
```json
{
    "status": "success",
    "tool": "generate_image",
    "api": "nanobanana",
    "prompt": "gato astronauta no espaço",
    "quality": "standard",
    "message": "Image generation framework ready for API integration",
    "image_url": "https://example.com/generated_nanobanana.png",
    "timestamp": "1234567.89"
}
```

### 2. `edit_image`

Edita uma imagem existente.

```python
await cliente.chamar_ferramenta("edit_image", {
    "image_url": "https://example.com/imagem.jpg",
    "operation": "resize",  # ou "crop", "enhance", "remove_bg"
    "parameters": {"width": 800, "height": 600}
})
```

**Resposta:**
```json
{
    "status": "success",
    "tool": "edit_image",
    "operation": "resize",
    "image_url": "https://example.com/imagem.jpg",
    "parameters": {"width": 800, "height": 600},
    "message": "Image editing framework ready for API integration",
    "edited_url": "https://example.com/edited_resize.png"
}
```

### 3. `batch_generate`

Gera múltiplas imagens em lote.

```python
await cliente.chamar_ferramenta("batch_generate", {
    "prompts": [
        "cachorro na praia",
        "gato em árvore",
        "flores selvagens"
    ],
    "api": "nanobanana"
})
```

**Resposta:**
```json
{
    "status": "success",
    "tool": "batch_generate",
    "api": "nanobanana",
    "prompts_count": 3,
    "prompts": ["cachorro na praia", "gato em árvore", "flores selvagens"],
    "message": "Batch generation framework ready for API integration",
    "generated_urls": [
        "https://example.com/batch_0_nanobanana.png",
        "https://example.com/batch_1_nanobanana.png",
        "https://example.com/batch_2_nanobanana.png"
    ]
}
```

## Executar Testes

```bash
# Python 3 (padrão, usa Python system)
python3 scripts/image-generation/test_mcp_client.py

# Python 3.11 (recomendado)
python3.11 scripts/image-generation/test_mcp_client.py
```

## Testes Incluídos

1. **Lista de Ferramentas** - Verifica se servidor retorna 3 ferramentas
2. **Generate Image (Nano Banana)** - Testa geração com API nanobanana
3. **Generate Image (GPT-4o)** - Testa geração com API gpt4o
4. **Edit Image** - Testa edição de imagem (resize)
5. **Batch Generate** - Testa geração em lote de 3 imagens
6. **Ferramenta Inválida** - Verifica tratamento de erro para ferramenta inexistente

## Saída Esperada

```
============================================================
🧪 TESTES DO CLIENTE MCP - IMAGE GENERATION
============================================================

1️⃣ Listando ferramentas disponíveis...
------------------------------------------------------------
🔌 Iniciando servidor MCP em: .../mcp-server/server_simple.py
✅ Cliente MCP conectado com sucesso
Ferramentas encontradas: 3
  • generate_image
  • edit_image
  • batch_generate
✅ Cliente MCP desconectado

[... mais testes ...]

============================================================
✅ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!
============================================================
```

## Protocolo JSON-RPC 2.0

O cliente comunica com o servidor via JSON-RPC 2.0 sobre stdin/stdout.

### Handshake de Inicialização

**Request:**
```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {
            "name": "test-client",
            "version": "1.0.0"
        }
    }
}
```

### Chamada de Ferramenta

**Request:**
```json
{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
        "name": "generate_image",
        "arguments": {
            "prompt": "gato astronauta",
            "api": "nanobanana"
        }
    }
}
```

**Response:**
```json
{
    "jsonrpc": "2.0",
    "id": 2,
    "result": [
        {
            "type": "text",
            "text": "{\"status\": \"success\", ...}"
        }
    ]
}
```

## Integração com Chatbots

Este cliente pode ser integrado em chatbots para chamar o MCP server:

```python
from scripts.image_generation.test_mcp_client import conectar_mcp
from pathlib import Path

# No seu chatbot
server_path = Path(__file__).parent.parent / "image-generation" / "mcp-server" / "server_simple.py"

async with conectar_mcp(str(server_path)) as cliente:
    # Listar ferramentas
    ferramentas = await cliente.listar_ferramentas()

    # Gerar imagem
    resultado = await cliente.chamar_ferramenta(
        "generate_image",
        {"prompt": "sua descrição aqui", "api": "nanobanana"}
    )

    image_url = resultado.get("image_url")
```

## Próximos Passos

1. **Integração de APIs Reais** - Conectar `generate_image` com Nano Banana API
2. **Autenticação** - Adicionar suporte a API keys seguros
3. **Cache** - Implementar cache de imagens geradas
4. **Webhooks** - Suportar gerações assíncronas com callbacks
5. **Logging** - Melhorar debug e monitoramento

## Requisitos

- Python 3.9+ (Python 3.11+ recomendado)
- asyncio (built-in)
- json (built-in)
- subprocess (built-in)

## Baseado Em

- `whatsapp-chatbot-carros/componentes/cliente_mcp.py` - Padrão de cliente MCP
- `whatsapp-chatbot-carros/mcp-server/server.py` - Estrutura de servidor MCP

## Status

✅ **Funcional** - Cliente testado e operacional com server_simple.py

🚧 **Em Desenvolvimento** - Integração com SDK oficial MCP em server.py
