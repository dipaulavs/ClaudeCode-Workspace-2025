# Traefik Labels Configuration for SSL

## Working Configuration (Validated 2025-01-10)

The following labels configuration has been tested and confirmed working with Let's Encrypt SSL certificates on VPS 82.25.68.132.

### Minimal Working Configuration

```yaml
deploy:
  labels:
    - "traefik.enable=true"
    - "traefik.http.routers.<service-name>.rule=Host(`<subdomain>.loop9.com.br`)"
    - "traefik.http.routers.<service-name>.entrypoints=websecure"
    - "traefik.http.routers.<service-name>.tls.certresolver=letsencryptresolver"
    - "traefik.http.routers.<service-name>.service=<service-name>"
    - "traefik.http.services.<service-name>.loadbalancer.server.port=<port>"
```

### Key Points

1. **Labels location:** Must be under `deploy.labels` for Docker Swarm mode, NOT at service top level
2. **certresolver:** Use `letsencryptresolver` (not `letsencrypt`)
3. **service reference:** Explicitly set `.service=<service-name>` on router
4. **No tls=true needed:** Don't add `tls=true` - it's implied by `tls.certresolver`
5. **No docker.network needed:** Traefik auto-detects `loop9Net`

### Example from Working Deployment (lf-dashboard)

```yaml
services:
  app:
    image: python:3.11-slim
    networks:
      - loop9Net
    deploy:
      labels:
        - "traefik.enable=true"
        - "traefik.http.routers.lfimoveis.rule=Host(`lfimoveis.loop9.com.br`)"
        - "traefik.http.routers.lfimoveis.entrypoints=websecure"
        - "traefik.http.routers.lfimoveis.tls.certresolver=letsencryptresolver"
        - "traefik.http.routers.lfimoveis.service=lfimoveis"
        - "traefik.http.services.lfimoveis.loadbalancer.server.port=5000"

networks:
  loop9Net:
    external: true
```

### Common Mistakes to Avoid

❌ **WRONG:** Labels at top level
```yaml
services:
  app:
    labels:  # WRONG - won't work in Swarm mode
      - "traefik.enable=true"
```

✅ **CORRECT:** Labels under deploy
```yaml
services:
  app:
    deploy:
      labels:  # CORRECT
        - "traefik.enable=true"
```

❌ **WRONG:** Using `letsencrypt` as certresolver
```yaml
- "traefik.http.routers.app.tls.certresolver=letsencrypt"  # WRONG
```

✅ **CORRECT:** Using `letsencryptresolver`
```yaml
- "traefik.http.routers.app.tls.certresolver=letsencryptresolver"  # CORRECT
```

❌ **WRONG:** Adding `tls=true` (causes default cert)
```yaml
- "traefik.http.routers.app.tls=true"  # DON'T ADD THIS
```

✅ **CORRECT:** Only certresolver, no tls=true
```yaml
- "traefik.http.routers.app.tls.certresolver=letsencryptresolver"  # CORRECT
```

### Troubleshooting

If certificate shows "TRAEFIK DEFAULT CERT":

1. Check labels are under `deploy.labels`
2. Verify certresolver is `letsencryptresolver`
3. Remove `tls=true` if present
4. Full stack recreation may be needed: `docker stack rm <name> && docker stack deploy -c docker-compose.yml <name>`
5. Wait 30-60 seconds for Let's Encrypt challenge to complete

### Validation Commands

```bash
# Check certificate issuer (should show Let's Encrypt R12/R13)
echo | openssl s_client -connect <subdomain>.loop9.com.br:443 -servername <subdomain>.loop9.com.br 2>/dev/null | openssl x509 -noout -issuer

# Check service labels are applied
ssh root@82.25.68.132 "docker service inspect <stack>_<service> --format '{{json .Spec.Labels}}' | jq 'with_entries(select(.key | startswith(\"traefik\")))'"
```
