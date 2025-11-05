#!/usr/bin/env python3
"""
🔌 CLIENTE MCP - Conexão com MCP Server

Cliente para chamar ferramentas do MCP server via stdio.
"""

import asyncio
import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional
from contextlib import asynccontextmanager


class ClienteMCP:
    """Cliente para comunicação com MCP Server"""

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

        # Inicia processo
        self.process = await asyncio.create_subprocess_exec(
            "python3",
            str(self.server_script),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        self.reader = self.process.stdout
        self.writer = self.process.stdin

        print("✅ Cliente MCP conectado", flush=True)

    async def desconectar(self):
        """Encerra processo do servidor"""
        if self.process:
            self.process.terminate()
            await self.process.wait()
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
            resultado = await cliente.chamar_ferramenta("calcular_financiamento", {...})
    """
    cliente = ClienteMCP(server_script)
    await cliente.conectar()
    try:
        yield cliente
    finally:
        await cliente.desconectar()


# ==============================================================================
# TESTE
# ==============================================================================

async def teste_cliente():
    """Testa cliente MCP"""
    print("🧪 Testando Cliente MCP\n")

    server_path = Path(__file__).parent.parent / "mcp-server" / "server.py"

    async with conectar_mcp(str(server_path)) as cliente:

        # 1. Lista ferramentas
        print("1️⃣ Listando ferramentas...")
        ferramentas = await cliente.listar_ferramentas()
        print(f"   Encontradas: {', '.join(ferramentas)}\n")

        # 2. Testa calcular_financiamento
        print("2️⃣ Testando calcular_financiamento...")
        resultado = await cliente.chamar_ferramenta(
            "calcular_financiamento",
            {
                "valor_veiculo": 45000,
                "valor_entrada": 10000,
                "taxa_juros_mensal": 1.99
            }
        )
        print(f"   Financiamento: {json.dumps(resultado, indent=2, ensure_ascii=False)}\n")

        # 3. Testa analisar_sentimento
        print("3️⃣ Testando analisar_sentimento...")
        resultado = await cliente.chamar_ferramenta(
            "analisar_sentimento",
            {
                "mensagens": ["obrigado!", "gostei muito", "perfeito"]
            }
        )
        print(f"   Sentimento: {json.dumps(resultado, indent=2, ensure_ascii=False)}\n")

        # 4. Testa consultar_fipe
        print("4️⃣ Testando consultar_fipe...")
        resultado = await cliente.chamar_ferramenta(
            "consultar_fipe",
            {
                "marca": "Volkswagen",
                "modelo": "Gol",
                "ano": "2020"
            }
        )
        print(f"   FIPE: {json.dumps(resultado, indent=2, ensure_ascii=False)}\n")

    print("✅ Todos os testes passaram!")


if __name__ == "__main__":
    asyncio.run(teste_cliente())
