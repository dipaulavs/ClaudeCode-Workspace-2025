# Guia Rápido - Evolution API WhatsApp

## Instalação Completa

A Evolution API já está configurada e funcionando! Sua instância `lfimoveis` está conectada e pronta para uso.

## Como Usar

### Opção 1: Usar o Helper Simplificado (RECOMENDADO)

```python
from whatsapp_helper import whatsapp

# Enviar mensagem
whatsapp.send_message("5511999999999", "Olá! Como você está?")

# Enviar imagem
whatsapp.send_image("5511999999999", "https://exemplo.com/foto.jpg", "Confira!")

# Criar grupo
grupo = whatsapp.create_group(
    name="Meu Grupo",
    participants=["5511999999999", "5511888888888"]
)

# Listar grupos
grupos = whatsapp.get_groups()
for g in grupos:
    print(f"Grupo: {g['subject']} - ID: {g['id']}")
```

### Opção 2: Usar a Classe Completa

```python
from evolution_api import EvolutionAPI
from config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME

api = EvolutionAPI(EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME)

# Enviar mensagem
api.send_text("5511999999999", "Olá!")

# Enviar mídia
api.send_media("5511999999999", "https://exemplo.com/foto.jpg", "Legenda", "image")
```

## Comandos Rápidos

### Testar Conexão
```bash
cd ~/Desktop/ClaudeCode-Workspace/evolution-api-integration
python3.11 test_connection.py
```

### Ver Exemplos
```bash
python3.11 examples.py
```

### Iniciar Helper
```bash
python3.11 whatsapp_helper.py
```

## Principais Funcionalidades

### Mensagens
- `send_message()` - Mensagem de texto
- `send_image()` - Enviar imagem
- `send_video()` - Enviar vídeo
- `send_document()` - Enviar documento
- `send_location()` - Enviar localização
- `create_poll()` - Criar enquete

### Grupos
- `create_group()` - Criar grupo
- `get_groups()` - Listar grupos
- `send_group_message()` - Mensagem no grupo
- `mention_in_group()` - Mencionar pessoas
- `add_to_group()` - Adicionar pessoas
- `remove_from_group()` - Remover pessoas
- `make_admin()` - Promover a admin

### Status
- `check_status()` - Verificar conexão

## Formato de Números

- **Individual**: `5511999999999` (DDI + DDD + Número)
- **Grupo**: `120363123456789@g.us` (obtido ao criar/listar grupos)

## Exemplos Práticos

### 1. Enviar mensagem com formatação
```python
whatsapp.send_message(
    "5511999999999",
    "*Texto em negrito*\n_Texto em itálico_\n~Texto riscado~"
)
```

### 2. Criar grupo e enviar mensagem
```python
# Criar grupo
grupo = whatsapp.create_group(
    "Grupo Vendas",
    ["5511999999999", "5511888888888"],
    "Grupo para vendas"
)

# Pegar o ID do grupo
grupo_id = grupo['id']

# Enviar mensagem
whatsapp.send_group_message(grupo_id, "Bem-vindos!")

# Mencionar alguém
whatsapp.mention_in_group(
    grupo_id,
    "@5511999999999 confira isso!",
    ["5511999999999"]
)
```

### 3. Enviar enquete
```python
whatsapp.create_poll(
    "120363123456789@g.us",  # ID do grupo
    "Melhor dia para reunião?",
    ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
)
```

### 4. Enviar localização
```python
whatsapp.send_location(
    "5511999999999",
    -23.550520,
    -46.633308,
    "Av. Paulista",
    "Avenida Paulista, São Paulo"
)
```

## Arquivos do Projeto

- `evolution_api.py` - Classe principal com todos os métodos
- `whatsapp_helper.py` - Helper simplificado (USE ESTE!)
- `config.py` - Configurações (URL, API Key, Instância)
- `test_connection.py` - Testar conexão
- `examples.py` - Todos os exemplos
- `README.md` - Documentação completa

## Status da Instalação

✅ Evolution API: **INSTALADA E FUNCIONANDO**
✅ Instância: **lfimoveis (CONECTADA)**
✅ Módulo Python: **PRONTO PARA USO**

## Suporte

Consulte o `README.md` para documentação completa de todos os métodos disponíveis.

---

**Tudo pronto! Comece a usar agora mesmo!**
