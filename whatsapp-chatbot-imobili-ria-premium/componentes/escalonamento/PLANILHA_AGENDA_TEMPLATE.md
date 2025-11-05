# 📅 PLANILHA DE AGENDA - Google Sheets Imobiliária Premium

## 📋 ESTRUTURA DA PLANILHA

### Aba 1: "Agenda" (Principal)

| A | B | C | D | E | F |
|---|---|---|---|---|---|
| **Data** | **Hora** | **Vendedor** | **Status** | **Cliente** | **Veículo** |
| 06/11/2025 | 10:00 | Bruno | disponível | - | - |
| 06/11/2025 | 14:00 | Bruno | disponível | - | - |
| 06/11/2025 | 15:00 | Bruno | disponível | - | - |
| 06/11/2025 | 16:00 | Fernanda | disponível | - | - |
| 07/11/2025 | 10:00 | Bruno | disponível | - | - |
| 07/11/2025 | 14:00 | Fernanda | disponível | - | - |
| 07/11/2025 | 15:00 | Bruno | agendado | João Silva | Civic 2018 |
| 07/11/2025 | 16:00 | Bruno | disponível | - | - |

### Aba 2: "Configuração" (Opcional)

| A | B |
|---|---|
| **Parâmetro** | **Valor** |
| Horário Início | 09:00 |
| Horário Fim | 18:00 |
| Intervalo (min) | 60 |
| Dias Antecedência | 7 |

---

## 🎯 COLUNAS OBRIGATÓRIAS

### Coluna A: **Data** (DD/MM/YYYY)
- Formato: `06/11/2025`
- SEMPRE usar barra (`/`)
- Ano com 4 dígitos

### Coluna B: **Hora** (HH:MM)
- Formato: `10:00` ou `14:30`
- SEMPRE com dois pontos (`:`)
- Formato 24h

### Coluna C: **Vendedor**
- Nome do vendedor responsável
- Exemplos: `Bruno`, `Fernanda`, `Carlos`

### Coluna D: **Status**
- Valores permitidos:
  - `disponível` - Horário livre
  - `agendado` - Horário ocupado
  - `cancelado` - Cliente cancelou
  - `realizado` - Visita já aconteceu

### Coluna E: **Cliente** (Preenchido após agendamento)
- Nome do cliente ou número de telefone
- Pode ficar vazio se status = disponível

### Coluna F: **Veículo** (Preenchido após agendamento)
- Carro de interesse do cliente
- Exemplo: `Civic 2018`, `Gol 2020`

---

## 🚀 COMO CRIAR A PLANILHA

### Passo 1: Criar no Google Sheets

1. Acesse: https://sheets.google.com
2. Clique em "Em branco" (nova planilha)
3. Renomeie para: `Agenda Automaia`

### Passo 2: Configurar Abas

**Aba 1: "Agenda"**
- Renomear primeira aba para `Agenda`
- Copiar estrutura acima (colunas A-F)
- Linha 1 = Header (negrito)
- Linha 2+ = Dados

**Header (Linha 1):**
```
A1: Data
B1: Hora
C1: Vendedor
D1: Status
E1: Cliente
F1: Veículo
```

### Passo 3: Formatar Células

**Coluna A (Data):**
- Selecionar coluna A
- Formato → Número → Data personalizada: `DD/MM/YYYY`

**Coluna B (Hora):**
- Selecionar coluna B
- Formato → Número → Hora personalizada: `HH:MM`

**Coluna D (Status):**
- Criar validação de dados:
  - Selecionar coluna D (de D2 até D100)
  - Dados → Validação de dados
  - Critério: Lista de opções
  - Opções: `disponível,agendado,cancelado,realizado`

### Passo 4: Preencher Dados Iniciais

**Gerar horários da semana:**
```
Copie e cole:

06/11/2025 | 10:00 | Bruno | disponível
06/11/2025 | 14:00 | Bruno | disponível
06/11/2025 | 15:00 | Bruno | disponível
06/11/2025 | 16:00 | Bruno | disponível
07/11/2025 | 10:00 | Fernanda | disponível
07/11/2025 | 14:00 | Fernanda | disponível
07/11/2025 | 15:00 | Fernanda | disponível
07/11/2025 | 16:00 | Fernanda | disponível
```

---

## 🔗 TORNAR PÚBLICA/COMPARTILHADA

### Opção 1: Acesso Público (Recomendado para testes)

1. Clicar em **Compartilhar** (canto superior direito)
2. Em "Acesso geral" → Mudar para: **"Qualquer pessoa com o link"**
3. Permissão: **"Leitor"** (só visualizar) ou **"Editor"** (editar)
4. Copiar link: `https://docs.google.com/spreadsheets/d/[ID]/edit`

### Opção 2: Compartilhar com Service Account (Produção)

1. Criar Service Account no Google Cloud
2. Compartilhar planilha com email do Service Account
3. Dar permissão de "Editor"

**Email do Service Account:**
```
exemplo-bot@projeto-12345.iam.gserviceaccount.com
```

---

## 🔧 CONECTAR NO BOT

### Passo 1: Extrair ID da Planilha

**Da URL:**
```
https://docs.google.com/spreadsheets/d/1A2B3C4D5E6F7G8H9I0J/edit
                                        ^^^^^^^^^^^^^^^^^^^^
                                        Copiar este ID
```

### Passo 2: Configurar no Código

**Arquivo:** `componentes/escalonamento/integrador.py`

```python
# Linha 26 - Trocar:
self.agenda = ConsultaAgenda(use_mock=True)

# Por:
self.agenda = ConsultaAgenda(
    use_mock=False,
    sheet_id="1A2B3C4D5E6F7G8H9I0J"  # ID da sua planilha
)
```

### Passo 3: Configurar Credenciais Google

**Criar Service Account:**

1. Acesse: https://console.cloud.google.com
2. Criar projeto: `automaia-bot`
3. Habilitar API: **Google Sheets API**
4. Criar credenciais:
   - Tipo: Service Account
   - Nome: `automaia-agenda-bot`
   - Role: Editor
5. Baixar JSON de credenciais

**Salvar credenciais:**
```bash
# Criar pasta config
mkdir -p config

# Salvar JSON
mv ~/Downloads/automaia-bot-*.json config/google_service_account.json
```

**Compartilhar planilha:**
- Abrir planilha Google Sheets
- Compartilhar com email do Service Account
- Dar permissão: **Editor**

---

## 📝 COMO O VENDEDOR USA

### 1️⃣ Adicionar Novos Horários

**Manual:**
- Abrir planilha
- Adicionar linha nova
- Preencher: Data, Hora, Vendedor, Status=`disponível`

**Exemplo:**
```
08/11/2025 | 10:00 | Bruno | disponível
```

### 2️⃣ Ver Agendamentos

**Filtrar por Status:**
- Clicar em coluna D (Status)
- Dados → Criar filtro
- Filtrar por: `agendado`

**Ver apenas hoje:**
- Filtrar coluna A (Data)
- Escolher data de hoje

### 3️⃣ Marcar Visita Realizada

Após visita acontecer:
- Localizar linha do agendamento
- Trocar Status: `agendado` → `realizado`

### 4️⃣ Cancelar Agendamento

Se cliente cancelar:
- Trocar Status: `agendado` → `cancelado`
- Limpar colunas E e F (Cliente e Veículo)

---

## 🤖 COMO O BOT USA

### Workflow Automático:

```
1. Cliente pede: "quero agendar"
   ↓
2. Bot consulta planilha:
   - Busca linhas com Status="disponível"
   - Filtra próximos 3 dias
   - Pega 3 primeiros horários
   ↓
3. Bot mostra: "1️⃣ 06/11 10h | 2️⃣ 06/11 14h | 3️⃣ 07/11 10h"
   ↓
4. Cliente escolhe: "a 2"
   ↓
5. Bot atualiza planilha:
   - Status: disponível → agendado
   - Cliente: 5531999999999
   - Veículo: Civic 2018
   ↓
6. Bot notifica vendedor via WhatsApp
```

### Atualização Automática:

**Quando bot agenda:**
- ✅ Status muda para `agendado`
- ✅ Cliente preenchido
- ✅ Veículo preenchido

**O que o vendedor deve fazer:**
- ❌ NÃO precisa mudar nada
- ✅ Só conferir agendamentos diários
- ✅ Marcar como `realizado` após visita

---

## 📊 IMOBILI-RIA-PREMIUM PRONTO (COPIAR/COLAR)

### Copie estas linhas para sua planilha:

```
Data	Hora	Vendedor	Status	Cliente	Veículo
06/11/2025	10:00	Bruno	disponível
06/11/2025	14:00	Bruno	disponível
06/11/2025	15:00	Bruno	disponível
06/11/2025	16:00	Fernanda	disponível
07/11/2025	10:00	Bruno	disponível
07/11/2025	14:00	Fernanda	disponível
07/11/2025	15:00	Bruno	disponível
07/11/2025	16:00	Fernanda	disponível
08/11/2025	10:00	Bruno	disponível
08/11/2025	14:00	Bruno	disponível
```

---

## 🎨 FORMATAÇÃO CONDICIONAL (Opcional)

### Colorir por Status:

**Criar regra:**
1. Selecionar range: `A2:F100`
2. Formato → Formatação condicional
3. Adicionar regras:

**Regra 1: Disponível (Verde)**
- Se: `D2` = "disponível"
- Cor fundo: Verde claro (#d9ead3)

**Regra 2: Agendado (Amarelo)**
- Se: `D2` = "agendado"
- Cor fundo: Amarelo claro (#fff2cc)

**Regra 3: Realizado (Azul)**
- Se: `D2` = "realizado"
- Cor fundo: Azul claro (#cfe2f3)

**Regra 4: Cancelado (Vermelho)**
- Se: `D2` = "cancelado"
- Cor fundo: Vermelho claro (#f4cccc)

---

## 📱 ACESSO MOBILE

### Google Sheets App

**Vendedor pode:**
- ✅ Abrir planilha no celular
- ✅ Ver agendamentos do dia
- ✅ Marcar como realizado
- ✅ Adicionar novos horários

**Download:**
- iOS: App Store → "Google Sheets"
- Android: Play Store → "Google Sheets"

---

## 🔐 SEGURANÇA

### Recomendações:

✅ **Fazer cópias de backup semanalmente**
✅ **Compartilhar só com equipe autorizada**
✅ **Usar Service Account em produção (não acesso público)**
✅ **Revisar permissões mensalmente**

❌ **NÃO compartilhar link publicamente na internet**
❌ **NÃO dar permissão de Editor para qualquer pessoa**

---

## 📞 SUPORTE

### Problemas Comuns:

**Bot não encontra horários:**
- Verificar formato da data: `DD/MM/YYYY`
- Verificar status: deve ser exatamente `disponível`
- Verificar se data é futura (não passada)

**Bot não atualiza status:**
- Verificar permissões do Service Account (deve ser Editor)
- Verificar se planilha está compartilhada com Service Account
- Verificar logs: `logs/chatbot_v4.log`

**Vendedor não recebe notificação:**
- Verificar número do vendedor em: `componentes/escalonamento/notificacao.py`
- Verificar se Evolution API está funcionando
- Testar envio manual via `scripts/whatsapp/send_message.py`

---

## 🚀 PRÓXIMOS PASSOS

1. ✅ Criar planilha Google Sheets
2. ✅ Preencher imobili-ria-premium
3. ✅ Tornar pública (ou criar Service Account)
4. ✅ Conectar ID no bot
5. ✅ Testar agendamento
6. ✅ Treinar vendedores

---

**Dúvidas?** Leia `componentes/escalonamento/README.md` ou `GOOGLE_SETUP.md`
