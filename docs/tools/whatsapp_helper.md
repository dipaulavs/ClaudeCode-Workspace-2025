# 💬 WhatsApp Helper - Evolution API

Controle programático completo do WhatsApp via Evolution API.

## 🚀 Uso Interativo

```bash
cd evolution-api-integration
python3.11 whatsapp_helper.py
```

## 📝 Uso em Código Python

```python
from whatsapp_helper import whatsapp

# Enviar mensagem
whatsapp.send_message("5511999999999", "Olá! Como você está?")

# Enviar imagem
whatsapp.send_image("5511999999999", "https://exemplo.com/foto.jpg", "Confira!")

# Enviar vídeo
whatsapp.send_video("5511999999999", "https://exemplo.com/video.mp4", "Veja isso!")

# Enviar documento
whatsapp.send_document("5511999999999", "https://exemplo.com/doc.pdf", "Documento")

# Enviar áudio
whatsapp.send_audio("5511999999999", "https://exemplo.com/audio.mp3")

# Criar grupo
grupo = whatsapp.create_group(
    name="Meu Grupo",
    participants=["5511999999999", "5511888888888"]
)

# Enviar enquete
whatsapp.create_poll(
    "120363123456789@g.us",  # ID do grupo
    "Melhor dia para reunião?",
    ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
)

# Enviar localização
whatsapp.send_location(
    "5511999999999",
    -23.550520,  # Latitude
    -46.633308,  # Longitude
    "Av. Paulista",
    "São Paulo"
)

# Listar grupos
grupos = whatsapp.list_groups()

# Adicionar membro ao grupo
whatsapp.add_group_member("GRUPO_ID@g.us", "5511999999999")

# Remover membro do grupo
whatsapp.remove_group_member("GRUPO_ID@g.us", "5511999999999")

# Promover a admin
whatsapp.promote_to_admin("GRUPO_ID@g.us", "5511999999999")
```

## 📋 Funcionalidades

### Mensagens
- Texto, imagem, vídeo, documento, áudio
- Stickers
- Reações

### Grupos
- Criar, listar
- Adicionar/remover membros
- Promover/rebaixar admins
- Atualizar configurações

### Recursos Avançados
- Enquetes
- Localização
- Menções (@)
- Status (stories)

## 📱 Formato de Números

**DDI + DDD + Número** (sem espaços, hífens ou parênteses)

```
✅ Correto: 5511999999999
❌ Errado: +55 (11) 99999-9999
❌ Errado: 11999999999
```

## 📖 Docs Completa

- `evolution-api-integration/README.md`
- `evolution-api-integration/GUIA_RAPIDO.md`

## 🔧 Config

Evolution API configurada em `whatsapp_helper.py`
