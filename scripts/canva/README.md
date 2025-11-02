# 🎨 Canva MCP Integration

Scripts para interagir com Canva via Model Context Protocol (MCP)

## 📋 Visão Geral

O Canva oferece um servidor MCP oficial que permite:
- ✅ Criar designs novos
- ✅ Autofill de templates (substituir texto/imagens)
- ✅ Buscar designs existentes
- ✅ Exportar designs (PDF/PNG)

## 🔐 Autenticação

O MCP do Canva requer autenticação OAuth. Existem 3 formas de usar:

### Opção 1: Claude.ai Web (Recomendado) ⭐

**Mais fácil e já configurado!**

1. Acesse https://claude.ai/
2. Vá em **Settings** → **Connectors** → **Canva** → **Connect**
3. Use diretamente via chat:
   ```
   "Liste meus designs do Canva"
   "Crie um post Instagram com [descrição]"
   "Preencha o template X com dados Y"
   ```

**Vantagens:**
- ✅ OAuth automático
- ✅ Interface natural (conversa)
- ✅ Sem configuração adicional

### Opção 2: Claude Code via Claude.ai Token

**Para scripts Python personalizados**

⚠️ **Limitação:** Tokens OAuth do Claude.ai web não são compartilhados com Claude Code CLI.

**Status:** Requer implementação de fluxo OAuth completo (complexo).

### Opção 3: API Canva Connect (Alternativa)

**Para automação completa via API REST**

Requer:
- Conta Canva Enterprise (pago)
- Configuração de app no Canva Developers
- Client ID + Client Secret

📚 **Documentação:** https://www.canva.dev/docs/connect/

## 📂 Scripts Disponíveis

| Script | Descrição | Status |
|--------|-----------|--------|
| `list_designs.py` | Lista designs do Canva | ⚠️ Requer OAuth |

## 🚀 Como Usar

### Via Claude.ai Web (Recomendado)

```bash
# 1. Autentique no Claude.ai web (já feito!)
# 2. Abra https://claude.ai/
# 3. Digite comandos naturais:

"Liste meus templates favoritos do Canva"
"Crie post Instagram: fundo azul, texto 'Novidade!'"
"Busque o template 'Promoção' e preencha com [dados]"
"Exporte o design X como PNG"
```

### Via Script Python (Teste - Sem OAuth)

```bash
# Testar conexão (mostrará erro de autenticação esperado)
python3.11 scripts/canva/list_designs.py
```

**Saída esperada:**
```
✅ Servidor respondeu: 401
⚠️ AUTENTICAÇÃO NECESSÁRIA
```

## 🎯 Casos de Uso

### 1. Autofill de Templates

**Problema resolvido:** Você quer usar template favorito, trocar texto/imagem mantendo padrão.

**Solução via Claude.ai:**
```
"Pegue o template 'Post Instagram - Promoção' e preencha:
- Título: 'Black Friday 50% OFF' (max 40 chars)
- Subtítulo: 'Apenas hoje!' (max 20 chars)
- Imagem: /caminho/imagem.jpg
- Exporte como PNG"
```

Claude via MCP:
1. Busca template
2. Valida tamanhos de texto
3. Faz upload da imagem
4. Preenche template
5. Exporta PNG

### 2. Criar Designs em Lote

```
"Para cada item desta lista, crie um post Instagram no Canva:
1. Produto A - R$50
2. Produto B - R$75
3. Produto C - R$100

Use template 'Promoção' e exporte todos como PNG"
```

### 3. Buscar e Reutilizar Designs

```
"Liste meus últimos 10 designs do Canva sobre 'marketing'"
"Pegue o design 'Campanha Janeiro' e crie variação com texto 'Fevereiro'"
```

## 📊 Controle de Caracteres

**Problema:** API não valida limite de caracteres automaticamente.

**Solução:** Validar antes de enviar ao Canva:

```python
def validar_texto(texto, max_chars):
    """Garante que texto não quebre layout"""
    if len(texto) > max_chars:
        return texto[:max_chars-3] + "..."
    return texto

# Uso
titulo = validar_texto("Título muito longo...", 40)
```

**Via Claude.ai (automático):**
```
"Preencha template garantindo:
- Título: max 40 caracteres
- Descrição: max 100 caracteres
Truncar se necessário"
```

Claude valida e ajusta automaticamente.

## 🛠️ Instalação de Dependências

```bash
# Requer Python 3.10+
python3.11 -m pip install mcp httpx
```

## ⚙️ Configuração MCP

```bash
# Adicionar servidor MCP (já feito no workspace)
claude mcp add --transport http canva https://mcp.canva.com/mcp

# Verificar status
claude mcp list
```

## 🔧 Troubleshooting

### Erro: "invalid_token" ou 401

**Normal!** MCP do Canva requer OAuth.

**Solução:** Use Claude.ai web (já autenticado).

### Como funciona OAuth no MCP?

1. Cliente (Claude) solicita acesso
2. Usuário autoriza no navegador (você já fez)
3. Canva emite token de acesso (4 horas)
4. Token é armazenado pelo Claude.ai
5. Requests usam token automaticamente

**Limitação:** Tokens não são compartilhados entre:
- ❌ Claude.ai web ↔ Claude Code CLI
- ❌ Claude Code ↔ Scripts Python customizados

### Alternativa: API Canva Connect Direto

Se precisa de scripts Python sem depender do Claude:

```python
import requests

# Requer: Client ID + Secret (Canva Enterprise)
# Docs: https://www.canva.dev/docs/connect/

# 1. Obter token OAuth
# 2. Criar design via API REST
# 3. Autofill template
# 4. Exportar
```

## 📚 Recursos

- **Canva MCP Docs:** https://www.canva.dev/docs/connect/mcp-server/
- **Canva Connect API:** https://www.canva.dev/docs/connect/
- **MCP Spec:** https://modelcontextprotocol.io/
- **Claude Code MCP:** https://docs.claude.com/en/docs/claude-code/mcp

## 🎯 Recomendação

**Para seu workflow:**

1. ✅ **Use Claude.ai web** para interagir com Canva via MCP
   - Já autenticado
   - Interface natural
   - Todas funcionalidades disponíveis

2. ⚠️ **Scripts Python** ficam como referência/futuro
   - Quando implementar OAuth completo
   - Ou migrar para API Canva Connect (Enterprise)

3. 🔮 **Futuro:** Se precisar automação Python completa
   - Investir em Canva Enterprise
   - Implementar OAuth flow completo
   - Ou usar alternativas (Placid.app, Bannerbear)

---

**Status:** ✅ MCP instalado | ⚠️ OAuth pendente (usar Claude.ai web)
