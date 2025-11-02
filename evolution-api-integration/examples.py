"""
Exemplos de uso da Evolution API
"""

from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME


def main():
    # Inicializa a API
    api = EvolutionAPI(
        base_url=EVOLUTION_API_URL,
        api_key=EVOLUTION_API_KEY,
        instance_name=EVOLUTION_INSTANCE_NAME
    )

    print("=" * 60)
    print("EVOLUTION API - EXEMPLOS DE USO")
    print("=" * 60)

    # ==================== VERIFICAR STATUS ====================
    print("\n1. Verificando status da instância...")
    try:
        status = api.get_instance_status()
        print(f"Status: {status}")
    except Exception as e:
        print(f"Erro ao verificar status: {e}")

    # ==================== ENVIAR MENSAGEM DE TEXTO ====================
    print("\n2. Exemplo de envio de mensagem de texto:")
    print("""
    # Enviar mensagem simples
    response = api.send_text(
        number="5511999999999",  # Número com DDI e DDD
        text="Olá! Esta é uma mensagem de teste."
    )
    """)

    # ==================== ENVIAR MÍDIA ====================
    print("\n3. Exemplo de envio de mídia (imagem):")
    print("""
    # Enviar imagem com legenda
    response = api.send_media(
        number="5511999999999",
        media_url="https://example.com/imagem.jpg",  # ou caminho local
        caption="Confira esta imagem!",
        media_type="image"
    )
    """)

    # ==================== ENVIAR ÁUDIO ====================
    print("\n4. Exemplo de envio de áudio:")
    print("""
    # Enviar áudio narrado (PTT)
    response = api.send_audio(
        number="5511999999999",
        audio_url="https://example.com/audio.ogg"  # ou caminho local
    )
    """)

    # ==================== ENVIAR LOCALIZAÇÃO ====================
    print("\n5. Exemplo de envio de localização:")
    print("""
    # Enviar localização
    response = api.send_location(
        number="5511999999999",
        latitude=-23.550520,
        longitude=-46.633308,
        name="Av. Paulista",
        address="Avenida Paulista, São Paulo - SP"
    )
    """)

    # ==================== ENVIAR CONTATO ====================
    print("\n6. Exemplo de envio de contato:")
    print("""
    # Enviar contato
    response = api.send_contact(
        number="5511999999999",
        contact_number="5511888888888",
        full_name="João Silva",
        organization="Empresa XYZ",
        email="joao@example.com"
    )
    """)

    # ==================== ENVIAR REAÇÃO ====================
    print("\n7. Exemplo de envio de reação:")
    print("""
    # Enviar reação a uma mensagem
    response = api.send_reaction(
        number="5511999999999",
        key="MESSAGE_ID_AQUI",  # ID da mensagem a reagir
        reaction="👍"  # Emoji da reação
    )
    """)

    # ==================== RESPONDER MENSAGEM ====================
    print("\n8. Exemplo de resposta a mensagem:")
    print("""
    # Responder uma mensagem
    response = api.send_reply(
        number="5511999999999",
        text="Esta é uma resposta!",
        message_id="MESSAGE_ID_AQUI"  # ID da mensagem a responder
    )
    """)

    # ==================== ENVIAR MENÇÃO ====================
    print("\n9. Exemplo de envio de menção em grupo:")
    print("""
    # Enviar mensagem com menções
    response = api.send_mention(
        group_id="120363123456789@g.us",  # ID do grupo
        text="Olá @5511999999999 e @5511888888888!",
        mentions=["5511999999999", "5511888888888"]
    )
    """)

    # ==================== ENVIAR ENQUETE ====================
    print("\n10. Exemplo de envio de enquete:")
    print("""
    # Enviar enquete
    response = api.send_poll(
        number="5511999999999",  # ou ID do grupo
        name="Qual a melhor opção?",
        options=["Opção 1", "Opção 2", "Opção 3"],
        selectable_count=1  # Quantas opções podem ser selecionadas
    )
    """)

    # ==================== CRIAR GRUPO ====================
    print("\n11. Exemplo de criação de grupo:")
    print("""
    # Criar novo grupo
    response = api.create_group(
        subject="Meu Grupo Teste",
        participants=["5511999999999", "5511888888888"],
        description="Descrição do grupo"
    )
    """)

    # ==================== GERENCIAR GRUPO ====================
    print("\n12. Exemplo de gerenciamento de grupo:")
    print("""
    # Atualizar nome do grupo
    api.update_group_name(
        group_id="120363123456789@g.us",
        subject="Novo Nome do Grupo"
    )

    # Atualizar descrição do grupo
    api.update_group_description(
        group_id="120363123456789@g.us",
        description="Nova descrição do grupo"
    )

    # Atualizar foto do grupo
    api.update_group_picture(
        group_id="120363123456789@g.us",
        image_url="https://example.com/foto.jpg"  # ou caminho local
    )

    # Adicionar participantes
    api.add_participant(
        group_id="120363123456789@g.us",
        participants=["5511777777777"]
    )

    # Promover a administrador
    api.promote_participant(
        group_id="120363123456789@g.us",
        participants=["5511777777777"]
    )

    # Remover administração
    api.demote_participant(
        group_id="120363123456789@g.us",
        participants=["5511777777777"]
    )

    # Remover participante
    api.remove_participant(
        group_id="120363123456789@g.us",
        participants=["5511777777777"]
    )
    """)

    # ==================== LISTAR GRUPOS ====================
    print("\n13. Exemplo de listagem de grupos:")
    print("""
    # Obter todos os grupos
    groups = api.get_all_groups()
    for group in groups:
        print(f"Grupo: {group['subject']}")
        print(f"ID: {group['id']}")
        print(f"Participantes: {len(group['participants'])}")
    """)

    # ==================== PERFIL ====================
    print("\n14. Exemplo de atualização de perfil:")
    print("""
    # Atualizar nome do perfil
    api.update_profile_name("Meu Novo Nome")

    # Atualizar status do perfil
    api.update_profile_status("Disponível")

    # Atualizar foto do perfil
    api.update_profile_picture("https://example.com/foto.jpg")

    # Obter informações do perfil
    profile = api.get_profile()
    print(profile)
    """)

    # ==================== CHATS E CONTATOS ====================
    print("\n15. Exemplo de obtenção de chats e contatos:")
    print("""
    # Obter todos os chats
    chats = api.get_all_chats()

    # Obter todos os contatos
    contacts = api.get_all_contacts()

    # Verificar se números existem no WhatsApp
    result = api.check_number_exists(["5511999999999", "5511888888888"])
    """)

    # ==================== MARCAR MENSAGEM COMO LIDA ====================
    print("\n16. Exemplo de marcar mensagem como lida:")
    print("""
    # Marcar mensagem como lida
    api.mark_message_as_read(
        number="5511999999999",
        message_id="MESSAGE_ID_AQUI"
    )
    """)

    # ==================== DELETAR MENSAGEM ====================
    print("\n17. Exemplo de deletar mensagem:")
    print("""
    # Deletar mensagem para todos
    api.delete_message(
        number="5511999999999",
        message_id="MESSAGE_ID_AQUI",
        delete_for_everyone=True
    )
    """)

    # ==================== WEBHOOKS ====================
    print("\n18. Exemplo de configuração de webhook:")
    print("""
    # Configurar webhook
    api.set_webhook(
        webhook_url="https://meusite.com/webhook",
        events=[
            "MESSAGES_UPSERT",  # Mensagens recebidas
            "MESSAGES_UPDATE",  # Mensagens atualizadas
            "SEND_MESSAGE",     # Mensagens enviadas
            "CONNECTION_UPDATE" # Atualização de conexão
        ],
        webhook_by_events=False,
        webhook_base64=False
    )

    # Obter configurações do webhook
    webhook_config = api.get_webhook()
    print(webhook_config)
    """)

    print("\n" + "=" * 60)
    print("FIM DOS EXEMPLOS")
    print("=" * 60)


if __name__ == "__main__":
    main()
