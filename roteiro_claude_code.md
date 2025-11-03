# Claude Code - Assistente de Programação Inteligente

## Slide 1: O Que É Claude Code?

**Conceito:** Um assistente IA que executa ações diretamente no seu computador

**Analogia:** Imagine ter um colega programador ao seu lado que não só sugere o código, mas realmente o implementa - abre arquivos, edita código, roda comandos, tudo em tempo real.

**Como funciona na prática:**
- Você: "Cria um botão de login"
- Claude Code: Abre o arquivo → Escreve o código → Salva
- Resultado: Botão implementado

**Diferença do ChatGPT:**
→ ChatGPT: Gera código (você copia/cola)
→ Claude Code: Executa código (modificação direta)

**Notas:** Enfatizar a autonomia - não é conversa, é execução real.

## Slide 2: Ferramentas Disponíveis

**Conceito:** Claude Code tem acesso a ferramentas para interagir com o sistema

**Analogia:** Um cérebro inteligente precisa de "mãos" para agir. As ferramentas são essas extensões que permitem Claude modificar seu projeto.

**5 Ferramentas Principais:**

→ **Read** (Leitura)
   Acessa e interpreta arquivos do projeto
   Exemplo: "Mostra o código de autenticação"

→ **Write** (Criação)
   Gera novos arquivos no projeto
   Exemplo: "Cria um arquivo de configuração"

→ **Edit** (Modificação)
   Altera arquivos existentes com precisão
   Exemplo: "Muda a cor primária de azul para verde"

→ **Bash** (Terminal)
   Executa comandos do sistema
   Exemplo: "Instala a biblioteca React Query"

→ **Grep** (Busca)
   Localiza padrões no código
   Exemplo: "Onde está definida a função de login?"

**Notas:** Ferramentas são a interface entre inteligência (Claude) e ação (modificações reais).

## Slide 3: Fluxo de Trabalho

**Conceito:** Conversa → Análise → Planejamento → Confirmação → Execução

**Analogia:** Como trabalhar com um desenvolvedor sênior: você explica o que quer, ele analisa o projeto, propõe uma solução, você aprova, e ele implementa.

**Fluxo Completo:**

**PASSO 1:** Solicitação
"Implementa dark mode no site"

↓

**PASSO 2:** Análise
Claude lê arquivos relevantes e entende a estrutura

↓

**PASSO 3:** Planejamento
"Vou criar ThemeProvider.js, modificar App.js e adicionar estilos CSS. Confirma?"

↓

**PASSO 4:** Aprovação
Você valida ou ajusta o plano

↓

**PASSO 5:** Implementação
Claude executa todas as mudanças

↓

**PASSO 6:** Validação
Dark mode funcionando ✓

**Notas:** Sempre há controle humano - nada é executado sem aprovação prévia.

## Slide 4: Skills (Capacidades Especializadas)

**Conceito:** Skills são contextos especializados que Claude ativa automaticamente

**Analogia:** Como um profissional que troca de "chapéu" conforme a tarefa - veste chapéu de designer para UI, chapéu de arquiteto para estrutura de dados, etc.

**Como funcionam:**

Você: "Valida essa ideia de aplicativo"
↓
Claude detecta contexto: Validação de produto
↓
Ativa skill: **idea-validator**
↓
Assume papel: Especialista em análise de mercado
↓
Entrega: Análise de viabilidade, saturação, monetização

**Exemplos de Skills:**
→ **idea-validator** = Valida viabilidade de produtos
→ **product-designer** = Cria interfaces profissionais
→ **marketing-writer** = Produz copy de marketing
→ **adaptive-mentor** = Explica conceitos técnicos

**Notas:** Skills mudam o comportamento de Claude automaticamente baseado no contexto da conversa.

## Slide 5: Exemplo Prático

**Conceito:** De requisito a implementação em minutos

**Analogia:** Aceleração de produtividade - tarefas que levariam 30 minutos manualmente são resolvidas em 2-3 minutos.

**Cenário:** Adicionar botão de "curtir" na página

**00:00 - Requisito:**
"Adiciona botão de curtir com contador na página inicial"

**00:15 - Análise:**
Read index.html → Read styles.css → Entende estrutura atual

**00:30 - Planejamento:**
"Vou adicionar HTML no index (linha 45), CSS para estilo, e JavaScript para funcionalidade. Posso prosseguir?"

**00:45 - Aprovação:**
"Sim, implementa"

**01:00 - Execução:**
Edit index.html → Edit styles.css → Write like.js

**01:30 - Teste:**
Abre página → Valida funcionamento

**02:00 - Concluído**
Feature implementada ✓

**Comparação:**
Manual: 15-30 minutos | Claude Code: 2 minutos

**Notas:** Velocidade vem da automação de tarefas mecânicas, não da inteligência bruta.

## Slide 6: CLAUDE.md (Configuração do Workspace)

**Conceito:** Arquivo que define o comportamento de Claude para seu projeto específico

**Analogia:** Manual de operação personalizado - como instruções específicas que você daria a um novo desenvolvedor entrando no projeto.

**Conteúdo do CLAUDE.md:**

→ **Regras do projeto:**
"Sempre usar TypeScript strict mode"
"Preferir composition sobre inheritance"

→ **Templates e scripts:**
"Para deploy, usar scripts/deploy.sh"
"Para testes, usar Jest com coverage"

→ **Skills ativadas:**
"11 skills disponíveis no workspace"

→ **Preferências de comunicação:**
"Respostas concisas e objetivas"
"Sempre solicitar confirmação antes de criar arquivos"

**Resultado:**
Claude se adapta ao padrão e fluxo específico do seu projeto

**Notas:** CLAUDE.md torna Claude consistente com as práticas estabelecidas em cada projeto.

## Slide 7: Vantagens Práticas

**Conceito:** Ganhos mensuráveis em produtividade, qualidade e aprendizado

**Analogia:** Multiplicador de capacidade - como ter ferramentas power tools em vez de ferramentas manuais.

**VANTAGEM 1: Velocidade**

Automação de tarefas repetitivas:
→ Criar formulário: 30 min → 3 min
→ Configurar autenticação: 2h → 15 min
→ Implementar API REST: 1 dia → 2 horas

**VANTAGEM 2: Consistência**

Código padronizado e livre de erros comuns:
→ Sem erros de sintaxe
→ Padrões de projeto aplicados automaticamente
→ Melhores práticas seguidas por padrão

**VANTAGEM 3: Aprendizado Contínuo**

Explicações contextuais durante execução:
→ "Usando async/await aqui para melhor legibilidade"
→ "Aplicando pattern Observer para reatividade"
→ Você aprende observando decisões em contexto real

**Conclusão:**
Não substitui desenvolvedor - amplifica capacidade. Você define estratégia, Claude executa táticas.

**Notas:** Claude Code é ferramenta de produtividade, não substituição de raciocínio humano.

## Slide 8: Resumo e Próximos Passos

**Conceito:** Claude Code em 3 pontos essenciais

**Analogia:** Como um resumo executivo - os 3 pilares que você precisa lembrar sobre a ferramenta.

**O QUE É:**
→ Assistente IA com acesso direto ao sistema
→ Não apenas sugere - executa modificações reais
→ 5 ferramentas principais: Read, Write, Edit, Bash, Grep

**COMO FUNCIONA:**
→ Fluxo: Solicitação → Análise → Planejamento → Aprovação → Execução
→ Você mantém controle total (sempre pede confirmação)
→ Skills especializadas ativam automaticamente

**POR QUE USAR:**
→ Velocidade: Tarefas de horas viram minutos
→ Consistência: Código padronizado e livre de erros
→ Aprendizado: Explicações contextuais em tempo real

**PRÓXIMOS PASSOS:**

✓ Experimente com tarefa simples primeiro
✓ Configure CLAUDE.md para seu projeto
✓ Explore skills disponíveis conforme necessário

**Lembre-se:** Você é o arquiteto, Claude é o executor.

**Notas:** Encerrar com mensagem motivadora - ferramenta está pronta para uso imediato.

## Slide 9: Obrigado!

**Conceito:** Gostou do conteúdo? Apoie o canal!

**Call-to-Action:**

👍 **DEIXE SEU LIKE** se o vídeo foi útil

🔔 **INSCREVA-SE NO CANAL** para mais conteúdo sobre IA

📱 **SIGA NO INSTAGRAM** @eusoupromptus
   Bastidores, dicas rápidas e novidades em primeira mão

**Até o próximo vídeo!** 🚀

**Notas:** CTA visual e direto - incentivar engajamento sem ser insistente.
