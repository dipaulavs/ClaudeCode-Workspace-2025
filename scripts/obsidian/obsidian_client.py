"""
Cliente para interagir com Obsidian via Local REST API

Documentação API: https://coddingtonbear.github.io/obsidian-local-rest-api/
"""

import requests
import json
from datetime import datetime
from pathlib import Path
import sys
import urllib3

# Adicionar path do config
sys.path.append(str(Path(__file__).parent.parent.parent))
from config.obsidian_config import *

# Desabilitar warnings de SSL (desenvolvimento local)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ObsidianClient:
    """Cliente para interagir com Obsidian via REST API"""

    def __init__(self):
        self.api_url = OBSIDIAN_API_URL
        self.headers = get_headers()
        self.verify_ssl = VERIFY_SSL

    def _request(self, method, endpoint, data=None):
        """Faz requisição à API"""
        url = f"{self.api_url}{endpoint}"

        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, verify=self.verify_ssl)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data, verify=self.verify_ssl)
            elif method == "PUT":
                response = requests.put(url, headers=self.headers, json=data, verify=self.verify_ssl)
            elif method == "PATCH":
                response = requests.patch(url, headers=self.headers, json=data, verify=self.verify_ssl)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.headers, verify=self.verify_ssl)

            response.raise_for_status()

            # Se resposta vazia, retornar sucesso
            if not response.content:
                return {"success": True}

            return response.json()

        except requests.exceptions.ConnectionError:
            raise Exception(
                "❌ Não foi possível conectar ao Obsidian!\n"
                "Certifique-se de que:\n"
                "1. Obsidian está aberto\n"
                "2. Plugin 'Local REST API' está ativado\n"
                "3. API está rodando em https://127.0.0.1:27124"
            )
        except requests.exceptions.HTTPError as e:
            raise Exception(f"❌ Erro na API: {e.response.status_code} - {e.response.text}")

    # ==========================================
    # OPERAÇÕES COM NOTAS
    # ==========================================

    def create_note(self, path, content, folder=None):
        """
        Cria uma nova nota

        Args:
            path: Nome/caminho da nota (ex: "Minha Nota" ou "Pasta/Minha Nota")
            content: Conteúdo da nota em Markdown
            folder: Pasta destino (ex: "inbox", "ideas", "projects")

        Returns:
            dict: Resposta da API
        """
        if folder:
            folder_path = FOLDERS.get(folder, folder)
            path = f"{folder_path}/{path}"

        # Adicionar .md se não tiver
        if not path.endswith(".md"):
            path += ".md"

        data = {"content": content}
        return self._request("PUT", f"/vault/{path}", data)

    def read_note(self, path):
        """
        Lê uma nota existente

        Args:
            path: Caminho da nota (ex: "00 - Inbox/Minha Nota.md")

        Returns:
            str: Conteúdo da nota
        """
        response = self._request("GET", f"/vault/{path}")
        return response

    def update_note(self, path, content):
        """
        Atualiza nota existente (sobrescreve)

        Args:
            path: Caminho da nota
            content: Novo conteúdo

        Returns:
            dict: Resposta da API
        """
        data = {"content": content}
        return self._request("PUT", f"/vault/{path}", data)

    def append_to_note(self, path, content):
        """
        Adiciona conteúdo no final de uma nota

        Args:
            path: Caminho da nota
            content: Conteúdo a adicionar

        Returns:
            dict: Resposta da API
        """
        data = {"content": content}
        return self._request("POST", f"/vault/{path}", data)

    def delete_note(self, path):
        """
        Deleta uma nota

        Args:
            path: Caminho da nota

        Returns:
            dict: Resposta da API
        """
        return self._request("DELETE", f"/vault/{path}")

    # ==========================================
    # OPERAÇÕES DE BUSCA
    # ==========================================

    def search(self, query):
        """
        Busca notas por texto

        Args:
            query: Termo de busca

        Returns:
            list: Notas encontradas
        """
        return self._request("POST", f"/search/simple/", {"query": query})

    def list_files(self):
        """
        Lista todos os arquivos do vault

        Returns:
            dict: Lista de arquivos
        """
        return self._request("GET", "/vault/")

    # ==========================================
    # DAILY NOTES
    # ==========================================

    def create_daily_note(self, date=None):
        """
        Cria daily note

        Args:
            date: Data (datetime object) ou None para hoje

        Returns:
            dict: Resposta da API
        """
        if date is None:
            date = datetime.now()

        date_str = date.strftime(DAILY_NOTE_FORMAT)
        weekday = date.strftime("%A")  # Nome do dia da semana

        # Traduzir dia da semana
        weekdays_pt = {
            "Monday": "Segunda-feira",
            "Tuesday": "Terça-feira",
            "Wednesday": "Quarta-feira",
            "Thursday": "Quinta-feira",
            "Friday": "Sexta-feira",
            "Saturday": "Sábado",
            "Sunday": "Domingo"
        }
        weekday_pt = weekdays_pt.get(weekday, weekday)

        filename = f"{date_str} - {weekday_pt}"

        content = f"""# {date_str} - {weekday_pt}

## ✅ Tarefas
- [ ]

## 📝 Notas do Dia


## 🎯 Projetos
-

## 💡 Ideias


## 🤖 Automações Executadas


## 📊 Métricas


## 🧠 Reflexões


---
Tags: #daily-note
Criado: {datetime.now().strftime("%Y-%m-%d %H:%M")}
"""

        return self.create_note(filename, content, folder="daily")

    def get_today_daily_note(self):
        """Retorna path da daily note de hoje"""
        date_str = datetime.now().strftime(DAILY_NOTE_FORMAT)
        weekday = datetime.now().strftime("%A")

        weekdays_pt = {
            "Monday": "Segunda-feira",
            "Tuesday": "Terça-feira",
            "Wednesday": "Quarta-feira",
            "Thursday": "Quinta-feira",
            "Friday": "Sexta-feira",
            "Saturday": "Sábado",
            "Sunday": "Domingo"
        }
        weekday_pt = weekdays_pt.get(weekday, weekday)

        filename = f"{date_str} - {weekday_pt}.md"
        return f"{FOLDERS['daily']}/{filename}"

    def log_to_daily(self, message, section="📝 Notas do Dia"):
        """
        Adiciona entrada na daily note de hoje

        Args:
            message: Mensagem a adicionar
            section: Seção onde adicionar

        Returns:
            dict: Resposta da API
        """
        daily_path = self.get_today_daily_note()

        # Tentar criar daily note se não existir
        try:
            self.create_daily_note()
        except:
            pass  # Já existe

        timestamp = datetime.now().strftime("%H:%M")
        entry = f"\n- **{timestamp}** - {message}"

        return self.append_to_note(daily_path, entry)

    # ==========================================
    # COMANDOS
    # ==========================================

    def execute_command(self, command_id):
        """
        Executa comando do Obsidian

        Args:
            command_id: ID do comando

        Returns:
            dict: Resposta da API
        """
        return self._request("POST", f"/commands/{command_id}")

    # ==========================================
    # UTILITÁRIOS
    # ==========================================

    def test_connection(self):
        """Testa conexão com API"""
        try:
            self.list_files()
            return True
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            return False

    def get_vault_info(self):
        """Retorna informações do vault"""
        return {
            "path": OBSIDIAN_VAULT_PATH,
            "api_url": self.api_url,
            "folders": FOLDERS
        }


# ==========================================
# FUNÇÕES DE CONVENIÊNCIA
# ==========================================

def quick_note(content, folder="inbox"):
    """Cria nota rápida no inbox"""
    client = ObsidianClient()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    filename = f"Quick Note - {datetime.now().strftime('%Y%m%d-%H%M%S')}"

    note_content = f"""# Quick Note

{content}

---
Criado: {timestamp}
"""

    return client.create_note(filename, note_content, folder=folder)


def capture_idea(title, description="", tags=[]):
    """Captura ideia no formato estruturado"""
    client = ObsidianClient()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    tags_str = " ".join([f"#{tag}" for tag in tags]) if tags else "#ideia"

    content = f"""# {title}

## 💡 Descrição

{description}

## 🎯 Contexto


## ✨ Próximos Passos

- [ ]

## 🔗 Links Relacionados


---
Tags: {tags_str}
Criado: {timestamp}
"""

    return client.create_note(title, content, folder="ideas")


if __name__ == "__main__":
    # Teste de conexão
    print("🔍 Testando conexão com Obsidian...")
    client = ObsidianClient()

    if client.test_connection():
        print("✅ Conexão estabelecida!")
        print(f"\n📊 Vault: {OBSIDIAN_VAULT_PATH}")
    else:
        print("❌ Falha na conexão")
