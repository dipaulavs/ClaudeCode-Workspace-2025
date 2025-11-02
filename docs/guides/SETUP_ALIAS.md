# 🚀 Setup - Claude Code Sem Permissões

Instruções para iniciar Claude Code automaticamente sem pedir permissões.

---

## 📋 Opções Disponíveis

### **Opção 1: Script Direto** (Mais simples)

Use o script `claude-start.sh` criado:

```bash
cd ~/Desktop/ClaudeCode-Workspace
./claude-start.sh
```

---

### **Opção 2: Alias Global** (Recomendado)

Crie um alias permanente no seu shell para iniciar de qualquer lugar.

#### **Para Zsh (padrão no Mac):**

```bash
# Abrir arquivo de configuração
nano ~/.zshrc

# Adicionar no final do arquivo:
alias cw='cd ~/Desktop/ClaudeCode-Workspace && claude --dangerously-skip-permissions'

# Salvar (Ctrl+O, Enter, Ctrl+X)

# Recarregar configuração
source ~/.zshrc
```

#### **Para Bash:**

```bash
# Abrir arquivo de configuração
nano ~/.bash_profile

# Adicionar no final do arquivo:
alias cw='cd ~/Desktop/ClaudeCode-Workspace && claude --dangerously-skip-permissions'

# Salvar (Ctrl+O, Enter, Ctrl+X)

# Recarregar configuração
source ~/.bash_profile
```

**Agora você pode usar em qualquer terminal:**
```bash
cw  # Entra no workspace e inicia Claude sem permissões
```

---

### **Opção 3: Função Shell Avançada** (Mais controle)

Adicione uma função ao seu `~/.zshrc` ou `~/.bash_profile`:

```bash
# Função Claude Workspace
cw() {
    cd ~/Desktop/ClaudeCode-Workspace
    echo "🚀 Iniciando Claude Code..."
    echo "📁 Workspace: ClaudeCode-Workspace"
    echo "📋 Auto-load: CLAUDE.md"
    echo ""
    claude --dangerously-skip-permissions "$@"
}
```

**Uso:**
```bash
cw              # Inicia normalmente
cw --help       # Passa argumentos para Claude
```

---

## ⚙️ Opções Adicionais do Claude

### Outras flags úteis:

```bash
# Sem permissões + modo verbose
claude --dangerously-skip-permissions --verbose

# Sem permissões + modelo específico
claude --dangerously-skip-permissions --model sonnet

# Sem permissões + sem cache
claude --dangerously-skip-permissions --no-cache
```

### Combinando no alias:

```bash
# Exemplo: sempre verbose
alias cw='cd ~/Desktop/ClaudeCode-Workspace && claude --dangerously-skip-permissions --verbose'
```

---

## 🔐 Sobre Skip Permissions

**O que faz:**
- `--dangerously-skip-permissions`: Não pede confirmação para executar comandos

**⚠️ Atenção:**
- Use APENAS em ambientes confiáveis
- Claude terá acesso total ao sistema
- Ideal para desenvolvimento/automação

**Segurança:**
- O arquivo `CLAUDE.md` tem regras de segurança
- Claude ainda seguirá boas práticas
- Pedirá confirmação para ações destrutivas importantes

---

## ✅ Verificar Configuração

Depois de configurar o alias:

```bash
# Testar alias
type cw

# Deve mostrar:
# cw is an alias for cd ~/Desktop/ClaudeCode-Workspace && claude --dangerously-skip-permissions
```

---

## 📁 Auto-load do CLAUDE.md

Quando você iniciar Claude no workspace, ele automaticamente:

1. ✅ Detecta arquivo `CLAUDE.md` na raiz
2. ✅ Carrega configurações e contexto
3. ✅ Lê estrutura do workspace
4. ✅ Conhece todas as ferramentas disponíveis
5. ✅ Sabe onde buscar documentação específica

**Você não precisa explicar nada!** Claude já sabe o que está disponível.

---

## 🎯 Uso Prático

### Antes (sem configuração):
```bash
cd ~/Desktop/ClaudeCode-Workspace
claude
# [pede permissões]
# "Leia README.md"
# "Quais ferramentas tenho?"
```

### Depois (com alias + CLAUDE.md):
```bash
cw
# 🚀 Já inicia sem permissões
# 📋 CLAUDE.md auto-carregado
# "Gere uma imagem de astronauta gato"
# ✅ Claude já sabe onde encontrar a ferramenta
```

---

## 🔄 Atualizar Configuração

Se mudar o caminho do workspace:

```bash
# Editar alias
nano ~/.zshrc

# Alterar caminho:
alias cw='cd /NOVO/CAMINHO/ClaudeCode-Workspace && claude --dangerously-skip-permissions'

# Recarregar
source ~/.zshrc
```

---

## 💡 Aliases Adicionais (Opcional)

Você pode criar mais aliases para tarefas específicas:

```bash
# Claude no projeto n8n
alias cn='cd ~/Desktop/ClaudeCode-Workspace/n8n-mcp-project && claude --dangerously-skip-permissions'

# Claude com modelo específico
alias cws='cd ~/Desktop/ClaudeCode-Workspace && claude --dangerously-skip-permissions --model sonnet'

# Iniciar chatbot
alias bot='cd ~/Desktop/ClaudeCode-Workspace/n8n-mcp-project && ./INICIAR_BOT_V4.sh'

# Parar chatbot
alias botstop='cd ~/Desktop/ClaudeCode-Workspace/n8n-mcp-project && ./PARAR_BOT_V4.sh'
```

---

## 📝 Exemplos de Uso

### Iniciar e usar ferramenta direto:

```bash
$ cw
🚀 Iniciando Claude Code...
📁 Workspace: ClaudeCode-Workspace
📋 Auto-load: CLAUDE.md

Claude> Gere uma imagem de "gato astronauta no espaço"

[Claude lê CLAUDE.md automaticamente]
[Sabe que existe generate_image.py]
[Lê docs/tools/generate_image.md]
[Executa comando correto]
✅ Imagem salva em ~/Downloads/gato_astronauta_espacial_a7f2.png
```

### Publicar no Instagram:

```bash
$ cw

Claude> Publique a última imagem gerada no Instagram com legenda "Explorando o cosmos 🚀"

[Claude já conhece publish_instagram_post.py]
[Lê docs/tools/publish_instagram_post.md]
[Executa comando]
✅ Post publicado no Instagram!
```

---

---

## 🎯 **Opção 4: Comando `claude` Global com Skip Permissions** (✅ CONFIGURADO)

**Status: ✅ ATIVO desde 2025-11-01**

Agora o comando `claude` **em qualquer pasta** já executa automaticamente com `--dangerously-skip-permissions`.

### Configuração no `~/.zshrc`:

```bash
# Claude Code - Always skip permissions (função para evitar recursão)
claude() {
  command claude --dangerously-skip-permissions "$@"
}
```

### Como funciona:

- **`claude()`** - Função que sobrescreve o comando `claude`
- **`command claude`** - Chama o binário original do Claude Code
- **`--dangerously-skip-permissions`** - Nunca pede confirmação
- **`"$@"`** - Repassa todos os argumentos extras

### Uso:

```bash
# Em QUALQUER pasta, simplesmente:
claude

# Com argumentos:
claude --model sonnet
claude --verbose
claude --help

# A flag --dangerously-skip-permissions é SEMPRE adicionada automaticamente!
```

### Verificar se está ativo:

```bash
type claude
# Deve mostrar: claude is a shell function from /Users/felipemdepaula/.zshrc
```

### Para desativar:

```bash
# Editar .zshrc
nano ~/.zshrc

# Comentar ou deletar as linhas da função claude()
# Recarregar
source ~/.zshrc
```

### ⚠️ Diferença dos outros aliases:

| Comando | Ação |
|---------|------|
| `claude` | ✅ Claude sem permissões (pasta atual) |
| `cw` | Claude sem permissões + entra no Workspace |
| `cn` | Claude sem permissões + entra no n8n-mcp-project |
| `bot` | Inicia Chatbot V4 |
| `botstop` | Para Chatbot V4 |

---

**Setup completo! 🎉**

Agora Claude Code inicia automaticamente com todo o contexto do workspace carregado e NUNCA pede permissões.
