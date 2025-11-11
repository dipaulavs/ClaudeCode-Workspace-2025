# Changelog - upto-vps

## 2025-11-10 - Deploy Alias Automation

### Added
- **Step 8: Create Deploy Alias** - Automação de criação de alias para deploy rápido
- Template de alias com todos os placeholders necessários
- Exemplo real do alias `deploy-lf` do projeto lfimoveis-dashboard
- Documentação de variáveis a substituir (project-slug, project-name, vps-folder, stack-name)
- Comandos de referência rápida incluindo uso do alias

### Changed
- Renumeração: "Step 7: Validation & Documentation" → "Step 7: Validation"
- Renumeração: "Update Documentation" → "Step 9: Update Documentation"
- Quick Reference Commands agora inclui exemplo de deploy com alias

### Improved
- Workflow completo agora inclui criação automática de alias de deploy
- Usuário pode atualizar projetos com um único comando após deploy inicial
- Documentação do projeto agora deve incluir comando do alias criado

### Impact
- Reduz tempo de deploy de atualizações de ~5 comandos para 1 comando
- Padroniza processo de atualização em todos os projetos
- Facilita manutenção de múltiplos projetos na VPS

## Previous Versions
- Skill criada com workflow completo de deploy (CNAME, GitHub, Docker Swarm, SSL)
- Validação automática de SSL e endpoints
- Sistema de auto-correção para prevenir erros recorrentes
