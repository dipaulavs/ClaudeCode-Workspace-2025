# 🔌 TEMPLATE CHATBOT v2.0 - MCP Híbrido

Template genérico para criar chatbots WhatsApp com arquitetura híbrida (Function Calling + MCP).

---

## 🎯 O Que É MCP Híbrido?

Combina o melhor dos dois mundos:

```
┌────────────────────────────────────────┐
│         CHATBOT (WhatsApp)             │
└────────────────┬───────────────────────┘
                 │
         ┌───────▼────────┐
         │  RAG HÍBRIDO   │
         └───────┬────────┘
                 │
        ┌────────┴────────┐
        │                 │
┌───────▼───────┐  ┌──────▼──────┐
│ FERRAMENTAS   │  │ FERRAMENTAS │
│ LOCAIS (4)    │  │  MCP (5)    │
├───────────────┤  ├─────────────┤
│ • lista       │  │ • sentimento│
│ • faq         │  │ • proposta  │
│ • taguear     │  │ • similares │
│ • agendar     │  │ • financ.   │
└───────────────┘  │ • tabela    │
  0ms latência     └─────────────┘
                    ~150ms latência
```

**Decisão inteligente:** A IA escolhe automaticamente qual ferramenta usar.

---

## ⚙️ Personalização (OBRIGATÓRIA)

### 1. MCP Server (`mcp-server/server.py`)

**Renomeie o servidor:**
```python
# Linha 38
app = Server("template-tools")  # ← MUDAR para "seu-negocio-tools"
```

**Ajuste ferramentas:**
- Mantenha as 5 padrão OU
- Adicione novas ferramentas específicas
- Remova ferramentas desnecessárias

### 2. RAG Híbrido (`componentes/rag_hibrido.py`)

**Ajuste prompt:**
```python
# Linha 55-85: system_prompt
# CUSTOMIZAR conforme seu negócio
```

**Renomeie referências:**
```python
# itens → carros/imoveis/produtos
# item → carro/imovel/produto
```

### 3. Ferramentas Locais (`ferramentas/`)

**Adapte para seu negócio:**
- `lista_itens.py` → `lista_carros.py`
- `consulta_faq.py` (ajustar parsing)
- `tagueamento.py` (OK genérico)
- `agendar_visita.py` (OK genérico)

---

## 🚀 Uso Automático

O script `criar_chatbot_cliente.py` faz tudo automaticamente:

```bash
python3 criar_chatbot_cliente.py
```

**O que ele faz:**
1. ✅ Valida que template tem estrutura MCP
2. ✅ Copia todo o template
3. ✅ Renomeia `itens/` → `carros/` (conforme nicho)
4. ✅ Renomeia `template-tools` → `seu-negocio-tools`
5. ✅ Ajusta todas as referências automaticamente
6. ✅ Cria README personalizado

**Resultado:** Chatbot pronto com 9 ferramentas!

---

## 📁 Estrutura do Template

```
chatbot-template/
├── mcp-server/
│   ├── server.py            ← MCP Server (5 ferramentas)
│   ├── requirements.txt
│   └── README.md
│
├── componentes/
│   ├── cliente_mcp.py       ← Cliente MCP
│   ├── rag_hibrido.py       ← RAG Híbrido (9 ferramentas)
│   ├── escalonamento/
│   ├── followup/
│   ├── score/
│   └── relatorios/
│
├── ferramentas/
│   ├── lista_itens.py       ← Lista itens (CUSTOMIZAR)
│   ├── consulta_faq.py      ← FAQ (CUSTOMIZAR)
│   ├── tagueamento.py       ← Tags Chatwoot
│   └── agendar_visita.py    ← Agendamento
│
├── itens/                   ← Pasta genérica (será renomeada)
│   └── .gitkeep
│
├── INSTALAR_MCP.sh          ← Instala dependências MCP
├── README_MCP.md            ← Este arquivo
└── personalidade.txt        ← Prompt da IA
```

---

## 🔧 Quando Personalizar Manualmente

**Personalização automática (criar_chatbot_cliente.py):**
- ✅ Renomeia pastas/arquivos
- ✅ Substitui palavras-chave (itens → carros)
- ✅ Ajusta portas/configs
- ✅ Cria README

**Personalização manual (você faz):**
- ⚠️ Ferramentas MCP específicas do negócio
- ⚠️ Parsing de dados (base.txt, detalhes.txt)
- ⚠️ Prompt da IA (tom, personalidade)
- ⚠️ Integrações adicionais (APIs externas)

---

## 📊 Performance Esperada

| Cenário | Tempo Médio |
|---------|-------------|
| Cliente lista itens | 1.4s (local) |
| Cliente calcula financiamento | 1.7s (MCP) |
| Cliente agenda + calcula | 3.0s (híbrido) |

**Vantagem híbrida:** ~50ms ganho por conversa em 70% dos casos.

---

## 🆕 Versão 2.0 - Changelog

**Novo:**
- ✅ Estrutura MCP híbrida
- ✅ 5 ferramentas MCP padrão
- ✅ RAG híbrido genérico
- ✅ Cliente MCP reutilizável
- ✅ Validação de template no script de criação

**Compatibilidade:**
- ✅ Mantém todas as features v1.0
- ✅ Backward compatible (pode usar só locais)
- ✅ MCP opcional (ativa se server_path fornecido)

---

## 📖 Referências

- **MCP Protocol:** https://modelcontextprotocol.io/
- **Anthropic MCP Docs:** https://docs.anthropic.com/mcp
- **Framework Original:** whatsapp-chatbot-carros (Automaia)

---

**Versão:** 2.0.0 | **Ferramentas:** 9 (4 locais + 5 MCP) | **Status:** ✅ Prod-ready
