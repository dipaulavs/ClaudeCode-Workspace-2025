# 🎯 Comandos Claude Code - Guia Rápido

## ⚡ BOTÕES DISPONÍVEIS

Todos os botões **copiam instantaneamente** - basta clicar, colar no terminal e dar Enter!

### 1. 🚀 **Iniciar Setup**
**Comando:**
```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace && bash iniciar.sh && cat README.md
```
**Função:** Inicializa o workspace e mostra todas as ferramentas disponíveis

---

### 2. ➕ **Nova Conversa**
**Comando:**
```
/new
```
**Função:** Limpa histórico completo e reinicia conversa (equivalente a `/reset` e `/clear`)

---

### 3. 🧹 **Limpar Histórico**
**Comando:**
```
/clear
```
**Função:** Remove histórico de mensagens mas mantém contexto menor

---

### 4. 📊 **Ver Contexto** (NOVO!)
**Comando:**
```
/context
```
**Função:** Mostra visualização do uso de contexto atual (grid colorido com estatísticas)

---

### 5. 💰 **Ver Custo** (NOVO!)
**Comando:**
```
/cost
```
**Função:** Exibe o custo total e duração da sessão atual

---

### 6. 🛠️ **Ver Ferramentas**
**Comando:**
```bash
ls tools/
```
**Função:** Lista todos os scripts Python disponíveis

---

### 7. 📁 **Últimos Arquivos**
**Comando:**
```bash
ls -lt ~/Downloads | head -10
```
**Função:** Mostra os 10 arquivos mais recentes em Downloads

---

## ⌨️ ATALHOS DE TECLADO

| Atalho | Comando | Descrição |
|--------|---------|-----------|
| `Ctrl+I` ou `Cmd+I` | Setup completo | Inicializa workspace |
| `Ctrl+N` ou `Cmd+N` | `/new` | Nova conversa |
| `Ctrl+K` ou `Cmd+K` | `/clear` | Limpar histórico |
| `Ctrl+Shift+C` | `/context` | Ver contexto |
| `Ctrl+Shift+D` | `/cost` | Ver custo |

---

## 📋 DIFERENÇAS ENTRE OS COMANDOS

### `/new` vs `/clear`

| Comando | Limpa Histórico | Reseta Contexto | Custo/Duração |
|---------|----------------|-----------------|---------------|
| `/new` | ✅ Completo | ✅ Total | ✅ Reseta |
| `/clear` | ✅ Completo | ⚠️ Parcial | ❌ Mantém |

**Use `/new` quando:**
- Quer começar 100% do zero
- Contexto muito grande
- Quer resetar contadores

**Use `/clear` quando:**
- Só quer limpar mensagens
- Quer manter parte do contexto
- Não quer perder estatísticas

---

## 💡 COMANDOS ÚTEIS DO CLAUDE CODE

### Navegação e Controle
```bash
/help          # Ajuda completa
/exit          # Sair do Claude Code
/config        # Abrir painel de configurações
```

### Gerenciamento
```bash
/new           # Nova conversa (reseta tudo)
/clear         # Limpar histórico
/reset         # Alias de /new
/compact       # Compactar histórico mas manter resumo
```

### Monitoramento
```bash
/context       # Visualizar uso de contexto (grid)
/cost          # Ver custo e duração da sessão
```

### Sessões e Trabalho
```bash
/add-dir       # Adicionar diretório de trabalho
/agents        # Gerenciar configurações de agentes
/bashes        # Listar e gerenciar tarefas em background
```

### Diagnóstico
```bash
/doctor        # Diagnosticar instalação do Claude Code
```

---

## 🎯 FLUXOS DE TRABALHO COMUNS

### Fluxo 1: Começar Nova Sessão
```
1. Clique "Nova Conversa" (ou Ctrl+N)
2. Cole no Claude Code: /new
3. Enter
4. Clique "Iniciar Setup" (ou Ctrl+I)
5. Cole no terminal bash
6. Enter
7. Pronto! Workspace inicializado
```

### Fluxo 2: Monitorar Uso
```
1. Clique "Ver Contexto" (ou Ctrl+Shift+C)
2. Cole: /context
3. Veja grid colorido com uso
4. Clique "Ver Custo" (ou Ctrl+Shift+D)
5. Cole: /cost
6. Veja quanto gastou e tempo de sessão
```

### Fluxo 3: Limpar Quando Necessário
```
Se contexto está grande mas não quer perder tudo:
→ Use /clear (Ctrl+K)

Se quer recomeçar do zero:
→ Use /new (Ctrl+N)
```

---

## 📊 ENTENDENDO `/context`

Quando você executa `/context`, verá:

```
████████████░░░░░░░░
█████████████████░░░
████████░░░░░░░░░░░░

📊 Context Statistics:
- Total tokens: 45,234 / 200,000
- Messages: 87
- Tools called: 23
```

**Cores:**
- 🟦 Azul = Mensagens do usuário
- 🟩 Verde = Respostas do Claude
- 🟨 Amarelo = Uso de ferramentas
- 🟥 Vermelho = Próximo do limite

---

## 💰 ENTENDENDO `/cost`

Quando você executa `/cost`, verá:

```
💰 Session Cost:
- Duration: 1h 23m
- Total cost: $2.34
- Input tokens: 123,456
- Output tokens: 45,678
- Tool calls: 23
```

**Útil para:**
- Saber quanto você gastou
- Ver duração da sessão
- Decidir quando fazer `/new` para resetar

---

## 🚀 EXEMPLO PRÁTICO COMPLETO

### Cenário: Gerar várias imagens e monitorar

```bash
# 1. Iniciar sessão limpa
/new

# 2. Ver workspace (botão ou comando manual)
bash iniciar.sh && cat README.md

# 3. Gerar imagens
python3 tools/generate_image_nanobanana.py "gato fofo"
python3 tools/generate_image_nanobanana.py "cachorro feliz"

# 4. Ver últimos arquivos (botão)
ls -lt ~/Downloads | head -10

# 5. Verificar uso de contexto
/context

# 6. Ver quanto gastou
/cost

# 7. Se contexto grande, limpar
/clear

# 8. Continuar trabalhando...
```

---

## 📱 USO NO CELULAR

Todos os botões e atalhos funcionam no mobile:

1. **Tocar no botão** → Comando copiado
2. **Tocar no terminal** → Focar
3. **Tocar e segurar** → Opção "Colar"
4. **Enter** → Executar

---

## ✅ CHECKLIST DE COMANDOS

### Comandos do Claude Code (use no Claude Code)
- [ ] `/new` - Nova conversa
- [ ] `/clear` - Limpar histórico
- [ ] `/context` - Ver uso
- [ ] `/cost` - Ver custo
- [ ] `/help` - Ajuda

### Comandos Bash (use no terminal bash)
- [ ] `bash iniciar.sh` - Iniciar workspace
- [ ] `ls tools/` - Ver ferramentas
- [ ] `ls ~/Downloads` - Ver arquivos
- [ ] `clear` - Limpar tela (bash)

---

## 🎨 VISUAL DOS BOTÕES

```
⚡ Clique para copiar:

[🚀 Iniciar Setup]  [➕ Nova Conversa]  [🧹 Limpar Histórico]

[📊 Ver Contexto]  [💰 Ver Custo]

[🛠️ Ver Ferramentas]  [📁 Últimos Arquivos]
```

**7 botões totais - 2 novos adicionados!**

---

## 🆘 FAQ

### P: Qual a diferença entre `/new` e `/clear`?

**R:** `/new` reseta TUDO (contexto, custos, duração). `/clear` só limpa o histórico de mensagens mas mantém parte do contexto e estatísticas.

### P: `/context` não mostra nada?

**R:** Certifique-se de colar no **Claude Code** (não no bash). Se estiver no bash, digite `claude` primeiro para entrar no Claude Code.

### P: `/cost` mostra $0?

**R:** Pode ser que você acabou de fazer `/new`. O custo é por sessão e reseta quando você usa `/new`.

### P: Quantos tokens tenho disponível?

**R:** Execute `/context` e veja o limite. Geralmente é 200,000 tokens por conversa.

---

## 🎉 RESUMO RÁPIDO

**7 Botões:**
1. 🚀 Setup
2. ➕ New
3. 🧹 Clear
4. 📊 Context (NOVO!)
5. 💰 Cost (NOVO!)
6. 🛠️ Tools
7. 📁 Files

**5 Atalhos:**
- Ctrl+I = Setup
- Ctrl+N = New
- Ctrl+K = Clear
- Ctrl+Shift+C = Context (NOVO!)
- Ctrl+Shift+D = Cost (NOVO!)

**Comandos principais:**
- `/new` = Recomeçar do zero
- `/clear` = Limpar histórico
- `/context` = Ver uso
- `/cost` = Ver gasto

---

**Recarregue a página e teste os novos botões!**

```
http://localhost:3000/chat.html
```
