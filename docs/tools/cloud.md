# ☁️ Nextcloud Upload - Documentação Completa

Upload de arquivos no Nextcloud com links públicos automáticos.

---

## 📋 Índice

- [Quick Start](#-quick-start)
- [Scripts Disponíveis](#-scripts-disponíveis)
- [Configuração](#-configuração)
- [Exemplos de Uso](#-exemplos-de-uso)
- [API e Funcionalidades](#-api-e-funcionalidades)
- [Segurança](#-segurança)
- [Troubleshooting](#-troubleshooting)

---

## ⚡ Quick Start

### Caso 1: Upload Rápido (Arquivo Mais Recente)

```bash
# Pega o arquivo mais recente do Downloads e faz upload (expira em 24h)
python3 scripts/nextcloud/upload_from_downloads.py
```

### Caso 2: Buscar e Upload por Nome

```bash
# Busca "screenshot" no Downloads e faz upload
python3 scripts/nextcloud/upload_from_downloads.py --name "screenshot"
```

### Caso 3: Upload Manual de Arquivo Específico

```bash
# Upload de arquivo com caminho completo
python3 scripts/nextcloud/upload_to_nextcloud.py /caminho/completo/arquivo.jpg
```

---

## 🛠️ Scripts Disponíveis

### 1. upload_from_downloads.py

**Função:** Upload rápido da pasta Downloads

**Localização:** `scripts/nextcloud/upload_from_downloads.py`

**Recursos:**
- ✅ Pega automaticamente arquivo mais recente
- ✅ Busca por nome parcial
- ✅ Lista arquivos recentes
- ✅ Exibição de tamanho e data
- ✅ Links públicos temporários ou permanentes

**Sintaxe:**
```bash
python3 scripts/nextcloud/upload_from_downloads.py [opções]
```

**Opções:**
- `--name SEARCH` - Buscar arquivo por nome (parcial, case-insensitive)
- `--days DAYS` - Dias até expiração (padrão: 1)
- `--permanent` - Link permanente (sem expiração)
- `--folder FOLDER` - Pasta no Nextcloud (padrão: claude-code)
- `--rename FILENAME` - Renomear arquivo no upload
- `--list` - Listar 10 arquivos mais recentes

**Exemplos:**
```bash
# Upload arquivo mais recente
python3 scripts/nextcloud/upload_from_downloads.py

# Buscar "foto" nos Downloads
python3 scripts/nextcloud/upload_from_downloads.py --name "foto"

# Upload com 7 dias de expiração
python3 scripts/nextcloud/upload_from_downloads.py --name "relatorio" --days 7

# Link permanente
python3 scripts/nextcloud/upload_from_downloads.py --permanent

# Ver arquivos recentes
python3 scripts/nextcloud/upload_from_downloads.py --list
```

---

### 2. upload_to_nextcloud.py

**Função:** Upload de qualquer arquivo com caminho completo

**Localização:** `scripts/nextcloud/upload_to_nextcloud.py`

**Recursos:**
- ✅ Upload de qualquer arquivo/diretório
- ✅ Renomeação no upload
- ✅ Pastas customizadas
- ✅ Links temporários ou permanentes
- ✅ Suporte a todos os tipos de arquivo

**Sintaxe:**
```bash
python3 scripts/nextcloud/upload_to_nextcloud.py <arquivo> [opções]
```

**Opções:**
- `arquivo` - Caminho completo do arquivo (obrigatório)
- `--days DAYS` - Dias até expiração (padrão: 1)
- `--permanent` - Link permanente (sem expiração)
- `--folder FOLDER` - Pasta no Nextcloud (padrão: claude-code)
- `--rename FILENAME` - Renomear arquivo no upload

**Exemplos:**
```bash
# Upload simples (24h)
python3 scripts/nextcloud/upload_to_nextcloud.py foto.jpg

# Upload com 30 dias
python3 scripts/nextcloud/upload_to_nextcloud.py documento.pdf --days 30

# Link permanente
python3 scripts/nextcloud/upload_to_nextcloud.py video.mp4 --permanent

# Pasta customizada
python3 scripts/nextcloud/upload_to_nextcloud.py relatorio.xlsx --folder "relatorios-2024"

# Renomear no upload
python3 scripts/nextcloud/upload_to_nextcloud.py arquivo.jpg --rename "foto-final.jpg"
```

---

## 🔧 Configuração

### Arquivo de Configuração

**Localização:** `config/nextcloud_config.py`

```python
# Configurações do Nextcloud
NEXTCLOUD_URL = "https://media.loop9.com.br"
NEXTCLOUD_USER = "dipaula"
NEXTCLOUD_PASSWORD = "sua_senha"
NEXTCLOUD_FOLDER = "claude-code"

# Configurações de expiração
DEFAULT_EXPIRE_DAYS = 1  # 24 horas
```

### Variáveis de Ambiente (.env)

```bash
# Nextcloud Config
NEXTCLOUD_URL=https://media.loop9.com.br
NEXTCLOUD_USER=seu_usuario
NEXTCLOUD_PASSWORD=sua_senha
NEXTCLOUD_FOLDER=claude-code
```

**Prioridade:**
1. Variáveis de ambiente (.env)
2. Configuração hardcoded (config/nextcloud_config.py)

---

## 📖 Exemplos de Uso

### Caso 1: Screenshot Rápido

```bash
# Acabou de tirar um screenshot?
# Upload direto do arquivo mais recente:
python3 scripts/nextcloud/upload_from_downloads.py --name "screenshot"

# Resultado:
# 📄 Arquivo encontrado: Screenshot 2024-11-01 at 15.30.45.png (2.3 MB, 01/11/2024 15:30)
# 📤 Fazendo upload de Screenshot 2024-11-01 at 15.30.45.png...
# ✅ Upload concluído!
# 🔗 Criando link público (expira em 1 dia(s) - 02/11/2024)...
# ✅ Link público criado!
#
# ============================================================
# 🎉 SUCESSO!
# ============================================================
#
# 📎 URL Pública:
#
# https://media.loop9.com.br/s/abc123/download/Screenshot...png
#
# ⏰ Link expira em: 02/11/2024 às 23:59
```

### Caso 2: Compartilhar Documento (7 dias)

```bash
python3 scripts/nextcloud/upload_from_downloads.py --name "contrato" --days 7
```

### Caso 3: Foto Permanente

```bash
python3 scripts/nextcloud/upload_to_nextcloud.py ~/Pictures/familia.jpg --permanent
```

### Caso 4: Vídeo Grande (Upload Manual)

```bash
python3 scripts/nextcloud/upload_to_nextcloud.py ~/Desktop/video-apresentacao.mp4 --days 14
```

### Caso 5: Organizar em Pastas

```bash
# Upload em pasta "fotos-ferias-2024"
python3 scripts/nextcloud/upload_from_downloads.py --name "praia" --folder "fotos-ferias-2024"
```

### Caso 6: Renomear ao Fazer Upload

```bash
# Baixou "documento_final_v3_revisado.pdf"
# Mas quer compartilhar como "contrato.pdf"
python3 scripts/nextcloud/upload_from_downloads.py --name "documento" --rename "contrato.pdf"
```

---

## 🔌 API e Funcionalidades

### NextcloudUploader Class

```python
from config.nextcloud_config import *

uploader = NextcloudUploader(
    url=NEXTCLOUD_URL,
    user=NEXTCLOUD_USER,
    password=NEXTCLOUD_PASSWORD,
    folder=NEXTCLOUD_FOLDER
)

# Upload e link público
public_url = uploader.upload_and_share(
    local_path="foto.jpg",
    expire_days=7,
    custom_filename="minha-foto.jpg"
)

print(public_url)
# https://media.loop9.com.br/s/abc123/download/minha-foto.jpg
```

### Métodos Principais

#### create_folder()
```python
uploader.create_folder()
# Cria pasta no Nextcloud se não existir
# Retorna: True
```

#### upload_file(local_path, custom_filename=None)
```python
remote_path = uploader.upload_file("foto.jpg", custom_filename="nova-foto.jpg")
# Retorna: "claude-code/nova-foto.jpg"
```

#### create_public_link(remote_path, expire_days=None)
```python
url = uploader.create_public_link("claude-code/foto.jpg", expire_days=7)
# Retorna: "https://media.loop9.com.br/s/abc123/download/foto.jpg"
```

#### upload_and_share(local_path, expire_days=None, custom_filename=None)
```python
url = uploader.upload_and_share(
    local_path="foto.jpg",
    expire_days=7,
    custom_filename="minha-foto.jpg"
)
# Faz upload + cria link público
# Retorna: URL completa
```

---

## 🔒 Segurança

### Tipos de Links

#### Links Temporários (Recomendado)
- **Expiração:** 1-365 dias
- **Comportamento:** Nextcloud deleta arquivo automaticamente após expiração
- **Uso:** Dados sensíveis, compartilhamentos temporários
- **Comando:** `--days 7` (padrão: 1 dia)

```bash
python3 scripts/nextcloud/upload_from_downloads.py --days 7
```

#### Links Permanentes
- **Expiração:** Nunca
- **Comportamento:** Arquivo fica disponível indefinidamente
- **Uso:** Conteúdo público, arquivos de longa duração
- **Comando:** `--permanent`

```bash
python3 scripts/nextcloud/upload_from_downloads.py --permanent
```

### Permissões

Todos os links públicos criados têm **somente leitura**:
- ✅ Download permitido
- ❌ Upload bloqueado
- ❌ Edição bloqueada
- ❌ Exclusão bloqueada

### Boas Práticas

✅ **Faça:**
- Use links temporários para dados sensíveis
- Configure expiração adequada (1-30 dias típico)
- Links permanentes apenas para conteúdo público
- Armazene credenciais em variáveis de ambiente
- Use pastas organizadas (--folder)

❌ **Evite:**
- Links permanentes para dados sensíveis
- Compartilhar credenciais do Nextcloud
- Expiração muito longa sem necessidade
- Upload de arquivos maliciosos/ilegais

---

## 🚀 Performance e Limites

### Tempos Médios

| Tamanho | Tempo Upload (WiFi) | Tempo Upload (4G) |
|---------|---------------------|-------------------|
| 1 MB | ~1-2s | ~3-5s |
| 10 MB | ~5-10s | ~15-30s |
| 100 MB | ~30-60s | ~2-5min |
| 1 GB | ~5-10min | ~15-30min |

**Nota:** Tempos variam conforme conexão e carga do servidor.

### Limites do Sistema

| Item | Limite |
|------|--------|
| Tamanho arquivo | Configuração do servidor (geralmente 10GB+) |
| Upload simultâneo | Ilimitado (mas respeite o servidor) |
| Taxa de requisições | Sem limite (use com moderação) |
| Expiração mínima | 1 dia |
| Expiração máxima | Ilimitada (permanente) |

### Otimizações

- Scripts usam streams para upload (baixo uso de memória)
- Upload paralelo não implementado (pode ser adicionado)
- Compressão não implementada (NextCloud pode comprimir)

---

## ❌ Troubleshooting

### Erro: "Arquivo não encontrado"

**Problema:** Script não encontrou o arquivo

**Soluções:**
```bash
# 1. Verifique se o arquivo existe
ls -la ~/Downloads

# 2. Liste arquivos recentes
python3 scripts/nextcloud/upload_from_downloads.py --list

# 3. Use caminho absoluto
python3 scripts/nextcloud/upload_to_nextcloud.py /Users/seu-usuario/Downloads/arquivo.jpg
```

---

### Erro: "401 Unauthorized"

**Problema:** Credenciais inválidas

**Soluções:**
```bash
# 1. Verifique config/nextcloud_config.py
cat config/nextcloud_config.py

# 2. Teste manualmente via curl
curl -u "usuario:senha" https://media.loop9.com.br/remote.php/dav/files/usuario/

# 3. Configure .env
echo "NEXTCLOUD_USER=seu_usuario" >> .env
echo "NEXTCLOUD_PASSWORD=sua_senha" >> .env
```

---

### Erro: "Connection timeout"

**Problema:** Servidor inacessível

**Soluções:**
```bash
# 1. Teste conexão
ping media.loop9.com.br

# 2. Verifique URL
curl https://media.loop9.com.br

# 3. Verifique VPN/firewall
```

---

### Link não abre / 404

**Problema:** Link expirou ou inválido

**Soluções:**
1. Verifique se o link não expirou
2. Crie novo link com `--permanent`
3. Verifique se o arquivo existe no Nextcloud

---

### Upload muito lento

**Problema:** Conexão lenta ou arquivo grande

**Soluções:**
1. Verifique velocidade de upload: https://fast.com
2. Use WiFi ao invés de 4G
3. Comprima arquivo antes (zip/tar.gz)
4. Aguarde - arquivos grandes demoram

---

### Arquivo não aparece no Nextcloud

**Problema:** Upload falhou silenciosamente

**Soluções:**
```bash
# 1. Refaça upload com output
python3 scripts/nextcloud/upload_to_nextcloud.py arquivo.jpg 2>&1 | tee upload.log

# 2. Verifique pasta
curl -u "usuario:senha" https://media.loop9.com.br/remote.php/dav/files/usuario/claude-code/

# 3. Tente pasta diferente
python3 scripts/nextcloud/upload_to_nextcloud.py arquivo.jpg --folder "teste"
```

---

## 🎯 Workflows Comuns

### Workflow 1: Compartilhar Screenshot

```bash
# 1. Tira screenshot (cmd+shift+4 no Mac)
# 2. Executa:
python3 scripts/nextcloud/upload_from_downloads.py --name "screenshot"
# 3. Copia URL e envia para quem precisar
# 4. Link expira em 24h automaticamente
```

### Workflow 2: Backup Temporário

```bash
# 1. Faz backup de arquivo importante
# 2. Upload com 30 dias
python3 scripts/nextcloud/upload_to_nextcloud.py backup.zip --days 30
# 3. Guarda URL em lugar seguro
# 4. Após 30 dias, Nextcloud deleta automaticamente
```

### Workflow 3: Galeria Permanente

```bash
# 1. Organiza fotos em pasta local
# 2. Upload de cada foto como permanente
for foto in fotos/*.jpg; do
    python3 scripts/nextcloud/upload_to_nextcloud.py "$foto" --folder "galeria-2024" --permanent
done
# 3. Todas as URLs ficam disponíveis indefinidamente
```

### Workflow 4: Envio de Proposta

```bash
# 1. Gera proposta.pdf
# 2. Upload com 7 dias
python3 scripts/nextcloud/upload_to_nextcloud.py proposta.pdf --days 7 --rename "Proposta-Cliente-XYZ.pdf"
# 3. Envia URL para cliente
# 4. Após aceitação, faz upload permanente
python3 scripts/nextcloud/upload_to_nextcloud.py proposta-assinada.pdf --permanent
```

---

## 📚 Recursos Adicionais

### Documentação Relacionada

- **README Scripts:** `scripts/nextcloud/README.md`
- **Config:** `config/nextcloud_config.py`
- **Nextcloud API:** [WebDAV Documentation](https://docs.nextcloud.com/server/latest/developer_manual/client_apis/WebDAV/index.html)
- **Nextcloud Sharing:** [Sharing API](https://docs.nextcloud.com/server/latest/developer_manual/client_apis/OCS/ocs-share-api.html)

### Servidor Nextcloud

- **URL:** https://media.loop9.com.br
- **Interface Web:** Login com suas credenciais
- **WebDAV:** `https://media.loop9.com.br/remote.php/dav/files/usuario/`

### Ferramentas Relacionadas

- **Instagram Upload:** Usa Nextcloud para hospedar imagens antes do post
- **WhatsApp Bot:** Usa Nextcloud para armazenar fotos de imóveis

---

## 🤖 Uso com Claude Code

### Comandos Rápidos

```
"Faça upload da última imagem do Downloads"
→ python3 scripts/nextcloud/upload_from_downloads.py

"Upload do screenshot mais recente"
→ python3 scripts/nextcloud/upload_from_downloads.py --name "screenshot"

"Upload de arquivo.pdf com 7 dias de expiração"
→ python3 scripts/nextcloud/upload_to_nextcloud.py arquivo.pdf --days 7

"Liste os arquivos recentes do Downloads"
→ python3 scripts/nextcloud/upload_from_downloads.py --list
```

### Automações

Claude Code pode automaticamente:
1. Detectar quando você baixou um arquivo
2. Fazer upload no Nextcloud
3. Retornar a URL pública
4. Usar a URL em outras ferramentas (Instagram, WhatsApp, etc)

---

## 🔄 Atualizações Futuras

### Planejado

- [ ] Upload de pastas completas (recursivo)
- [ ] Upload paralelo (múltiplos arquivos)
- [ ] Compressão automática (zip)
- [ ] Integração com clipboard (copiar URL automaticamente)
- [ ] GUI simples (interface gráfica)
- [ ] Suporte a outros serviços cloud (Google Drive, Dropbox)

---

**Última atualização:** 2025-11-01
**Versão:** 1.0
**Autor:** Claude Code Workspace
