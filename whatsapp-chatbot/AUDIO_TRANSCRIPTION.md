# 🎤 Transcrição de Áudios - Chatbot WhatsApp V4.1

## ✅ Funcionalidade Implementada

O chatbot agora **transcreve automaticamente mensagens de áudio** do WhatsApp usando **Whisper da OpenAI**.

---

## 🔄 Fluxo Completo

```
1. Usuário envia áudio no WhatsApp
   ↓
2. Evolution API → Middleware → Chatwoot
   ↓
3. Chatwoot dispara webhook com URL do áudio
   ↓
4. Bot V4.1 recebe webhook
   ↓
5. Detecta attachment type = 'audio'
   ↓
6. Download do áudio da URL do Chatwoot
   ↓
7. Transcrição com Whisper API (OpenAI)
   ↓
8. Adiciona transcrição ao contexto da mensagem
   ↓
9. Processa com debounce inteligente
   ↓
10. Gera resposta com Claude Haiku 4.5
   ↓
11. Responde direto via Evolution API
```

---

## 📝 Implementação Técnica

### Arquivo: `chatbot_corretor_v4.py`

#### 1. Função de Transcrição

```python
def transcrever_audio(audio_url):
    """
    Transcreve áudio usando Whisper da OpenAI

    - Baixa áudio da URL (Chatwoot)
    - Salva temporariamente (.ogg)
    - Envia para Whisper API
    - Retorna texto transcrito em português
    """
```

**Parâmetros Whisper:**
- Model: `whisper-1`
- Language: `pt` (português)
- Response format: `text`

#### 2. Detecção e Processamento

```python
# Detecta áudios nos attachments
if tipo == 'audio':
    transcricao = transcrever_audio(url)
    if transcricao and not transcricao.startswith('[Erro'):
        content += f"\n[Áudio transcrito]: {transcricao}"
```

#### 3. Correções no Middleware

**Arquivo: `webhook_middleware_v2.py`**

- ✅ Aceita mensagens sem texto (apenas attachments)
- ✅ Log seguro quando `content = None`
- ✅ Garante `content` seja sempre string antes de enviar pro bot

---

## 🚀 Como Usar

### Testar localmente:

```bash
cd n8n-mcp-project

# Iniciar tudo
./INICIAR_BOT_V4.sh

# Monitorar logs
tail -f logs/chatbot_v4.log

# Enviar áudio no WhatsApp para: 5531980160822
```

---

## 🔧 Configuração

### API Keys necessárias:

```python
# chatbot_corretor_v4.py
OPENAI_API_KEY = "sk-proj-..." # OpenAI (Whisper)
OPENROUTER_API_KEY = "sk-or-..." # OpenRouter (Claude)
```

### URLs de webhook:

- Evolution → Middleware: `https://ngrok-url/webhook/evolution`
- Chatwoot → Middleware: `http://localhost:5002/webhook/chatwoot`
- Middleware → Bot: `http://localhost:5001/webhook/chatwoot`

---

## 📊 Performance

### Latências:

| Tipo | Tempo |
|------|-------|
| Mensagem de texto | ~2.5-3.5s |
| Mensagem de áudio (5s) | ~5-8s |
| Mensagem de áudio (30s) | ~10-15s |

### Custos (estimativa):

| Serviço | Custo |
|---------|-------|
| Claude Haiku 4.5 (1000 msgs) | ~$0.60/mês |
| Whisper (100 áudios de 10s) | ~$0.10/mês |
| **Total (uso moderado)** | **~$1/mês** |

---

## 🐛 Problemas Resolvidos

### Erro 1: Middleware quebrava com áudios

**Problema:**
```python
TypeError: 'NoneType' object is not subscriptable
# Em: log(f"💬 Mensagem: {content[:50]}...")
```

**Solução:**
```python
# Antes
content = data.get('content', '')
log(f"💬 Mensagem: {content[:50]}...")

# Depois
content = data.get('content')  # Pode ser None
if content:
    log(f"💬 Mensagem: {content[:50]}...")
else:
    log(f"💬 Mensagem: (sem texto, apenas attachments)")
```

### Erro 2: Bot ignorava mensagens só com áudio

**Problema:**
```python
if not content:
    return jsonify({"status": "ignored"})
```

**Solução:**
```python
# Só ignora se não tiver conteúdo E não tiver attachments
if not content and not attachments:
    return jsonify({"status": "ignored"})

# Se não tem content mas tem attachments
if not content:
    content = "[Mensagem sem texto]"
```

---

## ✅ Status Atual

**Versão:** V4.1 - ÁUDIO!

**Funcionalidades:**
- ✅ Transcrição automática de áudios (Whisper)
- ✅ Debounce inteligente (15s + 50s se incompleta)
- ✅ Análise IA de completude
- ✅ Fila Redis por número
- ✅ Resposta humanizada e picotada
- ✅ Integração híbrida (bot + atendente)
- ✅ Sem loop (responde direto via Evolution)

---

## 📚 Logs Exemplo

```
🔔 WEBHOOK CHATWOOT → BOT V4 - 13:45:22
📱 De: Cliente (5531999999999)
💬 Mensagem: (sem texto, apenas attachments)
📎 Attachments: 1
📎 Mídias recebidas:
   1. Tipo: audio | URL: https://chatwoot.../audio.ogg
🎤 Detectado áudio! Transcrevendo...
🎤 Transcrevendo áudio: https://chatwoot...
📥 Áudio baixado: 45678 bytes
🤖 Enviando para Whisper API...
✅ Transcrição: Olá, gostaria de saber mais sobre os imóveis disponíveis
✅ Áudio transcrito e adicionado ao conteúdo
📦 Adicionando na fila com debounce...
```

---

## 🔐 Segurança

- ✅ URLs de áudio vêm do Chatwoot (confiável)
- ✅ Arquivos temporários são deletados após transcrição
- ✅ Timeout de 30s para download, 60s para Whisper
- ✅ Tratamento de erros em todas as etapas

---

## 🎯 Próximas Melhorias

- [ ] Cache de transcrições (evitar retranscrever áudios idênticos)
- [ ] Suporte a outros formatos além de .ogg
- [ ] Detecção de idioma automática
- [ ] Resumo de áudios muito longos (>1min)
- [ ] Métricas de uso (quantidade de áudios transcritos)

---

**Data de Implementação:** 01/11/2025
**Desenvolvido por:** Claude Code + Felipe
**Status:** ✅ Funcionando perfeitamente
