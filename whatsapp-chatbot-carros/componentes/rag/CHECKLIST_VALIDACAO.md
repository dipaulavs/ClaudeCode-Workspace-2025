# ✅ CHECKLIST DE VALIDAÇÃO - RAG + PROGRESSIVE DISCLOSURE

Use este checklist para validar a implementação completa.

---

## 📂 1. ESTRUTURA DE ARQUIVOS

- [x] `componentes/rag/` criado
- [x] `componentes/rag/__init__.py` (exporta classes)
- [x] `componentes/rag/busca_hibrida.py` (RAG Híbrido)
- [x] `componentes/rag/progressive_disclosure.py` (Progressive Disclosure)
- [x] `componentes/rag/ia_especialista.py` (IA Especialista)
- [x] `componentes/rag/integrador.py` (Integrador)
- [x] `componentes/rag/migrar_imoveis.py` (Migração)
- [x] `componentes/rag/test_rag.py` (Testes)
- [x] `componentes/rag/README.md` (Documentação)
- [x] `componentes/rag/ARQUITETURA_VISUAL.md` (Diagramas)
- [x] `componentes/rag/EXEMPLOS.md` (Exemplos práticos)

**Status:** ✅ 11/11 arquivos criados

---

## 🧪 2. TESTES FUNCIONAIS

### 2.1 Imports

```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot

python3 -c "from componentes.rag import RAGHibrido; print('✅ RAGHibrido')"
python3 -c "from componentes.rag import ProgressiveDisclosure; print('✅ ProgressiveDisclosure')"
python3 -c "from componentes.rag import IAEspecialista; print('✅ IAEspecialista')"
python3 -c "from componentes.rag import IntegradorRAG; print('✅ IntegradorRAG')"
```

- [ ] RAGHibrido importa
- [ ] ProgressiveDisclosure importa
- [ ] IAEspecialista importa
- [ ] IntegradorRAG importa

**Esperado:** 4/4 imports funcionando

---

### 2.2 Migração de Imóveis

```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot

# Dry run primeiro
python3 componentes/rag/migrar_imoveis.py
# Quando solicitar, digite: dry-run

# Se OK, executar migração real
python3 componentes/rag/migrar_imoveis.py
# Quando solicitar, digite: s
```

- [ ] Dry run executou sem erros
- [ ] Arquivos `base.txt` criados
- [ ] Arquivos existentes mantidos
- [ ] Migração real executou sem erros

**Esperado:** 4/4 passos OK

---

### 2.3 Testes Automatizados

```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot

python3 componentes/rag/test_rag.py
```

- [ ] Teste 1: RAG Híbrido (busca)
- [ ] Teste 2: Progressive Disclosure (níveis)
- [ ] Teste 3: 2 Estágios (identificação → especialista)
- [ ] Teste 4: Integração completa
- [ ] Teste 5: Economia de tokens

**Esperado:** ✅ TODOS OS TESTES PASSARAM!

---

## 🎯 3. FUNCIONALIDADES

### 3.1 RAG Híbrido

- [ ] Filtro keywords funciona
- [ ] Ranking semântico funciona
- [ ] Retorna máximo 3 candidatos
- [ ] Detecta tipo (apartamento/casa/lote)
- [ ] Detecta quartos (1, 2, 3+)
- [ ] Detecta região (savassi, lourdes, etc)
- [ ] Detecta preço máximo
- [ ] Detecta pet friendly

**Esperado:** 8/8 funcionalidades

---

### 3.2 Progressive Disclosure

- [ ] Detecta nível base (sempre)
- [ ] Detecta nível detalhes (metragem, área, m²)
- [ ] Detecta nível faq (preço, IPTU, pet)
- [ ] Detecta nível legal (documentação)
- [ ] Detecta nível financiamento (banco, parcela)
- [ ] Carrega apenas arquivos necessários
- [ ] Estima tokens corretamente
- [ ] Formata para prompt

**Esperado:** 8/8 funcionalidades

---

### 3.3 IA Especialista

- [ ] Usa Claude Haiku 4.5
- [ ] Responde com contexto limitado
- [ ] Respostas curtas (2-3 frases)
- [ ] Linguagem informal WhatsApp
- [ ] Usa emojis moderadamente
- [ ] Não inventa informações
- [ ] Responde "vou consultar" quando não sabe

**Esperado:** 7/7 funcionalidades

---

### 3.4 Integrador (2 Estágios)

- [ ] ESTÁGIO 1: RAG Híbrido funciona
- [ ] Apresenta lista de candidatos
- [ ] Salva candidatos no Redis
- [ ] Detecta escolha numérica ("1", "o primeiro")
- [ ] Define item_ativo após escolha
- [ ] ESTÁGIO 2: Progressive Disclosure funciona
- [ ] IA Especialista responde corretamente
- [ ] Item_ativo persiste no Redis (TTL 1h)

**Esperado:** 8/8 funcionalidades

---

## 📊 4. MÉTRICAS

### 4.1 Economia de Tokens

Testar com pergunta típica: "Qual o IPTU?"

- [ ] Progressive Disclosure: ~700 tokens
- [ ] Carregamento completo: ~1.700 tokens
- [ ] Economia: >= 50%

**Esperado:** Economia >= 50%

---

### 4.2 Precisão

Testar com 5 perguntas diferentes:

- [ ] Resposta 1: Correta (baseada em dados)
- [ ] Resposta 2: Correta (baseada em dados)
- [ ] Resposta 3: Correta (baseada em dados)
- [ ] Resposta 4: Correta (baseada em dados)
- [ ] Resposta 5: Correta (baseada em dados)

**Esperado:** 5/5 respostas corretas = 100% precisão

---

### 4.3 Velocidade

- [ ] RAG busca: < 100ms
- [ ] Progressive Disclosure: < 5ms
- [ ] IA resposta: < 2s
- [ ] Total: < 2.2s

**Esperado:** 4/4 dentro do limite

---

## 🔧 5. INTEGRAÇÃO

### 5.1 Redis

- [ ] Item_ativo salva corretamente
- [ ] Item_ativo expira após 1h
- [ ] Candidatos salvam corretamente
- [ ] Candidatos expiram após 10min
- [ ] Contexto mantém estrutura original

**Esperado:** 5/5 funcionalidades Redis

---

### 5.2 Compatibilidade

- [ ] Funciona com Python 3.9+
- [ ] Não quebra Chatbot V4 existente
- [ ] APIs OpenAI funcionam
- [ ] API OpenRouter funciona
- [ ] Redis Upstash funciona

**Esperado:** 5/5 compatibilidades OK

---

## 📚 6. DOCUMENTAÇÃO

- [ ] README.md completo
- [ ] ARQUITETURA_VISUAL.md com diagramas
- [ ] EXEMPLOS.md com código executável
- [ ] Docstrings em todos os módulos
- [ ] Comentários explicativos no código
- [ ] Type hints completos

**Esperado:** 6/6 documentações

---

## 🚀 7. PRÓXIMOS PASSOS

### 7.1 Validação Local

- [ ] Migrar imóveis existentes
- [ ] Executar testes automatizados
- [ ] Testar manualmente 5 conversas
- [ ] Validar economia de tokens real
- [ ] Validar precisão das respostas

---

### 7.2 Integração com V4

- [ ] Adicionar imports no chatbot_corretor_v4.py
- [ ] Instanciar IntegradorRAG
- [ ] Substituir lógica antiga por integrador
- [ ] Testar em ambiente de desenvolvimento
- [ ] Validar sem quebrar funcionalidades existentes

---

### 7.3 Deploy Produção

- [ ] Testar com 10 conversas reais
- [ ] Monitorar logs de erro
- [ ] Validar métricas (tokens, precisão)
- [ ] Ajustar keywords se necessário
- [ ] Documentar aprendizados

---

## 📋 RESUMO FINAL

| Categoria | Checklist | Status |
|-----------|-----------|--------|
| **Arquivos** | 11/11 | ✅ |
| **Imports** | 4/4 | ⏸️ Testar |
| **Migração** | 4/4 | ⏸️ Executar |
| **Testes** | 5/5 | ⏸️ Executar |
| **RAG** | 8/8 | ⏸️ Validar |
| **Progressive D** | 8/8 | ⏸️ Validar |
| **IA** | 7/7 | ⏸️ Validar |
| **Integrador** | 8/8 | ⏸️ Validar |
| **Métricas** | 13/13 | ⏸️ Medir |
| **Redis** | 5/5 | ⏸️ Validar |
| **Docs** | 6/6 | ✅ |

---

## 🎯 CRITÉRIOS DE SUCESSO

### Mínimo Viável

- [x] Todos os arquivos criados
- [ ] Todos os testes passam
- [ ] Economia >= 30% tokens
- [ ] Precisão >= 90%

### Ideal

- [x] Todos os arquivos criados
- [ ] Todos os testes passam
- [ ] Economia >= 50% tokens
- [ ] Precisão = 100%
- [ ] Velocidade < 2.2s
- [ ] 0 erros em produção

---

## 🐛 TROUBLESHOOTING

### ❌ Import Error

**Problema:** `ModuleNotFoundError: No module named 'componentes'`

**Solução:**
```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot
python3 -c "from componentes.rag import IntegradorRAG"
```

---

### ❌ Redis Connection Error

**Problema:** `ConnectionError` ao acessar Redis

**Solução:**
- Verificar URL Redis: `https://legible-collie-9537.upstash.io`
- Verificar token Redis
- Testar conexão: `redis.ping()`

---

### ❌ OpenAI API Error

**Problema:** `401 Unauthorized` ao gerar embeddings

**Solução:**
- Verificar chave OpenAI
- Verificar quota em platform.openai.com
- Usar fallback (busca só por keywords)

---

### ❌ Claude API Error

**Problema:** `401 Unauthorized` ao gerar resposta

**Solução:**
- Verificar chave OpenRouter
- Verificar modelo disponível
- Testar endpoint diretamente

---

## ✅ VALIDAÇÃO FINAL

Quando todos os itens estiverem marcados:

```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot

echo "🎯 SISTEMA RAG + PROGRESSIVE DISCLOSURE"
echo "✅ Arquivos: OK"
echo "✅ Testes: OK"
echo "✅ Funcionalidades: OK"
echo "✅ Métricas: OK"
echo "✅ Documentação: OK"
echo ""
echo "🚀 PRONTO PARA INTEGRAÇÃO COM CHATBOT V4!"
```

---

**Criado:** 2025-11-04
**Versão:** 1.0
**Próxima revisão:** Após testes em produção
