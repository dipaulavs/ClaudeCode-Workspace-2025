# 📅 Agendamento WhatsApp - Claude Code

## ✅ Status: ATIVO

**Agendamento configurado com sucesso!**

---

## 📋 Detalhes da Configuração

- **Horário:** 06:58 da manhã (todos os dias)
- **Destinatário:** 5531980160822
- **Script:** `test_scheduled_whatsapp.py`
- **Log:** `whatsapp_schedule.log`

---

## 🔍 Como Verificar se Está Funcionando

### 1. Verificar o crontab ativo:
```bash
crontab -l
```

### 2. Ver logs de execução:
```bash
cat whatsapp_schedule.log
```

### 3. Testar manualmente:
```bash
python3 test_scheduled_whatsapp.py
```

---

## ⚙️ Gerenciar o Agendamento

### Desativar o agendamento:
```bash
crontab -r
```

### Editar o agendamento:
```bash
crontab -e
```

### Alterar o horário:
Formato: `MINUTO HORA * * *`
- Exemplo 06:58: `58 6 * * *`
- Exemplo 14:30: `30 14 * * *`
- Exemplo 22:00: `0 22 * * *`

---

## ⚠️ Importante

**Para o agendamento funcionar:**
1. ✅ Seu Mac precisa estar **ligado** às 06:58
2. ✅ Seu Mac **não pode estar dormindo** (ajuste configurações de energia)
3. ✅ A Evolution API precisa estar ativa

### Desativar suspensão automática (recomendado):
```bash
# Desativar suspensão enquanto conectado na energia
sudo pmset -c sleep 0
sudo pmset -c displaysleep 10  # Apenas a tela apaga após 10 min
```

---

## 📝 Arquivos Criados

- `test_scheduled_whatsapp.py` - Script de envio
- `crontab_temp.txt` - Configuração do crontab
- `whatsapp_schedule.log` - Log de execuções (será criado na primeira execução)
- `AGENDAMENTO_WHATSAPP.md` - Esta documentação

---

## 🚀 Próximos Passos

Se quiser criar mais agendamentos:
1. Duplique o script `test_scheduled_whatsapp.py`
2. Modifique a mensagem e destinatário
3. Adicione nova linha no crontab com `crontab -e`

---

**Agendado por:** Claude Code
**Data:** 2025-11-01
**Instância WhatsApp:** Evolution API (loop9)
