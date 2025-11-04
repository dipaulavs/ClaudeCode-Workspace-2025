# ⏰ Configuração do Cron - Relatórios Automáticos

Guia completo para configurar envio automático de relatórios.

## 📋 Pré-requisitos

1. Redis rodando (porta 6379)
2. Python 3.8+ instalado
3. Scripts WhatsApp configurados
4. Número do gestor em `chatwoot_config.json`

## 🚀 Configuração Passo a Passo

### 1. Verificar Python

```bash
# Encontrar caminho do Python
which python3
# Exemplo: /usr/local/bin/python3

# Verificar versão
python3 --version
# Deve ser >= 3.8
```

### 2. Testar Script Manualmente

```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot

# Testar geração de relatório
python3 componentes/relatorios/cron_diario.py

# Deve imprimir relatório e tentar enviar
```

### 3. Configurar Número do Gestor

Editar `chatwoot_config.json`:

```json
{
  "chatwoot_url": "http://localhost:3000",
  "chatwoot_token": "seu_token",
  "relatorios": {
    "numero_gestor": "5531980160822"
  }
}
```

### 4. Criar Diretório de Logs

```bash
mkdir -p /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/logs
```

### 5. Configurar Crontab

```bash
# Abrir editor de crontab
crontab -e
```

**Adicionar linhas:**

```cron
# Relatório diário às 18h
0 18 * * * /usr/local/bin/python3 /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/componentes/relatorios/cron_diario.py >> /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/logs/relatorio_cron.log 2>&1

# Dashboard semanal às 9h de segunda-feira
0 9 * * 1 /usr/local/bin/python3 /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/componentes/relatorios/cron_semanal.py >> /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/logs/relatorio_semanal.log 2>&1
```

**Salvar e sair:**
- Vim: pressione `Esc`, depois `:wq` e `Enter`
- Nano: pressione `Ctrl+X`, depois `Y` e `Enter`

### 6. Verificar Instalação

```bash
# Listar cron jobs
crontab -l

# Deve mostrar as duas linhas adicionadas
```

## 🔍 Testando

### Teste Manual Imediato

Ao invés de esperar 18h, force execução:

```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot

# Executar script diretamente
python3 componentes/relatorios/cron_diario.py

# Verificar se relatório foi enviado
tail -f logs/relatorio_cron.log
```

### Teste com Cron (espera alguns minutos)

```bash
# Editar crontab temporariamente
crontab -e

# Adicionar teste: executar 2 minutos no futuro
# Se agora são 14:35, configure para 14:37:
37 14 * * * /usr/local/bin/python3 /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/componentes/relatorios/cron_diario.py >> /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/logs/relatorio_cron.log 2>&1

# Aguardar e verificar log
tail -f /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/logs/relatorio_cron.log
```

**Se funcionar:**
- Remover linha de teste
- Manter apenas horário correto (18h)

## 📊 Criando Script Semanal

Criar `componentes/relatorios/cron_semanal.py`:

```python
#!/usr/bin/env python3
"""
Gerador de relatório semanal
Executado via cron: 0 9 * * 1 (segunda-feira 9h)
"""

import sys
import json

sys.path.insert(0, '/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot')

from componentes.relatorios import DashboardSemanal, GeradorRelatorio


def main():
    """Gera e envia relatório semanal"""
    try:
        # Carrega config
        config_path = '/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/chatwoot_config.json'

        with open(config_path, 'r') as f:
            config = json.load(f)

        numero_gestor = config.get('relatorios', {}).get('numero_gestor', '5531980160822')

        # Gera dashboard
        dashboard = DashboardSemanal()
        relatorio = dashboard.gerar_relatorio_semanal()

        print("📊 Dashboard semanal gerado:")
        print(relatorio)
        print()

        # Envia
        gerador = GeradorRelatorio()
        sucesso = gerador.enviar_relatorio(relatorio, numero_gestor)

        if sucesso:
            print("✅ Dashboard semanal enviado")
            return 0
        else:
            print("❌ Falha ao enviar dashboard")
            return 1

    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
```

```bash
# Tornar executável
chmod +x /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/componentes/relatorios/cron_semanal.py
```

## 🔧 Troubleshooting

### Problema: Cron não executa

**Sintoma:** Nada no log após horário programado

**Soluções:**

1. **Verificar permissões do cron (macOS):**

```bash
# Abrir Preferências do Sistema → Segurança e Privacidade → Privacidade
# Selecionar "Acesso Total ao Disco"
# Adicionar: /usr/sbin/cron
```

2. **Verificar logs do sistema:**

```bash
# macOS
log show --predicate 'process == "cron"' --info --last 1h

# Linux
grep CRON /var/log/syslog
```

3. **Testar com script simples:**

```bash
crontab -e

# Adicionar linha de teste:
* * * * * echo "Cron funciona - $(date)" >> /tmp/cron_test.log

# Aguardar 1 minuto e verificar:
cat /tmp/cron_test.log
```

### Problema: Script executa mas não envia

**Sintoma:** Log mostra "Relatório gerado" mas não "enviado"

**Soluções:**

```bash
# Verificar se Evolution API está rodando
curl http://localhost:8080/

# Testar envio manual
python3 /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/scripts/whatsapp/send_message.py \
  --phone 5531980160822 \
  --message "Teste cron"

# Ver erro específico no log
tail -50 /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/logs/relatorio_cron.log
```

### Problema: Redis não conecta

**Sintoma:** Erro "Connection refused"

**Soluções:**

```bash
# Verificar se Redis está rodando
redis-cli ping
# Deve retornar: PONG

# Se não estiver, iniciar:
redis-server &

# Verificar porta
redis-cli -p 6379 ping
```

### Problema: Métricas zeradas

**Sintoma:** Relatório mostra todos os valores como 0

**Soluções:**

```bash
# Verificar se há dados no Redis
redis-cli keys "metricas:*"

# Popular dados de teste
python3 -c "
from componentes.relatorios import IntegradorMetricas
integrador = IntegradorMetricas()
integrador.on_nova_conversa('5531980160822')
integrador.on_bot_respondeu('5531980160822')
print('Dados populados')
"

# Gerar relatório novamente
python3 componentes/relatorios/cron_diario.py
```

## 📅 Horários Recomendados

| Relatório | Horário | Frequência | Justificativa |
|-----------|---------|------------|---------------|
| **Diário** | 18h | Todos os dias | Final do expediente, gestor revisa antes de sair |
| **Semanal** | 9h segunda | Semanal | Início da semana, planejamento |

**Customizar horários:**

```cron
# Diário às 20h (pós-expediente)
0 20 * * * /usr/local/bin/python3 .../cron_diario.py >> .../relatorio_cron.log 2>&1

# Semanal às 8h sexta (final da semana)
0 8 * * 5 /usr/local/bin/python3 .../cron_semanal.py >> .../relatorio_semanal.log 2>&1
```

## 📱 Notificações Adicionais

### Enviar por Email (opcional)

```bash
# Instalar mail
brew install mailutils  # macOS

# Adicionar ao cron
0 18 * * * /usr/local/bin/python3 .../cron_diario.py | mail -s "Relatório Diário" gestor@empresa.com
```

### Webhook para Slack (opcional)

```python
# Adicionar ao final de cron_diario.py
import requests

webhook_url = "https://hooks.slack.com/services/..."
requests.post(webhook_url, json={
    "text": f"📊 Relatório diário enviado para {numero_gestor}"
})
```

## ✅ Checklist de Configuração

- [ ] Redis instalado e rodando
- [ ] Python 3.8+ instalado
- [ ] Scripts WhatsApp funcionando
- [ ] Número gestor em `chatwoot_config.json`
- [ ] Diretório `logs/` criado
- [ ] Crontab configurado (diário)
- [ ] Crontab configurado (semanal)
- [ ] Teste manual executado com sucesso
- [ ] Teste com cron executado com sucesso
- [ ] Logs monitorados por 1 semana

## 🎯 Validação Final

Após 1 semana de uso:

```bash
# Verificar logs
tail -100 /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/logs/relatorio_cron.log

# Contar execuções bem-sucedidas
grep "✅ Relatório enviado" /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/logs/relatorio_cron.log | wc -l
# Deve ser >= 7 (uma por dia)

# Verificar métricas acumuladas
redis-cli keys "metricas:*" | wc -l
# Deve ter múltiplas chaves
```

## 📞 Suporte

**Erro não resolvido?**

1. Copiar logs completos:
```bash
cat /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/logs/relatorio_cron.log
```

2. Executar diagnóstico:
```bash
python3 componentes/relatorios/test_relatorios.py
```

3. Reportar com contexto completo.
