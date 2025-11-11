# Grok Image Skill - Learnings

## 2025-01-11: API Endpoint Update

### Problema
Grok-image skill falhando com erro 404 em `queryTask` endpoint.

### Causa Raiz
Kie.ai API mudou endpoint de query:
- ❌ **Antigo (removido):** `POST /api/v1/jobs/queryTask`
- ✅ **Novo (correto):** `GET /api/v1/jobs/recordInfo?taskId=XXX`

### Solução Aplicada
1. Atualizado `batch_generate_grok.py` função `query_task()`:
   - Mudou de POST para GET
   - Endpoint de `/queryTask` para `/recordInfo`
   - Parâmetro via query string

2. Atualizado `generate_grok_image.py` mesma correção

3. Adicionado state "waiting" aos estados válidos (além de pending/processing)

### Arquivos Modificados
- `.claude/skills/grok-image/scripts/batch_generate_grok.py` (linhas 50-83)
- `.claude/skills/grok-image/scripts/generate_grok_image.py` (linhas 63-100)

### Problema Adicional Encontrado
API retornava code 402: "Insufficient credits" - resolvido após usuário adicionar créditos.

### Resultado
✅ Skill funcionando perfeitamente
✅ Cada geração retorna 6 imagens
✅ Custo: $0.02 (4 créditos) por geração

### Prevenção
- Sempre consultar documentação atualizada da API
- Adicionar tratamento de erro 402 (sem créditos) com mensagem clara
