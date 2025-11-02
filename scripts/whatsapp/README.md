# 📱 WhatsApp Templates - Evolution API

Scripts prontos para operações WhatsApp via Evolution API.

**Status:** ✅ **22 templates criados - 19 funcionais**

---

## 📊 Visão Geral

| Categoria | Templates | Status |
|-----------|-----------|--------|
| **MENSAGENS** | 10 templates | 9 funcionais, 1 aguarda áudio |
| **GRUPOS** | 5 templates | 5 funcionais |
| **PERFIL E CONTATOS** | 4 templates | 1 funcional, 3 indisponíveis (API v2.3.4) |
| **AÇÕES** | 1 template | 1 funcional |
| **SISTEMA** | 2 templates | 2 funcionais |
| **TOTAL** | **22 templates** | **19 funcionais** |

---

## 📋 Índice de Templates

- [MENSAGENS (10 templates)](#-mensagens-10-templates)
  - [1. send_message.py](#1-send_messagepy---enviar-mensagem)
  - [2. send_media.py](#2-send_mediapy---enviar-mídia)
  - [3. send_poll.py](#3-send_pollpy---enviar-enquete)
  - [4. send_audio.py](#4-send_audiopy---enviar-áudio-ptt)
  - [5. send_location.py](#5-send_locationpy---enviar-localização)
  - [6. send_contact.py](#6-send_contactpy---enviar-contato)
  - [7. send_reaction.py](#7-send_reactionpy---reagir-a-mensagem)
  - [8. send_reply.py](#8-send_replypy---responder-mensagem)
  - [9. send_mention.py](#9-send_mentionpy---mencionar-em-grupo)
  - [10. send_status.py](#10-send_statuspy---postar-storystatus)
- [GRUPOS (5 templates)](#-grupos-5-templates)
  - [11. create_group.py](#11-create_grouppy---criar-grupo)
  - [12. update_group.py](#12-update_grouppy---atualizar-grupo)
  - [13. manage_participants.py](#13-manage_participantspy---gerenciar-participantes)
  - [14. list_groups.py](#14-list_groupspy---listar-grupos)
  - [15. leave_group.py](#15-leave_grouppy---sair-do-grupo)
- [PERFIL E CONTATOS (4 templates)](#-perfil-e-contatos-4-templates)
  - [16-18. Perfil e Contatos](#16-18-manage_profilepy-get_profilepy-get_contactspy)
  - [19. check_number.py](#19-check_numberpy---verificar-número)
- [AÇÕES (1 template)](#-ações-1-template)
  - [20. message_actions.py](#20-message_actionspy---ações-em-mensagens)
- [SISTEMA (2 templates)](#-sistema-2-templates)
  - [21. instance_info.py](#21-instance_infopy---informações-da-instância)
  - [22. manage_webhooks.py](#22-manage_webhookspy---gerenciar-webhooks)

---

## 📱 MENSAGENS (10 templates)

### 1. send_message.py - Enviar Mensagem

Envia mensagens de texto via WhatsApp.

**Status:** ✅ Funcional

#### Uso:
```bash
# Mensagem simples
python3 scripts/whatsapp/send_message.py --phone 5531980160822 --message "Olá!"

# Mensagem com formatação
python3 scripts/whatsapp/send_message.py --phone 5531980160822 --message "*Negrito* _Itálico_ ~Riscado~"

# Mensagem com delay
python3 scripts/whatsapp/send_message.py --phone 5531980160822 --message "Teste" --delay 1000
```

#### Parâmetros:
- `--phone`, `-p` (obrigatório): Número com DDI (ex: 5531980160822)
- `--message`, `-m` (obrigatório): Texto da mensagem
- `--delay`, `-d` (opcional): Delay em milissegundos (padrão: 0)

#### Formatação suportada:
- `*texto*` → **Negrito**
- `_texto_` → *Itálico*
- `~texto~` → ~~Riscado~~
- `` `código` `` → `Monoespaçado`
- Emojis ✅

---

### 2. send_media.py - Enviar Mídia

Envia imagens, vídeos, documentos e áudios via WhatsApp.

**Status:** ✅ Funcional

🚨 **IMPORTANTE:** Evolution API aceita APENAS URLs públicas. A opção `--file` foi removida.

✨ **NOVO:** Detecção automática do tipo de mídia pela extensão da URL (--type é opcional).

#### Uso:
```bash
# Enviar imagem via URL (tipo detectado automaticamente)
python3 scripts/whatsapp/send_media.py \
  --phone 5531980160822 \
  --url "https://exemplo.com/imagem.jpg" \
  --caption "Veja isso!"

# Enviar vídeo (tipo detectado automaticamente)
python3 scripts/whatsapp/send_media.py \
  --phone 5531980160822 \
  --url "https://tempfile.aiquickdraw.com/workers/video_xxx.mp4" \
  --caption "Novo vídeo!"

# Enviar documento com nome customizado
python3 scripts/whatsapp/send_media.py \
  --phone 5531980160822 \
  --url "https://exemplo.com/relatorio.pdf" \
  --filename "Relatório 2025.pdf"

# Especificar tipo manualmente (opcional)
python3 scripts/whatsapp/send_media.py \
  --phone 5531980160822 \
  --url "https://exemplo.com/arquivo_sem_extensao" \
  --type image
```

#### Parâmetros:
- `--phone`, `-p` (obrigatório): Número com DDI
- `--url`, `-u` (obrigatório): URL PÚBLICA da mídia (http:// ou https://)
- `--type`, `-t` (opcional): Tipo de mídia (`image`, `video`, `document`, `audio`) - detectado automaticamente pela extensão
- `--caption`, `-c` (opcional): Legenda da mídia
- `--filename`, `-f` (opcional): Nome do arquivo (para documentos)

#### Tipos suportados:
- `image` - Imagens (JPG, PNG, GIF)
- `video` - Vídeos (MP4, AVI)
- `document` - Documentos (PDF, DOC, TXT, etc)
- `audio` - Áudios (MP3, OGG)

---

### 3. send_poll.py - Enviar Enquete

Envia enquetes/votações via WhatsApp.

**Status:** ✅ Funcional

#### Uso:
```bash
# Enquete simples para contato
python3 scripts/whatsapp/send_poll.py \
  --phone 5531980160822 \
  --question "Melhor dia para reunião?" \
  --options "Segunda,Terça,Quarta,Quinta,Sexta"

# Enquete em grupo
python3 scripts/whatsapp/send_poll.py \
  --group 120363423739033485@g.us \
  --question "Pizza ou Hamburguer?" \
  --options "Pizza,Hamburguer"

# Enquete com seleção múltipla
python3 scripts/whatsapp/send_poll.py \
  --phone 5531980160822 \
  --question "Quais toppings você gosta?" \
  --options "Pepperoni,Cogumelos,Azeitonas,Queijo Extra" \
  --multiple
```

#### Parâmetros:
- `--phone`, `-p` OU `--group`, `-g` (obrigatório): Número ou ID do grupo
- `--question`, `-q` (obrigatório): Pergunta da enquete
- `--options`, `-o` (obrigatório): Opções separadas por vírgula
- `--multiple`, `-m` (opcional): Permitir seleção múltipla

#### Notas:
- Máximo de 12 opções por enquete
- Para grupos, use o formato: `120363123456789@g.us`

---

### 4. send_audio.py - Enviar Áudio PTT

Envia áudio no formato PTT (Push To Talk) via WhatsApp.

**Status:** ⚠️ Estrutura pronta, aguarda áudio válido OGG

#### Uso:
```bash
# Enviar áudio via URL
python3 scripts/whatsapp/send_audio.py --phone 5531980160822 --audio https://example.com/audio.ogg

# Enviar áudio local
python3 scripts/whatsapp/send_audio.py --phone 5531980160822 --audio /path/to/audio.ogg
```

#### Parâmetros:
- `--phone`, `-p` (obrigatório): Número com DDI (ex: 5531980160822)
- `--audio`, `-a` (obrigatório): URL do áudio ou caminho local

#### Notas:
- Formato recomendado: OGG Opus
- Para converter MP3 para OGG: `ffmpeg -i audio.mp3 -c:a libopus audio.ogg`
- Funcionalidade testada com estrutura validada, necessita áudio OGG válido

---

### 5. send_location.py - Enviar Localização

Envia localização geográfica via WhatsApp.

**Status:** ✅ Funcional

#### Uso:
```bash
# Enviar localização com nome
python3 scripts/whatsapp/send_location.py \
  --phone 5531980160822 \
  --lat -19.9167 \
  --lon -43.9345 \
  --name "Praça da Liberdade" \
  --address "Belo Horizonte, MG"

# Enviar apenas coordenadas
python3 scripts/whatsapp/send_location.py \
  --phone 5531980160822 \
  --lat -23.5505 \
  --lon -46.6333
```

#### Parâmetros:
- `--phone`, `-p` (obrigatório): Número com DDI (ex: 5531980160822)
- `--lat` (obrigatório): Latitude
- `--lon` (obrigatório): Longitude
- `--name`, `-n` (opcional): Nome do local
- `--address`, `-a` (opcional): Endereço do local

#### Notas:
- Coordenadas devem usar ponto decimal (ex: -19.9167)
- Nome e endereço são opcionais mas recomendados

---

### 6. send_contact.py - Enviar Contato

Envia contato (vCard) via WhatsApp.

**Status:** ✅ Funcional

#### Uso:
```bash
# Enviar contato completo
python3 scripts/whatsapp/send_contact.py \
  --phone 5531980160822 \
  --contact-number 5511999999999 \
  --name "João Silva" \
  --organization "Empresa XYZ" \
  --email "joao@example.com"

# Enviar contato simples
python3 scripts/whatsapp/send_contact.py \
  --phone 5531980160822 \
  --contact-number 5511999999999 \
  --name "Maria Santos"
```

#### Parâmetros:
- `--phone`, `-p` (obrigatório): Número destinatário com DDI
- `--contact-number`, `-c` (obrigatório): Número do contato a enviar
- `--name`, `-n` (obrigatório): Nome completo do contato
- `--organization`, `-o` (opcional): Empresa/Organização
- `--email`, `-e` (opcional): E-mail do contato

---

### 7. send_reaction.py - Reagir a Mensagem

Reage a uma mensagem com emoji via WhatsApp.

**Status:** ✅ Funcional

#### Uso:
```bash
# Reagir com curtida
python3 scripts/whatsapp/send_reaction.py \
  --phone 5531980160822 \
  --message-id "ABC123XYZ" \
  --emoji "👍"

# Reagir com coração
python3 scripts/whatsapp/send_reaction.py \
  --phone 5531980160822 \
  --message-id "ABC123XYZ" \
  --emoji "❤️"
```

#### Parâmetros:
- `--phone`, `-p` (obrigatório): Número com DDI
- `--message-id`, `-m` (obrigatório): ID da mensagem a reagir
- `--emoji`, `-e` (obrigatório): Emoji da reação (ex: 👍, ❤️, 😂)

#### Notas:
- O message-id é retornado ao enviar mensagens
- Para remover reação, envie emoji vazio

---

### 8. send_reply.py - Responder Mensagem

Responde uma mensagem (reply/quote) via WhatsApp.

**Status:** ✅ Funcional

#### Uso:
```bash
# Responder mensagem
python3 scripts/whatsapp/send_reply.py \
  --phone 5531980160822 \
  --message-id "ABC123XYZ" \
  --text "Esta é minha resposta!"

# Responder com agradecimento
python3 scripts/whatsapp/send_reply.py \
  --phone 5531980160822 \
  --message-id "ABC123XYZ" \
  --text "Obrigado pela mensagem!"
```

#### Parâmetros:
- `--phone`, `-p` (obrigatório): Número com DDI
- `--message-id`, `-m` (obrigatório): ID da mensagem a responder
- `--text`, `-t` (obrigatório): Texto da resposta

#### Notas:
- O message-id é retornado ao enviar mensagens
- A resposta aparece como "citação" da mensagem original

---

### 9. send_mention.py - Mencionar em Grupo

Menciona pessoas em mensagem de grupo via WhatsApp.

**Status:** ✅ Funcional

#### Uso:
```bash
# Mencionar uma pessoa
python3 scripts/whatsapp/send_mention.py \
  --group "120363123456789012@g.us" \
  --text "@5531980160822 atenção!" \
  --mentions "5531980160822"

# Mencionar várias pessoas
python3 scripts/whatsapp/send_mention.py \
  --group "120363123456789012@g.us" \
  --text "Olá @5531980160822 e @5511999999999!" \
  --mentions "5531980160822,5511999999999"
```

#### Parâmetros:
- `--group`, `-g` (obrigatório): ID do grupo (ex: 120363123456789012@g.us)
- `--text`, `-t` (obrigatório): Texto da mensagem (use @numero para mencionar)
- `--mentions`, `-m` (obrigatório): Números a mencionar separados por vírgula

#### Notas:
- Use @numero no texto para posicionar a menção
- Números devem estar na lista de mentions para notificar

---

### 10. send_status.py - Postar Story/Status

Posta status/story no WhatsApp.

**Status:** ✅ Funcional

#### Uso:
```bash
# Status de texto
python3 scripts/whatsapp/send_status.py \
  --content "Olá! Este é meu status!" \
  --type text \
  --bgcolor "#008000"

# Status de texto com cor customizada
python3 scripts/whatsapp/send_status.py \
  --content "Bom dia!" \
  --type text \
  --bgcolor "#FF0000" \
  --caption "Status do dia"

# Status com imagem
python3 scripts/whatsapp/send_status.py \
  --content "https://example.com/image.jpg" \
  --type image \
  --caption "Minha foto"
```

#### Parâmetros:
- `--content`, `-c` (obrigatório): Conteúdo (texto ou URL da mídia)
- `--type`, `-t` (opcional): Tipo do status (`text`, `image`, `video`, `audio`) - padrão: text
- `--bgcolor`, `-b` (opcional): Cor de fundo para texto (ex: #008000) - padrão: #000000
- `--caption`, `-p` (opcional): Legenda para imagem/vídeo

#### Notas:
- Status expira em 24 horas automaticamente
- Cor de fundo em formato hexadecimal (#RRGGBB)

---

## 👥 GRUPOS (5 templates)

### 11. create_group.py - Criar Grupo

Cria grupos no WhatsApp com configurações personalizadas.

**Status:** ✅ Funcional

#### Uso:
```bash
# Criar grupo simples
python3 scripts/whatsapp/create_group.py \
  --name "Meu Grupo" \
  --phones 5531980160822,5511999999999

# Criar grupo com descrição
python3 scripts/whatsapp/create_group.py \
  --name "Vendas 2025" \
  --phones 5531980160822,5511999999999,5521888888888 \
  --description "Grupo para discutir vendas de 2025"

# Criar grupo apenas para admins
python3 scripts/whatsapp/create_group.py \
  --name "Anúncios" \
  --phones 5531980160822,5511999999999 \
  --description "Apenas administradores podem enviar mensagens" \
  --admins-only
```

#### Parâmetros:
- `--name`, `-n` (obrigatório): Nome do grupo
- `--phones`, `-p` (obrigatório): Números separados por vírgula
- `--description`, `-d` (opcional): Descrição do grupo
- `--admins-only`, `-a` (opcional): Apenas admins podem enviar mensagens

#### Formato de números:
- DDI + DDD + Número (sem espaços/hífens)
- Exemplo: `5531980160822,5511999999999`
- Separados por vírgula (sem espaços)

---

### 12. update_group.py - Atualizar Grupo

Atualiza informações do grupo WhatsApp (nome, descrição, foto).

**Status:** ✅ Funcional

#### Uso:
```bash
# Atualizar nome
python3 scripts/whatsapp/update_group.py \
  --group 120363404863351747@g.us \
  --name "Novo Nome"

# Atualizar descrição
python3 scripts/whatsapp/update_group.py \
  --group 120363404863351747@g.us \
  --description "Nova descrição"

# Atualizar foto
python3 scripts/whatsapp/update_group.py \
  --group 120363404863351747@g.us \
  --picture "https://exemplo.com/imagem.jpg"

# Atualizar tudo
python3 scripts/whatsapp/update_group.py \
  --group 120363404863351747@g.us \
  --name "Grupo Atualizado" \
  --description "Descrição nova" \
  --picture "https://exemplo.com/foto.jpg"
```

#### Parâmetros:
- `--group`, `-g` (obrigatório): ID do grupo (ex: 120363404863351747@g.us)
- `--name`, `-n` (opcional): Novo nome do grupo
- `--description`, `-d` (opcional): Nova descrição do grupo
- `--picture`, `-p` (opcional): URL ou caminho da nova foto do grupo

#### Notas:
- Pelo menos um parâmetro de atualização é obrigatório
- Apenas administradores podem atualizar grupos

---

### 13. manage_participants.py - Gerenciar Participantes

Gerencia participantes de grupo WhatsApp (adicionar, remover, promover, rebaixar).

**Status:** ✅ Funcional

#### Uso:
```bash
# Adicionar participante
python3 scripts/whatsapp/manage_participants.py \
  --group 120363404863351747@g.us \
  --action add \
  --phones 5511999999999

# Remover múltiplos participantes
python3 scripts/whatsapp/manage_participants.py \
  --group 120363404863351747@g.us \
  --action remove \
  --phones 5511999999999,5511888888888

# Promover a administrador
python3 scripts/whatsapp/manage_participants.py \
  --group 120363404863351747@g.us \
  --action promote \
  --phones 5531980160822

# Remover administrador
python3 scripts/whatsapp/manage_participants.py \
  --group 120363404863351747@g.us \
  --action demote \
  --phones 5531980160822
```

#### Parâmetros:
- `--group`, `-g` (obrigatório): ID do grupo (ex: 120363404863351747@g.us)
- `--action`, `-a` (obrigatório): Ação (`add`, `remove`, `promote`, `demote`)
- `--phones`, `-p` (obrigatório): Números separados por vírgula

#### Ações disponíveis:
- `add` - Adicionar participantes ao grupo
- `remove` - Remover participantes do grupo
- `promote` - Tornar participante administrador
- `demote` - Remover administrador (voltar a participante)

#### Notas:
- Apenas administradores podem gerenciar participantes
- Use vírgula para separar múltiplos números (sem espaços)

---

### 14. list_groups.py - Listar Grupos

Lista todos os grupos do WhatsApp com filtros e detalhes.

**Status:** ✅ Funcional

#### Uso:
```bash
# Listar todos os grupos (resumo)
python3 scripts/whatsapp/list_groups.py

# Listar com detalhes completos
python3 scripts/whatsapp/list_groups.py --verbose

# Filtrar grupos por nome
python3 scripts/whatsapp/list_groups.py --filter "Teste"

# Filtrar com detalhes
python3 scripts/whatsapp/list_groups.py --verbose --filter "Template"
```

#### Parâmetros:
- `--verbose`, `-v` (opcional): Mostrar detalhes completos dos grupos
- `--filter`, `-f` (opcional): Filtrar grupos por nome

#### Informações exibidas:
- **Resumo:** Nome e ID do grupo
- **Verbose:** Participantes, administradores, descrição, data de criação

---

### 15. leave_group.py - Sair do Grupo

Sai de um grupo WhatsApp.

**Status:** ✅ Funcional

**⚠️ ATENÇÃO:** Esta ação é IRREVERSÍVEL! Você precisará ser adicionado novamente para retornar ao grupo.

#### Uso:
```bash
# Sair do grupo (requer confirmação)
python3 scripts/whatsapp/leave_group.py \
  --group 120363404863351747@g.us \
  --confirm
```

#### Parâmetros:
- `--group`, `-g` (obrigatório): ID do grupo (ex: 120363404863351747@g.us)
- `--confirm`, `-c` (obrigatório): Confirmação de segurança

#### Notas:
- Confirmação obrigatória com flag `--confirm`
- Confirmação adicional via input interativo (digite 'SAIR')
- Ação irreversível - será necessário ser adicionado novamente

---

## 👤 PERFIL E CONTATOS (4 templates)

### 16-18. manage_profile.py, get_profile.py, get_contacts.py

Gerenciamento de perfil e obtenção de contatos.

**Status:** ❌ Endpoints indisponíveis na Evolution API v2.3.4

#### Templates:
- `manage_profile.py` - Atualizar nome, foto e status do perfil
- `get_profile.py` - Obter informações do perfil de um número
- `get_contacts.py` - Listar todos os contatos

#### Notas:
- Endpoints não estão disponíveis na versão atual da Evolution API
- Templates mantidos para compatibilidade futura
- Estrutura pronta para quando endpoints forem implementados

---

### 19. check_number.py - Verificar Número

Verifica se números existem no WhatsApp.

**Status:** ✅ Funcional

#### Uso:
```bash
# Verificar um número
python3 scripts/whatsapp/check_number.py --phones 5531980160822

# Verificar múltiplos números
python3 scripts/whatsapp/check_number.py --phones 5531980160822,5511999999999,123456789
```

#### Parâmetros:
- `--phones`, `-p` (obrigatório): Números separados por vírgula

#### Retorna:
- Status de cada número (existe/não existe no WhatsApp)
- JID (identificador único) se número existe
- JSON completo com todos os detalhes

#### Notas:
- Útil para validar números antes de enviar mensagens
- Evita erros ao tentar enviar para números inválidos

---

## ⚙️ AÇÕES (1 template)

### 20. message_actions.py - Ações em Mensagens

Executa ações em mensagens WhatsApp (marcar como lida, deletar).

**Status:** ✅ Funcional

#### Uso:
```bash
# Marcar mensagem como lida
python3 scripts/whatsapp/message_actions.py \
  --action read \
  --phone 5531980160822 \
  --message-id 3EB0123456789ABCDEF

# Deletar mensagem (apenas para você)
python3 scripts/whatsapp/message_actions.py \
  --action delete \
  --phone 5531980160822 \
  --message-id 3EB0123456789ABCDEF

# Deletar mensagem para todos
python3 scripts/whatsapp/message_actions.py \
  --action delete \
  --phone 5531980160822 \
  --message-id 3EB0123456789ABCDEF \
  --for-everyone
```

#### Parâmetros:
- `--action`, `-a` (obrigatório): Ação (`read`, `delete`)
- `--phone`, `-p` (obrigatório): Número do destinatário com DDI
- `--message-id`, `-m` (obrigatório): ID da mensagem retornado ao enviar
- `--for-everyone` (opcional): Deletar para todos (apenas para action=delete)

#### Ações disponíveis:
- `read` - Marca mensagem como lida
- `delete` - Deleta mensagem (para você ou para todos)

#### Notas:
- O message-id é retornado ao enviar mensagens
- Deletar "para todos" tem limite de tempo (poucas horas)

---

## 🔧 SISTEMA (2 templates)

### 21. instance_info.py - Informações da Instância

Obtém informações e status da instância WhatsApp.

**Status:** ✅ Funcional

#### Uso:
```bash
# Ver informações básicas
python3 scripts/whatsapp/instance_info.py

# Ver com QR code (se desconectado)
python3 scripts/whatsapp/instance_info.py --qrcode

# Ver informações detalhadas
python3 scripts/whatsapp/instance_info.py --verbose
```

#### Parâmetros:
- `--qrcode`, `-q` (opcional): Mostrar QR code se disponível
- `--verbose`, `-v` (opcional): Mostrar informações detalhadas

#### Informações exibidas:
- Estado da conexão (conectado/desconectado)
- Nome da instância
- Número do WhatsApp (se conectado)
- Nome do perfil (se conectado)
- QR code (se desconectado e solicitado)

#### Notas:
- Use para verificar status antes de enviar mensagens
- QR code útil para reconectar instância

---

### 22. manage_webhooks.py - Gerenciar Webhooks

Gerencia webhooks da instância WhatsApp (ver configuração, configurar eventos).

**Status:** ✅ Funcional

**⚠️ ATENÇÃO:** Use com cuidado! Alterar webhooks pode afetar integrações em produção.

#### Uso:
```bash
# Ver webhooks atuais
python3 scripts/whatsapp/manage_webhooks.py --action get

# Configurar webhook (USE COM CUIDADO!)
python3 scripts/whatsapp/manage_webhooks.py \
  --action set \
  --url https://seu.webhook.com/events \
  --events MESSAGES_UPSERT,CONNECTION_UPDATE

# Webhook com eventos separados e base64
python3 scripts/whatsapp/manage_webhooks.py \
  --action set \
  --url https://seu.webhook.com/events \
  --events MESSAGES_UPSERT,SEND_MESSAGE \
  --by-events \
  --base64
```

#### Parâmetros:
- `--action`, `-a` (obrigatório): Ação (`get`, `set`)
- `--url`, `-u` (obrigatório para set): URL do webhook
- `--events`, `-e` (obrigatório para set): Eventos separados por vírgula
- `--by-events` (opcional): Criar webhook específico por evento
- `--base64` (opcional): Enviar mídias em base64

#### Eventos disponíveis:
- `MESSAGES_UPSERT` - Nova mensagem recebida
- `MESSAGES_UPDATE` - Mensagem atualizada (lida, deletada, etc)
- `MESSAGES_DELETE` - Mensagem deletada
- `SEND_MESSAGE` - Mensagem enviada
- `CONNECTION_UPDATE` - Mudança no estado da conexão
- `QRCODE_UPDATED` - QR code atualizado
- `GROUPS_UPSERT` - Novo grupo criado
- `GROUPS_UPDATE` - Grupo atualizado
- `GROUP_PARTICIPANTS_UPDATE` - Participantes do grupo atualizados

#### Notas:
- SEMPRE use `--action get` primeiro para ver configuração atual
- Ação `set` requer confirmação de segurança (digite 'SIM')
- Webhooks são essenciais para integrações (Chatwoot, n8n, etc)

---

## 🎯 Casos de Uso Comuns

### 1. Notificação de Cliente
```bash
python3 scripts/whatsapp/send_message.py \
  --phone 5531980160822 \
  --message "Olá! Seu pedido #1234 foi enviado e chegará em 2 dias úteis. 📦"
```

### 2. Enviar Comprovante
```bash
python3 scripts/whatsapp/send_media.py \
  --phone 5531980160822 \
  --url "https://exemplo.com/comprovante_pagamento.pdf" \
  --type document \
  --caption "Segue o comprovante do pagamento" \
  --filename "Comprovante.pdf"
```

### 3. Criar Grupo de Projeto
```bash
python3 scripts/whatsapp/create_group.py \
  --name "Projeto Website 2025" \
  --phones 5531980160822,5511999999999,5521888888888 \
  --description "Grupo para discutir o desenvolvimento do website"
```

### 4. Pesquisa de Satisfação
```bash
python3 scripts/whatsapp/send_poll.py \
  --phone 5531980160822 \
  --question "Como você avalia nosso atendimento?" \
  --options "Excelente,Bom,Regular,Ruim"
```

### 5. Enviar Localização de Imóvel
```bash
python3 scripts/whatsapp/send_location.py \
  --phone 5531980160822 \
  --lat -19.9167 \
  --lon -43.9345 \
  --name "Apartamento 3 Quartos" \
  --address "Rua das Flores, 123 - Belo Horizonte, MG"
```

### 6. Compartilhar Contato do Corretor
```bash
python3 scripts/whatsapp/send_contact.py \
  --phone 5531980160822 \
  --contact-number 5531999999999 \
  --name "João Silva - Corretor" \
  --organization "LF Imóveis" \
  --email "joao@lfimoveis.com.br"
```

### 7. Enviar Anúncio em Grupo
```bash
python3 scripts/whatsapp/send_mention.py \
  --group "120363123456789012@g.us" \
  --text "🏠 Novo imóvel disponível! @5531980160822 @5511999999999" \
  --mentions "5531980160822,5511999999999"
```

### 8. Responder Cliente Rapidamente
```bash
# 1. Capturar message_id ao enviar mensagem
MSG_ID=$(python3 scripts/whatsapp/send_message.py --phone 5531980160822 --message "Olá! Recebemos sua mensagem." | grep "Message ID" | cut -d: -f2)

# 2. Cliente responde, você replica citando a mensagem dele
python3 scripts/whatsapp/send_reply.py \
  --phone 5531980160822 \
  --message-id "$MSG_ID" \
  --text "Estamos analisando seu caso e retornaremos em breve!"
```

### 9. Verificar Números Antes de Campanha
```bash
# Validar lista de números antes de enviar mensagens em massa
python3 scripts/whatsapp/check_number.py \
  --phones 5531980160822,5511999999999,5521888888888
```

### 10. Monitorar Status da Instância
```bash
# Verificar antes de operações críticas
python3 scripts/whatsapp/instance_info.py
```

---

## 🔧 Configuração

### Pré-requisitos:

1. **Evolution API instalada e configurada**
   - URL: Configurado em `evolution-api-integration/config.py`
   - API Key: Configurado em `evolution-api-integration/config.py`
   - Instância: Conectada e ativa

2. **Python 3.9+**
   ```bash
   python3 --version
   ```

3. **Dependências instaladas**
   ```bash
   pip3 install requests
   ```

### Verificar conexão:
```bash
cd evolution-api-integration
python3 -c "from evolution_api import EvolutionAPI; from config import *; api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME); print(api.get_instance_status())"
```

---

## 📖 Integração com Claude Code

### Para o Agente Claude Code:

Quando o usuário pedir ações WhatsApp, **SEMPRE use estes templates** ao invés de criar scripts novos.

#### Exemplos de comandos do usuário:

**❌ NÃO fazer:**
```
Usuário: "Envie mensagem WhatsApp para 5531980160822"
Agente: Cria novo script test_whatsapp.py → Executa → Descarta
```

**✅ FAZER:**
```
Usuário: "Envie mensagem WhatsApp para 5531980160822"
Agente: python3 scripts/whatsapp/send_message.py --phone 5531980160822 --message "..."
```

#### Mapeamento de comandos:

| Pedido do usuário | Template a usar |
|-------------------|-----------------|
| "Enviar mensagem" | `send_message.py` |
| "Enviar imagem/vídeo/arquivo" | `send_media.py` |
| "Enviar enquete/votação" | `send_poll.py` |
| "Enviar áudio/PTT" | `send_audio.py` |
| "Enviar localização/endereço" | `send_location.py` |
| "Enviar contato" | `send_contact.py` |
| "Reagir mensagem" | `send_reaction.py` |
| "Responder mensagem/citar" | `send_reply.py` |
| "Mencionar em grupo" | `send_mention.py` |
| "Postar status/story" | `send_status.py` |
| "Criar grupo" | `create_group.py` |
| "Atualizar grupo/nome/descrição/foto" | `update_group.py` |
| "Adicionar/remover participantes" | `manage_participants.py` |
| "Listar grupos" | `list_groups.py` |
| "Sair do grupo" | `leave_group.py` |
| "Verificar número" | `check_number.py` |
| "Marcar lida/deletar mensagem" | `message_actions.py` |
| "Ver status da instância" | `instance_info.py` |
| "Configurar webhook" | `manage_webhooks.py` |

---

## 🐛 Troubleshooting

### Erro: "Módulo evolution_api não encontrado"
```bash
# Verifique o path do Python
export PYTHONPATH=$PYTHONPATH:/path/to/ClaudeCode-Workspace/evolution-api-integration
```

### Erro: "Instância não conectada"
```bash
# Verifique status da instância Evolution API
curl https://evolution.loop9.com.br/instance/connectionState/lfimoveis \
  -H "apikey: 178e43e1c4f459527e7008e57e378e1c"
```

### Erro: "Número inválido"
- Use formato: DDI + DDD + Número (ex: 5531980160822)
- Sem espaços, hífens ou parênteses
- Sem símbolo + ou 00

### Erro: "Message ID não encontrado"
- O message-id é retornado ao enviar mensagens
- Salve o output do envio para usar em reações/respostas
- Use `grep "Message ID"` para extrair o ID

### Erro ao enviar áudio PTT
- Certifique-se de usar formato OGG Opus
- Converta com: `ffmpeg -i audio.mp3 -c:a libopus audio.ogg`
- Teste a URL/arquivo antes de enviar

---

## 📊 Logs e Monitoramento

Todos os scripts exibem output em tempo real:

```
✅ = Sucesso
❌ = Erro
⚙️ = Processando
📤 = Enviando
📋 = Listando
🔍 = Verificando
👥 = Gerenciando participantes
📱 = Instância/Status
🔧 = Webhook/Configuração
```

### Exemplo de output:
```bash
$ python3 scripts/whatsapp/send_message.py --phone 5531980160822 --message "Teste"
📤 Enviando mensagem para 5531980160822...
✅ Mensagem enviada com sucesso!
   Message ID: 3EB01234567890ABCDEF1234567890AB
```

---

## 🔄 Roadmap / Próximas Funcionalidades

**Concluído (22/22 templates):**
- ✅ Envio de mensagens de texto
- ✅ Envio de mídias (imagem, vídeo, documento, áudio)
- ✅ Enquetes/votações
- ✅ Áudio PTT (Push To Talk)
- ✅ Localização geográfica
- ✅ Envio de contatos
- ✅ Reações a mensagens
- ✅ Respostas (reply/quote)
- ✅ Menções em grupos
- ✅ Status/Stories
- ✅ Criar grupos
- ✅ Atualizar grupos (nome, descrição, foto)
- ✅ Gerenciar participantes (add, remove, promote, demote)
- ✅ Listar grupos
- ✅ Sair de grupos
- ✅ Verificar números
- ✅ Ações em mensagens (read, delete)
- ✅ Informações da instância
- ✅ Gerenciar webhooks

**Aguardando Evolution API:**
- ⏳ Gerenciar perfil (manage_profile.py)
- ⏳ Obter perfil (get_profile.py)
- ⏳ Listar contatos (get_contacts.py)

**Futuras Melhorias:**
- 🔮 Mensagens em massa (bulk_message.py)
- 🔮 Agendamento integrado (schedule_message.py)
- 🔮 Template de mensagens (message_templates.py)
- 🔮 Estatísticas de mensagens (message_stats.py)
- 🔮 Backup de conversas (backup_chats.py)

---

## 📚 Documentação Relacionada

- **Evolution API:** `evolution-api-integration/README.md`
- **Chatbot WhatsApp V4:** `whatsapp-chatbot/README.md`
- **Sistema de Agendamento:** `scheduling-system/README.md`
- **CLAUDE.md:** Instruções gerais do workspace

---

## 🤝 Contribuindo

Para adicionar novos templates:

1. Crie o script em `scripts/whatsapp/`
2. Siga o padrão dos templates existentes:
   - Docstring com descrição e exemplos de uso
   - Imports do evolution_api e config
   - Função principal com lógica
   - main() com argparse
   - Output formatado (✅ ❌ 📤 etc)
3. Teste o template
4. Adicione documentação neste README
5. Atualize a estatística de templates no topo

---

**Última atualização:** 2025-11-01
**Versão:** 2.0 - 22 templates completos
**Integração:** Evolution API v2.3.4
**Status:** ✅ 19 funcionais | ⚠️ 1 aguarda áudio OGG | ❌ 3 aguardam API
