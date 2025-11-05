#!/usr/bin/env python3.11
"""
Cliente de teste para MCP Image Generation Server

Testa a conexão e chamadas de ferramentas do MCP server de image generation.
Baseado em: whatsapp-chatbot-carros/componentes/cliente_mcp.py

Uso:
    python3 scripts/image-generation/test_mcp_client.py
"""

import asyncio
import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional
from contextlib import asynccontextmanager
from datetime import datetime


class ImageGenMCPClient:
    """Cliente para comunicação com MCP Server de Image Generation"""

    def __init__(self, server_script: str):
        """
        Inicializa cliente MCP

        Args:
            server_script: Caminho para server.py
        """
        self.server_script = Path(server_script)
        self.process = None
        self.reader = None
        self.writer = None
        self.request_id = 0

    async def conectar(self):
        """Inicia processo do servidor MCP"""
        if not self.server_script.exists():
            raise FileNotFoundError(f"Server script não encontrado: {self.server_script}")

        print(f"🔌 Iniciando servidor MCP em: {self.server_script}")

        # Inicia processo (usa Python 3.11 para MCP compatibility)
        # stderr para stdout para capturar erros
        self.process = await asyncio.create_subprocess_exec(
            "python3.11",
            str(self.server_script),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        self.reader = self.process.stdout
        self.writer = self.process.stdin

        # Aguarda inicialização
        await asyncio.sleep(1)

        # Envia handshake de inicialização
        try:
            await self._enviar_inicializacao()
        except Exception as e:
            # Tenta ler mensagens de erro do servidor
            try:
                await asyncio.wait_for(self.reader.read(1024), timeout=0.5)
            except:
                pass
            raise

        print("✅ Cliente MCP conectado com sucesso", flush=True)

    async def _enviar_inicializacao(self):
        """Envia handshake de inicialização para o servidor MCP"""
        self.request_id += 1

        init_request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }

        request_json = json.dumps(init_request) + "\n"
        self.writer.write(request_json.encode())
        await self.writer.drain()

        # Lê resposta de inicialização
        response_line = await self.reader.readline()
        response = json.loads(response_line.decode())

        if "error" in response:
            raise RuntimeError(f"Erro na inicialização: {response['error']}")

    async def desconectar(self):
        """Encerra processo do servidor"""
        if self.process:
            try:
                self.process.terminate()
                await asyncio.wait_for(self.process.wait(), timeout=5)
            except (asyncio.TimeoutError, ProcessLookupError):
                try:
                    self.process.kill()
                except:
                    pass
            print("✅ Cliente MCP desconectado", flush=True)

    async def chamar_ferramenta(self, nome: str, parametros: Dict) -> Any:
        """
        Chama ferramenta no MCP server

        Args:
            nome: Nome da ferramenta
            parametros: Parâmetros da ferramenta

        Returns:
            Resultado da ferramenta
        """
        if not self.process:
            raise RuntimeError("Cliente não conectado. Chame conectar() primeiro.")

        self.request_id += 1

        # Monta request JSON-RPC 2.0
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/call",
            "params": {
                "name": nome,
                "arguments": parametros
            }
        }

        # Envia request
        request_json = json.dumps(request) + "\n"
        self.writer.write(request_json.encode())
        await self.writer.drain()

        # Lê resposta
        response_line = await self.reader.readline()
        response = json.loads(response_line.decode())

        # Verifica erro
        if "error" in response:
            raise RuntimeError(f"Erro MCP: {response['error']}")

        # Retorna resultado
        result = response.get("result", {})

        # Se resultado é lista de TextContent, extrai texto
        if isinstance(result, list) and len(result) > 0:
            if isinstance(result[0], dict) and "text" in result[0]:
                texto = result[0]["text"]
                # Tenta parsear JSON
                try:
                    return json.loads(texto)
                except:
                    return texto

        return result

    async def listar_ferramentas(self) -> List[str]:
        """
        Lista ferramentas disponíveis no servidor

        Returns:
            Lista de nomes de ferramentas
        """
        if not self.process:
            raise RuntimeError("Cliente não conectado. Chame conectar() primeiro.")

        self.request_id += 1

        # Monta request
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/list",
            "params": {}
        }

        # Envia
        request_json = json.dumps(request) + "\n"
        self.writer.write(request_json.encode())
        await self.writer.drain()

        # Lê resposta
        response_line = await self.reader.readline()
        response = json.loads(response_line.decode())

        # Extrai nomes
        tools = response.get("result", {}).get("tools", [])
        return [tool["name"] for tool in tools]


@asynccontextmanager
async def conectar_mcp(server_script: str):
    """
    Context manager para gerenciar conexão MCP

    Uso:
        async with conectar_mcp("mcp-server/server.py") as cliente:
            resultado = await cliente.chamar_ferramenta("generate_image", {...})
    """
    cliente = ImageGenMCPClient(server_script)
    await cliente.conectar()
    try:
        yield cliente
    finally:
        await cliente.desconectar()


# ==============================================================================
# TESTES
# ==============================================================================


async def teste_listar_ferramentas():
    """Testa listagem de ferramentas disponíveis"""
    print("\n1️⃣ Listando ferramentas disponíveis...")
    print("-" * 60)

    server_path = Path(__file__).parent / "mcp-server" / "server_simple.py"

    async with conectar_mcp(str(server_path)) as cliente:
        ferramentas = await cliente.listar_ferramentas()
        print(f"Ferramentas encontradas: {len(ferramentas)}")
        for ferramenta in ferramentas:
            print(f"  • {ferramenta}")


async def teste_generate_image_nanobanana():
    """Testa geração de imagem com Nano Banana"""
    print("\n2️⃣ Testando generate_image (API: nanobanana)...")
    print("-" * 60)

    server_path = Path(__file__).parent / "mcp-server" / "server_simple.py"

    async with conectar_mcp(str(server_path)) as cliente:
        inicio = datetime.now()

        resultado = await cliente.chamar_ferramenta(
            "generate_image",
            {
                "prompt": "gato astronauta flutuando no espaço",
                "api": "nanobanana",
                "quality": "standard"
            }
        )

        tempo = (datetime.now() - inicio).total_seconds()

        print(f"Status: {resultado.get('status', 'desconhecido')}")
        print(f"API: {resultado.get('api')}")
        print(f"Qualidade: {resultado.get('quality')}")
        print(f"Mensagem: {resultado.get('message')}")
        print(f"⏱️  Tempo de resposta: {tempo:.2f}s")


async def teste_generate_image_gpt4o():
    """Testa geração de imagem com GPT-4o"""
    print("\n3️⃣ Testando generate_image (API: gpt4o)...")
    print("-" * 60)

    server_path = Path(__file__).parent / "mcp-server" / "server_simple.py"

    async with conectar_mcp(str(server_path)) as cliente:
        inicio = datetime.now()

        resultado = await cliente.chamar_ferramenta(
            "generate_image",
            {
                "prompt": "paisagem montanhosa ao pôr do sol",
                "api": "gpt4o",
                "quality": "high"
            }
        )

        tempo = (datetime.now() - inicio).total_seconds()

        print(f"Status: {resultado.get('status', 'desconhecido')}")
        print(f"API: {resultado.get('api')}")
        print(f"Qualidade: {resultado.get('quality')}")
        print(f"Mensagem: {resultado.get('message')}")
        print(f"⏱️  Tempo de resposta: {tempo:.2f}s")


async def teste_edit_image():
    """Testa edição de imagem"""
    print("\n4️⃣ Testando edit_image...")
    print("-" * 60)

    server_path = Path(__file__).parent / "mcp-server" / "server_simple.py"

    async with conectar_mcp(str(server_path)) as cliente:
        inicio = datetime.now()

        resultado = await cliente.chamar_ferramenta(
            "edit_image",
            {
                "image_url": "https://example.com/imagem.jpg",
                "operation": "resize",
                "parameters": {"width": 800, "height": 600}
            }
        )

        tempo = (datetime.now() - inicio).total_seconds()

        print(f"Status: {resultado.get('status', 'desconhecido')}")
        print(f"Operação: {resultado.get('operation')}")
        print(f"Mensagem: {resultado.get('message')}")
        print(f"⏱️  Tempo de resposta: {tempo:.2f}s")


async def teste_batch_generate():
    """Testa geração em lote"""
    print("\n5️⃣ Testando batch_generate...")
    print("-" * 60)

    server_path = Path(__file__).parent / "mcp-server" / "server_simple.py"

    async with conectar_mcp(str(server_path)) as cliente:
        inicio = datetime.now()

        prompts = [
            "cachorro brincando na praia",
            "pássaro colorido em uma árvore",
            "flores selvagens em um campo"
        ]

        resultado = await cliente.chamar_ferramenta(
            "batch_generate",
            {
                "prompts": prompts,
                "api": "nanobanana"
            }
        )

        tempo = (datetime.now() - inicio).total_seconds()

        print(f"Status: {resultado.get('status', 'desconhecido')}")
        print(f"API: {resultado.get('api')}")
        print(f"Quantidade de prompts: {resultado.get('prompts_count')}")
        print(f"Mensagem: {resultado.get('message')}")
        print(f"⏱️  Tempo de resposta: {tempo:.2f}s")


async def teste_ferramenta_invalida():
    """Testa chamada a ferramenta inválida"""
    print("\n6️⃣ Testando chamada a ferramenta inválida...")
    print("-" * 60)

    server_path = Path(__file__).parent / "mcp-server" / "server_simple.py"

    async with conectar_mcp(str(server_path)) as cliente:
        try:
            resultado = await cliente.chamar_ferramenta(
                "ferramenta_inexistente",
                {"parametro": "valor"}
            )
            print(f"Resultado: {resultado}")
        except RuntimeError as e:
            print(f"❌ Erro esperado: {e}")


async def main():
    """Função principal que executa todos os testes"""
    print("\n" + "=" * 60)
    print("🧪 TESTES DO CLIENTE MCP - IMAGE GENERATION")
    print("=" * 60)

    try:
        # Teste 1: Listar ferramentas
        await teste_listar_ferramentas()

        # Teste 2: Generate image (Nano Banana)
        await teste_generate_image_nanobanana()

        # Teste 3: Generate image (GPT-4o)
        await teste_generate_image_gpt4o()

        # Teste 4: Edit image
        await teste_edit_image()

        # Teste 5: Batch generate
        await teste_batch_generate()

        # Teste 6: Ferramenta inválida
        await teste_ferramenta_invalida()

        print("\n" + "=" * 60)
        print("✅ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
        print("=" * 60 + "\n")

    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
