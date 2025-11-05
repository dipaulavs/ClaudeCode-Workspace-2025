# 🔔 Sistema de Follow-ups Anti-Abandono

Sistema automático para recuperar leads que abandonaram a conversa no chatbot WhatsApp.

**Objetivo:** Reduzir taxa de abandono de 83% para menos de 25% (recuperar 75% dos leads).

---

## 📊 Problema x Solução

### Problema
- Cliente clica no anúncio → pergunta 1-2 coisas → desaparece
- Taxa de abandono: 83%
- Oportunidades perdidas

### Solução
- Follow-ups automáticos estratégicos baseados em triggers
- Personalização por tipo de abandono
- Limite de tentativas (anti-spam)
- Lembretes de visitas

---

## 🎯 Como Funciona

```
Cliente pergunta "Qual o valor?"
    ↓
Bot responde "R$1.800 + R$420 condomínio"
    ↓
Cliente some (não responde)
    ↓
[2h depois] → "E aí, ficou alguma dúvida? 😊"
    ↓
[24h depois] → "Oi! Ainda tá procurando imóvel?"
    ↓
[48h depois] → "Achei mais opções na Savassi. Quer ver?"
```

---

## 🔧 Componentes

### 1. `sistema_followup.py`
Gerencia agendamento, processamento e envio de follow-ups.

**Principais métodos:**
- `agendar(cliente, trigger, contexto)` - Agenda follow-up
- `cancelar_todos(cliente)` - Cancela follow-ups pendentes
- `processar_pendentes()` - Processa fila (executado via cron)
- `registrar_envio()` - Registra tentativa
- `registrar_resposta()` - Registra quando cliente responde

### 2. `tipos_abandono.py`
Detecta tipo de abandono para personalizar follow-up.

**Tipos detectados:**
- **Curioso** - "só olhando", "vendo opções" → Follow-up 24h
- **Preguiçoso** - "depois eu vejo", "vou pensar" → Follow-up 2h
- **Indeciso** - "não sei", "talvez" → Envia fotos extras
- **Interessado** - "gostei", "interessante" → Follow-up 2h
- **Negociador** - "desconto", "muito caro" → Conversa sobre valor
- **Sumiu** - Sem mensagem → Follow-up 2h

### 3. `integrador.py`
Integra sistema com callbacks do chatbot.

**Callbacks disponíveis:**
- `on_mensagem_bot_enviada()` - Agenda follow-up de inatividade
- `on_mensagem_cliente_recebida()` - Cancela follow-ups
- `on_fotos_enviadas()` - Agenda follow-up pós-fotos
- `on_visita_agendada()` - Agenda lembretes
- `on_abandono_detectado()` - Follow-up personalizado

### 4. `processador_cron.py`
Script executado via cron a cada 5 minutos.

### 5. `metricas.py`
Gera relatórios de efetividade.

---

## 🚀 Instalação

### 1. Configurar Cron Job

```bash
# Editar crontab
crontab -e

# Adicionar linha (executar a cada 5 minutos)
*/5 * * * * /usr/local/bin/python3 /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/componentes/followup/processador_cron.py >> /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/logs/followup_cron.log 2>&1
```

### 2. Verificar Cron

```bash
# Listar cron jobs
crontab -l

# Ver logs
tail -f /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/logs/followup_cron.log
```

### 3. Integrar com Chatbot V4

No arquivo principal do chatbot (`chatbot_v4.py`):

```python
from componentes.followup import IntegradorFollowUp

# Inicializar integrador
integrador = IntegradorFollowUp()

# Callback quando bot envia mensagem
def on_resposta_enviada(cliente_numero, mensagem):
    integrador.on_mensagem_bot_enviada(cliente_numero, mensagem)

# Callback quando cliente responde
def on_mensagem_recebida(cliente_numero, mensagem):
    integrador.on_mensagem_cliente_recebida(cliente_numero, mensagem)

# Callback quando envia fotos
def on_fotos_enviadas(cliente_numero, imovel_id):
    integrador.on_fotos_enviadas(cliente_numero, imovel_id, quantidade=5)
```

---

## 🎛️ Triggers Disponíveis

| Trigger | Delay | Mensagem | Tipo |
|---------|-------|----------|------|
| `inatividade_2h` | 2 horas | "E aí, ficou alguma dúvida? 😊" | Inatividade |
| `inatividade_24h` | 24 horas | "Oi! Ainda tá procurando imóvel?" | Inatividade |
| `inatividade_48h` | 48 horas | "Achei mais opções na {regiao}" | Inatividade |
| `pos_fotos` | 1 hora | "Gostou das fotos? Quer agendar visita?" | Pós-interação |
| `pos_visita` | 4 horas | "E aí, gostou do imóvel? 😊" | Pós-interação |
| `lembrete_visita_24h` | 24h antes | "Amanhã às {hora} é sua visita!" | Lembrete |
| `lembrete_visita_2h` | 2h antes | "Daqui 2h é sua visita!" | Lembrete |

---

## 📖 Exemplos de Uso

### Exemplo 1: Agendamento Manual

```python
from componentes.followup import SistemaFollowUp

sistema = SistemaFollowUp()

# Agendar follow-up de inatividade
sistema.agendar("5531980160822", "inatividade_2h")

# Com contexto
sistema.agendar(
    "5531980160822",
    "inatividade_48h",
    dados_contexto={"regiao": "Savassi"}
)
```

### Exemplo 2: Visita Agendada

```python
from componentes.followup import IntegradorFollowUp
from datetime import datetime, timedelta

integrador = IntegradorFollowUp()

# Visita amanhã às 15h
data_visita = datetime.now() + timedelta(days=1)
data_visita = data_visita.replace(hour=15, minute=0)

integrador.on_visita_agendada(
    "5531980160822",
    data_visita,
    "imovel_123"
)
# Agenda automaticamente:
# - Lembrete 24h antes
# - Lembrete 2h antes
```

### Exemplo 3: Cancelamento ao Responder

```python
integrador = IntegradorFollowUp()

# Cliente respondeu → cancela todos follow-ups pendentes
integrador.on_mensagem_cliente_recebida(
    "5531980160822",
    "Oi! Quero agendar visita"
)
```

### Exemplo 4: Detectar Tipo de Abandono

```python
from componentes.followup import DetectorAbandono

detector = DetectorAbandono()

# Detectar tipo
tipo = detector.detectar_tipo("só to olhando mesmo")
# Retorna: "curioso"

# Escolher follow-up adequado
escolha = detector.escolher_followup(tipo)
# Retorna: {
#     "trigger": "inatividade_24h",
#     "mensagem": "Oi! Encontrei mais opções..."
# }
```

---

## 📊 Métricas

### Ver Relatório

```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot

python3 componentes/followup/metricas.py
```

**Saída:**
```
============================================================
📊 RELATÓRIO DE FOLLOW-UPS
============================================================

⏰ Data/Hora: 04/11/2025 14:30:00

📈 MÉTRICAS GERAIS
------------------------------------------------------------
Total enviados:     120
Total respondidos:  54
Taxa de resposta:   45.0%

📊 MÉTRICAS POR TRIGGER
------------------------------------------------------------

inatividade_2h:
  Enviados:    50
  Respondidos: 20
  Taxa:        40.0%

inatividade_24h:
  Enviados:    40
  Respondidos: 15
  Taxa:        37.5%

pos_fotos:
  Enviados:    20
  Respondidos: 12
  Taxa:        60.0%

============================================================
🎯 ANÁLISE DE PERFORMANCE
============================================================

⭐ Melhor trigger:  pos_fotos (60.0%)
⚠️  Pior trigger:   inatividade_48h (15.0%)

💡 Estimativa de leads recuperados:
   54 leads que teriam abandonado foram recuperados!
```

### Resetar Métricas (Testes)

```bash
python3 componentes/followup/metricas.py --reset
```

---

## 🧪 Testes

### Executar Suite de Testes

```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot

python3 componentes/followup/test_followup.py
```

**Testes incluídos:**
1. ✅ Agendamento básico
2. ✅ Agendamento com contexto
3. ✅ Cancelamento
4. ✅ Processamento de fila
5. ✅ Limite de tentativas
6. ✅ Detector de abandono
7. ✅ Integrador com chatbot
8. ✅ Lembretes de visita

---

## 🔐 Configurações

### Redis (Upstash)
- Host: `usw1-popular-stallion-42128.upstash.io`
- Port: `42128`
- SSL: Sim

### Evolution API
- URL: `https://megatalk.com.br`
- Instance: `lfimoveis`

---

## 🎯 Expectativas de Recuperação

| Trigger | Taxa Esperada |
|---------|---------------|
| Inatividade 2h | 40% respondem |
| Inatividade 24h | 25% respondem |
| Inatividade 48h | 15% respondem |
| Pós-fotos | 30% respondem |
| Pós-visita | 50% respondem |

**Meta geral:** Recuperar 75% dos leads abandonados.

---

## 🚨 Troubleshooting

### Follow-ups não estão sendo enviados

**Verificar:**
1. Cron está rodando? `crontab -l`
2. Logs do cron: `tail -f logs/followup_cron.log`
3. Redis está acessível? Testar conexão

### Cliente recebe múltiplos follow-ups

**Causa:** Callbacks não estão cancelando follow-ups.

**Solução:** Verificar integração no chatbot V4:
```python
# SEMPRE cancelar ao receber resposta
integrador.on_mensagem_cliente_recebida(numero, msg)
```

### Lembretes não chegam

**Causa:** Data/hora da visita incorreta.

**Solução:** Passar `datetime` object correto:
```python
from datetime import datetime

# ✅ Correto
data_visita = datetime(2025, 11, 5, 15, 0)

# ❌ Errado
data_visita = "05/11/2025 15:00"  # String não funciona
```

---

## 📚 Estrutura de Dados Redis

### Follow-ups Agendados
```
Chave: "followups"
Tipo: Sorted Set (score = timestamp)

Valor:
{
  "id": "fu_abc123",
  "cliente": "5531980160822",
  "trigger": "inatividade_2h",
  "tipo": "inatividade",
  "mensagem": "E aí, ficou alguma dúvida?",
  "tentativa": 1,
  "criado_em": 1699128000
}
```

### Contador de Tentativas
```
Chave: "followup_count:{numero}:{tipo}"
Tipo: String (counter)
TTL: 30 dias
```

### Histórico
```
Chave: "followup_history:{numero}"
Tipo: List (últimos 100)

Valor:
{
  "timestamp": 1699128000,
  "trigger": "inatividade_2h",
  "tipo": "inatividade",
  "enviado": true,
  "respondeu": true
}
```

### Métricas
```
Chave: "metricas:followup:total_enviados"
Chave: "metricas:followup:total_respondidos"
Chave: "metricas:followup:{trigger}:enviados"
Chave: "metricas:followup:{trigger}:respondidos"
Tipo: String (counter)
```

---

## 🎨 Personalização

### Adicionar Novo Trigger

Editar `sistema_followup.py`:

```python
TRIGGERS = {
    # ... triggers existentes ...

    "seu_trigger": {
        "delay": 3600,  # 1 hora
        "mensagem": "Sua mensagem aqui",
        "max_tentativas": 1,
        "tipo": "inatividade",
        "precisa_contexto": False
    }
}
```

### Adicionar Novo Tipo de Abandono

Editar `tipos_abandono.py`:

```python
TIPOS_ABANDONO = {
    # ... tipos existentes ...

    "seu_tipo": {
        "sinais": ["palavra1", "palavra2"],
        "followup": "inatividade_2h",
        "mensagem_personalizada": "Mensagem personalizada"
    }
}
```

---

## 📞 Suporte

**Logs:**
- Cron: `logs/followup_cron.log`
- Chatbot: `logs/chatbot_v4.log`

**Métricas:**
```bash
python3 componentes/followup/metricas.py
```

**Testes:**
```bash
python3 componentes/followup/test_followup.py
```

---

## 🎯 Roadmap

- [ ] Dashboard web para visualizar métricas
- [ ] A/B testing de mensagens
- [ ] Follow-ups por segmento (locatário vs comprador)
- [ ] Integração com CRM
- [ ] Análise de sentimento para personalização
