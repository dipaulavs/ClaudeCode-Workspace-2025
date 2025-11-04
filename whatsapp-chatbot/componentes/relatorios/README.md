# 📊 Sistema de Relatórios Automáticos

Sistema completo de coleta de métricas e geração de relatórios para o Chatbot WhatsApp V4.

## 📁 Arquivos

```
componentes/relatorios/
├── __init__.py                  # Exports principais
├── metricas.py                  # ColetorMetricas - coleta em tempo real
├── gerador_relatorio.py         # GeradorRelatorio - relatório diário
├── dashboard_semanal.py         # DashboardSemanal - relatório semanal
├── integrador.py                # IntegradorMetricas - callbacks para chatbot
├── cron_diario.py              # Script cron (18h diariamente)
├── test_relatorios.py          # Testes automatizados
├── README.md                    # Este arquivo
└── CRON_SETUP.md               # Instruções de configuração cron
```

## 🎯 Funcionalidades

### 1. Coleta de Métricas em Tempo Real

**Classe:** `ColetorMetricas`

**Métricas coletadas:**

| Métrica | Tipo | Descrição |
|---------|------|-----------|
| `leads_total` | Counter | Total acumulado de leads |
| `leads_novos_hoje` | Counter | Leads novos do dia |
| `leads_quentes` | Lista | Números com score >= 70 |
| `bot_atendeu` | Counter | Conversas respondidas pelo bot |
| `escaladas` | Counter | Conversas escaladas para humano |
| `visitas_agendadas` | Counter | Visitas confirmadas |
| `propostas_enviadas` | Counter | Propostas geradas |
| `followups_enviados` | Counter | Follow-ups automáticos enviados |
| `followups_respondidos` | Counter | Follow-ups com resposta |
| `imoveis_mais_procurados` | Sorted Set | {imovel_id: views} |

**Armazenamento:**
- Redis com TTL de 90 dias
- Chaves: `metricas:{data}:{metrica}`
- Exemplo: `metricas:2025-11-04:leads_novos_hoje`

### 2. Relatório Diário

**Classe:** `GeradorRelatorio`

**Enviado:** 18h (via cron)

**Conteúdo:**
- 👥 Leads (total, novos, quentes)
- 🤖 Bot (atendeu, escaladas, taxa)
- 🏠 Interesse (visitas, propostas)
- 💰 Conversão (lead→visita, visita→proposta)
- 📨 Follow-ups (enviados, respondidos, taxa)
- 🔥 Top 5 leads quentes (com scores)
- 🏘️ Top 3 imóveis mais procurados

### 3. Dashboard Semanal

**Classe:** `DashboardSemanal`

**Enviado:** Segunda-feira (resumo seg-dom)

**Conteúdo:**
- 📈 Resumo semanal consolidado
- 🤖 Performance bot (média)
- 💰 Funil completo
- 📨 Efetividade follow-ups
- 🏘️ Imóveis mais procurados da semana
- 💡 Insights automáticos

### 4. Integrador de Métricas

**Classe:** `IntegradorMetricas`

**Callbacks disponíveis:**

```python
integrador = IntegradorMetricas()

# Nova conversa iniciada
integrador.on_nova_conversa("5531980160822")

# Bot respondeu
integrador.on_bot_respondeu("5531980160822")

# Conversa escalada
integrador.on_escalamento("5531980160822")

# Lead ficou quente
integrador.on_lead_quente("5531980160822", score=75)

# Visita agendada
integrador.on_visita_agendada("5531980160822", "imovel_001")

# Proposta enviada
integrador.on_proposta_enviada("5531980160822")

# Follow-up enviado
integrador.on_followup_enviado("5531980160822")

# Cliente respondeu follow-up
integrador.on_followup_respondido("5531980160822")

# Cliente visualizou imóvel
integrador.on_imovel_visualizado("5531980160822", "imovel_001")
```

## 🚀 Como Usar

### Uso Básico

```python
from componentes.relatorios import ColetorMetricas, GeradorRelatorio

# Coletar métrica
coletor = ColetorMetricas()
coletor.incrementar("leads_novos_hoje")

# Gerar relatório
gerador = GeradorRelatorio()
relatorio = gerador.gerar_relatorio_diario()
print(relatorio)

# Enviar para gestor
gerador.enviar_relatorio(relatorio, "5531980160822")
```

### Integração no Chatbot

```python
from componentes.relatorios import IntegradorMetricas

# No processamento de mensagens
integrador = IntegradorMetricas()

# Quando nova conversa
if primeira_mensagem:
    integrador.on_nova_conversa(cliente_numero)

# Quando bot responde
if bot_respondeu:
    integrador.on_bot_respondeu(cliente_numero)

# Quando lead fica quente
from componentes.score import SistemaScore
score_system = SistemaScore()
score = score_system.get_score(cliente_numero)
integrador.on_lead_quente(cliente_numero, score)
```

### Dashboard Semanal

```python
from componentes.relatorios import DashboardSemanal

dashboard = DashboardSemanal()
relatorio_semanal = dashboard.gerar_relatorio_semanal()
print(relatorio_semanal)
```

## 📊 Exemplo de Relatório Diário

```
📊 RELATÓRIO DIÁRIO - 04/11/2025

👥 LEADS:
   • Total: 23
   • Novos hoje: 8
   • Quentes: 5 🔥

🤖 BOT:
   • Conversas atendidas: 18 (78%)
   • Escaladas para humano: 5 (22%)

🏠 INTERESSE:
   • Visitas agendadas: 3
   • Propostas enviadas: 1

💰 CONVERSÃO:
   • Lead → Visita: 13%
   • Visita → Proposta: 33%

📨 FOLLOW-UPS:
   • Enviados: 12
   • Respondidos: 5 (42%)

🔥 LEADS QUENTES HOJE:
   1. 5531980160822 (Score 85)
   2. 5531988887777 (Score 78)
   3. 5531977776666 (Score 72)

🏘️ IMÓVEIS MAIS PROCURADOS:
   • imovel_001: 15 visualizações
   • imovel_003: 12 visualizações
   • imovel_007: 8 visualizações
```

## 🧪 Testes

```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot

# Rodar todos os testes
python3 componentes/relatorios/test_relatorios.py

# Testar geração manual
python3 -c "
from componentes.relatorios import GeradorRelatorio
gerador = GeradorRelatorio()
print(gerador.gerar_relatorio_diario())
"

# Testar envio (não envia, só valida)
python3 componentes/relatorios/cron_diario.py
```

## ⚙️ Configuração

### 1. Configurar número do gestor

Editar `chatwoot_config.json`:

```json
{
  "relatorios": {
    "numero_gestor": "5531980160822"
  }
}
```

### 2. Configurar cron

Ver instruções detalhadas em `CRON_SETUP.md`.

**Resumo:**

```bash
# Editar crontab
crontab -e

# Adicionar linha (18h diariamente):
0 18 * * * /usr/local/bin/python3 /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/componentes/relatorios/cron_diario.py >> /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/logs/relatorio_cron.log 2>&1

# Adicionar linha (segunda-feira 9h):
0 9 * * 1 /usr/local/bin/python3 -c "import sys; sys.path.insert(0, '/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot'); from componentes.relatorios import DashboardSemanal; print(DashboardSemanal().gerar_relatorio_semanal())" | /usr/local/bin/python3 /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/scripts/whatsapp/send_message.py --phone 5531980160822 --message -
```

## 🔧 Requisitos

- Redis rodando (porta 6379)
- Python 3.8+
- Dependências: `redis`, `requests`

```bash
pip install redis requests
```

## 📝 Logs

```bash
# Ver logs do cron
tail -f /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/logs/relatorio_cron.log

# Ver todas as métricas do dia
python3 -c "
from componentes.relatorios import ColetorMetricas
from datetime import datetime

coletor = ColetorMetricas()
hoje = datetime.now().date()

print('Leads novos:', coletor.buscar('leads_novos_hoje', hoje))
print('Bot atendeu:', coletor.buscar('bot_atendeu', hoje))
print('Escaladas:', coletor.buscar('escaladas', hoje))
print('Visitas:', coletor.buscar('visitas_agendadas', hoje))
"
```

## 🐛 Troubleshooting

**Problema:** Relatório não envia

```bash
# Verificar se script roda manualmente
python3 componentes/relatorios/cron_diario.py

# Verificar logs
cat logs/relatorio_cron.log
```

**Problema:** Métricas zeradas

```bash
# Verificar Redis
redis-cli ping  # Deve retornar PONG

# Verificar chaves
redis-cli keys "metricas:*"

# Ver valor específico
redis-cli get "metricas:2025-11-04:leads_novos_hoje"
```

**Problema:** Cron não executa

```bash
# Verificar se cron está ativo
crontab -l

# Ver logs do sistema
grep CRON /var/log/system.log  # macOS
```

## 🎯 Roadmap

- [ ] Dashboard web (visualização gráfica)
- [ ] Comparação período anterior
- [ ] Alertas automáticos (queda conversão)
- [ ] Export CSV/Excel
- [ ] Integração com Google Sheets
- [ ] Métricas por corretor (quando multi-corretor)

## 📚 Referências

- [Sistema de Score](../score/README.md)
- [Chatbot V4](../../README.md)
- [WhatsApp Scripts](../../../../scripts/whatsapp/README.md)
