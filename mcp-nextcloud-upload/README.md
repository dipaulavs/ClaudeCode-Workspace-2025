# 📦 Nextcloud Upload MCP Server

MCP Server para upload de imagens no Nextcloud com links públicos permanentes automáticos.

---

## 🎯 Features

```
1 MCP Server = 4 Tools
├─ mcp__nextcloud__upload_image      → Upload 1 imagem
├─ mcp__nextcloud__upload_batch      → Upload múltiplo (paralelo)
├─ mcp__nextcloud__scan_folder       → Escaneia ~/Pictures/upload/
└─ mcp__nextcloud__upload_from_scan  → Scan + Upload automático
```

**Características:**
- 📂 **Pasta fixa:** `imagens/upload/` (Nextcloud)
- ♾️  **Links permanentes** (sem expiração)
- 🗑️  **Auto-delete:** Apaga arquivo local após upload (configurável)
- ⚡ **Upload paralelo** para batch
- 🔄 **Async/await** nativo

---

## 📥 Instalação

### 1. Instalar dependências

```bash
cd mcp-nextcloud-upload
pip install -r requirements.txt
```

### 2. Configurar Claude Desktop

Editar `~/.claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "nextcloud-upload": {
      "command": "python3",
      "args": [
        "/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/mcp-nextcloud-upload/server.py"
      ]
    }
  }
}
```

**⚠️ Importante:** Usar caminho absoluto completo!

### 3. Reiniciar Claude Desktop

Fechar completamente e reabrir.

---

## 🚀 Uso

### Tool 1: upload_image

Upload de 1 imagem individual.

```json
{
  "file_path": "/Users/user/Pictures/foto.jpg",
  "auto_delete": true
}
```

**Retorno:**
```json
{
  "success": true,
  "filename": "foto.jpg",
  "url": "https://media.loop9.com.br/s/abc123/download/foto.jpg",
  "deleted": true,
  "error": ""
}
```

### Tool 2: upload_batch

Upload múltiplo em paralelo.

```json
{
  "file_paths": [
    "/Users/user/Pictures/foto1.jpg",
    "/Users/user/Pictures/foto2.jpg",
    "/Users/user/Pictures/foto3.jpg"
  ],
  "auto_delete": true
}
```

**Retorno:**
```json
{
  "success": true,
  "total": 3,
  "success_count": 3,
  "failed_count": 0,
  "results": [
    {
      "success": true,
      "filename": "foto1.jpg",
      "url": "https://media.loop9.com.br/s/xyz/download/foto1.jpg",
      "deleted": true,
      "error": ""
    },
    ...
  ]
}
```

### Tool 3: scan_folder

Escaneia `~/Pictures/upload/` e lista arquivos disponíveis.

```json
{}
```

**Retorno:**
```json
{
  "success": true,
  "folder": "/Users/user/Pictures/upload",
  "count": 5,
  "files": [
    {
      "filename": "foto1.jpg",
      "path": "/Users/user/Pictures/upload/foto1.jpg",
      "size": 2048576,
      "size_mb": 1.95,
      "modified": 1699123456.789
    },
    ...
  ]
}
```

### Tool 4: upload_from_scan

Workflow completo: escaneia pasta + upload automático.

```json
{
  "auto_delete": true
}
```

**Retorno:**
```json
{
  "success": true,
  "folder": "/Users/user/Pictures/upload",
  "total": 5,
  "success_count": 5,
  "failed_count": 0,
  "results": [...]
}
```

---

## 💬 Exemplos de Conversação

```
User: "Faz upload das fotos na pasta upload"
Claude: [usa mcp__nextcloud__upload_from_scan]
→ 5 fotos enviadas
→ 5 links públicos gerados
→ Arquivos locais deletados
```

```
User: "Quantas fotos tem na pasta de upload?"
Claude: [usa mcp__nextcloud__scan_folder]
→ 3 arquivos (4.2 MB total)
```

```
User: "Upload dessas 3 fotos mas mantém os arquivos locais"
Claude: [usa mcp__nextcloud__upload_batch com auto_delete: false]
→ 3 links gerados
→ Arquivos locais mantidos
```

---

## 🔧 Configuração

### Credenciais

Configuradas em `config/nextcloud_config.py`:

```python
NEXTCLOUD_URL = "https://media.loop9.com.br"
NEXTCLOUD_USER = "dipaula"
NEXTCLOUD_PASSWORD = "sua_senha"
```

### Pasta Local

Por padrão: `~/Pictures/upload/`

**Criar atalho no Finder:**
1. `⌘+Shift+G`
2. Digitar: `~/Pictures/upload/`
3. Arrastar pasta para Favoritos

---

## 📊 Workflow Recomendado

```
1. Joga imagens em: ~/Pictures/upload/
                ↓
2. Diz pro Claude: "Upload das fotos"
                ↓
3. Claude usa: mcp__nextcloud__upload_from_scan
                ↓
4. Recebe links públicos permanentes
                ↓
5. Arquivos locais deletados automaticamente
```

---

## 🎯 Casos de Uso

### 1. Carrossel Meta Ads (skill)

```python
# Antes (via Bash)
subprocess.run(["python3", "scripts/nextcloud/upload_rapido.py", "--from-local"])

# Agora (via MCP)
await mcp.upload_from_scan(auto_delete=True)
```

### 2. Chatbot WhatsApp (fotos de produtos)

```python
# Upload de fotos de imóveis/carros
results = await mcp.upload_batch(file_paths=[...])
urls = [r['url'] for r in results['results'] if r['success']]
```

### 3. Uso Manual

```
"Faz upload da foto X" → upload_image
"Upload de todas as fotos" → upload_from_scan
"Quantas fotos tem?" → scan_folder
```

---

## ⚡ Performance

| Operação | Tempo |
|----------|-------|
| Upload 1 imagem (1MB) | ~2-3s |
| Upload batch 5 imagens (paralelo) | ~3-5s |
| Scan folder | <1s |
| Upload + scan | ~3-6s |

**Paralelo vs Sequencial:**
- 5 imagens sequencial: ~10-15s
- 5 imagens paralelo (MCP): ~3-5s

---

## ❌ Troubleshooting

### MCP não aparece

```bash
# 1. Verificar instalação
pip list | grep mcp

# 2. Verificar config
cat ~/.claude_desktop_config.json

# 3. Testar server manualmente
python3 mcp-nextcloud-upload/server.py
```

### Erro 401 Unauthorized

```python
# Verificar credenciais em config/nextcloud_config.py
NEXTCLOUD_PASSWORD = "senha_correta"
```

### Pasta upload não existe

```bash
# Criar pasta
mkdir -p ~/Pictures/upload
```

### Arquivo não encontrado

```bash
# Verificar path absoluto
ls -la /caminho/completo/arquivo.jpg
```

---

## 🔗 Links

**Configuração:** `config/nextcloud_config.py`
**Script original:** `scripts/nextcloud/upload_rapido.py`
**Template MCP:** `scripts/image-generation/mcp-server/`
**Docs MCP:** https://github.com/anthropics/mcp-sdk-python

---

## 📚 Comparação Script vs MCP

```
SCRIPT PYTHON:                    MCP SERVER:
┌───────────────────┐            ┌───────────────────┐
│ Claude usa Bash   │            │ Claude usa tool   │
│ → Python script   │            │ nativo MCP        │
│ → Retorna output  │            │ (direto)          │
└───────────────────┘            └───────────────────┘
      ↓                                  ↓
┌───────────────────┐            ┌───────────────────┐
│ Lento (overhead)  │            │ Rápido (nativo)   │
│ Sem paralelismo   │            │ Paralelo built-in │
│ Parse output      │            │ JSON estruturado  │
└───────────────────┘            └───────────────────┘
```

**Vantagens MCP:**
- ✅ Integração nativa
- ✅ Upload paralelo (batch)
- ✅ Cache/persistent server
- ✅ Retorno estruturado (JSON)
- ✅ Reutilizável (skills/chatbots)

---

**Versão:** 1.0
**Última atualização:** 2025-11-05
