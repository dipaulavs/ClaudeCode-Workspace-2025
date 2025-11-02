# 🚀 Quick Start - Sistema de Agendamento WhatsApp

Guia rápido para começar a usar em 3 minutos!

---

## 📍 Onde Estou?

```bash
# Você está aqui:
scheduling-system/
```

---

## ⚡ 3 Comandos para Começar

### 1️⃣ Testar o Sistema (Ver Ajuda)

```bash
python3 schedule_whatsapp.py --help
```

**Mostra:** Todos os comandos disponíveis com exemplos

---

### 2️⃣ Agendar Sua Primeira Mensagem

```bash
python3 schedule_whatsapp.py \
  --phone 5531980160822 \
  --message "🎉 Olá! Esta é minha primeira mensagem agendada pelo Claude Code!" \
  --time 17:00
```

**Resultado:** Mensagem será enviada hoje às 17h

---

### 3️⃣ Verificar Agendamentos

```bash
python3 schedule_whatsapp.py --list
```

**Mostra:** Lista de todas as tarefas agendadas

---

## 🎯 Exemplos Práticos

### Piada Diária às 17h

```bash
python3 schedule_whatsapp.py \
  --name piada_diaria \
  --phone 5531980160822 \
  --message "Por que o JavaScript foi ao psicólogo? Porque tinha muitos callbacks! 😄" \
  --time 17:00 \
  --daily
```

---

### Mensagem Motivacional às 9h (Todo Dia)

```bash
python3 schedule_whatsapp.py \
  --name motivacao \
  --phone 5531980160822 \
  --message "🌅 Bom dia! Hoje será um ótimo dia! Você é capaz de tudo! 💪" \
  --time 09:00 \
  --daily
```

---

### Lembrete Pontual (Uma Vez)

```bash
python3 schedule_whatsapp.py \
  --phone 5531999887766 \
  --message "🔔 Lembrete: Reunião em 30 minutos! Link: https://meet.google.com/xxx" \
  --time 14:30
```

---

## 🔍 Gerenciar Agendamentos

### Ver o que está agendado:

```bash
python3 schedule_whatsapp.py --list
```

### Remover um agendamento específico:

```bash
python3 schedule_whatsapp.py --remove piada_diaria
```

### Remover TODOS os agendamentos:

```bash
python3 schedule_whatsapp.py --clear-all
```

---

## 📂 Ver Logs

```bash
# Ver log de uma tarefa
cat logs/piada_diaria.log

# Ver todos os logs
ls -lh logs/
```

---

## ✅ Checklist para Funcionar

Antes de agendar, certifique-se:

- [ ] Mac vai estar **ligado** no horário agendado
- [ ] Mac **não vai estar dormindo** (ajuste energia)
- [ ] Evolution API está **ativa**
- [ ] Número está no formato correto (5531980160822)

---

## 📱 Formato do Número

✅ **Correto:** `5531980160822`
- 55 = Brasil
- 31 = DDD
- 980160822 = Número

❌ **Errado:**
- `+55 31 98016-0822`
- `(31) 98016-0822`
- `55 31 980160822`

---

## 💡 Dicas

### 1. Usar nome personalizado facilita:

```bash
--name piada_diaria    # ✅ Fácil de lembrar e remover depois
```

Sem nome, o sistema gera automaticamente: `whatsapp_task_20251101_143020`

### 2. Mensagens de múltiplas linhas:

```bash
python3 schedule_whatsapp.py \
  --phone 5531980160822 \
  --message "Linha 1
Linha 2
Linha 3" \
  --time 17:00
```

### 3. Verificar antes de executar:

Sempre teste com `--list` depois de agendar para confirmar

---

## 🛑 Parar/Remover

### Remover tarefa específica:

```bash
# 1. Listar para ver o nome
python3 schedule_whatsapp.py --list

# 2. Remover pelo nome
python3 schedule_whatsapp.py --remove [nome_da_tarefa]
```

### Limpar tudo:

```bash
python3 schedule_whatsapp.py --clear-all
```

⚠️ Pede confirmação antes de remover tudo

---

## 📚 Documentação Completa

**Quer mais detalhes?**

- `README.md` (nesta pasta) - Documentação completa
- `docs/tools/scheduling_system.md` - Docs técnica
- `CLAUDE.md` (raiz) - Quick Actions

---

## 🆘 Problemas?

### Mensagem não foi enviada?

```bash
# 1. Ver logs
cat logs/[nome_tarefa].log

# 2. Testar manualmente
python3 scheduled_tasks/[nome_tarefa].py

# 3. Verificar Evolution API
curl https://evolution.loop9.com.br/instance/connectionState/lfimoveis
```

### Tarefa não aparece na lista?

```bash
# Verificar crontab diretamente
crontab -l
```

---

## 🎉 Pronto!

Você já sabe o básico! Comece agendando sua primeira mensagem:

```bash
python3 schedule_whatsapp.py \
  --phone 5531980160822 \
  --message "Teste do sistema de agendamento! 🚀" \
  --time 17:00
```

**Boa sorte!** 🍀
