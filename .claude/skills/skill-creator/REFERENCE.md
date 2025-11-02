# Referência Técnica - Skill Creator

Este arquivo contém documentação técnica completa sobre Progressive Disclosure e templates para criação de Skills.

---

## 📐 Progressive Disclosure: O Conceito

### O Que É

Progressive Disclosure é um padrão de design que apresenta informações gradualmente, mostrando apenas o essencial primeiro e revelando detalhes conforme necessário.

**Aplicado a Skills:**
- Claude carrega apenas o arquivo principal (SKILL.md) inicialmente
- Arquivos adicionais são carregados sob demanda quando Claude precisa de informações específicas
- Economiza tokens e melhora performance

### Como Funciona na Prática

```
1. Skill ativa → Claude lê SKILL.md (sempre)
   ↓
2. Precisa de detalhes técnicos → Claude lê REFERENCE.md (sob demanda)
   ↓
3. Precisa de exemplo → Claude lê EXAMPLES.md (sob demanda)
   ↓
4. Encontra erro → Claude lê TROUBLESHOOTING.md (sob demanda)
```

**Benefício:** Carrega ~45 linhas inicialmente, em vez de 200+ linhas de arquivo único.

### Comparação: Antes vs Depois

#### ❌ Estrutura Antiga (Arquivo Único)

```
estudar-video/
└── SKILL.md (226 linhas)
    ├─ Instruções (40 linhas)
    ├─ Documentação técnica (80 linhas)
    ├─ Exemplos (50 linhas)
    ├─ Troubleshooting (30 linhas)
    └─ Histórico (26 linhas)
```

**Problema:** 226 linhas carregadas sempre, mesmo quando não necessário!

#### ✅ Estrutura Nova (Progressive Disclosure)

```
estudar-video/
├── SKILL.md (45 linhas) ← Sempre carregado
├── REFERENCE.md (80 linhas) ← Sob demanda
├── EXAMPLES.md (50 linhas) ← Sob demanda
└── TROUBLESHOOTING.md (30 linhas) ← Sob demanda
```

**Benefício:** 80% de redução no carregamento inicial!

---

## 📁 Estrutura Completa de uma Skill

### Estrutura Padrão (4 Arquivos Obrigatórios)

```
.claude/skills/
└── nome-da-skill/
    ├── SKILL.md                # Instruções principais (30-60 linhas, máx 80)
    ├── REFERENCE.md            # Documentação técnica detalhada
    ├── EXAMPLES.md             # Casos de uso reais (mínimo 2)
    └── TROUBLESHOOTING.md      # Guia de erros comuns (mínimo 2)
```

### Estrutura Estendida (Com Scripts/Templates)

```
.claude/skills/
└── nome-da-skill/
    ├── SKILL.md
    ├── REFERENCE.md
    ├── EXAMPLES.md
    ├── TROUBLESHOOTING.md
    ├── scripts/                # (Opcional) Scripts auxiliares
    │   ├── helper.py
    │   ├── validator.py
    │   └── utils.py
    └── templates/              # (Opcional) Templates de arquivos
        ├── output.md.template
        ├── config.yaml.template
        └── README.md
```

---

## 📄 SKILL.md - Especificação Detalhada

### Propósito

Arquivo principal com workflow focado e claro. É o único arquivo carregado automaticamente quando a skill é ativada.

### Especificações Técnicas

**Tamanho:**
- Ideal: 30-60 linhas
- Máximo absoluto: 80 linhas
- Se passar de 80 linhas, mover conteúdo para REFERENCE.md

**YAML Frontmatter (Obrigatório):**

```yaml
---
name: nome-da-skill              # lowercase, hífens, máx 64 chars
description: [Descrição]         # triggers claros, máx 1024 chars
allowed-tools: Read, Write       # (opcional) restringe ferramentas
---
```

**Campo `name`:**
- Formato: lowercase com hífens
- Exemplos válidos: `api-validator`, `code-analyzer`, `estudar-video`
- Exemplos inválidos: `API_Validator`, `Code Analyzer`, `estudarVideo`

**Campo `description`:**
- Deve incluir triggers claros que ativam a skill automaticamente
- Usar verbos de ação: "Use quando usuário pedir para..."
- Mencionar contextos específicos
- Máximo 1024 caracteres

**Campo `allowed-tools` (opcional):**
- Se presente, restringe ferramentas que Claude pode usar
- Ferramentas comuns: Read, Write, Edit, Bash, Grep, Glob
- Se omitido, Claude pode usar todas as ferramentas disponíveis

### Estrutura Obrigatória do SKILL.md

```markdown
---
[YAML frontmatter]
---

# [Nome Descritivo da Skill]

## Quando Usar
[Triggers claros e específicos]

## Workflow Principal ([N] Etapas)

### Etapa 1: [Nome] 📋
[Descrição concisa]

### Etapa 2: [Nome] 🔍
[Descrição concisa + referência a REFERENCE.md se necessário]

### Etapa 3: [Nome] ✅
[Finalização]

## Exemplos de Uso
Veja [EXAMPLES.md](EXAMPLES.md) para casos completos.
[Quick example opcional]

## Output Final para o Usuário
[Template do que mostrar ao usuário]

## Troubleshooting
Veja [TROUBLESHOOTING.md](TROUBLESHOOTING.md) para guia completo.
[Erros mais comuns com solução rápida]

## Regras Importantes

### ✅ FAZER:
- **Sempre** [regra crítica 1]
- **Sempre** [regra crítica 2]

### ❌ NÃO FAZER:
- **NÃO** [anti-pattern 1]
- **NÃO** [anti-pattern 2]

## Referência Técnica
Veja [REFERENCE.md](REFERENCE.md) para documentação completa.
```

### O Que Incluir

- ✅ Workflow principal (etapas claras e numeradas)
- ✅ Quando usar (triggers específicos)
- ✅ Regras importantes (FAZER e NÃO FAZER)
- ✅ Links para outros arquivos
- ✅ Template de output final
- ✅ Emoji para organização visual (opcional)

### O Que NÃO Incluir

- ❌ Documentação técnica detalhada (→ REFERENCE.md)
- ❌ Exemplos longos (→ EXAMPLES.md)
- ❌ Lista de erros completa (→ TROUBLESHOOTING.md)
- ❌ Configurações detalhadas (→ REFERENCE.md)
- ❌ Histórico de mudanças (→ git log)
- ❌ Teoria/fundamentos extensos (→ REFERENCE.md)

---

## 📚 REFERENCE.md - Especificação Detalhada

### Propósito

Documentação técnica completa e detalhada. Carregado sob demanda quando Claude precisa de informações técnicas durante execução.

### Especificações Técnicas

**Tamanho:** Sem limite (quanto mais completo, melhor)

**Quando Claude lê:**
- Precisa de detalhes sobre framework/metodologia
- Precisa verificar configurações
- Precisa entender parâmetros/APIs
- Precisa de informações técnicas específicas

### Estrutura Recomendada

```markdown
# Referência Técnica - [Nome da Skill]

## 🎯 Framework Detalhado
[Metodologia completa, fundamentos teóricos]

## ⚙️ Configurações
[Variáveis, caminhos, APIs]

## 📝 Parâmetros
[Lista completa de opções]

## 🔌 APIs e Integrações
[Documentação de APIs/ferramentas usadas]

## 📥 Formatos de Input
[Estruturas de dados esperadas]

## 📤 Formatos de Output
[Estruturas de dados geradas]

## 🧮 Algoritmos e Lógica
[Pseudocódigo, complexidade]

## 🎨 Padrões e Convenções
[Nomenclatura, estrutura]

## 🔐 Segurança
[Considerações de segurança]

## 📊 Performance
[Benchmarks, otimizações]

## 🔗 Recursos Externos
[Links para docs oficiais]
```

### Seções Comuns

#### Framework Detalhado
- Metodologia usada (se aplicável)
- Fundamentos teóricos
- Papers/research relevantes

#### Configurações
```yaml
# Variáveis de ambiente
VARIABLE_NAME: description
ANOTHER_VAR: description

# Caminhos
/path/to/important/files/
/another/relevant/path/

# APIs
api_name:
  endpoint: https://api.example.com
  auth: Bearer Token
  docs: https://docs.example.com
```

#### Parâmetros

Para cada parâmetro:
```markdown
### [Nome do Parâmetro]

**Tipo:** string | number | boolean | array
**Obrigatório:** sim | não
**Padrão:** [valor]
**Valores possíveis:** [lista ou range]
**Descrição:** [O que faz]

**Exemplos:**
```
valor1  # [Caso de uso]
valor2  # [Outro caso]
```
```

#### APIs e Integrações

Para cada endpoint:
```markdown
#### `METHOD /endpoint`

**Request:**
```json
{
  "field1": "value",
  "field2": "value"
}
```

**Response:**
```json
{
  "result": "value"
}
```

**Erros possíveis:**
- `400` - [Descrição]
- `401` - [Descrição]
- `500` - [Descrição]
```

---

## 💡 EXAMPLES.md - Especificação Detalhada

### Propósito

Casos de uso reais e completos. Carregado sob demanda quando Claude precisa ver exemplos práticos.

### Especificações Técnicas

**Mínimo:** 2 exemplos completos
**Recomendado:** 3-5 exemplos cobrindo diferentes cenários

**Tipos de exemplos a incluir:**
- ✅ Caso simples (happy path)
- ✅ Caso complexo (múltiplas variáveis)
- ✅ Edge case (situações raras/difíceis)

**Quando Claude lê:**
- Precisa entender caso de uso concreto
- Usuário pediu algo similar a exemplo existente
- Precisa adaptar workflow para situação específica

### Estrutura de Cada Exemplo

```markdown
## Exemplo [N]: [Nome Descritivo do Caso]

### Contexto
[Situação do usuário, problema que precisa resolver]

### Input do Usuário
```
[Exatamente o que o usuário digitou]
```

### Processo de Execução

**Etapa 1: [Nome]**
- [O que aconteceu]
- [Ferramenta usada]
- [Resultado parcial]

**Etapa 2: [Nome]**
- [O que aconteceu]
- [Resultado parcial]

**Etapa 3: [Nome]**
- [Finalização]

### Output Gerado

```
[Output completo mostrado ao usuário]
```

### Arquivos Criados/Modificados (se aplicável)

```
pasta/
├── arquivo1.ext
└── arquivo2.ext
```

### Observações

- **Insight 1:** [Aprendizado deste caso]
- **Insight 2:** [Detalhe importante]
- **Variação possível:** [Como adaptar para casos similares]
- **Tempo de execução:** [Se relevante]
- **Custo:** [Se aplicável]
```

### Galeria de Inputs Comuns

Ao final do arquivo, incluir seção com variações de input:

```markdown
## Galeria de Inputs Comuns

Exemplos rápidos de variações de input que ativam a skill:

```
"[Variação 1]"
"[Variação 2]"
"[Variação 3]"
```

Todos seguem o workflow padrão.
```

---

## 🔧 TROUBLESHOOTING.md - Especificação Detalhada

### Propósito

Guia completo de erros comuns e soluções. Carregado sob demanda quando Claude encontra erro durante execução.

### Especificações Técnicas

**Mínimo:** 2 erros documentados
**Recomendado:** Documentar todos os erros já encontrados

**Quando Claude lê:**
- Encontrou erro durante execução
- Precisa debugar problema
- Usuário reportou comportamento inesperado

### Estrutura de Cada Erro

```markdown
## 🚨 Erro: [Descrição Clara do Erro]

### Sintoma

```
[Como o erro aparece - mensagem exata ou descrição do comportamento]
```

### Causa

[Por que este erro acontece - causa raiz técnica]

### Solução

**Passo a passo:**

1. [Passo 1 específico]
```bash
[Comando ou ação]
```

2. [Passo 2]
```bash
[Comando ou ação]
```

3. [Verificação]
```bash
[Como confirmar que está resolvido]
```

### Prevenção

Como evitar este erro no futuro:
- [Prática preventiva 1]
- [Prática preventiva 2]
- [Validação a fazer antes]

### Relacionado

- Veja também: [Link para erro relacionado neste arquivo]
- Documentação: [Link para seção relevante no REFERENCE.md]
```

### Seções Adicionais Importantes

#### Debugging Geral

```markdown
## 🔍 Debugging Geral

### Se Nenhuma Solução Acima Funcionou

**1. Verificar logs:**
```bash
[Como acessar logs da skill]
```

**2. Modo verbose:**
```bash
[Como executar em modo debug]
```

**3. Validar ambiente:**
```bash
# Verificar versões
python --version
[outras verificações]
```

**4. Estado limpo:**
```bash
[Como resetar para estado inicial]
```
```

#### Tabela de Frequência

```markdown
## 📊 Erros por Frequência

| Erro | Frequência | Tempo Médio de Resolução |
|------|------------|--------------------------|
| [Erro 1] | 🔴 Alta | 2min |
| [Erro 2] | 🟡 Média | 5min |
| [Erro 3] | 🟢 Baixa | 10min |
```

#### Quando Pedir Ajuda

```markdown
## 🆘 Quando Pedir Ajuda

Se após seguir todos os passos o erro persistir:

1. Coletar informações:
```bash
[Comandos para coletar info de debug]
```

2. Criar issue com:
   - Descrição do erro
   - Passos para reproduzir
   - Output dos comandos de debug
   - Ambiente (OS, Python version, etc)

3. [Link para abrir issue/contato]
```

#### Checklist de Validação

```markdown
## ✅ Checklist de Validação

Antes de relatar bug, verificar:

- [ ] Seguiu todos os passos de solução
- [ ] Verificou configurações no REFERENCE.md
- [ ] Testou com exemplo simples do EXAMPLES.md
- [ ] Ambiente está correto (dependências, versões)
- [ ] Leu REFERENCE.md para confirmar uso correto
```

---

## 📂 Pastas Opcionais

### scripts/ (Scripts Auxiliares)

**Quando incluir:** Se a skill precisa de scripts Python/Bash auxiliares.

**Estrutura:**
```
nome-da-skill/
└── scripts/
    ├── helper.py           # Script auxiliar principal
    ├── validator.py        # Validador
    ├── utils.py            # Utilidades
    └── requirements.txt    # Dependências (se necessário)
```

**Regras:**
- ✅ Documentar cada script no REFERENCE.md
- ✅ Adicionar exemplos de uso no EXAMPLES.md
- ✅ Scripts devem ter docstrings claras
- ✅ Incluir requirements.txt se tiver dependências extras
- ✅ Scripts devem ser executáveis independentemente

**Exemplo de documentação no REFERENCE.md:**

```markdown
## Scripts Auxiliares

### helper.py

**Localização:** `.claude/skills/nome-da-skill/scripts/helper.py`

**Propósito:** [O que faz]

**Uso:**
```bash
python3 .claude/skills/nome-da-skill/scripts/helper.py [args]
```

**Parâmetros:**
- `--arg1`: [Descrição]
- `--arg2`: [Descrição]

**Exemplo:**
```bash
python3 .claude/skills/nome-da-skill/scripts/helper.py --arg1 value
```
```

### templates/ (Templates de Arquivos)

**Quando incluir:** Se a skill usa templates de arquivos para gerar outputs.

**Estrutura:**
```
nome-da-skill/
└── templates/
    ├── output.md.template      # Template de output
    ├── config.yaml.template    # Template de configuração
    └── README.md               # Doc dos templates
```

**Regras:**
- ✅ Documentar cada template no REFERENCE.md
- ✅ Incluir README.md na pasta templates explicando cada template
- ✅ Usar placeholders claros (ex: `{{VARIABLE_NAME}}`)
- ✅ Adicionar exemplos de uso no EXAMPLES.md

---

## 🎯 Templates Completos Prontos para Copiar

### Template: SKILL.md

```markdown
---
name: nome-da-skill
description: [Descrição clara com triggers que ativam automaticamente a skill. Inclua verbos de ação e contextos específicos.]
allowed-tools: Read, Write, Edit, Bash  # (opcional - remover se não restringir)
---

# [Nome Descritivo da Skill]

## Quando Usar

Use esta skill automaticamente quando o usuário:
- Pedir para **[ação 1]**: "[exemplo de frase]"
- Pedir para **[ação 2]**: "[exemplo de frase]"
- Mencionar **[contexto específico]**
- Solicitar **[tipo de tarefa]**

**IMPORTANTE:** [Alguma regra crítica de comportamento - ex: executar automaticamente sem confirmação, sempre perguntar antes, etc]

---

## Workflow Principal ([N] Etapas)

### Etapa 1: [Nome da Etapa] 📋

**O que fazer:**
[Descrição clara da etapa]

**Ferramentas:**
- [Ferramenta 1]
- [Ferramenta 2]

**Output esperado:**
[O que deve resultar desta etapa]

---

### Etapa 2: [Nome da Etapa] 🔍

**O que fazer:**
[Descrição clara - para detalhes técnicos, referenciar REFERENCE.md]

Para framework completo, veja [REFERENCE.md](REFERENCE.md).

---

### Etapa 3: [Nome da Etapa] ✅

**O que fazer:**
[Descrição final]

---

## Exemplos de Uso

Veja [EXAMPLES.md](EXAMPLES.md) para casos reais completos.

**Quick example:**
```
Usuário: "[exemplo rápido]"
Claude: [resposta]
```

---

## Output Final para o Usuário

Após completar workflow, mostrar:

```
✅ [Tarefa] concluída!

[Seção 1]
[Informações relevantes]

[Seção 2]
[Mais informações]

💡 Próximo passo sugerido: [sugestão]
```

---

## Troubleshooting

Veja [TROUBLESHOOTING.md](TROUBLESHOOTING.md) para guia completo de erros.

**Erros comuns:**
- **[Erro 1]:** [Solução rápida]
- **[Erro 2]:** [Solução rápida]

---

## Regras Importantes

### ✅ FAZER:

- **Sempre** [regra crítica 1]
- **Sempre** [regra crítica 2]
- **Sempre** [regra crítica 3]

### ❌ NÃO FAZER:

- **NÃO** [anti-pattern 1]
- **NÃO** [anti-pattern 2]
- **NÃO** [anti-pattern 3]

---

## Referência Técnica

Veja [REFERENCE.md](REFERENCE.md) para:
- Framework detalhado
- Configurações completas
- Parâmetros e opções
- APIs e integrações

---

**Criado em:** [DATA]
**Framework usado:** [Se aplicável]
**Status:** ✅ [Status da skill]
```

### Template: REFERENCE.md

```markdown
# Referência Técnica - [Nome da Skill]

Este arquivo contém documentação técnica completa e detalhada.

---

## 🎯 Framework Detalhado

### Metodologia

[Explicação completa do framework/metodologia usada]

### Fundamentos Teóricos

[Base teórica, papers, referências]

---

## ⚙️ Configurações

### Variáveis de Ambiente

```bash
VARIABLE_NAME=value
ANOTHER_VAR=value
```

### Caminhos

```
/caminho/para/arquivos/importantes/
/outro/caminho/relevante/
```

### APIs Utilizadas

| API | Endpoint | Autenticação | Docs |
|-----|----------|--------------|------|
| [Nome] | `https://api.example.com` | Bearer Token | [Link] |

---

## 📝 Parâmetros

### Parâmetro 1: [Nome]

**Tipo:** string | number | boolean
**Obrigatório:** sim | não
**Padrão:** [valor]
**Descrição:** [O que faz]

**Exemplos:**
```
valor1  # [Caso de uso]
valor2  # [Outro caso]
```

### Parâmetro 2: [Nome]

[Mesmo formato...]

---

## 🔌 APIs e Integrações

### API 1: [Nome]

**Documentação:** [URL]

**Endpoints usados:**

#### `POST /endpoint`

**Request:**
```json
{
  "field1": "value",
  "field2": "value"
}
```

**Response:**
```json
{
  "result": "value"
}
```

**Erros possíveis:**
- `400` - [Descrição]
- `401` - [Descrição]
- `500` - [Descrição]

---

## 📥 Formatos de Input

### Formato 1: [Nome]

**Estrutura:**
```json
{
  "campo1": "tipo",
  "campo2": "tipo"
}
```

**Validação:**
- `campo1`: [Regras de validação]
- `campo2`: [Regras de validação]

---

## 📤 Formatos de Output

### Output Padrão

**Estrutura:**
```
[Formato do output]
```

### Output Alternativo

[Se houver variações]

---

## 🧮 Algoritmos e Lógica

### Algoritmo Principal

**Pseudocódigo:**
```
INICIO
  [Passo 1]
  PARA cada [item]:
    [Passo 2]
  FIM PARA
  [Passo 3]
FIM
```

**Complexidade:** O(n) | O(n²) | etc

---

## 🎨 Padrões e Convenções

### Nomenclatura

[Regras de nomes de arquivos, variáveis, etc]

### Estrutura de Dados

[Padrões de estrutura]

---

## 🔐 Segurança

### Considerações

- [Ponto de segurança 1]
- [Ponto de segurança 2]

### Boas Práticas

- [Prática 1]
- [Prática 2]

---

## 📊 Performance

### Benchmarks

| Operação | Tempo | Memória |
|----------|-------|---------|
| [Op 1] | [tempo] | [mem] |
| [Op 2] | [tempo] | [mem] |

### Otimizações

- [Dica 1]
- [Dica 2]

---

## 🔗 Recursos Externos

- [Documentação oficial]: URL
- [Tutorial]: URL
- [Paper/Research]: URL

---

**Última atualização:** [DATA]
**Versão:** [X.Y]
```

### Template: EXAMPLES.md

```markdown
# Exemplos - [Nome da Skill]

Este arquivo contém casos de uso reais e completos.

---

## Exemplo 1: [Nome Descritivo do Caso]

### Contexto

[Situação do usuário, problema que precisa resolver]

### Input do Usuário

```
[Exatamente o que o usuário digitou]
```

### Processo de Execução

**Etapa 1: [Nome]**
- [O que aconteceu]
- [Ferramenta usada]

**Etapa 2: [Nome]**
- [O que aconteceu]
- [Resultado parcial]

**Etapa 3: [Nome]**
- [Finalização]

### Output Gerado

```
[Output completo mostrado ao usuário]
```

### Arquivos Criados/Modificados

```
pasta/
├── arquivo1.ext
└── arquivo2.ext
```

### Observações

- **Insight 1:** [Aprendizado deste caso]
- **Insight 2:** [Detalhe importante]
- **Variação possível:** [Como adaptar para casos similares]

---

## Exemplo 2: [Caso Mais Complexo]

### Contexto

[Cenário mais complexo com múltiplas variáveis]

### Input do Usuário

```
[Input completo]
```

### Processo de Execução

[Mesmo formato do Exemplo 1, mas mais detalhado]

### Output Gerado

```
[Output]
```

### Desafios Encontrados

- **Desafio 1:** [Problema encontrado]
  - **Solução:** [Como foi resolvido]

### Observações

[Insights específicos deste caso complexo]

---

## Exemplo 3: Edge Case - [Caso Especial]

### Contexto

[Situação rara ou difícil]

### Por Que É Especial

[O que torna este caso um edge case]

### Input do Usuário

```
[Input]
```

### Adaptações Necessárias

- [Adaptação 1]
- [Adaptação 2]

### Output Gerado

```
[Output]
```

### Lições Aprendidas

[Como este caso melhorou a skill]

---

## Exemplo 4: [Outro Caso Real]

[Adicionar quantos exemplos forem relevantes]

---

## Galeria de Inputs Comuns

Exemplos rápidos de variações de input:

```
"[Variação 1]"
"[Variação 2]"
"[Variação 3]"
```

Todos ativam a skill e seguem o workflow padrão.

---

**Total de exemplos:** [N]
**Casos cobertos:** [Categorias de casos]
**Última atualização:** [DATA]
```

### Template: TROUBLESHOOTING.md

```markdown
# Troubleshooting - [Nome da Skill]

Guia completo para resolver erros comuns.

---

## 🚨 Erro: [Descrição Clara do Erro]

### Sintoma

```
[Como o erro aparece - mensagem exata ou descrição do comportamento]
```

### Causa

[Por que este erro acontece - causa raiz]

### Solução

**Passo a passo:**

1. [Passo 1 específico]
```bash
[Comando ou ação]
```

2. [Passo 2]
```bash
[Comando ou ação]
```

3. [Verificação]
```bash
[Como confirmar que está resolvido]
```

### Prevenção

Como evitar este erro no futuro:
- [Prática preventiva 1]
- [Prática preventiva 2]

### Relacionado

- Veja também: [Link para erro relacionado neste arquivo]

---

## 🚨 Erro: [Outro Erro Comum]

### Sintoma

```
[Descrição do erro]
```

### Causa

[Causa raiz]

### Solução Rápida

```bash
[Comando rápido para resolver]
```

### Solução Completa

[Se solução rápida não funcionar]

1. [Passo 1]
2. [Passo 2]

---

## 🚨 Erro: [Erro de Configuração]

### Sintoma

[Descrição]

### Causa

[Geralmente relacionado a...]

### Solução

Verificar configurações:

```bash
# Verificar variável X
echo $VARIABLE_NAME

# Corrigir se necessário
export VARIABLE_NAME=correct_value
```

---

## 🚨 Erro: [Erro de Dependência]

### Sintoma

```
ModuleNotFoundError: No module named 'xyz'
```

### Causa

Dependência não instalada

### Solução

```bash
pip install xyz
# ou
pip install -r requirements.txt
```

---

## 🚨 Erro: [Erro de Permissão]

### Sintoma

```
Permission denied: /path/to/file
```

### Solução

```bash
chmod +x /path/to/file
# ou
sudo chown user:group /path/to/file
```

---

## 🔍 Debugging Geral

### Se Nenhuma Solução Acima Funcionou

**1. Verificar logs:**
```bash
[Como acessar logs da skill]
```

**2. Modo verbose:**
```bash
[Como executar em modo debug]
```

**3. Validar ambiente:**
```bash
# Verificar versões
python --version
[outras verificações]
```

**4. Estado limpo:**
```bash
[Como resetar para estado inicial]
```

---

## 📊 Erros por Frequência

| Erro | Frequência | Tempo Médio de Resolução |
|------|------------|--------------------------|
| [Erro 1] | 🔴 Alta | 2min |
| [Erro 2] | 🟡 Média | 5min |
| [Erro 3] | 🟢 Baixa | 10min |

---

## 🆘 Quando Pedir Ajuda

Se após seguir todos os passos o erro persistir:

1. Coletar informações:
```bash
[Comandos para coletar info de debug]
```

2. Criar issue com:
   - Descrição do erro
   - Passos para reproduzir
   - Output dos comandos de debug
   - Ambiente (OS, Python version, etc)

3. [Link para abrir issue/contato]

---

## ✅ Checklist de Validação

Antes de relatar bug, verificar:

- [ ] Seguiu todos os passos de solução
- [ ] Verificou configurações
- [ ] Testou com exemplo simples do EXAMPLES.md
- [ ] Ambiente está correto (dependências, versões)
- [ ] Leu REFERENCE.md para confirmar uso correto

---

**Total de erros documentados:** [N]
**Última atualização:** [DATA]
**Contribuições:** [Como adicionar novos erros neste doc]
```

---

## ✅ Checklist de Validação Completo

### Antes de Considerar a Skill Completa

#### Estrutura
- [ ] Pasta criada em `.claude/skills/nome-da-skill/`
- [ ] SKILL.md existe e tem frontmatter YAML válido
- [ ] REFERENCE.md existe e está completo
- [ ] EXAMPLES.md existe com mínimo 2 exemplos
- [ ] TROUBLESHOOTING.md existe com mínimo 2 erros

#### Qualidade SKILL.md
- [ ] Tem entre 30-60 linhas (máximo 80)
- [ ] Frontmatter YAML está correto
- [ ] Campo `name` em lowercase com hífens
- [ ] Campo `description` tem triggers claros
- [ ] Referencia outros arquivos com links markdown corretos
- [ ] Workflow está claro e numerado
- [ ] Tem seção "Quando Usar" com triggers específicos
- [ ] Tem seção "Regras Importantes" (FAZER e NÃO FAZER)
- [ ] Tem template de output final

#### Qualidade REFERENCE.md
- [ ] Contém toda documentação técnica necessária
- [ ] Framework/metodologia está detalhado
- [ ] Configurações estão documentadas
- [ ] Parâmetros estão listados completamente
- [ ] APIs/integrações estão documentadas
- [ ] Formatos de input/output estão especificados

#### Qualidade EXAMPLES.md
- [ ] Tem mínimo 2 exemplos completos
- [ ] Cada exemplo tem: Contexto, Input, Processo, Output, Observações
- [ ] Cobre caso simples (happy path)
- [ ] Cobre caso complexo ou edge case
- [ ] Exemplos são concretos (não genéricos)
- [ ] Tem "Galeria de Inputs Comuns" ao final

#### Qualidade TROUBLESHOOTING.md
- [ ] Tem mínimo 2 erros documentados
- [ ] Cada erro tem: Sintoma, Causa, Solução, Prevenção
- [ ] Tem seção "Debugging Geral"
- [ ] Tem "Checklist de Validação"
- [ ] Soluções são específicas e acionáveis

#### Links e Referências
- [ ] Todos os links markdown funcionam
- [ ] Links entre arquivos usam paths corretos
- [ ] Case-sensitive correto (SKILL.md, não skill.md)
- [ ] Referências cruzadas fazem sentido

#### Integração
- [ ] Entry adicionada no CLAUDE.md (seção Skills)
- [ ] Commit criado com mensagem `feat: adicionar skill nome-da-skill`
- [ ] Testado manualmente (trigger funciona?)
- [ ] Scripts auxiliares (se houver) estão documentados
- [ ] Templates (se houver) estão documentados

---

## 🚫 Anti-Padrões (Evitar)

### ❌ 1. Arquivo único gigante

```
nome-da-skill/
└── SKILL.md (200+ linhas)  # ERRADO!
```

**Por quê:** Carrega tudo sempre, desperdiça tokens, dificulta manutenção.

**Correto:** Dividir em 4 arquivos (Progressive Disclosure).

---

### ❌ 2. SKILL.md com documentação técnica

```markdown
# Skill

## Workflow
[30 linhas de workflow...]

## API Documentation
[50 linhas de docs da API...]  # ERRADO!

## Configurações Detalhadas
[40 linhas de configs...]  # ERRADO!
```

**Por quê:** SKILL.md deve ser focado e limpo (30-60 linhas).

**Correto:** Mover docs técnicas para REFERENCE.md.

---

### ❌ 3. Sem exemplos

```
nome-da-skill/
├── SKILL.md
├── REFERENCE.md
└── TROUBLESHOOTING.md
# Falta EXAMPLES.md!  # ERRADO!
```

**Por quê:** Claude precisa de exemplos concretos para entender casos de uso.

**Correto:** Sempre incluir EXAMPLES.md com mínimo 2 exemplos.

---

### ❌ 4. Referências quebradas

```markdown
Veja [REFERENCE.md](reference.md)  # ERRADO! Case errado
Veja [EXAMPLES.md](examples)       # ERRADO! Falta extensão
Veja [Link](./SKILL.md)            # ERRADO! Path relativo desnecessário
```

**Correto:**
```markdown
Veja [REFERENCE.md](REFERENCE.md)  # Correto!
Veja [EXAMPLES.md](EXAMPLES.md)    # Correto!
```

---

### ❌ 5. Triggers vagos na description

```yaml
description: Uma skill útil para fazer coisas  # ERRADO! Muito vago
```

**Por quê:** Claude não saberá quando ativar automaticamente.

**Correto:**
```yaml
description: Use quando usuário pedir para validar APIs REST, testar endpoints, ou verificar responses HTTP. Automaticamente ativa ao mencionar "validar API", "testar endpoint", ou "check API".
```

---

### ❌ 6. SKILL.md muito longo

```markdown
---
name: minha-skill
---

# Minha Skill

[100 linhas de conteúdo...]  # ERRADO! Máximo é 80
```

**Por quê:** Progressive Disclosure perde propósito se SKILL.md for grande demais.

**Correto:** Manter entre 30-60 linhas (máximo absoluto: 80).

---

### ❌ 7. Exemplos genéricos

```markdown
## Exemplo 1: Usar a Skill

Usuário pediu para usar a skill.
Claude usou a skill.
Funcionou.
```

**Por quê:** Não ajuda Claude a entender casos reais.

**Correto:** Exemplos concretos com input/output completos.

---

### ❌ 8. Falta de prevenção nos erros

```markdown
## Erro: API falhou

### Sintoma
Erro 500

### Solução
Tentar novamente
```

**Por quê:** Não ensina como evitar o erro.

**Correto:** Incluir seção "Prevenção" em cada erro.

---

## 🎓 Boas Práticas

### 1. Mantenha SKILL.md Limpo

- ✅ Apenas workflow principal
- ✅ Triggers claros
- ✅ Links para outros arquivos
- ❌ Sem documentação técnica
- ❌ Sem exemplos longos

### 2. Use Links Markdown Corretos

```markdown
Correto: [REFERENCE.md](REFERENCE.md)
Correto: [EXAMPLES.md](EXAMPLES.md)
Correto: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
```

### 3. Seja Específico nos Triggers

```yaml
# Vago (evitar):
description: Skill para APIs

# Específico (preferir):
description: Use quando usuário pedir para validar APIs REST, testar endpoints HTTP, ou verificar responses. Ativa automaticamente com "validar API", "testar endpoint", "check API response".
```

### 4. Documente Erros Reais

- ✅ Erros que você já viu acontecer
- ✅ Mensagens de erro exatas
- ✅ Soluções testadas
- ❌ Não invente erros hipotéticos

### 5. Exemplos Concretos

- ✅ Input real do usuário
- ✅ Output completo gerado
- ✅ Arquivos criados (se aplicável)
- ✅ Observações com insights
- ❌ Não usar "exemplo genérico"

### 6. Atualize Continuamente

- Adicione novos exemplos conforme surgem
- Documente novos erros encontrados
- Melhore documentação técnica
- Use git para rastrear mudanças

### 7. Teste Antes de Commitar

- [ ] Trigger funciona?
- [ ] Links não estão quebrados?
- [ ] Tamanho do SKILL.md está OK?
- [ ] Exemplos fazem sentido?

---

## 📊 Referências

### Documentação Oficial

- **Claude Code Skills:** https://docs.claude.com/en/docs/claude-code/skills.md
- **Progressive Disclosure:** Padrão de design UX/UI aplicado a LLMs

### Baseado Em

- Refactoring da skill `estudar-video` (226 linhas → 4 arquivos)
- Best practices de documentação técnica
- Feedback de uso real das skills existentes

---

**Última atualização:** 02/11/2025
**Versão:** 2.0
**Padrão:** Progressive Disclosure (obrigatório)
