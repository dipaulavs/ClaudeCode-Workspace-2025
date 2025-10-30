# 🚨 REGRAS CRÍTICAS DO CLAUDE CODE - NUNCA IGNORE

## 📋 Regra #1: OUTPUT DE AGENTES OPENROUTER

**NUNCA MODIFICAR OU ALTERAR O OUTPUT DOS AGENTES**

Quando executar um agente via OpenRouter:
- ✅ Retornar a mensagem EXATAMENTE como o agente retornou
- ✅ Output deve ser IDÊNTICO ao original
- ❌ NUNCA resumir
- ❌ NUNCA simplificar
- ❌ NUNCA "melhorar a apresentação"
- ❌ NUNCA extrair apenas "os melhores"
- ❌ NUNCA criar versões reduzidas

### Exemplo Correto:
```
Usuário pede para ativar agente X
→ Executo o agente
→ Retorno TODO o output do agente SEM modificações
```

### Exemplo ERRADO (Não fazer):
```
Usuário pede para ativar agente X
→ Executo o agente
→ "Resumo" ou "destaco apenas o melhor"
→ ❌ ERRADO! Isso esconde informação do usuário
```

---

**Data de criação**: 2025-10-30
**Motivo**: Usuário solicitou 7 headlines, agente entregou 21 organizadas em 7 categorias. Claude resumiu para apenas 3, escondendo o trabalho completo do agente.

**Lição**: O usuário sabe o que quer. Não presuma que "menos é melhor". Mostre tudo.
