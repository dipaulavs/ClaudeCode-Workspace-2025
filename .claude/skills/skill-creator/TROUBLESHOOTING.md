# Troubleshooting - Skill Creator

Guia completo para resolver problemas ao criar Skills.

---

## 🚨 Erro: SKILL.md Passou de 80 Linhas

### Sintoma

```
SKILL.md criado com 95 linhas (limite: 80 linhas)
```

ou

Você percebe que o SKILL.md está muito longo e tem muitos detalhes técnicos.

### Causa

SKILL.md contém informação que deveria estar em REFERENCE.md:
- Documentação técnica detalhada
- Especificações de APIs
- Configurações extensas
- Algoritmos complexos
- Múltiplos exemplos longos

### Solução

**Passo a passo:**

1. **Identificar conteúdo para mover:**
```bash
# Ler SKILL.md e identificar seções longas
# Marcar seções com > 10 linhas de detalhes técnicos
```

2. **Mover para REFERENCE.md:**
```markdown
# No SKILL.md (ANTES):
## Configurações
- API_KEY: chave da API
- ENDPOINT: https://...
- TIMEOUT: 30s
[20 linhas de configurações...]

# No SKILL.md (DEPOIS):
## Configurações
Veja [REFERENCE.md](REFERENCE.md) para configurações completas.

# No REFERENCE.md (ADICIONAR):
## ⚙️ Configurações

### Variáveis de Ambiente
API_KEY=your_key
ENDPOINT=https://...
TIMEOUT=30
[20 linhas de configs...]
```

3. **Reduzir workflow para essencial:**
```markdown
# ANTES (detalhado demais no SKILL.md):
### Etapa 2: Validação
Usar biblioteca X para validar Y.
A biblioteca X funciona assim: [10 linhas]
Parâmetros: [15 linhas]

# DEPOIS (focado):
### Etapa 2: Validação
Usar biblioteca X para validar Y.
Para detalhes da biblioteca, veja [REFERENCE.md](REFERENCE.md).
```

4. **Verificar tamanho:**
```bash
wc -l .claude/skills/nome-da-skill/SKILL.md
# Deve retornar <= 80 linhas
```

### Prevenção

**ANTES de escrever SKILL.md:**
- [ ] Planejar: Workflow tem quantas etapas? (máx 5)
- [ ] Cada etapa: 3-5 linhas de descrição (não mais)
- [ ] Detalhes técnicos: SEMPRE no REFERENCE.md
- [ ] Exemplos longos: SEMPRE no EXAMPLES.md

**Regra prática:** Se você está escrevendo parágrafo > 5 linhas no SKILL.md, mova para REFERENCE.md.

### Relacionado

- Veja também: [Erro: Mistura de Documentação Técnica no SKILL.md](#-erro-mistura-de-documentação-técnica-no-skillmd)

---

## 🚨 Erro: Links Markdown Quebrados

### Sintoma

```
SKILL.md referencia [REFERENCE.md](reference.md)
Mas arquivo real é REFERENCE.md (maiúsculas)
Link não funciona!
```

ou

Claude tenta carregar arquivo referenciado mas não encontra.

### Causa

**Causa 1:** Case-sensitive errado
- Escrito: `[REFERENCE.md](reference.md)`
- Arquivo real: `REFERENCE.md`
- macOS/Windows: Pode funcionar (case-insensitive)
- Linux/Git: NÃO funciona (case-sensitive)

**Causa 2:** Path relativo errado
- Escrito: `[REFERENCE.md](./docs/REFERENCE.md)`
- Arquivo real: `REFERENCE.md` (mesma pasta)

**Causa 3:** Extensão faltando
- Escrito: `[EXAMPLES](EXAMPLES)`
- Arquivo real: `EXAMPLES.md`

### Solução

**Passo a passo:**

1. **Verificar case:**
```bash
# Listar arquivos reais
ls .claude/skills/nome-da-skill/
# Output: SKILL.md  REFERENCE.md  EXAMPLES.md  TROUBLESHOOTING.md
```

2. **Corrigir links no SKILL.md:**
```markdown
# ERRADO:
[REFERENCE.md](reference.md)
[Examples](examples.md)
[troubleshooting](TROUBLESHOOTING)

# CORRETO:
[REFERENCE.md](REFERENCE.md)
[EXAMPLES.md](EXAMPLES.md)
[TROUBLESHOOTING.md](TROUBLESHOOTING.md)
```

3. **Testar links:**
```bash
# Verificar que arquivos existem
test -f .claude/skills/nome-da-skill/REFERENCE.md && echo "OK"
test -f .claude/skills/nome-da-skill/EXAMPLES.md && echo "OK"
test -f .claude/skills/nome-da-skill/TROUBLESHOOTING.md && echo "OK"
```

4. **Grep para encontrar outros links:**
```bash
# Buscar todos os links markdown no SKILL.md
grep -E '\[.*\]\(.*\)' .claude/skills/nome-da-skill/SKILL.md
# Verificar cada um manualmente
```

### Prevenção

**Template de links (copiar sempre):**
```markdown
Veja [REFERENCE.md](REFERENCE.md) para detalhes.
Veja [EXAMPLES.md](EXAMPLES.md) para casos completos.
Veja [TROUBLESHOOTING.md](TROUBLESHOOTING.md) para erros.
```

**Checklist antes de commitar:**
- [ ] Todos os arquivos referenciados existem
- [ ] Case está correto (maiúsculas: REFERENCE, EXAMPLES, TROUBLESHOOTING)
- [ ] Extensão .md está presente
- [ ] Path não tem `./` desnecessário (arquivos na mesma pasta)

### Relacionado

- Documentação: [REFERENCE.md - Links e Referências](#)

---

## 🚨 Erro: Triggers Vagos na Description

### Sintoma

```yaml
description: Uma skill útil para fazer coisas com código
```

Skill não ativa automaticamente quando deveria.

ou

Claude não sabe quando usar a skill.

### Causa

Description não tem triggers claros:
- Verbos de ação vagos ("fazer coisas", "ajudar com")
- Sem contextos específicos
- Sem frases-gatilho
- Genérico demais

**Problema:** Claude é model-invoked - precisa de triggers específicos para decidir quando ativar a skill automaticamente.

### Solução

**Passo a passo:**

1. **Identificar ações específicas da skill:**
```
# Perguntar:
- O que EXATAMENTE a skill faz?
- Quais verbos o usuário usaria?
- Em que contexto seria usado?
- Que palavras-chave indicam essa tarefa?
```

2. **Formular description com triggers:**
```yaml
# VAGO (evitar):
description: Uma skill para APIs

# ESPECÍFICO (usar):
description: Use quando usuário pedir para validar APIs REST, testar endpoints HTTP, ou verificar responses. Ativa automaticamente com "validar API", "testar endpoint", "check API response".
```

**Template de description:**
```yaml
description: Use quando usuário pedir para [AÇÃO 1], [AÇÃO 2], ou [AÇÃO 3]. [Contexto adicional]. Ativa automaticamente com "[FRASE 1]", "[FRASE 2]", "[FRASE 3]".
```

3. **Exemplos de descriptions boas:**

**API Validator:**
```yaml
description: Use quando usuário pedir para validar APIs REST, testar endpoints, ou verificar responses HTTP. Ativa automaticamente com "validar API", "testar endpoint", "check API response".
```

**Code Analyzer:**
```yaml
description: Use quando usuário pedir para analisar qualidade de código Python, verificar PEP8, checar complexidade ciclomática, validar documentação, ou auditar segurança. Ativa com "analisar código", "check code quality", "audit Python code".
```

**Database Schema Validator:**
```yaml
description: Use quando usuário pedir para validar schema de banco de dados, verificar constraints, analisar indexes, checar relationships, ou otimizar performance. Suporta PostgreSQL, MySQL, MongoDB, SQLite. Ativa com "validar schema", "check database", "analyze DB schema".
```

4. **Testar triggers:**
```
# Testar frases que DEVERIAM ativar:
"Valide esta API"  → Skill ativa?
"Check API response" → Skill ativa?
"Teste este endpoint" → Skill ativa?

# Se não ativar, adicionar variação na description
```

### Prevenção

**Ao criar nova skill:**
1. Liste 5-10 frases que usuário poderia dizer
2. Identifique palavras-chave comuns
3. Inclua na description
4. Teste com variações

**Características de boa description:**
- ✅ Verbos de ação específicos
- ✅ Contextos claros
- ✅ Frases-gatilho entre aspas
- ✅ 2-3 sinônimos da mesma ação
- ✅ Menciona tecnologias/formatos suportados

**Características de description vaga:**
- ❌ "Skill útil para..."
- ❌ "Ajuda com..."
- ❌ "Faz coisas relacionadas a..."
- ❌ Sem verbos específicos
- ❌ Sem frases-gatilho

### Relacionado

- Veja: [REFERENCE.md - Especificações do Frontmatter YAML](#)
- Veja: [EXAMPLES.md - Galeria de Inputs Comuns](#)

---

## 🚨 Erro: Exemplos Genéricos no EXAMPLES.md

### Sintoma

```markdown
## Exemplo 1: Usar a Skill

### Contexto
Usuário quer usar a skill.

### Input
"Use a skill"

### Output
Skill foi usada com sucesso.
```

Exemplo não ajuda a entender caso real.

### Causa

Exemplos são muito genéricos:
- Sem contexto específico
- Input vago
- Output incompleto
- Sem detalhes do processo
- Sem observações/insights

### Solução

**Passo a passo:**

1. **Usar caso real (ou criar um realista):**
```markdown
# GENÉRICO (evitar):
## Exemplo 1: Validar API
Usuário: "Valide a API"
Claude: "API validada"

# ESPECÍFICO (usar):
## Exemplo 1: Validar API Pública do GitHub

### Contexto
Usuário está desenvolvendo integração com GitHub e quer verificar
se a API pública está funcionando corretamente antes de implementar.
Precisa validar endpoints de repos, users, e issues.

### Input do Usuário
```
"Valide a API do GitHub - endpoints de repos, users e issues:
https://api.github.com"
```

### Processo de Execução
**Etapa 1: Análise**
- Identificado: API REST pública
- Endpoints a testar: /repos, /users, /issues
- Autenticação: Não necessária (endpoints públicos)

**Etapa 2: Validação**
- GET /users/octocat → 200 OK (1.2s)
- GET /repos/octocat/Hello-World → 200 OK (0.8s)
- GET /repos/octocat/Hello-World/issues → 200 OK (1.5s)
- Schemas validados: ✅ Todos conformes

**Etapa 3: Relatório**
- Gerado: github_api_validation.md
- Status: ✅ Todos endpoints funcionando
- Performance: Boa (< 2s por request)

### Output Gerado
```
✅ API GitHub validada com sucesso!

📊 Resultados:
  • 3 endpoints testados
  • 3 responses válidas (100%)
  • Tempo médio: 1.2s

📝 Relatório: github_api_validation.md

💡 API está pronta para integração!
```

### Observações
- **Insight 1:** API pública não precisa auth, simplifica teste
- **Insight 2:** Response times variaram (0.8s - 1.5s), considerar cache
- **Variação:** Para API privada, adicionar header Authorization
```

2. **Estrutura completa obrigatória:**
```markdown
## Exemplo [N]: [Nome ESPECÍFICO]

### Contexto
[Situação real do usuário, problema específico, objetivos]

### Input do Usuário
```
[Input EXATO, com detalhes]
```

### Processo de Execução
[Cada etapa com o que aconteceu]

### Output Gerado
```
[Output COMPLETO, não resumido]
```

### Arquivos Criados/Modificados (se aplicável)
[Lista de arquivos]

### Observações
- **Insight 1:** [Aprendizado]
- **Insight 2:** [Detalhe importante]
- **Variação:** [Como adaptar]
```

3. **Mínimo 2 exemplos diferentes:**
- Exemplo 1: Caso simples (happy path)
- Exemplo 2: Caso complexo ou com desafios
- Exemplo 3 (opcional): Edge case

4. **Verificar qualidade:**
```bash
# Perguntas para validar exemplo:
# - Está claro o problema do usuário?
# - Input é copiável/reproduzível?
# - Processo mostra cada etapa?
# - Output está completo (não "...")?
# - Tem insights úteis?

# Se respondeu "não" em alguma: reescrever exemplo
```

### Prevenção

**Ao criar EXAMPLES.md:**
1. Basear em casos reais sempre que possível
2. Se inventar: Ser MUITO específico
3. Incluir números, nomes, URLs reais
4. Mostrar outputs completos
5. Adicionar observações com insights

**Checklist de exemplo bom:**
- [ ] Contexto explica situação específica
- [ ] Input é reproduzível
- [ ] Processo mostra todas as etapas
- [ ] Output está completo (não truncado)
- [ ] Tem observações com insights
- [ ] Variações estão documentadas

### Relacionado

- Veja: [REFERENCE.md - Estrutura de Cada Exemplo](#)
- Veja: [EXAMPLES.md para referência](#)

---

## 🚨 Erro: Estrutura Não Segue Progressive Disclosure

### Sintoma

Skill criada com estrutura diferente:
```
nome-da-skill/
└── SKILL.md (arquivo único de 200 linhas)
```

ou

```
nome-da-skill/
├── skill.md
├── docs.md
└── errors.md
```

### Causa

**Causa 1:** Não seguiu o padrão de 4 arquivos
**Causa 2:** Nomes de arquivos incorretos (lowercase, nomes diferentes)
**Causa 3:** Tentou usar estrutura antiga (single file)

### Solução

**Passo a passo:**

1. **Verificar estrutura atual:**
```bash
ls .claude/skills/nome-da-skill/
# O que tem?
```

2. **Criar estrutura correta:**
```bash
cd .claude/skills/nome-da-skill/

# Se tiver apenas SKILL.md grande:
# 1. Backup
cp SKILL.md SKILL.md.backup

# 2. Criar arquivos vazios
touch REFERENCE.md EXAMPLES.md TROUBLESHOOTING.md

# 3. Dividir conteúdo:
# - Workflow principal → SKILL.md
# - Docs técnicas → REFERENCE.md
# - Exemplos → EXAMPLES.md
# - Erros → TROUBLESHOOTING.md
```

3. **Renomear se nomes errados:**
```bash
# Se arquivos em lowercase:
mv skill.md SKILL.md
mv reference.md REFERENCE.md
mv examples.md EXAMPLES.md
mv troubleshooting.md TROUBLESHOOTING.md

# Se nomes diferentes:
mv docs.md REFERENCE.md
mv errors.md TROUBLESHOOTING.md
```

4. **Verificar estrutura final:**
```bash
ls .claude/skills/nome-da-skill/
# Deve ter:
# SKILL.md
# REFERENCE.md
# EXAMPLES.md
# TROUBLESHOOTING.md
```

5. **Atualizar links no SKILL.md:**
```markdown
Veja [REFERENCE.md](REFERENCE.md)
Veja [EXAMPLES.md](EXAMPLES.md)
Veja [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
```

### Prevenção

**SEMPRE usar estrutura padrão:**
```
.claude/skills/nome-da-skill/
├── SKILL.md                # Workflow (30-60 linhas)
├── REFERENCE.md            # Docs técnicas
├── EXAMPLES.md             # Casos de uso (min 2)
└── TROUBLESHOOTING.md      # Erros (min 2)
```

**Nomes obrigatórios:**
- ✅ SKILL.md (maiúsculas)
- ✅ REFERENCE.md (maiúsculas)
- ✅ EXAMPLES.md (maiúsculas)
- ✅ TROUBLESHOOTING.md (maiúsculas)

**Nunca:**
- ❌ skill.md (lowercase)
- ❌ docs.md (nome diferente)
- ❌ README.md (confunde com docs de projeto)
- ❌ Arquivo único grande

### Relacionado

- Veja: [REFERENCE.md - Estrutura Padrão](#)

---

## 🚨 Erro: Faltam Exemplos Mínimos

### Sintoma

```
.claude/skills/nome-da-skill/
├── SKILL.md
├── REFERENCE.md
├── EXAMPLES.md (vazio ou com 1 exemplo apenas)
└── TROUBLESHOOTING.md
```

ou

EXAMPLES.md tem menos de 2 exemplos.

### Causa

Esqueceu de adicionar exemplos suficientes ou apenas criou placeholders.

### Solução

**Passo a passo:**

1. **Identificar casos de uso:**
```
# Perguntas:
- Qual é o caso mais simples? (happy path)
- Qual é um caso mais complexo?
- Há algum edge case importante?
```

2. **Criar mínimo 2 exemplos:**

**Exemplo 1 - Simples:**
```markdown
## Exemplo 1: [Caso Simples - Happy Path]

### Contexto
[Situação mais comum, tudo funciona]

### Input do Usuário
```
[Input direto]
```

### Processo de Execução
[Workflow padrão]

### Output Gerado
[Resultado esperado]

### Observações
[Insights básicos]
```

**Exemplo 2 - Complexo/Edge Case:**
```markdown
## Exemplo 2: [Caso Complexo ou Edge Case]

### Contexto
[Situação com múltiplas variáveis ou caso raro]

### Input do Usuário
```
[Input mais elaborado]
```

### Processo de Execução
[Workflow com adaptações]

### Desafios Encontrados
- [Desafio 1 e como foi resolvido]

### Output Gerado
[Resultado]

### Observações
[Insights avançados]
```

3. **Adicionar Galeria de Inputs:**
```markdown
## Galeria de Inputs Comuns

Variações de input que ativam a skill:

```
"[Variação 1]"
"[Variação 2]"
"[Variação 3]"
"[Variação 4]"
```

Todos seguem workflow padrão.
```

### Prevenção

**Checklist ao criar EXAMPLES.md:**
- [ ] Tem mínimo 2 exemplos completos
- [ ] Exemplo 1 é caso simples (happy path)
- [ ] Exemplo 2 é caso complexo ou edge case
- [ ] Cada exemplo tem todas as seções (Contexto, Input, Processo, Output, Observações)
- [ ] Tem "Galeria de Inputs Comuns" ao final

**Regra:** NUNCA commitar skill com < 2 exemplos no EXAMPLES.md.

### Relacionado

- Veja: [Erro: Exemplos Genéricos](#)
- Veja: [REFERENCE.md - EXAMPLES.md Especificação](#)

---

## 🚨 Erro: Validação de Frontmatter YAML Falhou

### Sintoma

```
Error: Invalid YAML frontmatter in SKILL.md
```

ou

Skill não é reconhecida por Claude Code.

### Causa

**Causa 1:** Sintaxe YAML errada
```yaml
---
name: nome da skill  # ERRADO: espaços no nome
description: [falta fechar aspas
---
```

**Causa 2:** Campos obrigatórios faltando
```yaml
---
name: minha-skill
# description: faltou!
---
```

**Causa 3:** Delimitadores incorretos
```markdown
--  # ERRADO: só 2 hífens
name: skill
---
```

### Solução

**Passo a passo:**

1. **Verificar sintaxe:**
```yaml
# Template correto:
---
name: nome-da-skill
description: [Descrição com triggers claros]
allowed-tools: Read, Write  # (opcional)
---
```

2. **Validar campos:**

**Campo `name` (obrigatório):**
- ✅ lowercase
- ✅ hífens (não underscores ou espaços)
- ✅ máx 64 chars
- ✅ Exemplo: `api-validator`, `code-analyzer`
- ❌ Não: `API Validator`, `api_validator`, `ApiValidator`

**Campo `description` (obrigatório):**
- ✅ String (com ou sem aspas)
- ✅ máx 1024 chars
- ✅ Com triggers claros
- ❌ Não vazio

**Campo `allowed-tools` (opcional):**
- ✅ Lista separada por vírgula: `Read, Write, Edit, Bash`
- ✅ Ou array YAML: `[Read, Write, Edit]`
- Se omitido: Claude pode usar todas as ferramentas

3. **Testar YAML:**
```bash
# Instalar yamllint (se não tiver):
pip install yamllint

# Validar YAML:
yamllint .claude/skills/nome-da-skill/SKILL.md
# Ou online: https://www.yamllint.com/
```

4. **Corrigir erros comuns:**

**Erro: Aspas não fechadas**
```yaml
# ERRADO:
description: Use quando "validar API

# CORRETO:
description: Use quando validar API
# ou
description: "Use quando validar API"
```

**Erro: Caracteres especiais**
```yaml
# ERRADO:
description: Use quando: validar API  # ":" confunde YAML

# CORRETO:
description: Use quando validar API ou testar endpoints
```

**Erro: Delimitadores**
```yaml
# ERRADO:
--
name: skill
--

# CORRETO:
---
name: skill
---
```

### Prevenção

**Template seguro (copiar sempre):**
```yaml
---
name: nome-da-skill
description: Use quando usuário pedir para [AÇÃO]. Ativa com [TRIGGERS].
allowed-tools: Read, Write, Edit, Bash
---
```

**Checklist antes de salvar:**
- [ ] Delimitadores: `---` (3 hífens) no início e fim
- [ ] Campo `name` presente (lowercase, hífens)
- [ ] Campo `description` presente (não vazio)
- [ ] Sem aspas quebradas
- [ ] Sem `:` em lugares errados

**Validação online rápida:**
```
1. Copiar frontmatter YAML
2. Colar em: https://www.yamllint.com/
3. Verificar se válido
```

### Relacionado

- Veja: [REFERENCE.md - YAML Frontmatter Obrigatório](#)

---

## 🔍 Debugging Geral

### Se Nenhuma Solução Acima Funcionou

**1. Verificar estrutura completa:**
```bash
# Listar arquivos
ls -la .claude/skills/nome-da-skill/

# Deve ter:
# SKILL.md
# REFERENCE.md
# EXAMPLES.md
# TROUBLESHOOTING.md
```

**2. Verificar conteúdo de cada arquivo:**
```bash
# SKILL.md tem frontmatter?
head -10 .claude/skills/nome-da-skill/SKILL.md

# Tamanho OK?
wc -l .claude/skills/nome-da-skill/SKILL.md
# Deve ser <= 80 linhas

# Outros arquivos não estão vazios?
wc -l .claude/skills/nome-da-skill/*.md
```

**3. Testar links:**
```bash
# Extrair todos os links
grep -E '\[.*\]\(.*\)' .claude/skills/nome-da-skill/SKILL.md

# Verificar que arquivos referenciados existem
# Links devem ser: REFERENCE.md, EXAMPLES.md, TROUBLESHOOTING.md
```

**4. Validar YAML:**
```bash
# Extrair frontmatter
sed -n '/^---$/,/^---$/p' .claude/skills/nome-da-skill/SKILL.md

# Copiar output e validar em: https://www.yamllint.com/
```

**5. Comparar com skill existente:**
```bash
# Usar estudar-video como referência:
diff .claude/skills/nome-da-skill/SKILL.md .claude/skills/estudar-video/SKILL.md

# Estrutura deve ser similar
```

---

## 📊 Checklist de Validação Completo

Antes de considerar a skill pronta, verificar:

### Estrutura
- [ ] Pasta `.claude/skills/nome-da-skill/` existe
- [ ] SKILL.md existe
- [ ] REFERENCE.md existe
- [ ] EXAMPLES.md existe
- [ ] TROUBLESHOOTING.md existe
- [ ] Nomes em MAIÚSCULAS corretos

### SKILL.md
- [ ] Frontmatter YAML válido
- [ ] Campo `name` presente (lowercase, hífens)
- [ ] Campo `description` presente com triggers claros
- [ ] Tamanho: 30-80 linhas
- [ ] Referencia outros arquivos com links corretos
- [ ] Tem seção "Quando Usar"
- [ ] Tem workflow numerado
- [ ] Tem "Regras Importantes"

### REFERENCE.md
- [ ] Não está vazio
- [ ] Contém documentação técnica detalhada
- [ ] Configurações/parâmetros documentados
- [ ] APIs/integrações explicadas

### EXAMPLES.md
- [ ] Tem mínimo 2 exemplos completos
- [ ] Cada exemplo tem: Contexto, Input, Processo, Output, Observações
- [ ] Exemplos são específicos (não genéricos)
- [ ] Tem "Galeria de Inputs Comuns"

### TROUBLESHOOTING.md
- [ ] Tem mínimo 2 erros documentados
- [ ] Cada erro tem: Sintoma, Causa, Solução, Prevenção
- [ ] Tem seção "Debugging Geral"
- [ ] Tem "Checklist de Validação"

### Links
- [ ] Todos os links markdown funcionam
- [ ] Case correto (SKILL.md, não skill.md)
- [ ] Extensões presentes (.md)

### Integração
- [ ] CLAUDE.md atualizado (seção Skills)
- [ ] Commit criado: `feat: adicionar skill nome-da-skill`
- [ ] Testado manualmente

---

## 🆘 Quando Pedir Ajuda

Se após seguir todos os passos o problema persistir:

1. **Coletar informações:**
```bash
# Estrutura de arquivos
ls -la .claude/skills/nome-da-skill/

# Conteúdo do frontmatter
head -10 .claude/skills/nome-da-skill/SKILL.md

# Tamanhos dos arquivos
wc -l .claude/skills/nome-da-skill/*.md

# Links encontrados
grep -E '\[.*\]\(.*\)' .claude/skills/nome-da-skill/SKILL.md
```

2. **Criar issue com:**
   - Descrição do problema
   - Output dos comandos acima
   - O que você já tentou
   - Skill que está criando (propósito)

3. **Onde buscar ajuda:**
   - Documentação oficial: https://docs.claude.com/en/docs/claude-code/skills.md
   - Comparar com skills existentes: `estudar-video`, `orshot`, etc

---

## 📈 Erros por Frequência

| Erro | Frequência | Tempo Médio de Resolução |
|------|------------|--------------------------|
| SKILL.md muito longo | 🔴 Alta | 5min (mover conteúdo para REFERENCE.md) |
| Links quebrados | 🔴 Alta | 2min (corrigir case) |
| Triggers vagos | 🟡 Média | 10min (reescrever description) |
| Exemplos genéricos | 🟡 Média | 15min (criar exemplos concretos) |
| Estrutura errada | 🟡 Média | 5min (renomear/reorganizar) |
| Faltam exemplos | 🟢 Baixa | 10min (adicionar 1-2 exemplos) |
| YAML inválido | 🟢 Baixa | 3min (corrigir sintaxe) |

---

## 💡 Dicas para Evitar Problemas

### 1. Use o Script Auxiliar

```bash
# Criar skill com estrutura automática:
python3 scripts/claude-skills/create_skill.py nome-da-skill

# Já cria 4 arquivos com templates corretos
```

### 2. Copie de Skill Existente

```bash
# Usar skill existente como base:
cp -r .claude/skills/estudar-video .claude/skills/minha-skill

# Depois adaptar conteúdo
```

### 3. Valide Antes de Commitar

```bash
# Checklist rápido:
wc -l .claude/skills/minha-skill/SKILL.md  # <= 80?
ls .claude/skills/minha-skill/  # 4 arquivos?
grep "description:" .claude/skills/minha-skill/SKILL.md  # Tem triggers?
```

### 4. Teste Manualmente

```
# Após criar skill, testar:
"[Frase que deveria ativar a skill]"

# Skill ativou? Se não, melhorar triggers na description
```

---

**Total de erros documentados:** 7 principais
**Última atualização:** 02/11/2025
**Contribuições:** Para adicionar novo erro, use este template e crie PR
