# 🤖 Chatbot Imobiliária Premium

**Nicho:** Imobiliária
**Descrição:** Vendas de imóveis residenciais e comerciais de alto padrão
**Framework:** v2.0 MCP Híbrido ✨

## 🚀 Setup Rápido

### 1. Instalar MCP (Primeira vez)

```bash
cd whatsapp-chatbot-imobili-ria-premium
chmod +x INSTALAR_MCP.sh
./INSTALAR_MCP.sh
```

### 2. Configurar Chatwoot + Evolution

Edite `chatwoot_config_imobili-ria-premium.json`:
- Chatwoot token + inbox_id
- Evolution API key

### 3. Criar Agenda Google Sheets

```bash
# Autenticar OAuth (1x)
python3 componentes/escalonamento/autenticar_google.py

# Criar planilha
python3 componentes/escalonamento/criar_agenda_publica_oauth.py
```

### 4. Adicionar Imóveis

Estrutura em `imoveis/`:

```
imoveis/
└── apartamento-leblon-001/
    ├── base.txt
    ├── detalhes.txt
    ├── faq.txt
    └── links.json
```

### 5. Iniciar Bot

```bash
./INICIAR_COM_NGROK.sh
```

## 🛠️ Componentes

### Ferramentas Locais (0ms overhead)
- ✅ lista_imoveis - Lista itens
- ✅ consulta_faq - FAQ do item ativo
- ✅ taguear_cliente - Marca interesse
- ✅ agendar_visita - Agenda (2 etapas)

### Ferramentas MCP (~150ms cada)
- ✅ analisar_sentimento - Análise emocional
- ✅ gerar_proposta_comercial - Proposta formal
- ✅ buscar_itens_similares - Busca semântica
- ✅ calcular_financiamento - Simulação completa
- ✅ consultar_tabela_preco - Preço de mercado

### Automações
- ✅ Follow-ups automáticos
- ✅ Score de leads (0-100)
- ✅ Escalonamento inteligente
- ✅ Agenda Google Sheets
- ✅ Áudio (Whisper) + Imagem (GPT-4o)
- ✅ Métricas e relatórios

## 📊 Portas

- Bot: 5007
- Middleware: 5008

## 🔧 Manutenção

```bash
# Ver logs
tail -f logs/chatbot_imobili-ria-premium.log

# Parar
./PARAR_BOT_IMOBILI-RIA-PREMIUM.sh && pkill -f ngrok

# Adicionar imóvel
# 1. Criar pasta em imoveis/
# 2. Preencher arquivos .txt
# 3. Upload fotos: python3 upload_fotos_imoveis.py
```

## 🔌 Arquitetura Híbrida

```
Chatbot → RAG Híbrido
            ├─ Ferramentas Locais (rápidas)
            └─ Ferramentas MCP (pesadas)
```

**Decisão Inteligente:** A IA escolhe automaticamente qual ferramenta usar baseado no contexto.

---

**Framework:** Chatbot Universal v2.0 MCP Híbrido
**Baseado em:** whatsapp-chatbot-carros (Automaia)
**Ferramentas:** 9 (4 locais + 5 MCP)
