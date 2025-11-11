#!/usr/bin/env python3
"""
Backend FastAPI para Claude Code Workspace
Expõe as ferramentas Python como API REST
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
import subprocess
import os
import glob
from datetime import datetime
from pathlib import Path
import json
import asyncio
from typing import AsyncGenerator

app = FastAPI(title="Claude Code Workspace API")

# CORS para permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
WORKSPACE_ROOT = Path(__file__).parent.parent.parent
TOOLS_DIR = WORKSPACE_ROOT / "tools"
DOWNLOADS_DIR = Path.home() / "Downloads"

# Models
class ImageGenerateRequest(BaseModel):
    prompt: str
    tool: str = "nanobanana"  # nanobanana ou gpt
    variants: int = 1
    enhance: bool = False
    format: str = "PNG"

class AudioGenerateRequest(BaseModel):
    text: str
    voice: str = "felipe"
    model: str = "eleven_v3"
    format: str = "mp3_high"

class VideoGenerateRequest(BaseModel):
    prompt: str
    aspect: str = "portrait"
    watermark: bool = False

class TranscribeRequest(BaseModel):
    url: str
    lang: str = "pt"
    task: str = "transcribe"

class TerminalCommandRequest(BaseModel):
    command: str

# Endpoints
@app.get("/")
async def root():
    return {
        "name": "Claude Code Workspace API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/generate/image")
async def generate_image(request: ImageGenerateRequest):
    """Gera imagem usando Google Gemini (Nanobanana) - FAST & CHEAP"""
    try:
        backend_dir = Path(__file__).parent
        venv_python = backend_dir / "venv" / "bin" / "python3"
        script_path = backend_dir / "generate_gemini.py"

        cmd = [
            str(venv_python),
            str(script_path),
            request.prompt,
            "--format", request.format.lower(),
            "--output", str(DOWNLOADS_DIR)
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=backend_dir
        )

        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)

        # Extrair nome do arquivo do output
        output = result.stdout
        file_path = None
        filename = None

        for line in output.split('\n'):
            if '.png' in line or '.jpg' in line or '.jpeg' in line or '.webp' in line:
                parts = line.split(': ')
                if len(parts) >= 2:
                    filename = parts[-1].strip()
                    file_path = str(DOWNLOADS_DIR / filename)
                    break

        return {
            "success": True,
            "output": f"✅ Imagem gerada!\n\n{output}",
            "file_path": file_path,
            "tool": "google-gemini-2.5-flash-image"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate/audio")
async def generate_audio(request: AudioGenerateRequest):
    """Gera áudio usando ElevenLabs"""
    try:
        cmd = [
            "python3",
            str(TOOLS_DIR / "generate_audio_elevenlabs.py"),
            request.text,
            "--voice", request.voice,
            "--model", request.model,
            "--format", request.format
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=WORKSPACE_ROOT
        )

        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)

        # Extrair caminho do arquivo
        output = result.stdout
        file_path = None
        for line in output.split('\n'):
            if 'Áudio salvo em:' in line or 'salvo em:' in line:
                file_path = line.split(':', 1)[1].strip()
                break

        return {
            "success": True,
            "output": output,
            "file_path": file_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate/video")
async def generate_video(request: VideoGenerateRequest):
    """Gera vídeo usando Sora 2"""
    try:
        cmd = [
            "python3",
            str(TOOLS_DIR / "generate_video_sora.py"),
            request.prompt,
            "--aspect", request.aspect
        ]

        if request.watermark:
            cmd.append("--watermark")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=WORKSPACE_ROOT
        )

        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)

        output = result.stdout
        file_path = None
        for line in output.split('\n'):
            if 'Vídeo salvo em:' in line or 'salvo em:' in line:
                file_path = line.split(':', 1)[1].strip()
                break

        return {
            "success": True,
            "output": output,
            "file_path": file_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/transcribe")
async def transcribe(request: TranscribeRequest):
    """Transcreve vídeo/áudio"""
    try:
        cmd = [
            "python3",
            str(TOOLS_DIR / "transcribe_universal.py"),
            request.url,
            "--lang", request.lang,
            "--task", request.task
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=WORKSPACE_ROOT
        )

        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)

        return {
            "success": True,
            "output": result.stdout
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/files")
async def list_files(limit: int = 50):
    """Lista arquivos gerados recentemente em ~/Downloads"""
    try:
        files = []

        # Padrões de arquivos gerados pelas ferramentas
        patterns = ["*.png", "*.jpg", "*.jpeg", "*.mp3", "*.m4a", "*.mp4", "*.txt"]

        for pattern in patterns:
            for file_path in DOWNLOADS_DIR.glob(pattern):
                stat = file_path.stat()
                files.append({
                    "name": file_path.name,
                    "path": str(file_path),
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "type": file_path.suffix[1:]
                })

        # Ordenar por data de modificação (mais recentes primeiro)
        files.sort(key=lambda x: x["modified"], reverse=True)

        return {
            "files": files[:limit],
            "total": len(files)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/files/download/{filename}")
async def download_file(filename: str):
    """Download de arquivo específico"""
    file_path = DOWNLOADS_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )

@app.get("/api/tools")
async def list_tools():
    """Lista todas as ferramentas disponíveis"""
    tools = []

    for py_file in TOOLS_DIR.glob("*.py"):
        if py_file.name.startswith("__"):
            continue

        tool_info = {
            "name": py_file.stem,
            "file": py_file.name,
            "category": "unknown"
        }

        # Categorizar por nome
        if "image" in py_file.stem:
            tool_info["category"] = "image"
        elif "audio" in py_file.stem:
            tool_info["category"] = "audio"
        elif "video" in py_file.stem:
            tool_info["category"] = "video"
        elif "transcribe" in py_file.stem:
            tool_info["category"] = "transcribe"
        elif "extract" in py_file.stem:
            tool_info["category"] = "extract"

        tools.append(tool_info)

    return {"tools": tools}

@app.post("/api/terminal/execute")
async def execute_terminal_command(request: TerminalCommandRequest):
    """Executa um comando no terminal (bash)"""
    try:
        # Criar arquivo temporário com o comando
        import tempfile
        import time

        # Criar script temporário
        timestamp = int(time.time())
        script_file = f"/tmp/claude_cmd_{timestamp}.sh"
        output_file = f"/tmp/claude_output_{timestamp}.txt"

        # Escrever comando no script
        with open(script_file, 'w') as f:
            f.write(f"""#!/bin/bash
cd {WORKSPACE_ROOT}
{request.command} > {output_file} 2>&1
""")

        # Dar permissão de execução
        os.chmod(script_file, 0o755)

        # Executar script em background
        subprocess.Popen([script_file])

        # Aguardar um pouco para o comando começar
        time.sleep(0.5)

        # Ler output se disponível
        output = ""
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                output = f.read()

        return {
            "success": True,
            "command": request.command,
            "output": output[:1000] if output else "Comando executado. Veja o resultado no terminal.",
            "note": "O comando está sendo executado no background. Veja o terminal para o output completo."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/terminal/stream")
async def stream_claude_code(request: TerminalCommandRequest):
    """Executa comando no Claude Code CLI com streaming em tempo real"""

    async def generate_stream() -> AsyncGenerator[str, None]:
        try:
            # Criar processo Claude Code
            process = await asyncio.create_subprocess_exec(
                'claude',
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=WORKSPACE_ROOT
            )

            # Enviar comando para Claude Code
            if process.stdin:
                process.stdin.write(f"{request.command}\n".encode())
                await process.stdin.drain()
                process.stdin.close()

            # Flag para controlar se começamos a receber output
            output_started = False
            buffer = ""

            # Ler stdout linha por linha em tempo real
            if process.stdout:
                while True:
                    try:
                        line = await asyncio.wait_for(process.stdout.readline(), timeout=0.5)
                        if not line:
                            break

                        decoded_line = line.decode('utf-8', errors='replace')
                        buffer += decoded_line

                        # Enviar como SSE (Server-Sent Events)
                        yield f"data: {json.dumps({'type': 'output', 'content': decoded_line})}\n\n"
                        output_started = True

                    except asyncio.TimeoutError:
                        # Enviar heartbeat para manter conexão viva
                        yield f"data: {json.dumps({'type': 'heartbeat'})}\n\n"

                        # Verificar se processo terminou
                        if process.returncode is not None:
                            break

            # Aguardar processo terminar
            await process.wait()

            # Enviar conclusão
            if process.returncode == 0:
                yield f"data: {json.dumps({'type': 'done', 'success': True})}\n\n"
            else:
                # Ler stderr se houver erro
                stderr = ""
                if process.stderr:
                    stderr_bytes = await process.stderr.read()
                    stderr = stderr_bytes.decode('utf-8', errors='replace')

                yield f"data: {json.dumps({'type': 'error', 'content': stderr or 'Processo terminou com erro'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"

    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando Claude Code Workspace API...")
    print(f"📂 Workspace: {WORKSPACE_ROOT}")
    print(f"📥 Downloads: {DOWNLOADS_DIR}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
