# ⚡ Scripts Templates - Referência Rápida

**Comandos prontos para copiar e colar!**

Todos os comandos devem ser executados a partir do diretório raiz do workspace:
```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace
```

---

## 📱 WhatsApp (Evolution API)

### Enviar Mensagem
```bash
python3 scripts/whatsapp/send_message.py \
  --phone 5531980160822 \
  --message "Sua mensagem aqui"
```

### Enviar Imagem
```bash
python3 scripts/whatsapp/send_media.py \
  --phone 5531980160822 \
  --file "caminho/para/imagem.jpg" \
  --type image \
  --caption "Legenda da imagem"
```

### Enviar Documento
```bash
python3 scripts/whatsapp/send_media.py \
  --phone 5531980160822 \
  --file "documento.pdf" \
  --type document \
  --filename "Relatório.pdf"
```

### Criar Grupo
```bash
python3 scripts/whatsapp/create_group.py \
  --name "Nome do Grupo" \
  --phones 5531980160822,5511999999999
```

### Criar Grupo Apenas Admins
```bash
python3 scripts/whatsapp/create_group.py \
  --name "Anúncios" \
  --phones 5531980160822 \
  --admins-only
```

### Enviar Enquete
```bash
python3 scripts/whatsapp/send_poll.py \
  --phone 5531980160822 \
  --question "Qual a melhor opção?" \
  --options "Opção 1,Opção 2,Opção 3"
```

---

## 📸 Instagram (Templates Base)

```bash
python3 scripts/instagram/publish_post.py \
  --image "foto.jpg" \
  --caption "Meu post"
```
**Status:** ⚠️ Implementar Instagram Graph API

---

## 🎯 Meta Ads (Templates Base)

```bash
python3 scripts/meta-ads/create_campaign.py \
  --name "Minha Campanha" \
  --objective "OUTCOME_TRAFFIC"
```
**Status:** ⚠️ Implementar Meta Ads Marketing API

---

## 💡 Dicas

### Formatação WhatsApp:
- `*negrito*` → **negrito**
- `_itálico_` → *itálico*
- `~riscado~` → ~~riscado~~
- `` `código` `` → `código`

### Múltiplos números (grupos):
- Separe por vírgula SEM espaços: `5531980160822,5511999999999`

### Ajuda de qualquer script:
```bash
python3 scripts/whatsapp/send_message.py --help
```

---

## 📚 Documentação Completa

- **Geral:** `scripts/README.md`
- **WhatsApp:** `scripts/whatsapp/README.md`
- **Instagram:** `scripts/instagram/README.md`
- **Meta Ads:** `scripts/meta-ads/README.md`

---

**Última atualização:** 2025-11-01
