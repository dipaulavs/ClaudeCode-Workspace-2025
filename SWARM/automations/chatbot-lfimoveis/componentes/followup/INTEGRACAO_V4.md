# 🔌 Integração com Chatbot V4

Instruções para integrar sistema de follow-ups com o chatbot existente.

---

## 📋 Checklist de Integração

- [ ] Instalar dependências (`pip3 install redis`)
- [ ] Configurar cron job (`CRON_SETUP.md`)
- [ ] Adicionar imports no chatbot
- [ ] Implementar callbacks
- [ ] Testar em produção

---

## 🚀 Passo 1: Imports

No arquivo principal do chatbot (`chatbot_v4.py`):

```python
from componentes.followup import IntegradorFollowUp

# Inicializar integrador (global)
integrador_followup = IntegradorFollowUp()
```

---

## 🔗 Passo 2: Callbacks

### 2.1 Bot Envia Mensagem

**Onde adicionar:** Toda vez que o bot responde ao cliente.

```python
def enviar_mensagem_whatsapp(numero, mensagem):
    """
    Função existente que envia mensagem via Evolution API
    """
    # ... código existente ...

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        # ✅ ADICIONAR AQUI: Agendar follow-up de inatividade
        integrador_followup.on_mensagem_bot_enviada(numero, mensagem)

    return response
```

### 2.2 Cliente Responde

**Onde adicionar:** Webhook que recebe mensagens do cliente.

```python
@app.post("/webhook")
async def webhook(request: Request):
    """
    Webhook existente que recebe mensagens
    """
    data = await request.json()

    # Extrair dados
    numero = data['key']['remoteJid'].replace('@s.whatsapp.net', '')
    mensagem = data['message'].get('conversation', '')

    # ✅ ADICIONAR AQUI: Cancelar follow-ups (cliente respondeu)
    integrador_followup.on_mensagem_cliente_recebida(numero, mensagem)

    # ... resto do processamento ...
```

### 2.3 Bot Envia Fotos

**Onde adicionar:** Quando bot envia fotos do imóvel.

```python
def enviar_fotos_imovel(numero, imovel_id):
    """
    Função que envia fotos do imóvel
    """
    fotos = buscar_fotos_imovel(imovel_id)

    for foto in fotos:
        enviar_foto_whatsapp(numero, foto)

    # ✅ ADICIONAR AQUI: Agendar follow-up pós-fotos
    integrador_followup.on_fotos_enviadas(numero, imovel_id, quantidade=len(fotos))
```

### 2.4 Visita Agendada

**Onde adicionar:** Quando cliente agenda visita.

```python
def agendar_visita(numero, imovel_id, data_hora):
    """
    Função que agenda visita
    """
    # Salvar no banco de dados
    salvar_visita(numero, imovel_id, data_hora)

    # Enviar confirmação
    enviar_mensagem_whatsapp(
        numero,
        f"Visita agendada para {data_hora.strftime('%d/%m/%Y às %H:%M')}! 📅"
    )

    # ✅ ADICIONAR AQUI: Agendar lembretes
    integrador_followup.on_visita_agendada(numero, data_hora, imovel_id)
```

---

## 🎯 Passo 3: Exemplo Completo

```python
from fastapi import FastAPI, Request
from datetime import datetime
from componentes.followup import IntegradorFollowUp

app = FastAPI()
integrador_followup = IntegradorFollowUp()

# =====================
# WEBHOOK DE MENSAGENS
# =====================
@app.post("/webhook")
async def webhook(request: Request):
    """
    Recebe mensagens do WhatsApp
    """
    data = await request.json()

    # Extrair dados
    numero = data['key']['remoteJid'].replace('@s.whatsapp.net', '')
    mensagem = data['message'].get('conversation', '')

    # ✅ Cliente respondeu → cancelar follow-ups
    integrador_followup.on_mensagem_cliente_recebida(numero, mensagem)

    # Processar mensagem com IA
    resposta = processar_com_ia(numero, mensagem)

    # Enviar resposta
    enviar_mensagem(numero, resposta)

    return {"status": "ok"}


# =====================
# ENVIAR MENSAGEM
# =====================
def enviar_mensagem(numero, mensagem):
    """
    Envia mensagem via Evolution API
    """
    url = f"{EVOLUTION_URL}/message/sendText/{EVOLUTION_INSTANCE}"

    payload = {
        "number": numero,
        "text": mensagem
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        # ✅ Bot enviou mensagem → agendar follow-up
        integrador_followup.on_mensagem_bot_enviada(numero, mensagem)

    return response


# =====================
# ENVIAR FOTOS
# =====================
def enviar_fotos_imovel(numero, imovel_id):
    """
    Envia fotos do imóvel
    """
    fotos = buscar_fotos_imovel(imovel_id)

    for foto in fotos:
        enviar_foto_whatsapp(numero, foto['url'])

    # ✅ Fotos enviadas → follow-up pós-fotos
    integrador_followup.on_fotos_enviadas(numero, imovel_id, quantidade=len(fotos))


# =====================
# AGENDAR VISITA
# =====================
def agendar_visita(numero, imovel_id, data_str):
    """
    Agenda visita ao imóvel

    Args:
        numero: Número do cliente
        imovel_id: ID do imóvel
        data_str: "05/11/2025 15:00"
    """
    # Converter string para datetime
    data_hora = datetime.strptime(data_str, "%d/%m/%Y %H:%M")

    # Salvar no banco
    salvar_visita(numero, imovel_id, data_hora)

    # Confirmar ao cliente
    enviar_mensagem(
        numero,
        f"Visita agendada para {data_hora.strftime('%d/%m/%Y às %H:%M')}! 📅"
    )

    # ✅ Visita agendada → lembretes
    integrador_followup.on_visita_agendada(numero, data_hora, imovel_id)
```

---

## 🧪 Passo 4: Testar Integração

### Teste 1: Fluxo Completo

```python
# Simular cliente enviando mensagem
numero = "5531999999999"

# 1. Cliente envia mensagem
integrador_followup.on_mensagem_cliente_recebida(numero, "Oi! Quero apartamento")

# 2. Bot responde
integrador_followup.on_mensagem_bot_enviada(numero, "Oi! Posso te ajudar...")

# 3. Bot envia fotos
integrador_followup.on_fotos_enviadas(numero, "imovel_123", quantidade=5)

# 4. Agendar visita
from datetime import datetime, timedelta
data_visita = datetime.now() + timedelta(days=1, hours=15)
integrador_followup.on_visita_agendada(numero, data_visita, "imovel_123")
```

### Teste 2: Verificar Fila

```python
# Ver follow-ups agendados
import json
from componentes.followup import SistemaFollowUp

sistema = SistemaFollowUp()
followups = sistema.redis_client.zrange("followups", 0, -1)

print(f"Follow-ups na fila: {len(followups)}")
for f in followups:
    print(json.dumps(json.loads(f), indent=2))
```

---

## 📊 Passo 5: Monitorar

### Ver Logs do Cron

```bash
tail -f logs/followup_cron.log
```

### Ver Métricas

```bash
python3 componentes/followup/metricas.py
```

### Dashboard Simples (Opcional)

Criar endpoint no FastAPI:

```python
@app.get("/dashboard/followups")
async def dashboard_followups():
    """
    Dashboard simples de follow-ups
    """
    from componentes.followup.metricas import MetricasFollowUp

    metricas = MetricasFollowUp()
    relatorio = metricas.gerar_relatorio()

    return relatorio
```

**Acessar:** `http://localhost:8000/dashboard/followups`

---

## 🎛️ Configurações Avançadas

### Personalizar Trigger por Contexto

```python
from componentes.followup import SistemaFollowUp

sistema = SistemaFollowUp()

# Agendar follow-up com região específica
sistema.agendar(
    "5531980160822",
    "inatividade_48h",
    dados_contexto={"regiao": "Savassi"}
)
# Mensagem: "Oi! Achei mais opções na Savassi. Quer ver?"
```

### Detectar Tipo de Abandono

```python
from componentes.followup import DetectorAbandono

detector = DetectorAbandono()

# Analisar última mensagem do cliente
tipo = detector.detectar_tipo("só to olhando mesmo")
# Retorna: "curioso"

# Escolher follow-up adequado
escolha = detector.escolher_followup(tipo)
print(escolha["mensagem"])
# "Oi! Encontrei mais opções que podem te interessar. Quer dar uma olhada? 😊"
```

### Resetar Tentativas

Quando cliente volta ativamente:

```python
integrador_followup.resetar_tentativas("5531980160822")
# Permite que follow-ups sejam enviados novamente
```

---

## 🚨 Tratamento de Erros

### Evolution API Indisponível

```python
try:
    integrador_followup.on_mensagem_bot_enviada(numero, mensagem)
except Exception as e:
    print(f"⚠️ Erro ao agendar follow-up: {e}")
    # Continuar normalmente (não bloquear chatbot)
```

### Redis Indisponível

Sistema de follow-up falha silenciosamente. Chatbot continua funcionando.

**Logs:** Verificar `logs/followup_cron.log` para erros.

---

## 📈 Análise de Resultados

### Após 1 Semana

```bash
python3 componentes/followup/metricas.py
```

**Perguntas:**
- Qual trigger tem melhor taxa de resposta?
- Follow-ups estão recuperando leads?
- Algum trigger está irritando clientes?

### Ajustes Recomendados

**Se taxa de resposta baixa:**
- Testar mensagens diferentes
- Ajustar delays (mais rápido ou mais lento)
- Adicionar mais contexto

**Se clientes reclamam:**
- Aumentar delays
- Reduzir max_tentativas
- Personalizar mais mensagens

---

## 🎯 Checklist Final

- [ ] Callbacks implementados em todas as funções
- [ ] Cron job rodando (`crontab -l`)
- [ ] Logs sendo gerados (`tail -f logs/followup_cron.log`)
- [ ] Teste com cliente real realizado
- [ ] Métricas sendo coletadas
- [ ] Nenhum cliente bloqueado/irritado

---

## 📞 Suporte

**Problema:** Follow-ups não estão sendo enviados

**Verificar:**
1. Cron está rodando? → `tail -f logs/followup_cron.log`
2. Callbacks estão sendo chamados? → Adicionar prints temporários
3. Redis acessível? → Testar conexão

**Problema:** Cliente recebe múltiplos follow-ups

**Solução:** Verificar se `on_mensagem_cliente_recebida()` está sendo chamado corretamente.

**Problema:** Métricas não atualizam

**Solução:** Verificar se `registrar_resposta()` está sendo chamado quando cliente responde.
