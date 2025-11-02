# 🔄 Sistema de Workflows

Workflows são automações completas que executam múltiplas etapas sequencialmente, combinando agentes e ferramentas.

## O que são Workflows?

Workflows são arquivos `.md` que definem uma sequência de ações automatizadas. Ao invés de executar cada comando manualmente, você ativa o workflow e o Claude Code executa todos os passos do início ao fim.

## Estrutura de um Workflow

Cada workflow deve conter:

```markdown
# Workflow: Nome do Workflow

**Objetivo:** Descrição clara do que o workflow faz

## Input Necessário
- Lista dos inputs que o usuário precisa fornecer

## Etapas do Workflow

### 1. Nome da Etapa
**Ferramenta:** Qual ferramenta/agente usar
**Ação:** Comando ou descrição da ação
**Output:** O que essa etapa produz

### 2. Nome da Próxima Etapa
...
```

## Como Usar Workflows

### Ativar um Workflow

Simplesmente mencione o nome do workflow:

```
Ative o workflow headline-to-image para o nicho de fitness, gerando 4 imagens.
```

O Claude Code irá:
1. Ler o arquivo do workflow
2. Identificar as etapas necessárias
3. Executar cada passo sequencialmente
4. Passar outputs entre etapas automaticamente

### Listar Workflows Disponíveis

```
Liste os workflows disponíveis
```

ou

```
Mostre os workflows que tenho
```

## Workflows Disponíveis

### headline-to-image
Gera imagens com headlines virais automaticamente.

**Input:** Nicho/tema + quantidade de imagens
**Output:** Imagens com headlines otimizadas para redes sociais
**Tempo estimado:** 3-5 minutos

**Etapas:**
1. Gera headlines virais (agente OpenRouter 1201)
2. Cria prompts de imagem (agente imagem-colada)
3. Gera imagens (Nano Banana)

---

## Criar Seus Próprios Workflows

1. Crie um arquivo `.md` em `workflows/`
2. Siga a estrutura padrão (veja exemplos existentes)
3. Defina claramente:
   - Inputs necessários
   - Etapas sequenciais
   - Comandos específicos
   - Outputs esperados

### Exemplo Mínimo

```markdown
# Workflow: Meu Workflow

**Objetivo:** Fazer X, Y e Z

## Input Necessário
- Parâmetro A
- Parâmetro B

## Etapas do Workflow

### 1. Primeira Ação
**Ferramenta:** Nome da ferramenta
**Ação:** python3 tools/script.py "input"
**Output:** Resultado esperado

### 2. Segunda Ação
**Ferramenta:** Nome da ferramenta
**Ação:** Usar output da etapa 1 para...
**Output:** Resultado final
```

## Dicas

- **Seja específico:** Quanto mais detalhes, mais fácil para o Claude Code executar
- **Numere as etapas:** Facilita o acompanhamento do progresso
- **Defina outputs:** Deixe claro o que cada etapa produz
- **Use comandos exatos:** Inclua comandos bash completos quando possível
- **Documente inputs:** Sempre especifique o que o usuário precisa fornecer

## Tipos de Workflows Úteis

- **Conteúdo → Imagem:** Texto/headline → prompt → imagem
- **Conteúdo → Vídeo:** Script → vídeo com narração
- **Análise → Criação:** Pesquisa → análise → conteúdo
- **Batch Processing:** Processar múltiplos itens de uma vez
- **Multi-formato:** Criar o mesmo conteúdo em vários formatos

## Vantagens

✅ **Automação completa:** Um comando executa tudo
✅ **Reusável:** Crie uma vez, use sempre
✅ **Consistente:** Mesmo processo todas as vezes
✅ **Documentado:** Workflow serve como documentação
✅ **Escalável:** Fácil adicionar novos workflows

---

**Localização:** `/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/workflows/`
