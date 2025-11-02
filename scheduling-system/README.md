# 📅 Sistema de Agendamento WhatsApp

Sistema centralizado para agendar mensagens WhatsApp para serem enviadas em horários específicos.

---

## 📂 Estrutura

```
scheduling-system/
├── README.md                    # Esta documentação
├── schedule_whatsapp.py         # Script principal
├── scheduled_tasks/             # Tarefas agendadas
│   └── examples/                # Exemplos e arquivos antigos
├── logs/                        # Logs de execução das tarefas
└── templates/                   # Templates de mensagens (futuro)
```

---

## 🚀 Como Usar

### 📍 Comando Base

```bash
cd scheduling-system
python3 schedule_whatsapp.py [opções]
```

Ou da raiz do workspace:

```bash
python3 scheduling-system/schedule_whatsapp.py [opções]
```

---

## 📋 Comandos Principais

### 1️⃣ Agendar Mensagem Única (Hoje)

```bash
python3 schedule_whatsapp.py \
  --phone 5531980160822 \
  --message "Olá! Esta é uma mensagem agendada" \
  --time 17:00
```

**Use quando:** Quer enviar algo hoje em um horário específico (aniversário, lembrete pontual, etc)

---

### 2️⃣ Agendar Mensagem Recorrente (Todos os Dias)

```bash
python3 schedule_whatsapp.py \
  --phone 5531980160822 \
  --message "Bom dia! Como está seu dia?" \
  --time 09:00 \
  --daily
```

**Use quando:** Quer enviar algo repetidamente no mesmo horário (piada diária, mensagem motivacional, etc)

---

### 3️⃣ Agendar com Nome Personalizado

```bash
python3 schedule_whatsapp.py \
  --name piada_diaria \
  --phone 5531980160822 \
  --message "Piada do dia: Por que o JavaScript foi ao psicólogo? Porque tinha muitos callbacks!" \
  --time 17:00 \
  --daily
```

**Use quando:** Quer identificar facilmente a tarefa depois (facilita remoção)

---

### 4️⃣ Listar Tarefas Agendadas

```bash
python3 schedule_whatsapp.py --list
```

**Mostra:** Todas as tarefas atualmente agendadas no sistema

---

### 5️⃣ Remover Tarefa Específica

```bash
python3 schedule_whatsapp.py --remove piada_diaria
```

**Use quando:** Quer cancelar uma tarefa específica sem afetar as outras

---

### 6️⃣ Remover TODAS as Tarefas

```bash
python3 schedule_whatsapp.py --clear-all
```

⚠️ **CUIDADO:** Remove todos os agendamentos! Pede confirmação antes.

---

## 💡 Exemplos Práticos

### Exemplo 1: Piada às 17h (Hoje)

```bash
python3 schedule_whatsapp.py \
  --phone 5531980160822 \
  --message "Por que o notebook foi ao médico? Porque estava com vírus! 😄" \
  --time 17:00
```

---

### Exemplo 2: Mensagem Motivacional Diária

```bash
python3 schedule_whatsapp.py \
  --name motivacao_matinal \
  --phone 5531980160822 \
  --message "🌅 Bom dia! Hoje vai ser um ótimo dia! Você é capaz de conquistar tudo que quiser! 💪" \
  --time 07:00 \
  --daily
```

---

### Exemplo 3: Lembrete de Reunião

```bash
python3 schedule_whatsapp.py \
  --name lembrete_reuniao \
  --phone 5531999887766 \
  --message "🔔 Lembrete: Reunião em 30 minutos! Link: https://meet.google.com/xxx" \
  --time 14:30
```

---

### Exemplo 4: Mensagem para Múltiplas Linhas

```bash
python3 schedule_whatsapp.py \
  --phone 5531980160822 \
  --message "📊 Relatório Diário:

✅ Vendas: R$ 5.000
📈 Leads: 15 novos
🎯 Meta: 80% atingida

Continue assim! 🚀" \
  --time 18:00 \
  --daily
```

---

## 🔍 Verificar Logs

Cada tarefa gera um log individual:

```bash
# Ver log de uma tarefa específica
cat logs/piada_diaria.log

# Ver logs em tempo real
tail -f logs/piada_diaria.log

# Ver todos os logs
ls -lh logs/
```

---

## ⚙️ Como Funciona

1. **Você agenda** → Script cria arquivo Python com sua tarefa
2. **Crontab registra** → Sistema macOS adiciona no agendador
3. **Horário chega** → Crontab executa automaticamente
4. **Mensagem enviada** → Evolution API envia para WhatsApp
5. **Log gravado** → Tudo registrado em `logs/`

---

## 📱 Formato do Número

**Correto:** `5531980160822`
- 55 (Brasil)
- 31 (DDD)
- 980160822 (número com 9 dígitos)

**Sem:** espaços, hífens, parênteses, +55

---

## ⚠️ Requisitos para Funcionar

### ✅ O que precisa estar ok:

1. **Mac ligado** no horário agendado
2. **Mac não pode estar dormindo** (ajuste energia)
3. **Evolution API ativa** (instância: lfimoveis)
4. **Internet funcionando**

### 🔧 Desativar suspensão automática:

```bash
# Desativar suspensão quando conectado na energia
sudo pmset -c sleep 0
sudo pmset -c displaysleep 10  # Apenas tela apaga após 10 min
```

---

## 🎯 Casos de Uso

| Situação | Comando | Recorrente? |
|----------|---------|-------------|
| Piada às 17h hoje | `--time 17:00` | Não |
| Piada às 17h todo dia | `--time 17:00 --daily` | Sim |
| Bom dia às 9h todo dia | `--time 09:00 --daily` | Sim |
| Lembrete reunião hoje 14h | `--time 14:00` | Não |
| Relatório diário 18h | `--time 18:00 --daily` | Sim |

---

## 🛠️ Troubleshooting

### Tarefa não executou?

```bash
# 1. Verificar se está agendada
python3 schedule_whatsapp.py --list

# 2. Verificar crontab diretamente
crontab -l

# 3. Ver logs de erro
cat logs/[nome_da_tarefa].log

# 4. Testar manualmente
python3 scheduled_tasks/[nome_da_tarefa].py
```

### Mensagem não enviou?

1. ✅ Evolution API está ativa?
2. ✅ Número está correto (formato: 5531980160822)?
3. ✅ Internet funcionando?
4. ✅ Mac estava ligado no horário?

---

## 📊 Gerenciamento de Tarefas

### Ver todas as tarefas criadas:

```bash
ls -lh scheduled_tasks/*.py
```

### Ver quando foi a última execução:

```bash
ls -lt logs/
```

### Deletar tarefa manualmente:

```bash
# 1. Remover do crontab
python3 schedule_whatsapp.py --remove nome_da_tarefa

# 2. Deletar arquivo (opcional)
rm scheduled_tasks/nome_da_tarefa.py
rm logs/nome_da_tarefa.log
```

---

## 🎨 Templates (Futuro)

A pasta `templates/` está preparada para templates de mensagens reutilizáveis:

```bash
templates/
├── piadas.txt           # Lista de piadas
├── motivacional.txt     # Frases motivacionais
├── vendas.txt           # Templates de vendas
└── aniversario.txt      # Mensagens de aniversário
```

*(Em desenvolvimento)*

---

## 📚 Arquivos de Exemplo

A pasta `scheduled_tasks/examples/` contém:

- `test_scheduled_whatsapp.py` - Script antigo de teste
- `EXEMPLO_ANTIGO.md` - Documentação anterior

Esses arquivos são referência de como o sistema funcionava antes da reorganização.

---

## 🔐 Segurança

- ✅ Scripts ficam locais (não sobem para git se configurado)
- ✅ Logs ficam locais
- ✅ Apenas você tem acesso ao crontab
- ⚠️ Nunca commite API keys ou números sensíveis

---

## 💰 Custo

**ZERO!** ✨

- Evolution API: Grátis (auto-hospedada)
- Crontab: Nativo do macOS
- WhatsApp: Usa sua conta existente

---

## 📞 Suporte

**Problemas?** Verifique:

1. Esta documentação (`README.md`)
2. Documentação geral: `docs/tools/scheduling_system.md`
3. Exemplos: `scheduled_tasks/examples/`
4. CLAUDE.md (seção de agendamento)

---

## 🎯 Quick Start

**3 passos para agendar sua primeira mensagem:**

```bash
# 1. Entrar na pasta
cd scheduling-system

# 2. Agendar
python3 schedule_whatsapp.py --phone 5531980160822 --message "Teste!" --time 17:00

# 3. Confirmar
python3 schedule_whatsapp.py --list
```

Pronto! Sua mensagem será enviada às 17h! 🚀

---

**Criado por:** Claude Code
**Data:** 2025-11-01
**Versão:** 1.0
**Localização:** `scheduling-system/`
