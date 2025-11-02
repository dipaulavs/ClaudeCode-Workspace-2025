"""
Evolution API - Módulo completo para integração com WhatsApp
Documentação: https://doc.evolution-api.com
"""

import requests
import json
from typing import Optional, Dict, List, Union
from pathlib import Path
import base64
import mimetypes


class EvolutionAPI:
    """
    Classe para integração completa com a Evolution API

    Recursos disponíveis:
    - Gerenciamento de instâncias
    - Envio de mensagens (texto, mídia, áudio, localização, contatos)
    - Gerenciamento de grupos
    - Perfil e status
    - Webhooks
    - E muito mais
    """

    def __init__(self, base_url: str, api_key: str, instance_name: str):
        """
        Inicializa a conexão com a Evolution API

        Args:
            base_url: URL base da API (ex: https://evolution.loop9.com.br)
            api_key: Chave de autenticação da API
            instance_name: Nome da instância do WhatsApp
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.instance_name = instance_name
        self.headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, files: Optional[Dict] = None) -> Dict:
        """
        Faz uma requisição HTTP para a API

        Args:
            method: Método HTTP (GET, POST, PUT, DELETE)
            endpoint: Endpoint da API
            data: Dados a serem enviados
            files: Arquivos a serem enviados

        Returns:
            Resposta da API em formato JSON
        """
        url = f"{self.base_url}{endpoint}"

        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers, params=data)
            elif method.upper() == 'POST':
                if files:
                    headers = {'apikey': self.api_key}
                    response = requests.post(url, headers=headers, data=data, files=files)
                else:
                    response = requests.post(url, headers=self.headers, json=data)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=self.headers, json=data)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=self.headers, json=data)
            else:
                raise ValueError(f"Método HTTP inválido: {method}")

            response.raise_for_status()
            return response.json() if response.text else {}

        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            if hasattr(e.response, 'text'):
                print(f"Resposta do servidor: {e.response.text}")
            raise

    # ==================== INSTÂNCIAS ====================

    def create_instance(self, qrcode: bool = True) -> Dict:
        """Cria uma nova instância do WhatsApp"""
        endpoint = f"/instance/create"
        data = {
            "instanceName": self.instance_name,
            "qrcode": qrcode
        }
        return self._make_request('POST', endpoint, data)

    def get_instance_status(self) -> Dict:
        """Obtém o status da instância"""
        endpoint = f"/instance/connectionState/{self.instance_name}"
        return self._make_request('GET', endpoint)

    def logout_instance(self) -> Dict:
        """Desconecta a instância"""
        endpoint = f"/instance/logout/{self.instance_name}"
        return self._make_request('DELETE', endpoint)

    def delete_instance(self) -> Dict:
        """Deleta a instância"""
        endpoint = f"/instance/delete/{self.instance_name}"
        return self._make_request('DELETE', endpoint)

    # ==================== MENSAGENS ====================

    def send_text(self, number: str, text: str, delay: int = 0) -> Dict:
        """
        Envia mensagem de texto

        Args:
            number: Número do destinatário (com DDI e DDD, sem símbolos)
            text: Texto da mensagem
            delay: Delay em milissegundos (opcional)

        Returns:
            Resposta da API
        """
        endpoint = f"/message/sendText/{self.instance_name}"
        data = {
            "number": number,
            "text": text,
            "delay": delay
        }
        return self._make_request('POST', endpoint, data)

    def send_media(self, number: str, media_url: str, caption: str = "",
                   media_type: str = "image", filename: Optional[str] = None) -> Dict:
        """
        Envia mídia (imagem, vídeo, documento)

        Args:
            number: Número do destinatário
            media_url: URL da mídia ou caminho local do arquivo
            caption: Legenda da mídia
            media_type: Tipo de mídia (image, video, document, audio)
            filename: Nome do arquivo (obrigatório para documentos)

        Returns:
            Resposta da API
        """
        endpoint = f"/message/sendMedia/{self.instance_name}"

        # Se for um arquivo local, converte para base64
        if Path(media_url).exists():
            with open(media_url, 'rb') as f:
                media_base64 = base64.b64encode(f.read()).decode('utf-8')
                mime_type = mimetypes.guess_type(media_url)[0] or 'application/octet-stream'
                media_url = f"data:{mime_type};base64,{media_base64}"

        data = {
            "number": number,
            "mediatype": media_type,
            "media": media_url,
            "caption": caption
        }

        if filename:
            data["fileName"] = filename

        return self._make_request('POST', endpoint, data)

    def send_audio(self, number: str, audio_url: str) -> Dict:
        """
        Envia áudio narrado (PTT - Push To Talk)

        Args:
            number: Número do destinatário
            audio_url: URL do áudio ou caminho local

        Returns:
            Resposta da API
        """
        endpoint = f"/message/sendWhatsAppAudio/{self.instance_name}"

        # Se for um arquivo local, converte para base64
        if Path(audio_url).exists():
            with open(audio_url, 'rb') as f:
                audio_base64 = base64.b64encode(f.read()).decode('utf-8')
                audio_url = f"data:audio/ogg;base64,{audio_base64}"

        data = {
            "number": number,
            "audio": audio_url
        }
        return self._make_request('POST', endpoint, data)

    def send_location(self, number: str, latitude: float, longitude: float,
                      name: str = "", address: str = "") -> Dict:
        """
        Envia localização

        Args:
            number: Número do destinatário
            latitude: Latitude
            longitude: Longitude
            name: Nome do local
            address: Endereço do local

        Returns:
            Resposta da API
        """
        endpoint = f"/message/sendLocation/{self.instance_name}"
        data = {
            "number": number,
            "latitude": latitude,
            "longitude": longitude,
            "name": name,
            "address": address
        }
        return self._make_request('POST', endpoint, data)

    def send_contact(self, number: str, contact_number: str,
                     full_name: str, organization: str = "", email: str = "") -> Dict:
        """
        Envia contato

        Args:
            number: Número do destinatário
            contact_number: Número do contato a ser enviado
            full_name: Nome completo do contato
            organization: Empresa/Organização
            email: E-mail do contato

        Returns:
            Resposta da API
        """
        endpoint = f"/message/sendContact/{self.instance_name}"
        data = {
            "number": number,
            "contact": [{
                "fullName": full_name,
                "wuid": contact_number,
                "phoneNumber": contact_number,
                "organization": organization,
                "email": email
            }]
        }
        return self._make_request('POST', endpoint, data)

    def send_reaction(self, number: str, key: Union[str, Dict], reaction: str) -> Dict:
        """
        Envia reação a uma mensagem

        Args:
            number: Número do destinatário
            key: ID da mensagem a reagir (string) ou objeto key completo (dict)
            reaction: Emoji da reação

        Returns:
            Resposta da API
        """
        endpoint = f"/message/sendReaction/{self.instance_name}"

        # Se key for string, converte para objeto
        if isinstance(key, str):
            key_obj = {
                "remoteJid": f"{number}@s.whatsapp.net" if '@' not in number else number,
                "fromMe": True,
                "id": key
            }
        else:
            key_obj = key

        data = {
            "key": key_obj,
            "reaction": reaction
        }
        return self._make_request('POST', endpoint, data)

    def send_reply(self, number: str, text: str, message_id: str) -> Dict:
        """
        Responde uma mensagem

        Args:
            number: Número do destinatário
            text: Texto da resposta
            message_id: ID da mensagem a responder

        Returns:
            Resposta da API
        """
        endpoint = f"/message/sendText/{self.instance_name}"
        data = {
            "number": number,
            "text": text,
            "quoted": {
                "key": {
                    "id": message_id
                }
            }
        }
        return self._make_request('POST', endpoint, data)

    def send_mention(self, group_id: str, text: str, mentions: List[str]) -> Dict:
        """
        Envia mensagem com menções

        Args:
            group_id: ID do grupo
            text: Texto da mensagem
            mentions: Lista de números a mencionar

        Returns:
            Resposta da API
        """
        endpoint = f"/message/sendText/{self.instance_name}"
        data = {
            "number": group_id,
            "text": text,
            "mentions": mentions
        }
        return self._make_request('POST', endpoint, data)

    def send_poll(self, number: str, name: str, options: List[str],
                  selectable_count: int = 1) -> Dict:
        """
        Envia enquete

        Args:
            number: Número do destinatário ou grupo
            name: Título da enquete
            options: Lista de opções
            selectable_count: Quantidade de opções selecionáveis

        Returns:
            Resposta da API
        """
        endpoint = f"/message/sendPoll/{self.instance_name}"
        data = {
            "number": number,
            "name": name,
            "selectableCount": selectable_count,
            "values": options
        }
        return self._make_request('POST', endpoint, data)

    def send_status(self, content: str, type: str = "text",
                    background_color: str = "#000000", font: int = 1,
                    all_contacts: bool = True, status_jid_list: Optional[List[str]] = None,
                    caption: str = "") -> Dict:
        """
        Envia status/história

        Args:
            content: Conteúdo do status (texto ou URL da mídia)
            type: Tipo (text, image, audio)
            background_color: Cor de fundo para texto (ex: #008000)
            font: Fonte para texto (1-5)
            all_contacts: Se True, envia para todos. Se False, usa statusJidList
            status_jid_list: Lista de contatos específicos (quando all_contacts=False)
            caption: Legenda para imagem/vídeo

        Returns:
            Resposta da API
        """
        endpoint = f"/message/sendStatus/{self.instance_name}"
        data = {
            "type": type,
            "content": content,
            "allContacts": all_contacts
        }

        # Só adiciona statusJidList se allContacts for False
        if not all_contacts and status_jid_list:
            data["statusJidList"] = status_jid_list

        # Adiciona campos específicos por tipo
        if type == "text":
            data["backgroundColor"] = background_color
            data["font"] = font
        elif type in ["image", "video"]:
            if caption:
                data["caption"] = caption

        return self._make_request('POST', endpoint, data)

    # ==================== GRUPOS ====================

    def create_group(self, subject: str, participants: List[str],
                     description: str = "") -> Dict:
        """
        Cria um novo grupo

        Args:
            subject: Nome do grupo
            participants: Lista de números dos participantes
            description: Descrição do grupo

        Returns:
            Resposta da API
        """
        endpoint = f"/group/create/{self.instance_name}"
        data = {
            "subject": subject,
            "participants": participants,
            "description": description
        }
        return self._make_request('POST', endpoint, data)

    def update_group_name(self, group_id: str, subject: str) -> Dict:
        """
        Atualiza o nome do grupo

        Args:
            group_id: ID do grupo
            subject: Novo nome do grupo

        Returns:
            Resposta da API
        """
        endpoint = f"/group/updateGroupSubject/{self.instance_name}?groupJid={group_id}"
        data = {
            "subject": subject
        }
        return self._make_request('POST', endpoint, data)

    def update_group_description(self, group_id: str, description: str) -> Dict:
        """
        Atualiza a descrição do grupo

        Args:
            group_id: ID do grupo
            description: Nova descrição

        Returns:
            Resposta da API
        """
        endpoint = f"/group/updateGroupDescription/{self.instance_name}?groupJid={group_id}"
        data = {
            "description": description
        }
        return self._make_request('POST', endpoint, data)

    def update_group_picture(self, group_id: str, image_url: str) -> Dict:
        """
        Atualiza a foto do grupo

        Args:
            group_id: ID do grupo
            image_url: URL da imagem ou caminho local

        Returns:
            Resposta da API
        """
        endpoint = f"/group/updateGroupPicture/{self.instance_name}?groupJid={group_id}"

        # Se for um arquivo local, converte para base64
        if Path(image_url).exists():
            with open(image_url, 'rb') as f:
                image_base64 = base64.b64encode(f.read()).decode('utf-8')
                image_url = f"data:image/png;base64,{image_base64}"

        data = {
            "image": image_url
        }
        return self._make_request('POST', endpoint, data)

    def add_participant(self, group_id: str, participants: List[str]) -> Dict:
        """
        Adiciona participantes ao grupo

        Args:
            group_id: ID do grupo
            participants: Lista de números a adicionar

        Returns:
            Resposta da API
        """
        endpoint = f"/group/updateParticipant/{self.instance_name}?groupJid={group_id}"
        data = {
            "action": "add",
            "participants": participants
        }
        return self._make_request('POST', endpoint, data)

    def remove_participant(self, group_id: str, participants: List[str]) -> Dict:
        """
        Remove participantes do grupo

        Args:
            group_id: ID do grupo
            participants: Lista de números a remover

        Returns:
            Resposta da API
        """
        endpoint = f"/group/updateParticipant/{self.instance_name}?groupJid={group_id}"
        data = {
            "action": "remove",
            "participants": participants
        }
        return self._make_request('POST', endpoint, data)

    def promote_participant(self, group_id: str, participants: List[str]) -> Dict:
        """
        Promove participantes a administradores

        Args:
            group_id: ID do grupo
            participants: Lista de números a promover

        Returns:
            Resposta da API
        """
        endpoint = f"/group/updateParticipant/{self.instance_name}?groupJid={group_id}"
        data = {
            "action": "promote",
            "participants": participants
        }
        return self._make_request('POST', endpoint, data)

    def demote_participant(self, group_id: str, participants: List[str]) -> Dict:
        """
        Remove administração de participantes

        Args:
            group_id: ID do grupo
            participants: Lista de números a remover administração

        Returns:
            Resposta da API
        """
        endpoint = f"/group/updateParticipant/{self.instance_name}?groupJid={group_id}"
        data = {
            "action": "demote",
            "participants": participants
        }
        return self._make_request('POST', endpoint, data)

    def get_all_groups(self) -> Dict:
        """
        Obtém todos os grupos

        Returns:
            Lista de grupos
        """
        endpoint = f"/group/fetchAllGroups/{self.instance_name}"
        data = {"getParticipants": "true"}
        return self._make_request('GET', endpoint, data)

    def leave_group(self, group_id: str) -> Dict:
        """
        Sai do grupo

        Args:
            group_id: ID do grupo

        Returns:
            Resposta da API
        """
        endpoint = f"/group/leaveGroup/{self.instance_name}"
        data = {"groupJid": group_id}
        return self._make_request('DELETE', endpoint, data)

    def update_group_settings(self, group_id: str, setting: str) -> Dict:
        """
        Atualiza configurações do grupo

        Args:
            group_id: ID do grupo
            setting: Configuração a aplicar:
                - 'announcement': Apenas admins podem enviar mensagens
                - 'not_announcement': Todos podem enviar mensagens
                - 'locked': Apenas admins podem editar configurações
                - 'unlocked': Todos podem editar configurações

        Returns:
            Resposta da API
        """
        endpoint = f"/group/updateSetting/{self.instance_name}?groupJid={group_id}"
        data = {"action": setting}
        return self._make_request('POST', endpoint, data)

    # ==================== PERFIL ====================

    def update_profile_name(self, name: str) -> Dict:
        """
        Atualiza o nome do perfil

        Args:
            name: Novo nome

        Returns:
            Resposta da API
        """
        endpoint = f"/profile/updateProfileName/{self.instance_name}"
        data = {"name": name}
        return self._make_request('PUT', endpoint, data)

    def update_profile_status(self, status: str) -> Dict:
        """
        Atualiza o status do perfil

        Args:
            status: Novo status

        Returns:
            Resposta da API
        """
        endpoint = f"/profile/updateProfileStatus/{self.instance_name}"
        data = {"status": status}
        return self._make_request('PUT', endpoint, data)

    def update_profile_picture(self, image_url: str) -> Dict:
        """
        Atualiza a foto do perfil

        Args:
            image_url: URL da imagem ou caminho local

        Returns:
            Resposta da API
        """
        endpoint = f"/profile/updateProfilePicture/{self.instance_name}"

        # Se for um arquivo local, converte para base64
        if Path(image_url).exists():
            with open(image_url, 'rb') as f:
                image_base64 = base64.b64encode(f.read()).decode('utf-8')
                image_url = f"data:image/png;base64,{image_base64}"

        data = {"picture": image_url}
        return self._make_request('PUT', endpoint, data)

    def get_profile(self, number: Optional[str] = None) -> Dict:
        """
        Obtém informações do perfil

        Args:
            number: Número do perfil (se não informado, retorna o próprio perfil)

        Returns:
            Informações do perfil
        """
        endpoint = f"/profile/fetchProfile/{self.instance_name}"
        data = {"number": number} if number else {}
        return self._make_request('GET', endpoint, data)

    # ==================== CHATS E CONTATOS ====================

    def get_all_chats(self) -> Dict:
        """Obtém todos os chats"""
        endpoint = f"/chat/fetchAllChats/{self.instance_name}"
        return self._make_request('GET', endpoint)

    def get_all_contacts(self) -> Dict:
        """Obtém todos os contatos"""
        endpoint = f"/chat/fetchAllContacts/{self.instance_name}"
        return self._make_request('GET', endpoint)

    def check_number_exists(self, numbers: List[str]) -> Dict:
        """
        Verifica se números existem no WhatsApp

        Args:
            numbers: Lista de números a verificar

        Returns:
            Status dos números
        """
        endpoint = f"/chat/whatsappNumbers/{self.instance_name}"
        data = {"numbers": numbers}
        return self._make_request('POST', endpoint, data)

    def mark_message_as_read(self, number: str, message_id: str) -> Dict:
        """
        Marca mensagem como lida

        Args:
            number: Número do chat
            message_id: ID da mensagem

        Returns:
            Resposta da API
        """
        endpoint = f"/chat/markMessageAsRead/{self.instance_name}"
        data = {
            "readMessages": [{
                "remoteJid": number if '@' in number else f"{number}@s.whatsapp.net",
                "fromMe": False,
                "id": message_id
            }]
        }
        return self._make_request('POST', endpoint, data)

    def delete_message(self, number: str, message_id: str, delete_for_everyone: bool = False) -> Dict:
        """
        Deleta mensagem

        Args:
            number: Número do chat
            message_id: ID da mensagem
            delete_for_everyone: Se True, deleta para todos

        Returns:
            Resposta da API
        """
        endpoint = f"/chat/deleteMessageForEveryone/{self.instance_name}"
        data = {
            "id": message_id,
            "fromMe": True,
            "remoteJid": number if '@' in number else f"{number}@s.whatsapp.net"
        }
        return self._make_request('DELETE', endpoint, data)

    # ==================== WEBHOOKS ====================

    def set_webhook(self, webhook_url: str, events: List[str],
                    webhook_by_events: bool = False, webhook_base64: bool = False) -> Dict:
        """
        Configura webhook para a instância

        Args:
            webhook_url: URL que receberá os eventos
            events: Lista de eventos a monitorar
            webhook_by_events: Se True, cria URL específica para cada evento
            webhook_base64: Se True, envia mídias em base64

        Returns:
            Resposta da API
        """
        endpoint = f"/webhook/set/{self.instance_name}"
        data = {
            "url": webhook_url,
            "webhook_by_events": webhook_by_events,
            "webhook_base64": webhook_base64,
            "events": events
        }
        return self._make_request('POST', endpoint, data)

    def get_webhook(self) -> Dict:
        """Obtém configurações do webhook"""
        endpoint = f"/webhook/find/{self.instance_name}"
        return self._make_request('GET', endpoint)

    # ==================== UTILIDADES ====================

    def get_qrcode(self) -> Dict:
        """Obtém QR Code para conectar"""
        endpoint = f"/instance/connect/{self.instance_name}"
        return self._make_request('GET', endpoint)

    def format_phone_number(self, number: str) -> str:
        """
        Formata número de telefone para o padrão da API
        Remove todos os caracteres especiais e adiciona @s.whatsapp.net para grupos

        Args:
            number: Número a formatar

        Returns:
            Número formatado
        """
        # Remove todos os caracteres não numéricos
        number = ''.join(filter(str.isdigit, number))

        # Se for um ID de grupo, mantém o formato
        if '@g.us' in number or '@s.whatsapp.net' in number:
            return number

        # Adiciona @s.whatsapp.net se não tiver
        if '@' not in number:
            return f"{number}@s.whatsapp.net"

        return number
