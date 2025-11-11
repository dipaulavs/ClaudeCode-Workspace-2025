"""
Helper principal para usar a Evolution API de forma simplificada
"""

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME
from typing import List, Optional


class WhatsAppHelper:
    """
    Classe helper que facilita o uso da Evolution API
    com métodos simplificados e validações
    """

    def __init__(self):
        """Inicializa o helper"""
        self.api = EvolutionAPI(
            base_url=EVOLUTION_API_URL,
            api_key=EVOLUTION_API_KEY,
            instance_name=EVOLUTION_INSTANCE_NAME
        )

    def send_message(self, number: str, message: str) -> dict:
        """
        Envia uma mensagem de texto simples

        Args:
            number: Número do destinatário (ex: 5511999999999)
            message: Texto da mensagem

        Returns:
            Resposta da API
        """
        try:
            response = self.api.send_text(number=number, text=message)
            print(f"✅ Mensagem enviada para {number}")
            return response
        except Exception as e:
            print(f"❌ Erro ao enviar mensagem: {e}")
            raise

    def send_image(self, number: str, image_url: str, caption: str = "") -> dict:
        """
        Envia uma imagem

        Args:
            number: Número do destinatário
            image_url: URL ou caminho da imagem
            caption: Legenda da imagem

        Returns:
            Resposta da API
        """
        try:
            response = self.api.send_media(
                number=number,
                media_url=image_url,
                caption=caption,
                media_type="image"
            )
            print(f"✅ Imagem enviada para {number}")
            return response
        except Exception as e:
            print(f"❌ Erro ao enviar imagem: {e}")
            raise

    def send_video(self, number: str, video_url: str, caption: str = "") -> dict:
        """
        Envia um vídeo

        Args:
            number: Número do destinatário
            video_url: URL ou caminho do vídeo
            caption: Legenda do vídeo

        Returns:
            Resposta da API
        """
        try:
            response = self.api.send_media(
                number=number,
                media_url=video_url,
                caption=caption,
                media_type="video"
            )
            print(f"✅ Vídeo enviado para {number}")
            return response
        except Exception as e:
            print(f"❌ Erro ao enviar vídeo: {e}")
            raise

    def send_document(self, number: str, document_url: str,
                      filename: str, caption: str = "") -> dict:
        """
        Envia um documento

        Args:
            number: Número do destinatário
            document_url: URL ou caminho do documento
            filename: Nome do arquivo
            caption: Legenda do documento

        Returns:
            Resposta da API
        """
        try:
            response = self.api.send_media(
                number=number,
                media_url=document_url,
                caption=caption,
                media_type="document",
                filename=filename
            )
            print(f"✅ Documento enviado para {number}")
            return response
        except Exception as e:
            print(f"❌ Erro ao enviar documento: {e}")
            raise

    def create_group(self, name: str, participants: List[str],
                     description: str = "") -> dict:
        """
        Cria um novo grupo

        Args:
            name: Nome do grupo
            participants: Lista de números dos participantes
            description: Descrição do grupo

        Returns:
            Informações do grupo criado
        """
        try:
            response = self.api.create_group(
                subject=name,
                participants=participants,
                description=description
            )
            print(f"✅ Grupo '{name}' criado com sucesso!")
            print(f"   ID do grupo: {response.get('id', 'N/A')}")
            return response
        except Exception as e:
            print(f"❌ Erro ao criar grupo: {e}")
            raise

    def send_group_message(self, group_id: str, message: str) -> dict:
        """
        Envia mensagem em um grupo

        Args:
            group_id: ID do grupo (ex: 120363123456789@g.us)
            message: Texto da mensagem

        Returns:
            Resposta da API
        """
        try:
            response = self.api.send_text(number=group_id, text=message)
            print(f"✅ Mensagem enviada no grupo")
            return response
        except Exception as e:
            print(f"❌ Erro ao enviar mensagem no grupo: {e}")
            raise

    def mention_in_group(self, group_id: str, message: str,
                         mentions: List[str]) -> dict:
        """
        Envia mensagem mencionando pessoas no grupo

        Args:
            group_id: ID do grupo
            message: Texto da mensagem
            mentions: Lista de números a mencionar

        Returns:
            Resposta da API
        """
        try:
            response = self.api.send_mention(
                group_id=group_id,
                text=message,
                mentions=mentions
            )
            print(f"✅ Mensagem com menções enviada no grupo")
            return response
        except Exception as e:
            print(f"❌ Erro ao enviar mensagem com menções: {e}")
            raise

    def add_to_group(self, group_id: str, participants: List[str]) -> dict:
        """
        Adiciona pessoas ao grupo

        Args:
            group_id: ID do grupo
            participants: Lista de números a adicionar

        Returns:
            Resposta da API
        """
        try:
            response = self.api.add_participant(
                group_id=group_id,
                participants=participants
            )
            print(f"✅ Participantes adicionados ao grupo")
            return response
        except Exception as e:
            print(f"❌ Erro ao adicionar participantes: {e}")
            raise

    def remove_from_group(self, group_id: str, participants: List[str]) -> dict:
        """
        Remove pessoas do grupo

        Args:
            group_id: ID do grupo
            participants: Lista de números a remover

        Returns:
            Resposta da API
        """
        try:
            response = self.api.remove_participant(
                group_id=group_id,
                participants=participants
            )
            print(f"✅ Participantes removidos do grupo")
            return response
        except Exception as e:
            print(f"❌ Erro ao remover participantes: {e}")
            raise

    def make_admin(self, group_id: str, participants: List[str]) -> dict:
        """
        Promove pessoas a administradores do grupo

        Args:
            group_id: ID do grupo
            participants: Lista de números a promover

        Returns:
            Resposta da API
        """
        try:
            response = self.api.promote_participant(
                group_id=group_id,
                participants=participants
            )
            print(f"✅ Participantes promovidos a administradores")
            return response
        except Exception as e:
            print(f"❌ Erro ao promover participantes: {e}")
            raise

    def send_location(self, number: str, latitude: float, longitude: float,
                      name: str = "", address: str = "") -> dict:
        """
        Envia localização

        Args:
            number: Número do destinatário
            latitude: Latitude
            longitude: Longitude
            name: Nome do local
            address: Endereço

        Returns:
            Resposta da API
        """
        try:
            response = self.api.send_location(
                number=number,
                latitude=latitude,
                longitude=longitude,
                name=name,
                address=address
            )
            print(f"✅ Localização enviada para {number}")
            return response
        except Exception as e:
            print(f"❌ Erro ao enviar localização: {e}")
            raise

    def create_poll(self, number: str, question: str,
                    options: List[str], multiple_choice: bool = False) -> dict:
        """
        Cria uma enquete

        Args:
            number: Número ou ID do grupo
            question: Pergunta da enquete
            options: Lista de opções
            multiple_choice: Se permite múltipla escolha

        Returns:
            Resposta da API
        """
        try:
            selectable_count = len(options) if multiple_choice else 1
            response = self.api.send_poll(
                number=number,
                name=question,
                options=options,
                selectable_count=selectable_count
            )
            print(f"✅ Enquete criada")
            return response
        except Exception as e:
            print(f"❌ Erro ao criar enquete: {e}")
            raise

    def get_groups(self) -> List[dict]:
        """
        Lista todos os grupos

        Returns:
            Lista de grupos
        """
        try:
            response = self.api.get_all_groups()
            groups = response.get('groups', [])
            print(f"✅ {len(groups)} grupos encontrados")
            return groups
        except Exception as e:
            print(f"❌ Erro ao listar grupos: {e}")
            raise

    def check_status(self) -> dict:
        """
        Verifica o status da conexão

        Returns:
            Status da instância
        """
        try:
            status = self.api.get_instance_status()
            state = status.get('state', 'Desconhecido')
            print(f"✅ Status da instância: {state}")
            return status
        except Exception as e:
            print(f"❌ Erro ao verificar status: {e}")
            raise

    def format_number(self, number: str) -> str:
        """
        Formata número para o padrão correto

        Args:
            number: Número a formatar

        Returns:
            Número formatado
        """
        # Remove caracteres especiais
        number = ''.join(filter(str.isdigit, number))

        # Adiciona DDI 55 se não tiver
        if not number.startswith('55'):
            number = '55' + number

        return number


# Instância global para facilitar o uso
whatsapp = WhatsAppHelper()


if __name__ == "__main__":
    # Teste básico
    print("=" * 60)
    print("WHATSAPP HELPER - TESTE")
    print("=" * 60)

    # Verifica status
    whatsapp.check_status()

    print("\n" + "=" * 60)
    print("Helper inicializado com sucesso!")
    print("=" * 60)
    print("\nExemplos de uso:")
    print("\n1. Enviar mensagem:")
    print('   whatsapp.send_message("5511999999999", "Olá!")')
    print("\n2. Criar grupo:")
    print('   whatsapp.create_group("Meu Grupo", ["5511999999999", "5511888888888"])')
    print("\n3. Listar grupos:")
    print('   grupos = whatsapp.get_groups()')
