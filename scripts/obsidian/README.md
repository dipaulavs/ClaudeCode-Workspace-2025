# 🧠 Obsidian Automation Scripts

Scripts Python para integração e automação do Obsidian via Local REST API.

---

## 📋 Pré-requisitos

### 1. Plugin Instalado

✅ **Local REST API** instalado e ativado no Obsidian

**Como instalar:**
1. Abra Obsidian → Settings (⚙️)
2. Community plugins → Browse
3. Busque "Local REST API"
4. Install → Enable

### 2. API Key Configurada

Após instalar o plugin:
1. Settings → Local REST API
2. Copie a **API Key** gerada
3. Adicione ao `.env` do workspace:

```bash
echo 'OBSIDIAN_API_KEY=sua_api_key_aqui' >> .env
```

### 3. Dependências Python

```bash
pip3 install requests urllib3
```

---

## 🚀 Scripts Disponíveis

### 📝 Quick Note - Captura Rápida

Cria nota rápida no Inbox ou outra pasta.

```bash
# Nota rápida no Inbox
python3 scripts/obsidian/quick_note.py "Minha ideia genial"

# Nota em pasta específica
python3 scripts/obsidian/quick_note.py "Anotação importante" --folder knowledge

# Com título personalizado
python3 scripts/obsidian/quick_note.py "Conteúdo" --title "Meu Título"
```

**Opções de pasta:**
- `inbox` - Inbox (padrão)
- `ideas` - Ideias
- `projects` - Projetos
- `knowledge` - Conhecimento
- `automations` - Automações
- `resources` - Recursos

---

### 💡 Capture Idea - Captura de Ideias Estruturada

Cria nota de ideia com template estruturado.

```bash
# Ideia básica
python3 scripts/obsidian/capture_idea.py "App de Fitness"

# Com descrição
python3 scripts/obsidian/capture_idea.py "App de Fitness" --desc "App para treinos personalizados"

# Com tags
python3 scripts/obsidian/capture_idea.py "E-commerce Nicho" --tags "negocio,ecommerce" --desc "Loja online especializada"

# Completo
python3 scripts/obsidian/capture_idea.py "SaaS de Marketing" \
  --desc "Plataforma de automação de marketing" \
  --tags "negocio,saas,marketing" \
  --context "Mercado em crescimento, baixa concorrência local"
```

**Estrutura criada:**
- Descrição
- Contexto
- Próximos passos (checklist)
- Links relacionados
- Tags automáticas

---

### 📅 Create Daily - Criar Daily Note

Cria nota diária com estrutura padrão.

```bash
# Daily note de hoje
python3 scripts/obsidian/create_daily.py

# Data específica
python3 scripts/obsidian/create_daily.py --date 2025-11-01
```

**Estrutura da daily note:**
- ✅ Tarefas
- 📝 Notas do Dia
- 🎯 Projetos
- 💡 Ideias
- 🤖 Automações Executadas
- 📊 Métricas
- 🧠 Reflexões

---

### 📂 New Project - Criar Projeto Completo

Cria estrutura completa de projeto com múltiplos arquivos.

```bash
# Projeto básico
python3 scripts/obsidian/new_project.py "Meu Projeto"

# Com descrição
python3 scripts/obsidian/new_project.py "App Fitness" --desc "App de treinos personalizados"

# Completo
python3 scripts/obsidian/new_project.py "E-commerce" \
  --desc "Loja online de produtos fitness" \
  --goal "Lançar MVP em 3 meses"
```

**Estrutura criada:**
```
01 - Projetos/
└── Nome do Projeto/
    ├── README.md       # Visão geral
    ├── Tarefas.md      # To-dos
    └── Recursos.md     # Links e arquivos
```

---

## 🔧 Configuração

### Arquivo: `config/obsidian_config.py`

```python
# URL da API
OBSIDIAN_API_URL = "https://127.0.0.1:27124"

# API Key (configure no .env)
OBSIDIAN_API_KEY = os.getenv("OBSIDIAN_API_KEY", "")

# Caminho do vault
OBSIDIAN_VAULT_PATH = "/Users/.../Obsidian [meu cerebro]/dipaula/claude-code"
```

### Variáveis de Ambiente (.env)

```bash
# API Key do Obsidian
OBSIDIAN_API_KEY=sua_api_key_aqui
```

---

## 📂 Estrutura do Vault

```
claude-code/
├── 00 - Inbox/              # Captura rápida
├── 01 - Projetos/           # Gestão de projetos
├── 02 - Ideias/             # Banco de ideias
├── 03 - Conhecimento/       # Base de conhecimento
├── 04 - Automações/         # Docs de automações
├── 05 - Templates/          # Templates reutilizáveis
├── 06 - Daily Notes/        # Diário diário
└── 07 - Recursos/           # Arquivos e referências
```

Cada pasta tem um `README.md` explicativo.

---

## 🤖 Cliente Python (obsidian_client.py)

### Importar e Usar

```python
from obsidian_client import ObsidianClient

client = ObsidianClient()

# Criar nota
client.create_note("Minha Nota", "Conteúdo aqui", folder="inbox")

# Ler nota
content = client.read_note("00 - Inbox/Minha Nota.md")

# Atualizar nota
client.update_note("00 - Inbox/Minha Nota.md", "Novo conteúdo")

# Adicionar ao final
client.append_to_note("00 - Inbox/Minha Nota.md", "\n\nMais conteúdo")

# Buscar
results = client.search("palavra-chave")

# Daily note
client.create_daily_note()
client.log_to_daily("Evento importante")
```

### Funções de Conveniência

```python
from obsidian_client import quick_note, capture_idea

# Quick note
quick_note("Minha nota rápida", folder="inbox")

# Captura de ideia
capture_idea(
    title="Minha Ideia",
    description="Descrição aqui",
    tags=["negocio", "app"]
)
```

---

## 🔍 Troubleshooting

### ❌ "Não foi possível conectar ao Obsidian"

**Causas:**
1. Obsidian não está aberto
2. Plugin não está ativado
3. API não está rodando

**Solução:**
1. Abra o Obsidian
2. Settings → Community plugins → Local REST API → Enable
3. Verifique se está rodando em `https://127.0.0.1:27124`

---

### ❌ "API Key não configurada"

**Solução:**
```bash
# Obter API Key
# Obsidian → Settings → Local REST API → Copiar API Key

# Adicionar ao .env
echo 'OBSIDIAN_API_KEY=sua_key_aqui' >> .env
```

---

### ❌ "Certificado SSL inválido"

Isso é normal para API local. Os scripts já estão configurados com `VERIFY_SSL=False`.

---

## 📱 Sincronização iPhone

✅ **iCloud Drive ativo** - Todas as notas sincronizam automaticamente

**Setup no iPhone:**
1. Baixe [Obsidian](https://apps.apple.com/app/obsidian-connected-notes/id1557175442)
2. Abra vault `claude-code` do iCloud
3. Pronto! Sincronizado 🎉

---

## 🔗 Integrações com Workspace

### Documentar Automações

```python
from obsidian_client import ObsidianClient

client = ObsidianClient()

# Documentar execução
client.create_note(
    "Automação - WhatsApp Bot",
    "Configuração e logs do bot...",
    folder="automations"
)
```

### Salvar Outputs

```python
# Salvar resultado de scraping
result = "dados extraídos..."
client.create_note(
    f"Scraping Instagram - {datetime.now().strftime('%Y-%m-%d')}",
    result,
    folder="automations"
)
```

### Log em Daily Note

```python
# Registrar evento importante
client.log_to_daily("✅ Campanha Meta Ads criada com sucesso")
```

---

## 📖 Documentação API

- **Local REST API:** https://coddingtonbear.github.io/obsidian-local-rest-api/
- **Obsidian:** https://help.obsidian.md/

---

## ✨ Próximas Funcionalidades

- [ ] Transcrição de áudio → Nota
- [ ] Extração de conhecimento de URLs
- [ ] Geração de mapas mentais
- [ ] Resumo semanal automático
- [ ] Integração com IA para análise de ideias
- [ ] Templates adicionais
- [ ] Backup automático

---

**Última atualização:** 2025-11-02
**Criado por:** Claude Code
**Vault:** claude-code (iCloud)
