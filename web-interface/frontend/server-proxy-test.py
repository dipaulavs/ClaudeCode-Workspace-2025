#!/usr/bin/env python3
"""
Servidor HTTP com proxy para terminal (ttyd) - VERSÃO DE TESTE
"""
import http.server
import socketserver
import os
import urllib.request
import urllib.error

PORT = 3001  # Usar porta diferente para teste
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
TERMINAL_URL = "http://localhost:7681"

print("="*50)
print("INICIANDO SERVIDOR DE TESTE COM PROXY")
print("="*50)

class ProxyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        print(f"\n>>> [PROXY GET] Request: {self.path}")

        if self.path.startswith('/terminal'):
            print(f">>> [PROXY] Fazendo proxy para terminal: {self.path}")
            self.proxy_to_terminal()
        else:
            print(f">>> [STATIC] Servindo arquivo estático: {self.path}")
            super().do_GET()

    def do_HEAD(self):
        print(f"\n>>> [PROXY HEAD] Request: {self.path}")

        if self.path.startswith('/terminal'):
            print(f">>> [PROXY] Fazendo proxy HEAD para terminal: {self.path}")
            self.proxy_to_terminal()
        else:
            super().do_HEAD()

    def proxy_to_terminal(self):
        """Faz proxy das requisições /terminal/* para localhost:7681"""
        try:
            # Remover /terminal do path
            terminal_path = self.path.replace('/terminal', '', 1)
            if not terminal_path:
                terminal_path = '/'

            proxy_url = f"{TERMINAL_URL}{terminal_path}"
            print(f">>> [PROXY] URL de destino: {proxy_url}")

            # Fazer requisição ao ttyd
            req = urllib.request.Request(proxy_url)

            # Copiar headers importantes
            for header in ['Cookie', 'User-Agent']:
                if header in self.headers:
                    req.add_header(header, self.headers[header])

            # Executar requisição
            with urllib.request.urlopen(req) as response:
                print(f">>> [PROXY] Resposta recebida: {response.status}")

                # Enviar resposta
                self.send_response(response.status)

                # Copiar headers da resposta
                for header, value in response.headers.items():
                    if header.lower() not in ['connection', 'transfer-encoding']:
                        self.send_header(header, value)

                self.end_headers()

                # Copiar conteúdo
                self.wfile.write(response.read())
                print(f">>> [PROXY] Conteúdo enviado com sucesso")

        except urllib.error.URLError as e:
            print(f">>> [PROXY ERROR] Terminal offline: {str(e)}")
            self.send_error(503, f"Terminal offline: {str(e)}")
        except Exception as e:
            print(f">>> [PROXY ERROR] Erro no proxy: {str(e)}")
            self.send_error(500, f"Erro no proxy: {str(e)}")

    def end_headers(self):
        if not self.path.startswith('/terminal'):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), ProxyHTTPRequestHandler) as httpd:
        print(f"\n🌐 Servidor de TESTE rodando em http://localhost:{PORT}")
        print(f"📂 Servindo arquivos de: {DIRECTORY}")
        print(f"🖥️  Proxy terminal: http://localhost:{PORT}/terminal → {TERMINAL_URL}")
        print("\n💡 Teste com: curl http://localhost:3001/terminal")
        print("="*50)
        print("\n")
        httpd.serve_forever()
