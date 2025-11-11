---
name: fix-skill
description: Corrige erros em skills automaticamente e registra aprendizados em LEARNINGS.md para prevenir recorrência. Auto-invoca quando usuário pedir para corrigir/fix skill após erro, ou usar comando /fix-skill. Atualiza SKILL.md e mantém histórico de correções.
---

# Fix Skill

Corrige automaticamente erros em skills e mantém histórico de aprendizados.

## Overview

Esta skill detecta e corrige erros em outras skills automaticamente através de:
1. **Detecção Automática** - Identifica qual skill falhou
2. **Análise de Erro** - Entende o problema específico
3. **Correção Automática** - Atualiza SKILL.md da skill problemática
4. **Registro de Aprendizado** - Cria/atualiza LEARNINGS.md com histórico
5. **Prevenção** - Garante que mesmo erro não aconteça novamente

**Objetivo:** Nunca repetir o mesmo erro duas vezes.

---

## Quando Usar

Auto-invoca quando usuário diz (após um erro de skill):
- "Corrige"
- "Fix"
- "Corrige esse erro"
- "Atualiza a skill"
- "/fix-skill" (comando direto)
- "Corrige o erro da skill X"

---

## Fluxo Principal

### Workflow Completo

```
Erro ocorre em skill
↓
Usuário pede correção
↓
1. Detectar skill que falhou
2. Identificar erro específico
3. Analisar SKILL.md
4. Aplicar correção
5. Registrar em LEARNINGS.md
6. Confirmar
```

---

## 1. Detectar Skill que Falhou

**Como identificar:**

### Opção A: Usuário especifica
```
Usuário: "Corrige o erro da skill gerar-foto-realista"
→ Skill: gerar-foto-realista
```

### Opção B: Última skill executada
```
[Histórico da conversa]
Skill gerar-foto-realista executou → erro
Usuário: "Corrige"
→ Skill: gerar-foto-realista (última que falhou)
```

### Opção C: Perguntar
```
Múltiplas skills falharam recentemente
→ Perguntar: "Qual skill deseja corrigir?"
```

**Validação:**
- Verificar se `.claude/skills/{skill_name}/` existe
- Verificar se `.claude/skills/{skill_name}/SKILL.md` existe

---

## 2. Identificar Erro Específico

**Análise do erro:**

### Tipos comuns de erros:

**A. Erro de sintaxe em comando**
```
Erro: "unrecognized arguments: --prompt"
↓
Problema: Flag --prompt não existe
Solução: Remover --prompt, usar argumento posicional
```

**B. Script não encontrado**
```
Erro: "No such file or directory: scripts/foo.py"
↓
Problema: Path incorreto
Solução: Corrigir path no SKILL.md
```

**C. Parâmetro incorreto**
```
Erro: "missing required argument: count"
↓
Problema: Faltando parâmetro
Solução: Adicionar parâmetro no comando
```

**D. Timeout ou falha de API**
```
Erro: "Request timeout"
↓
Problema: API demorou muito
Solução: Adicionar retry ou aumentar timeout
```

**Extração de informações:**
- Mensagem de erro completa
- Linha/comando que falhou
- Output do erro (se disponível)

---

## 3. Analisar SKILL.md

**Leitura da skill problemática:**

```bash
# Ler SKILL.md completo
cat .claude/skills/{skill_name}/SKILL.md
```

**Localizar seção problemática:**
- Buscar comando que gerou o erro
- Identificar linha exata (se possível)
- Entender contexto ao redor

**Exemplo:**
```markdown
Erro encontrado na linha 97:
python3 SCRIPTS/generate.py --prompt "texto"
                            ^^^^^^^^ (problema aqui)
```

---

## 4. Aplicar Correção

**Uso do script `update_skill.py`:**

```bash
python3 .claude/skills/fix-skill/scripts/update_skill.py \
    ".claude/skills/{SKILL_NAME}" \
    "{TEXTO_ANTIGO}" \
    "{TEXTO_NOVO}"
```

**Exemplos de correções:**

### Exemplo A: Remover flag incorreta
```bash
python3 .claude/skills/fix-skill/scripts/update_skill.py \
    ".claude/skills/gerar-foto-realista" \
    'python3 SCRIPTS/generate.py --prompt "{PROMPT}"' \
    'python3 SCRIPTS/generate.py "{PROMPT}"'
```

### Exemplo B: Corrigir path
```bash
python3 .claude/skills/fix-skill/scripts/update_skill.py \
    ".claude/skills/example-skill" \
    'scripts/foo.py' \
    '.claude/skills/example-skill/scripts/foo.py'
```

### Exemplo C: Adicionar parâmetro
```bash
python3 .claude/skills/fix-skill/scripts/update_skill.py \
    ".claude/skills/example-skill" \
    'script.py {PROMPT}' \
    'script.py --count 5 {PROMPT}'
```

**Validação:**
- Confirmar que texto antigo existe
- Verificar que substituição faz sentido
- Não sobrescrever se ambíguo

---

## 5. Registrar em LEARNINGS.md

**Uso do script `log_learning.py`:**

```bash
python3 .claude/skills/fix-skill/scripts/log_learning.py \
    ".claude/skills/{SKILL_NAME}" \
    "{DESCRIÇÃO_ERRO}" \
    "{DESCRIÇÃO_CORREÇÃO}" \
    "{LINHA_AFETADA}"
```

**Exemplo:**
```bash
python3 .claude/skills/fix-skill/scripts/log_learning.py \
    ".claude/skills/gerar-foto-realista" \
    "Erro: --prompt não reconhecido" \
    "Removido flag --prompt, usando argumento posicional" \
    "SKILL.md:97"
```

**O que acontece:**
- Se LEARNINGS.md não existe → cria do template
- Adiciona nova entrada no topo
- Formato padronizado com data, problema, correção

**Formato da entrada:**
```markdown
### 2025-01-07 - Erro: --prompt não reconhecido

**Problema:** Flag --prompt não existe no script
**Correção:** Removido --prompt, prompt agora é argumento posicional
**Linha afetada:** SKILL.md:97
**Status:** ✅ Corrigido

---
```

---

## 6. Confirmar

**Mensagem de confirmação:**

```
✅ Skill {nome} corrigida com sucesso!

📝 Correção aplicada:
   Removido: --prompt "{texto}"
   Novo: "{texto}" (argumento posicional)

📚 Aprendizado registrado:
   Arquivo: LEARNINGS.md
   Data: 2025-01-07
   Linha afetada: SKILL.md:97

🔄 Próxima execução não terá esse erro!
```

**Opcional:** Sugerir testar novamente
```
💡 Deseja testar a skill novamente agora?
```

---

## Validações

### Antes de Corrigir

1. **Skill existe:**
   - Verificar `.claude/skills/{skill_name}/`

2. **SKILL.md existe:**
   - Verificar `.claude/skills/{skill_name}/SKILL.md`

3. **Erro bem compreendido:**
   - Se erro ambíguo, perguntar mais detalhes ao usuário

4. **Correção clara:**
   - Se múltiplas soluções possíveis, perguntar qual aplicar

5. **Scripts disponíveis:**
   - Verificar `scripts/update_skill.py`
   - Verificar `scripts/log_learning.py`

---

## Tratamento de Erros

### Erro: Skill não encontrada
```
❌ Erro: Skill '{nome}' não encontrada em .claude/skills/
💡 Skills disponíveis: {lista}
```
→ Perguntar qual skill o usuário quis dizer

### Erro: Texto não encontrado no SKILL.md
```
⚠️  Aviso: Texto antigo não encontrado no SKILL.md
📝 Procurando: "{texto}"
💡 O erro pode já ter sido corrigido, ou texto mudou
```
→ Pedir ao usuário para confirmar texto exato

### Erro: Múltiplas ocorrências
```
⚠️  Aviso: Texto aparece {N} vezes no SKILL.md
💡 Qual ocorrência corrigir? (linha X, Y, Z)
```
→ Pedir ao usuário para especificar

### Erro: Scripts não encontrados
```
❌ Erro: Scripts de correção não encontrados
📁 Esperado: .claude/skills/fix-skill/scripts/
💡 Reinstalar skill fix-skill
```

---

## Exemplos Completos

### Exemplo 1: Erro de flag --prompt

```
[Contexto: skill gerar-foto-realista falhou]

Usuário: "Corrige"

fix-skill:
├─ Detecta: skill = gerar-foto-realista
├─ Identifica: erro = "--prompt não reconhecido"
├─ Lê: SKILL.md linha 97
├─ Correção:
│   old: 'python3 script.py --prompt "{text}"'
│   new: 'python3 script.py "{text}"'
├─ Executa: update_skill.py
├─ Executa: log_learning.py
└─ Confirma:
    "✅ Skill gerar-foto-realista corrigida!
     📝 Removido: --prompt
     📚 Registrado em LEARNINGS.md"
```

### Exemplo 2: Path incorreto

```
Usuário: "Fix o erro da skill example"

fix-skill:
├─ Detecta: skill = example
├─ Identifica: erro = "script não encontrado"
├─ Analisa: path incorreto "scripts/foo.py"
├─ Correção:
│   old: 'scripts/foo.py'
│   new: '.claude/skills/example/scripts/foo.py'
├─ Executa: update_skill.py
├─ Executa: log_learning.py
└─ Confirma: "✅ Path corrigido!"
```

### Exemplo 3: Usuário especifica skill

```
Usuário: "Corrige o erro da skill gerar-foto-realista que deu problema com --prompt"

fix-skill:
├─ Detecta: skill = gerar-foto-realista (especificada)
├─ Identifica: erro = "--prompt" (especificado)
├─ Lê SKILL.md
├─ Localiza: linha 97 com "--prompt"
├─ Correção automática
├─ Registra learning
└─ Confirma
```

---

## Scripts Bundled

### `scripts/update_skill.py`

**Função:** Atualiza SKILL.md de uma skill

**Uso:**
```bash
python3 scripts/update_skill.py <skill_path> <old_text> <new_text>
```

**Exemplo:**
```bash
python3 scripts/update_skill.py \
    .claude/skills/gerar-foto-realista \
    "--prompt" \
    ""
```

**Comportamento:**
- Lê SKILL.md
- Substitui old_text por new_text
- Salva arquivo
- Retorna sucesso/falha

---

### `scripts/log_learning.py`

**Função:** Registra aprendizado em LEARNINGS.md

**Uso:**
```bash
python3 scripts/log_learning.py <skill_path> <error_desc> <fix_desc> [line]
```

**Exemplo:**
```bash
python3 scripts/log_learning.py \
    .claude/skills/gerar-foto-realista \
    "Erro: --prompt não reconhecido" \
    "Removido --prompt" \
    "SKILL.md:97"
```

**Comportamento:**
- Cria LEARNINGS.md se não existe (do template)
- Adiciona nova entrada no topo
- Formato padronizado
- Retorna sucesso/falha

---

## Assets

### `assets/LEARNINGS_TEMPLATE.md`

**Função:** Template para criar LEARNINGS.md em skills

**Conteúdo:**
```markdown
# Learnings - {SKILL_NAME}

Este arquivo registra todos os erros corrigidos...

## Histórico de Correções

<!-- Entradas mais recentes primeiro -->
```

**Uso:** Copiado automaticamente pelo `log_learning.py` quando LEARNINGS.md não existe

---

## Notas Técnicas

### Estrutura de uma skill após correção

```
.claude/skills/gerar-foto-realista/
├── SKILL.md (✅ corrigido)
├── LEARNINGS.md (✅ criado/atualizado)
└── scripts/
    └── ...
```

### Quando LEARNINGS.md é criado

- Primeira vez que fix-skill corrige aquela skill
- Criado do template em `assets/LEARNINGS_TEMPLATE.md`
- Nome da skill substituído no template

### Backup automático

**Não implementado ainda.** Possível melhoria futura:
- Criar backup de SKILL.md antes de modificar
- `.claude/skills/{name}/SKILL.md.backup`

---

## Checklist de Execução

Para cada correção, seguir esta ordem:

- [ ] Detectar qual skill falhou
- [ ] Identificar erro específico
- [ ] Ler SKILL.md da skill
- [ ] Localizar linha/seção problemática
- [ ] Determinar correção apropriada
- [ ] Executar `update_skill.py`
- [ ] Executar `log_learning.py`
- [ ] Confirmar com detalhes da correção
- [ ] Sugerir testar novamente (opcional)

---

## Melhorias Futuras

Possíveis expansões desta skill:

1. **Backup automático** antes de modificar
2. **Análise de padrões** (erros recorrentes em múltiplas skills)
3. **Sugestões proativas** (detectar potenciais erros antes de acontecerem)
4. **Correção em batch** (corrigir mesmo erro em múltiplas skills)
5. **Integração com skill-creator** (adicionar learning system no template)
