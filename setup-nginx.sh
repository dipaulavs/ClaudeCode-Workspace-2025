#!/bin/bash
# 🌐 Setup Nginx + SSL - Reverse Proxy para Automações
# Uso: ./setup-nginx.sh <seu-dominio.com>

set -e

if [ -z "$1" ]; then
    echo "Uso: ./setup-nginx.sh <dominio.com>"
    exit 1
fi

DOMAIN="$1"
VPS_HOST="root@82.25.68.132"

echo "🌐 Configurando Nginx + SSL para: $DOMAIN"

# 1. Instalar Nginx e Certbot na VPS
echo "📦 Instalando Nginx e Certbot..."
ssh $VPS_HOST << 'EOF'
apt update -qq
apt install -y nginx certbot python3-certbot-nginx

# Iniciar Nginx
systemctl enable nginx
systemctl start nginx

echo "✅ Nginx instalado"
EOF

# 2. Criar configuração base
echo "⚙️ Criando configuração Nginx..."
ssh $VPS_HOST "cat > /etc/nginx/sites-available/automations <<'NGINX_EOF'
# Mapa de subdomínios → portas
map \$http_host \$backend_port {
    hostnames;

    # Adicione seus serviços aqui:
    # subdomain.DOMAIN           porta
    chatbot.DOMAIN               8000;
    api.DOMAIN                   8001;
    webhook.DOMAIN               8002;
    n8n.DOMAIN                   5678;

    # Padrão (se não encontrar)
    default                      8000;
}

server {
    listen 80;
    server_name *.DOMAIN DOMAIN;

    # Limite de upload (ajuste conforme necessário)
    client_max_body_size 50M;

    location / {
        proxy_pass http://localhost:\$backend_port;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        # WebSocket support (para n8n e outros)
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection \"upgrade\";

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 'OK';
        add_header Content-Type text/plain;
    }
}
NGINX_EOF
"

# Substituir DOMAIN pelo domínio real
ssh $VPS_HOST "sed -i 's/DOMAIN/$DOMAIN/g' /etc/nginx/sites-available/automations"

# Ativar configuração
ssh $VPS_HOST "ln -sf /etc/nginx/sites-available/automations /etc/nginx/sites-enabled/automations"
ssh $VPS_HOST "rm -f /etc/nginx/sites-enabled/default"
ssh $VPS_HOST "nginx -t && systemctl reload nginx"

echo "✅ Nginx configurado"

# 3. Obter certificado SSL (Let's Encrypt)
echo "🔒 Obtendo certificado SSL..."
echo ""
echo "⚠️  IMPORTANTE: Certifique-se que o domínio $DOMAIN já está apontando para 82.25.68.132"
echo ""
read -p "Domínio configurado? (s/N): " -r
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo "Configure o domínio primeiro e rode novamente."
    exit 0
fi

ssh $VPS_HOST "certbot --nginx -d $DOMAIN -d *.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN || echo 'SSL falhou, mas Nginx está rodando'"

echo ""
echo "✅ Setup concluído!"
echo ""
echo "🎯 Seus serviços agora estão em:"
echo "   https://chatbot.$DOMAIN (porta 8000)"
echo "   https://api.$DOMAIN (porta 8001)"
echo "   https://webhook.$DOMAIN (porta 8002)"
echo "   https://n8n.$DOMAIN (porta 5678)"
echo ""
echo "📝 Para adicionar novos subdomínios:"
echo "   1. Edite: ssh $VPS_HOST nano /etc/nginx/sites-available/automations"
echo "   2. Adicione linha no 'map': subdomain.$DOMAIN porta;"
echo "   3. Recarregue: ssh $VPS_HOST systemctl reload nginx"
echo ""
