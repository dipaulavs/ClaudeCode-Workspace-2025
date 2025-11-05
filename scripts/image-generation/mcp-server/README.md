# MCP Server - Image Generation Tools

MCP (Model Context Protocol) server para geracao de imagens usando multiplas APIs.

## Ferramentas Disponíveis

### 1. `generate_nanobanana` - Nano Banana Image Generation IMPLEMENTADO

Gera imagens usando Nano Banana (Gemini 2.5 Flash).

**Características:**
- Formato fixo: Portrait 2:3
- Salva automaticamente em ~/Downloads com nome descritivo
- Suporta PNG ou JPEG
- Nomes de arquivo gerados em portugues baseados no prompt
- Aguarda conclusao com timeout de 300 segundos
- Função async completa: `generate_nanobanana_image()`

**Input Schema:**
```json
{
  "prompt": "string (obrigatório) - Descricao detalhada da imagem",
  "format": "PNG | JPEG (padrao: PNG)"
}
```

**Response:**
```json
{
  "success": bool,
  "image_url": "string - URL da imagem gerada",
  "file_path": "string - Caminho local do arquivo salvo",
  "error": "string - Mensagem de erro (se houver)"
}
```

### 2. `generate_image` - Generic Image Generation

Framework para geracao de imagem com multiplas APIs.

**Status:** Framework base implementado

### 3. `edit_image` - Image Editing

Framework para edicao de imagens.

**Status:** Framework base implementado

### 4. `batch_generate` - Batch Image Generation

Framework para geracao em lote de multiplas imagens.

**Status:** Framework base implementado

## Funcoes Async Implementadas

### Nucleo Nano Banana

```python
async def generate_nanobanana_image(prompt: str, format: str = "PNG") -> Dict
```

Funcao orquestradora que coordena:

1. **Criacao de tarefa** → `generate_image_async()`
2. **Monitoramento de status** → `wait_for_completion_async()`
3. **Download de imagens** → `download_image_async()`
4. **Manipulacao de nomes** → `create_descriptive_filename()`

### Funcoes de Suporte

- `generate_image_async()` - Submete requisicao ao API Nano Banana
- `check_status_async()` - Verifica status da tarefa
- `wait_for_completion_async()` - Aguarda conclusao com polling
- `download_image_async()` - Baixa e salva imagem localmente
- `translate_to_portuguese()` - Traduz prompt para portugues
- `create_descriptive_filename()` - Gera nome descritivo em PT-BR

## Configuracao

### Credenciais
- API Key: `fa32b7ea4ff0e9b5acce83abe09d2b06`
- Base URL: `https://api.kie.ai`
- Endpoints:
  - `POST /api/v1/jobs/createTask` - Criar tarefa
  - `GET /api/v1/jobs/recordInfo` - Verificar status

### Diretorios
- Downloads: `~/Downloads` (destino padrao das imagens)

## Instalacao

```bash
pip install aiohttp httpx requests mcp
python3 scripts/image-generation/mcp-server/server.py
```

## Fluxo de Execucao

```
Cliente MCP
    |
    v
[list_tools()] → Retorna ferramentas disponiveis
    |
    v
[call_tool(name, arguments)] → Roteia para handler
    |
    +---> handle_generate_nanobanana()
            |
            v
        generate_nanobanana_image(prompt, format)
            |
            +---> generate_image_async()
            |       └→ POST /api/v1/jobs/createTask
            |
            +---> wait_for_completion_async()
            |       └→ Loop: GET /api/v1/jobs/recordInfo
            |
            +---> download_image_async()
                    └→ GET image_url + Save ~/Downloads/
    |
    v
Return JSON result com sucesso/erro
```

## Status de Implementacao

✅ Funcao async `generate_nanobanana_image()` - COMPLETA
✅ Todas as funcoes de suporte - ASYNC IMPLEMENTADAS
✅ Handler MCP - IMPLEMENTADO
✅ Tool definition - IMPLEMENTADA
✅ Tratamento de erros - IMPLEMENTADO
⏳ `generate_image` - Framework base (placeholders)
⏳ `edit_image` - Framework base (placeholders)
⏳ `batch_generate` - Framework base (placeholders)

## Arquivo Original Migrado

Funcionalidade original migrada de:
- `tools/generate_image_nanobanana.py`

Melhorias:
- Funcoes async para melhor performance
- Integracao com protocolo MCP
- Suporte a multiplas APIs
- Framework extensivel
- Melhor tratamento de erros
