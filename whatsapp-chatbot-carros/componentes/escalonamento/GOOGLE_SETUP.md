# 📅 Configuração Google Sheets API

Instruções para integrar consulta de agenda com Google Sheets real (sem MOCK).

---

## 🎯 Visão Geral

Por padrão, o sistema usa **modo MOCK** (dados simulados). Para usar Google Sheets real:

1. Criar Service Account no Google Cloud
2. Baixar credenciais JSON
3. Criar planilha de agenda
4. Configurar permissões
5. Ativar no código

**Custo:** GRÁTIS (Google Sheets API)

---

## 📋 Passo a Passo

### 1️⃣ Criar Service Account

1. Acesse: https://console.cloud.google.com/
2. Crie novo projeto (ou use existente)
3. Ative **Google Sheets API**:
   - Menu: APIs & Services → Library
   - Busque: "Google Sheets API"
   - Clique: Enable

4. Crie Service Account:
   - Menu: APIs & Services → Credentials
   - Clique: "Create Credentials" → "Service Account"
   - Nome: `chatbot-whatsapp-agenda`
   - Role: Editor
   - Clique: Done

5. Crie chave JSON:
   - Clique no Service Account criado
   - Aba: Keys
   - Clique: "Add Key" → "Create new key"
   - Tipo: JSON
   - Download: `service-account-key.json`

---

### 2️⃣ Salvar Credenciais

Coloque o arquivo JSON em:

```bash
/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot/config/google_service_account.json
```

**⚠️ IMPORTANTE:** Adicione ao `.gitignore`:

```bash
# .gitignore
config/google_service_account.json
```

---

### 3️⃣ Instalar Bibliotecas Google

```bash
pip install google-api-python-client google-auth
```

---

### 4️⃣ Criar Planilha de Agenda

1. Acesse: https://docs.google.com/spreadsheets/
2. Crie nova planilha: "Agenda Visitas"
3. Crie aba: "Agenda"

**Estrutura (colunas):**

```
A: Data (DD/MM/YYYY)
B: Hora (HH:MM)
C: Corretor
D: Status (disponível / agendado / ocupado)
E: Cliente (se agendado)
F: Imóvel (se agendado)
```

**Exemplo:**

| Data       | Hora  | Corretor | Status      | Cliente      | Imóvel   |
|------------|-------|----------|-------------|--------------|----------|
| 05/11/2025 | 10:00 | Bruno    | disponível  |              |          |
| 05/11/2025 | 14:00 | Bruno    | disponível  |              |          |
| 05/11/2025 | 15:00 | Bruno    | agendado    | 5531980160822 | apto-001 |
| 06/11/2025 | 10:00 | Fernanda | disponível  |              |          |

---

### 5️⃣ Compartilhar Planilha

1. Abra o arquivo `google_service_account.json`
2. Copie o valor do campo `"client_email"`
   - Exemplo: `chatbot-whatsapp@projeto-12345.iam.gserviceaccount.com`

3. Na planilha Google Sheets:
   - Clique: Compartilhar (Share)
   - Cole o email do Service Account
   - Permissão: **Editor**
   - Clique: Done

---

### 6️⃣ Pegar Sheet ID

Na URL da planilha:

```
https://docs.google.com/spreadsheets/d/1ABcDEfGhIjKlMnOpQrStUvWxYz/edit
                                  ^^^^^^^^^^^^^^^^^^^^^^^^
                                  Este é o SHEET_ID
```

Copie o `SHEET_ID`.

---

### 7️⃣ Configurar no Código

Edite `config/config.py`:

```python
# Google Sheets
GOOGLE_SHEET_ID = "1ABcDEfGhIjKlMnOpQrStUvWxYz"  # Cole aqui
```

---

### 8️⃣ Ativar no Código

Edite `componentes/escalonamento/integrador.py`:

```python
# Linha 18: Altere de True para False
self.agenda = ConsultaAgenda(use_mock=False)  # ✅ Ativa Google API
```

---

## 🧪 Testar Integração

```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/whatsapp-chatbot
python3 -c "
from componentes.escalonamento import ConsultaAgenda

agenda = ConsultaAgenda(use_mock=False)
horarios = agenda.buscar_horarios_disponiveis()

print('✅ Integração OK!')
print(f'Horários encontrados: {len(horarios)}')
for h in horarios:
    print(f'  • {h[\"data_formatada\"]} às {h[\"hora\"]} ({h[\"corretor\"]})')
"
```

**Saída esperada:**

```
✅ Integração OK!
Horários encontrados: 3
  • 05/11 (ter) às 10:00 (Bruno)
  • 05/11 (ter) às 14:00 (Bruno)
  • 06/11 (qua) às 10:00 (Fernanda)
```

---

## 📊 Gerenciar Agenda

### Adicionar Horários Disponíveis

Basta adicionar linhas na planilha:

```
05/11/2025 | 16:00 | Bruno | disponível | |
```

### Marcar Como Ocupado

Mude status:

```
05/11/2025 | 10:00 | Bruno | ocupado | |
```

### Agendamento Manual

Preencha todas colunas:

```
05/11/2025 | 14:00 | Bruno | agendado | 5531999999999 | apto-002
```

---

## 🔒 Segurança

### ⚠️ Nunca Commite Credenciais

```bash
# Verifique se está no .gitignore:
cat .gitignore | grep google_service_account.json
```

### Permissões Mínimas

Service Account só precisa de:
- **Google Sheets API**: Enabled
- **Role**: Editor (apenas na planilha específica)

---

## 🐛 Troubleshooting

### Erro: "google module not found"

**Solução:**

```bash
pip install google-api-python-client google-auth
```

---

### Erro: "Permission denied"

**Causa:** Service Account não tem acesso à planilha

**Solução:** Compartilhe planilha com email do Service Account (ver passo 5)

---

### Erro: "Invalid credentials"

**Causa:** JSON incorreto ou corrompido

**Solução:** Baixe novamente o JSON do Google Cloud Console

---

### Modo MOCK ativado automaticamente

**Causa:** Sistema detecta erro e usa fallback

**Logs:**

```
⚠️ Credenciais Google não encontradas. Usando MOCK mode.
```

**Solução:** Verifique se:
- JSON está em `config/google_service_account.json`
- Bibliotecas instaladas
- Planilha compartilhada

---

## 🔄 Migração Futura (Google Calendar)

**Próxima versão** irá migrar para Google Calendar API (mais robusto):

- Suporte a eventos recorrentes
- Sincronização com calendários externos (Outlook, iOS)
- Notificações automáticas por email
- Conflitos de horário detectados automaticamente

**Preparação:** Mesmo Service Account funcionará para Calendar API.

---

## 📚 Referências

- [Google Sheets API Docs](https://developers.google.com/sheets/api)
- [Service Account Auth](https://cloud.google.com/iam/docs/service-accounts)
- [Python Quickstart](https://developers.google.com/sheets/api/quickstart/python)

---

**Documentação completa** | Versão 1.0 | Última atualização: 04/11/2025
