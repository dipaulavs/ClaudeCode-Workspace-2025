# 📦 Nextcloud Upload Scripts

Scripts para upload de arquivos no Nextcloud com links públicos automáticos.

---

## 📋 Templates Disponíveis

| Script | Função | Status |
|--------|--------|--------|
| `upload_to_nextcloud.py` | Upload de qualquer arquivo com link público | ✅ Pronto |
| `upload_from_downloads.py` | Upload rápido da pasta Downloads | ✅ Pronto |
| `upload_rapido.py` | Upload de imagens para criativos com auto-delete | ✅ Pronto |

---

## ⚡ Quick Start

### Upload Rápido (Downloads)

```bash
# Upload do arquivo mais recente do Downloads (expira em 24h)
python3 scripts/nextcloud/upload_from_downloads.py

# Buscar arquivo por nome
python3 scripts/nextcloud/upload_from_downloads.py --name "imagem"

# Upload com expiração de 7 dias
python3 scripts/nextcloud/upload_from_downloads.py --days 7

# Upload permanente
python3 scripts/nextcloud/upload_from_downloads.py --permanent

# Listar arquivos recentes
python3 scripts/nextcloud/upload_from_downloads.py --list
```

### Upload Manual

```bash
# Upload de arquivo específico (expira em 24h)
python3 scripts/nextcloud/upload_to_nextcloud.py /caminho/arquivo.jpg

# Upload com expiração customizada
python3 scripts/nextcloud/upload_to_nextcloud.py arquivo.pdf --days 30

# Upload permanente
python3 scripts/nextcloud/upload_to_nextcloud.py arquivo.zip --permanent

# Upload em pasta customizada
python3 scripts/nextcloud/upload_to_nextcloud.py arquivo.jpg --folder "fotos-2024"

# Renomear no upload
python3 scripts/nextcloud/upload_to_nextcloud.py arquivo.jpg --rename "foto-final.jpg"
```

---

## 🔧 Configuração

### Variáveis de Ambiente (.env)

```bash
NEXTCLOUD_URL=https://media.loop9.com.br
NEXTCLOUD_USER=seu_usuario
NEXTCLOUD_PASSWORD=sua_senha
NEXTCLOUD_FOLDER=claude-code
```

### Config File

Configurações centralizadas em: `config/nextcloud_config.py`

```python
NEXTCLOUD_URL = "https://media.loop9.com.br"
NEXTCLOUD_USER = "dipaula"
NEXTCLOUD_PASSWORD = "sua_senha"
NEXTCLOUD_FOLDER = "claude-code"
DEFAULT_EXPIRE_DAYS = 1  # 24 horas
```

---

## 📖 Documentação Completa

### upload_to_nextcloud.py

**Upload de qualquer arquivo com link público**

```bash
python3 scripts/nextcloud/upload_to_nextcloud.py <arquivo> [opções]
```

**Opções:**
- `--days DAYS` - Dias até expiração (padrão: 1)
- `--permanent` - Link permanente (sem expiração)
- `--folder FOLDER` - Pasta no Nextcloud (padrão: claude-code)
- `--rename FILENAME` - Renomear arquivo no upload

**Exemplos:**
```bash
# Imagem expira em 24h
python3 scripts/nextcloud/upload_to_nextcloud.py foto.jpg

# PDF expira em 7 dias
python3 scripts/nextcloud/upload_to_nextcloud.py documento.pdf --days 7

# Link permanente
python3 scripts/nextcloud/upload_to_nextcloud.py video.mp4 --permanent

# Upload em pasta específica
python3 scripts/nextcloud/upload_to_nextcloud.py relatorio.xlsx --folder "relatorios-2024"
```

---

### upload_from_downloads.py

**Upload rápido da pasta Downloads**

```bash
python3 scripts/nextcloud/upload_from_downloads.py [opções]
```

**Opções:**
- `--name SEARCH` - Buscar arquivo por nome (parcial)
- `--days DAYS` - Dias até expiração (padrão: 1)
- `--permanent` - Link permanente (sem expiração)
- `--folder FOLDER` - Pasta no Nextcloud (padrão: claude-code)
- `--rename FILENAME` - Renomear arquivo no upload
- `--list` - Listar 10 arquivos mais recentes

**Exemplos:**
```bash
# Upload do arquivo mais recente
python3 scripts/nextcloud/upload_from_downloads.py

# Buscar "screenshot" nos Downloads
python3 scripts/nextcloud/upload_from_downloads.py --name "screenshot"

# Upload com 30 dias de expiração
python3 scripts/nextcloud/upload_from_downloads.py --name "relatorio" --days 30

# Ver arquivos recentes
python3 scripts/nextcloud/upload_from_downloads.py --list
```

**Como Funciona:**
1. Sem `--name`: Pega o arquivo mais recente do Downloads
2. Com `--name`: Busca por nome parcial (case-insensitive)
3. Se múltiplos arquivos: Escolhe o mais recente
4. Faz upload automático e gera link público

---

## 🎯 Casos de Uso

### 1. Screenshot Rápido
```bash
# Tirou screenshot? Upload direto:
python3 scripts/nextcloud/upload_from_downloads.py --name "screenshot"
```

### 2. Compartilhar Foto Temporária
```bash
# Foto expira em 24h
python3 scripts/nextcloud/upload_from_downloads.py --name "foto"
```

### 3. Documento Permanente
```bash
# PDF sem expiração
python3 scripts/nextcloud/upload_to_nextcloud.py contrato.pdf --permanent
```

### 4. Arquivo Grande (Vídeo)
```bash
# Upload de vídeo com 7 dias de expiração
python3 scripts/nextcloud/upload_from_downloads.py --name "video" --days 7
```

---

## 🔒 Segurança

### Links Públicos
- **Temporários:** Expiram automaticamente (padrão: 24h)
- **Permanentes:** Nunca expiram (use com cuidado)
- **Somente leitura:** Links não permitem edição/exclusão
- **Auto-delete:** Nextcloud deleta arquivo após expiração

### Boas Práticas
✅ Use links temporários para dados sensíveis
✅ Configure expiração adequada (1-30 dias)
✅ Links permanentes apenas para conteúdo público
✅ Credenciais em variáveis de ambiente (.env)

---

## 🚀 Performance

| Operação | Tempo Médio |
|----------|-------------|
| Upload 1MB | ~1-2s |
| Upload 10MB | ~5-10s |
| Upload 100MB | ~30-60s |
| Criar link | ~1s |

**Limites:**
- Tamanho máximo: Depende do servidor Nextcloud
- Taxa de upload: Depende da conexão
- Expiração mínima: 1 dia
- Expiração máxima: Ilimitada (permanente)

---

## ❌ Troubleshooting

### Erro: "Arquivo não encontrado"
```bash
# Verifique o caminho
ls -la ~/Downloads

# Liste arquivos recentes
python3 scripts/nextcloud/upload_from_downloads.py --list
```

### Erro: "401 Unauthorized"
```bash
# Verifique credenciais em config/nextcloud_config.py
# Ou configure variáveis de ambiente no .env
```

### Erro: "Connection timeout"
```bash
# Verifique conexão com servidor
curl https://media.loop9.com.br
```

### Link não abre
- Verifique se o link não expirou
- Tente criar link permanente com `--permanent`

---

## 📚 Recursos

**Configuração:** `config/nextcloud_config.py`
**Docs completa:** `docs/tools/cloud.md`
**Nextcloud API:** [WebDAV Docs](https://docs.nextcloud.com/server/latest/developer_manual/client_apis/WebDAV/index.html)

---

## 🤖 Uso com Claude Code

```
"Faça upload da última imagem do Downloads para o Nextcloud"
→ python3 scripts/nextcloud/upload_from_downloads.py

"Upload da foto.jpg com 7 dias de expiração"
→ python3 scripts/nextcloud/upload_to_nextcloud.py foto.jpg --days 7

"Liste os arquivos recentes do Downloads"
→ python3 scripts/nextcloud/upload_from_downloads.py --list
```

---

### upload_rapido.py

**Upload rápido de imagens para criativos com auto-delete**

```bash
python3 scripts/nextcloud/upload_rapido.py <arquivo(s)> [opções]
```

**Características:**
- 📂 **Pasta fixa:** `imagens/upload/`
- ♾️  **Links permanentes** (sem expiração)
- 🗑️  **Auto-delete:** Apaga arquivo local após upload
- 📸 **Múltiplos arquivos:** Upload em lote

**Opções:**
- `--name SEARCH` - Buscar arquivo no Downloads por nome

**Exemplos:**
```bash
# Upload da pasta local (~/Pictures/upload/)
python3 scripts/nextcloud/upload_rapido.py --from-local

# 1 imagem
python3 scripts/nextcloud/upload_rapido.py foto.jpg

# Múltiplas imagens
python3 scripts/nextcloud/upload_rapido.py foto1.jpg foto2.jpg foto3.jpg

# Buscar no Downloads
python3 scripts/nextcloud/upload_rapido.py --name "screenshot"

# Todas as fotos de um imóvel
python3 scripts/nextcloud/upload_rapido.py /path/imoveis/*.jpg
```

**Como Funciona:**
1. Upload para `imagens/upload/` (Nextcloud)
2. Cria link público permanente
3. Deleta arquivo local automaticamente
4. Retorna URL(s) pública(s)

**Workflow Recomendado:**
```
1. Jogue imagens em: ~/Pictures/upload/
2. Execute: python3 scripts/nextcloud/upload_rapido.py --from-local
3. Receba links permanentes
4. Arquivos locais deletados automaticamente
```

**Pasta Local:** `~/Pictures/upload/`
- Arraste imagens para essa pasta
- Use Finder: `⌘+Shift+G` → `~/Pictures/upload/`
- Atalho criado automaticamente

**Caso de Uso:**
- Upload de imagens para criativos de anúncios
- Imagens de imóveis para Meta Ads/Instagram
- Fotos que você quer compartilhar e não manter localmente

---

**Última atualização:** 2025-11-03
**Versão:** 1.1
