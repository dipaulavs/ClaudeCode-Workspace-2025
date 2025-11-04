# 🎯 Prompt Templates - Biblioteca de Arquiteturas de Prompts

## Quando Usar

Quando usuário **comandar explicitamente**:
- "Pesquise um template de prompt para [objetivo]"
- "Busque template de prompt para [contexto]"
- "Procure prompt engineering para [caso de uso]"
- "Tem algum template de prompt que [faz X]?"

**Fonte:** https://www.aitmpl.com (Claude Code Templates - 100+ templates)

---

## Workflow (3 Passos)

### 1️⃣ Identificar Categoria

Mapear objetivo do usuário para categoria:

| Categoria | Usar Quando | Exemplos |
|-----------|-------------|----------|
| **🤖 Agents** | Especialistas de domínio | Security auditor, React optimizer, DB architect |
| **⚡ Commands** | Comandos customizados | `/generate-tests`, `/optimize-bundle`, `/check-security` |
| **🎨 Skills** | Capacidades reutilizáveis | PDF processing, Excel automation, workflows |
| **🔌 MCPs** | Integrações externas | GitHub, PostgreSQL, Stripe, AWS, OpenAI |
| **⚙️ Settings** | Configurações | Timeouts, memory, output styles |
| **🪝 Hooks** | Automações/triggers | Pre-commit validation, post-completion actions |

### 2️⃣ Consultar Fonte (WebFetch)

**Opção A - Site:** `https://www.aitmpl.com/[categoria]`
- Exemplo: `https://www.aitmpl.com/agents`
- Carregamento dinâmico (pode retornar vazio)

**Opção B - GitHub (fallback):** `https://github.com/davila7/claude-code-templates`
- Mais confiável para listar templates
- Estrutura organizada por categoria

**Estratégia:**
1. Tentar WebFetch no site primeiro
2. Se vazio → consultar GitHub repo
3. Buscar por keywords no conteúdo retornado

### 3️⃣ Apresentar Resultados

Formato de saída:
```
🎯 Templates encontrados para [objetivo]:

📂 Categoria: [nome]

✅ Template 1: [nome]
   → Descrição: [resumo]
   → Quando usar: [contexto]
   → Link: [URL se disponível]

✅ Template 2: [nome]
   ...

💡 Como usar:
   npx claude-code-templates@latest
```

**Se não encontrar:**
- Sugerir categoria mais próxima
- Listar templates relacionados
- Oferecer criar skill customizada (via skill-creator)

---

## Regras Importantes

### ✅ FAZER:
- **Sempre** consultar WebFetch (site ou GitHub)
- **Sempre** mapear para categoria correta
- **Sempre** mostrar link para instalação
- **Sempre** oferecer alternativa se não encontrar

### ❌ NÃO FAZER:
- **NÃO** inventar templates (sempre consultar fonte)
- **NÃO** assumir que site carregou (verificar conteúdo)
- **NÃO** limitar a 1 categoria (explorar múltiplas se necessário)

---

## Ferramentas Permitidas

- **WebFetch** (obrigatório)
- **Read** (para cache local, se criar futuramente)
- **Write** (para salvar resultados, opcional)

---

## Documentação Adicional

- **URLs + Estrutura Completa:** Ver [REFERENCE.md](REFERENCE.md)
- **Exemplos de Consultas:** Ver [EXAMPLES.md](EXAMPLES.md)
- **Problemas Comuns:** Ver [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Skill Type:** Comando explícito (não auto-invoca)
**Versão:** 1.0
**Fonte:** https://www.aitmpl.com + https://github.com/davila7/claude-code-templates
