# Evolution API v2 - Documentação Completa

**Fonte:** https://doc.evolution-api.com/v2/
**Data do Scraping:** 06/11/2025
**Total de Linhas:** 544
**Método:** Apify Web Scraper

---

## 📋 Índice

### 1. Get Started
- **Recursos Disponíveis** - Lista completa de funcionalidades

### 2. Instalação
- **Docker** - Setup completo com Docker e Docker Compose
- **Docker Swarm** - Deployment escalável

### 3. Integrações
- **Chatwoot** - Integração com plataforma de suporte
- **Typebot** - Integração com bot automation

### 4. API Reference
- **Get Information** - Informações da API
- **Instance/Create** - Criar nova instância
- **Instance/Connect** - Conectar instância (QR Code)
- **Message/Send-Text** - Enviar mensagem de texto
- **Message/Send-Media** - Enviar mídia (imagem, vídeo, documento)
- **Webhook/Set** - Configurar webhooks

---

## 🔗 URLs Scraped

1. `https://doc.evolution-api.com/v2/pt/get-started/introduction`
2. `https://doc.evolution-api.com/v2/pt/install/docker`
3. `https://doc.evolution-api.com/v2/pt/integrations/chatwoot`
4. `https://doc.evolution-api.com/v2/pt/integrations/typebot`
5. `https://doc.evolution-api.com/v2/api-reference/get-information`
6. `https://doc.evolution-api.com/v2/api-reference/instance/create`
7. `https://doc.evolution-api.com/v2/api-reference/instance/connect`
8. `https://doc.evolution-api.com/v2/api-reference/message/send-text`
9. `https://doc.evolution-api.com/v2/api-reference/message/send-media`
10. `https://doc.evolution-api.com/v2/api-reference/webhook/set`

---

## 📊 Recursos Principais

### Mensagens
✅ Texto (simples, formatado)
✅ Mídia (imagem, vídeo, documento)
✅ Áudio narrado
✅ Localização
✅ Contato
✅ Reação (emojis)
✅ Pré-visualização de link
✅ Resposta (reply)
✅ Menção (@)
✅ Enquete
✅ Status/História
✅ Adesivo
✅ Lista (em homologação)
❌ Botões (descontinuado - só API Cloud)

### Perfil
✅ Atualizar nome
✅ Atualizar foto
✅ Atualizar status

### Grupos
✅ Criar grupo
✅ Atualizar foto
✅ Atualizar assunto
✅ Atualizar descrição
✅ Listar grupos e participantes

---

## 🐳 Quick Start - Docker

```yaml
version: '3.9'
services:
  evolution-api:
    container_name: evolution_api
    image: atendai/evolution-api:v2.1.1
    restart: always
    ports:
      - "8080:8080"
    env_file:
      - .env
    volumes:
      - evolution_instances:/evolution/instances

volumes:
  evolution_instances:
```

**Variável obrigatória (.env):**
```bash
AUTHENTICATION_API_KEY=sua-chave-aqui
```

**Comandos:**
```bash
# Iniciar
docker compose up -d

# Logs
docker logs evolution_api

# Parar
docker compose down

# Acessar API
http://localhost:8080
```

---

# Scraping Completo: doc

**URL Original:** https://doc.evolution-api.com/v2/pt/get-started/introduction
**Data:** 06/11/2025 23:10:35
**Total de Páginas:** 1

---

# Página 1: Recursos Disponíveis - Evolution API Documentation

**URL:** https://doc.evolution-api.com/v2/pt/get-started/introduction


# Recursos Disponíveis - Evolution API Documentation

## Recursos de Mensagens e Grupos

### Mensagens (Individuais ou em Grupo)

| Recurso | Disponibilidade | Descrição |
| --- | --- | --- |
| Envio de Texto | ✅   | (Texto simples, em negrito, itálico, riscado, em formato de código e emojis) |
| Envio de Mídia | ✅   | (Vídeo, imagem e documento) |
| Envio de Áudio Narrado | ✅   | (Funcionando bem no Android e iOS) |
| Envio de Localização | ✅   | (Com nome e descrição do local) |
| Envio de Contato | ✅   | (Com Nome, Empresa, Telefone, E-mail e URL) |
| Envio de Reação | ✅   | (Envie qualquer emoji para reação) |
| Envio de Pré-visualização de Link | ✅   | (Busca por informações de SEO) 🆕 |
| Envio de Resposta | ✅   | (Marcar mensagens em resposta) 🆕 |
| Envio de Menção | ✅   | (Individual, para alguns ou todos os membros) 🆕 |
| Envio de Enquete | ✅   | (Enviar e receber votos de uma enquete) 🆕 |
| Envio de Status/História | ✅   | (Texto, pré-visualização de link, vídeo, imagem e forma de onda) 🆕 |
| Envio de Adesivo | ✅   | (Imagem estática) 🆕 |
| Envio de Lista (Homologação) | ✅   | (Testando) |
| Envio de Botões (Descontinuado) | ❌   | (Só funciona na API em nuvem) |

### Perfil

| Recurso | Disponibilidade | Descrição |
| --- | --- | --- |
| Atualizar Nome | ✅   | (Alterar o nome do perfil conectado) |
| Atualizar Foto | ✅   | (Alterar a foto do perfil conectado) 🆕 |
| Atualizar Status | ✅   | (Alterar o status do perfil conectado) 🆕 |
| E muitos outros… |     |     |

### Grupo

| Recurso | Disponibilidade | Descrição |
| --- | --- | --- |
| Criar Grupo | ✅   | (Novos grupos) |
| Atualizar Foto | ✅   | (Alterar foto do grupo) |
| Atualizar Assunto | ✅   | (Alterar o nome do grupo) 🆕 |
| Atualizar Descrição | ✅   | (Alterar a descrição do grupo) 🆕 |
| Obter Todos os Grupos | ✅   | (Obter todos os grupos e participantes) 🆕 |
| E muitos outros… |     |     |


---

# Scraping Completo: doc

**URL Original:** https://doc.evolution-api.com/v2/pt/install/docker
**Data:** 06/11/2025 23:12:44
**Total de Páginas:** 1

---

# Página 1: Recursos Disponíveis - Evolution API Documentation

**URL:** https://doc.evolution-api.com/v2/pt/install/docker


# Recursos Disponíveis - Evolution API Documentation

## Recursos de Mensagens e Grupos

### Mensagens (Individuais ou em Grupo)

| Recurso | Disponibilidade | Descrição |
| --- | --- | --- |
| Envio de Texto | ✅   | (Texto simples, em negrito, itálico, riscado, em formato de código e emojis) |
| Envio de Mídia | ✅   | (Vídeo, imagem e documento) |
| Envio de Áudio Narrado | ✅   | (Funcionando bem no Android e iOS) |
| Envio de Localização | ✅   | (Com nome e descrição do local) |
| Envio de Contato | ✅   | (Com Nome, Empresa, Telefone, E-mail e URL) |
| Envio de Reação | ✅   | (Envie qualquer emoji para reação) |
| Envio de Pré-visualização de Link | ✅   | (Busca por informações de SEO) 🆕 |
| Envio de Resposta | ✅   | (Marcar mensagens em resposta) 🆕 |
| Envio de Menção | ✅   | (Individual, para alguns ou todos os membros) 🆕 |
| Envio de Enquete | ✅   | (Enviar e receber votos de uma enquete) 🆕 |
| Envio de Status/História | ✅   | (Texto, pré-visualização de link, vídeo, imagem e forma de onda) 🆕 |
| Envio de Adesivo | ✅   | (Imagem estática) 🆕 |
| Envio de Lista (Homologação) | ✅   | (Testando) |
| Envio de Botões (Descontinuado) | ❌   | (Só funciona na API em nuvem) |

### Perfil

| Recurso | Disponibilidade | Descrição |
| --- | --- | --- |
| Atualizar Nome | ✅   | (Alterar o nome do perfil conectado) |
| Atualizar Foto | ✅   | (Alterar a foto do perfil conectado) 🆕 |
| Atualizar Status | ✅   | (Alterar o status do perfil conectado) 🆕 |
| E muitos outros… |     |     |

### Grupo

| Recurso | Disponibilidade | Descrição |
| --- | --- | --- |
| Criar Grupo | ✅   | (Novos grupos) |
| Atualizar Foto | ✅   | (Alterar foto do grupo) |
| Atualizar Assunto | ✅   | (Alterar o nome do grupo) 🆕 |
| Atualizar Descrição | ✅   | (Alterar a descrição do grupo) 🆕 |
| Obter Todos os Grupos | ✅   | (Obter todos os grupos e participantes) 🆕 |
| E muitos outros… |     |     |


---

# Scraping Completo: doc

**URL Original:** https://doc.evolution-api.com/v2/pt/integrations/chatwoot
**Data:** 06/11/2025 23:14:38
**Total de Páginas:** 1

---

# Página 1: Recursos Disponíveis - Evolution API Documentation

**URL:** https://doc.evolution-api.com/v2/pt/integrations/chatwoot


# Recursos Disponíveis - Evolution API Documentation

## Recursos de Mensagens e Grupos

### Mensagens (Individuais ou em Grupo)

| Recurso | Disponibilidade | Descrição |
| --- | --- | --- |
| Envio de Texto | ✅   | (Texto simples, em negrito, itálico, riscado, em formato de código e emojis) |
| Envio de Mídia | ✅   | (Vídeo, imagem e documento) |
| Envio de Áudio Narrado | ✅   | (Funcionando bem no Android e iOS) |
| Envio de Localização | ✅   | (Com nome e descrição do local) |
| Envio de Contato | ✅   | (Com Nome, Empresa, Telefone, E-mail e URL) |
| Envio de Reação | ✅   | (Envie qualquer emoji para reação) |
| Envio de Pré-visualização de Link | ✅   | (Busca por informações de SEO) 🆕 |
| Envio de Resposta | ✅   | (Marcar mensagens em resposta) 🆕 |
| Envio de Menção | ✅   | (Individual, para alguns ou todos os membros) 🆕 |
| Envio de Enquete | ✅   | (Enviar e receber votos de uma enquete) 🆕 |
| Envio de Status/História | ✅   | (Texto, pré-visualização de link, vídeo, imagem e forma de onda) 🆕 |
| Envio de Adesivo | ✅   | (Imagem estática) 🆕 |
| Envio de Lista (Homologação) | ✅   | (Testando) |
| Envio de Botões (Descontinuado) | ❌   | (Só funciona na API em nuvem) |

### Perfil

| Recurso | Disponibilidade | Descrição |
| --- | --- | --- |
| Atualizar Nome | ✅   | (Alterar o nome do perfil conectado) |
| Atualizar Foto | ✅   | (Alterar a foto do perfil conectado) 🆕 |
| Atualizar Status | ✅   | (Alterar o status do perfil conectado) 🆕 |
| E muitos outros… |     |     |

### Grupo

| Recurso | Disponibilidade | Descrição |
| --- | --- | --- |
| Criar Grupo | ✅   | (Novos grupos) |
| Atualizar Foto | ✅   | (Alterar foto do grupo) |
| Atualizar Assunto | ✅   | (Alterar o nome do grupo) 🆕 |
| Atualizar Descrição | ✅   | (Alterar a descrição do grupo) 🆕 |
| Obter Todos os Grupos | ✅   | (Obter todos os grupos e participantes) 🆕 |
| E muitos outros… |     |     |


---

# Scraping Completo: doc

**URL Original:** https://doc.evolution-api.com/v2/pt/integrations/typebot
**Data:** 06/11/2025 23:16:35
**Total de Páginas:** 1

---

# Página 1: Recursos Disponíveis - Evolution API Documentation

**URL:** https://doc.evolution-api.com/v2/pt/integrations/typebot


# Recursos Disponíveis - Evolution API Documentation

## Recursos de Mensagens e Grupos

### Mensagens (Individuais ou em Grupo)

| Recurso | Disponibilidade | Descrição |
| --- | --- | --- |
| Envio de Texto | ✅   | (Texto simples, em negrito, itálico, riscado, em formato de código e emojis) |
| Envio de Mídia | ✅   | (Vídeo, imagem e documento) |
| Envio de Áudio Narrado | ✅   | (Funcionando bem no Android e iOS) |
| Envio de Localização | ✅   | (Com nome e descrição do local) |
| Envio de Contato | ✅   | (Com Nome, Empresa, Telefone, E-mail e URL) |
| Envio de Reação | ✅   | (Envie qualquer emoji para reação) |
| Envio de Pré-visualização de Link | ✅   | (Busca por informações de SEO) 🆕 |
| Envio de Resposta | ✅   | (Marcar mensagens em resposta) 🆕 |
| Envio de Menção | ✅   | (Individual, para alguns ou todos os membros) 🆕 |
| Envio de Enquete | ✅   | (Enviar e receber votos de uma enquete) 🆕 |
| Envio de Status/História | ✅   | (Texto, pré-visualização de link, vídeo, imagem e forma de onda) 🆕 |
| Envio de Adesivo | ✅   | (Imagem estática) 🆕 |
| Envio de Lista (Homologação) | ✅   | (Testando) |
| Envio de Botões (Descontinuado) | ❌   | (Só funciona na API em nuvem) |

### Perfil

| Recurso | Disponibilidade | Descrição |
| --- | --- | --- |
| Atualizar Nome | ✅   | (Alterar o nome do perfil conectado) |
| Atualizar Foto | ✅   | (Alterar a foto do perfil conectado) 🆕 |
| Atualizar Status | ✅   | (Alterar o status do perfil conectado) 🆕 |
| E muitos outros… |     |     |

### Grupo

| Recurso | Disponibilidade | Descrição |
| --- | --- | --- |
| Criar Grupo | ✅   | (Novos grupos) |
| Atualizar Foto | ✅   | (Alterar foto do grupo) |
| Atualizar Assunto | ✅   | (Alterar o nome do grupo) 🆕 |
| Atualizar Descrição | ✅   | (Alterar a descrição do grupo) 🆕 |
| Obter Todos os Grupos | ✅   | (Obter todos os grupos e participantes) 🆕 |
| E muitos outros… |     |     |


---

# Scraping Completo: doc

**URL Original:** https://doc.evolution-api.com/v2/api-reference/get-information
**Data:** 06/11/2025 23:21:11
**Total de Páginas:** 1

---

# Página 1: Get Information - Evolution API Documentation

**URL:** https://doc.evolution-api.com/v2/api-reference/get-information


# Get Information - Evolution API Documentation

#### Path Parameters

ID of the instance to connect

#### Response

The HTTP status of the response

Descriptive message about the current state of the API

The current version of the API

URL to the API's Swagger documentation

URL to the detailed API documentation


---

# Scraping Completo: doc

**URL Original:** https://doc.evolution-api.com/v2/api-reference/instance/create
**Data:** 06/11/2025 23:24:08
**Total de Páginas:** 1

---

# Página 1: Recursos Disponíveis - Evolution API Documentation

**URL:** https://doc.evolution-api.com/v2/api-reference/instance/create


# Recursos Disponíveis - Evolution API Documentation

## Recursos de Mensagens e Grupos

### Mensagens (Individuais ou em Grupo)

| Recurso | Disponibilidade | Descrição |
| --- | --- | --- |
| Envio de Texto | ✅   | (Texto simples, em negrito, itálico, riscado, em formato de código e emojis) |
| Envio de Mídia | ✅   | (Vídeo, imagem e documento) |
| Envio de Áudio Narrado | ✅   | (Funcionando bem no Android e iOS) |
| Envio de Localização | ✅   | (Com nome e descrição do local) |
| Envio de Contato | ✅   | (Com Nome, Empresa, Telefone, E-mail e URL) |
| Envio de Reação | ✅   | (Envie qualquer emoji para reação) |
| Envio de Pré-visualização de Link | ✅   | (Busca por informações de SEO) 🆕 |
| Envio de Resposta | ✅   | (Marcar mensagens em resposta) 🆕 |
| Envio de Menção | ✅   | (Individual, para alguns ou todos os membros) 🆕 |
| Envio de Enquete | ✅   | (Enviar e receber votos de uma enquete) 🆕 |
| Envio de Status/História | ✅   | (Texto, pré-visualização de link, vídeo, imagem e forma de onda) 🆕 |
| Envio de Adesivo | ✅   | (Imagem estática) 🆕 |
| Envio de Lista (Homologação) | ✅   | (Testando) |
| Envio de Botões (Descontinuado) | ❌   | (Só funciona na API em nuvem) |

### Perfil

| Recurso | Disponibilidade | Descrição |
| --- | --- | --- |
| Atualizar Nome | ✅   | (Alterar o nome do perfil conectado) |
| Atualizar Foto | ✅   | (Alterar a foto do perfil conectado) 🆕 |
| Atualizar Status | ✅   | (Alterar o status do perfil conectado) 🆕 |
| E muitos outros… |     |     |

### Grupo

| Recurso | Disponibilidade | Descrição |
| --- | --- | --- |
| Criar Grupo | ✅   | (Novos grupos) |
| Atualizar Foto | ✅   | (Alterar foto do grupo) |
| Atualizar Assunto | ✅   | (Alterar o nome do grupo) 🆕 |
| Atualizar Descrição | ✅   | (Alterar a descrição do grupo) 🆕 |
| Obter Todos os Grupos | ✅   | (Obter todos os grupos e participantes) 🆕 |
| E muitos outros… |     |     |


---

# Scraping Completo: doc

**URL Original:** https://doc.evolution-api.com/v2/api-reference/instance/connect
**Data:** 06/11/2025 23:26:17
**Total de Páginas:** 1

---

# Página 1: Recursos Disponíveis - Evolution API Documentation

**URL:** https://doc.evolution-api.com/v2/api-reference/instance/connect


# Recursos Disponíveis - Evolution API Documentation

## Recursos de Mensagens e Grupos

### Mensagens (Individuais ou em Grupo)

| Recurso | Disponibilidade | Descrição |
| --- | --- | --- |
| Envio de Texto | ✅   | (Texto simples, em negrito, itálico, riscado, em formato de código e emojis) |
| Envio de Mídia | ✅   | (Vídeo, imagem e documento) |
| Envio de Áudio Narrado | ✅   | (Funcionando bem no Android e iOS) |
| Envio de Localização | ✅   | (Com nome e descrição do local) |
| Envio de Contato | ✅   | (Com Nome, Empresa, Telefone, E-mail e URL) |
| Envio de Reação | ✅   | (Envie qualquer emoji para reação) |
| Envio de Pré-visualização de Link | ✅   | (Busca por informações de SEO) 🆕 |
| Envio de Resposta | ✅   | (Marcar mensagens em resposta) 🆕 |
| Envio de Menção | ✅   | (Individual, para alguns ou todos os membros) 🆕 |
| Envio de Enquete | ✅   | (Enviar e receber votos de uma enquete) 🆕 |
| Envio de Status/História | ✅   | (Texto, pré-visualização de link, vídeo, imagem e forma de onda) 🆕 |
| Envio de Adesivo | ✅   | (Imagem estática) 🆕 |
| Envio de Lista (Homologação) | ✅   | (Testando) |
| Envio de Botões (Descontinuado) | ❌   | (Só funciona na API em nuvem) |

### Perfil

| Recurso | Disponibilidade | Descrição |
| --- | --- | --- |
| Atualizar Nome | ✅   | (Alterar o nome do perfil conectado) |
| Atualizar Foto | ✅   | (Alterar a foto do perfil conectado) 🆕 |
| Atualizar Status | ✅   | (Alterar o status do perfil conectado) 🆕 |
| E muitos outros… |     |     |

### Grupo

| Recurso | Disponibilidade | Descrição |
| --- | --- | --- |
| Criar Grupo | ✅   | (Novos grupos) |
| Atualizar Foto | ✅   | (Alterar foto do grupo) |
| Atualizar Assunto | ✅   | (Alterar o nome do grupo) 🆕 |
| Atualizar Descrição | ✅   | (Alterar a descrição do grupo) 🆕 |
| Obter Todos os Grupos | ✅   | (Obter todos os grupos e participantes) 🆕 |
| E muitos outros… |     |     |


---

# Scraping Completo: doc

**URL Original:** https://doc.evolution-api.com/v2/api-reference/message/send-text
**Data:** 06/11/2025 23:28:56
**Total de Páginas:** 1

---

# Página 1: Recursos Disponíveis - Evolution API Documentation

**URL:** https://doc.evolution-api.com/v2/api-reference/message/send-text


# Recursos Disponíveis - Evolution API Documentation

## Recursos de Mensagens e Grupos

### Mensagens (Individuais ou em Grupo)

| Recurso | Disponibilidade | Descrição |
| --- | --- | --- |
| Envio de Texto | ✅   | (Texto simples, em negrito, itálico, riscado, em formato de código e emojis) |
| Envio de Mídia | ✅   | (Vídeo, imagem e documento) |
| Envio de Áudio Narrado | ✅   | (Funcionando bem no Android e iOS) |
| Envio de Localização | ✅   | (Com nome e descrição do local) |
| Envio de Contato | ✅   | (Com Nome, Empresa, Telefone, E-mail e URL) |
| Envio de Reação | ✅   | (Envie qualquer emoji para reação) |
| Envio de Pré-visualização de Link | ✅   | (Busca por informações de SEO) 🆕 |
| Envio de Resposta | ✅   | (Marcar mensagens em resposta) 🆕 |
| Envio de Menção | ✅   | (Individual, para alguns ou todos os membros) 🆕 |
| Envio de Enquete | ✅   | (Enviar e receber votos de uma enquete) 🆕 |
| Envio de Status/História | ✅   | (Texto, pré-visualização de link, vídeo, imagem e forma de onda) 🆕 |
| Envio de Adesivo | ✅   | (Imagem estática) 🆕 |
| Envio de Lista (Homologação) | ✅   | (Testando) |
| Envio de Botões (Descontinuado) | ❌   | (Só funciona na API em nuvem) |

### Perfil

| Recurso | Disponibilidade | Descrição |
| --- | --- | --- |
| Atualizar Nome | ✅   | (Alterar o nome do perfil conectado) |
| Atualizar Foto | ✅   | (Alterar a foto do perfil conectado) 🆕 |
| Atualizar Status | ✅   | (Alterar o status do perfil conectado) 🆕 |
| E muitos outros… |     |     |

### Grupo

| Recurso | Disponibilidade | Descrição |
| --- | --- | --- |
| Criar Grupo | ✅   | (Novos grupos) |
| Atualizar Foto | ✅   | (Alterar foto do grupo) |
| Atualizar Assunto | ✅   | (Alterar o nome do grupo) 🆕 |
| Atualizar Descrição | ✅   | (Alterar a descrição do grupo) 🆕 |
| Obter Todos os Grupos | ✅   | (Obter todos os grupos e participantes) 🆕 |
| E muitos outros… |     |     |


---

# Scraping Completo: doc

**URL Original:** https://doc.evolution-api.com/v2/api-reference/message/send-media
**Data:** 06/11/2025 23:30:47
**Total de Páginas:** 1

---

# Página 1: Recursos Disponíveis - Evolution API Documentation

**URL:** https://doc.evolution-api.com/v2/api-reference/message/send-media


# Recursos Disponíveis - Evolution API Documentation

## Recursos de Mensagens e Grupos

### Mensagens (Individuais ou em Grupo)

| Recurso | Disponibilidade | Descrição |
| --- | --- | --- |
| Envio de Texto | ✅   | (Texto simples, em negrito, itálico, riscado, em formato de código e emojis) |
| Envio de Mídia | ✅   | (Vídeo, imagem e documento) |
| Envio de Áudio Narrado | ✅   | (Funcionando bem no Android e iOS) |
| Envio de Localização | ✅   | (Com nome e descrição do local) |
| Envio de Contato | ✅   | (Com Nome, Empresa, Telefone, E-mail e URL) |
| Envio de Reação | ✅   | (Envie qualquer emoji para reação) |
| Envio de Pré-visualização de Link | ✅   | (Busca por informações de SEO) 🆕 |
| Envio de Resposta | ✅   | (Marcar mensagens em resposta) 🆕 |
| Envio de Menção | ✅   | (Individual, para alguns ou todos os membros) 🆕 |
| Envio de Enquete | ✅   | (Enviar e receber votos de uma enquete) 🆕 |
| Envio de Status/História | ✅   | (Texto, pré-visualização de link, vídeo, imagem e forma de onda) 🆕 |
| Envio de Adesivo | ✅   | (Imagem estática) 🆕 |
| Envio de Lista (Homologação) | ✅   | (Testando) |
| Envio de Botões (Descontinuado) | ❌   | (Só funciona na API em nuvem) |

### Perfil

| Recurso | Disponibilidade | Descrição |
| --- | --- | --- |
| Atualizar Nome | ✅   | (Alterar o nome do perfil conectado) |
| Atualizar Foto | ✅   | (Alterar a foto do perfil conectado) 🆕 |
| Atualizar Status | ✅   | (Alterar o status do perfil conectado) 🆕 |
| E muitos outros… |     |     |

### Grupo

| Recurso | Disponibilidade | Descrição |
| --- | --- | --- |
| Criar Grupo | ✅   | (Novos grupos) |
| Atualizar Foto | ✅   | (Alterar foto do grupo) |
| Atualizar Assunto | ✅   | (Alterar o nome do grupo) 🆕 |
| Atualizar Descrição | ✅   | (Alterar a descrição do grupo) 🆕 |
| Obter Todos os Grupos | ✅   | (Obter todos os grupos e participantes) 🆕 |
| E muitos outros… |     |     |


---

# Scraping Completo: doc

**URL Original:** https://doc.evolution-api.com/v2/api-reference/webhook/set
**Data:** 06/11/2025 23:32:20
**Total de Páginas:** 1

---

# Página 1: Set Webhook - Evolution API Documentation

**URL:** https://doc.evolution-api.com/v2/api-reference/webhook/set


# Set Webhook - Evolution API Documentation

#### Authorizations

Your authorization key header

#### Path Parameters

#### Body

enable webhook to instance

Enables Webhook by events

Sends files in base64 when available

Events to be sent to the Webhook

Minimum length: `1`

#### Response


---

