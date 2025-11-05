#!/usr/bin/env python3
"""
Teste simples do MCP server de geração de imagens
Compatível com Python 3.9
"""

import json
import subprocess
import sys
import time
from pathlib import Path


class SimpleMCPClient:
    """Cliente JSON-RPC simples"""

    def __init__(self, server_path):
        self.server_path = server_path
        self.process = None
        self.request_id = 0

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.disconnect()

    def connect(self):
        """Inicia servidor"""
        print("🔌 Conectando ao MCP server...")

        self.process = subprocess.Popen(
            ["python3", str(self.server_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Redireciona stderr para stdout
            text=True,
            bufsize=1
        )

        # Handshake
        self.request_id += 1
        init_request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }

        self.process.stdin.write(json.dumps(init_request) + "\n")
        self.process.stdin.flush()

        # Lê linhas até encontrar JSON válido
        response = None
        for _ in range(10):  # Máximo 10 tentativas
            line = self.process.stdout.readline().strip()
            if not line:
                continue
            # Ignora logs (começam com [MCP])
            if line.startswith("[MCP"):
                print(f"  {line}")
                continue
            # Tenta parsear como JSON
            try:
                result = json.loads(line)
                response = line
                break
            except json.JSONDecodeError:
                continue

        if not response:
            raise RuntimeError("Não recebeu resposta do servidor")

        if "error" in result:
            raise RuntimeError(f"Erro na inicialização: {result['error']}")

        print("✅ Conectado!")
        time.sleep(0.1)

    def disconnect(self):
        """Encerra servidor"""
        if self.process:
            self.process.terminate()
            self.process.wait(timeout=5)
            print("✅ Desconectado")

    def call_tool(self, name, arguments):
        """Chama ferramenta"""
        self.request_id += 1

        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments
            }
        }

        self.process.stdin.write(json.dumps(request) + "\n")
        self.process.stdin.flush()

        # Lê linhas até encontrar JSON válido
        response = None
        for _ in range(200):  # Geração pode demorar
            line = self.process.stdout.readline().strip()
            if not line:
                continue
            # Ignora logs (começam com [MCP])
            if line.startswith("[MCP"):
                print(f"  {line}")
                continue
            # Tenta parsear como JSON
            try:
                result = json.loads(line)
                response = line
                break
            except json.JSONDecodeError:
                continue

        if not response:
            raise RuntimeError("Não recebeu resposta do servidor")

        if "error" in result:
            raise RuntimeError(f"Erro: {result['error']}")

        # Extrai conteúdo
        content = result.get("result", {}).get("content", [])
        if content and len(content) > 0:
            text = content[0].get("text", "{}")
            return json.loads(text)

        return result.get("result")


def test_generate_nanobanana():
    """Testa geração de imagem"""
    server_path = Path(__file__).parent / "mcp-server" / "server_py39.py"

    if not server_path.exists():
        print(f"❌ Servidor não encontrado: {server_path}")
        return

    print("┌────────────────────────────────────────────────┐")
    print("│  TESTE: generate_nanobanana via MCP            │")
    print("└────────────────────────────────────────────────┘\n")

    with SimpleMCPClient(server_path) as client:
        print("🎨 Gerando imagem: 'gato astronauta no espaço'\n")

        start_time = time.time()

        try:
            result = client.call_tool(
                "generate_nanobanana",
                {
                    "prompt": "gato astronauta no espaço, arte digital",
                    "format": "PNG"
                }
            )

            elapsed = time.time() - start_time

            print("\n┌─────────────── RESULTADO ───────────────┐")
            if result.get("success"):
                print("│ ✅ Sucesso!                             │")
                print(f"│ 📁 Arquivo: {result.get('file_path', '')[:35]:<35} │")
                print(f"│ ⏱️  Tempo: {elapsed:.2f}s                         │")
            else:
                print("│ ❌ Falha                                │")
                print(f"│ Erro: {result.get('error', '')[:37]:<37} │")
            print("└─────────────────────────────────────────┘")

        except Exception as e:
            print(f"\n❌ Erro: {e}")
            elapsed = time.time() - start_time
            print(f"⏱️  Tempo até erro: {elapsed:.2f}s")


if __name__ == "__main__":
    test_generate_nanobanana()
