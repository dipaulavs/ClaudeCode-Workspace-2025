# 🔔 Sistema de Escalonamento Inteligente

Transferência automática de conversas para corretores humanos com consulta de agenda e agendamento de visitas.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Componentes](#componentes)
- [Fluxo de Escalonamento](#fluxo-de-escalonamento)
- [Triggers de Escalonamento](#triggers-de-escalonamento)
- [Agendamento de Visitas](#agendamento-de-visitas)
- [Integração com Chatwoot](#integração-com-chatwoot)
- [Uso](#uso)
- [Testes](#testes)
- [Configuração](#configuração)

---

## 🎯 Visão Geral

Sistema completo de escalonamento inteligente que:

1. **Detecta triggers** para transferir atendimento
2. **Atribui corretor** automaticamente (round-robin)
3. **Notifica corretor** via WhatsApp
4. **Consulta agenda** e sugere horários disponíveis
5. **Agenda visitas** automaticamente
6. **Cria follow-ups** (lembretes pré-visita)

### Objetivo

Reduzir tempo do corretor em **78%**, atendendo apenas leads qualificados e automatizando agendamento de visitas.

---

## 🧩 Componentes

### 1. `triggers.py` - Detector de Triggers

Detecta 5 situações de escalonamento:

```python
from componentes.escalonamento import DetectorEscalonamento

detector = DetectorEscalonamento()

trigger = detector.detectar_trigger(
    mensagem="Quero visitar o imóvel",
    score=65
)
# Retorna: "quer_visitar"
```

### 2. `consulta_agenda.py` - Consulta de Disponibilidade

Busca horários disponíveis (Google Sheets ou MOCK):

```python
from componentes.escalonamento import ConsultaAgenda

agenda = ConsultaAgenda(use_mock=True)

horarios = agenda.buscar_horarios_disponiveis(dias_frente=3, limite=3)
# Retorna: [
#   {"data": date(2025, 11, 5), "hora": "10:00", "corretor": "Bruno", ...},
#   {"data": date(2025, 11, 5), "hora": "14:00", "corretor": "Bruno", ...},
#   ...
# ]
```

### 3. `chatwoot_integration.py` - Integração Chatwoot

Gerencia conversas no Chatwoot:

```python
from componentes.escalonamento import ChatwootEscalonamento

chatwoot = ChatwootEscalonamento()

# Busca conversa
conv_id = chatwoot.buscar_conversa_id("5531980160822")

# Atribui corretor
chatwoot.atribuir_corretor(conv_id, corretor_id=1)

# Aplica tag
chatwoot.aplicar_tag_escalonamento(conv_id, "quer_visitar")

# Adiciona nota privada
chatwoot.adicionar_nota_privada(conv_id, "Cliente quer agendar visita")
```

### 4. `notificacao.py` - Notificação de Corretores

Notifica corretores via WhatsApp:

```python
from componentes.escalonamento import NotificadorCorretor

notificador = NotificadorCorretor()

# Busca próximo corretor (round-robin)
corretor = notificador.buscar_corretor_disponivel()

# Notifica
notificador.notificar_whatsapp(
    corretor=corretor,
    cliente_numero="5531980160822",
    trigger="quer_visitar",
    score=75,
    conv_id=12345,
    link_conversa="https://chatwoot.loop9.com.br/app/..."
)
```

### 5. `integrador.py` - Pipeline Completo

Orquestra todo o processo:

```python
from componentes.escalonamento import IntegradorEscalonamento

integrador = IntegradorEscalonamento()

# Processa mensagem
resposta = integrador.processar_mensagem(
    cliente_numero="5531980160822",
    mensagem="Quero visitar o imóvel",
    score=75
)
# Retorna: "Opa! Vou chamar o Bruno pra agendar sua visita! 📅"
```

---

## 🔄 Fluxo de Escalonamento

```
Cliente: "Quero visitar"
    ↓
[1] DetectorEscalonamento detecta: "quer_visitar"
    ↓
[2] ChatwootEscalonamento busca conversa
    ↓
[3] ChatwootEscalonamento aplica tag + nota
    ↓
[4] NotificadorCorretor busca corretor (round-robin)
    ↓
[5] ChatwootEscalonamento atribui corretor
    ↓
[6] NotificadorCorretor envia WhatsApp:
    "🔔 NOVO ATENDIMENTO
    Cliente: 5531980160822
    Motivo: quer_visitar
    Score: 75 🔥
    Link: https://chatwoot.loop9.com.br/..."
    ↓
[7] Redis: bot_standby = true (24h)
    ↓
Bot: "Opa! Vou chamar o Bruno pra agendar sua visita! 📅"
```

---

## 🎯 Triggers de Escalonamento

### 1. Cliente Pede Humano (Prioridade: ALTA)

**Keywords:**
- "falar com humano"
- "quero falar"
- "atendente"
- "corretor"
- "pessoa de verdade"

**Score mínimo:** 0 (sempre escala)

**Mensagem:** "Vou chamar um corretor agora mesmo! 👍"

---

### 2. Cliente Frustrado (Prioridade: ALTA)

**Keywords:**
- "não entendi"
- "não respondeu"
- "ruim"
- "péssimo"
- "não ajudou"

**Score mínimo:** 0 (sempre escala)

**Mensagem:** "Desculpa! Vou chamar um corretor pra te ajudar melhor 🙏"

---

### 3. Quer Visitar (Prioridade: ALTA)

**Keywords:**
- "visitar"
- "conhecer"
- "ver pessoalmente"
- "agendar visita"

**Score mínimo:** 40

**Mensagem:** "Opa! Vou chamar o Bruno pra agendar sua visita! 📅"

---

### 4. Quer Proposta/Fechar (Prioridade: ALTA)

**Keywords:**
- "proposta"
- "contrato"
- "fechar"
- "documentação"
- "quero alugar"

**Score mínimo:** 60

**Mensagem:** "Ótimo! Vou chamar o Bruno pra fazer sua proposta! 📝"

---

### 5. Lead Quente Automático (Prioridade: MÉDIA)

**Keywords:** Nenhum (só score)

**Score mínimo:** 80

**Mensagem:** "Vejo que você está bem interessado! Vou chamar o Bruno pra conversar com você 🔥"

---

## 📅 Agendamento de Visitas

### Fluxo Completo

```
Cliente: "Quero visitar"
    ↓
Bot consulta agenda → 3 horários disponíveis
    ↓
Bot: "Posso agendar pra:
     1️⃣ 05/11 (ter) às 10h
     2️⃣ 05/11 (ter) às 14h
     3️⃣ 06/11 (qua) às 15h
     Qual prefere?"
    ↓
Cliente: "1"
    ↓
Bot agenda no Google Sheets
Bot agenda follow-ups (lembretes)
    ↓
Bot: "✅ Agendado! Visita em 05/11 (ter) às 10h. Te mando lembretes antes! 📅"
```

### Sugerir Horários

```python
mensagem = integrador.sugerir_horarios(
    cliente_numero="5531980160822",
    imovel_id="apto-001"
)
```

### Confirmar Agendamento

```python
sucesso, mensagem = integrador.confirmar_agendamento(
    cliente_numero="5531980160822",
    escolha="1",  # ou "amanhã 10h"
    imovel_id="apto-001"
)
```

### Follow-ups Automáticos

Após agendar, cria 3 follow-ups:

1. **24h antes:** Lembrete da visita
2. **2h antes:** Lembrete urgente
3. **4h depois:** Pós-visita (coleta feedback)

---

## 🔗 Integração com Chatwoot

### Configuração

```python
# config/config.py
CHATWOOT_API_URL = "https://chatwoot.loop9.com.br"
CHATWOOT_API_TOKEN = "SEU_TOKEN_AQUI"
CHATWOOT_ACCOUNT_ID = 1
```

### Funcionalidades

- **Busca conversa** por número do cliente
- **Atribui corretor** (round-robin)
- **Aplica tags** (`escalonamento_quer_visitar`)
- **Adiciona notas privadas** (contexto para equipe)
- **Gera link direto** para conversa

---

## 🚀 Uso

### Uso Básico

```python
from componentes.escalonamento import IntegradorEscalonamento

integrador = IntegradorEscalonamento()

# No loop do chatbot:
mensagem_cliente = "Quero visitar o imóvel"
score = 75

resposta = integrador.processar_mensagem(
    cliente_numero="5531980160822",
    mensagem=mensagem_cliente,
    score=score
)

if resposta:
    # Escalonou! Envia resposta ao cliente
    print(resposta)
    # "Opa! Vou chamar o Bruno pra agendar sua visita! 📅"
else:
    # Não escalonou, continua atendimento normal
    pass
```

### Workflow Completo (Visita)

```python
# 1. Cliente manifesta interesse
resposta = integrador.processar_mensagem(
    cliente_numero="5531980160822",
    mensagem="Quero visitar o apartamento",
    score=70
)
# Resposta: "Opa! Vou chamar o Bruno pra agendar sua visita! 📅"

# 2. Sugere horários
horarios_msg = integrador.sugerir_horarios(
    cliente_numero="5531980160822",
    imovel_id="apto-001"
)
# Retorna: "Posso agendar pra:\n1️⃣ 05/11 (ter) às 10h\n..."

# 3. Cliente escolhe
sucesso, confirmacao = integrador.confirmar_agendamento(
    cliente_numero="5531980160822",
    escolha="1",
    imovel_id="apto-001"
)
# confirmacao: "✅ Agendado! Visita em 05/11 (ter) às 10h..."
```

---

## 🧪 Testes

### Executar Testes

```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot
python3 componentes/escalonamento/test_escalonamento.py
```

### Cobertura

- ✅ Detecção de triggers (6 cenários)
- ✅ Consulta de agenda (MOCK)
- ✅ Agendamento de visitas
- ✅ Escalonamento completo
- ✅ Sugestão de horários
- ✅ Confirmação de agendamento
- ✅ Bot em standby

---

## ⚙️ Configuração

### 1. Corretores

Edite `notificacao.py`:

```python
CORRETORES = [
    {
        "id": 1,
        "nome": "Bruno",
        "whatsapp": "5531999999999",  # Número real
        "chatwoot_id": 1
    },
    {
        "id": 2,
        "nome": "Fernanda",
        "whatsapp": "5531888888888",  # Número real
        "chatwoot_id": 2
    }
]
```

### 2. Google Sheets (Opcional)

Para usar Google API em vez de MOCK, veja: `GOOGLE_SETUP.md`

### 3. Redis

Certifique-se que Redis está rodando:

```bash
redis-cli ping
# Resposta esperada: PONG
```

---

## 📊 Métricas Esperadas

- **78% redução** de tempo do corretor
- **2 minutos** para agendar visita (vs 10min manual)
- **0 conflitos** de horário (consulta agenda)
- **100% dos leads quentes** atendidos imediatamente

---

## 🔧 Troubleshooting

### "Conversa não encontrada no Chatwoot"

**Causa:** Cliente ainda não tem conversa no Chatwoot

**Solução:** Sistema usa `_escalonar_sem_chatwoot()` (notifica corretor sem atribuição)

### "Opções expiraram"

**Causa:** Cliente demorou >1h para escolher horário

**Solução:** Bot pede para repetir

### Bot não entra em standby

**Causa:** Redis não está salvando

**Solução:** Verifique config Redis em `config/config.py`

---

## 📝 TODO Futuro

- [ ] Migrar de Google Sheets para Google Calendar
- [ ] Suporte a múltiplas agendas (por corretor)
- [ ] Dashboard de escalonamentos
- [ ] ML para prever melhor momento de escalonar
- [ ] Integração com CRM (Pipedrive/HubSpot)

---

## 📚 Arquivos

```
componentes/escalonamento/
├── __init__.py                   # Exports
├── triggers.py                   # Detector de triggers (5 tipos)
├── consulta_agenda.py            # Consulta horários (Google + MOCK)
├── chatwoot_integration.py       # Integração Chatwoot API
├── notificacao.py                # Notificação de corretores
├── integrador.py                 # Pipeline completo
├── test_escalonamento.py         # Testes automatizados
├── README.md                     # Este arquivo
└── GOOGLE_SETUP.md               # Instruções Google API
```

---

**Documentação completa** | Versão 1.0 | Última atualização: 04/11/2025
