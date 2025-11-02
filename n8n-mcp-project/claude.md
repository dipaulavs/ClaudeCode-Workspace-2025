# n8n-MCP Claude Code Instructions

## ⚠️ CRITICAL SAFETY RULES

### 🚫 NEVER DELETE WORKFLOWS
**NEVER, UNDER ANY CIRCUMSTANCES, DELETE ANY WORKFLOW WITHOUT EXPLICIT USER CONFIRMATION.**

Before deleting ANY workflow, you MUST:
1. Show the workflow name and ID
2. Ask for explicit confirmation: "Do you want me to DELETE workflow '[name]' (ID: [id])? This cannot be undone."
3. Wait for user's YES/NO response
4. Only proceed if user explicitly confirms with "yes", "delete", "confirm" or similar affirmative response

**This is a HARD RULE. Violation of this rule is unacceptable.**

---

## Overview
This project uses the n8n-MCP server to create and manage n8n workflows through natural language prompts.

**Instance:** https://n8n.loop9.com.br

## Available Tools via n8n-MCP

- `list_nodes`: Get all available n8n nodes
- `get_node_documentation`: Get detailed documentation for specific nodes
- `list_templates`: Browse 3000+ workflow templates
- `create_workflow`: Create new workflows on n8n instance
- `update_workflow`: Modify existing workflows
- `get_workflow`: Retrieve workflow details
- `list_workflows`: List all workflows on instance
- `delete_workflow`: ⚠️ REQUIRES USER CONFIRMATION - See safety rules above

## Best Practices

### 1. Always use Plan Mode for complex workflows
   - Ask clarifying questions before implementation
   - Break down complex automations into phases
   - Validate approach with user before building

### 2. Start with node discovery
   - Use `list_nodes` to see available options
   - Check `get_node_documentation` for specific nodes
   - Search `list_templates` for similar workflows

### 3. Iterative approach
   - Start simple, test, then enhance
   - Build workflows in logical phases
   - Test each phase before moving forward

### 4. When creating workflows
   - Use descriptive Portuguese names (ex: "Chatbot com OpenAI e Wikipedia")
   - Add helpful notes to nodes in Portuguese
   - Set up error handling when applicable
   - Configure proper credentials
   - Always inform user which workflows were created/modified

## Workflow Complexity Guidelines

### Simple workflows (1-5 nodes)
- Can usually be one-shotted
- Direct prompt is fine
- Examples: Simple chatbots, basic notifications, single API calls

### Medium workflows (5-15 nodes)
- Use plan mode
- Ask for clarification on integrations
- Check templates for similar patterns
- Examples: Newsletter automations, multi-step data processing, scheduled reports

### Complex workflows (15+ nodes)
- ALWAYS use plan mode
- Break into multiple phases
- Ask detailed questions about:
  - Data sources
  - Transformation requirements
  - Error handling needs
  - Scheduling preferences
  - Integration credentials
- Examples: Multi-stage scraping, advanced AI agents, complex data pipelines

## Example Prompts

### Good prompts:
- "Crie um chatbot usando OpenAI com memória e ferramenta Wikipedia"
- "Crie uma newsletter diária que extrai RSS feeds, resume com AI e envia por Gmail"
- "Configure um trigger de formulário que processa dados através de múltiplas APIs e armazena no Airtable"

### Better prompts (for complex workflows):
- "Preciso de uma automação de vagas do LinkedIn. Me diga quais detalhes você precisa antes de começar."
- "Crie um workflow de onboarding de clientes. Pergunte sobre fontes de dados e integrações primeiro."

## Safety Guidelines

### ⚠️ NEVER:
- Delete workflows without explicit user confirmation (see critical rules above)
- Edit production workflows without asking first
- Run workflows without user review
- Make destructive changes without confirmation
- Assume what the user wants - always clarify

### ✅ ALWAYS:
- Create copies of existing workflows before editing (ask first)
- Show complete workflow structure before deploying
- Ask for confirmation before executing changes
- Suggest testing in development first
- Use descriptive Portuguese names for workflows and nodes
- Document what you created/changed
- List workflow IDs when referring to specific workflows

## Communication Style

- **Language:** Respond in Portuguese (BR)
- **Tone:** Professional but friendly
- **Clarity:** Always explain what you're doing with n8n-mcp
- **Transparency:** Show workflow names, IDs, and structures when relevant

## Troubleshooting

If n8n-MCP is not responding:
1. Check if .mcp.json is properly configured
2. Verify N8N_API_URL doesn't have trailing slash
3. Confirm N8N_API_KEY is valid
4. Restart Claude Code
5. Test connection: `npx n8n-mcp` in terminal

## Project Structure

- `.mcp.json` - MCP server configuration (configured ✅)
- `claude.md` - This instruction file
- `workflows/` - Directory for exported workflows (optional)
- `docs/` - Documentation for created workflows (optional)

## n8n Instance Details

- **URL:** https://n8n.loop9.com.br
- **API Access:** Configured ✅
- **Scopes:** Full access (all scopes enabled)

## Quick Reference

### Create a simple workflow
```
"Crie um workflow simples que [descrição]"
```

### Plan a complex workflow
```
"Modo de planejamento: Preciso criar [descrição complexa]. O que você precisa saber?"
```

### List existing workflows
```
"Liste todos os workflows na instância n8n"
```

### Update existing workflow
```
"Atualize o workflow [nome/ID] para [mudanças desejadas]"
```

### Get workflow details
```
"Mostre os detalhes do workflow [nome/ID]"
```

---

**Remember:** Safety first! Never delete workflows without confirmation. Always communicate clearly what you're doing with the n8n instance.
