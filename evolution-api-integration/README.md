# Evolution API - Integração WhatsApp

Módulo completo em Python para integração com a Evolution API, permitindo enviar mensagens, criar grupos e gerenciar todas as funcionalidades do WhatsApp via API.

## Configuração

### Credenciais
As credenciais já estão configuradas no arquivo `config.py`:

```python
EVOLUTION_API_URL = "https://evolution.loop9.com.br"
EVOLUTION_API_KEY = "178e43e1c4f459527e7008e57e378e1c"
EVOLUTION_INSTANCE_NAME = "lfimoveis"
```

### Instalação de Dependências

```bash
pip install requests
```

## Uso Básico

```python
from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME

# Inicializar a API
api = EvolutionAPI(
    base_url=EVOLUTION_API_URL,
    api_key=EVOLUTION_API_KEY,
    instance_name=EVOLUTION_INSTANCE_NAME
)

# Verificar status da instância
status = api.get_instance_status()
print(status)
```

## Funcionalidades Disponíveis

### 1. Gerenciamento de Instâncias

#### Verificar Status
```python
status = api.get_instance_status()
```

#### Obter QR Code (para conectar)
```python
qrcode = api.get_qrcode()
```

#### Desconectar
```python
api.logout_instance()
```

#### Deletar Instância
```python
api.delete_instance()
```

---

### 2. Envio de Mensagens

#### Mensagem de Texto
```python
response = api.send_text(
    number="5511999999999",  # Número com DDI e DDD (sem caracteres especiais)
    text="Olá! Esta é uma mensagem de teste.",
    delay=0  # Delay em milissegundos (opcional)
)
```

**Formatação de texto suportada:**
- Negrito: `*texto em negrito*`
- Itálico: `_texto em itálico_`
- Riscado: `~texto riscado~`
- Monoespaçado: `` `código` ``
- Emojis: ✅

#### Enviar Mídia (Imagem, Vídeo, Documento)
```python
# Usando URL
response = api.send_media(
    number="5511999999999",
    media_url="https://example.com/imagem.jpg",
    caption="Confira esta imagem!",
    media_type="image"  # image, video, document
)

# Usando arquivo local
response = api.send_media(
    number="5511999999999",
    media_url="/caminho/para/arquivo.pdf",
    caption="Documento anexo",
    media_type="document",
    filename="relatorio.pdf"  # Nome do arquivo
)
```

#### Enviar Áudio Narrado (PTT)
```python
response = api.send_audio(
    number="5511999999999",
    audio_url="https://example.com/audio.ogg"  # ou caminho local
)
```

#### Enviar Localização
```python
response = api.send_location(
    number="5511999999999",
    latitude=-23.550520,
    longitude=-46.633308,
    name="Av. Paulista",
    address="Avenida Paulista, São Paulo - SP"
)
```

#### Enviar Contato
```python
response = api.send_contact(
    number="5511999999999",
    contact_number="5511888888888",
    full_name="João Silva",
    organization="Empresa XYZ",
    email="joao@example.com"
)
```

#### Enviar Reação
```python
response = api.send_reaction(
    number="5511999999999",
    key="MESSAGE_ID_AQUI",  # ID da mensagem
    reaction="👍"  # Qualquer emoji
)
```

#### Responder Mensagem
```python
response = api.send_reply(
    number="5511999999999",
    text="Esta é uma resposta!",
    message_id="MESSAGE_ID_AQUI"
)
```

#### Enviar Menção (em Grupos)
```python
response = api.send_mention(
    group_id="120363123456789@g.us",
    text="Olá @5511999999999 e @5511888888888!",
    mentions=["5511999999999", "5511888888888"]  # Números a mencionar
)
```

#### Enviar Enquete
```python
response = api.send_poll(
    number="5511999999999",  # Pode ser grupo também
    name="Qual a melhor opção?",
    options=["Opção 1", "Opção 2", "Opção 3"],
    selectable_count=1  # Quantas opções podem ser selecionadas
)
```

#### Enviar Status/História
```python
# Status de texto
response = api.send_status(
    content="Meu status de texto",
    type="text",
    background_color="#FF5733"
)

# Status de mídia
response = api.send_status(
    content="https://example.com/imagem.jpg",
    type="image"
)
```

---

### 3. Gerenciamento de Grupos

#### Criar Grupo
```python
response = api.create_group(
    subject="Meu Grupo Teste",
    participants=["5511999999999", "5511888888888"],
    description="Descrição do grupo"
)
```

#### Atualizar Nome do Grupo
```python
response = api.update_group_name(
    group_id="120363123456789@g.us",
    subject="Novo Nome do Grupo"
)
```

#### Atualizar Descrição
```python
response = api.update_group_description(
    group_id="120363123456789@g.us",
    description="Nova descrição do grupo"
)
```

#### Atualizar Foto do Grupo
```python
response = api.update_group_picture(
    group_id="120363123456789@g.us",
    image_url="https://example.com/foto.jpg"  # ou caminho local
)
```

#### Adicionar Participantes
```python
response = api.add_participant(
    group_id="120363123456789@g.us",
    participants=["5511777777777", "5511666666666"]
)
```

#### Remover Participantes
```python
response = api.remove_participant(
    group_id="120363123456789@g.us",
    participants=["5511777777777"]
)
```

#### Promover a Administrador
```python
response = api.promote_participant(
    group_id="120363123456789@g.us",
    participants=["5511777777777"]
)
```

#### Remover Administração
```python
response = api.demote_participant(
    group_id="120363123456789@g.us",
    participants=["5511777777777"]
)
```

#### Listar Todos os Grupos
```python
groups = api.get_all_groups()

for group in groups:
    print(f"Grupo: {group['subject']}")
    print(f"ID: {group['id']}")
    print(f"Participantes: {len(group['participants'])}")
```

#### Sair do Grupo
```python
response = api.leave_group(group_id="120363123456789@g.us")
```

#### Atualizar Configurações do Grupo
```python
# Configurar para apenas admins enviarem mensagens
response = api.update_group_settings(
    group_id="120363123456789@g.us",
    setting="announcement"  # Apenas admins enviam mensagens
)

# Permitir que todos enviem mensagens
response = api.update_group_settings(
    group_id="120363123456789@g.us",
    setting="not_announcement"  # Todos podem enviar
)

# Configurações disponíveis:
# - 'announcement': Apenas admins podem enviar mensagens
# - 'not_announcement': Todos podem enviar mensagens
# - 'locked': Apenas admins podem editar configurações do grupo
# - 'unlocked': Todos podem editar configurações do grupo
```

---

### 4. Perfil

#### Atualizar Nome do Perfil
```python
response = api.update_profile_name("Meu Novo Nome")
```

#### Atualizar Status do Perfil
```python
response = api.update_profile_status("Disponível")
```

#### Atualizar Foto do Perfil
```python
response = api.update_profile_picture("https://example.com/foto.jpg")
```

#### Obter Informações do Perfil
```python
# Seu próprio perfil
profile = api.get_profile()

# Perfil de outro usuário
profile = api.get_profile(number="5511999999999")
```

---

### 5. Chats e Contatos

#### Obter Todos os Chats
```python
chats = api.get_all_chats()
```

#### Obter Todos os Contatos
```python
contacts = api.get_all_contacts()
```

#### Verificar se Números Existem no WhatsApp
```python
result = api.check_number_exists(
    numbers=["5511999999999", "5511888888888"]
)
```

#### Marcar Mensagem como Lida
```python
response = api.mark_message_as_read(
    number="5511999999999",
    message_id="MESSAGE_ID_AQUI"
)
```

#### Deletar Mensagem
```python
# Deletar para todos
response = api.delete_message(
    number="5511999999999",
    message_id="MESSAGE_ID_AQUI",
    delete_for_everyone=True
)
```

---

### 6. Webhooks

#### Configurar Webhook
```python
response = api.set_webhook(
    webhook_url="https://meusite.com/webhook",
    events=[
        "MESSAGES_UPSERT",      # Mensagens recebidas
        "MESSAGES_UPDATE",      # Mensagens atualizadas
        "MESSAGES_DELETE",      # Mensagens deletadas
        "SEND_MESSAGE",         # Mensagens enviadas
        "CONNECTION_UPDATE",    # Atualização de conexão
        "QRCODE_UPDATED",       # QR Code atualizado
        "GROUPS_UPSERT",        # Grupos criados
        "GROUPS_UPDATE",        # Grupos atualizados
        "GROUP_PARTICIPANTS_UPDATE"  # Participantes atualizados
    ],
    webhook_by_events=False,  # Se True, cria URL específica para cada evento
    webhook_base64=False      # Se True, envia mídias em base64
)
```

#### Obter Configurações do Webhook
```python
webhook_config = api.get_webhook()
```

#### Eventos Disponíveis
- `APPLICATION_STARTUP` - Inicialização da aplicação
- `QRCODE_UPDATED` - QR Code atualizado
- `CONNECTION_UPDATE` - Status de conexão
- `MESSAGES_SET` - Mensagens carregadas
- `MESSAGES_UPSERT` - Mensagens recebidas
- `MESSAGES_UPDATE` - Mensagens atualizadas
- `MESSAGES_DELETE` - Mensagens deletadas
- `SEND_MESSAGE` - Mensagens enviadas
- `CONTACTS_SET` - Contatos carregados
- `CONTACTS_UPSERT` - Contatos criados
- `CONTACTS_UPDATE` - Contatos atualizados
- `PRESENCE_UPDATE` - Presença atualizada (digitando, gravando)
- `CHATS_SET` - Chats carregados
- `CHATS_UPSERT` - Chats criados
- `CHATS_UPDATE` - Chats atualizados
- `CHATS_DELETE` - Chats deletados
- `GROUPS_UPSERT` - Grupos criados
- `GROUPS_UPDATE` - Grupos atualizados
- `GROUP_PARTICIPANTS_UPDATE` - Participantes atualizados
- `CALL` - Chamadas
- `NEW_TOKEN` - Token JWT atualizado

---

## Formato de Números

### Números Individuais
- Formato: `DDI + DDD + NÚMERO` (sem caracteres especiais)
- Exemplo: `5511999999999`
- A API adiciona automaticamente `@s.whatsapp.net`

### IDs de Grupos
- Formato: `NUMERO@g.us`
- Exemplo: `120363123456789@g.us`
- Você obtém este ID ao criar o grupo ou listá-los

---

## Exemplos Práticos

### Exemplo 1: Enviar Mensagem Simples
```python
from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME

api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

# Enviar mensagem
response = api.send_text(
    number="5511999999999",
    text="Olá! Como você está?"
)

print(f"Mensagem enviada: {response}")
```

### Exemplo 2: Criar Grupo e Enviar Mensagem
```python
# Criar grupo
group = api.create_group(
    subject="Grupo de Vendas",
    participants=["5511999999999", "5511888888888"],
    description="Grupo para discutir vendas"
)

group_id = group['id']

# Enviar mensagem no grupo
api.send_text(
    number=group_id,
    text="Bem-vindos ao grupo de vendas!"
)

# Enviar mensagem mencionando todos
api.send_mention(
    group_id=group_id,
    text="@5511999999999 e @5511888888888, confiram as novidades!",
    mentions=["5511999999999", "5511888888888"]
)
```

### Exemplo 3: Enviar Mídia com Legenda
```python
# Enviar imagem
api.send_media(
    number="5511999999999",
    media_url="https://example.com/produto.jpg",
    caption="*Produto em Promoção!*\n\nApenas R$ 99,90\nGaranta o seu!",
    media_type="image"
)
```

### Exemplo 4: Enviar Localização de Endereço
```python
api.send_location(
    number="5511999999999",
    latitude=-23.561684,
    longitude=-46.655981,
    name="Shopping Ibirapuera",
    address="Av. Ibirapuera, 3103 - São Paulo"
)
```

### Exemplo 5: Criar Enquete
```python
api.send_poll(
    number="120363123456789@g.us",  # ID do grupo
    name="Melhor dia para reunião?",
    options=["Segunda", "Terça", "Quarta", "Quinta", "Sexta"],
    selectable_count=1
)
```

---

## Tratamento de Erros

```python
try:
    response = api.send_text(
        number="5511999999999",
        text="Teste"
    )
    print("Sucesso:", response)
except requests.exceptions.RequestException as e:
    print(f"Erro ao enviar mensagem: {e}")
```

---

## Arquivo de Teste

Execute o arquivo `examples.py` para ver todos os exemplos:

```bash
python3 examples.py
```

---

## Estrutura do Projeto

```
evolution-api-integration/
├── evolution_api.py    # Módulo principal com a classe EvolutionAPI
├── config.py           # Configurações (URL, API Key, Instância)
├── examples.py         # Exemplos de uso
└── README.md           # Esta documentação
```

---

## Documentação Oficial

Para mais informações, consulte a documentação oficial:
- https://doc.evolution-api.com

---

## Notas Importantes

1. **Números de Telefone**: Sempre use o formato internacional completo (DDI + DDD + Número) sem caracteres especiais
2. **IDs de Mensagens**: São retornados nas respostas da API quando você envia mensagens
3. **IDs de Grupos**: Use o formato `NUMERO@g.us`
4. **Arquivos Locais**: O módulo converte automaticamente arquivos locais para base64
5. **Rate Limiting**: Respeite os limites de envio do WhatsApp para evitar banimento
6. **Webhooks**: Configure webhooks para receber eventos em tempo real

---

## Suporte

Em caso de dúvidas ou problemas:
1. Verifique se a instância está conectada: `api.get_instance_status()`
2. Verifique os logs da API Evolution
3. Consulte a documentação oficial
4. Teste os exemplos fornecidos

---

Desenvolvido para facilitar a integração com a Evolution API.
