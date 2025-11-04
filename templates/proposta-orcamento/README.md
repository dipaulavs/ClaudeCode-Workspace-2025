# 🎬 Template de Apresentação Interativa para Propostas

**Template HTML profissional com revelação progressiva para apresentações de orçamento em videochamadas.**

---

## 📋 O Que É

Template de apresentação estilo **PowerPoint interativo** com:
- ✅ Animações progressivas (itens aparecem ao clicar)
- ✅ Design MotherDuck (beige + yellow + dark gray)
- ✅ 100% responsivo e standalone (funciona offline)
- ✅ Ideal para videochamadas (compartilhar tela)
- ✅ Navegação por teclado ou clique

---

## 🎯 Estrutura Padrão (9 Slides)

1. **Capa** → Título + Cliente + Objetivo
2. **Situação Atual** → 4 problemas (cards progressivos)
3. **Solução Proposta** → 6 serviços (cards progressivos)
4. **Como Funciona** → Fluxo + Diferenciais + Gestão
5. **Timeline** → Fases de implementação
6. **Investimento Detalhado** → Tabela progressiva (10 steps!)
7. **Comparação Mercado** → Economia vs concorrentes
8. **O Que Está Incluso** → Detalhamento entregáveis
9. **Próximos Passos** → CTA + Forma pagamento

---

## 🚀 Como Usar

### **Método 1: Customizar Direto no HTML (Rápido)**

1. Copiar `template_proposta_interativa.html` para novo arquivo:
   ```bash
   cp template_proposta_interativa.html proposta_[CLIENTE].html
   ```

2. Buscar e substituir (Find & Replace) no editor:
   - `Up Uniformes` → Nome do seu cliente
   - `R$ 3.497` → Seu valor final
   - `10 dias úteis` → Seu prazo
   - Etc.

3. Abrir no navegador e testar:
   ```bash
   open proposta_[CLIENTE].html
   ```

---

### **Método 2: Gerar via Skill (Recomendado)**

Usar skill `orcamento-profissional`:

```
Usuário: "Preciso fazer orçamento para [Cliente] que quer [Serviços]"

Claude:
1. Coleta dados do projeto
2. Mapeia recursos disponíveis
3. Calcula preço baseado em valor
4. Gera HTML a partir deste template
5. Customiza com dados do cliente
```

---

## 🎨 Características do Template

### **Animações Progressivas**

Cada slide tem `data-total-steps` definindo quantos itens revelam:

```html
<div class="slide" data-total-steps="4">
    <div class="card reveal-item" data-step="1">...</div>
    <div class="card reveal-item" data-step="2">...</div>
    <div class="card reveal-item" data-step="3">...</div>
    <div class="card reveal-item" data-step="4">...</div>
</div>
```

**Funcionamento:**
- Nada aparece ao entrar no slide
- Cada clique/→ revela próximo item (`data-step`)
- Indicador no canto: "(3/4)" mostra progresso
- Hint dinâmico: "Clique para revelar próximo item"

---

### **Slide de Investimento (Mais Importante)**

**Estrutura em 10 steps para máximo impacto:**

```
Step 1-4: Cada serviço (linha da tabela)
Step 5: SUBTOTAL (amarelo)
Step 6: Desconto combo
Step 7: FINAL tabela
Step 8: 💥 QUADRADO AMARELO GIGANTE 💥 (clímax!)
Step 9: Box pagamentos únicos
Step 10: Box resumo primeiro mês
```

**Por que funciona:** Cliente vê matemática sendo construída → desconto acontecendo → BOOM valor final dramático!

---

## 🎮 Navegação

**Teclado:**
- `→` ou `Espaço` → Próximo item/slide
- `←` → Slide anterior
- `F` → Fullscreen
- `ESC` → Sair fullscreen

**Mouse:**
- Clicar 1/3 esquerdo → Voltar
- Clicar 1/3 direito → Avançar
- Clicar centro → Avançar

---

## 📝 Pontos de Customização

### **1. Capa (Slide 1)**

```html
<h1>Proposta: [TÍTULO DO PROJETO]</h1>
<p class="subtitle">[SUBTÍTULO]</p>
<div class="box">
    <h3>Para: [NOME CLIENTE]</h3>
    <p><strong>Indústria:</strong> [DESCRIÇÃO]</p>
    <p><strong>Funcionários:</strong> [NÚMERO]</p>
    <p><strong>Objetivo:</strong> [OBJETIVO]</p>
</div>
```

---

### **2. Situação Atual (Slide 2)**

```html
<div class="card reveal-item" data-step="1">
    <h3>❌ [PROBLEMA 1]</h3>
    <p>[Descrição específica do problema]</p>
</div>
<!-- Repetir para 4 problemas -->
```

---

### **3. Solução Proposta (Slide 3)**

```html
<div class="card reveal-item" data-step="1">
    <h3>[ÍCONE] [SERVIÇO]</h3>
    <p><strong>[Destaque]</strong></p>
    <p>[Descrição]</p>
    <div class="differentials" style="margin-top: 15px; padding: 12px; background: #FFDE00; border: none;">
        <p style="font-size: 16px; font-weight: 600; margin: 0;">✅ [Diferencial 1]</p>
        <p style="font-size: 16px; font-weight: 600; margin: 0;">✅ [Diferencial 2]</p>
    </div>
</div>
<!-- Repetir para cada serviço -->
```

---

### **4. Investimento (Slide 6) - CRÍTICO**

**Tabela de preços:**

```html
<div class="price-row reveal-item" data-step="1">
    <span>[SERVIÇO]</span>
    <span>R$ [TABELA]</span>
    <span>R$ [COM DESCONTO]</span>
</div>
```

**Quadrado amarelo (CLÍMAX):**

```html
<div class="final-price-box reveal-item" data-step="8">
    <h3>Investimento Mensal [CLIENTE]</h3>
    <p class="big-price">R$ [VALOR FINAL]</p>
    <p class="small">Economia de R$ [ECONOMIA] (XX% de desconto)</p>
</div>
```

---

### **5. Timeline (Slide 5)**

```html
<div class="box reveal-item" data-step="1">
    <h3>Fase 1: Setup Inicial ([PRAZO])</h3>
    <ul>
        <li><strong>[Período 1]:</strong> [Atividades]</li>
        <li><strong>[Período 2]:</strong> [Atividades]</li>
    </ul>
</div>
```

---

### **6. Comparação Mercado (Slide 7)**

```html
<div class="comparison-row reveal-item" data-step="1">
    <span>[Serviço mercado]</span>
    <span>R$ [PREÇO MERCADO]</span>
</div>
```

---

## 🎨 Estilo Visual (MotherDuck)

**Cores:**
- Background: `#F4EFEA` (beige)
- Texto: `#383838` (dark gray)
- Destaque: `#FFDE00` (yellow)
- Borders: `2px solid #383838`

**Tipografia:**
- Font: `SF Mono`, `Monaco`, monospace
- H1: 48px
- H2: 38px
- H3: 24px
- Body: 19px

**Animações:**
- Fade in + scale: `0.4s cubic-bezier(0.4, 0, 0.2, 1)`
- Hover cards: shadow 8px offset solid

---

## 📊 Checklist Antes de Apresentar

- [ ] Nome do cliente atualizado em todos slides?
- [ ] Valores corretos (tabela, desconto, final)?
- [ ] Prazo de implementação correto?
- [ ] Problemas específicos do cliente no Slide 2?
- [ ] Serviços alinhados com o que foi conversado?
- [ ] Comparação de mercado realista (não exagerada)?
- [ ] Testado navegação (cliques revelam corretamente)?
- [ ] Testado responsividade (resize janela)?
- [ ] Abrir em fullscreen (F) antes de compartilhar tela?

---

## 🎬 Dicas para Videochamada

### **Preparação:**
1. Abrir HTML no navegador
2. Pressionar `F` para fullscreen
3. Testar navegação (clicar ou →)
4. Compartilhar tela inteira (não só janela)

### **Durante Apresentação:**
1. **Slide 1 (Capa):** Deixar 5-10s para cliente processar
2. **Slide 2 (Problemas):** Explicar cada problema enquanto revela
3. **Slide 3 (Solução):** Explicar cada serviço (não apressar)
4. **Slide 6 (Investimento):**
   - Revelar linha por linha (criar tensão)
   - Pausa dramática antes do quadrado amarelo
   - "Esse é o investimento mensal..."
   - Revelar pagamentos únicos por último

### **Ritmo Ideal:**
- 1-2 minutos por slide
- Não apressar Slide 6 (mais importante!)
- Total: 15-20 minutos de apresentação

---

## 🔧 Troubleshooting

### **Animações não funcionam:**
- Verificar `data-total-steps` do slide
- Verificar `data-step` dos items
- Console do navegador (F12) para erros

### **Responsividade quebrada:**
- Padding dos slides: `40px 60px`
- `overflow-y: auto` nos slides
- Fontes reduzidas se necessário

### **Valores não se ajustam:**
- Usar Find & Replace no editor
- Buscar por "R$ " para pegar todos valores
- Conferir quadrado amarelo (step 8) separado

---

## 📚 Exemplos de Uso

### **Caso 1: Up Uniformes (Original)**

**Projeto:** Marketing digital completo (tráfego + vídeos + Instagram)
**Valor:** R$ 3.497/mês
**Prazo:** 10 dias úteis
**Arquivo:** `orcamento_up_uniformes.html`

---

### **Caso 2: Dentista Implantes**

**Projeto:** Sistema de leads Meta Ads + CRM
**Valor:** R$ 10.000 (setup único)
**Customizações:**
- Slide 2: Problemas específicos (dependência indicação, sem leads qualificados)
- Slide 3: 3 serviços (não 6)
- Slide 6: Sem recorrência mensal (só pagamento único)

---

### **Caso 3: Infoprodutor Instagram**

**Projeto:** Automação Instagram 2x/dia
**Valor:** R$ 25.000 (setup) + R$ 5.000/mês
**Customizações:**
- Slide 3: Copy com especificidade estilo Apple
- Slide 6: Ancoragem por tempo economizado (500h/ano)
- Slide 7: Comparação vs agência (R$ 96k/ano)

---

## 🎯 Próximos Passos

1. **Testar template:** Criar proposta teste
2. **Feedback cliente:** Ajustar baseado em reação
3. **Biblioteca de casos:** Salvar versões customizadas
4. **Melhorias futuras:**
   - Modo escuro toggle
   - Exportar para PDF
   - Vídeo de demonstração embutido

---

## 📖 Referências

- **Skill relacionada:** `.claude/skills/orcamento-profissional/`
- **Template base:** `template_proposta_interativa.html`
- **Metodologia:** Precificação por valor (não tempo)
- **Copy:** Frameworks Hormozi (hooks, headlines, ancoragem)
- **Design:** MotherDuck Style (retro-moderno, warm)

---

**Versão:** 1.0
**Criado:** 2025-11-04
**Base:** Proposta Up Uniformes (caso real testado)
