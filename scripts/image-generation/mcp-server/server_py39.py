#!/usr/bin/env python3
"""
MCP Server for Image Generation - Python 3.9 Compatible
Servidor simplificado sem dependências MCP oficiais
"""

import json
import sys
import os
import time
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional

# Paths
DOWNLOADS_PATH = str(Path.home() / "Downloads")

# API Configuration
API_KEY = "fa32b7ea4ff0e9b5acce83abe09d2b06"
BASE_URL = "https://api.kie.ai"


class ImageGenServer:
    """Servidor JSON-RPC para geração de imagens"""

    def __init__(self):
        self.tools = self._define_tools()

    def _define_tools(self) -> List[Dict]:
        """Define ferramentas disponíveis"""
        return [
            {
                "name": "generate_nanobanana",
                "description": "Gera imagem usando Nano Banana (Gemini 2.5 Flash). Portrait 2:3 fixo.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "Descrição da imagem"
                        },
                        "format": {
                            "type": "string",
                            "enum": ["PNG", "JPEG"],
                            "description": "Formato de saída",
                            "default": "PNG"
                        }
                    },
                    "required": ["prompt"]
                }
            }
        ]

    def handle_request(self, request: Dict) -> Dict:
        """Processa requisição JSON-RPC"""
        method = request.get("method")
        params = request.get("params", {})
        req_id = request.get("id")

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {
                        "name": "image-generation-server",
                        "version": "1.0.0"
                    },
                    "capabilities": {
                        "tools": {}
                    }
                }
            }

        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"tools": self.tools}
            }

        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})

            try:
                result = self._execute_tool(tool_name, arguments)
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, ensure_ascii=False)
                            }
                        ]
                    }
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32000,
                        "message": str(e)
                    }
                }

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": "Method not found"}
        }

    def _execute_tool(self, name: str, args: Dict) -> Dict:
        """Executa ferramenta"""
        if name == "generate_nanobanana":
            return self._generate_nanobanana(
                args.get("prompt"),
                args.get("format", "PNG")
            )
        raise ValueError(f"Unknown tool: {name}")

    def _generate_nanobanana(self, prompt: str, format: str = "PNG") -> Dict:
        """Gera imagem com Nano Banana"""
        try:
            # 1. Criar tarefa
            print(f"[MCP] Gerando imagem: {prompt[:50]}...", file=sys.stderr)

            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "google/nano-banana",
                "input": {
                    "prompt": prompt,
                    "image_size": "2:3",
                    "output_format": format.lower()
                }
            }

            response = requests.post(
                f"{BASE_URL}/api/v1/jobs/createTask",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()

            response_data = response.json()
            print(f"[MCP DEBUG] Create task response: {json.dumps(response_data)[:200]}", file=sys.stderr)

            if not response_data:
                return {"success": False, "error": "Response vazio da API"}

            data = response_data.get("data")
            if not data:
                return {"success": False, "error": f"Sem 'data' no response: {response_data}"}

            # Tenta taskId primeiro, depois id
            task_id = data.get("taskId") or data.get("id")

            if not task_id:
                return {
                    "success": False,
                    "error": "Falha ao criar tarefa"
                }

            # 2. Aguardar conclusão
            print(f"[MCP] Aguardando conclusão...", file=sys.stderr)

            max_attempts = 60
            for attempt in range(max_attempts):
                time.sleep(5)

                status_response = requests.get(
                    f"{BASE_URL}/api/v1/jobs/recordInfo",
                    params={"taskId": task_id},
                    headers=headers,
                    timeout=30
                )
                status_response.raise_for_status()

                status_data = status_response.json()

                if not status_data:
                    continue

                data_obj = status_data.get("data")
                if not data_obj:
                    continue

                status = data_obj.get("status")

                if status == "SUCCESS":
                    print(f"[MCP DEBUG] Status SUCCESS, data: {json.dumps(data_obj)[:300]}", file=sys.stderr)

                    result_json = data_obj.get("resultJson")

                    # Parse resultJson se for string
                    if isinstance(result_json, str):
                        result = json.loads(result_json)
                    elif isinstance(result_json, dict):
                        result = result_json
                    else:
                        result = {}

                    image_urls = result.get("image_urls", [])

                    # Fallback: tentar pegar diretamente de data_obj
                    if not image_urls:
                        image_urls = data_obj.get("image_urls", [])

                    print(f"[MCP DEBUG] Image URLs: {image_urls}", file=sys.stderr)

                    if image_urls:
                        # 3. Baixar imagem
                        image_url = image_urls[0]
                        filename = f"nanobanana_{int(time.time())}.{format.lower()}"
                        filepath = os.path.join(DOWNLOADS_PATH, filename)

                        print(f"[MCP] Baixando imagem...", file=sys.stderr)

                        img_response = requests.get(image_url, stream=True, timeout=60)
                        img_response.raise_for_status()

                        with open(filepath, 'wb') as f:
                            for chunk in img_response.iter_content(chunk_size=8192):
                                f.write(chunk)

                        print(f"[MCP] ✅ Salvo: {filepath}", file=sys.stderr)

                        return {
                            "success": True,
                            "image_url": image_url,
                            "file_path": filepath,
                            "error": ""
                        }

                elif status == "FAILED":
                    return {
                        "success": False,
                        "error": "Geração falhou"
                    }

            return {
                "success": False,
                "error": "Timeout (5 minutos)"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def run(self):
        """Loop principal do servidor"""
        print("[MCP] Image Generation Server iniciado", file=sys.stderr)
        print("[MCP] Aguardando requisições...", file=sys.stderr)

        for line in sys.stdin:
            try:
                request = json.loads(line.strip())
                response = self.handle_request(request)
                print(json.dumps(response), flush=True)
            except json.JSONDecodeError:
                continue
            except Exception as e:
                print(f"[MCP] Erro: {e}", file=sys.stderr)


if __name__ == "__main__":
    server = ImageGenServer()
    server.run()
