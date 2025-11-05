#!/opt/homebrew/bin/python3.10
# -*- coding: utf-8 -*-
"""
MCP Server for Nextcloud Upload
Provides tools for uploading images to Nextcloud with automatic public links.
"""

import json
import sys
import asyncio
import os
import requests
import xml.etree.ElementTree as ET
from typing import Any, Dict, Optional, List
from pathlib import Path

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, CallToolResult


# Importa configurações do Nextcloud
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.nextcloud_config import (
    NEXTCLOUD_URL,
    NEXTCLOUD_USER,
    NEXTCLOUD_PASSWORD
)

# Configuração fixa
FIXED_FOLDER = "imagens/upload"
UPLOAD_FOLDER = str(Path.home() / "Pictures" / "upload")

# Initialize MCP Server
app = Server("nextcloud-upload")


# ============================================================================
# NEXTCLOUD HELPER FUNCTIONS
# ============================================================================

class NextcloudUploader:
    """Cliente para upload no Nextcloud"""

    def __init__(self, url, user, password):
        self.url = url.rstrip('/')
        self.user = user
        self.password = password
        self.folder = FIXED_FOLDER
        self.webdav_url = f"{self.url}/remote.php/dav/files/{self.user}"
        self.auth = (user, password)

    def upload_file(self, local_path: str) -> str:
        """Faz upload de arquivo para o Nextcloud"""
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {local_path}")

        filename = os.path.basename(local_path)
        remote_path = f"{self.folder}/{filename}"
        upload_url = f"{self.webdav_url}/{remote_path}"

        with open(local_path, 'rb') as f:
            response = requests.put(
                upload_url,
                data=f,
                auth=self.auth,
                headers={'Content-Type': 'application/octet-stream'},
                timeout=60
            )

        if response.status_code in [201, 204]:
            return remote_path
        else:
            raise Exception(f"Erro no upload: {response.status_code}")

    def create_public_link(self, remote_path: str) -> str:
        """Cria link público permanente"""
        ocs_url = f"{self.url}/ocs/v2.php/apps/files_sharing/api/v1/shares"

        data = {
            'path': f"/{remote_path}",
            'shareType': 3,  # Link público
            'permissions': 1  # Somente leitura
        }

        headers = {
            'OCS-APIRequest': 'true',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(
            ocs_url,
            data=data,
            auth=self.auth,
            headers=headers,
            timeout=30
        )

        if response.status_code == 200:
            root = ET.fromstring(response.content)
            token = root.find('.//token')

            if token is not None:
                share_token = token.text
                filename = os.path.basename(remote_path)
                direct_url = f"{self.url}/s/{share_token}/download/{filename}"
                return direct_url
            else:
                raise Exception("Token não encontrado")
        else:
            raise Exception(f"Erro ao criar link: {response.status_code}")

    def upload_and_get_link(self, local_path: str, auto_delete: bool = True) -> Dict:
        """
        Upload + Link + Delete local (opcional)

        Returns:
            dict: {'filename': str, 'url': str, 'deleted': bool}
        """
        filename = os.path.basename(local_path)

        try:
            # Upload
            remote_path = self.upload_file(local_path)

            # Link público
            public_url = self.create_public_link(remote_path)

            # Delete arquivo local (opcional)
            deleted = False
            if auto_delete:
                os.remove(local_path)
                deleted = True

            return {
                'success': True,
                'filename': filename,
                'url': public_url,
                'deleted': deleted,
                'error': ''
            }

        except Exception as e:
            return {
                'success': False,
                'filename': filename,
                'url': '',
                'deleted': False,
                'error': str(e)
            }


def get_files_from_folder(folder_path: str) -> List[Path]:
    """Lista todos os arquivos de uma pasta"""
    folder = Path(folder_path)

    if not folder.exists():
        return []

    files = []
    for file_path in folder.iterdir():
        if file_path.is_file():
            files.append(file_path)

    # Ordena por data de modificação (mais recente primeiro)
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files


async def upload_single_image(file_path: str, auto_delete: bool = True) -> Dict:
    """
    Upload de imagem única

    Args:
        file_path: Caminho do arquivo
        auto_delete: Se True, deleta arquivo local após upload

    Returns:
        {"success": bool, "filename": str, "url": str, "deleted": bool, "error": str}
    """
    try:
        uploader = NextcloudUploader(
            NEXTCLOUD_URL,
            NEXTCLOUD_USER,
            NEXTCLOUD_PASSWORD
        )

        # Upload em thread separada para não bloquear
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            uploader.upload_and_get_link,
            file_path,
            auto_delete
        )

        return result

    except Exception as e:
        return {
            'success': False,
            'filename': os.path.basename(file_path),
            'url': '',
            'deleted': False,
            'error': str(e)
        }


async def upload_batch_images(file_paths: List[str], auto_delete: bool = True) -> List[Dict]:
    """
    Upload batch de múltiplas imagens (paralelo)

    Args:
        file_paths: Lista de caminhos dos arquivos
        auto_delete: Se True, deleta arquivos locais após upload

    Returns:
        Lista de resultados (mesmo formato de upload_single_image)
    """
    tasks = [upload_single_image(path, auto_delete) for path in file_paths]
    results = await asyncio.gather(*tasks)
    return list(results)


async def scan_upload_folder() -> List[Dict]:
    """
    Escaneia pasta ~/Pictures/upload/ e retorna lista de arquivos

    Returns:
        Lista de dicts com info dos arquivos: [{"filename": str, "path": str, "size": int, "modified": str}]
    """
    try:
        files = get_files_from_folder(UPLOAD_FOLDER)

        if not files:
            return []

        result = []
        for file_path in files:
            stat = file_path.stat()
            result.append({
                'filename': file_path.name,
                'path': str(file_path),
                'size': stat.st_size,
                'size_mb': round(stat.st_size / (1024 * 1024), 2),
                'modified': stat.st_mtime
            })

        return result

    except Exception as e:
        return []


# ============================================================================
# Tool Definitions
# ============================================================================

@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    List all available Nextcloud upload tools.
    Returns metadata for each tool that clients can discover and use.
    """
    return [
        Tool(
            name="upload_image",
            description="Faz upload de 1 imagem para Nextcloud (imagens/upload/) e retorna link público permanente. Por padrão deleta arquivo local após upload.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Caminho completo do arquivo a fazer upload"
                    },
                    "auto_delete": {
                        "type": "boolean",
                        "default": True,
                        "description": "Se True, deleta arquivo local após upload bem-sucedido"
                    }
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="upload_batch",
            description="Upload de múltiplas imagens em paralelo. Retorna lista com URLs públicas permanentes. Por padrão deleta arquivos locais após upload.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Lista de caminhos completos dos arquivos"
                    },
                    "auto_delete": {
                        "type": "boolean",
                        "default": True,
                        "description": "Se True, deleta arquivos locais após upload bem-sucedido"
                    }
                },
                "required": ["file_paths"]
            }
        ),
        Tool(
            name="scan_folder",
            description="Escaneia pasta ~/Pictures/upload/ e retorna lista de arquivos disponíveis para upload. Útil para descobrir imagens antes de fazer upload.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="upload_from_scan",
            description="Escaneia ~/Pictures/upload/ e faz upload automático de todos os arquivos encontrados. Retorna URLs públicas permanentes. Por padrão deleta arquivos locais.",
            inputSchema={
                "type": "object",
                "properties": {
                    "auto_delete": {
                        "type": "boolean",
                        "default": True,
                        "description": "Se True, deleta arquivos locais após upload bem-sucedido"
                    }
                },
                "required": []
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[CallToolResult]:
    """
    Execute a tool call and return the result.
    Routes the request to appropriate handler based on tool name.
    """

    if name == "upload_image":
        return await handle_upload_image(arguments)
    elif name == "upload_batch":
        return await handle_upload_batch(arguments)
    elif name == "scan_folder":
        return await handle_scan_folder(arguments)
    elif name == "upload_from_scan":
        return await handle_upload_from_scan(arguments)
    else:
        return [
            CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps({"error": f"Unknown tool: {name}"})
                )],
                isError=True
            )
        ]


async def handle_upload_image(arguments: dict) -> list[CallToolResult]:
    """Handle single image upload"""
    file_path = arguments.get("file_path", "")
    auto_delete = arguments.get("auto_delete", True)

    if not file_path:
        return [CallToolResult(
            content=[TextContent(
                type="text",
                text=json.dumps({"success": False, "error": "file_path é obrigatório"}, ensure_ascii=False)
            )],
            isError=True
        )]

    if not os.path.exists(file_path):
        return [CallToolResult(
            content=[TextContent(
                type="text",
                text=json.dumps({"success": False, "error": f"Arquivo não encontrado: {file_path}"}, ensure_ascii=False)
            )],
            isError=True
        )]

    result = await upload_single_image(file_path, auto_delete)

    return [CallToolResult(
        content=[TextContent(
            type="text",
            text=json.dumps(result, ensure_ascii=False, indent=2)
        )],
        isError=not result.get("success", False)
    )]


async def handle_upload_batch(arguments: dict) -> list[CallToolResult]:
    """Handle batch image upload"""
    file_paths = arguments.get("file_paths", [])
    auto_delete = arguments.get("auto_delete", True)

    if not file_paths or not isinstance(file_paths, list):
        return [CallToolResult(
            content=[TextContent(
                type="text",
                text=json.dumps({"success": False, "error": "file_paths deve ser uma lista não vazia"}, ensure_ascii=False)
            )],
            isError=True
        )]

    # Valida existência dos arquivos
    missing_files = [path for path in file_paths if not os.path.exists(path)]
    if missing_files:
        return [CallToolResult(
            content=[TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": f"Arquivos não encontrados: {', '.join(missing_files)}"
                }, ensure_ascii=False)
            )],
            isError=True
        )]

    results = await upload_batch_images(file_paths, auto_delete)

    # Resumo
    success_count = sum(1 for r in results if r.get('success'))
    summary = {
        'success': success_count == len(results),
        'total': len(results),
        'success_count': success_count,
        'failed_count': len(results) - success_count,
        'results': results
    }

    return [CallToolResult(
        content=[TextContent(
            type="text",
            text=json.dumps(summary, ensure_ascii=False, indent=2)
        )],
        isError=not summary['success']
    )]


async def handle_scan_folder(arguments: dict) -> list[CallToolResult]:
    """Handle folder scan"""
    files = await scan_upload_folder()

    response = {
        'success': True,
        'folder': UPLOAD_FOLDER,
        'count': len(files),
        'files': files
    }

    return [CallToolResult(
        content=[TextContent(
            type="text",
            text=json.dumps(response, ensure_ascii=False, indent=2)
        )],
        isError=False
    )]


async def handle_upload_from_scan(arguments: dict) -> list[CallToolResult]:
    """Handle scan + upload workflow"""
    auto_delete = arguments.get("auto_delete", True)

    # Escaneia pasta
    files = await scan_upload_folder()

    if not files:
        return [CallToolResult(
            content=[TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": f"Nenhum arquivo encontrado em {UPLOAD_FOLDER}"
                }, ensure_ascii=False)
            )],
            isError=True
        )]

    # Faz upload de todos
    file_paths = [f['path'] for f in files]
    results = await upload_batch_images(file_paths, auto_delete)

    # Resumo
    success_count = sum(1 for r in results if r.get('success'))
    summary = {
        'success': success_count == len(results),
        'folder': UPLOAD_FOLDER,
        'total': len(results),
        'success_count': success_count,
        'failed_count': len(results) - success_count,
        'results': results
    }

    return [CallToolResult(
        content=[TextContent(
            type="text",
            text=json.dumps(summary, ensure_ascii=False, indent=2)
        )],
        isError=not summary['success']
    )]


async def main():
    """
    Main entry point for the MCP server.
    Starts stdio server for communication with MCP clients.
    """
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="nextcloud-upload",
                server_version="1.0.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer shutting down...", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        sys.exit(1)
