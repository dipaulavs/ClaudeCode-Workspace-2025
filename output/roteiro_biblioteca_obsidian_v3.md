# Roteiro v3: Biblioteca no Obsidian com Bases + Book Search

## Abordagem: Workflow Visual (Setup → Uso → Troubleshooting)

---

## Slide 1: Título
**Sistema de Biblioteca no Obsidian**
Bases + Book Search = Organização Visual Completa

---

## Slide 2: Pré-requisitos (Card Interativo)
**Checklist de Setup**
- ✅ Obsidian v1.9.10+ (versão com Bases nativo)
- ✅ Plugin Bases (nativo, ativar em Settings)
- ✅ Plugin Book Search (comunidade, instalar)
- ✅ Criar pasta "Books" (organização)

**Onde verificar:** Settings → About → Installer/App version

---

## Slide 3: Fluxo de Adição de Livros
**Workflow Visual (com setas numeradas)**

```
1. Clicar ícone "New Book" (barra lateral)
   ↓
2. Buscar nome do livro (ex: "A Arte de Fazer Acontecer")
   ↓
3. Selecionar resultado correto (autor/edição)
   ↓
4. Nota criada automaticamente com:
   • Título + Subtítulo
   • Autor
   • Descrição
   • Cover URL (capa do livro)
   ↓
5. Adicionar tag "books" (propriedade obrigatória)
```

---

## Slide 4: Configuração da View Library (Cards Clicáveis)

**Card 1: Criar Nota Library**
- Comando: Ctrl/Cmd + P → "Bases: Insert new base"
- Filtrar por tag: `books`
- Resultado: Lista todos os livros

**Card 2: Customizar Visualização**
- Tipo: Card (visual com capas)
- Propriedade de imagem: `coverURL`
- Ajustar tamanho: Fit = "contain"
- Layout: Grid de cards com capas

**Card 3: Configurar Book Search**
- Settings → Book Search
- Pasta padrão: `Books/`
- Formato nome: `title - author`
- Tag automática: `books`

---

## Slide 5: Troubleshooting Interativo (Quiz)

**Problema 1: Livro não aparece na Library**
Quiz: Qual o erro?
- [ ] Plugin não instalado
- [x] Tag "books" não adicionada (CORRETO)
- [ ] Pasta errada

**Problema 2: Livro não encontrado no Book Search**
Solução: Adicionar manualmente
1. Criar nota em Books/ com nome do livro
2. Adicionar propriedades:
   - `title: "Nome do Livro"`
   - `coverURL: [[link-da-capa]]`
   - Tag: `books`

**Problema 3: Capa do livro errada/feia**
Solução: Substituir coverURL
1. Tirar foto da capa física
2. Adicionar ao Obsidian
3. Copiar link interno: `![[foto-capa.jpg]]`
4. Colar em `coverURL`

---

## Slide 6: Exemplo Prático - Livro Manual

**Cenário:** "Arrume Sua Cama" (William H. McRaven) não encontrado

**Passo a passo:**
```
1. Nova nota: Books/Arrume Sua Cama
2. Ctrl + P → Add Properties
3. Propriedades:
   title: "Arrume Sua Cama"
   author: "William H. McRaven"
   coverURL: [[capa-arrume-sua-cama.jpg]]
   tags: books
4. Salvar → Aparece automaticamente na Library
```

---

## Slide 7: Resumo (3 Colunas)

**O Que É**
- Sistema visual de biblioteca
- Bases (nativo) + Book Search (comunidade)
- Cards com capas de livros

**Como Funciona**
- Book Search busca metadados automáticos
- Bases filtra por tag e exibe em grid
- Adição manual quando necessário

**Por Que Usar**
- Centraliza leituras e notas
- Visual profissional (capas)
- Flexível (auto + manual)

---

## Slide 8: CTA Final

**Gostou? Ajude o canal!**

👍 Deixe seu LIKE
🔔 INSCREVA-SE no canal
📸 Siga no Instagram: @eusoupromptus

💬 Tem dúvida sobre o template? Comente!
📧 Newsletter: 1% Melhor Todo Dia (link na descrição)

---

**Total de slides:** 8 (6 conteúdo + 1 resumo + 1 CTA)
**Elementos interativos:** 3 cards clicáveis + 1 fluxo visual + 3 quizzes
