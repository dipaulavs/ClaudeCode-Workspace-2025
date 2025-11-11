# 📅 AGENDA GOOGLE SHEETS - Escolha Seu Método

## 🎯 QUAL MÉTODO USAR?

| Método | Dificuldade | Tempo | Melhor Para |
|--------|-------------|-------|-------------|
| **🥇 OAuth (Login)** | ⭐☆☆☆☆ | 3-5 min | **Testes rápidos** |
| 🥈 Manual (Template) | ⭐⭐☆☆☆ | 5-7 min | Sem programação |
| 🥉 Service Account | ⭐⭐⭐☆☆ | 10 min | **Produção** |

---

## 🥇 MÉTODO 1: OAuth (RECOMENDADO para começar)

**Mais fácil! Login + Clica "Autorizar"**

### Vantagens:
✅ Super rápido (3-5 min total)
✅ Login no navegador (sem JSON complexo)
✅ Planilha no seu Drive
✅ Token renova automaticamente

### Documentação:
📘 **Ver:** `OAUTH_FACIL.md`

### Comandos:
```bash
# 1. Autenticar (só 1x)
python3 componentes/escalonamento/autenticar_google.py

# 2. Criar planilha
python3 componentes/escalonamento/criar_agenda_publica_oauth.py
```

---

## 🥈 MÉTODO 2: Manual (Template CSV)

**Importar template pronto no Google Sheets**

### Vantagens:
✅ Sem código
✅ Controle total
✅ Fácil de entender

### Desvantagens:
⚠️ Precisa formatar manualmente
⚠️ Precisa tornar pública manualmente

### Documentação:
📘 **Ver:** `README_AGENDA_RAPIDA.md`

### Passos:
1. Google Sheets → Nova planilha
2. Arquivo → Importar → `agenda_template.csv`
3. Compartilhar → "Qualquer um com link" → Editor
4. Copiar ID da URL
5. Salvar em `chatwoot_config_automaia.json`

---

## 🥉 MÉTODO 3: Service Account (Produção)

**Totalmente automatizado com credenciais de robô**

### Vantagens:
✅ Token nunca expira
✅ Ideal para servidores
✅ Sem intervenção humana
✅ Mais seguro para produção

### Desvantagens:
⚠️ Setup mais complexo (10 min)
⚠️ Precisa compartilhar planilha com email do Service Account

### Documentação:
📘 **Ver:** `CRIACAO_AUTOMATICA.md`

### Comandos:
```bash
# Criar planilha automaticamente
python3 componentes/escalonamento/criar_agenda_publica.py
```

---

## 🔀 FLUXOGRAMA DE DECISÃO

```
Quer começar rápido?
    ├─ SIM → OAuth (Método 1) ✅
    └─ NÃO → Continue...

Sabe programar?
    ├─ NÃO → Manual/Template (Método 2)
    └─ SIM → Continue...

Vai usar em produção?
    ├─ SIM → Service Account (Método 3)
    └─ NÃO → OAuth (Método 1) ✅
```

---

## 📊 COMPARAÇÃO DETALHADA

### Setup Inicial

| | OAuth | Manual | Service Account |
|-|-------|--------|-----------------|
| **Tempo** | 3-5 min | 5-7 min | 10 min |
| **Passos** | 3 | 5 | 6 |
| **Dificuldade** | Fácil | Médio | Difícil |

### Autenticação

| | OAuth | Manual | Service Account |
|-|-------|--------|-----------------|
| **Tipo** | Login Google | N/A | JSON |
| **Expira?** | 7 dias (renova) | N/A | Nunca |
| **Interação** | Clica "Autorizar" | N/A | Automático |

### Planilha

| | OAuth | Manual | Service Account |
|-|-------|--------|-----------------|
| **Criação** | Automática | Manual | Automática |
| **Formatação** | Automática | Manual | Automática |
| **Localização** | Seu Drive | Seu Drive | Service Account Drive |
| **Pública** | Automático | Manual | Automático |

### Manutenção

| | OAuth | Manual | Service Account |
|-|-------|--------|-----------------|
| **Adicionar horários** | Script | Manual/Script | Script |
| **Atualizar** | Script | Manual/Script | Script |
| **Token** | Renova automático | N/A | Não expira |

---

## 🚀 INICIO RÁPIDO (Recomendado)

### 1️⃣ Instalar Dependências

```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 2️⃣ Escolher Método

**Mais fácil (OAuth):**
```bash
# Ver: OAUTH_FACIL.md
python3 componentes/escalonamento/autenticar_google.py
python3 componentes/escalonamento/criar_agenda_publica_oauth.py
```

**Produção (Service Account):**
```bash
# Ver: CRIACAO_AUTOMATICA.md
python3 componentes/escalonamento/criar_agenda_publica.py
```

**Manual (Template):**
```bash
# Ver: README_AGENDA_RAPIDA.md
# Importar: agenda_template.csv no Google Sheets
```

### 3️⃣ Configurar Bot

ID é salvo automaticamente (OAuth/Service Account) ou:

```json
// chatwoot_config_automaia.json
{
  "google_sheet_id": "ID_DA_PLANILHA"
}
```

### 4️⃣ Reiniciar Bot

```bash
./PARAR_BOT_AUTOMAIA.sh
./INICIAR_COM_NGROK.sh
```

---

## 📁 ARQUIVOS DISPONÍVEIS

```
componentes/escalonamento/
├── 🥇 OAUTH_FACIL.md                    (Método OAuth - RECOMENDADO)
├── 🥈 README_AGENDA_RAPIDA.md           (Método Manual)
├── 🥉 CRIACAO_AUTOMATICA.md             (Método Service Account)
│
├── 📋 README_ESCOLHA_METODO.md          (Este arquivo)
├── 📘 PLANILHA_AGENDA_TEMPLATE.md       (Documentação detalhada)
├── 🔐 GOOGLE_SETUP.md                   (Setup Service Account)
│
├── 🔧 autenticar_google.py              (OAuth - Passo 1)
├── 🚀 criar_agenda_publica_oauth.py     (OAuth - Passo 2)
├── 🚀 criar_agenda_publica.py           (Service Account)
├── 🔄 atualizar_agenda.py               (Manutenção)
│
└── 📄 agenda_template.csv               (Template para importar)
```

---

## 💡 DICAS

### Para Testar Hoje:
👉 Use **OAuth** (`OAUTH_FACIL.md`)

### Para Produção:
👉 Use **Service Account** (`CRIACAO_AUTOMATICA.md`)

### Sem Programação:
👉 Use **Manual** (`README_AGENDA_RAPIDA.md`)

---

## 🆘 PRECISA DE AJUDA?

### OAuth não funciona?
- Ver: `OAUTH_FACIL.md` seção "Solução de Problemas"

### Service Account não funciona?
- Ver: `CRIACAO_AUTOMATICA.md` seção "Solução de Problemas"

### Planilha não atualiza?
- Ver: `PLANILHA_AGENDA_TEMPLATE.md` seção "Suporte"

### Bot não consulta agenda?
- Verificar: `chatwoot_config_automaia.json`
- Verificar: Logs em `logs/chatbot_v4.log`

---

## 🎯 RECOMENDAÇÃO FINAL

**1. Começar:** OAuth (3-5 min)
   ```bash
   python3 componentes/escalonamento/autenticar_google.py
   python3 componentes/escalonamento/criar_agenda_publica_oauth.py
   ```

**2. Testar:** Bot com agenda real

**3. Produção:** Migrar para Service Account (se necessário)

---

**✅ ESCOLHA O SEU E COMECE!** 🚀
