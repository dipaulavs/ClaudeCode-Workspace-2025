# ⏰ Configuração do Cron Job - Follow-ups

Instruções passo a passo para configurar o processamento automático de follow-ups.

---

## 🎯 Objetivo

Executar `processador_cron.py` a cada 5 minutos para enviar follow-ups pendentes.

---

## 🚀 Instalação

### 1. Verificar Python

```bash
# Verificar versão
python3 --version

# Verificar caminho
which python3
# Saída esperada: /usr/local/bin/python3
```

### 2. Testar Processador Manualmente

```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot

# Executar uma vez
python3 componentes/followup/processador_cron.py
```

**Saída esperada:**
```
============================================================
🔔 Processador de Follow-ups | 04/11/2025 14:30:00
============================================================

✓ Nenhum follow-up pendente no momento

============================================================
```

### 3. Dar Permissão de Execução

```bash
chmod +x componentes/followup/processador_cron.py
```

### 4. Configurar Cron

```bash
# Editar crontab
crontab -e
```

**Adicionar linha (pressione 'i' para inserir):**
```
*/5 * * * * /usr/local/bin/python3 /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/componentes/followup/processador_cron.py >> /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/logs/followup_cron.log 2>&1
```

**Salvar e sair (pressione ESC, depois ':wq', ENTER)**

### 5. Verificar Configuração

```bash
# Listar cron jobs
crontab -l

# Saída esperada:
# */5 * * * * /usr/local/bin/python3 ...
```

---

## 📊 Monitoramento

### Ver Logs em Tempo Real

```bash
tail -f /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/logs/followup_cron.log
```

### Ver Últimas 50 Linhas

```bash
tail -n 50 /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/logs/followup_cron.log
```

### Ver Todas as Execuções de Hoje

```bash
grep "$(date '+%d/%m/%Y')" /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/logs/followup_cron.log
```

---

## 🔍 Verificação de Funcionamento

### Método 1: Agendar Follow-up de Teste

```python
from componentes.followup import SistemaFollowUp
import time

sistema = SistemaFollowUp()

# Agendar follow-up para daqui 30 segundos
followup_data = {
    "id": "fu_teste",
    "cliente": "5531999999999",
    "trigger": "teste",
    "tipo": "teste",
    "mensagem": "Teste de cron",
    "tentativa": 1,
    "criado_em": time.time()
}

import json
sistema.redis_client.zadd(
    "followups",
    {json.dumps(followup_data): time.time() + 30}
)

print("✅ Follow-up de teste agendado para 30 segundos")
print("Aguarde e verifique logs...")
```

### Método 2: Verificar Última Execução

```bash
# Ver última linha do log
tail -n 1 /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/logs/followup_cron.log
```

**Se estiver funcionando, verá algo como:**
```
============================================================
```

---

## 🛠️ Troubleshooting

### Cron não está executando

**1. Verificar permissões de Full Disk Access (macOS)**

```
System Preferences → Security & Privacy → Privacy → Full Disk Access
→ Adicionar Terminal ou iTerm
```

**2. Verificar se cron está habilitado**

```bash
# macOS
sudo launchctl list | grep cron

# Se não estiver na lista:
sudo launchctl load -w /System/Library/LaunchDaemons/com.vix.cron.plist
```

**3. Verificar logs do sistema**

```bash
# macOS
tail -f /var/log/system.log | grep cron
```

### Erros no Log

**Erro: "ModuleNotFoundError"**

**Causa:** Python não encontra módulos.

**Solução:** Verificar caminho no cron:
```bash
# Adicionar PYTHONPATH no início do comando cron
PYTHONPATH=/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot */5 * * * * /usr/local/bin/python3 ...
```

**Erro: "Permission denied"**

**Causa:** Arquivo não tem permissão de execução.

**Solução:**
```bash
chmod +x componentes/followup/processador_cron.py
```

**Erro: "Connection refused" (Redis)**

**Causa:** Redis não está acessível.

**Solução:** Verificar credenciais em `sistema_followup.py`:
```python
REDIS_HOST = "usw1-popular-stallion-42128.upstash.io"
REDIS_PORT = 42128
REDIS_PASSWORD = "..."
```

---

## 🎛️ Ajustes de Frequência

### Executar a Cada 1 Minuto (Testes)

```
* * * * * /usr/local/bin/python3 ...
```

### Executar a Cada 10 Minutos

```
*/10 * * * * /usr/local/bin/python3 ...
```

### Executar a Cada 30 Minutos

```
*/30 * * * * /usr/local/bin/python3 ...
```

### Executar Apenas em Horário Comercial (9h-18h)

```
*/5 9-18 * * * /usr/local/bin/python3 ...
```

### Executar Apenas de Segunda a Sexta

```
*/5 * * * 1-5 /usr/local/bin/python3 ...
```

---

## 📧 Notificações de Erro (Opcional)

### Receber Email em Caso de Erro

```bash
# Adicionar no início do crontab
MAILTO=seu_email@gmail.com

*/5 * * * * /usr/local/bin/python3 ...
```

**Requisito:** Servidor SMTP configurado no sistema.

---

## 🧹 Manutenção de Logs

### Limpar Logs Antigos (Manual)

```bash
# Ver tamanho do log
ls -lh /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/logs/followup_cron.log

# Limpar (manter últimas 1000 linhas)
tail -n 1000 /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/logs/followup_cron.log > temp.log
mv temp.log /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/logs/followup_cron.log
```

### Rotação Automática de Logs (Cron Adicional)

```bash
# Adicionar ao crontab (executar todo domingo às 3h)
0 3 * * 0 tail -n 1000 /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/logs/followup_cron.log > /tmp/temp.log && mv /tmp/temp.log /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/logs/followup_cron.log
```

---

## ⏸️ Parar/Remover Cron

### Desabilitar Temporariamente

```bash
# Editar crontab
crontab -e

# Comentar linha (adicionar # no início)
# */5 * * * * /usr/local/bin/python3 ...
```

### Remover Completamente

```bash
# Editar crontab
crontab -e

# Deletar linha (pressione 'dd' na linha)
```

### Remover Todo Crontab

```bash
crontab -r
```

---

## 📋 Checklist de Instalação

- [ ] Python 3 instalado e caminho verificado
- [ ] `processador_cron.py` executado manualmente com sucesso
- [ ] Permissão de execução concedida (`chmod +x`)
- [ ] Cron job adicionado ao crontab
- [ ] Cron job listado em `crontab -l`
- [ ] Logs sendo gerados em `logs/followup_cron.log`
- [ ] Follow-up de teste enviado com sucesso
- [ ] Full Disk Access configurado (macOS)

---

## 🎯 Próximos Passos

Após configurar o cron:

1. **Monitorar primeiras execuções** (30 minutos)
2. **Verificar métricas** (`python3 componentes/followup/metricas.py`)
3. **Integrar com chatbot V4** (callbacks)
4. **Ajustar mensagens** baseado em feedback
5. **Analisar taxa de resposta** após 1 semana

---

## 📞 Suporte

**Problemas com cron:**
- Verificar logs: `tail -f logs/followup_cron.log`
- Executar manualmente: `python3 componentes/followup/processador_cron.py`

**Problemas com follow-ups:**
- Verificar Redis: Testar conexão
- Ver fila: `python3 -c "from componentes.followup import SistemaFollowUp; s = SistemaFollowUp(); print(s.redis_client.zrange('followups', 0, -1))"`
