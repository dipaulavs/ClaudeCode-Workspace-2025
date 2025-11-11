# 🔧 Visual Explainer - Troubleshooting

## Problemas Comuns e Soluções

---

## Erro 1: HTML Não Abre Automaticamente no Navegador

### Sintoma
```
✅ Apresentação criada: apresentacao_tema.html
❌ Navegador não abre automaticamente
```

### Causa
Permissões do sistema podem bloquear abertura automática de arquivos.

### Solução (MCP Filesystem)

**Skill usa `Bash` tool para abrir:**
```bash
# macOS (skill executa automaticamente)
open "/Users/felipemdepaula/Documents/Obsidian/Claude-code-ios/📺 Vídeos/Apresentações/apresentacao_tema.html"
```

**Se falhar, abrir manualmente:**
```bash
# Vault Obsidian
open "/Users/felipemdepaula/Documents/Obsidian/Claude-code-ios/📺 Vídeos/Apresentações/apresentacao_tema.html"

# Workspace
open "/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/apresentacao_tema.html"
```

**Linux:**
```bash
xdg-open [caminho-completo]
```

**Windows:**
```cmd
start [caminho-completo]
```

### Prevenção
Skill usa `Bash` tool (`open` command) automaticamente. Se falhar, mostra caminho completo para abrir manualmente.

---

## Erro 2: Atalhos de Teclado Não Funcionam

### Sintoma
- Pressiona setas ← → mas nada acontece
- Tecla F não ativa fullscreen
- Espaço não avança slides

### Causa
**Possibilidade 1:** Foco está fora da apresentação (clicou fora da janela)
**Possibilidade 2:** Navegador bloqueou JavaScript
**Possibilidade 3:** Console do DevTools está aberto e capturando teclas

### Solução

1. **Reativar foco:**
   - Clique dentro da apresentação
   - Pressione Tab até voltar para área de conteúdo

2. **Verificar JavaScript:**
   - Abra DevTools (F12)
   - Vá em Console
   - Procure erros em vermelho
   - Se houver: Reporte o erro

3. **Fechar DevTools:**
   - Pressione F12 novamente
   - Tente atalhos novamente

4. **Testar atalhos manualmente:**
   - Abra Console (F12 → Console)
   - Digite: `document.addEventListener('keydown', e => console.log(e.key))`
   - Pressione teclas e veja se aparecem no console

### Prevenção
Sempre clique dentro da apresentação antes de usar atalhos.

---

## Erro 3: Notas do Apresentador Não Aparecem

### Sintoma
```
Apresentação abre normalmente mas:
❌ Não vejo as notas na parte inferior
❌ Rodapé está vazio
```

### Causa
**Possibilidade 1:** Resolução da tela muito pequena (notas estão cortadas)
**Possibilidade 2:** CSS não carregou corretamente
**Possibilidade 3:** Conteúdo não tinha notas no roteiro original

### Solução

1. **Verificar se notas existem:**
   - Abra DevTools (F12 → Elements)
   - Procure por `class="apresentador-notas"`
   - Se não existir: Roteiro original não tinha notas

2. **Aumentar altura das notas:**
   - Pressione F12 → Console
   - Cole: `document.querySelector('.apresentador-notas').style.height = '30vh'`
   - Enter

3. **Scroll para baixo:**
   - Se tela pequena, as notas podem estar fora da viewport
   - Scroll até o final da página

4. **Recriar apresentação (MCP):**
   - Pedir novamente: "Claude, cria apresentação com notas visíveis"
   - Skill usa `Write` tool para gerar novo HTML

### Prevenção
Sempre inclua seção "Notas do Apresentador" no roteiro:
```markdown
## Slide X
[Conteúdo]

**Notas:** O que você deve falar aqui
```

---

## Erro 4: Timer Não Inicia ou Fica Parado em 00:00

### Sintoma
```
✅ Apresentação aberta
⏱️  Timer mostra 00:00 mas não conta
```

### Causa
JavaScript do timer pode ter falhado ao inicializar.

### Solução

1. **Reiniciar timer manualmente:**
   - Pressione F12 → Console
   - Cole: `startTimer()`
   - Enter

2. **Verificar erros JavaScript:**
   - Console mostrará erros (se houver)
   - Procure por: `timer is not defined` ou similar

3. **Resetar timer:**
   - Recarregue página (Ctrl+R ou Cmd+R)
   - Timer deve iniciar automaticamente

4. **Desativar timer se não precisar:**
   - Pedir: "Claude, cria apresentação sem timer"
   - Skill gera HTML sem componente de timer

### Prevenção
Timer inicia automaticamente ao carregar página. Se não iniciar, é bug — reporte!

---

## Erro 5: Mapa Mental Está Muito Pequeno/Grande

### Sintoma
- Nós do mapa mental aparecem minúsculos
- Ou: Mapa mental não cabe na tela

### Causa
Zoom inicial do SVG pode estar incorreto para quantidade de nós.

### Solução

1. **Usar controles de zoom:**
   - Botões `[Zoom +]` e `[Zoom -]` no topo
   - Ou: Ctrl + Scroll do mouse

2. **Resetar view:**
   - Clique em `[Reset]`
   - Mapa centraliza automaticamente

3. **Ajustar zoom via código:**
   - F12 → Console
   - Cole: `setZoom(1.5)` (aumenta 50%)
   - Ou: `setZoom(0.7)` (diminui 30%)

4. **Recriar com zoom customizado:**
   - Pedir: "Claude, cria mapa mental com zoom inicial 1.2x"
   - Skill gera HTML com configuração ajustada

### Prevenção
Skill calcula zoom automaticamente, mas você pode ajustar manualmente após abrir.

---

## Erro 6: Template Errado Foi Escolhido

### Sintoma
```
Você esperava: Mapa Mental
Skill gerou: Notion Style
```

### Causa
Algoritmo de decisão automática interpretou conteúdo diferente do esperado.

### Solução

**Opção 1 - Forçar template manualmente:**
```
"Claude, cria apresentação MAPA MENTAL sobre [assunto]"
          (especifica o template)↑
```

**Opção 2 - Regenerar (MCP):**
- Pedir: "Claude, cria apresentação [assunto] usando template mapa-mental"
- Skill usa `Read` + `Write` tools para gerar corretamente

**Opção 3 - Melhorar roteiro:**
Adicione palavras-chave que ativam o template desejado:
- **Mapa Mental:** "arquitetura", "componentes", "relações", "sistema"
- **Tech Futurista:** "lançamento", "novidade", "anúncio", "impacto"
- **Notion:** "explicação", "conceito", "tutorial", "passo a passo"

### Prevenção
Se tem preferência clara, sempre especifique o template no prompt.

---

## Erro 7: Apresentação Não Carrega (Tela Branca)

### Sintoma
- Navegador abre
- Tela fica branca/preta
- Nada aparece

### Causa
**Possibilidade 1:** HTML corrompido ou incompleto
**Possibilidade 2:** Erro crítico de JavaScript
**Possibilidade 3:** Arquivo muito grande (>10MB)

### Solução

1. **Verificar console:**
   - F12 → Console
   - Procure erros em vermelho
   - Se houver: Anote e reporte

2. **Testar HTML manualmente:**
   ```bash
   # Ver tamanho do arquivo
   ls -lh apresentacao_tema.html

   # Se > 10MB, está muito grande
   ```

3. **Validar HTML:**
   - Abra o arquivo em editor de texto
   - Verifique se termina com `</html>`
   - Se não termina: Arquivo corrompido

4. **Regenerar do zero (MCP):**
   - Pedir: "Claude, recria apresentação [assunto]"
   - Skill usa `Write` tool para sobrescrever arquivo

5. **Testar em outro navegador:**
   - Chrome não funciona? Tente Firefox
   - Firefox não funciona? Tente Edge/Safari

### Prevenção
Mantenha roteiros com tamanho razoável (< 20 slides). Para apresentações gigantes, divida em múltiplos arquivos.

---

## Erro 8: Fontes Não Carregam (Texto em Fallback)

### Sintoma
- Apresentação abre
- Mas texto está em fonte genérica (Times New Roman, Arial)
- Não está com Inter ou Space Grotesk

### Causa
Fontes customizadas não foram embedadas corretamente.

### Solução

1. **Verificar se é problema real:**
   - Fontes de fallback (system-ui) são aceitáveis
   - Não impacta muito a gravação

2. **Forçar fontes do sistema:**
   - Templates já usam fallbacks adequados
   - Não impacta funcionalidade (apenas estética)

3. **Instalar fontes localmente:**
   ```bash
   # macOS/Linux
   # Baixar Inter: https://rsms.me/inter/
   # Instalar no sistema
   ```

### Prevenção
Templates usam `font-family` com fallbacks:
```css
font-family: 'Inter', system-ui, -apple-system, sans-serif;
```
Mesmo que Inter não carregue, fallback funciona bem.

---

## Erro 9: Progresso (●●●○○○) Não Atualiza

### Sintoma
- Navega entre slides
- Mas indicador fica sempre em `●○○○○○ 1/6`

### Causa
JavaScript de atualização de progresso falhou.

### Solução

1. **Recarregar página:**
   - Ctrl+R (Win/Linux) ou Cmd+R (Mac)
   - Tente navegar novamente

2. **Forçar atualização manual:**
   - F12 → Console
   - Cole: `updateProgress()`
   - Enter após cada navegação

3. **Verificar erros:**
   - Console deve mostrar erro se houver
   - Reporte se encontrar

### Prevenção
Bug raro — se acontecer, reporte com detalhes do roteiro usado.

---

## Erro 10: Fullscreen (F ou F11) Não Funciona

### Sintoma
- Pressiona F ou F11
- Nada acontece

### Causa
**Possibilidade 1:** Navegador bloqueia fullscreen sem interação do usuário
**Possibilidade 2:** Permissão de fullscreen negada
**Possibilidade 3:** Atalho está em conflito com sistema operacional

### Solução

1. **Usar botão manual:**
   - Clique com botão direito na apresentação
   - "Entrar em tela cheia" (Chrome/Firefox)

2. **Tentar F11 nativo do navegador:**
   - Ignora script, usa fullscreen do browser

3. **Permitir fullscreen:**
   - Chrome: Settings → Site Settings → Permissions → Fullscreen
   - Permitir para `file://` URLs

4. **Shortcut alternativo:**
   - macOS: Ctrl+Cmd+F (fullscreen nativo)
   - Windows: F11

### Prevenção
Sempre clique na apresentação antes de tentar fullscreen.

---

## Erro 11: Cards Cortados ou Escondidos (RESPONSIVIDADE)

### Sintoma
- ❌ Alguns cards ficam cortados na lateral
- ❌ Conteúdo escondido (precisa scroll horizontal)
- ❌ Em mobile, cards minúsculos ou sobrepostos
- ❌ Em telas grandes, cards se escondem atrás de outros

### Causa
**CSS com responsividade quebrada:**
- `overflow: hidden` escondendo conteúdo
- `height: XXpx` fixo em containers
- Grid sem `auto-fit` / Flexbox sem `wrap`
- Falta de media queries

### Solução

#### 1. Verificar CSS do Container:

**Abra DevTools (F12 → Elements) e procure:**

```css
/* ❌ SE VER ISTO, está errado: */
.cards-container {
  overflow: hidden;  /* Remove isso */
  height: 600px;     /* Remove isso */
}
```

**Substitua por:**

```css
/* ✅ Correto: */
.cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  grid-auto-rows: auto;
  overflow-y: auto; /* Scroll vertical OK */
}
```

#### 2. Fixar Responsividade via Console:

```javascript
// Cole no Console (F12 → Console):

// Corrigir container de cards
document.querySelectorAll('.cards-container, .grid, .flex-container').forEach(el => {
  el.style.overflow = 'visible';
  el.style.height = 'auto';
  el.style.display = 'grid';
  el.style.gridTemplateColumns = 'repeat(auto-fit, minmax(280px, 1fr))';
  el.style.gap = '1.5rem';
});

// Corrigir cards individuais
document.querySelectorAll('.card').forEach(card => {
  card.style.height = 'auto';
  card.style.minHeight = '120px';
  card.style.overflow = 'visible';
});
```

#### 3. Media Queries Ausentes:

**Adicione no HTML (dentro da tag `<style>`):**

```css
@media (max-width: 768px) {
  .cards-container {
    grid-template-columns: 1fr !important; /* 1 coluna mobile */
    padding: 1rem !important;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .cards-container {
    grid-template-columns: repeat(2, 1fr) !important; /* 2 colunas tablet */
  }
}

@media (min-width: 1025px) {
  .cards-container {
    grid-template-columns: repeat(3, 1fr) !important; /* 3+ colunas desktop */
  }
}
```

#### 4. Testar em Múltiplas Resoluções:

**DevTools → Toggle Device Toolbar (Ctrl+Shift+M):**

- Mobile: 375px (iPhone SE)
- Tablet: 768px (iPad)
- Desktop: 1920px (Full HD)
- Ultrawide: 2560px

**Verificar checklist:**
- [ ] Todos os cards visíveis?
- [ ] Nenhum texto cortado?
- [ ] Scroll horizontal NÃO existe?
- [ ] Scroll vertical funciona (se necessário)?

#### 5. Regenerar Apresentação (MCP):

Se o problema persistir, **regenere via skill:**

```
Pedir: "Claude, cria apresentação sobre [assunto] (certifica que todos os cards estejam visíveis)"

Skill usa:
- Read tool: Carregar template corrigido
- Write tool: Salvar HTML com responsividade garantida
```

### Prevenção

**A partir de agora, a skill `visual-explainer` SEMPRE:**
- ✅ Usa CSS Grid com `auto-fit` e `minmax()`
- ✅ Nunca fixa `height` em containers
- ✅ Nunca usa `overflow: hidden` em conteúdo
- ✅ Inclui media queries para mobile/tablet/desktop
- ✅ Testa visualmente se cards estão visíveis

**Se você editar o HTML manualmente:**
- ⚠️ NUNCA use `overflow: hidden` em `.cards-container`
- ⚠️ NUNCA fixe altura com `height: XXpx` em containers
- ⚠️ SEMPRE use `grid-auto-rows: auto` ou `height: auto`

### Debug Visual Rápido:

**Para destacar cards cortados:**

```javascript
// Cole no Console:
document.querySelectorAll('.card').forEach(card => {
  const rect = card.getBoundingClientRect();
  if (rect.right > window.innerWidth || rect.bottom > window.innerHeight) {
    card.style.border = '3px solid red'; // Cards cortados ficam vermelhos
    console.log('Card cortado:', card);
  }
});
```

---

## Como Reportar Bugs

Se encontrar erro não listado aqui:

1. **Abra issue no GitHub** (ou contato definido)
2. **Inclua:**
   - Descrição do erro
   - Template usado (Notion/Mapa/Tech)
   - Console logs (F12 → Console, screenshot)
   - Trecho do roteiro (se possível)
   - Navegador + versão + OS

3. **Workaround temporário:**
   - Use template diferente
   - Ou simplifique o roteiro

---

## FAQ Rápido

**P: Posso editar o HTML depois de gerado?**
R: Sim! É arquivo standalone, edite à vontade.

**P: Funciona offline?**
R: Sim, 100% standalone (sem dependências online).

**P: Posso adicionar imagens/vídeos?**
R: Sim, edite HTML e adicione tags `<img>` ou `<video>`.

**P: Como exportar para PDF?**
R: Ctrl+P → "Salvar como PDF" (funciona em todos navegadores).

**P: Posso usar em OBS?**
R: Sim! Adicione como "Browser Source" (URL: file://caminho/apresentacao.html).

**P: Apresentação expira?**
R: Não, arquivo HTML funciona para sempre (offline).
