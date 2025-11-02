# Templates de Arquivos - Claude Skills

Templates completos prontos para copiar ao criar novas Skills.

---

## 📄 Template: SKILL.md

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

---

## 📚 Template: REFERENCE.md

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

---

## 💡 Template: EXAMPLES.md

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

---

## 🔧 Template: TROUBLESHOOTING.md

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

## 🎯 Notas de Uso dos Templates

### Customização

Ao usar estes templates:

1. **Substituir placeholders:**
   - `[Nome da Skill]` → Nome real
   - `[DATA]` → Data atual
   - `[N]` → Números reais
   - `[descrição]` → Descrição real

2. **Adicionar seções específicas:**
   - Cada skill é única, adapte conforme necessário
   - Remova seções não aplicáveis

3. **Manter consistência:**
   - Use os mesmos headers em todas as skills
   - Mantenha formato de links igual
   - Progressive Disclosure sempre

### Validação

Após preencher templates:

- [ ] SKILL.md não excede 80 linhas
- [ ] Todos os links markdown funcionam
- [ ] Mínimo 2 exemplos em EXAMPLES.md
- [ ] Mínimo 2 erros em TROUBLESHOOTING.md
- [ ] REFERENCE.md está completo

---

**Templates prontos para:** Criar skills profissionais em minutos
**Baseado em:** Padrão Progressive Disclosure (documentação oficial)
**Última atualização:** 02/11/2025
