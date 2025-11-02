---
name: orshot-design
description: Generate professional designs and images using Orshot API. Use when user asks to create images, designs, social media posts, certificates, or any visual content. Automates image generation from templates with custom text, colors, and data. Model-invoked - activates automatically when user needs image generation or design automation.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# Orshot Design Generator Skill

## Objetivo
Automatizar a criação de designs profissionais usando Orshot API - alternativa 3x mais barata que Canva ($0.01/render).

## Quando Usar Esta Skill
**Automaticamente ativada** quando usuário:
- Pede para criar imagens/designs
- Quer gerar posts para redes sociais
- Precisa de certificados/convites personalizados
- Solicita múltiplas variações de um design
- Quer automatizar geração de imagens em escala

## Workflow Automático

### 1. Entender Requisição
- Analisar o que o usuário quer criar
- Identificar tipo de design (post, certificado, OG image, etc)
- Definir textos/cores/dados necessários

### 2. Escolher Template
- Usar template pré-pronto do Orshot OU
- Criar template customizado no Studio

### 3. Gerar Imagem
Usar script apropriado:
- **Único:** `scripts/orshot/generate_image.py`
- **Múltiplos:** `scripts/orshot/batch_generate.py`
- **Listar:** `scripts/orshot/list_templates.py`

### 4. Salvar/Mostrar Resultado
- Salvar imagem localmente
- Mostrar preview ao usuário
- Oferecer exportar/compartilhar

## Scripts Principais

```bash
# Gerar imagem única
python3 scripts/orshot/generate_image.py --template "open-graph-image-1" --title "Título" --output "result.png"

# Gerar em lote
python3 scripts/orshot/batch_generate.py --template "certificado" --data "dados.json" --output-dir "certificados/"

# Listar templates
python3 scripts/orshot/list_templates.py
```

## Documentação Adicional
- **Capacidades e configuração:** Ver `REFERENCE.md`
- **Casos de uso práticos:** Ver `EXAMPLES.md`
- **Solução de problemas:** Ver `TROUBLESHOOTING.md`

---

**Skill Type:** Model-invoked (ativação automática)
**Versão:** 2.0 (Progressive Disclosure)
