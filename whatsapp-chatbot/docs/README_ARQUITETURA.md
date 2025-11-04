# 📚 DOCUMENTAÇÃO - CHATBOT PROFISSIONAL

**Versão:** 4.3 (Atual) + Framework Híbrido (Futuro)
**Data:** 04/11/2025

---

## 📄 DOCUMENTO PRINCIPAL

**[ARQUITETURA_COMPLETA_V4.md](ARQUITETURA_COMPLETA_V4.md)**

Documento mestre com:
- ✅ Estado atual do Bot V4 (tudo que funciona)
- 🚀 Framework Híbrido (futuro planejado)
- 📋 Roadmap de implementação (6 fases)

---

## 🎯 ACESSO RÁPIDO

### 📊 O QUE FUNCIONA HOJE (V4)

1. **Debounce Inteligente** → Agrupa mensagens (15s + IA)
2. **Transcrição Áudio** → Whisper (Português BR)
3. **Visão de Imagens** → GPT-4o (análise automática)
4. **Contexto Persistente** → Redis (14 dias, 30 mensagens)
5. **Fila no Redis** → Evita duplicação
6. **Mensagens Humanizadas** → Chunks com delay
7. **Resposta Direta** → Evolution (sem loop)
8. **Banco de Imóveis** → Carregamento automático

**Custo:** ~$0.60/mês (1.000 mensagens)

---

### 🚀 O QUE VEM NO FRAMEWORK

1. **RAG Híbrido** → Busca precisa (keywords + semântico)
2. **Progressive Disclosure** → Carrega só necessário (economia 50%)
3. **2 Estágios** → Identificação → Especialista (100% precisão)
4. **Sistema de Score** → 0-100 (qualificação automática)
5. **Tags Automáticas** → Chatwoot (organização)
6. **Follow-ups** → Reengajamento (2h, 24h, pós-visita)
7. **Escalonamento Inteligente** → Bot → Humano (momento certo)
8. **Relatórios Diários** → Métricas via WhatsApp (18h)

**Economia:** ~50% tokens | **Precisão:** 100%

---

## 🗺️ ROADMAP

| Fase | Objetivo | Tempo | Status |
|------|----------|-------|--------|
| **Fase 1** | RAG + Progressive Disclosure | 5h | 📋 Planejado |
| **Fase 2** | Score + Tags | 3h | 📋 Planejado |
| **Fase 3** | Follow-ups | 2h | 📋 Planejado |
| **Fase 4** | Escalonamento | 2h | 📋 Planejado |
| **Fase 5** | Relatórios | 1h | 📋 Planejado |
| **Fase 6** | Framework Reutilizável | 8h | 📋 Planejado |

**Tempo Total:** 21h (~3 dias úteis)

---

## 💡 CONCEITOS-CHAVE

### RAG (Retrieval Augmented Generation)
Busca informação relevante ANTES de responder (ao invés de injetar tudo no prompt).

### Progressive Disclosure
Carrega informações em camadas (só o necessário para cada pergunta).

### 2 Estágios
1. **Identificação** → Cliente escolhe item (RAG)
2. **Especialista** → IA focada APENAS nesse item (100% precisão)

### Orquestrador
Decide qual componente usar em cada momento (fluxo, IA, RAG, humano).

---

## 📞 SUPORTE

**Documentação completa:**
- `ARQUITETURA_COMPLETA_V4.md` → Documento mestre

**Arquivos relacionados:**
- `../chatbot_corretor_v4.py` → Código do bot atual
- `../webhook_middleware_v2.py` → Middleware Chatwoot
- `../README.md` → Guia de uso básico
- `../IMOVEIS_README.md` → Sistema de imóveis

---

**Última atualização:** 04/11/2025
