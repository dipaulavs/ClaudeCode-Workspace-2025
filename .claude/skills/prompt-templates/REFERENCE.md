# 📚 Prompt Templates - Referência Técnica Completa

## Fonte de Dados

### Site Principal
**URL:** https://www.aitmpl.com
**Descrição:** Claude Code Templates - repositório de 100+ templates prontos

### GitHub Repository
**URL:** https://github.com/davila7/claude-code-templates
**Owner:** davila7
**Licença:** MIT (Agents: wshobson/agents | Commands: awesome-claude-code CC0)

---

## Estrutura de Categorias

### 🤖 Agents (48 templates)
**URL:** https://www.aitmpl.com/agents
**Descrição:** AI specialists para domínios específicos
**Fonte:** wshobson's agents library (MIT licensed)

**Exemplos:**
- Security auditors
- React performance optimizers
- Database architects
- Code reviewers
- API designers

**Quando usar:** Usuário precisa de especialista em [área técnica]

---

### ⚡ Commands (21 templates)
**URL:** https://www.aitmpl.com/commands
**Descrição:** Comandos slash customizados para Claude Code
**Fonte:** awesome-claude-code collection (CC0 1.0)

**Exemplos:**
- `/generate-tests` - Gerar testes automaticamente
- `/optimize-bundle` - Otimizar bundle size
- `/check-security` - Auditar vulnerabilidades
- `/refactor-code` - Refatoração inteligente
- `/document-api` - Documentar APIs

**Quando usar:** Usuário quer criar comando customizado para [ação repetitiva]

---

### 🎨 Skills (NEW)
**URL:** https://www.aitmpl.com/skills
**Descrição:** Capacidades reutilizáveis model-invoked

**Exemplos:**
- PDF processing
- Excel automation (xlsx)
- Custom workflows
- Data transformation
- File operations

**Quando usar:** Usuário precisa de capacidade reutilizável para [tipo de arquivo/workflow]

---

### 🔌 MCPs (Model Context Protocols)
**URL:** https://www.aitmpl.com/mcps
**Descrição:** Integrações com serviços externos

**Plataformas disponíveis (30+):**
- **OpenAI** - GPT, DALL-E, Whisper APIs
- **Anthropic** - Claude AI integration
- **GitHub** - Git automation & Actions
- **PostgreSQL** - Database queries
- **Stripe** - Payment processing
- **AWS** - Cloud & serverless APIs
- **Salesforce** - CRM & Lightning platform
- **Shopify** - E-commerce APIs
- **Twilio** - Communication APIs

**Quando usar:** Usuário quer integrar Claude Code com [plataforma/serviço]

---

### ⚙️ Settings
**URL:** https://www.aitmpl.com/settings
**Descrição:** Configurações do Claude Code

**Tipos:**
- Timeouts (request/response)
- Memory settings (context window)
- Output styles (formatting)
- Logging levels
- Rate limiting

**Quando usar:** Usuário precisa customizar [comportamento do Claude Code]

---

### 🪝 Hooks
**URL:** https://www.aitmpl.com/hooks
**Descrição:** Automações e triggers

**Tipos:**
- Pre-commit validation (linting, testes)
- Post-completion actions (deploy, notify)
- On-error handlers
- Context switching triggers

**Quando usar:** Usuário quer automatizar [ação antes/depois de evento]

---

## Estratégia de Consulta (WebFetch)

### Ordem de Prioridade

1. **Site Principal (aitmpl.com)**
   ```
   https://www.aitmpl.com/[categoria]
   ```
   - **Vantagem:** Interface visual, descrições
   - **Desvantagem:** Carregamento dinâmico (pode retornar vazio)

2. **GitHub Repo (fallback confiável)**
   ```
   https://github.com/davila7/claude-code-templates
   ```
   - **Vantagem:** Sempre disponível, estrutura clara
   - **Desvantagem:** Sem UI, formato raw

3. **Documentação Oficial**
   ```
   https://docs.aitmpl.com
   ```
   - **Vantagem:** Guias detalhados
   - **Desvantagem:** Pode não ter lista completa

### Formato de Consulta WebFetch

```python
# Exemplo 1: Buscar Agents
WebFetch(
    url="https://www.aitmpl.com/agents",
    prompt="List all available agent templates with: 1) Name, 2) Description, 3) Use cases. Format as markdown table."
)

# Exemplo 2: Buscar por keyword
WebFetch(
    url="https://github.com/davila7/claude-code-templates",
    prompt="Find all templates related to 'security auditing' or 'vulnerability scanning'. List name, category, and description."
)

# Exemplo 3: Categoria específica no GitHub
WebFetch(
    url="https://github.com/davila7/claude-code-templates/tree/main/agents",
    prompt="List all agent templates in this directory with their descriptions."
)
```

### Parsing de Resultados

**Site carregou vazio?**
- Verificar se conteúdo retornado tem "Loading Components..."
- Verificar se contador mostra "Found(0 results)"
- Se sim → usar GitHub como fallback

**Conteúdo parcial?**
- Extrair o que foi carregado
- Complementar com consulta GitHub

**Sucesso total?**
- Apresentar resultados formatados
- Incluir links diretos

---

## Ferramentas Adicionais do Site

### 1. Claude Code Analytics
**Comando:** `npx claude-code-templates@latest analytics`
**Função:** Performance monitoring

### 2. Claude Code Health Check
**Comando:** `npx claude-code-templates@latest health`
**Função:** Optimization diagnostics

### 3. Claude Conversation Monitor
**Comando:** `npx claude-code-templates@latest monitor`
**Função:** Real-time response analysis

### 4. Plugin Dashboard
**Comando:** `npx claude-code-templates@latest plugins`
**Função:** Visual plugin management

---

## Instalação de Templates

### Via NPX (recomendado)
```bash
npx claude-code-templates@latest
```
- Interface interativa
- Stack Builder visual
- Instalação guiada

### Manual (GitHub)
1. Clonar repo: `git clone https://github.com/davila7/claude-code-templates`
2. Navegar para categoria desejada
3. Copiar arquivo de template
4. Colar em `.claude/[categoria]/`

---

## Mapeamento Usuário → Categoria

| Pedido do Usuário | Categoria Provável | URL Consultar |
|-------------------|-------------------|---------------|
| "Auditar segurança" | Agents → Security | `/agents` |
| "Criar comando para testes" | Commands | `/commands` |
| "Integrar com Stripe" | MCPs | `/mcps` |
| "Processar PDFs" | Skills | `/skills` |
| "Validar antes de commit" | Hooks | `/hooks` |
| "Configurar timeout" | Settings | `/settings` |
| "Otimizar React" | Agents → Performance | `/agents` |
| "Gerar docs de API" | Commands | `/commands` |

---

## Limitações Conhecidas

### Site (aitmpl.com)
- **Carregamento dinâmico:** JavaScript pode não executar no WebFetch
- **Mobile optimization:** Mensagem "Optimizing for mobile" indica carregamento lento
- **Search vazio:** Interface mostra "Found(0 results)" antes de carregar

### GitHub (fallback)
- **Sem descrições ricas:** README pode ter menos detalhes que site
- **Estrutura de pastas:** Templates podem estar em subdiretórios
- **Licenças mistas:** Agents (MIT) vs Commands (CC0)

### WebFetch Geral
- **Timeout:** Páginas pesadas podem não carregar completo
- **Conteúdo dinâmico:** JavaScript não executa (só HTML inicial)
- **Rate limiting:** Evitar múltiplas consultas rápidas

---

## Expansão Futura (Opcional)

### Cache Local (se demanda aumentar)
1. Criar `prompt-templates-cache.json`
2. Indexar todos templates 1x
3. Atualizar semanalmente (cron job)
4. Busca offline (Read + JSON parse)

### Integração com skill-creator
- Se template não existe → oferecer criar skill customizada
- Usar template base do aitmpl.com
- Adaptar para contexto do usuário

---

## Links Úteis

- **Site:** https://www.aitmpl.com
- **GitHub:** https://github.com/davila7/claude-code-templates
- **Docs:** https://docs.aitmpl.com
- **Discord:** https://discord.gg/[link-comunidade]
- **NPM:** https://www.npmjs.com/package/claude-code-templates

---

**Versão:** 1.0
**Atualização:** 2025-11-04
