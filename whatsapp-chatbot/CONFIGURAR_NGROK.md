# 🔧 Configurar ngrok

O ngrok precisa de autenticação para funcionar. Siga os passos abaixo:

---

## 📝 Passo a Passo

### **1. Criar conta no ngrok (GRÁTIS)**

Acesse: https://dashboard.ngrok.com/signup

- Pode usar Google, GitHub ou email
- É 100% gratuito
- Não precisa cartão de crédito

---

### **2. Pegar seu authtoken**

Após criar a conta, acesse: https://dashboard.ngrok.com/get-started/your-authtoken

Você verá algo assim:
```
Your Authtoken
2abcDEFghiJKLmno3PQRstu4VWXyz5ABC6def7GHI8jkl
```

**Copie esse token!**

---

### **3. Configurar o authtoken no ngrok**

No terminal, execute:

```bash
ngrok config add-authtoken SEU_TOKEN_AQUI
```

Exemplo:
```bash
ngrok config add-authtoken 2abcDEFghiJKLmno3PQRstu4VWXyz5ABC6def7GHI8jkl
```

---

### **4. Pronto! Agora pode usar o ngrok**

```bash
ngrok http 5001
```

Você verá algo assim:
```
Forwarding    https://abc123.ngrok-free.app -> http://localhost:5001
```

**Copie essa URL!**

---

## 🚀 Depois de configurar

1. Com ngrok rodando, configure o webhook:
```bash
python3 configurar_webhook.py https://SUA-URL-NGROK.ngrok-free.app/webhook
```

2. Teste enviando mensagem para **5531980160822**

---

## ⚡ Atalho Rápido

Se já tiver o authtoken, execute:

```bash
# Configurar authtoken (só precisa fazer uma vez)
ngrok config add-authtoken SEU_TOKEN_AQUI

# Iniciar ngrok
ngrok http 5001
```

---

## 📌 Notas

- **Plano gratuito:** Funciona perfeitamente para testes
- **URL muda:** Toda vez que reiniciar o ngrok, a URL muda (reconfigure webhook)
- **Plano pago:** Se quiser URL fixa, considere upgrade ($8/mês)

---

**Precisa de ajuda?** Docs oficiais: https://ngrok.com/docs/getting-started
