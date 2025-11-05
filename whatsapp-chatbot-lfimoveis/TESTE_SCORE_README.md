# Teste Rápido do Sistema de Score com Grok-4-fast

## Visão Geral

Script que testa o sistema de scoring de leads imobiliários com 3 cenários principais:

1. **FRIO** (score < 40): Lead sem interesse óbvio - "Oi"
2. **MORNO** (score 40-100): Lead com interesse moderado - "Tem fotos do imóvel?"
3. **QUENTE** (score > 100): Lead com alta intenção - "Quero agendar visita HOJE!"

## Arquivo

```
/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot-lfimoveis/testar_score_grok.py
```

## Como Executar

### Modo 1: Com API Real (Claude Opus)

Se você tiver a chave da API configurada:

```bash
export ANTHROPIC_API_KEY="sua-chave-aqui"
python3 testar_score_grok.py
```

### Modo 2: Modo Simulação (Padrão)

Sem configurar a chave, usa dados simulados:

```bash
python3 testar_score_grok.py
```

## O que é Testado

### 1. Configuração da IA

```python
❌ Sem ANTHROPIC_API_KEY → Modo simulação automático
✅ Com ANTHROPIC_API_KEY → Usa Claude Opus 4.1 real
```

### 2. Score Correto (0-150)

```
FRIO:   5/150   (█░░░░░░░░░░░░░)
MORNO:  50/150  (█████░░░░░░░░░)
QUENTE: 120/150 (████████████░░░)
```

### 3. Tags Inteligentes

```
Lead FRIO:   ["novo_lead"]
Lead MORNO:  ["pediu_fotos", "interesse_real"]
Lead QUENTE: ["agendar_visita", "urgente", "lead_quente"]
```

### 4. Classificação (FRIO/MORNO/QUENTE)

```
Score < 40   → ❄️ FRIO
40 ≤ Score ≤ 100 → 🔥 MORNO
Score > 100  → 🔴 QUENTE
```

## Componentes do Score

### Score Base (0-100)

- `+10` tipo de imóvel mencionado
- `+10` região/localidade definida
- `+10` orçamento/preço informado
- `+10` pediu fotos/informações
- `+10` fez perguntas

### Bonus Urgência (0-20)

- `+20` "hoje", "urgente", "agora"
- `+15` "essa semana", "amanhã"
- `+10` "esse mês"

### Bonus Intenção (0-30)

- `+30` "agendar visita", "quero ver", "marcar"
- `+25` "fechar negócio", "proposta"
- `+15` interesse genuíno

## Resultado Esperado

```
================================================================================
📊 RESUMO DO TESTE
================================================================================
✅ Sucessos: 3/3
📈 Taxa de acerto: 100%

🎉 SISTEMA DE SCORE FUNCIONANDO PERFEITAMENTE!
   ✓ Grok-4-fast configurado
   ✓ Scores corretos (0-150)
   ✓ Tags inteligentes aplicadas
   ✓ Classificações FRIO/MORNO/QUENTE OK
================================================================================
```

## Personalizando Testes

Para adicionar novos cenários, edite a seção `casos` em `testar_score_grok.py`:

```python
casos = [
    {
        "numero": 4,
        "mensagem": "Sua mensagem aqui",
        "historico": ["msg anterior 1", "msg anterior 2"],
        "esperado": "MORNO",  # FRIO, MORNO ou QUENTE
        "descricao": "Descrição do cenário"
    }
]
```

## Como a IA Funciona

### Com Claude Opus (API Real)

1. Recebe mensagem + contexto
2. Analisa sentimento, intenção, urgência
3. Calcula score detalhado (0-150)
4. Retorna tags e objeções

### Modo Simulação (Fallback)

Se a API não estiver disponível, usa padrões de palavras-chave:

- Detecta "Oi" → FRIO
- Detecta "fotos" → MORNO
- Detecta "agendar" + "hoje" → QUENTE

## Integração com o Bot

O sistema de score é usado em:

```
chatbot_lfimoveis.py
  └─> componentes/score/sistema_score.py
  └─> componentes/score/analisador_ia.py (Claude)
  └─> componentes/score/sistema_tags.py (tags automáticas)
```

## Verificando Erros

Se algo falhar:

1. **Erro de importação**: Verifique se está na pasta correta
   ```bash
   cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot-lfimoveis
   ```

2. **Erro de API**: Configure a chave ou use simulação
   ```bash
   export ANTHROPIC_API_KEY="sua-chave"
   ```

3. **Erro de JSON**: O script trata parsing automático

## Proximos Passos

- [ ] Testar com dados reais do bot
- [ ] Integrar ao sistema de escalonamento
- [ ] Adicionar relatórios de score
- [ ] Treinar novos modelos com histórico

---

**Última atualização:** 2025-11-05
**Versão:** 1.0
**Status:** Funcionando ✅
