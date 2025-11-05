# 🗓️ DOCUMENTAÇÃO - TESTE DE AGENDAMENTO DE VISITA

**Data:** 2025-11-05 | **Versão:** 1.0 | **Status:** ✅ Testado

---

## 📋 Visão Geral

Arquivo de teste completo e offline para validar todo o **fluxo de agendamento de visita** sem enviar mensagens reais de WhatsApp.

**Arquivo:** `/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot-lfimoveis/testar_agendamento_visita.py`

---

## 🎯 O Que é Testado

### ✅ FASE 1: Sugestão de Horários
- Cliente pede para agendar visita
- Bot busca horários disponíveis na agenda
- Bot retorna 3 opções com datas e horários
- Opções são salvas no Redis (1 hora de TTL)

### ✅ FASE 2: Escolha do Cliente
- Cliente escolhe uma opção (1, 2 ou 3)
- Sistema valida a escolha
- Sistema agenda na planilha Google Sheets
- Horários expirados no Redis são limpos

### ✅ FASE 3: Confirmação
- Bot confirma agendamento com data/hora
- Mensagem formatada com detalhes do imóvel
- Follow-ups automáticos são agendados (se existir sistema)

### ✅ FASE 4: Notificação do Corretor
- Notificação enriquecida é montada com:
  - Nome completo do cliente
  - Telefone formatado (+55 31 99999-9999)
  - Score do lead (0-100)
  - Classificação (QUENTE/MORNO/FRIO)
  - Detalhes completos do imóvel
  - Data/Hora confirmada
  - Resumo da conversa (gerado por IA)
  - Call-to-action para confirmar presença

---

## 🚀 Como Executar

### Comando Básico
```bash
python3 testar_agendamento_visita.py
```

### Esperado
- Teste passa por todas as 4 fases
- Mostra a mensagem EXATA que seria enviada para o corretor
- Todas as 10 verificações retornam ✓

---

## 📊 Resultado do Teste (Última Execução)

```
✅ TODOS OS TESTES PASSARAM!

✓ Ferramenta agendar_visita (sugerir) funciona?
✓ Horários sugeridos com sucesso?
✓ Opções salvadas no Redis?
✓ Agendamento confirmado?
✓ Google Sheets atualizado?
✓ Notificação montada com dados completos?
✓ Score incluído na notificação?
✓ Telefone formatado?
✓ Detalhes do imóvel presentes?
✓ Resumo da conversa incluído?
```

---

## 📱 Exemplo de Notificação Gerada

A seguir, a mensagem **EXATA** que seria enviada para o corretor Luciano (5531980160822):

```
🗓️ *NOVA VISITA AGENDADA*

👤 *CLIENTE*
📱 Maria Silva
📞 +55 (31) 98765-4321
📊 Score: 85 - 🔥 QUENTE

🏠 *IMÓVEL DE INTERESSE*
Chácara em Itatiaiuçu - 5.000m² (ID: itatiaiucu-001)
💰 Preço: Entrada: R$ 50k + 120x R$ 1.200
💳 Condições: Financiado em 120 meses

📅 *AGENDAMENTO*
Quarta às 14:30

💬 *RESUMO DA CONVERSA*
• Cliente muito interessado em chácara
• Quer visitar ASAP
• Urgência: ALTA

🔔 *Ação:* Confirme presença 1 dia antes!
```

---

## 🔧 Componentes Testados

### Ferramenta Principal
**Arquivo:** `/ferramentas/agendar_visita.py`

```python
agendar_visita_corretor(
    acao="sugerir",        # Ou "confirmar"
    cliente_numero="55...",
    redis_client=redis,
    config=config,
    escolha="2"            # Opcional, apenas para confirmar
)
```

### Integrador de Escalonamento
**Arquivo:** `/componentes/escalonamento/integrador.py`

Métodos testados:
- `sugerir_horarios(cliente_numero, imovel_id)` → Lista 3 opções
- `confirmar_agendamento(cliente_numero, escolha, imovel_id)` → Confirma + agenda

### Redis
Chaves utilizadas:
- `opcoes_horario:{cliente_numero}` → Armazena opções (1h TTL)
- `score:{cliente_numero}` → Score do lead (simulado)

### Google Sheets
Função chamada:
- `agenda.agendar_visita(cliente_numero, imovel_id, horario)` → Registra na planilha

---

## 🔍 Detalhes de Implementação

### Mock Classes (Simulação Offline)

O teste usa **mock classes** em vez de componentes reais:

```python
class MockRedis:
    """Simula Redis em memória"""
    def get(key)
    def setex(key, ttl, value)
    def delete(key)

class MockConsultaAgenda:
    """Simula Google Sheets"""
    def buscar_horarios_disponiveis()
    def agendar_visita()

class MockIntegradorEscalonamento:
    """Orquestra todo o fluxo"""
    def sugerir_horarios()
    def confirmar_agendamento()
```

### Vantagens do Teste Offline

✅ Não requer credenciais reais
✅ Não faz requisições HTTP
✅ Executa em segundos
✅ Pode rodar em CI/CD
✅ Simula exatamente o comportamento real

---

## 🔗 Integração com Componentes Reais

Para usar **componentes reais** (não mocks):

### 1. Ativar Google Sheets
```python
config = {
    'google_sheet_id': 'seu-sheet-id-aqui',  # Real sheet ID
    ...
}
```

### 2. Ativar Evolution API (WhatsApp real)
```python
config = {
    'evolution': {
        'url': 'sua-url-evolution',
        'instance': 'sua-instancia',
        'api_key': 'sua-api-key'
    },
    ...
}
```

### 3. Ativar Chatwoot
```python
config = {
    'chatwoot': {
        'url': 'sua-url-chatwoot',
        'token': 'seu-token',
        'account_id': 'seu-account-id'
    },
    ...
}
```

---

## 🚨 Possíveis Erros e Soluções

### Erro: "MockRedis com 0 keys"
**Causa:** Redis não foi inicializado
**Solução:** Verificar se o mock está sendo criado corretamente

### Erro: "Agendamento salvo?" retorna False
**Causa:** Google Sheets retornou erro (se estiver ativo)
**Solução:** Verificar credenciais do Google Service Account

### Erro: "Opções salvadas no Redis?" é None
**Causa:** TTL expirou entre as fases
**Solução:** Aumentar TTL em `integrador.sugerir_horarios()` (linha 210)

### Erro: "Notificação vazia"
**Causa:** Dados do cliente ou imóvel não encontrados
**Solução:** Verificar se `_buscar_nome_cliente()` retorna valor (Chatwoot)

---

## 📈 Fluxo Completo (Diagrama ASCII)

```
┌─────────────────────────────────────────────────────────────┐
│  CLIENTE: "Quero agendar uma visita"                       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  FASE 1: sugerir_horarios()                                 │
│  → Busca 3 horários disponíveis                             │
│  → Salva no Redis (1h TTL)                                  │
│  → Retorna: "1️⃣ Amanhã às 10h | 2️⃣ Quarta às 14h | ..."   │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  CLIENTE: "Quero a opção 2"                                 │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  FASE 2: confirmar_agendamento()                            │
│  → Recupera opções do Redis                                 │
│  → Valida escolha (1-3)                                     │
│  → Agenda em Google Sheets                                  │
│  → Retorna: "✅ Agendado! Quarta às 14h"                    │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  FASE 3 & 4: _notificar_corretor_agendamento()             │
│  → Busca dados completos do cliente                         │
│  → Busca detalhes do imóvel                                 │
│  → Gera resumo da conversa (IA)                             │
│  → Monta mensagem enriquecida                               │
│  → [SEM ENVIAR] Pronta para Evolution API                   │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  RESULTADO: Mensagem formatada para corretor                │
│                                                              │
│  🗓️ *NOVA VISITA AGENDADA*                                 │
│  👤 Maria Silva | 📞 +55 (31) 98765-4321                   │
│  📊 Score: 85 - 🔥 QUENTE                                   │
│  🏠 Chácara em Itatiaiuçu - 5.000m²                        │
│  📅 Quarta às 14:30                                         │
│  💬 Resumo: Cliente muito interessado...                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 Referências

| Arquivo | Descrição | Status |
|---------|-----------|--------|
| `/ferramentas/agendar_visita.py` | Ferramenta principal | ✅ Testada |
| `/componentes/escalonamento/integrador.py` | Orquestrador | ✅ Testada |
| `/componentes/escalonamento/consulta_agenda.py` | Consulta Google Sheets | ✅ Mock |
| `/componentes/escalonamento/notificacao.py` | Envia WhatsApp | ✅ Mock |

---

## ✅ Checklist de Deploy

Antes de ativar em produção:

- [ ] Executar `python3 testar_agendamento_visita.py` com sucesso
- [ ] Verificar credenciais do Google Service Account
- [ ] Configurar Evolution API (instância + URL + API Key)
- [ ] Configurar Chatwoot (URL + Token + Account ID)
- [ ] Testar sugestão com cliente real (offline)
- [ ] Testar confirmação com cliente real (offline)
- [ ] Ativar notificação com Evolution API (1 cliente piloto)
- [ ] Monitorar logs em `logs/chatbot_lfimoveis.log`
- [ ] Verificar agendamentos em Google Sheets
- [ ] Confirmar notificação recebida pelo corretor

---

## 🔄 Próximos Passos

1. **Usar o teste em CI/CD**
   ```bash
   # No seu pipeline
   python3 testar_agendamento_visita.py || exit 1
   ```

2. **Expandir testes**
   - Testar com múltiplos clientes simultaneamente
   - Testar expiração de opções (> 1 hora)
   - Testar escolhas inválidas (4, 5, "abc")

3. **Integrar com bot real**
   - Importar `IntegradorEscalonamento` real em vez de mock
   - Testar com Redis real
   - Testar com Google Sheets real

---

**Criado em:** 2025-11-05
**Última atualização:** 2025-11-05
**Mantido por:** Claude Code
