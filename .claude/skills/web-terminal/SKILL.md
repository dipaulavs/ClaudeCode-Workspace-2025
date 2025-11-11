---
name: web-terminal
description: Launch and manage a full-featured web-based terminal accessible from any device. Auto-invokes when user requests "web terminal", "terminal web", "remote terminal access", "browser terminal", or wants to run Claude Code from their phone/tablet. Includes FastAPI backend, image/audio/video generation tools, and secure Cloudflare tunnel for remote access.
---

# Web Terminal

## Overview

Launch a complete web-based terminal system that provides Claude Code CLI access through any browser, with integrated tools for image generation (Google Gemini), audio, video, and transcription. Access locally via localhost or remotely from any device via secure Cloudflare tunnel at `https://claude.loop9.com.br`.

## When to Use This Skill

Auto-invoke when user requests:
- **Web terminal access**: "Start the web terminal", "Launch browser terminal"
- **Remote terminal**: "I want to access Claude Code from my phone", "Run terminal on iPad"
- **Terminal with tools**: "Terminal with image generator", "Browser-based Claude with tools"
- **System management**: "Stop web terminal", "Restart terminal server"

## Quick Start

### Start Everything

```bash
bash scripts/start.sh
```

This launches:
- Backend API (port 8000) - FastAPI with generation tools
- Frontend UI (port 3000) - Web interface
- Terminal (port 7681) - ttyd with Claude Code CLI
- Cloudflare Tunnel - Secure remote access

### Stop Everything

```bash
bash scripts/stop.sh
```

Stops all services cleanly.

### Access URLs

**Local Access:**
- Frontend: `http://localhost:3000`
- Chat: `http://localhost:3000/chat.html`
- Terminal: `http://localhost:7681`
- API: `http://localhost:8000`

**Remote Access (via Cloudflare):**
- Frontend: `https://claude.loop9.com.br`
- Chat: `https://claude.loop9.com.br/chat.html`
- Terminal WebSocket: `https://claude.loop9.com.br/ws`
- API: `https://claude.loop9.com.br/api`

## Core Features

### 1. Browser-Based Terminal
- Full Claude Code CLI in browser
- Works on desktop, tablet, mobile
- Persistent sessions via ttyd
- WebSocket-based real-time streaming

### 2. Image Generation
- Google Gemini 2.5 Flash Image (Nanobanana)
- $0.039 per image (3.5x cheaper than GPT-4)
- Multiple formats: PNG, JPEG, WebP
- Saves to `~/Downloads/`

### 3. Audio Generation
- Text-to-speech via integrated APIs
- Multiple voices and formats
- High-quality output

### 4. Video Generation
- AI-generated video clips
- Multiple aspect ratios
- Configurable settings

### 5. Transcription
- YouTube video/audio transcription
- Multiple languages supported
- Text extraction

### 6. Secure Remote Access
- Cloudflare Tunnel (Zero Trust)
- HTTPS encrypted
- No open ports needed
- Access from anywhere

## System Architecture

The web-terminal consists of four integrated components:

```
User Browser
    ↓
https://claude.loop9.com.br (Cloudflare)
    ↓
┌───────────────────────────────────────┐
│  Path-based routing:                  │
│  /api/* → Backend (8000)              │
│  /ws    → Terminal (7681)             │
│  /*     → Frontend (3000)             │
└───────────────────────────────────────┘
```

**See `references/architecture.md` for detailed system architecture.**

## Workflow

### Launching the System

1. **Run startup script**:
   ```bash
   bash scripts/start.sh
   ```

2. **Verify services**:
   - Check logs at `/tmp/backend.log`, `/tmp/frontend.log`, `/tmp/ttyd.log`, `/tmp/cloudflare.log`
   - Test health: `curl https://claude.loop9.com.br/api/health`

3. **Access interface**:
   - Open `https://claude.loop9.com.br` on any device
   - Use image generator, chat, or terminal as needed

### Using Image Generation

From web interface:
1. Navigate to "Gerar Imagem" tab
2. Enter prompt (e.g., "um gatinho fofo")
3. Select format (PNG/JPEG/WebP)
4. Click "Gerar Imagem"
5. Image saved to `~/Downloads/`

From API:
```bash
curl -X POST https://claude.loop9.com.br/api/generate/image \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"um pinguim fofo","format":"PNG"}'
```

### Accessing Terminal Remotely

1. Open `https://claude.loop9.com.br` on phone/tablet
2. Click "Abrir Chat" or navigate to terminal
3. Full Claude Code CLI available
4. Run any command as if on Mac

### Stopping Services

```bash
bash scripts/stop.sh
```

Cleanly terminates:
- Backend API process
- Frontend server
- ttyd terminal
- Cloudflare tunnel

## Configuration

### Backend Setup

Backend requires Python venv with dependencies:

```bash
cd web-interface/backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn anthropic python-dotenv pillow google-genai
```

Dependencies are already configured in existing setup.

### Cloudflare Tunnel

**Config file**: `~/.cloudflared/config.yml`

Current routing:
- `api.loop9.com.br` → port 8000 (optional dedicated API subdomain)
- `claude.loop9.com.br/api/*` → port 8000 (API via main domain)
- `claude.loop9.com.br/ws` → port 7681 (terminal WebSocket)
- `claude.loop9.com.br/*` → port 3000 (frontend catch-all)

**See `references/cloudflare.md` for detailed Cloudflare configuration.**

### Environment Variables

Backend uses:
- `GOOGLE_API_KEY` - For Gemini image generation (from system env)
- `ANTHROPIC_API_KEY` - For Claude Code API calls

## Troubleshooting

### Backend Not Starting

Check venv activation:
```bash
cd web-interface/backend
source venv/bin/activate
python3 main.py
```

Check dependencies:
```bash
pip list | grep -E '(fastapi|pillow|google-genai)'
```

### Image Generation Fails

Verify Google API key:
```bash
echo $GOOGLE_API_KEY
```

Check backend logs:
```bash
tail -50 /tmp/backend.log
```

Test script directly:
```bash
cd web-interface/backend
source venv/bin/activate
python3 generate_gemini.py "test prompt"
```

### Remote Access Not Working

Verify Cloudflare tunnel:
```bash
ps aux | grep cloudflared
tail -30 /tmp/cloudflare.log
```

Test specific routes:
```bash
curl https://claude.loop9.com.br/api/health
```

Restart tunnel:
```bash
pkill cloudflared
cloudflared tunnel run > /tmp/cloudflare.log 2>&1 &
```

### Port Already in Use

Kill existing processes:
```bash
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:3000 | xargs kill -9  # Frontend
lsof -ti:7681 | xargs kill -9  # Terminal
```

Then restart with `scripts/start.sh`.

## Advanced Usage

### Running Individual Components

Start only backend:
```bash
cd web-interface/backend
source venv/bin/activate
python3 main.py
```

Start only frontend:
```bash
cd web-interface/frontend
python3 server.py
```

Start only terminal:
```bash
ttyd -p 7681 claude
```

Start only Cloudflare:
```bash
cloudflared tunnel run > /tmp/cloudflare.log 2>&1 &
```

### Custom Backend Configuration

Modify `web-interface/backend/main.py` to:
- Add new API endpoints
- Integrate additional tools
- Change output directories
- Adjust CORS settings

### Custom Cloudflare Routes

Edit `~/.cloudflared/config.yml`:
```yaml
ingress:
  - hostname: your-domain.com
    path: ^/custom-path
    service: http://localhost:PORT
```

Then reload:
```bash
pkill cloudflared
cloudflared tunnel run > /tmp/cloudflare.log 2>&1 &
```

## Resources

### Scripts

- `scripts/start.sh` - Launch all services
- `scripts/stop.sh` - Stop all services
- `scripts/update_skill.py` - Auto-correction (fix SKILL.md)
- `scripts/log_learning.py` - Auto-correction (log fixes)

### References

- `references/architecture.md` - Detailed system architecture, component descriptions, data flow
- `references/cloudflare.md` - Cloudflare tunnel configuration, DNS setup, troubleshooting

### Location

System code at: `/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/web-interface/`

## Auto-Correction System

This skill includes automatic error correction:

```bash
# Fix SKILL.md
python3 scripts/update_skill.py <old_text> <new_text>

# Log the fix
python3 scripts/log_learning.py <error_desc> <fix_desc> [line]
```

Example:
```bash
python3 scripts/update_skill.py \
    "bash start.sh" \
    "bash scripts/start.sh"

python3 scripts/log_learning.py \
    "Script path incorrect" \
    "Added scripts/ prefix to path" \
    "SKILL.md:42"
```

All fixes logged in `LEARNINGS.md` to prevent recurrence.
