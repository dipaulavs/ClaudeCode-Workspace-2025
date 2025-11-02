# 📅 Sistema de Agendamento WhatsApp

## 📍 Localização

**Pasta:** `scheduling-system/`

**Script principal:** `scheduling-system/schedule_whatsapp.py`

---

## 🎯 O que faz

Sistema completo para agendar mensagens WhatsApp (únicas ou recorrentes) usando crontab do macOS + Evolution API.

---

## ⚡ Quick Start

```bash
# Da raiz do workspace
python3 scheduling-system/schedule_whatsapp.py \
  --phone 5531980160822 \
  --message "Sua mensagem aqui" \
  --time 17:00
```

---

## 📋 Comandos Disponíveis

### Agendar Mensagem Única

```bash
python3 scheduling-system/schedule_whatsapp.py \
  --phone 5531980160822 \
  --message "Mensagem de teste" \
  --time 17:00
```

### Agendar Mensagem Recorrente (Diária)

```bash
python3 scheduling-system/schedule_whatsapp.py \
  --phone 5531980160822 \
  --message "Bom dia!" \
  --time 09:00 \
  --daily
```

### Listar Agendamentos

```bash
python3 scheduling-system/schedule_whatsapp.py --list
```

### Remover Agendamento

```bash
python3 scheduling-system/schedule_whatsapp.py --remove [nome_da_tarefa]
```

### Remover Todos os Agendamentos

```bash
python3 scheduling-system/schedule_whatsapp.py --clear-all
```

---

## 🔧 Parâmetros

| Parâmetro | Obrigatório | Descrição | Exemplo |
|-----------|-------------|-----------|---------|
| `--phone` | ✅ | Número WhatsApp (DDI+DDD+Número) | `5531980160822` |
| `--message` | ✅ | Mensagem a enviar | `"Olá mundo!"` |
| `--time` | ✅ | Horário (HH:MM) | `17:00` |
| `--name` | ❌ | Nome da tarefa (auto se omitido) | `piada_diaria` |
| `--daily` | ❌ | Repetir diariamente | flag |
| `--list` | ❌ | Listar agendamentos | flag |
| `--remove` | ❌ | Remover tarefa específica | nome |
| `--clear-all` | ❌ | Remover todos | flag |

---

## 📂 Estrutura de Arquivos

```
scheduling-system/
├── README.md                    # Documentação completa
├── schedule_whatsapp.py         # Script principal
├── scheduled_tasks/             # Tarefas agendadas (.py)
│   ├── piada_diaria.py         # Exemplo: tarefa criada
│   └── examples/               # Exemplos antigos
├── logs/                        # Logs de execução
│   └── piada_diaria.log        # Log individual por tarefa
└── templates/                   # Templates futuros
```

---

## 💡 Exemplos de Uso

### Exemplo 1: Piada do Dia (17h todo dia)

```bash
python3 scheduling-system/schedule_whatsapp.py \
  --name piada_diaria \
  --phone 5531980160822 \
  --message "Por que o Python foi ao médico? Porque tinha muitos bugs! 🐛😄" \
  --time 17:00 \
  --daily
```

### Exemplo 2: Lembrete Pontual (Hoje às 14h)

```bash
python3 scheduling-system/schedule_whatsapp.py \
  --phone 5531999887766 \
  --message "🔔 Lembrete: Reunião em 30 minutos!" \
  --time 14:00
```

### Exemplo 3: Mensagem Motivacional (9h todo dia)

```bash
python3 scheduling-system/schedule_whatsapp.py \
  --name motivacao \
  --phone 5531980160822 \
  --message "🌅 Bom dia! Hoje será um ótimo dia! 💪" \
  --time 09:00 \
  --daily
```

---

## 🔄 Fluxo de Funcionamento

1. **Usuário executa comando** → `schedule_whatsapp.py --phone X --message Y --time Z`
2. **Script cria tarefa** → Gera arquivo Python em `scheduled_tasks/nome.py`
3. **Adiciona ao crontab** → Registra no agendador do macOS
4. **Horário chega** → Crontab executa automaticamente
5. **Envia mensagem** → Via Evolution API + WhatsApp Helper
6. **Grava log** → Salva resultado em `logs/nome.log`

---

## 📊 Como Funciona Internamente

### 1. Criação da Tarefa

Quando você agenda, o sistema:

1. Gera arquivo Python executável em `scheduled_tasks/`
2. Arquivo contém: número, mensagem, lógica de envio
3. Adiciona entrada no crontab do macOS

### 2. Execução (Crontab)

Linha do crontab gerada:

```bash
# Formato: MINUTO HORA * * * comando >> log 2>&1
17 14 * * * cd /path/workspace && python3 scheduling-system/scheduled_tasks/tarefa.py >> logs/tarefa.log 2>&1
```

### 3. Envio (WhatsApp Helper)

```python
from whatsapp_helper import whatsapp
whatsapp.send_message(phone, message)
```

---

## 🔍 Verificar Status

### Ver tarefas agendadas:

```bash
python3 scheduling-system/schedule_whatsapp.py --list
```

### Ver crontab diretamente:

```bash
crontab -l
```

### Ver logs:

```bash
# Log específico
cat scheduling-system/logs/piada_diaria.log

# Todos os logs
ls -lh scheduling-system/logs/

# Monitorar em tempo real
tail -f scheduling-system/logs/piada_diaria.log
```

---

## ⚠️ Requisitos

### Para funcionar corretamente:

1. ✅ **Mac ligado** no horário agendado
2. ✅ **Mac não pode estar em sleep mode**
3. ✅ **Evolution API ativa** (instância: lfimoveis)
4. ✅ **Internet funcionando**
5. ✅ **WhatsApp Helper configurado**

### Desativar suspensão automática:

```bash
sudo pmset -c sleep 0                # Nunca suspender quando plugado
sudo pmset -c displaysleep 10        # Tela apaga em 10 min
```

---

## 🛠️ Troubleshooting

### Mensagem não foi enviada?

**1. Verificar se está agendada:**
```bash
python3 scheduling-system/schedule_whatsapp.py --list
```

**2. Ver logs de erro:**
```bash
cat scheduling-system/logs/[nome_tarefa].log
```

**3. Testar manualmente:**
```bash
python3 scheduling-system/scheduled_tasks/[nome_tarefa].py
```

**4. Verificar crontab:**
```bash
crontab -l
```

### Tarefa não aparece na lista?

- Verifique se o comando de agendamento retornou sucesso
- Execute `crontab -l` para ver o crontab raw

### Evolution API não responde?

```bash
# Verificar status da API
curl https://evolution.loop9.com.br/instance/connectionState/lfimoveis

# Ver configuração
cat evolution-api-integration/config.py
```

---

## 🔐 Segurança

- ✅ Tarefas ficam apenas no seu Mac (local)
- ✅ Logs ficam apenas no seu Mac (local)
- ✅ Crontab é do seu usuário (isolado)
- ⚠️ **NUNCA** commite para git se tiver mensagens sensíveis

---

## 💰 Custo

**ZERO!** ✨

- Crontab: Nativo do macOS (grátis)
- Evolution API: Auto-hospedada (grátis)
- WhatsApp: Usa sua conta existente (grátis)

---

## 📱 Formato do Número

**Correto:** `5531980160822`

- `55` = DDI Brasil
- `31` = DDD
- `980160822` = Número (9 dígitos)

**Sem:** +, espaços, hífens, parênteses

---

## 🎯 Casos de Uso

| Caso de Uso | Comando | Recorrente |
|-------------|---------|------------|
| Piada às 17h hoje | `--time 17:00` | ❌ |
| Piada às 17h todo dia | `--time 17:00 --daily` | ✅ |
| Bom dia às 9h todo dia | `--time 09:00 --daily` | ✅ |
| Lembrete pontual | `--time 14:30` | ❌ |
| Relatório diário | `--time 18:00 --daily` | ✅ |

---

## 📚 Documentação Completa

**README da pasta:** `scheduling-system/README.md`

Contém:
- ✅ Exemplos detalhados
- ✅ Todos os parâmetros
- ✅ Troubleshooting completo
- ✅ Templates futuros

---

## 🔗 Integrações

- **Evolution API:** `evolution-api-integration/`
- **WhatsApp Helper:** `evolution-api-integration/whatsapp_helper.py`
- **Crontab:** Sistema nativo macOS

---

## 🆕 Versão

**Versão:** 1.0
**Criado:** 2025-11-01
**Status:** ✅ Ativo

---

## 📞 Como Solicitar ao Claude

**Frases que funcionam:**

- "Agende uma mensagem para às 17h no WhatsApp"
- "Crie um agendamento diário às 9h"
- "Quero enviar uma piada todo dia às 17h para o número X"
- "Liste meus agendamentos ativos"
- "Remova o agendamento de piadas"

**Claude vai:**
1. Reconhecer que é agendamento
2. Usar `scheduling-system/schedule_whatsapp.py`
3. Montar o comando correto
4. Executar e confirmar

---

**Última atualização:** 2025-11-01
