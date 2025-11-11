# 🧠 Obsidian Integration - Documentação Completa

Integração completa do Obsidian com ClaudeCode-Workspace via Local REST API.

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Instalação](#instalação)
3. [Configuração](#configuração)
4. [Estrutura do Vault](#estrutura-do-vault)
5. [Scripts Disponíveis](#scripts-disponíveis)
6. [API Client](#api-client)
7. [Integrações](#integrações)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral

Sistema completo de automação do Obsidian que permite:

✅ **Captura automática** de ideias e notas
✅ **Gestão de projetos** estruturada
✅ **Base de conhecimento** organizada
✅ **Daily notes** automáticas
✅ **Sincronização** iCloud (Mac + iPhone)
✅ **Integração** com todas as ferramentas do workspace

### Tecnologias

- **Obsidian:** PKM (Personal Knowledge Management)
- **Local REST API:** Plugin oficial para API REST
- **Python:** Scripts de automação
- **iCloud Drive:** Sincronização multiplataforma

---

## 🚀 Instalação

### Passo 1: Instalar Obsidian

**Mac:**
```bash
# Via Homebrew
brew install --cask obsidian

# Ou baixar em: https://obsidian.md/
```

**iPhone:**
- [App Store - Obsidian](https://apps.apple.com/app/obsidian-connected-notes/id1557175442)

### Passo 2: Criar Vault no iCloud

1. Abra Obsidian
2. "Create new vault"
3. Nome: `claude-code` (ou personalizado)
4. **Localização:** `~/Library/Mobile Documents/com~apple~CloudDocs/Obsidian/`
   - ⚠️ Importante: Dentro do iCloud Drive para sincronizar

### Passo 3: Instalar Plugin Local REST API

1. Obsidian → Settings (⚙️)
2. **Community plugins** → Turn on
3. **Browse** → Buscar "Local REST API"
4. **Install** → **Enable**

### Passo 4: Configurar API Key

1. Settings → **Local REST API**
2. Copiar **API Key** gerada
3. Adicionar ao `.env` do workspace:

```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace
echo 'OBSIDIAN_API_KEY=sua_api_key_aqui' >> .env
```

### Passo 5: Instalar Dependências Python

```bash
pip3 install requests urllib3
```

---

## ⚙️ Configuração

### Arquivo: `config/obsidian_config.py`

```python
# URL da API (padrão local)
OBSIDIAN_API_URL = "https://127.0.0.1:27124"

# API Key (configurar no .env)
OBSIDIAN_API_KEY = os.getenv("OBSIDIAN_API_KEY", "")

# Caminho do vault
OBSIDIAN_VAULT_PATH = "/path/to/vault"

# Estrutura de pastas
FOLDERS = {
    "inbox": "00 - Inbox",
    "projects": "01 - Projetos",
    "ideas": "02 - Ideias",
    "knowledge": "03 - Conhecimento",
    "automations": "04 - Automações",
    "templates": "05 - Templates",
    "daily": "06 - Daily Notes",
    "resources": "07 - Recursos"
}
```

### Variáveis de Ambiente

**Arquivo: `.env`**
```bash
OBSIDIAN_API_KEY=sua_api_key_aqui
```

---

## 📂 Estrutura do Vault

```
claude-code/
│
├── 00 - Inbox/              # 📥 Captura rápida
│   └── README.md
│
├── 01 - Projetos/           # 💼 Gestão de projetos
│   ├── README.md
│   └── [Projetos]/
│       ├── README.md
│       ├── Tarefas.md
│       └── Recursos.md
│
├── 02 - Ideias/             # 💡 Banco de ideias
│   └── README.md
│
├── 03 - Conhecimento/       # 📚 Base de conhecimento
│   ├── README.md
│   └── [Tópicos]/
│
├── 04 - Automações/         # 🤖 Docs de automações
│   ├── README.md
│   └── [Ferramentas]/
│
├── 05 - Templates/          # 📋 Templates
│   ├── README.md
│   ├── Template - Projeto.md
│   ├── Template - Ideia.md
│   ├── Template - Conhecimento.md
│   └── Template - Reunião.md
│
├── 06 - Daily Notes/        # 📅 Diário diário
│   ├── README.md
│   └── [YYYY-MM-DD - Dia].md
│
├── 07 - Recursos/           # 📎 Arquivos
│   ├── README.md
│   ├── Imagens/
│   ├── PDFs/
│   └── Links/
│
└── ÍNDICE GERAL.md          # 🏠 Home do vault
```

### Filosofia de Organização

1. **00 - Inbox:** Tudo começa aqui (captura rápida)
2. **Processamento:** Revisar inbox diariamente
3. **Categorização:** Mover para pastas apropriadas
4. **Conexão:** Criar links entre notas relacionadas
5. **Refinamento:** Evoluir notas para conhecimento permanente

---

## 🛠️ Scripts Disponíveis

### 1. Quick Note (`quick_note.py`)

**Captura rápida de notas**

```bash
# Básico
python3 scripts/obsidian/quick_note.py "Minha ideia"

# Com pasta personalizada
python3 scripts/obsidian/quick_note.py "Nota importante" --folder knowledge

# Com título
python3 scripts/obsidian/quick_note.py "Conteúdo" --title "Meu Título"
```

**Quando usar:**
- Ideias rápidas
- Lembretes
- Anotações temporárias

---

### 2. Capture Idea (`capture_idea.py`)

**Captura estruturada de ideias**

```bash
# Básico
python3 scripts/obsidian/capture_idea.py "App de Fitness"

# Completo
python3 scripts/obsidian/capture_idea.py "SaaS Marketing" \
  --desc "Plataforma de automação" \
  --tags "negocio,saas" \
  --context "Mercado em crescimento"
```

**Estrutura gerada:**
- 💡 Descrição
- 🎯 Contexto
- ✨ Próximos passos
- 🔗 Links relacionados
- 🏷️ Tags automáticas

---

### 3. Create Daily (`create_daily.py`)

**Criar daily note**

```bash
# Hoje
python3 scripts/obsidian/create_daily.py

# Data específica
python3 scripts/obsidian/create_daily.py --date 2025-11-01
```

**Seções da daily note:**
- ✅ Tarefas
- 📝 Notas do Dia
- 🎯 Projetos
- 💡 Ideias
- 🤖 Automações Executadas
- 📊 Métricas
- 🧠 Reflexões

---

### 4. New Project (`new_project.py`)

**Criar projeto completo**

```bash
# Básico
python3 scripts/obsidian/new_project.py "Meu Projeto"

# Completo
python3 scripts/obsidian/new_project.py "E-commerce" \
  --desc "Loja online fitness" \
  --goal "Lançar MVP em 3 meses"
```

**Arquivos criados:**
- `README.md` - Visão geral do projeto
- `Tarefas.md` - Lista de to-dos
- `Recursos.md` - Links e referências

---

## 🐍 API Client (`obsidian_client.py`)

### Importar

```python
from scripts.obsidian.obsidian_client import ObsidianClient
```

### Criar Cliente

```python
client = ObsidianClient()

# Testar conexão
if client.test_connection():
    print("✅ Conectado!")
```

### Operações com Notas

```python
# Criar nota
client.create_note(
    path="Minha Nota",
    content="# Conteúdo\n\nTexto aqui",
    folder="inbox"  # opcional
)

# Ler nota
content = client.read_note("00 - Inbox/Minha Nota.md")

# Atualizar nota (sobrescrever)
client.update_note(
    path="00 - Inbox/Minha Nota.md",
    content="Novo conteúdo"
)

# Adicionar ao final
client.append_to_note(
    path="00 - Inbox/Minha Nota.md",
    content="\n\nMais texto"
)

# Deletar
client.delete_note("00 - Inbox/Minha Nota.md")
```

### Busca

```python
# Buscar por texto
results = client.search("palavra-chave")

# Listar todos os arquivos
files = client.list_files()
```

### Daily Notes

```python
# Criar daily note de hoje
client.create_daily_note()

# Data específica
from datetime import datetime
date = datetime(2025, 11, 1)
client.create_daily_note(date)

# Adicionar log na daily note de hoje
client.log_to_daily(
    message="Evento importante",
    section="📝 Notas do Dia"
)
```

### Funções de Conveniência

```python
from scripts.obsidian.obsidian_client import quick_note, capture_idea

# Quick note
quick_note("Minha nota", folder="inbox")

# Captura de ideia
capture_idea(
    title="Minha Ideia",
    description="Descrição",
    tags=["negocio", "app"]
)
```

---

## 🔗 Integrações com Workspace

### 1. Documentar Automações

```python
from scripts.obsidian.obsidian_client import ObsidianClient

client = ObsidianClient()

# Documentar configuração de bot
bot_config = """
# WhatsApp Bot V4 - Configuração

## Status
Ativo desde 2025-11-02

## Modelo
Claude Haiku 4.5

## Funcionalidades
- Transcrição de áudios
- Visão de imagens
- Memória conversacional
"""

client.create_note(
    "WhatsApp Bot V4",
    bot_config,
    folder="automations"
)
```

### 2. Salvar Outputs de Ferramentas

```python
# Após scraping Instagram
scraping_result = "Dados extraídos..."

client.create_note(
    f"Scraping Instagram - {datetime.now().strftime('%Y-%m-%d')}",
    f"# Scraping Instagram\n\n{scraping_result}",
    folder="automations"
)
```

### 3. Log de Execuções

```python
# Registrar execução importante
client.log_to_daily(
    "✅ Campanha Meta Ads 'Imóveis BH' criada com sucesso (ID: 123456)",
    section="🤖 Automações Executadas"
)
```

### 4. Captura de Ideias via IA

```python
# Ideia gerada por brainstorming com IA
ai_idea = "App de gestão de treinos com IA"

capture_idea(
    title=ai_idea,
    description="IA cria treinos personalizados baseados em objetivos",
    tags=["app", "ia", "fitness"]
)
```

---

## 📱 Sincronização iPhone

### Setup

1. **Instalar app:** [Obsidian iOS](https://apps.apple.com/app/obsidian-connected-notes/id1557175442)
2. **Abrir vault:** Selecionar `claude-code` do iCloud
3. **Sincronizar:** Automático via iCloud Drive

### Uso Mobile

- ✅ Todas as funcionalidades do desktop
- ✅ Plugins funcionam
- ✅ Sync bidirecional automático
- ✅ Captura rápida via mobile

---

## 🔍 Troubleshooting

### ❌ Erro: "Não foi possível conectar ao Obsidian"

**Causa:** Obsidian não está aberto ou plugin desativado

**Solução:**
1. Abrir Obsidian
2. Settings → Community plugins → Local REST API → Enable
3. Verificar se API está em `https://127.0.0.1:27124`

---

### ❌ Erro: "OBSIDIAN_API_KEY não configurada"

**Solução:**
```bash
# 1. Obter API Key
# Obsidian → Settings → Local REST API → Copiar key

# 2. Adicionar ao .env
echo 'OBSIDIAN_API_KEY=sua_key_aqui' >> .env

# 3. Recarregar ambiente ou reiniciar script
```

---

### ❌ Erro: "SSL Certificate Verify Failed"

**Causa:** API local usa certificado auto-assinado

**Solução:** Scripts já configurados com `VERIFY_SSL=False`. Isso é normal e seguro para API local.

---

### ❌ Sincronização iCloud lenta

**Solução:**
1. Verificar espaço no iCloud
2. Verificar conexão internet
3. Forçar sync: Fechar e reabrir Obsidian
4. Alternativa: Usar Obsidian Sync ($8/mês)

---

### ❌ Nota não aparece no iPhone

**Solução:**
1. Aguardar alguns segundos (sync iCloud)
2. No iPhone: Pull down para refresh
3. Verificar se vault correto está aberto
4. Reiniciar app Obsidian iOS

---

## 📊 Performance

| Operação | Latência |
|----------|----------|
| Criar nota | ~50-100ms |
| Ler nota | ~30-50ms |
| Buscar | ~100-200ms |
| Sync iCloud | ~5-30s |

---

## 🎯 Melhores Práticas

### 1. Captura Rápida

- Use `quick_note.py` para ideias instantâneas
- Não se preocupe com organização no Inbox
- Processe inbox diariamente

### 2. Daily Notes

- Crie daily note no início do dia
- Use como diário e registro de atividades
- Automações logam automaticamente

### 3. Projetos

- Use `new_project.py` para estrutura consistente
- Mantenha README.md atualizado
- Crie subpastas conforme necessário

### 4. Conhecimento

- Uma nota = um conceito
- Use suas próprias palavras
- Conecte com `[[links]]`

### 5. Tags

- Use tags consistentes
- Prefixos: `#ideia/`, `#projeto/`, `#conhecimento/`
- Evite tags demais

---

## 🚀 Próximas Funcionalidades

- [ ] Transcrição de áudio → Nota automática
- [ ] Extração de conhecimento de URLs
- [ ] Análise de ideias com IA
- [ ] Geração de mapas mentais
- [ ] Resumo semanal automático
- [ ] Backup automático para Nextcloud
- [ ] Integração com n8n
- [ ] Voice commands via WhatsApp

---

## 📖 Recursos

- **Local REST API Docs:** https://coddingtonbear.github.io/obsidian-local-rest-api/
- **Obsidian Help:** https://help.obsidian.md/
- **Zettelkasten Method:** https://zettelkasten.de/
- **PARA Method:** https://fortelabs.com/blog/para/

---

## 📞 Suporte

**Docs:**
- Este arquivo
- `scripts/obsidian/README.md`
- READMEs de cada pasta no vault

**Testes:**
```bash
# Testar conexão
python3 scripts/obsidian/obsidian_client.py

# Criar nota de teste
python3 scripts/obsidian/quick_note.py "Teste de integração"
```

---

**Última atualização:** 2025-11-02
**Criado por:** Claude Code
**Versão:** 1.0
**Vault:** Claude-code-ios (iCloud)
**Localização:** `/Users/felipemdepaula/Documents/Obsidian/Claude-code-ios/`
