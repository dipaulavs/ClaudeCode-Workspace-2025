# ⚡ Comandos Rápidos - Guia

## 🎯 Como Funciona Agora

Os botões **não executam automaticamente** - eles mostram um popup com o comando para você **copiar e colar** no terminal. Isso é mais simples e confiável!

---

## 🚀 LISTA DE COMANDOS

### 1. **Iniciar Setup**

**Comando:**
```bash
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace && bash iniciar.sh && cat README.md
```

**O que faz:**
- Navega para o workspace
- Executa o script de boas-vindas
- Mostra o README completo

**Quando usar:**
- Primeira vez que abre o terminal
- Quando quer ver as ferramentas disponíveis
- Para inicializar o ambiente

---

### 2. **Nova Conversa**

**Comando:**
```bash
exec bash
```

**O que faz:**
- Reinicia o shell bash
- Limpa todas as variáveis de ambiente
- Reseta o histórico
- **Contexto anterior é perdido**

**Quando usar:**
- Terminal travado
- Quer começar limpo
- Resetar variáveis de ambiente
- Limpar memória/contexto

---

### 3. **Limpar Tela**

**Comando:**
```bash
clear
```

**O que faz:**
- Limpa visualmente o terminal
- Histórico é mantido (use setas ↑↓)
- **NÃO limpa contexto ou variáveis**

**Quando usar:**
- Terminal muito poluído
- Quer ver só comandos novos
- Organizar visualmente

---

### 4. **Ver Ferramentas**

**Comando:**
```bash
ls tools/
```

**O que faz:**
- Lista todos os scripts Python em `tools/`
- Mostra ferramentas disponíveis

**Quando usar:**
- Lembrar nome de uma ferramenta
- Ver o que está disponível
- Explorar o workspace

---

### 5. **Últimos Arquivos**

**Comando:**
```bash
ls -lt ~/Downloads | head -10
```

**O que faz:**
- Lista últimos 10 arquivos em Downloads
- Ordenados por data (mais recentes primeiro)
- Mostra tamanho e permissões

**Quando usar:**
- Ver suas gerações recentes
- Verificar se arquivo foi criado
- Encontrar arquivos rapidamente

---

## 💡 COMO USAR OS BOTÕES

### Passo a Passo:

1. **Clique no botão** (ex: "Iniciar Setup")

2. **Popup aparece** com:
   - Título do comando
   - Box preto com o comando
   - Botão "Copiar"
   - Instruções

3. **Clique em "Copiar"** ou **"Copiar e Fechar"**

4. **Notificação verde** aparece: "✓ Comando copiado!"

5. **Clique no terminal** (área preta)

6. **Cole o comando:**
   - Mac: `Cmd + V`
   - Windows/Linux: `Ctrl + V`

7. **Pressione Enter**

8. **Comando executa!** 🎉

---

## 🎨 VISUAL DO POPUP

```
┌─────────────────────────────────────────┐
│ Iniciar Setup                      [X] │
├─────────────────────────────────────────┤
│ Copie o comando abaixo e cole:         │
│                                         │
│ ┌─────────────────────────────┐       │
│ │ cd /Users/.../Workspace &&  │ [📋]  │
│ │ bash iniciar.sh && ...      │       │
│ └─────────────────────────────┘       │
│                                         │
│ ℹ️  Como usar: Clique em "Copiar"...  │
│                                         │
│ [Copiar e Fechar]  [Fechar]           │
└─────────────────────────────────────────┘
```

---

## ⌨️ ATALHOS DE TECLADO

| Atalho | Ação |
|--------|------|
| `Ctrl+K` ou `Cmd+K` | Mostrar comando "Limpar Tela" |
| `Ctrl+N` ou `Cmd+N` | Mostrar comando "Nova Conversa" |
| `ESC` | Fechar popup |

---

## 📱 FUNCIONA NO CELULAR?

**SIM!** Funciona perfeitamente:

1. Toque no botão
2. Popup abre
3. Toque em "Copiar"
4. Toque no terminal
5. Toque e segure → "Colar"
6. Pressione Enter no teclado virtual

---

## 🔍 DIFERENÇAS ENTRE OS COMANDOS

### `clear` vs `exec bash`

| Comando | Limpa Tela | Limpa Histórico | Reseta Variáveis | Reinicia Shell |
|---------|------------|-----------------|------------------|----------------|
| `clear` | ✅ | ❌ | ❌ | ❌ |
| `exec bash` | ✅ | ✅ | ✅ | ✅ |

**Use `clear` quando:**
- Só quer limpar visualmente
- Quer manter histórico (setas ↑↓)
- Rápido e simples

**Use `exec bash` quando:**
- Quer recomeçar do zero
- Terminal travou
- Resetar tudo

---

## 💬 EXEMPLOS DE USO

### Exemplo 1: Primeira Vez

```
1. Abrir: http://localhost:3000/chat.html
2. Clicar: "Iniciar Setup"
3. Copiar comando
4. Colar no terminal
5. Enter
6. Ver README e ferramentas
```

### Exemplo 2: Terminal Bagunçado

```
1. Clicar: "Limpar Tela"
2. Copiar: clear
3. Colar no terminal
4. Enter
5. Tela limpa! ✨
```

### Exemplo 3: Recomeçar do Zero

```
1. Clicar: "Nova Conversa"
2. Copiar: exec bash
3. Colar no terminal
4. Enter
5. Shell reinicia completamente
6. Contexto limpo!
```

---

## 🎯 COMANDOS ADICIONAIS ÚTEIS

Aqui estão outros comandos que você pode usar direto no terminal:

### Navegação
```bash
# Ver onde você está
pwd

# Ir para workspace
cd /Users/felipemdepaula/Desktop/ClaudeCode-Workspace

# Voltar para home
cd ~

# Listar arquivos
ls -la
```

### Ferramentas
```bash
# Gerar imagem
python3 tools/generate_image_nanobanana.py "seu prompt"

# Gerar áudio
python3 tools/generate_audio_elevenlabs.py "seu texto"

# Ver README
cat README.md
```

### Informações
```bash
# Ver últimas 20 linhas de um arquivo
tail -20 README.md

# Procurar texto em arquivo
grep "imagem" README.md

# Ver tamanho de Downloads
du -sh ~/Downloads
```

---

## ❓ FAQ - PERGUNTAS FREQUENTES

### P: Por que não executar automaticamente?

**R:** Porque o terminal (iframe) é isolado por segurança. JavaScript não pode injetar comandos diretamente. Copiar/colar é a forma mais confiável e funciona 100%.

### P: O comando some depois que copio?

**R:** Não! O comando fica no popup até você fechar. Você pode copiar quantas vezes quiser.

### P: Posso editar o comando antes de colar?

**R:** Sim! Depois de colar no terminal, você pode editar normalmente antes de dar Enter.

### P: Funciona em todos os navegadores?

**R:** Sim! Chrome, Firefox, Safari, Edge, Opera. Mobile também funciona.

### P: O que é "exec bash"?

**R:** É um comando que substitui o shell atual por um novo. Reinicia completamente o bash sem fechar a janela.

---

## ✅ CHECKLIST DE USO

Primeira vez usando?

- [ ] Acesse http://localhost:3000/chat.html
- [ ] Clique em "Iniciar Setup"
- [ ] Copie o comando
- [ ] Cole no terminal
- [ ] Pressione Enter
- [ ] Veja o README
- [ ] Explore as ferramentas!

---

## 🆘 PROBLEMAS COMUNS

### Botão não abre popup

**Solução:** Recarregue a página (F5 ou Ctrl+R)

### Botão "Copiar" não funciona

**Solução:**
1. Selecione o texto manualmente
2. Copie com Ctrl+C ou Cmd+C

### Comando não cola no terminal

**Solução:**
1. Clique dentro do terminal (área preta)
2. Certifique-se que o terminal está focado
3. Tente colar novamente

### Terminal não aceita input

**Solução:**
1. Recarregue a página do chat
2. Ou execute: `exec bash` para reiniciar

---

**🎉 Agora você sabe usar todos os comandos rápidos!**

**Recarregue a página e teste:** http://localhost:3000/chat.html
