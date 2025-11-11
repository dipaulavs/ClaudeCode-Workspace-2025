# Cloudflare Tunnel Configuration

## Current Configuration

The Cloudflare tunnel provides secure remote access to the web-terminal system.

### Tunnel Details
- **Tunnel ID**: `1812daeb-9807-4c31-a8f2-30852e39a98d`
- **Credentials**: `~/.cloudflared/1812daeb-9807-4c31-a8f2-30852e39a98d.json`
- **Config file**: `~/.cloudflared/config.yml`

## Routing Configuration

```yaml
ingress:
  # API Backend (optional dedicated subdomain)
  - hostname: api.loop9.com.br
    service: http://localhost:8000
    originRequest:
      noTLSVerify: true

  # API via main domain
  - hostname: claude.loop9.com.br
    path: ^/api/.*
    service: http://localhost:8000
    originRequest:
      noTLSVerify: true

  # WebSocket for terminal
  - hostname: claude.loop9.com.br
    path: ^/ws
    service: http://localhost:7681
    originRequest:
      noTLSVerify: true

  # Frontend (default)
  - hostname: claude.loop9.com.br
    service: http://localhost:3000
    originRequest:
      noTLSVerify: true

  # Catch-all 404
  - service: http_status:404
```

## Route Priority

Routes are evaluated in order. More specific paths must come before general ones:

1. `/api/*` → Backend (8000) - Most specific
2. `/ws` → Terminal (7681) - Specific path
3. `/*` → Frontend (3000) - Catch-all

## DNS Setup

To enable `api.loop9.com.br`:

1. Access Cloudflare Dashboard
2. Select domain `loop9.com.br`
3. Go to DNS section
4. Add CNAME record:
   - **Type**: CNAME
   - **Name**: api
   - **Target**: `1812daeb-9807-4c31-a8f2-30852e39a98d.cfargotunnel.com`
   - **Proxy**: Enabled (orange cloud)

## Managing the Tunnel

### Start Tunnel
```bash
cloudflared tunnel run
```

### Start in Background
```bash
cloudflared tunnel run > /tmp/cloudflare.log 2>&1 &
```

### Stop Tunnel
```bash
pkill cloudflared
```

### View Logs
```bash
tail -f /tmp/cloudflare.log
```

### Validate Configuration
```bash
cloudflared tunnel ingress validate
```

## Troubleshooting

### Tunnel Not Connecting
```bash
# Check if cloudflared is running
ps aux | grep cloudflared

# Check logs
tail -50 /tmp/cloudflare.log

# Restart tunnel
pkill cloudflared
cloudflared tunnel run > /tmp/cloudflare.log 2>&1 &
```

### Route Not Working
```bash
# Verify config syntax
cloudflared tunnel ingress validate

# Test specific URL
cloudflared tunnel ingress url https://claude.loop9.com.br/api/health
```

### DNS Not Resolving
```bash
# Check DNS propagation
dig api.loop9.com.br
nslookup api.loop9.com.br
```

## Security Notes

- All traffic encrypted via Cloudflare
- No open ports on local machine
- Credentials stored securely in `~/.cloudflared/`
- `noTLSVerify: true` only for localhost connections
