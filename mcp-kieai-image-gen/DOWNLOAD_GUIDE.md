# 📥 Guia de Download de Imagens

## 🔗 Sobre os Links

### Links da API KIE.AI

```
https://tempfile.aiquickdraw.com/workers/nano/image_xxx.png
          ↑
      "tempfile" = Arquivo temporário
```

**Características:**
- ✅ Links **oficiais** da API KIE.AI
- ⚠️ **Podem expirar** (domínio sugere arquivos temporários)
- 🌐 Hospedados no servidor deles, não no nosso MCP

**Recomendação:** Sempre baixe as imagens para ter cópia permanente!

---

## 📂 3 Formas de Salvar Imagens

### 1️⃣ Download Automático (Recomendado) ⚡

Baixa **durante** a geração:

```python
result = await session.call_tool(
    "generate_image",
    arguments={
        "prompt": "Um gato fofo",
        "auto_download": True  # 🔥 Salva automaticamente
    }
)
```

**Vantagens:**
- ✅ Automático - não precisa fazer nada
- ✅ Garante que não vai perder a imagem
- ✅ Já fica salvo em ~/Downloads

**Resultado:**
```json
{
  "status": "success",
  "image_urls": ["https://tempfile..."],
  "downloads": [
    {
      "path": "/Users/você/Downloads/image_xxx.png",
      "filename": "image_xxx.png"
    }
  ]
}
```

---

### 2️⃣ Download Manual

Primeiro gera, depois baixa:

```python
# Passo 1: Gera a imagem
result = await session.call_tool(
    "generate_image",
    arguments={
        "prompt": "Um gato fofo",
        "auto_download": False  # Não baixa ainda
    }
)

# Passo 2: Extrai a URL
url = result["image_urls"][0]

# Passo 3: Baixa depois
download_result = await session.call_tool(
    "download_image",
    arguments={
        "url": url,
        "filename": "meu_gato.png"  # Nome customizado
    }
)
```

**Vantagens:**
- ✅ Você escolhe o nome do arquivo
- ✅ Pode baixar depois (mas cuidado com expiração!)

---

### 3️⃣ Apenas URLs (Não Recomendado) ⚠️

```python
result = await session.call_tool(
    "generate_image",
    arguments={
        "prompt": "Um gato fofo"
        # auto_download=False (padrão)
    }
)

# Você recebe apenas a URL
url = result["image_urls"][0]
# https://tempfile.aiquickdraw.com/...
```

**Desvantagens:**
- ❌ Link pode expirar
- ❌ Você pode perder a imagem
- ❌ Precisa baixar manualmente depois

**Use apenas se:**
- Vai usar a imagem imediatamente
- Vai fazer upload para outro serviço logo
- Tem certeza que não vai precisar depois

---

## 🎯 Recomendações por Caso de Uso

### 📱 Bot WhatsApp
```python
# Gera e envia direto pela URL (expira depois, mas já enviou)
result = generate_image(prompt)
whatsapp.send_image(url=result["image_urls"][0])
```

### 🖼️ Galeria / Portfólio
```python
# SEMPRE baixa localmente
result = generate_image(prompt, auto_download=True)
# Agora você tem a imagem em ~/Downloads
```

### 🎨 Design / Trabalho Criativo
```python
# Baixa com nome customizado
result = generate_image(prompt)
url = result["image_urls"][0]
download_image(url, filename="projeto_cliente_v1.png")
```

### ⚡ Uso Rápido / Teste
```python
# Só pega a URL e abre no navegador
result = generate_image(prompt)
print(result["image_urls"][0])
# Copia e cola no navegador
```

---

## 🔍 Onde Ficam as Imagens?

```bash
# Localização padrão
~/Downloads/

# Exemplos:
/Users/felipemdepaula/Downloads/image_1762352617073_t6wzla_1x1_1024x1024.png
```

### Verificar Downloads

```bash
# Listar imagens recentes
ls -lth ~/Downloads/*.png | head -5

# Abrir pasta Downloads
open ~/Downloads
```

---

## ⚙️ Configuração do Auto-Download

### No Código Python

```python
# Sempre baixar
result = await session.call_tool(
    "generate_image",
    arguments={
        "prompt": "...",
        "auto_download": True  # 🔥
    }
)
```

### No Claude Desktop

Quando você usar o MCP via Claude Desktop:

```
Você: Gere uma imagem de um robô fofo e salve no meu computador

Claude: [usa generate_image com auto_download=True automaticamente]
```

O Claude pode decidir usar `auto_download=true` automaticamente se você pedir para salvar!

---

## 📊 Comparação

| Método | Velocidade | Permanente | Controle Nome | Recomendado |
|--------|-----------|-----------|---------------|-------------|
| auto_download=true | ⚡⚡ Rápido | ✅ Sim | ❌ Não | ✅ Sim |
| download_image() | ⚡ Médio | ✅ Sim | ✅ Sim | ✅ Sim |
| Apenas URL | ⚡⚡⚡ Instantâneo | ⚠️ Temporário | ➖ N/A | ❌ Não |

---

## 🐛 Troubleshooting

### Erro: "Arquivo não encontrado em ~/Downloads"
```bash
# Verifica se pasta existe
ls ~/Downloads

# Se não existir, cria
mkdir -p ~/Downloads
```

### Erro: "Permission denied"
```bash
# Dá permissão
chmod +w ~/Downloads
```

### Link expirou
```
❌ Não tem como recuperar
💡 Sempre use auto_download=True!
```

---

## ✅ Checklist

Antes de gerar imagens importantes:

- [ ] Usar `auto_download=true` OU
- [ ] Baixar com `download_image()` logo após gerar
- [ ] Verificar que a imagem foi salva em ~/Downloads
- [ ] Fazer backup se for muito importante

**Lembre-se:** URLs podem expirar! Sempre baixe imagens que você quer manter! 💾
