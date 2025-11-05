# 🚀 CRIAÇÃO AUTOMÁTICA - Planilha Google Sheets

## ⚡ TUDO AUTOMÁTICO EM 1 COMANDO!

Script que cria planilha completa e configurada:
- ✅ Cria planilha no Google Sheets
- ✅ Adiciona header formatado
- ✅ Preenche com horários disponíveis
- ✅ Formata colunas (largura ideal)
- ✅ Validação de dados (Status)
- ✅ Formatação condicional (cores)
- ✅ Torna pública automaticamente
- ✅ Retorna ID e link prontos

---

## 📋 PRÉ-REQUISITOS

### 1. Instalar Google API

```bash
pip install google-api-python-client google-auth
```

### 2. Obter Credenciais Google (Service Account)

**Passo a passo:**

1. **Criar projeto Google Cloud:**
   - Acesse: https://console.cloud.google.com
   - Criar novo projeto: `automaia-bot`

2. **Habilitar APIs:**
   - Google Sheets API
   - Google Drive API

3. **Criar Service Account:**
   - IAM & Admin → Service Accounts
   - Criar conta: `automaia-agenda-bot`
   - Role: `Editor`

4. **Gerar chave JSON:**
   - Clicar na conta criada
   - Keys → Add Key → Create new key
   - Tipo: JSON
   - Download automático

5. **Salvar credenciais:**
   ```bash
   mkdir -p config
   mv ~/Downloads/automaia-bot-*.json config/google_service_account.json
   ```

---

## 🎯 USO BÁSICO

### Criar Planilha Padrão

```bash
python3 componentes/escalonamento/criar_agenda_publica.py
```

**Cria:**
- Nome: "Agenda Automaia"
- Próximos 7 dias
- Vendedores: Bruno, Fernanda
- Horários: 10h, 14h, 15h, 16h
- Status: Pública (qualquer um pode editar)

---

## 🔧 USO AVANÇADO

### Nome Customizado

```bash
python3 componentes/escalonamento/criar_agenda_publica.py \
  --nome "Agenda Automaia 2025"
```

### Mais Dias

```bash
python3 componentes/escalonamento/criar_agenda_publica.py \
  --dias 14  # Próximas 2 semanas
```

### Vendedores Customizados

```bash
python3 componentes/escalonamento/criar_agenda_publica.py \
  --vendedores "Bruno,Fernanda,Carlos,Maria"
```

### Horários Customizados

```bash
python3 componentes/escalonamento/criar_agenda_publica.py \
  --horarios "09:00,10:00,14:00,15:00,16:00,17:00"
```

### Tudo Junto

```bash
python3 componentes/escalonamento/criar_agenda_publica.py \
  --nome "Agenda Completa 2025" \
  --dias 30 \
  --vendedores "Bruno,Fernanda,Carlos" \
  --horarios "09:00,10:30,14:00,15:30,17:00"
```

---

## 📊 O QUE O SCRIPT FAZ

### 1️⃣ Cria Planilha

```
Planilha: "Agenda Automaia"
Aba: "Agenda"
Congela: Primeira linha (header)
```

### 2️⃣ Adiciona Header Formatado

| Data | Hora | Vendedor | Status | Cliente | Veículo |
|------|------|----------|--------|---------|---------|

**Formatação:**
- Negrito
- Fundo cinza claro

### 3️⃣ Preenche Dados

```
06/11/2025 | 10:00 | Bruno | disponível
06/11/2025 | 14:00 | Bruno | disponível
06/11/2025 | 15:00 | Bruno | disponível
...
```

**Quantidade:** `(dias) × (horários/dia) × (vendedores)`

Exemplo: 7 dias × 4 horários × 2 vendedores = **56 linhas**

### 4️⃣ Ajusta Largura das Colunas

- Data: 120px
- Hora: 80px
- Vendedor: 100px
- Status: 120px
- Cliente: 150px
- Veículo: 120px

### 5️⃣ Validação de Dados (Dropdown)

**Coluna Status:**
- disponível
- agendado
- cancelado
- realizado

### 6️⃣ Formatação Condicional (Cores)

- 🟢 **Verde:** disponível
- 🟡 **Amarelo:** agendado
- 🔵 **Azul:** realizado
- 🔴 **Vermelho:** cancelado

### 7️⃣ Torna Pública

**Permissões:**
- Qualquer pessoa com o link
- Pode editar (writer)

---

## ✅ RESULTADO FINAL

```
🚀 CRIANDO PLANILHA DE AGENDA
====================================
📝 Nome: Agenda Automaia
📅 Dias: 7
👥 Vendedores: Bruno, Fernanda
⏰ Horários: 10:00, 14:00, 15:00, 16:00

1️⃣ Criando planilha...
✅ Planilha criada: 1A2B3C4D5E6F7G8H9I0J

2️⃣ Adicionando header...
✅ Header adicionado

3️⃣ Adicionando horários disponíveis...
✅ 56 horários adicionados

4️⃣ Formatando colunas...
✅ Colunas formatadas

5️⃣ Adicionando validação de status...
✅ Validação adicionada (coluna Status)

6️⃣ Adicionando formatação condicional...
✅ Formatação condicional adicionada

7️⃣ Tornando planilha pública...
✅ Planilha pública (qualquer pessoa com link pode editar)

====================================
✅ PLANILHA CRIADA COM SUCESSO!
====================================

📊 ID: 1A2B3C4D5E6F7G8H9I0J
🔗 Link: https://docs.google.com/spreadsheets/d/1A2B3C4D5E6F7G8H9I0J/edit

💾 Salvar ID no config:
   "google_sheet_id": "1A2B3C4D5E6F7G8H9I0J"

🔧 Quer configurar automaticamente no bot? (s/n): s

✅ ID salvo em: chatwoot_config_automaia.json
🔄 Reinicie o bot para aplicar
```

---

## 🔄 CONFIGURAÇÃO AUTOMÁTICA

**O script pergunta ao final:**
```
🔧 Quer configurar automaticamente no bot? (s/n): s
```

**Se responder 's':**
- ✅ Salva ID no `chatwoot_config_automaia.json`
- ✅ Bot já usa agenda real após reiniciar

**Se responder 'n':**
- ℹ️ Copiar ID manualmente
- ℹ️ Editar config depois

---

## 🐛 SOLUÇÃO DE PROBLEMAS

### Erro: Credenciais não encontradas

```
❌ Credenciais Google não encontradas: config/google_service_account.json
```

**Solução:**
1. Criar Service Account (ver seção Pré-requisitos)
2. Baixar JSON
3. Salvar em: `config/google_service_account.json`

### Erro: Google API não instalada

```
❌ Google API não instalada
Instale: pip install google-api-python-client google-auth
```

**Solução:**
```bash
pip install google-api-python-client google-auth
```

### Erro: Permission denied

```
❌ googleapiclient.errors.HttpError: 403 Forbidden
```

**Solução:**
1. Verificar se APIs estão habilitadas:
   - Google Sheets API
   - Google Drive API
2. Verificar permissões do Service Account
3. Aguardar 1-2 minutos (propagação)

---

## 📚 DEPOIS DE CRIAR

### 1. Abrir Planilha

Clique no link fornecido:
```
https://docs.google.com/spreadsheets/d/[ID]/edit
```

### 2. Configurar Bot

**Manual:**
```json
// chatwoot_config_automaia.json
{
  "google_sheet_id": "COLAR_ID_AQUI"
}
```

**Ou deixar o script configurar automaticamente (resposta 's')**

### 3. Reiniciar Bot

```bash
./PARAR_BOT_AUTOMAIA.sh
./INICIAR_COM_NGROK.sh
```

### 4. Testar

```
Cliente: "quero agendar"
Bot: Mostra horários da planilha real ✅
```

---

## 🔒 SEGURANÇA

### Planilha Pública

✅ **Vantagens:**
- Fácil compartilhar com equipe
- Não precisa adicionar emails
- Acesso imediato

⚠️ **Cuidados:**
- Qualquer um com link pode editar
- Não compartilhar link publicamente
- Usar só com equipe confiável

### Alternativa: Compartilhar por Email

**Modificar script (linha 292):**
```python
# Em vez de:
permission = {'type': 'anyone', 'role': 'writer'}

# Usar:
permission = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': 'vendedor@empresa.com'
}
```

---

## 📱 VENDEDOR USA NO CELULAR

**App Google Sheets:**
1. Download (App Store / Play Store)
2. Abrir link da planilha
3. Editar direto no celular

**Acesso via navegador:**
1. Abrir link no celular
2. Funciona em qualquer navegador

---

## 🔄 MANUTENÇÃO

### Adicionar Mais Horários (Semanal)

```bash
python3 componentes/escalonamento/atualizar_agenda.py \
  --sheet-id "ID_DA_PLANILHA" \
  --dias 7 \
  --limpar
```

### Limpar Horários Passados

```bash
python3 componentes/escalonamento/atualizar_agenda.py \
  --sheet-id "ID_DA_PLANILHA" \
  --limpar
```

---

## 💡 DICAS

✅ **Criar nova planilha a cada mês**
✅ **Compartilhar link com toda equipe**
✅ **Adicionar horários toda semana (script automático)**
✅ **Usar formatação condicional pra visualizar status**

❌ **NÃO compartilhar link publicamente na internet**
❌ **NÃO deletar planilha sem backup**

---

## 🎯 COMPARAÇÃO: Manual vs Automático

| Aspecto | Manual | Script Automático |
|---------|--------|-------------------|
| **Tempo** | 15-20 min | 30 segundos |
| **Erros** | Comum | Zero |
| **Formatação** | Manual | Perfeita |
| **Validação** | Não tem | Automática |
| **Cores** | Manual | Automática |
| **Configuração bot** | Manual | Opção automática |

---

## 📞 SUPORTE

**Problemas com credenciais?**
- Ver: `GOOGLE_SETUP.md`

**Quer usar template manual?**
- Ver: `README_AGENDA_RAPIDA.md`

**Dúvidas sobre a planilha?**
- Ver: `PLANILHA_AGENDA_TEMPLATE.md`

---

**✅ TUDO PRONTO EM 1 COMANDO!** 🚀
