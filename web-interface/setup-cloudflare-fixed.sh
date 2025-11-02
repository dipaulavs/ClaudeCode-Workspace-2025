#!/bin/bash

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║   🌍 Configuração de Link Fixo - Cloudflare Tunnel        ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📍 Domínio: claude.loop9.com.br"
echo "📍 Apontando para: http://localhost:3000"
echo ""

# Verificar se cloudflared está instalado
if ! command -v cloudflared &> /dev/null; then
    echo "❌ cloudflared não está instalado!"
    echo "   Execute: brew install cloudflare/cloudflare/cloudflared"
    exit 1
fi

echo "✅ cloudflared encontrado: $(cloudflared --version)"
echo ""

# Nome do túnel
TUNNEL_NAME="claude-workspace"
DOMAIN="claude.loop9.com.br"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PASSO 1: Login no Cloudflare"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Você será redirecionado para o navegador para fazer login..."
echo "Pressione ENTER para continuar..."
read

cloudflared tunnel login

if [ $? -ne 0 ]; then
    echo "❌ Erro no login. Tente novamente."
    exit 1
fi

echo ""
echo "✅ Login realizado com sucesso!"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PASSO 2: Criar túnel nomeado"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Verificar se o túnel já existe
if cloudflared tunnel list | grep -q "$TUNNEL_NAME"; then
    echo "⚠️  Túnel '$TUNNEL_NAME' já existe!"
    echo "   Deseja usar o túnel existente? (s/n)"
    read -r response
    if [[ "$response" != "s" ]]; then
        echo "❌ Operação cancelada."
        exit 1
    fi
    echo "✅ Usando túnel existente: $TUNNEL_NAME"
else
    echo "Criando túnel: $TUNNEL_NAME..."
    cloudflared tunnel create $TUNNEL_NAME

    if [ $? -ne 0 ]; then
        echo "❌ Erro ao criar túnel."
        exit 1
    fi
    echo "✅ Túnel criado com sucesso!"
fi

echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PASSO 3: Configurar rota DNS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Criando CNAME: $DOMAIN → túnel..."

cloudflared tunnel route dns $TUNNEL_NAME $DOMAIN

if [ $? -ne 0 ]; then
    echo "⚠️  Rota DNS pode já existir. Continuando..."
else
    echo "✅ DNS configurado com sucesso!"
fi

echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PASSO 4: Criar arquivo de configuração"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Obter UUID do túnel
TUNNEL_ID=$(cloudflared tunnel list | grep "$TUNNEL_NAME" | awk '{print $1}')

if [ -z "$TUNNEL_ID" ]; then
    echo "❌ Não foi possível encontrar o ID do túnel."
    exit 1
fi

echo "✅ Túnel ID: $TUNNEL_ID"

# Criar diretório de config se não existir
mkdir -p ~/.cloudflared

# Criar arquivo de configuração
CONFIG_FILE="$HOME/.cloudflared/config.yml"

cat > "$CONFIG_FILE" << EOF
tunnel: $TUNNEL_ID
credentials-file: $HOME/.cloudflared/$TUNNEL_ID.json

ingress:
  - hostname: $DOMAIN
    service: http://localhost:3000
  - service: http_status:404
EOF

echo "✅ Arquivo de configuração criado: $CONFIG_FILE"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PASSO 5: Criar script de inicialização"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

SCRIPT_PATH="$(dirname "$0")/start-cloudflare-fixed.sh"

cat > "$SCRIPT_PATH" << 'EOF'
#!/bin/bash

echo "🌍 Iniciando Cloudflare Tunnel..."
echo "📍 URL Fixa: https://claude.loop9.com.br"
echo ""
echo "⚠️  IMPORTANTE: Mantenha este terminal aberto!"
echo ""

cloudflared tunnel run
EOF

chmod +x "$SCRIPT_PATH"

echo "✅ Script criado: $SCRIPT_PATH"
echo ""

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║               ✅ CONFIGURAÇÃO CONCLUÍDA! 🎉                ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "🎯 Seu link fixo está pronto:"
echo ""
echo "   ➜  https://claude.loop9.com.br"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 PRÓXIMOS PASSOS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1️⃣  Iniciar o túnel:"
echo "   bash start-cloudflare-fixed.sh"
echo ""
echo "2️⃣  Acessar no navegador (ou celular):"
echo "   https://claude.loop9.com.br"
echo ""
echo "3️⃣  Parar o túnel:"
echo "   Ctrl+C no terminal"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 DICA: O túnel precisa estar rodando para funcionar!"
echo "   Mantenha o terminal aberto enquanto usar remotamente."
echo ""
echo "✅ Deseja testar agora? (s/n)"
read -r test_response

if [[ "$test_response" == "s" ]]; then
    echo ""
    echo "🚀 Iniciando túnel de teste..."
    echo "   Pressione Ctrl+C para parar"
    echo ""
    sleep 2
    cloudflared tunnel run
fi
