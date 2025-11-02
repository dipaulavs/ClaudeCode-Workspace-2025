# 🏠 SISTEMA DE GESTÃO DE IMÓVEIS - BOT WHATSAPP

Sistema completo para gerenciar imóveis e enviar fotos automaticamente via WhatsApp.

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Estrutura de Arquivos](#estrutura-de-arquivos)
3. [Adicionar Novo Imóvel](#adicionar-novo-imóvel)
4. [Como o Bot Funciona](#como-o-bot-funciona)
5. [Comandos Úteis](#comandos-úteis)

---

## 🎯 Visão Geral

O bot agora possui um **banco de dados de imóveis** completo com:

- ✅ Descrições detalhadas
- ✅ Localização
- ✅ FAQ com perguntas frequentes
- ✅ Fotos hospedadas no Nextcloud
- ✅ Envio automático de fotos via WhatsApp

---

## 📂 Estrutura de Arquivos

```
n8n-mcp-project/
├── imoveis/                          # Banco de dados de imóveis
│   ├── exemplo-001/                  # Cada imóvel tem sua pasta
│   │   ├── descricao.txt            # Descrição completa
│   │   ├── localizacao.txt          # Endereço e proximidades
│   │   ├── faq.txt                  # Perguntas frequentes
│   │   └── links.json               # Links das fotos (gerado automaticamente)
│   │
│   └── imovel-002/
│       ├── descricao.txt
│       ├── localizacao.txt
│       ├── faq.txt
│       └── links.json
│
├── upload_fotos_imoveis.py          # Script para upload de fotos
└── chatbot_corretor_v4.py           # Bot principal
```

---

## ➕ Adicionar Novo Imóvel

### PASSO 1: Organize as Fotos

Crie uma pasta no Desktop com as fotos do imóvel:

```bash
mkdir -p ~/Desktop/"fotos de imoveis"/imovel-002
```

Adicione as fotos:
```bash
# Copie suas fotos para a pasta
cp foto1.jpg ~/Desktop/"fotos de imoveis"/imovel-002/
cp foto2.jpg ~/Desktop/"fotos de imoveis"/imovel-002/
cp foto3.jpg ~/Desktop/"fotos de imoveis"/imovel-002/
```

### PASSO 2: Faça Upload das Fotos

Execute o script de upload:

```bash
cd ~/Desktop/ClaudeCode-Workspace/n8n-mcp-project
python3 upload_fotos_imoveis.py
```

O script irá:
1. ✅ Fazer upload de todas as fotos para o Nextcloud
2. ✅ Gerar links públicos permanentes
3. ✅ Criar estrutura de pastas em `imoveis/`
4. ✅ Salvar links em `links.json`
5. ✅ Criar templates dos arquivos `.txt`

### PASSO 3: Edite as Informações

Edite os arquivos criados automaticamente:

**`imoveis/imovel-002/descricao.txt`**
```txt
# DESCRIÇÃO DO IMÓVEL: imovel-002

Casa espaçosa de 3 quartos em condomínio fechado.

Características:
- 3 quartos (2 suítes)
- 3 banheiros
- Sala ampla com pé-direito duplo
- Cozinha gourmet
- Quintal com churrasqueira
- 2 vagas de garagem
- 120m² de área construída

Estado: Pronto para morar
Mobiliado: Não
IPTU: R$ 250/mês
Condomínio: R$ 600/mês
```

**`imoveis/imovel-002/localizacao.txt`**
```txt
# LOCALIZAÇÃO: imovel-002

Endereço: Rua das Flores, 456
Bairro: Buritis
Cidade: Belo Horizonte
Estado: MG
CEP: 30455-000

Proximidades:
- 10 min do Shopping Cidade
- Próximo ao Parque Municipal
- Escolas e supermercados na região
```

**`imoveis/imovel-002/faq.txt`**
```txt
# FAQ: imovel-002

## Qual o valor?
R$ 750.000,00

## Aceita financiamento?
Sim! Aceita financiamento bancário.

## Tem quintal?
Sim, quintal espaçoso com churrasqueira.

## Aceita pets?
Sim, o condomínio aceita pets.
```

### PASSO 4: Reinicie o Bot

Para carregar o novo imóvel:

```bash
./PARAR_BOT_V4.sh
./INICIAR_BOT_V4.sh
```

Ou simplesmente:

```bash
./PARAR_BOT_V4.sh && ./INICIAR_BOT_V4.sh
```

---

## 🤖 Como o Bot Funciona

### Carregamento Automático

Ao iniciar, o bot:
1. 📂 Lê todos os diretórios em `imoveis/`
2. 📝 Carrega descrições, localização e FAQ
3. 📸 Carrega links das fotos do `links.json`
4. 🧠 Memoriza tudo para responder perguntas

### Interação com Cliente

**Exemplo 1: Cliente pede fotos**
```
Cliente: "Me mostra as fotos do apartamento"

Bot processa:
  🔍 Identifica pedido de fotos
  🏠 Localiza imóvel relevante
  💬 Responde: "Olha só! Esse apê é top 😍"
  📸 Envia fotos automaticamente
```

**Exemplo 2: Cliente pergunta sobre localização**
```
Cliente: "Onde fica esse imóvel?"

Bot processa:
  🔍 Consulta localizacao.txt
  💬 Responde: "Fica na Savassi, perto da Praça! 📍"
```

**Exemplo 3: Cliente pergunta sobre valor**
```
Cliente: "Quanto custa?"

Bot processa:
  🔍 Consulta faq.txt
  💬 Responde: "R$ 450 mil, mas rola negociar! 😊"
```

### Comando Especial: `[ENVIAR_FOTOS:ID]`

O bot usa um comando interno para enviar fotos:

```
Bot gera: "Olha só! Esse apê é demais! [ENVIAR_FOTOS:exemplo-001]"

Sistema detecta comando e:
  ✅ Remove [ENVIAR_FOTOS:exemplo-001] da mensagem
  ✅ Envia texto: "Olha só! Esse apê é demais!"
  ✅ Envia todas as fotos do exemplo-001 automaticamente
```

---

## 🛠️ Comandos Úteis

### Verificar Status do Bot

```bash
curl -s http://localhost:5001/health | python3 -m json.tool
```

Retorna:
```json
{
  "status": "online",
  "version": "4.3 - CORRETOR COMPLETO!",
  "imoveis": {
    "total": 2,
    "total_fotos": 8,
    "ids": ["exemplo-001", "imovel-002"]
  }
}
```

### Listar Imóveis Carregados

```bash
ls -la imoveis/
```

### Ver Logs em Tempo Real

```bash
tail -f logs/chatbot_v4.log
```

### Testar Upload Individual

```bash
python3 /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/tools/upload_to_nextcloud.py foto.jpg --permanent
```

---

## 📸 Gestão de Fotos

### Limites

- **Máximo por imóvel**: 10 fotos
- **Bot envia**: Até 5 fotos por vez (evita spam)
- **Formato**: JPG, JPEG, PNG
- **Tamanho**: Ilimitado (Nextcloud)

### Links Permanentes

Fotos são hospedadas com links **permanentes** que:
- ✅ Nunca expiram
- ✅ Terminam em `.jpg` (compatível com WhatsApp)
- ✅ Podem ser usados múltiplas vezes

### Atualizar Fotos

Para atualizar fotos de um imóvel:

1. Adicione novas fotos em `~/Desktop/fotos de imoveis/imovel-ID/`
2. Execute `python3 upload_fotos_imoveis.py`
3. Reinicie o bot

---

## 🎯 Recursos Avançados

### Busca Inteligente

O bot identifica imóveis por:
- **ID direto**: "exemplo-001", "imovel-002"
- **Palavras-chave**: "apartamento", "casa", "2 quartos"
- **Contexto**: Se tem apenas 1 imóvel, sempre fala dele

### Múltiplos Imóveis

Com vários imóveis, o bot:
- Lista opções disponíveis
- Pergunta qual cliente prefere
- Mostra fotos do imóvel escolhido

### Contexto de 14 Dias

O bot lembra de:
- ✅ Conversas anteriores
- ✅ Imóveis que o cliente já viu
- ✅ Preferências demonstradas

---

## ⚠️ Troubleshooting

### Bot não carrega imóveis

```bash
# Verificar estrutura
ls -R imoveis/

# Verificar logs
tail -f logs/chatbot_v4.log | grep "Carregando"
```

### Fotos não enviam

1. Verifique se `links.json` existe e tem fotos
2. Teste link manualmente no navegador
3. Verifique logs: `tail -f logs/chatbot_v4.log`

### Upload falha

```bash
# Testar conexão Nextcloud
curl -u "dipaula:senha" https://media.loop9.com.br/status.php
```

---

## 📝 Exemplo Completo

### Estrutura Final de um Imóvel

```
imoveis/apartamento-savassi-001/
├── descricao.txt          # 500 caracteres de descrição
├── localizacao.txt        # Endereço completo
├── faq.txt                # 5-10 perguntas frequentes
└── links.json             # {"id": "...", "fotos": [{link, nome, ordem}]}
```

### Interação Real

```
👤 Cliente: "Oi, tudo bem?"
🤖 Bot: "Eae! Tudo certo por aqui! 😊 E aí, procurando imóvel?"

👤 Cliente: "Sim! Tem algum apartamento disponível?"
🤖 Bot: "Tenho sim! Apê top na Savassi, 2 quartos. Quer ver fotos?"

👤 Cliente: "Quero!"
🤖 Bot: "Olha só! Esse apê é demais! 😍"
      [Envia 5 fotos automaticamente]

👤 Cliente: "Quanto custa?"
🤖 Bot: "R$ 450 mil, mas rola negociar! 💰"

👤 Cliente: "Posso visitar?"
🤖 Bot: "Claro! Segunda a sábado, 9h-18h. Agenda comigo! 📅"
```

---

## 🚀 Próximos Passos

1. ✅ **Sistema está funcionando!**
2. 📸 **Adicione fotos reais** dos seus imóveis
3. 📝 **Edite descrições** com informações corretas
4. 🧪 **Teste** enviando mensagens no WhatsApp
5. 🔄 **Ajuste respostas** conforme necessário

---

## 📞 Suporte

- **Logs**: `tail -f logs/chatbot_v4.log`
- **Status**: `curl http://localhost:5001/health`
- **Parar bot**: `./PARAR_BOT_V4.sh`
- **Iniciar bot**: `./INICIAR_BOT_V4.sh`

---

**Bot Versão**: 4.3 - CORRETOR COMPLETO!
**Recursos**: Áudio + Visão + Imóveis + Fotos
**Status**: ✅ Online e funcionando!
