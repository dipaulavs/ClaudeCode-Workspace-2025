#!/bin/bash
# Validate SSL certificate for a domain

DOMAIN=$1

if [ -z "$DOMAIN" ]; then
    echo "Usage: $0 <subdomain>.loop9.com.br"
    exit 1
fi

echo "🔍 Checking SSL certificate for $DOMAIN..."
echo ""

# Check certificate issuer
echo "📜 Certificate Details:"
echo | openssl s_client -connect "$DOMAIN:443" -servername "$DOMAIN" 2>/dev/null | openssl x509 -noout -issuer -subject -dates 2>/dev/null

echo ""
echo "✅ If issuer shows 'Let's Encrypt', SSL is working correctly"
echo "❌ If issuer shows 'TRAEFIK DEFAULT CERT', SSL configuration failed"
