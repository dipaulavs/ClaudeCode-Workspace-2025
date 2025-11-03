# 💡 Adaptive Mentor - Exemplos de Uso

## Exemplo 1: Explicar Conceito Técnico (APIs REST)

### Input do Usuário
```
"Explica o que é API REST de forma simples, quero entender mesmo."
```

### Output da Skill

```markdown
# 🎓 O Que É API REST

## O Que É (ELI5)

API REST é como um **garçom de restaurante**:

- Você (cliente) está sentado na mesa (seu app/site)
- Você faz um pedido (request): "Quero um hambúrguer"
- Garçom (API) leva o pedido para a cozinha (servidor)
- Cozinha prepara (processa)
- Garçom traz seu hambúrguer (response com dados)

A parte "REST" significa que o garçom segue regras específicas:
- Sempre entrega no mesmo formato (JSON geralmente)
- Você pode pedir, modificar, ou cancelar pedidos
- Cada pedido é independente (garçom não lembra pedidos anteriores)

## Como Funciona (Visual)

┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  Seu App    │      │  API REST   │      │  Servidor   │
│  (Frontend) │      │  (Garçom)   │      │  (Cozinha)  │
└──────┬──────┘      └──────┬──────┘      └──────┬──────┘
       │                    │                    │
       │ GET /users/123     │                    │
       │─────────────────>  │                    │
       │                    │  Busca usuário 123 │
       │                    │─────────────────>  │
       │                    │                    │
       │                    │  { "nome": "João" }│
       │                    │  <─────────────────│
       │  { "nome": "João" }│                    │
       │  <─────────────────│                    │
       │                    │                    │
```

## Exemplo Prático

Imagine que você quer ver informações de um usuário no Instagram:

**Seu código faz:**
```python
response = requests.get('https://api.instagram.com/users/123')
```

**API responde:**
```json
{
  "id": 123,
  "username": "joao_silva",
  "followers": 1500,
  "bio": "Fotógrafo profissional"
}
```

**Principais "verbos" do garçom (métodos HTTP):**
- `GET` → "Me traz isso" (buscar dados)
- `POST` → "Cria algo novo" (criar usuário, post, etc)
- `PUT` → "Atualiza isso aqui" (editar perfil)
- `DELETE` → "Remove isso" (deletar post)

## Por Que Usar APIs REST?

1. **Separação clara**: Frontend e Backend não precisam estar no mesmo lugar
2. **Reutilização**: Mesma API serve app mobile, web, desktop
3. **Padrão universal**: Qualquer linguagem consegue "conversar"

---

Ficou claro? Quer que eu mostre como **criar** uma API REST simples ou como **usar** uma API existente no seu projeto?
```

---

## Exemplo 2: Implementar Funcionalidade (Sistema de Cache)

### Input do Usuário
```
"Quero adicionar cache no meu app Python pra não ficar fazendo requests repetidos
na API. Como fazer?"
```

### Output da Skill

```markdown
# 🎓 Implementar Sistema de Cache

## O Que Vou Fazer (Explicação)

**Cache é como um caderninho de anotações rápidas:**

Imagine que você sempre pergunta para sua mãe "Que horas fecha o mercado?".
Toda vez ela precisa ligar no mercado pra confirmar.

Com cache: Primeira vez ela liga, mas **anota a resposta**.
Próximas vezes: Só olha o caderninho (muito mais rápido!).

## Como Funciona (Visual)

### Sem Cache (Lento):
```
App → API → API → API (toda hora busca de novo)
     3s    3s    3s
```

### Com Cache (Rápido):
```
App → API (primeira vez - 3s)
    ↓
  Cache salva
    ↓
App → Cache → Cache → Cache (próximas vezes - 0.001s)
```

## Diagrama da Solução

┌─────────────────────────────────────┐
│         Seu App Python              │
│                                     │
│  1. Precisa de dados?               │
│     ↓                               │
│  2. Verifica Cache primeiro         │
│     ├─ Existe? → Usa (rápido!)      │
│     └─ Não existe?                  │
│        ↓                            │
│  3. Busca na API (lento)            │
│     ↓                               │
│  4. Salva no Cache                  │
│     ↓                               │
│  5. Retorna dados                   │
└─────────────────────────────────────┘

## 🎯 Plano para Implementar

### Visão Geral (Simples):

1. **Instalar biblioteca de cache** (Redis ou memória)
   Resultado: Você terá onde guardar dados temporariamente

2. **Adicionar lógica de verificação**
   Resultado: App vai checar cache antes de chamar API

3. **Testar e validar**
   Resultado: Requests serão 100x mais rápidos

⏱️ Tempo estimado: 5-10 minutos

---

### Plano Técnico (Executável):

#### Opção 1: Cache em Memória (Simples - Recomendado para começar)

**Ferramentas:**
- `functools.lru_cache` (built-in Python)

**Arquivos que vou modificar:**
- Seu arquivo de API calls (ex: `api_client.py`)

**O que vou fazer:**
1. Adicionar decorator `@lru_cache` na função que faz request
2. Criar exemplo de uso
3. Adicionar teste para validar

**Código que vou adicionar:**
```python
from functools import lru_cache
import requests

@lru_cache(maxsize=128)  # Guarda até 128 responses
def get_user_data(user_id):
    """Busca dados do usuário (com cache automático)"""
    response = requests.get(f'https://api.example.com/users/{user_id}')
    return response.json()

# Uso:
user = get_user_data(123)  # Primeira vez: faz request (3s)
user = get_user_data(123)  # Segunda vez: usa cache (0.001s)
```

#### Opção 2: Cache com Redis (Avançado - Persiste entre execuções)

**Ferramentas:**
- Redis (precisa instalar)
- Biblioteca `redis-py`

**Arquivos que vou criar:**
- `cache_manager.py` (gerenciador de cache)
- `config/redis_config.py` (configurações)

**O que vou fazer:**
1. Instalar Redis (via Docker ou brew)
2. Criar wrapper de cache com TTL (tempo de expiração)
3. Integrar com suas funções de API

---

### Qual você prefere?

**Opção 1 (Simples)**: Cache em memória, mais fácil, perfeito para começar
**Opção 2 (Avançado)**: Redis, mais poderoso, persiste entre reinícios

Me confirma qual você quer que eu implemente?
```

---

## Exemplo 3: Resolver Problema (Erro de Import)

### Input do Usuário
```
"Tá dando erro 'ModuleNotFoundError: No module named requests' quando rodo meu script"
```

### Output da Skill

```markdown
# 🔧 Solução: ModuleNotFoundError

## Diagnóstico

Identifiquei que: **A biblioteca 'requests' não está instalada no seu ambiente Python**

## Por Que Acontece (Analogia)

É como tentar usar uma ferramenta que você não tem na sua caixa de ferramentas:

- Seu script (você) tenta usar `requests` (chave inglesa)
- Python procura na caixa de ferramentas (site-packages)
- Não encontra → Erro!

## Como Resolver (Passo a Passo)

┌─────────────────────────────────────┐
│ 1. Abrir terminal                   │
│    ↓                                │
│ 2. Instalar biblioteca requests     │
│    $ pip install requests           │
│    ↓                                │
│ 3. Verificar instalação             │
│    $ pip show requests              │
│    ↓                                │
│ 4. Rodar script novamente           │
│    ✅ Funciona!                     │
└─────────────────────────────────────┘

## 🎯 Implementação

### Visão Geral (Simples):

1. **Instalar biblioteca faltante**
   Resultado: Python encontrará o módulo requests

2. **Validar instalação**
   Resultado: Confirmar que tudo funcionou

3. **Testar seu script**
   Resultado: Erro desaparece

⏱️ Tempo estimado: 1 minuto

---

### Plano Técnico:

**Comandos que vou executar:**
```bash
# 1. Instalar requests
pip install requests

# 2. Verificar instalação
pip show requests
```

**Se você tiver requirements.txt, vou atualizar também:**
- Adicionar `requests==2.31.0` em `requirements.txt`

**Posso executar isso agora?**
```

---

## Exemplo 4: Criar Nova Funcionalidade (Sistema de Notificações)

### Input do Usuário
```
"Preciso criar um sistema de notificações por email e WhatsApp pro meu app.
Como organizar isso?"
```

### Output da Skill

```markdown
# 🎓 Sistema de Notificações Multi-Canal

## Arquitetura Recomendada (Explicação)

Imagine um **centro de distribuição de correspondências**:

- Você escreve uma mensagem (notificação)
- Centro de distribuição decide: vai por carta (email) ou Correios expressos (WhatsApp)?
- Cada canal tem seu "carteiro" especializado
- Você só se preocupa com a mensagem, não com como entregar

## Como Funciona (Diagrama)

```
┌──────────────────────────────────────────────────────┐
│              Seu App                                 │
│  notification_service.send("Pedido aprovado!", user) │
└───────────────────┬──────────────────────────────────┘
                    │
        ┌───────────▼───────────┐
        │ NotificationManager   │ (Centro de Distribuição)
        │ - decide canal        │
        │ - formata mensagem    │
        └───────┬───────────┬───┘
                │           │
       ┌────────▼─────┐  ┌──▼─────────┐
       │ EmailSender  │  │ WhatsAppSender │
       │ (SMTP/API)   │  │ (Evolution API)│
       └──────────────┘  └────────────────┘
```

## Estrutura de Arquivos

```
notifications/
├── __init__.py
├── manager.py              # Centro de distribuição
├── channels/
│   ├── __init__.py
│   ├── email.py           # Carteiro email
│   └── whatsapp.py        # Carteiro WhatsApp
├── templates/
│   ├── order_approved.html
│   └── order_approved.txt
└── config.py              # Configurações
```

## 🎯 Plano para Implementar

### Visão Geral (Simples):

1. **Criar estrutura base** (pastas + arquivos)
   Resultado: Organização profissional do código

2. **Implementar cada canal** (Email e WhatsApp separados)
   Resultado: Cada canal funciona independente

3. **Criar gerenciador central** (decide qual canal usar)
   Resultado: Interface única para enviar notificações

4. **Adicionar templates** (mensagens reutilizáveis)
   Resultado: Fácil criar novos tipos de notificação

5. **Testar e integrar** com seu app
   Resultado: Sistema funcionando end-to-end

⏱️ Tempo estimado: 20-30 minutos

---

### Plano Técnico (Executável):

#### Arquivos que vou criar:

**1. notifications/manager.py**
```python
class NotificationManager:
    def send(self, message, user, channels=['email', 'whatsapp']):
        """Envia notificação pelos canais especificados"""
        # Lógica de roteamento
```

**2. notifications/channels/email.py**
```python
class EmailSender:
    def send(self, to, subject, body):
        """Envia email via SMTP/API"""
```

**3. notifications/channels/whatsapp.py**
```python
class WhatsAppSender:
    def send(self, phone, message):
        """Envia WhatsApp via Evolution API"""
```

**4. Integração com seu app:**
```python
# Uso simples:
from notifications import NotificationManager

notifier = NotificationManager()
notifier.send(
    message="Seu pedido #123 foi aprovado!",
    user=user_obj,
    channels=['whatsapp']  # ou ['email'] ou ambos
)
```

#### Ferramentas que vou usar:
- Write (criar novos arquivos)
- Bash (instalar dependências se necessário)
- Read (verificar configurações existentes)

#### Benefícios desta arquitetura:
✅ **Extensível**: Adicionar SMS/Push no futuro é fácil
✅ **Testável**: Cada canal pode ser testado isoladamente
✅ **Reutilizável**: Templates evitam código duplicado
✅ **Manutenível**: Mudanças em um canal não afetam outros

---

**Posso implementar isso para você?** (confirme antes de eu criar os arquivos)
```

---

## Exemplo 5: Mentoria Estratégica (Monetização de App)

### Input do Usuário
```
"Tenho um app de receitas vegetarianas com 5k usuários.
Como monetizar sem afastar os usuários?"
```

### Output da Skill

```markdown
# 💰 Estratégia de Monetização - App de Receitas

## Análise do Contexto

Você tem:
- ✅ Produto validado (5k usuários = tem demanda)
- ✅ Nicho específico (vegetariano = comunidade engajada)
- ⚠️ Preocupação legítima (monetizar sem afastar usuários)

## Estratégias Recomendadas (por Prioridade)

### 1. Modelo Freemium (Melhor Opção)

**Analogia:** É como Spotify Free vs Premium

**Free (mantém maioria feliz):**
- Acesso a 80% das receitas
- Busca básica
- Salvar favoritos (limite de 20)

**Premium (R$ 9.90/mês):**
- 100% das receitas + exclusivas semanais
- Plano de refeições semanal automático
- Lista de compras inteligente
- Sem anúncios
- Modo offline

**Por que funciona:**
- 95% dos usuários continuam usando (grátis)
- 5% convertem (250 usuários × R$9.90 = R$2,475/mês)
- Não "tira" nada de quem já usa

### 2. Parcerias com Marcas Vegetarianas (Receita Passiva)

**Analogia:** Como blogueiros de culinária ganham

**Como funciona:**
- Marcas de alimentos vegetarianos te pagam
- Para destacar produtos nas receitas
- Exemplo: "Esta receita usa Tofu X"

**Projeção:**
- 3-5 parcerias × R$ 500-1000/mês
- Receita extra: R$ 1,500 - 5,000/mês

### 3. eBook Premium (Lançamento pontual)

**Produto:**
- "30 Dias de Receitas Vegetarianas Completas"
- R$ 29.90 (compra única)
- Distribuir para sua base de 5k usuários

**Projeção conservadora:**
- 2% convertem (100 vendas) = R$ 2,990
- Sem custo recorrente de manutenção

## 🎯 Plano de Implementação (Fase 1: Freemium)

### Visão Geral:

1. **Definir paywall** (o que é free vs premium)
   Resultado: Clareza do que oferecer em cada tier

2. **Integrar pagamentos** (Stripe/PagSeguro)
   Resultado: Sistema de cobrança funcionando

3. **Criar funcionalidades premium** (plano de refeições)
   Resultado: Valor real para quem pagar

4. **Soft launch** (oferecer para 10% da base)
   Resultado: Validar antes de escalar

5. **Analisar conversão e ajustar**
   Resultado: Otimizar baseado em dados reais

⏱️ Tempo estimado: 2-3 semanas

---

### Plano Técnico (High-Level):

**Mudanças no app:**

1. **Sistema de autenticação + assinatura**
   - Adicionar campo `subscription_tier` no banco
   - Criar middleware de validação
   - Integrar Stripe Checkout

2. **Paywalls estratégicos**
   - Após usuário salvar 20 receitas (limite free)
   - Ao tentar acessar "Plano Semanal"
   - CTA sutil no footer

3. **Funcionalidade Premium: Plano de Refeições**
   - Input: Preferências alimentares
   - Output: 7 dias de café/almoço/jantar
   - Gera lista de compras automática

**Tech stack sugerido:**
- Stripe (pagamentos) - já integrado facilmente
- PostgreSQL (adicionar coluna subscription)
- Celery (gerar planos de refeição em background)

---

### Próximos Passos

Quer que eu:
A) **Detalhe o plano técnico** de implementação do Freemium?
B) **Crie templates de email** para anunciar premium aos usuários?
C) **Analise viabilidade** de parcerias com marcas?

Me diz qual caminho seguir!
```

---

## Padrões Observados nos Exemplos

### Estrutura Consistente

Todos os exemplos seguem:
1. **Explicação ELI5** com analogia
2. **Diagrama visual** (ASCII ou descrição)
3. **Exemplo prático** concreto
4. **Plano dual** (simples + técnico)
5. **Pergunta de confirmação** antes de executar

### Adaptação por Contexto

- **Exemplo 1 (Explicação):** Foco em didática
- **Exemplo 2 (Implementação):** Foco em código
- **Exemplo 3 (Problema):** Foco em solução rápida
- **Exemplo 4 (Arquitetura):** Foco em design de sistema
- **Exemplo 5 (Estratégia):** Foco em business + tech

### Linguagem Acessível

Uso consistente de:
- Analogias do cotidiano
- Emojis para clareza visual
- Evitar jargões (ou explicar quando usar)
- Perguntas para guiar próximos passos
