# Web Terminal Architecture

## System Overview

The web-terminal system provides a full-featured terminal interface accessible via web browser, with both local and remote access capabilities.

## Components

### 1. Backend API (FastAPI) - Port 8000
- **Location**: `web-interface/backend/main.py`
- **Purpose**: REST API for generating images, audio, video, transcriptions
- **Key endpoints**:
  - `/api/health` - Health check
  - `/api/generate/image` - Google Gemini image generation
  - `/api/generate/audio` - Audio generation
  - `/api/generate/video` - Video generation
  - `/api/transcribe` - Transcription
  - `/api/terminal/stream` - Claude Code streaming
- **Dependencies**: Installed in venv at `backend/venv/`

### 2. Frontend (Python HTTP Server) - Port 3000
- **Location**: `web-interface/frontend/index.html`
- **Purpose**: Web UI for tools and terminal
- **Features**:
  - Image generator interface
  - Audio generator
  - Video generator
  - Transcription tool
  - File browser
  - Chat interface

### 3. Terminal Web (ttyd) - Port 7681
- **Command**: `ttyd claude`
- **Purpose**: Web-based terminal emulator running Claude Code CLI
- **Access**: WebSocket at `/ws`

### 4. Cloudflare Tunnel
- **Config**: `~/.cloudflared/config.yml`
- **Purpose**: Secure remote access via HTTPS
- **Routes**:
  - `claude.loop9.com.br/api/*` → Backend (port 8000)
  - `claude.loop9.com.br/ws` → Terminal (port 7681)
  - `claude.loop9.com.br/*` → Frontend (port 3000)

## Data Flow

```
User (Browser)
    ↓
https://claude.loop9.com.br
    ↓
Cloudflare Tunnel
    ↓
┌────────────────────────────────────┐
│  Routing by path:                  │
│  /api/* → localhost:8000 (Backend) │
│  /ws    → localhost:7681 (Terminal)│
│  /*     → localhost:3000 (Frontend)│
└────────────────────────────────────┘
```

## File Structure

```
web-interface/
├── backend/
│   ├── venv/              # Python virtual environment
│   ├── main.py            # FastAPI application
│   ├── generate_gemini.py # Google Gemini integration
│   └── start-backend.sh   # Startup script
├── frontend/
│   ├── index.html         # Main web interface
│   ├── chat.html          # Chat interface
│   └── server.py          # Simple HTTP server
├── iniciar-tudo.sh        # Master startup script
├── start-backend.sh       # Backend only
├── start-frontend.sh      # Frontend only
├── start-terminal.sh      # Terminal only
└── start-cloudflare.sh    # Cloudflare only
```

## Environment Detection

The frontend automatically detects the environment:

```javascript
const API_BASE = window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : window.location.origin;
```

- **Local**: Uses `http://localhost:8000` directly
- **Remote**: Uses `https://claude.loop9.com.br` (proxied to backend)

## Access URLs

### Local Access
- Frontend: `http://localhost:3000`
- Chat: `http://localhost:3000/chat.html`
- Terminal: `http://localhost:7681`
- API: `http://localhost:8000`

### Remote Access (via Cloudflare)
- Frontend: `https://claude.loop9.com.br`
- Chat: `https://claude.loop9.com.br/chat.html`
- Terminal: `https://claude.loop9.com.br/ws` (WebSocket)
- API: `https://claude.loop9.com.br/api`
