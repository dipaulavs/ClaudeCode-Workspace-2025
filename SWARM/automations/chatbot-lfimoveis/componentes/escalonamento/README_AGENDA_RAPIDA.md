# ⚡ SETUP RÁPIDO - Agenda Google Sheets

## 🎯 3 PASSOS PARA COMEÇAR

### 1️⃣ Criar Planilha (2 minutos)

1. Acesse: https://sheets.google.com
2. Nova planilha em branco
3. Arquivo → Importar → Upload → Escolher arquivo:
   ```
   componentes/escalonamento/agenda_template.csv
   ```
4. Renomear aba para: `Agenda`
5. Copiar ID da URL:
   ```
   https://docs.google.com/spreadsheets/d/1A2B3C4D5E6F7G8H9I0J/edit
                                           ^^^^^^^^^^^^^^^^^^^^
                                           Copiar este ID
   ```

---

### 2️⃣ Tornar Pública (30 segundos)

**Opção A: Acesso Público (Mais Fácil)**
1. Botão "Compartilhar" (canto direito)
2. Alterar para: "Qualquer pessoa com o link"
3. Permissão: "Editor"
4. Pronto! ✅

**Opção B: Service Account (Produção)**
- Ver: `GOOGLE_SETUP.md` (mais seguro, mas +10 min setup)

---

### 3️⃣ Conectar no Bot (1 minuto)

**Arquivo:** `componentes/escalonamento/integrador.py`

```python
# Linha 26 - Alterar de:
self.agenda = ConsultaAgenda(use_mock=True)

# Para:
self.agenda = ConsultaAgenda(
    use_mock=False,
    sheet_id="SEU_ID_AQUI"  # ← Colar ID da planilha
)
```

**Reiniciar bot:**
```bash
./PARAR_BOT_AUTOMAIA.sh
./INICIAR_COM_NGROK.sh
```

---

## 🚀 PRONTO! Como Testar

**Via WhatsApp:**
```
Cliente: "quero agendar uma visita"
Bot: Mostra 3 opções de horário
Cliente: "a 2"
Bot: ✅ Agendado! [notifica vendedor]
```

**Verificar planilha:**
- Status mudou para: `agendado`
- Cliente preenchido
- Veículo preenchido

---

## 🔄 Manutenção Semanal (Automática)

**Adicionar horários pros próximos 7 dias:**

```bash
python3 componentes/escalonamento/atualizar_agenda.py \
  --sheet-id "SEU_ID_AQUI" \
  --dias 7 \
  --limpar
```

**Agendar via cron (toda segunda-feira 8h):**
```bash
crontab -e

# Adicionar linha:
0 8 * * 1 cd /caminho/projeto && python3 componentes/escalonamento/atualizar_agenda.py --sheet-id "SEU_ID" --dias 7 --limpar
```

---

## 📱 Vendedor Usa no Celular

**App Google Sheets:**
1. Download: App Store / Play Store
2. Abrir planilha (link compartilhado)
3. Ver agendamentos do dia
4. Marcar como "realizado" após visita

**Filtros úteis:**
- Status = `agendado` → Ver agendamentos
- Data = Hoje → Ver visitas de hoje
- Vendedor = Bruno → Ver só de Bruno

---

## 🎨 ESTRUTURA DA PLANILHA

| Data | Hora | Vendedor | Status | Cliente | Veículo |
|------|------|----------|--------|---------|---------|
| 06/11/2025 | 10:00 | Bruno | disponível | | |
| 06/11/2025 | 14:00 | Bruno | agendado | João | Civic |

**Status possíveis:**
- `disponível` - Horário livre
- `agendado` - Cliente agendou (bot preenche)
- `cancelado` - Cliente cancelou
- `realizado` - Visita já aconteceu

---

## 🐛 Solução de Problemas

### Bot não mostra horários

**Verificar:**
```python
# integrador.py linha 26
use_mock=False  # ← Deve ser False
sheet_id="..."  # ← ID correto?
```

**Testar manualmente:**
```bash
python3 -c "
from componentes.escalonamento import ConsultaAgenda
agenda = ConsultaAgenda(use_mock=False, sheet_id='SEU_ID')
print(agenda.buscar_horarios_disponiveis())
"
```

### Erro de permissão

**Solução:**
1. Abrir planilha
2. Compartilhar → "Qualquer pessoa com link"
3. Permissão: "Editor"

### Bot não atualiza status

**Verificar planilha:**
- Aba deve se chamar exatamente: `Agenda`
- Coluna D deve ter status: `disponível`
- Formato data: `DD/MM/YYYY` (06/11/2025)
- Formato hora: `HH:MM` (10:00)

---

## 📚 Documentação Completa

- **Template detalhado:** `PLANILHA_AGENDA_TEMPLATE.md`
- **Setup Service Account:** `GOOGLE_SETUP.md`
- **Código fonte:** `consulta_agenda.py`

---

## 💡 Dicas

✅ **Adicionar horários toda semana** (script automático)
✅ **Vendedor marca "realizado" após visita**
✅ **Filtrar por "agendado" pra ver compromissos**
✅ **Copiar semana anterior** (CTRL+C/V) para replicar padrão

❌ **NÃO deletar linhas** (só mudar status)
❌ **NÃO mudar nome das colunas** (bot depende delas)
❌ **NÃO mudar formato de data/hora** (deve ser exato)

---

**✅ Tudo pronto! Bot consultando agenda real do Google Sheets!** 🎉
