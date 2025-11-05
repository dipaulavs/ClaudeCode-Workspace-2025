"""
Integração com Chatwoot para Escalonamento
Atribuição de corretores e gerenciamento de conversas
"""

import requests
import os
from typing import Optional, Dict


class ChatwootEscalonamento:
    """Gerencia escalonamento via Chatwoot API"""

    def __init__(self, chatwoot_config: Optional[Dict] = None):
        """
        Args:
            chatwoot_config: Dict com url, token, account_id
                            Se None, usa variáveis de ambiente
        """
        if chatwoot_config:
            self.api_url = chatwoot_config.get('url', '').rstrip('/')
            self.api_token = chatwoot_config.get('token', '')
            self.account_id = chatwoot_config.get('account_id', '')
        else:
            # Fallback para variáveis de ambiente
            self.api_url = os.getenv('CHATWOOT_API_URL', '').rstrip('/')
            self.api_token = os.getenv('CHATWOOT_API_TOKEN', '')
            self.account_id = os.getenv('CHATWOOT_ACCOUNT_ID', '')

        self.headers = {
            'api_access_token': self.api_token,
            'Content-Type': 'application/json'
        }

    def buscar_conversa_id(self, cliente_numero: str) -> Optional[int]:
        """
        Busca conversation_id do cliente no Chatwoot

        Args:
            cliente_numero: Número do cliente (formato: 5531980160822)

        Returns:
            conversation_id ou None
        """
        try:
            # Busca conversas do account
            url = f"{self.api_url}/api/v1/accounts/{self.account_id}/conversations"

            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                conversations = response.json().get('data', {}).get('payload', [])

                # Procura conversa do cliente
                for conv in conversations:
                    contact = conv.get('meta', {}).get('sender', {})
                    phone = contact.get('phone_number', '').replace('+', '')

                    if phone == cliente_numero:
                        return conv.get('id')

            print(f"⚠️ Conversa não encontrada para {cliente_numero}")
            return None

        except Exception as e:
            print(f"❌ Erro ao buscar conversa: {e}")
            return None

    def atribuir_corretor(self, conv_id: int, corretor_id: int) -> bool:
        """
        Atribui corretor à conversa

        Args:
            conv_id: ID da conversa
            corretor_id: ID do corretor no Chatwoot

        Returns:
            True se atribuído
        """
        try:
            url = f"{self.api_url}/api/v1/accounts/{self.account_id}/conversations/{conv_id}/assignments"

            payload = {
                "assignee_id": corretor_id
            }

            response = requests.post(url, headers=self.headers, json=payload)

            if response.status_code in [200, 201]:
                print(f"✅ Corretor {corretor_id} atribuído à conversa {conv_id}")
                return True
            else:
                print(f"⚠️ Erro ao atribuir: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"❌ Erro ao atribuir corretor: {e}")
            return False

    def aplicar_tag_escalonamento(self, conv_id: int, trigger: str) -> bool:
        """
        Aplica tag de escalonamento na conversa

        Args:
            conv_id: ID da conversa
            trigger: Nome do trigger (ex: "quer_visitar")

        Returns:
            True se aplicado
        """
        try:
            url = f"{self.api_url}/api/v1/accounts/{self.account_id}/conversations/{conv_id}/labels"

            # Tag no formato: escalonamento_quer_visitar
            tag = f"escalonamento_{trigger}"

            payload = {
                "labels": [tag]
            }

            response = requests.post(url, headers=self.headers, json=payload)

            if response.status_code in [200, 201]:
                print(f"✅ Tag '{tag}' aplicada à conversa {conv_id}")
                return True
            else:
                print(f"⚠️ Erro ao aplicar tag: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Erro ao aplicar tag: {e}")
            return False

    def adicionar_nota_privada(self, conv_id: int, nota: str) -> bool:
        """
        Adiciona nota privada (visível só para equipe)

        Args:
            conv_id: ID da conversa
            nota: Texto da nota

        Returns:
            True se adicionado
        """
        try:
            url = f"{self.api_url}/api/v1/accounts/{self.account_id}/conversations/{conv_id}/messages"

            payload = {
                "content": nota,
                "message_type": "outgoing",
                "private": True
            }

            response = requests.post(url, headers=self.headers, json=payload)

            if response.status_code in [200, 201]:
                print(f"✅ Nota privada adicionada à conversa {conv_id}")
                return True
            else:
                print(f"⚠️ Erro ao adicionar nota: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Erro ao adicionar nota: {e}")
            return False

    def criar_nota_escalonamento(
        self,
        conv_id: int,
        trigger: str,
        score: int,
        cliente_numero: str
    ) -> bool:
        """
        Cria nota privada completa de escalonamento

        Args:
            conv_id: ID da conversa
            trigger: Trigger que causou escalonamento
            score: Score do lead
            cliente_numero: Número do cliente

        Returns:
            True se criado
        """
        emoji_score = "🔥" if score >= 70 else "🌡️" if score >= 40 else "❄️"

        nota = f"""
🔔 ESCALONAMENTO AUTOMÁTICO

Trigger: {trigger}
Score: {score} {emoji_score}
Cliente: {cliente_numero}
Data/Hora: {self._get_timestamp()}
        """.strip()

        return self.adicionar_nota_privada(conv_id, nota)

    def _get_timestamp(self) -> str:
        """Retorna timestamp formatado"""
        from datetime import datetime
        return datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    def get_link_conversa(self, conv_id: int) -> str:
        """
        Retorna link direto para conversa no Chatwoot

        Args:
            conv_id: ID da conversa

        Returns:
            URL da conversa
        """
        # Assume que Chatwoot está em loop9.com.br
        # Ajustar se for outro domínio
        base_url = self.api_url.replace('/api/v1', '')
        return f"{base_url}/app/accounts/{self.account_id}/conversations/{conv_id}"
