# Sistema de Score + Tags + Origem

Sistema completo de qualificação de leads para Chatbot WhatsApp V4.

## Visão Geral

```
Cliente envia mensagem
    ↓
Sistema analisa e pontua:
    ├─ Informações: +40 pontos (tipo, região, orçamento)
    ├─ Comportamento: +40 pontos (rapidez, fotos, perguntas)
    └─ Urgência: +20 pontos (hoje, essa semana, urgente)
    ↓
Score total: 0-100
    ├─ 70-100 → QUENTE 🔥
    ├─ 40-69 → MORNO 🌡️
    └─ 0-39 → FRIO ❄️
    ↓
Tags aplicadas automaticamente no Chatwoot:
    • primeiro_contato, interessado, quente
    • tem_pet, quer_mobilia, prioridade_alta
    • origem_facebook, imovel_apto-001
    ↓
Corretor vê no Chatwoot: Score + Tags + Origem
```

## Componentes

### 1. SistemaScore (`sistema_score.py`)

Pontua leads de 0-100 baseado em:

**Informações fornecidas (max 40):**
- Tipo de imóvel definido: +10
- Região definida: +10
- Orçamento definido: +20

**Comportamento (max 40):**
- Resposta rápida (< 2min): +10
- Pediu fotos: +10
- Fez perguntas: +10
- Mencionou prazo: +10

**Urgência (max 20):**
- Urgente/hoje: +20
- Esta semana: +15
- Este mês: +10
- Próximo mês: +5

**Métodos principais:**
```python
score = SistemaScore(redis_client)

# Calcular pontos de uma mensagem
delta = score.calcular_delta(mensagem, estado_cliente)

# Atualizar score
novo_score = score.atualizar_score(cliente_numero, delta)

# Buscar score
score_atual = score.get_score(cliente_numero)

# Classificar
classificacao = score.classificar_lead(score_atual)  # QUENTE/MORNO/FRIO
```

### 2. SistemaTags (`sistema_tags.py`)

Aplica tags automáticas no Chatwoot baseado em palavras-chave e score.

**Tags disponíveis:**

**Estágio do funil:**
- `primeiro_contato`: "oi", "olá", "bom dia"
- `interessado`: "quero", "procurando", "busco"
- `engajado`: "foto", "visitar", "quando posso"

**Preferências:**
- `tem_pet`: "pet", "cachorro", "gato"
- `quer_mobilia`: "mobiliado", "móveis"
- `vaga_garagem`: "garagem", "vaga"

**Urgência:**
- `prioridade_alta`: "urgente", "hoje", "rápido"
- `prioridade_media`: "essa semana", "amanhã"

**Comportamento:**
- `visual`: "foto", "imagem", "vídeo"
- `preco_sensivel`: "valor", "preço", "quanto custa"

**Score:**
- `lead_quente`: score >= 70
- `lead_morno`: 40 <= score < 70
- `lead_frio`: score < 40

**Métodos principais:**
```python
tags = SistemaTags(redis_client, chatwoot_config)

# Detectar tags de uma mensagem
tags_detectadas = tags.detectar_tags(mensagem, score)

# Aplicar tags no Chatwoot
tags.aplicar_chatwoot(cliente_numero, tags_detectadas)

# Atualizar custom attributes
tags.atualizar_custom_attributes(cliente_numero, {
    "score": 75,
    "classificacao": "QUENTE"
})
```

### 3. DeteccaoOrigem (`deteccao_origem.py`)

Rastreia de onde o lead veio via UTM tracking.

**Como funciona:**

Link do anúncio:
```
https://wa.me/5531980160822?text=oi&utm_source=facebook&imovel=apto-savassi-001
```

Cliente clica → WhatsApp abre → Bot detecta origem e imóvel.

**Origens suportadas:**
- facebook
- instagram
- google
- whatsapp
- indicacao
- site
- olx
- imovelweb

**Métodos principais:**
```python
origem = DeteccaoOrigem(redis_client, sistema_tags)

# Extrair origem da primeira mensagem
origem_data = origem.extrair_origem_inicial(
    mensagem,
    link_params={"utm_source": "facebook", "imovel": "apto-001"}
)

# Salvar origem
origem.salvar_origem(cliente_numero, origem_data)

# Aplicar tags de origem no Chatwoot
origem.aplicar_tags_origem(cliente_numero)

# Registrar conversão
origem.registrar_conversao(cliente_numero, "visita_agendada")

# Estatísticas
conversoes = origem.get_conversoes("facebook", periodo_dias=30)
imoveis = origem.get_imoveis_mais_procurados(limit=10)
```

### 4. IntegradorScore (`integrador.py`)

Pipeline completo que executa score + tags + origem em cada mensagem.

**Fluxo:**
```python
integrador = IntegradorScore(redis_client, chatwoot_config)

# Processar mensagem
resultado = integrador.processar_mensagem(
    cliente_numero="5531980160822",
    mensagem="Quero apartamento 2 quartos Savassi até 2000",
    eh_primeira_msg=False,
    link_params=None  # Só na primeira mensagem
)

# Resultado:
# {
#     "score": 40,
#     "classificacao": "MORNO",
#     "tags_aplicadas": ["interessado", "lead_morno"],
#     "delta": 40,
#     "origem": "facebook"
# }
```

**Métodos úteis:**
```python
# Resumo completo do cliente
resumo = integrador.get_resumo_cliente(cliente_numero)

# Estatísticas gerais
stats = integrador.get_estatisticas()

# Reset (usar com cuidado)
integrador.reset_cliente(cliente_numero)
```

## Uso Completo

### Inicialização

```python
import redis
import json
from componentes.score import IntegradorScore

# Conectar Redis
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

# Carregar config do Chatwoot
with open("chatwoot_config.json") as f:
    config = json.load(f)
    chatwoot_config = config["chatwoot"]

# Inicializar integrador
integrador = IntegradorScore(redis_client, chatwoot_config)
```

### Primeira Mensagem (com UTM)

```python
# Cliente clicou em link do Facebook
# https://wa.me/5531980160822?text=oi&utm_source=facebook&imovel=apto-savassi-001

resultado = integrador.processar_mensagem(
    cliente_numero="5531980160822",
    mensagem="Oi, tudo bem?",
    eh_primeira_msg=True,
    link_params={
        "utm_source": "facebook",
        "imovel": "apto-savassi-001"
    }
)

# Resultado:
# - Origem salva: facebook
# - Tags aplicadas: origem_facebook, imovel_apto-savassi-001, primeiro_contato
# - Custom attributes: origem=facebook, imovel_interesse=apto-savassi-001
```

### Mensagens Subsequentes

```python
# Mensagem 2
resultado = integrador.processar_mensagem(
    cliente_numero="5531980160822",
    mensagem="Quero apartamento 2 quartos Savassi até 2000"
)
# Score: +40 (tipo + região + orçamento)
# Tags: interessado, lead_morno

# Mensagem 3
resultado = integrador.processar_mensagem(
    cliente_numero="5531980160822",
    mensagem="Pode me enviar fotos?"
)
# Score: +10 (pediu_fotos)
# Tags: visual

# Mensagem 4
resultado = integrador.processar_mensagem(
    cliente_numero="5531980160822",
    mensagem="É urgente, preciso pra hoje"
)
# Score: +20 (urgente)
# Classificação: QUENTE (score >= 70)
# Tags: prioridade_alta, lead_quente (remove lead_morno)
```

### Buscar Resumo do Cliente

```python
resumo = integrador.get_resumo_cliente("5531980160822")

# {
#     "score": 70,
#     "classificacao": "QUENTE",
#     "historico_score": [
#         {"timestamp": 1234567890, "delta": 20, "score_total": 70},
#         {"timestamp": 1234567880, "delta": 10, "score_total": 50},
#         ...
#     ],
#     "origem": {
#         "utm_source": "facebook",
#         "imovel_id": "apto-savassi-001",
#         "timestamp": 1234567800
#     },
#     "tags": ["origem_facebook", "imovel_apto-savassi-001", "interessado", "visual", "lead_quente"],
#     "estado": {
#         "tem_tipo_definido": True,
#         "tem_regiao_definida": True,
#         "tem_orcamento_definido": True,
#         "pediu_fotos": True,
#         "tem_urgencia": "urgente"
#     }
# }
```

### Estatísticas Gerais

```python
stats = integrador.get_estatisticas()

# {
#     "total_leads": 50,
#     "leads_quentes": 10,
#     "leads_mornos": 25,
#     "leads_frios": 15,
#     "score_medio": 52.4,
#     "origens": {
#         "facebook": 30,
#         "instagram": 15,
#         "direto": 5
#     },
#     "imoveis_mais_procurados": [
#         {"imovel_id": "apto-savassi-001", "leads": 12},
#         {"imovel_id": "casa-lourdes-002", "leads": 8},
#         ...
#     ]
# }
```

## Integração com Chatwoot

### Tags

Tags são aplicadas automaticamente via API:

```
POST /api/v1/accounts/{account_id}/conversations/{conv_id}/labels
Body: {"labels": ["tag1", "tag2"]}
```

**Visível em:** Chatwoot → Conversa → Sidebar → Labels

### Custom Attributes

Atributos personalizados visíveis no painel:

```
POST /api/v1/accounts/{account_id}/conversations/{conv_id}/custom_attributes
Body: {
    "custom_attributes": {
        "score": 75,
        "classificacao": "QUENTE",
        "origem": "facebook",
        "imovel_interesse": "apto-savassi-001"
    }
}
```

**Visível em:** Chatwoot → Conversa → Sidebar → Custom Attributes

## Testes

Execute os testes:

```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/componentes/score
python3 test_score.py
```

**Cenários testados:**
1. Cálculo de score
2. Tags automáticas
3. Detecção de origem
4. Pipeline completo (conversa inteira)
5. Estatísticas gerais

## Dados no Redis

### Estrutura de chaves

```
score:{cliente_numero}             # Score atual (0-100)
score_history:{cliente_numero}     # Histórico de pontuações
estado:{cliente_numero}            # Estado do cliente (flags)
origem:{cliente_numero}            # Dados de origem (UTM)
tags_aplicadas:{cliente_numero}    # Cache de tags
conversao:{cliente_numero}         # Dados de conversão
chatwoot:conv_id:{cliente_numero}  # Cache do ID da conversa
```

### Exemplo de dados

```redis
> GET score:5531980160822
"75"

> LRANGE score_history:5531980160822 0 2
1) "{\"timestamp\": 1234567890, \"delta\": 20, \"score_total\": 75}"
2) "{\"timestamp\": 1234567880, \"delta\": 10, \"score_total\": 55}"
3) "{\"timestamp\": 1234567870, \"delta\": 40, \"score_total\": 45}"

> GET origem:5531980160822
"{\"utm_source\": \"facebook\", \"imovel_id\": \"apto-savassi-001\", \"timestamp\": 1234567800}"

> SMEMBERS tags_aplicadas:5531980160822
1) "origem_facebook"
2) "interessado"
3) "visual"
4) "lead_quente"
```

## Exemplo Prático: Conversa Completa

```python
# Cliente: 5531980160822
# Clicou em anúncio do Facebook (imóvel: apto-savassi-001)

# Mensagem 1 (primeira)
integrador.processar_mensagem(
    "5531980160822",
    "Oi",
    eh_primeira_msg=True,
    link_params={"utm_source": "facebook", "imovel": "apto-savassi-001"}
)
# Score: 0 → Tags: origem_facebook, imovel_apto-savassi-001, primeiro_contato

# Mensagem 2
integrador.processar_mensagem("5531980160822", "Quero apartamento Savassi")
# Score: 0 → 20 (tipo + região) → Tags: interessado, lead_frio

# Mensagem 3
integrador.processar_mensagem("5531980160822", "Quanto custa? Tem fotos?")
# Score: 20 → 30 (pediu_fotos) → Tags: visual, preco_sensivel

# Mensagem 4
integrador.processar_mensagem("5531980160822", "Até 2000 reais")
# Score: 30 → 50 (orçamento) → Tags: lead_morno (remove lead_frio)

# Mensagem 5
integrador.processar_mensagem("5531980160822", "É urgente, preciso pra hoje")
# Score: 50 → 70 (urgente) → Tags: prioridade_alta, lead_quente (remove lead_morno)

# Resumo final
resumo = integrador.get_resumo_cliente("5531980160822")
# Score: 70, Classificação: QUENTE, Origem: facebook, Imóvel: apto-savassi-001
```

## Dependências

```python
redis>=5.0.0
requests>=2.31.0
```

## Configuração

Requer arquivo `chatwoot_config.json` na raiz do projeto:

```json
{
  "chatwoot": {
    "url": "https://chatwoot.loop9.com.br",
    "token": "xp1AcWvf6F2p2ZypabNWHfW6",
    "account_id": 1,
    "inbox_id": 40
  }
}
```

## Autor

Sub-Agente 2: Sistema de Score + Tags + Origem
Chatbot WhatsApp V4 - LF Imóveis
