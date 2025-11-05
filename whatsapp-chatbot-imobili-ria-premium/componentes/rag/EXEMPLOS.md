# 📘 EXEMPLOS PRÁTICOS - RAG + PROGRESSIVE DISCLOSURE

Exemplos reais de uso do sistema.

---

## 🎯 EXEMPLO 1: Uso Básico

```python
from componentes.rag import IntegradorRAG
from upstash_redis import Redis
from pathlib import Path

# Setup
imoveis_dir = Path("imoveis")
openai_key = "sk-proj-..."
openrouter_key = "sk-or-v1-..."
redis = Redis(url="...", token="...")

# Criar integrador
integrador = IntegradorRAG(imoveis_dir, openai_key, openrouter_key, redis)

# Processar mensagem
resposta = integrador.processar_mensagem(
    cliente_numero="5531980160822",
    mensagem="Apartamento 2 quartos Savassi",
    contexto=[]
)

print(resposta)
```

**Output esperado:**
```
Achei 2 opções na Savassi! 😊
1️⃣ Rua Pernambuco - 2 quartos
2️⃣ Rua Sergipe - 2 quartos
Qual te interessa mais? Me fala o número!
```

---

## 🔍 EXEMPLO 2: RAG Híbrido Standalone

```python
from componentes.rag import RAGHibrido
from pathlib import Path

# Setup
imoveis_dir = Path("imoveis")
openai_key = "sk-proj-..."

# Criar RAG
rag = RAGHibrido(imoveis_dir, openai_key)

# Buscar
candidatos = rag.buscar("Apartamento 2 quartos Savassi pet friendly até 2000")

# Mostrar resultados
print(f"Encontrados: {len(candidatos)} candidatos\n")

for i, candidato in enumerate(candidatos, 1):
    print(f"{i}. {candidato['id']}")
    print(f"   Tipo: {candidato.get('tipo')}")
    print(f"   Quartos: {candidato.get('quartos')}")
    print(f"   Região: {candidato.get('regiao')}")
    print(f"   Pet friendly: {candidato.get('pet_friendly')}")
    print(f"   Preço: R$ {candidato.get('preco')}")
    print()
```

**Output esperado:**
```
Encontrados: 2 candidatos

1. apto-savassi-001
   Tipo: apartamento
   Quartos: 2
   Região: savassi
   Pet friendly: True
   Preço: R$ 1800

2. apto-savassi-002
   Tipo: apartamento
   Quartos: 2
   Região: savassi
   Pet friendly: True
   Preço: R$ 1950
```

---

## 📚 EXEMPLO 3: Progressive Disclosure Standalone

```python
from componentes.rag import ProgressiveDisclosure
from pathlib import Path

# Setup
imoveis_dir = Path("imoveis")

# Criar disclosure
disclosure = ProgressiveDisclosure(imoveis_dir)

# Cenário 1: Pergunta básica
print("=== Pergunta básica ===")
niveis = disclosure.detectar_nivel("Me fala sobre esse imóvel")
print(f"Níveis: {niveis}")

dados = disclosure.carregar("apto-savassi-001", niveis)
print(f"Tokens: {dados['tokens']}")
print()

# Cenário 2: Pergunta específica (IPTU)
print("=== Pergunta sobre IPTU ===")
niveis = disclosure.detectar_nivel("Qual o IPTU?")
print(f"Níveis: {niveis}")

dados = disclosure.carregar("apto-savassi-001", niveis)
print(f"Tokens: {dados['tokens']}")
print()

# Cenário 3: Múltiplas informações
print("=== Múltiplas informações ===")
niveis = disclosure.detectar_nivel("Qual a metragem e o IPTU?")
print(f"Níveis: {niveis}")

dados = disclosure.carregar("apto-savassi-001", niveis)
print(f"Tokens: {dados['tokens']}")
print()

# Formatar para prompt
texto = disclosure.formatar_para_prompt(dados)
print("=== Texto formatado ===")
print(texto[:500] + "...")
```

**Output esperado:**
```
=== Pergunta básica ===
Níveis: ['base']
Tokens: 200

=== Pergunta sobre IPTU ===
Níveis: ['base', 'faq']
Tokens: 700

=== Múltiplas informações ===
Níveis: ['base', 'detalhes', 'faq']
Tokens: 1000

=== Texto formatado ===
## INFORMAÇÕES BÁSICAS

Apartamento moderno de 2 quartos no coração de BH...

## DETALHES TÉCNICOS

Área útil: 75m²...

## PERGUNTAS FREQUENTES

Qual o valor?
R$ 450.000,00...
```

---

## 🤖 EXEMPLO 4: IA Especialista Standalone

```python
from componentes.rag import IAEspecialista, ProgressiveDisclosure
from pathlib import Path

# Setup
openrouter_key = "sk-or-v1-..."
imoveis_dir = Path("imoveis")

# Criar componentes
disclosure = ProgressiveDisclosure(imoveis_dir)
ia = IAEspecialista(openrouter_key)

# Carregar dados
niveis = disclosure.detectar_nivel("Qual o IPTU?")
dados = disclosure.carregar("apto-savassi-001", niveis)

# Gerar resposta
resposta = ia.responder(
    dados_disclosure=dados,
    mensagem_cliente="Qual o IPTU?",
    contexto=[]
)

print(f"Tokens contexto: {dados['tokens']}")
print(f"Resposta: {resposta}")
```

**Output esperado:**
```
Tokens contexto: 700
Resposta: O IPTU é R$180/mês 👍
```

---

## 🔄 EXEMPLO 5: Conversa Completa (Simulação)

```python
from componentes.rag import IntegradorRAG
from upstash_redis import Redis
from pathlib import Path

# Setup
imoveis_dir = Path("imoveis")
openai_key = "sk-proj-..."
openrouter_key = "sk-or-v1-..."
redis = Redis(url="...", token="...")

integrador = IntegradorRAG(imoveis_dir, openai_key, openrouter_key, redis)

# Cliente de teste
cliente = "5531999999999"

# Limpa estado anterior
integrador.limpar_imóvel_ativo(cliente)

# === MENSAGEM 1: Busca inicial ===
print("👤 Cliente: Apartamento 2 quartos Savassi")
print()

resposta1 = integrador.processar_mensagem(
    cliente,
    "Apartamento 2 quartos Savassi"
)

print(f"🤖 Bot: {resposta1}")
print()
print("-" * 60)
print()

# === MENSAGEM 2: Escolha ===
print("👤 Cliente: O primeiro")
print()

resposta2 = integrador.processar_mensagem(
    cliente,
    "O primeiro"
)

print(f"🤖 Bot: {resposta2}")
print()
print("-" * 60)
print()

# === MENSAGEM 3: Pergunta sobre IPTU ===
print("👤 Cliente: Qual o IPTU?")
print()

resposta3 = integrador.processar_mensagem(
    cliente,
    "Qual o IPTU?"
)

print(f"🤖 Bot: {resposta3}")
print()
print("-" * 60)
print()

# === MENSAGEM 4: Pergunta sobre metragem ===
print("👤 Cliente: Qual a metragem?")
print()

resposta4 = integrador.processar_mensagem(
    cliente,
    "Qual a metragem?"
)

print(f"🤖 Bot: {resposta4}")
print()
print("-" * 60)
print()

# === MENSAGEM 5: Pergunta sobre financiamento ===
print("👤 Cliente: Aceita financiamento?")
print()

resposta5 = integrador.processar_mensagem(
    cliente,
    "Aceita financiamento?"
)

print(f"🤖 Bot: {resposta5}")
print()

# Limpa teste
integrador.limpar_imóvel_ativo(cliente)
```

**Output esperado:**
```
👤 Cliente: Apartamento 2 quartos Savassi

🤖 Bot: Achei 2 opções na Savassi! 😊
1️⃣ Rua Pernambuco - 2 quartos
2️⃣ Rua Sergipe - 2 quartos
Qual te interessa mais? Me fala o número!

------------------------------------------------------------

👤 Cliente: O primeiro

🤖 Bot: Show! Vou te falar mais sobre esse imóvel. O que quer saber? 😊

------------------------------------------------------------

👤 Cliente: Qual o IPTU?

🤖 Bot: O IPTU é R$180/mês 👍

------------------------------------------------------------

👤 Cliente: Qual a metragem?

🤖 Bot: O apartamento tem 75m² de área útil 📐

------------------------------------------------------------

👤 Cliente: Aceita financiamento?

🤖 Bot: Sim! Aceita financiamento pela Caixa, Banco do Brasil e Itaú. Quer simular? 😊
```

---

## 🔄 EXEMPLO 6: Migração de Imóveis

```python
from componentes.rag.migrar_imoveis import MigradorImoveis
from pathlib import Path

# Setup
imoveis_dir = Path("imoveis")

# Criar migrador (dry-run)
migrador = MigradorImoveis(imoveis_dir, dry_run=True)

# Executar
migrador.migrar_todos()
```

**Output esperado:**
```
🔄 Migrando 2 imóveis...
   Dry run: True

📦 apto-savassi-001
   [DRY RUN] Criaria base.txt:
   Apartamento moderno e espaçoso de 2 quartos no coração de BH...

   [DRY RUN] Criaria detalhes.txt:
   📐 DETALHES TÉCNICOS
   75m² de área útil...

   ✅ Criados: base.txt, detalhes.txt, faq.txt (mantido)

📦 lote-cascata-001
   ✅ Criados: base.txt, faq.txt

✅ Migração concluída!
```

---

## 🧪 EXEMPLO 7: Testes Automatizados

```python
# Execute o script de testes
import subprocess

resultado = subprocess.run(
    ["python3", "componentes/rag/test_rag.py"],
    cwd="/path/to/whatsapp-chatbot",
    capture_output=True,
    text=True
)

print(resultado.stdout)

if resultado.returncode == 0:
    print("\n✅ Todos os testes passaram!")
else:
    print("\n❌ Alguns testes falharam")
    print(resultado.stderr)
```

**Output esperado:**
```
🧪 TESTES RAG + PROGRESSIVE DISCLOSURE
============================================================

📁 Diretório imóveis: /path/to/imoveis
📦 Imóveis disponíveis: 2

============================================================
🧪 TESTE 1: RAG HÍBRIDO
============================================================

📋 Cenário 1: Busca específica
--------------------------------------------------
🔍 RAG Híbrido: Iniciando busca...
   Database: 2 imóveis
   Filtro keywords: 2 candidatos
   Ranking semântico: Não necessário (2 <= 3)
✅ RAG Híbrido: 2 imóveis retornados
✅ Retornou 2 candidatos
   1. apto-savassi-001 - apartamento - savassi
   2. apto-savassi-002 - apartamento - savassi

... [mais testes] ...

============================================================
✅ TODOS OS TESTES PASSARAM!
============================================================

📊 RESUMO:
   ✅ RAG Híbrido funcionando
   ✅ Progressive Disclosure funcionando
   ✅ 2 Estágios funcionando
   ✅ Integração completa funcionando
   ✅ Economia de tokens validada
```

---

## 🔧 EXEMPLO 8: Verificar Estado no Redis

```python
from upstash_redis import Redis

redis = Redis(url="...", token="...")

cliente = "5531980160822"

# Ver imóvel ativo
imóvel_ativo = redis.get(f"imóvel_ativo:{cliente}")
if imóvel_ativo:
    print(f"Imóvel ativo: {imóvel_ativo.decode()}")
else:
    print("Sem imóvel ativo")

# Ver candidatos salvos
candidatos = redis.get(f"candidatos:{cliente}")
if candidatos:
    import json
    lista = json.loads(candidatos.decode())
    print(f"Candidatos: {len(lista)}")
    for c in lista:
        print(f"  - {c['id']}")
else:
    print("Sem candidatos salvos")

# Ver contexto
contexto = redis.get(f"contexto:{cliente}")
if contexto:
    import json
    msgs = json.loads(contexto.decode())
    print(f"Contexto: {len(msgs)} mensagens")
else:
    print("Sem contexto")
```

**Output esperado:**
```
Imóvel ativo: apto-savassi-001
Candidatos: 2
  - apto-savassi-001
  - apto-savassi-002
Contexto: 8 mensagens
```

---

## 📊 EXEMPLO 9: Análise de Economia

```python
from componentes.rag import ProgressiveDisclosure
from pathlib import Path

imoveis_dir = Path("imoveis")
disclosure = ProgressiveDisclosure(imoveis_dir)

# Simula diferentes tipos de perguntas
perguntas = [
    "Me fala sobre esse imóvel",
    "Qual o IPTU?",
    "Qual a metragem?",
    "Aceita financiamento?",
    "Tem documentação regularizada?"
]

print("📊 ANÁLISE DE ECONOMIA DE TOKENS\n")
print("-" * 60)

total_pd = 0
total_completo = 0

for pergunta in perguntas:
    # Progressive Disclosure
    niveis = disclosure.detectar_nivel(pergunta)
    tokens_pd = disclosure.estimar_tokens(niveis)

    # Completo (modo antigo)
    tokens_completo = 1700  # Estimativa V4 atual

    economia = 1 - (tokens_pd / tokens_completo)

    print(f"\n❓ \"{pergunta}\"")
    print(f"   Níveis: {niveis}")
    print(f"   PD: {tokens_pd} tokens")
    print(f"   Completo: {tokens_completo} tokens")
    print(f"   Economia: {economia*100:.0f}%")

    total_pd += tokens_pd
    total_completo += tokens_completo

print("\n" + "=" * 60)
print(f"\n📊 TOTAL ({len(perguntas)} perguntas):")
print(f"   PD: {total_pd} tokens")
print(f"   Completo: {total_completo} tokens")
print(f"   Economia média: {(1 - total_pd/total_completo)*100:.0f}%")
```

**Output esperado:**
```
📊 ANÁLISE DE ECONOMIA DE TOKENS

------------------------------------------------------------

❓ "Me fala sobre esse imóvel"
   Níveis: ['base']
   PD: 200 tokens
   Completo: 1700 tokens
   Economia: 88%

❓ "Qual o IPTU?"
   Níveis: ['base', 'faq']
   PD: 700 tokens
   Completo: 1700 tokens
   Economia: 59%

❓ "Qual a metragem?"
   Níveis: ['base', 'detalhes']
   PD: 500 tokens
   Completo: 1700 tokens
   Economia: 71%

❓ "Aceita financiamento?"
   Níveis: ['base', 'faq', 'financiamento']
   PD: 1100 tokens
   Completo: 1700 tokens
   Economia: 35%

❓ "Tem documentação regularizada?"
   Níveis: ['base', 'legal']
   PD: 500 tokens
   Completo: 1700 tokens
   Economia: 71%

============================================================

📊 TOTAL (5 perguntas):
   PD: 3000 tokens
   Completo: 8500 tokens
   Economia média: 65%
```

---

## 🎯 EXEMPLO 10: Integração com Chatbot V4

```python
# No arquivo chatbot_corretor_v4.py

# === NO TOPO DO ARQUIVO ===
from componentes.rag import IntegradorRAG

# === APÓS INICIALIZAR REDIS ===
integrador_rag = IntegradorRAG(
    IMOVEIS_DIR,
    OPENAI_API_KEY,
    OPENROUTER_API_KEY,
    redis
)

print("✅ IntegradorRAG inicializado", flush=True)

# === NA FUNÇÃO processar_mensagem_ia() ===
def processar_mensagem_ia(numero_cliente, mensagem_agregada, contexto):
    """
    Processa mensagem usando RAG + Progressive Disclosure
    """

    # Usa IntegradorRAG em vez da lógica antiga
    resposta = integrador_rag.processar_mensagem(
        numero_cliente,
        mensagem_agregada,
        contexto
    )

    return resposta
```

---

**Criado:** 2025-11-04
**Versão:** 1.0
**Última atualização:** 2025-11-04
