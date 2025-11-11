#!/bin/bash

# Script para criar estrutura de projeto organizada
# Uso: ./scaffold_project.sh <project-name> <type>
# Exemplo: ./scaffold_project.sh my-api flask

set -e

PROJECT_NAME=$1
TYPE=$2
BASE_DIR="/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/APPS E SITES"
DATE=$(date +%Y-%m-%d)

if [ -z "$PROJECT_NAME" ]; then
    echo "❌ Erro: Nome do projeto não especificado"
    echo "Uso: $0 <project-name> <type>"
    echo "Tipos: static, flask, node, api, dashboard"
    exit 1
fi

if [ -z "$TYPE" ]; then
    TYPE="static"
    echo "⚠️  Tipo não especificado, usando padrão: static"
fi

PROJECT_DIR="${BASE_DIR}/${PROJECT_NAME}"

if [ -d "$PROJECT_DIR" ]; then
    echo "❌ Erro: Projeto '$PROJECT_NAME' já existe em $PROJECT_DIR"
    exit 1
fi

echo "🚀 Criando estrutura do projeto: $PROJECT_NAME"
echo "📁 Tipo: $TYPE"
echo "📂 Localização: $PROJECT_DIR"
echo ""

# Criar diretório do projeto
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Copiar template INDEX.md
if [ -f "../../.claude/skills/upto-vps/assets/PROJECT_INDEX_TEMPLATE.md" ]; then
    cp "../../.claude/skills/upto-vps/assets/PROJECT_INDEX_TEMPLATE.md" INDEX.md

    # Substituir placeholders
    sed -i '' "s/{{PROJECT_NAME}}/${PROJECT_NAME}/g" INDEX.md
    sed -i '' "s/{{DATE}}/${DATE}/g" INDEX.md
    sed -i '' "s/{{TYPE}}/${TYPE}/g" INDEX.md
    sed -i '' "s/{{SUBDOMAIN}}/${PROJECT_NAME}/g" INDEX.md
    sed -i '' "s/{{REPO_NAME}}/${PROJECT_NAME}/g" INDEX.md
    sed -i '' "s/{{STACK_NAME}}/${PROJECT_NAME}/g" INDEX.md
    sed -i '' "s/{{STATUS}}/dev/g" INDEX.md

    # Substituir tech stack baseado no tipo
    case $TYPE in
        static)
            sed -i '' "s/{{TECH}}/HTML\/CSS\/JS/g" INDEX.md
            sed -i '' "s/{{SERVER}}/Nginx Alpine/g" INDEX.md
            sed -i '' "s/{{PORT}}/80/g" INDEX.md
            ;;
        flask)
            sed -i '' "s/{{TECH}}/Python 3.11 + Flask/g" INDEX.md
            sed -i '' "s/{{SERVER}}/Gunicorn/g" INDEX.md
            sed -i '' "s/{{PORT}}/5000/g" INDEX.md
            ;;
        node)
            sed -i '' "s/{{TECH}}/Node.js 20 + Express/g" INDEX.md
            sed -i '' "s/{{SERVER}}/Node/g" INDEX.md
            sed -i '' "s/{{PORT}}/3000/g" INDEX.md
            ;;
        api)
            sed -i '' "s/{{TECH}}/Flask\/FastAPI/g" INDEX.md
            sed -i '' "s/{{SERVER}}/Uvicorn\/Gunicorn/g" INDEX.md
            sed -i '' "s/{{PORT}}/8000/g" INDEX.md
            ;;
        dashboard)
            sed -i '' "s/{{TECH}}/React\/Next.js/g" INDEX.md
            sed -i '' "s/{{SERVER}}/Node/g" INDEX.md
            sed -i '' "s/{{PORT}}/3000/g" INDEX.md
            ;;
        *)
            sed -i '' "s/{{TECH}}/TBD/g" INDEX.md
            sed -i '' "s/{{SERVER}}/TBD/g" INDEX.md
            sed -i '' "s/{{PORT}}/8080/g" INDEX.md
            ;;
    esac

    echo "✅ INDEX.md criado"
else
    echo "⚠️  Template INDEX.md não encontrado, criando básico..."
    echo "# ${PROJECT_NAME}\n\nCriado em: ${DATE}" > INDEX.md
fi

# Criar CHANGELOG.md
cat > CHANGELOG.md << EOF
# Changelog - ${PROJECT_NAME}

## ${DATE} - Initial Release

### Added
- Projeto criado via scaffold script
- Estrutura inicial configurada
- Documentação básica

### Status
- [x] Estrutura criada
- [ ] Docker configurado
- [ ] DNS CNAME criado
- [ ] Deploy realizado
- [ ] SSL provisionado
EOF

echo "✅ CHANGELOG.md criado"

# Criar .gitignore básico
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.npm
.pnp/
dist/
build/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Env
.env
.env.local
*.log
EOF

echo "✅ .gitignore criado"

# Criar README.md básico
cat > README.md << EOF
# ${PROJECT_NAME}

${TYPE} application deployed on loop9.com.br infrastructure.

## Quick Start

\`\`\`bash
# Development
# (Add your dev commands here)

# Deploy
git add . && git commit -m "feat: update" && git push
ssh root@82.25.68.132 "cd /root/${PROJECT_NAME} && git pull && docker service update --force ${PROJECT_NAME}_app"
\`\`\`

## Documentation

See [INDEX.md](INDEX.md) for complete documentation.

## Links

- Production: https://${PROJECT_NAME}.loop9.com.br
- Repository: https://github.com/dipaulavs/${PROJECT_NAME}
EOF

echo "✅ README.md criado"

echo ""
echo "✅ Estrutura do projeto criada com sucesso!"
echo ""
echo "📋 Próximos passos:"
echo ""
echo "1. Adicionar código fonte ao projeto:"
echo "   cd '$PROJECT_DIR'"
echo ""
echo "2. Criar/copiar arquivos da aplicação"
echo ""
echo "3. Configurar docker-compose.yml:"
echo "   cp ../../.claude/skills/upto-vps/assets/docker-compose.template.yml docker-compose.yml"
echo ""
echo "4. Atualizar master INDEX:"
echo "   # Editar: ${BASE_DIR}/INDEX.md"
echo ""
echo "5. Usar skill upto-vps para deploy completo"
echo ""
echo "📂 Projeto criado em: $PROJECT_DIR"
