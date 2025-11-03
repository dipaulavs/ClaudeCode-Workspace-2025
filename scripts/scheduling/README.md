# 📅 Scheduling - Scripts Agendados

Scripts para automação com agendamento via cron.

---

## 📋 Scripts Disponíveis

### 🤖 AI News Digest - `daily_ai_news.py`

Busca automática de notícias sobre IA no Twitter, cria resumo detalhado e envia.

**O que faz:**
1. Busca no Twitter sobre OpenAI, Anthropic/Claude e Google/Gemini (xAI Search)
2. Analisa e cria resumo consolidado com Grok
3. Salva nota no Obsidian (com fallback para arquivo local)
4. Envia resumo via WhatsApp

**Uso:**
```bash
# Execução manual
python3.11 scripts/scheduling/daily_ai_news.py

# Apenas Obsidian (sem WhatsApp)
python3.11 scripts/scheduling/daily_ai_news.py --no-whatsapp

# Customizar número de posts
python3.11 scripts/scheduling/daily_ai_news.py --max-posts 20

# Customizar telefone
python3.11 scripts/scheduling/daily_ai_news.py --phone 5531999999999
```

**Parâmetros:**
- `--phone`: Número WhatsApp (padrão: 5531980160822)
- `--no-whatsapp`: Não enviar WhatsApp
- `--max-posts`: Máximo de posts por empresa (padrão: 10)

**Outputs:**
- Nota no Obsidian: `00 - Inbox/AI News - YYYY-MM-DD.md`
- Fallback local: `output/ai-news/AI News - YYYY-MM-DD.md`
- Mensagem WhatsApp com resumo executivo
- Log: `logs/ai_news.log`

**APIs usadas:**
- xAI/Grok (busca Twitter + análise)
- Obsidian Local REST API (salvar nota)
- Evolution API (enviar WhatsApp)

**Custo estimado:** ~$0.03 por execução

---

## ⏰ Agendamento (Cron)

### Verificar agendamentos
```bash
crontab -l
```

### Editar agendamentos
```bash
crontab -e
```

### Remover agendamento
```bash
crontab -r
```

### Exemplo: Agendar AI News para todo dia às 7h
```bash
# Criar arquivo de configuração
cat > /tmp/my_cron.txt << 'EOF'
0 7 * * * /opt/homebrew/bin/python3.11 /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/scripts/scheduling/daily_ai_news.py >> /Users/felipemdepaula/Desktop/ClaudeCode-Workspace/logs/ai_news.log 2>&1
EOF

# Aplicar
crontab /tmp/my_cron.txt
```

### Formato Crontab
```
┌───────── minuto (0-59)
│ ┌─────── hora (0-23)
│ │ ┌───── dia do mês (1-31)
│ │ │ ┌─── mês (1-12)
│ │ │ │ ┌─ dia da semana (0-7, 0 ou 7 = domingo)
│ │ │ │ │
* * * * * comando
```

**Exemplos:**
```bash
0 7 * * *     # Todo dia às 7h
0 9 * * 1     # Toda segunda às 9h
0 18 * * 1-5  # Dias úteis às 18h
0 */6 * * *   # A cada 6 horas
```

---

## 📊 Logs

Ver logs em tempo real:
```bash
tail -f logs/ai_news.log
```

Ver últimas 50 linhas:
```bash
tail -50 logs/ai_news.log
```

---

## 🔧 Troubleshooting

### Cron não está executando
1. Verificar permissões do Terminal no macOS:
   - System Settings → Privacy & Security → Full Disk Access
   - Adicionar Terminal/iTerm

2. Verificar se cron está rodando:
   ```bash
   sudo launchctl list | grep cron
   ```

3. Verificar logs do sistema:
   ```bash
   log show --predicate 'process == "cron"' --last 1h
   ```

### Script falha no agendamento mas funciona manual
- Verificar paths absolutos (não usar paths relativos)
- Verificar variáveis de ambiente (cron não carrega .zshrc)
- Adicionar `cd` ao diretório antes de rodar:
  ```bash
  0 7 * * * cd /path/workspace && python3.11 script.py
  ```

### Obsidian não disponível
- Script tem fallback automático para arquivo local
- Arquivos salvos em `output/ai-news/`
- Transferir manualmente para Obsidian depois

---

**Criado:** 03/11/2025
**Localização:** `scripts/scheduling/`
