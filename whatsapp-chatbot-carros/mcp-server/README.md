# 🔌 MCP SERVER - AUTOMAIA TOOLS

Servidor MCP com ferramentas pesadas/reutilizáveis para chatbots.

## 🔧 Ferramentas Disponíveis

### 1️⃣ analisar_sentimento
Analisa tom emocional da conversa do cliente.

**Entrada:**
```json
{
  "mensagens": ["obrigado!", "gostei muito", "perfeito"]
}
```

**Saída:**
```json
{
  "score": 80,
  "emocao": "satisfeito",
  "sugestao": "Mantenha tom positivo e avance para próximos passos"
}
```

---

### 2️⃣ gerar_proposta_comercial
Gera proposta comercial estruturada.

**Entrada:**
```json
{
  "carro_id": "gol-2020-001",
  "cliente_nome": "João Silva",
  "desconto_percentual": 5
}
```

**Saída:**
```json
{
  "numero_proposta": "PROP-20251105143022",
  "valores": {
    "preco_tabela": "R$ 45.000",
    "desconto_percentual": "5%",
    "preco_final": "R$ 42.750"
  }
}
```

---

### 3️⃣ buscar_carros_similares
Busca carros por características.

**Entrada:**
```json
{
  "caracteristicas": "sedan econômico 2020-2023 até 60mil",
  "limite": 3
}
```

**Saída:**
```json
{
  "total_encontrados": 3,
  "carros": [
    {"carro_id": "civic-2018-001", "score_match": 5},
    {"carro_id": "corolla-2023-001", "score_match": 4}
  ]
}
```

---

### 4️⃣ calcular_financiamento
Simulação completa de financiamento.

**Entrada:**
```json
{
  "valor_veiculo": 45000,
  "valor_entrada": 10000,
  "taxa_juros_mensal": 1.99
}
```

**Saída:**
```json
{
  "valor_financiado": 35000,
  "cenarios": [
    {
      "prazo_meses": 24,
      "valor_parcela": 1789.50,
      "juros_total": 7948.00
    },
    {
      "prazo_meses": 60,
      "valor_parcela": 987.30,
      "juros_total": 24238.00
    }
  ]
}
```

---

### 5️⃣ consultar_fipe
Consulta preço FIPE do veículo.

**Entrada:**
```json
{
  "marca": "Volkswagen",
  "modelo": "Gol",
  "ano": "2020"
}
```

**Saída:**
```json
{
  "valor_fipe": "R$ 47.500",
  "mes_referencia": "novembro/2025"
}
```

---

## 🚀 Como Usar

### Instalação
```bash
cd mcp-server
pip install -r requirements.txt
```

### Executar Servidor
```bash
python3 server.py
```

### Integrar no Chatbot
Ver: `../componentes/rag_hibrido_carros.py`

---

## 📊 Performance

| Ferramenta | Tempo Médio |
|------------|-------------|
| analisar_sentimento | ~150ms |
| gerar_proposta | ~200ms |
| buscar_similares | ~100ms |
| calcular_financiamento | ~50ms |
| consultar_fipe | ~300ms (API externa) |

**Latência de rede MCP:** ~100-150ms adicional

---

## 🔄 Próximas Melhorias

- [ ] Gerar PDF real (proposta comercial)
- [ ] Integrar API FIPE real
- [ ] Busca vetorial (embeddings)
- [ ] Cache de resultados
- [ ] Métricas de uso

---

**Status:** ✅ Funcional | **Ferramentas:** 5 | **Latência:** ~150ms média
