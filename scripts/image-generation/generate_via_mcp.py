#!/usr/bin/env python3
"""Gera imagem via MCP server - Versão simplificada"""

import json
import subprocess
import sys
import time
from pathlib import Path

server_path = Path(__file__).parent / "mcp-server" / "server_py39.py"

# Inicia servidor
process = subprocess.Popen(
    ["python3", str(server_path)],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

def send_request(method, params):
    """Envia requisição JSON-RPC"""
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params
    }
    process.stdin.write(json.dumps(request) + "\n")
    process.stdin.flush()

    # Lê até encontrar JSON válido
    for _ in range(300):
        line = process.stdout.readline().strip()
        if not line:
            continue
        if line.startswith("[MCP"):
            print(line)
            continue
        try:
            return json.loads(line)
        except:
            continue
    return None

# Initialize
print("🔌 Conectando ao MCP server...")
result = send_request("initialize", {
    "protocolVersion": "2024-11-05",
    "clientInfo": {"name": "test", "version": "1.0"}
})
print("✅ Conectado!\n")

# Gera imagem
prompt = input("Digite o prompt da imagem: ") or "astronauta gato no espaço"
print(f"\n🎨 Gerando: {prompt}\n")

start = time.time()
result = send_request("tools/call", {
    "name": "generate_nanobanana",
    "arguments": {
        "prompt": prompt,
        "format": "PNG"
    }
})

elapsed = time.time() - start

if result and "result" in result:
    content = result["result"]["content"][0]["text"]
    data = json.loads(content)

    print("\n" + "="*50)
    if data.get("success"):
        print("✅ SUCESSO!")
        print(f"📁 Arquivo: {data.get('file_path')}")
        print(f"🔗 URL: {data.get('image_url')[:60]}...")
        print(f"⏱️  Tempo: {elapsed:.1f}s")
    else:
        print("❌ FALHA")
        print(f"Erro: {data.get('error')}")
    print("="*50)
else:
    print("❌ Sem resposta")

process.terminate()
process.wait()
