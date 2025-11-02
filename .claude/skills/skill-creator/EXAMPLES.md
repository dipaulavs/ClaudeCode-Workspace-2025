# Exemplos - Skill Creator

Este arquivo contém casos reais completos de criação de Skills usando Progressive Disclosure.

---

## Exemplo 1: API Validator (Skill Simples)

### Contexto

Usuário quer criar uma skill que valide APIs REST automaticamente - verificar endpoints, responses, status codes, e documentar problemas.

### Input do Usuário

```
Usuário: "Crie uma skill para validar APIs REST"
```

### Processo de Execução

**Etapa 1: Coletar Informações**

Claude pergunta:
- Nome da skill: `api-validator`
- Descrição: "Use quando usuário pedir para validar APIs REST, testar endpoints, ou verificar responses HTTP"
- Quando usar: Ao mencionar "validar API", "testar endpoint", "check API"
- Ferramentas: Read, Write, Bash (para curl)
- Scripts auxiliares: Sim (validator.py)

**Etapa 2: Gerar Estrutura**

```
.claude/skills/api-validator/
├── SKILL.md
├── REFERENCE.md
├── EXAMPLES.md
├── TROUBLESHOOTING.md
└── scripts/
    └── validator.py
```

**Etapa 3: Criar Arquivos**

SKILL.md (45 linhas):
```yaml
---
name: api-validator
description: Use quando usuário pedir para validar APIs REST, testar endpoints, ou verificar responses HTTP. Ativa automaticamente com "validar API", "testar endpoint", "check API response".
allowed-tools: Read, Write, Bash
---

# API Validator

## Quando Usar
- Pedir para validar API REST
- Testar endpoints HTTP/HTTPS
- Verificar status codes e responses

## Workflow Principal (3 Etapas)

### Etapa 1: Análise do Endpoint
- Ler documentação ou specs fornecidas
- Identificar endpoints a testar
- Preparar requests

### Etapa 2: Validação
- Executar requests com curl
- Verificar status codes
- Validar response structure
Veja [REFERENCE.md](REFERENCE.md) para specs completas.

### Etapa 3: Relatório
- Gerar relatório com resultados
- Documentar erros encontrados
- Sugerir correções

## Exemplos
Veja [EXAMPLES.md](EXAMPLES.md) para casos completos.

## Regras Importantes
✅ FAZER:
- Sempre testar todos os métodos HTTP
- Sempre documentar erros
❌ NÃO FAZER:
- NÃO testar em produção sem permissão
```

REFERENCE.md (detalhado):
- HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Status codes (200, 201, 400, 401, 404, 500)
- Headers comuns
- Estrutura de responses
- Validação de schemas JSON

EXAMPLES.md (3 exemplos):
1. Validar API pública simples
2. Validar API com autenticação
3. Validar múltiplos endpoints

TROUBLESHOOTING.md (erros comuns):
1. Timeout
2. CORS errors
3. Authentication failures
4. Schema mismatches

scripts/validator.py:
```python
#!/usr/bin/env python3
"""API Validator - Valida endpoints REST"""

import requests
import json
import sys

def validate_endpoint(url, method="GET", headers=None):
    # Implementação...
```

**Etapa 4: Documentar e Commitar**

1. Atualizar CLAUDE.md:
```markdown
| **api-validator** | Valida APIs REST, testa endpoints, verifica responses | `.claude/skills/api-validator/` |
```

2. Commit:
```bash
git add .claude/skills/api-validator/
git commit -m "feat: adicionar skill api-validator"
```

### Output Gerado

```
✅ Skill criada com Progressive Disclosure!

📂 Estrutura:
  .claude/skills/api-validator/
  ├── SKILL.md (45 linhas)
  ├── REFERENCE.md (120 linhas - HTTP specs completas)
  ├── EXAMPLES.md (3 exemplos)
  ├── TROUBLESHOOTING.md (4 erros)
  └── scripts/
      └── validator.py

🎯 Como usar: "Valide esta API: https://api.example.com"
📝 Claude carrega SKILL.md sempre, outros sob demanda
💾 Committed: feat: adicionar skill api-validator

💡 Teste agora: "Valide a API do GitHub: https://api.github.com"
```

### Arquivos Criados/Modificados

```
.claude/skills/api-validator/
├── SKILL.md (45 linhas)
├── REFERENCE.md (120 linhas)
├── EXAMPLES.md (3 exemplos)
├── TROUBLESHOOTING.md (4 erros)
└── scripts/
    └── validator.py (80 linhas)

CLAUDE.md (atualizado - seção Skills)
```

### Observações

- **Insight 1:** Skill simples só precisa de 1 script auxiliar
- **Insight 2:** SKILL.md ficou em 45 linhas (ideal!)
- **Insight 3:** REFERENCE.md tem specs HTTP completas (não precisa estar no SKILL.md)
- **Tempo total:** ~5 minutos para criar tudo
- **Variação possível:** Pode adicionar suporte para GraphQL depois

---

## Exemplo 2: Code Analyzer (Skill Complexa com Múltiplos Scripts)

### Contexto

Usuário quer skill que analise qualidade de código Python - verifica PEP8, complexidade ciclomática, docstrings, type hints, testes, security issues, e gera relatório detalhado.

### Input do Usuário

```
Usuário: "Crie uma skill para analisar qualidade de código Python - quero checagem de PEP8, complexidade, docstrings, type hints, cobertura de testes, e security issues"
```

### Processo de Execução

**Etapa 1: Coletar Informações**

Claude identifica que é caso complexo e pergunta:
- Nome: `code-analyzer`
- Descrição: "Use quando usuário pedir para analisar qualidade de código Python, verificar PEP8, checar complexidade, validar documentação, ou auditar segurança"
- Ferramentas: Read, Write, Edit, Bash, Grep, Glob
- Scripts auxiliares: Sim (múltiplos: pep8_checker.py, complexity_analyzer.py, docs_validator.py, security_scanner.py, report_generator.py)
- Templates: Sim (report template)

**Etapa 2: Gerar Estrutura Complexa**

```
.claude/skills/code-analyzer/
├── SKILL.md
├── REFERENCE.md
├── EXAMPLES.md
├── TROUBLESHOOTING.md
├── scripts/
│   ├── pep8_checker.py
│   ├── complexity_analyzer.py
│   ├── docs_validator.py
│   ├── security_scanner.py
│   ├── report_generator.py
│   ├── utils.py
│   └── requirements.txt
└── templates/
    ├── report.md.template
    └── README.md
```

**Etapa 3: Criar Arquivos Principais**

SKILL.md (60 linhas - mais complexo, mas ainda focado):
```yaml
---
name: code-analyzer
description: Use quando usuário pedir para analisar qualidade de código Python, verificar PEP8, checar complexidade ciclomática, validar documentação, auditar segurança, ou gerar relatório de qualidade. Ativa com "analisar código", "check code quality", "audit Python code".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Code Analyzer - Análise de Qualidade Python

## Quando Usar
- Analisar qualidade de código Python
- Verificar PEP8 compliance
- Checar complexidade ciclomática
- Validar docstrings e type hints
- Auditar security issues
- Gerar relatório de qualidade

## Workflow Principal (5 Etapas)

### Etapa 1: Scan do Projeto 🔍
- Usar Glob para encontrar arquivos .py
- Identificar estrutura do projeto
- Listar módulos a analisar

### Etapa 2: Análise Estática 📊
- PEP8: Executar scripts/pep8_checker.py
- Complexidade: Executar scripts/complexity_analyzer.py
- Docs: Executar scripts/docs_validator.py
Veja [REFERENCE.md](REFERENCE.md) para métricas detalhadas.

### Etapa 3: Análise de Segurança 🔐
- Security: Executar scripts/security_scanner.py
- Verificar imports perigosos
- Checar SQL injection risks

### Etapa 4: Geração de Relatório 📝
- Compilar resultados
- Usar template em templates/report.md.template
- Executar scripts/report_generator.py

### Etapa 5: Recomendações ✅
- Priorizar issues (critical, high, medium, low)
- Sugerir refactorings
- Mostrar quick wins

## Exemplos
Veja [EXAMPLES.md](EXAMPLES.md) para 3 casos: projeto simples, projeto Django, e projeto com issues críticos.

## Troubleshooting
Veja [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

**Erros comuns:**
- Dependências faltando → pip install -r scripts/requirements.txt
- Timeout em projetos grandes → usar --exclude-dirs

## Regras Importantes
✅ SEMPRE:
- Executar em ordem: PEP8 → Complexity → Docs → Security
- Gerar relatório completo
- Priorizar issues

❌ NUNCA:
- Modificar código automaticamente sem permissão
- Rodar em código de produção sem backup
```

REFERENCE.md (200+ linhas - muito detalhado):
- Métricas PEP8 (todas as regras)
- Complexidade ciclomática (thresholds: <10 OK, 10-20 Warning, >20 Crítico)
- Docstrings formats (Google, NumPy, Sphinx)
- Type hints rules
- Security patterns (SQL injection, XSS, hardcoded secrets, etc)
- Benchmarks de performance
- Configurações de cada script

EXAMPLES.md (4 exemplos extensos):
1. Projeto simples (1 arquivo)
2. Projeto Django completo
3. Projeto com issues críticos de segurança
4. Edge case: projeto sem testes

TROUBLESHOOTING.md (8 erros):
1. Dependências faltando
2. Timeout em projetos grandes
3. False positives em PEP8
4. Encoding errors
5. Memory issues
6. Conflito de versões Python
7. Scripts não executáveis
8. Template não encontrado

scripts/requirements.txt:
```
pylint==3.0.0
flake8==6.1.0
radon==6.0.1
bandit==1.7.5
mypy==1.7.0
```

templates/report.md.template:
```markdown
# Code Quality Report - {{PROJECT_NAME}}

**Data:** {{DATE}}
**Analisado por:** Claude Code (skill: code-analyzer)

---

## Resumo Executivo
- **Score geral:** {{OVERALL_SCORE}}/100
- **Issues críticos:** {{CRITICAL_COUNT}}
- **Issues altos:** {{HIGH_COUNT}}
...
```

**Etapa 4: Criar Scripts Auxiliares**

Cada script (pep8_checker.py, complexity_analyzer.py, etc) criado com:
- Docstrings completas
- Type hints
- CLI arguments
- Error handling
- Output em JSON para report_generator.py consumir

**Etapa 5: Documentar e Commitar**

### Output Gerado

```
✅ Skill complexa criada com Progressive Disclosure!

📂 Estrutura:
  .claude/skills/code-analyzer/
  ├── SKILL.md (60 linhas)
  ├── REFERENCE.md (220 linhas - métricas completas)
  ├── EXAMPLES.md (4 exemplos)
  ├── TROUBLESHOOTING.md (8 erros)
  ├── scripts/ (5 scripts + utils + requirements)
  │   ├── pep8_checker.py (120 linhas)
  │   ├── complexity_analyzer.py (150 linhas)
  │   ├── docs_validator.py (100 linhas)
  │   ├── security_scanner.py (180 linhas)
  │   ├── report_generator.py (90 linhas)
  │   ├── utils.py (60 linhas)
  │   └── requirements.txt
  └── templates/
      ├── report.md.template
      └── README.md

🎯 Como usar: "Analise a qualidade do código em src/"
📝 Scripts documentados no REFERENCE.md
💾 Committed: feat: adicionar skill code-analyzer

💡 Instalar dependências:
  cd .claude/skills/code-analyzer/scripts/
  pip install -r requirements.txt

💡 Teste agora: "Analise o código do meu projeto Python"
```

### Arquivos Criados/Modificados

```
.claude/skills/code-analyzer/
├── SKILL.md (60 linhas)
├── REFERENCE.md (220 linhas)
├── EXAMPLES.md (4 exemplos, 180 linhas)
├── TROUBLESHOOTING.md (8 erros, 150 linhas)
├── scripts/ (700+ linhas total)
└── templates/ (2 arquivos)

CLAUDE.md (atualizado)
```

### Desafios Encontrados

- **Desafio 1:** SKILL.md estava ficando com 90 linhas (muito!)
  - **Solução:** Mover descrição de métricas para REFERENCE.md, deixar só workflow em SKILL.md (reduziu para 60 linhas)

- **Desafio 2:** 5 scripts diferentes, como organizar?
  - **Solução:** Criar utils.py com código comum, documentar ordem de execução no REFERENCE.md

- **Desafio 3:** Template muito específico, como manter flexível?
  - **Solução:** Usar placeholders {{VARIABLE}} e documentar todos no REFERENCE.md

### Observações

- **Insight 1:** Skills complexas se beneficiam MUITO de Progressive Disclosure
  - Sem: 400+ linhas em arquivo único
  - Com: SKILL.md de 60 linhas + detalhes sob demanda
- **Insight 2:** Scripts auxiliares precisam de requirements.txt próprio
- **Insight 3:** Templates são poderosos para outputs consistentes
- **Insight 4:** TROUBLESHOOTING.md é crítico em skills complexas (8 erros documentados salvam tempo depois)
- **Tempo total:** ~25 minutos (skill complexa com 5 scripts)
- **Variação possível:** Adicionar suporte para JavaScript/TypeScript depois

---

## Exemplo 3: Database Schema Validator (Edge Case - Múltiplos Formatos)

### Contexto

Usuário quer skill que valide schemas de databases - suporte para PostgreSQL, MySQL, MongoDB, e SQLite. Deve verificar constraints, indexes, relationships, e detectar problemas de performance.

### Input do Usuário

```
Usuário: "Quero uma skill que valide schemas de banco de dados - PostgreSQL, MySQL, MongoDB e SQLite. Precisa checar constraints, indexes, relationships, e dar sugestões de performance"
```

### Por Que É Especial

Edge case porque:
1. Múltiplos formatos de input (SQL, JSON schema, DDL statements)
2. Múltiplos dialetos (PostgreSQL != MySQL != MongoDB)
3. Precisa de validação cross-database
4. Performance analysis é complexo

### Processo de Execução

**Etapa 1: Coletar Informações (Detalhado)**

Claude identifica complexidade e pergunta:
- Nome: `db-schema-validator`
- Descrição: "Use quando usuário pedir para validar schema de banco de dados, verificar constraints, analisar indexes, ou otimizar performance. Suporta PostgreSQL, MySQL, MongoDB, SQLite."
- Ferramentas: Read, Write, Bash (para conexão DB), Grep (para buscar schemas)
- Scripts: Múltiplos por tipo de DB
- Pergunta adicional: "Precisa conectar em DBs reais ou apenas validar schemas em arquivos?"
  - Resposta: "Ambos - arquivos .sql E conexão real"

**Etapa 2: Gerar Estrutura Adaptada**

```
.claude/skills/db-schema-validator/
├── SKILL.md
├── REFERENCE.md
├── EXAMPLES.md
├── TROUBLESHOOTING.md
├── scripts/
│   ├── validators/
│   │   ├── postgresql_validator.py
│   │   ├── mysql_validator.py
│   │   ├── mongodb_validator.py
│   │   └── sqlite_validator.py
│   ├── analyzers/
│   │   ├── index_analyzer.py
│   │   ├── relationship_checker.py
│   │   └── performance_auditor.py
│   ├── parsers/
│   │   ├── sql_parser.py
│   │   └── json_schema_parser.py
│   ├── main.py
│   ├── config.yaml
│   └── requirements.txt
└── templates/
    ├── postgresql_report.md.template
    ├── mysql_report.md.template
    ├── mongodb_report.md.template
    └── sqlite_report.md.template
```

**Etapa 3: Criar SKILL.md Focado em Workflow Multi-Formato**

SKILL.md (65 linhas):
```yaml
---
name: db-schema-validator
description: Use quando usuário pedir para validar schema de banco de dados, verificar constraints, analisar indexes, checar relationships, ou otimizar performance. Suporta PostgreSQL, MySQL, MongoDB, SQLite. Ativa com "validar schema", "check database", "analyze DB schema".
allowed-tools: Read, Write, Bash, Grep
---

# Database Schema Validator

## Quando Usar
- Validar schemas de bancos de dados
- Verificar constraints (PK, FK, UNIQUE, CHECK)
- Analisar indexes (performance)
- Checar relationships e integridade
- Detectar anti-patterns

**Suportado:** PostgreSQL, MySQL, MongoDB, SQLite

## Workflow Principal (4 Etapas)

### Etapa 1: Detectar Formato 🔍
- Identificar tipo de DB (auto-detect ou pergunta usuário)
- Determinar se é arquivo ou conexão real
- Selecionar validator apropriado

### Etapa 2: Parse do Schema 📊
- SQL: Usar scripts/parsers/sql_parser.py
- JSON: Usar scripts/parsers/json_schema_parser.py
- Extrair: tables, columns, constraints, indexes

### Etapa 3: Validação Multi-Layer 🔐
- Layer 1: Syntax validation (parser)
- Layer 2: Constraint validation (validator específico)
- Layer 3: Performance analysis (analyzers/)
Veja [REFERENCE.md](REFERENCE.md) para rules completas.

### Etapa 4: Relatório Customizado 📝
- Usar template específico do DB
- Priorizar issues (P0, P1, P2, P3)
- Gerar sugestões de otimização

## Exemplos
Veja [EXAMPLES.md](EXAMPLES.md) para 5 casos:
1. PostgreSQL arquivo .sql
2. MySQL conexão real
3. MongoDB JSON schema
4. SQLite embedded
5. Cross-database comparison

## Adaptações por DB
- **PostgreSQL:** Suporta arrays, JSONB, custom types
- **MySQL:** Diferentes engines (InnoDB, MyISAM)
- **MongoDB:** Schema-less validation, embedded docs
- **SQLite:** Limitações de constraints
Ver detalhes em [REFERENCE.md](REFERENCE.md).

## Troubleshooting
Veja [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

**Erros comuns por DB:**
- PostgreSQL: Role permissions
- MySQL: Charset issues
- MongoDB: Connection string format
- SQLite: File locks

## Regras Importantes
✅ SEMPRE:
- Auto-detectar tipo de DB quando possível
- Validar em 3 layers (syntax → constraints → performance)
- Adaptar relatório ao formato do DB
❌ NUNCA:
- Aplicar rules de PostgreSQL em MySQL
- Conectar em produção sem permissão explícita
```

**Etapa 4: REFERENCE.md com Specs de Cada DB (Massivo)**

REFERENCE.md (~400 linhas):
- PostgreSQL specs (constraints, indexes, types, extensions)
- MySQL specs (engines, storage, collations)
- MongoDB specs (validation rules, indexes, sharding)
- SQLite specs (limitations, pragmas, WAL mode)
- Performance benchmarks por DB
- Anti-patterns comuns
- Connection strings formats
- Parser algorithms

**Etapa 5: EXAMPLES.md com Casos de Cada DB**

5 exemplos extensos:
1. PostgreSQL: Validar schema de e-commerce (FK, indexes, partitions)
2. MySQL: Analisar performance de queries (ENGINE, INDEX usage)
3. MongoDB: Validar schema de analytics (embedded vs referenced)
4. SQLite: Validar schema de app mobile (size optimization)
5. Cross-DB: Migrar de MySQL para PostgreSQL (compatibility check)

**Etapa 6: TROUBLESHOOTING.md Específico por DB**

10+ erros documentados:
- Erros de conexão (cada DB)
- Parser failures (dialetos SQL)
- Missing privileges
- Charset/encoding issues
- Version compatibility
- File format errors

### Output Gerado

```
✅ Skill multi-formato criada com Progressive Disclosure!

📂 Estrutura:
  .claude/skills/db-schema-validator/
  ├── SKILL.md (65 linhas)
  ├── REFERENCE.md (400+ linhas - specs de 4 DBs)
  ├── EXAMPLES.md (5 exemplos, cada um com DB diferente)
  ├── TROUBLESHOOTING.md (10+ erros)
  ├── scripts/
  │   ├── validators/ (4 scripts)
  │   ├── analyzers/ (3 scripts)
  │   ├── parsers/ (2 scripts)
  │   ├── main.py
  │   ├── config.yaml
  │   └── requirements.txt
  └── templates/ (4 templates)

🎯 Como usar: "Valide o schema em database.sql"
🔀 Multi-formato: Auto-detecta PostgreSQL/MySQL/MongoDB/SQLite
📝 Specs completas no REFERENCE.md
💾 Committed: feat: adicionar skill db-schema-validator

💡 Instalar dependências:
  cd .claude/skills/db-schema-validator/scripts/
  pip install -r requirements.txt

💡 Teste: "Valide este schema PostgreSQL: [cola arquivo]"
```

### Lições Aprendidas

**1. Progressive Disclosure é ESSENCIAL para multi-formato:**
- SKILL.md: Workflow geral (65 linhas)
- REFERENCE.md: Specs de cada DB (400 linhas - carregado só quando precisa)
- Sem PD: Seria 500+ linhas em arquivo único!

**2. Auto-detection é poderosa:**
- Claude detecta tipo de DB automaticamente
- Usuário não precisa especificar
- Fallback: perguntar se não detectar

**3. Templates customizados por formato:**
- Cada DB tem template próprio
- Relatórios adaptados ao contexto
- Mesmo workflow, outputs diferentes

**4. TROUBLESHOOTING.md organizado por DB:**
- Fácil encontrar erro específico
- Links cruzados entre erros relacionados

**5. Scripts organizados por função:**
- validators/ - Um por DB
- analyzers/ - Compartilhados
- parsers/ - Por formato de input
- Boa separação de concerns

---

## Galeria de Inputs Comuns

### Para api-validator:
```
"Valide esta API: https://api.example.com"
"Teste os endpoints da minha API REST"
"Check API response do GitHub"
"Validar documentação da API"
```

### Para code-analyzer:
```
"Analise a qualidade do código Python"
"Check code quality no projeto src/"
"Audite segurança do código"
"Verifique PEP8 compliance"
"Gere relatório de qualidade"
```

### Para db-schema-validator:
```
"Valide o schema database.sql"
"Analise o banco PostgreSQL"
"Check schema MongoDB"
"Otimize indexes do MySQL"
"Compare schemas PostgreSQL vs MySQL"
```

Todos ativam as skills automaticamente!

---

## Comparação: Skill Simples vs Complexa

| Aspecto | API Validator (Simples) | Code Analyzer (Complexa) | DB Schema (Multi-Formato) |
|---------|-------------------------|--------------------------|---------------------------|
| **SKILL.md** | 45 linhas | 60 linhas | 65 linhas |
| **REFERENCE.md** | 120 linhas | 220 linhas | 400+ linhas |
| **Scripts** | 1 script | 5 scripts + utils | 9 scripts (organizado em pastas) |
| **Templates** | Nenhum | 1 template | 4 templates (um por DB) |
| **Exemplos** | 3 exemplos | 4 exemplos | 5 exemplos (um por formato) |
| **Erros documentados** | 4 erros | 8 erros | 10+ erros (organizado por DB) |
| **Tempo criação** | ~5 min | ~25 min | ~35 min |
| **Manutenção** | Fácil | Média | Complexa (mas bem organizada) |

**Insight:** Progressive Disclosure escala bem! Mesmo skill com 400 linhas de REFERENCE.md mantém SKILL.md limpo (65 linhas).

---

**Total de exemplos:** 3
**Casos cobertos:** Skill simples, complexa, e edge case multi-formato
**Última atualização:** 02/11/2025
