# INDEX - Apps e Sites

**Localização:** `/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/APPS E SITES`

**Propósito:** Centralizar todos os apps e sites criados para deploy no VPS com organização padronizada.

---

## 📋 Regras de Organização

### Estrutura Obrigatória
```
APPS E SITES/
├── INDEX.md (este arquivo)
└── <nome-do-projeto>/
    ├── INDEX.md (status, logs, progresso)
    ├── CHANGELOG.md (histórico de mudanças)
    ├── docker-compose.yml
    ├── Dockerfile (se necessário)
    └── código fonte
```

### Naming Convention
- **Pastas:** kebab-case (ex: `obrigado-site`, `api-webhook`, `lf-dashboard`)
- **Arquivos:** snake_case para scripts, kebab-case para configs
- **Subdomínios:** Mesmo nome da pasta (ex: `obrigado-site` → `obrigado-site.loop9.com.br`)

### INDEX.md Individual (template)
Cada projeto DEVE ter seu INDEX.md com:
- Status atual (dev/staging/production)
- URL de acesso
- Última atualização
- Tecnologias usadas
- Próximos passos
- Log de deploys

---

## 📦 Apps e Sites

### 🟢 Ativos (em produção)

#### obrigado-site
- **URL:** https://obrigado.loop9.com.br
- **Tipo:** Página estática (Nginx)
- **Status:** ✅ Production
- **Deploy:** 2025-11-10
- **Repo:** https://github.com/dipaulavs/obrigado-site
- **INDEX:** [obrigado-site/INDEX.md](obrigado-site/INDEX.md)

---

## 📂 Categorias Organizadas

### 📊 Dashboards
- **INDEX:** [dashboards/INDEX.md](dashboards/INDEX.md)
- **Quantidade:** 1 dashboard
- **Subcategorias:**
  - `real-estate/` - Dashboards para imobiliárias (1)
  - `automation/` - Dashboards de automação (0)
  - `analytics/` - Dashboards de análise (0)

**Projetos:**
- [dashboard-imoveis](dashboards/real-estate/dashboard-imoveis/) - Sistema completo de leads + agenda para imobiliária

---

### 🟡 Em Desenvolvimento

*(Nenhum projeto em desenvolvimento)*

---

### 🔴 Arquivados

*(Nenhum projeto arquivado)*

---

## 📊 Estatísticas

- **Total de projetos:** 2
- **Em produção:** 2
- **Em desenvolvimento:** 0
- **Arquivados:** 0
- **Categorias:** 1 (Dashboards)

---

## 🔧 Comandos Rápidos

```bash
# Criar novo projeto
cd "/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/APPS E SITES"
bash ../.claude/skills/upto-vps/scripts/scaffold_project.sh <nome-projeto> <tipo>

# Listar todos os projetos
ls -la

# Ver status de um projeto
cat <nome-projeto>/INDEX.md
```

---

**Última atualização:** 2025-11-10
