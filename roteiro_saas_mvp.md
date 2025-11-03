# Roteiro: Complete Workflow - Google AI Studio to Production Ready SaaS App

**Tema:** Tutorial de desenvolvimento rápido de SaaS MVP usando Google AI Studio + Claude Code + Supabase + Stripe

**Duração estimada:** 12-15 minutos

**Tom:** Didático, direto ao ponto, focado em velocidade de execução

---

## Slide 1: O Workflow Completo em 1 Hora

**Título:** "De Protótipo AI a SaaS Real em 66 Minutos"

**Conceito:**
É possível transformar um projeto experimental do Google AI Studio em uma aplicação SaaS funcional com autenticação, pagamentos e banco de dados em pouco mais de 1 hora. O segredo está em usar ferramentas que já resolvem problemas complexos (Supabase para auth, Stripe para pagamentos, Claude Code para automação).

**Analogia:**
Pense em montar um carro: antigamente você construía cada peça do zero (motor, rodas, bancos). Hoje você compra componentes prontos e certificados, e apenas os conecta. Google AI Studio te dá o "motor" (a funcionalidade AI), Supabase te dá a "estrutura" (banco de dados + autenticação), e Stripe te dá o "sistema de cobrança".

**Exemplo:**
No vídeo, o desenvolvedor parte de um gerador de thumbnails (Google AI Studio) e em 66 minutos tem: banco de dados relacional, sistema de login com magic link, planos free/pro ($29.99), controle de créditos (50 vs 500 imagens), webhooks do Stripe funcionando, e frontend completo.

**Notas de Gravação:**
- **Abertura impactante:** Mostrar timer começando em 00:00
- **Ênfase:** "Não é sobre fazer perfeito, é sobre fazer FUNCIONAL"
- **Visual:** Split screen mostrando os 4 pilares: Google AI Studio | Supabase | Stripe | Claude Code
- **Transição:** "Vamos quebrar esse workflow em etapas claras"

---

## Slide 2: Por Que Google AI Studio é o Ponto de Partida Ideal

**Título:** "Multimodalidade em Uma Única API"

**Conceito:**
O diferencial do Google AI Studio (Gemini SDK) é a multimodalidade nativa: você consegue processar texto, imagens, vídeos, gerar conteúdo, fazer web scraping, tudo com a mesma API. Isso elimina a necessidade de integrar 5-10 serviços diferentes para criar funcionalidades complexas.

**Analogia:**
É como ter um canivete suíço vs carregar 10 ferramentas separadas. Claude (Anthropic) é excelente para texto, mas se você precisa processar imagens E gerar conteúdo E fazer scraping, você precisaria de OpenAI + Vision API + Scraping Service. Com Gemini, tudo está em um lugar.

**Exemplo:**
O app do vídeo recebe uma imagem de thumbnail, extrai as palavras-chave mais importantes (processamento de texto em imagem), e gera 4 variações de ícones modernos (geração de imagem). Tudo usando apenas o Gemini SDK, sem trocar de API.

**Notas de Gravação:**
- **Demonstração:** Mostrar a interface do Google AI Studio em modo "Build"
- **Contraste:** "Eu AMO Claude, mas ele não faz isso [mostrar exemplo multimodal]"
- **Prático:** Mostrar o prompt real usado: "upload image → extract buzzwords → generate 4 icon variations"
- **Transição:** "Ok, temos o cérebro AI. Agora precisamos da infraestrutura"

---

## Slide 3: Supabase - Database + Auth em Minutos

**Título:** "Backend Completo Sem Escrever Backend"

**Conceito:**
Supabase oferece banco de dados PostgreSQL + autenticação + edge functions + storage, tudo gerenciado. Para MVPs, você pode rodar localmente (Supabase CLI) e depois fazer deploy com um comando. Magic Link Auth elimina a complexidade de senhas, hashing, sessões.

**Analogia:**
É como alugar um apartamento mobiliado vs construir uma casa do zero. Você não precisa instalar encanamento (database schema), sistema elétrico (auth flows), ou móveis (storage). Já está tudo lá, você só configura os detalhes.

**Exemplo:**
No vídeo, com `supabase init` e alguns prompts para Claude Code, foram criados:
- Schema de 3 tabelas (users, generations, subscriptions)
- Magic link auth (email sem senha)
- Edge functions para webhooks do Stripe
- Tudo rodando em localhost para testes, pronto para deploy

**Notas de Gravação:**
- **Mostrar código:** Schema SQL gerado automaticamente (users table, generations table)
- **Demonstração:** Login com magic link (receber email, clicar, estar logado)
- **Dica técnica:** "Use Supabase CLI, não MCP. CLIs são mais confiáveis para automação"
- **Transição:** "Banco e auth resolvidos. Falta monetizar"

---

## Slide 4: Stripe - Monetização em 20 Minutos

**Título:** "Sistema de Créditos + Assinatura Recorrente"

**Conceito:**
Stripe CLI permite testar pagamentos localmente sem subir nada para produção. Você cria produtos/preços, integra checkout, e configura webhooks para atualizar o banco quando alguém paga. Sistema de créditos (50 free, 500 pro) é apenas uma coluna no banco que decrementa a cada uso.

**Analogia:**
Pense em uma máquina de venda automática: você insere moeda (Stripe checkout), a máquina verifica o pagamento (webhook), libera o produto (atualiza créditos no banco), e registra a transação (Supabase log). Tudo automático.

**Exemplo:**
No vídeo:
1. Stripe CLI cria 2 produtos: Free ($0, 50 créditos) e Pro ($29.99/mês, 500 créditos)
2. Claude Code integra Stripe Checkout na página /pricing
3. Webhook escuta evento `checkout.session.completed`
4. Edge function atualiza tabela `subscriptions` e adiciona créditos
5. UI mostra "499 créditos restantes" após gerar 1 thumbnail

**Notas de Gravação:**
- **Mostrar terminal:** `stripe listen --forward-to localhost:54321/functions/v1/stripe-webhook`
- **Demonstração:** Clicar em "Upgrade to Pro", preencher cartão de teste, ver créditos atualizarem
- **Debugar ao vivo:** No vídeo teve erro 404 (webhook errado) → mostra que até erros são rápidos de corrigir
- **Transição:** "Temos AI, banco, auth, pagamentos. Falta a cola que une tudo"

---

## Slide 5: Claude Code - A Cola Que Une Tudo

**Título:** "Automação de Desenvolvimento com IA"

**Conceito:**
Claude Code não é apenas um copilot que sugere código. Ele executa comandos no terminal, edita múltiplos arquivos, lê documentação de APIs, e entende contexto de projetos inteiros. Você descreve o que quer ("adicione magic link auth"), e ele faz: instala dependências, cria arquivos, configura .env, atualiza UI.

**Analogia:**
É como ter um desenvolvedor júnior muito rápido e obediente. Você é o arquiteto (define "quero auth + stripe + créditos"), e ele é o pedreiro (escreve código, roda comandos, testa). Ele não toma decisões de produto, mas executa perfeitamente o que você manda.

**Exemplo:**
Prompts usados no vídeo (ordem cronológica):
1. "Set up Supabase environment with local database"
2. "Add magic link auth, create account + sign in in header"
3. "Create pricing page with 2 plans: Free (50 credits) and Pro (500 credits, $29.99/month)"
4. "Integrate Stripe checkout, add webhooks, show credits in UI"

Em cada prompt, Claude Code criou 5-10 arquivos, rodou 3-5 comandos, e testou localmente.

**Notas de Gravação:**
- **Mostrar split screen:** Prompt do Claude (esquerda) + arquivos sendo criados em tempo real (direita)
- **Dica avançada:** "Use sub-agents para tarefas paralelas (eu esqueci nesse vídeo, mas recomendo)"
- **Realismo:** "Nem sempre funciona de primeira [mostrar erro 401], mas corrigir é rápido"
- **Transição:** "Agora vamos ver tudo funcionando integrado"

---

## Slide 6: Testando o MVP Completo

**Título:** "66 Minutos: Da Ideia ao App Funcional"

**Conceito:**
Um SaaS MVP não precisa ser perfeito. Precisa demonstrar a proposta de valor e validar se alguém pagaria por aquilo. O workflow mostrado prova que a barreira técnica para testar uma ideia caiu drasticamente - de semanas para horas.

**Analogia:**
É como fazer um protótipo de carro: você não precisa de pintura premium, bancos de couro, ou ar-condicionado de 5 zonas. Precisa de 4 rodas, motor, freios, e volante. Se as pessoas gostarem do conceito, DEPOIS você melhora os detalhes.

**Exemplo:**
Funcionalidades testadas no vídeo (ao vivo, na tela):
1. **Cadastro:** Email → recebe magic link → loga automaticamente
2. **Geração:** Upload de imagem → 4 thumbnails gerados (usando Gemini)
3. **Créditos:** Contador decrementa de 50 para 49
4. **Upgrade:** Click em "Upgrade to Pro" → Stripe checkout → pagamento com cartão de teste
5. **Atualização:** Recarrega página, mostra "Pro Plan" e 499 créditos

**Notas de Gravação:**
- **Demonstração ao vivo:** Gravar tela fazendo o fluxo completo (cadastro → geração → upgrade)
- **Celebração:** "1 hora e 6 minutos. De ZERO a isso [mostrar app]"
- **Honestidade:** "Tem bugs? Sim [mostrar que gerações não estavam sendo salvas]. É perfeito? Não. Mas FUNCIONA."
- **Transição:** "Mas e para lançar para o mundo?"

---

## Slide 7: Deploy e Próximos Passos

**Título:** "De localhost a Produção (Bonus)"

**Conceito:**
Lançar o MVP é a parte "fácil" comparado ao resto. Com DigitalOcean CLI (ou Vercel, Railway, Render), você faz: `git init` → `git push` → app no ar. Supabase tem deploy com 1 comando. Stripe já está em modo produção (só trocar keys de test para live).

**Analogia:**
É como mudar de um ensaio fechado (localhost) para um show ao vivo (produção). O palco é o mesmo, os instrumentos são os mesmos, você só precisa abrir as portas para o público entrar.

**Exemplo:**
Passos finais (não mostrados no vídeo, mas mencionados):
1. `supabase link --project-ref your-project` (conecta ao Supabase cloud)
2. `supabase db push` (aplica migrations no banco de produção)
3. Criar app no DigitalOcean: `doctl apps create --spec .do/app.yaml`
4. Configurar .env de produção (Stripe live keys, Supabase prod URL)
5. Git push → deploy automático

**Notas de Gravação:**
- **Tom:** "Eu não vou mostrar deploy nesse vídeo porque seria repetitivo, MAS..."
- **Mostrar terminal:** Comandos que seriam executados (sem executar)
- **Prometer:** "Se vocês quiserem um vídeo só sobre deploy, deixem nos comentários"
- **Realidade:** "A parte difícil não é colocar no ar. É conseguir os primeiros clientes."
- **Transição:** "Então, o que aprendemos?"

---

## Slide 8: Lições e Filosofia do MVP Rápido

**Título:** "Velocidade > Perfeição (Para Validação)"

**Conceito:**
A maior armadilha de desenvolvedores é gastar 6 meses construindo algo que ninguém quer. O workflow mostrado inverte isso: em 1-2 dias você tem um MVP testável, coloca na frente de 10 pessoas reais, e descobre se a ideia faz sentido. Se não faz, você perdeu 2 dias, não 6 meses.

**Analogia:**
É como testar uma receita nova: você não abre um restaurante de 500 lugares antes de saber se as pessoas gostam da comida. Você faz 10 pratos, dá para amigos provarem, ajusta o tempero, e SÓ ENTÃO pensa em escalar.

**Exemplo:**
No vídeo, o app gerou thumbnails "ok" (não perfeitas). Mas isso não importa para validação. As perguntas são:
1. Alguém pagaria $30/mês por isso?
2. O problema (criar thumbnails) é real?
3. A solução (AI gerando ícones) é valiosa?

Se sim, DEPOIS você melhora a qualidade da AI, adiciona edição manual, templates, etc.

**Notas de Gravação:**
- **Mensagem final:** "Não tenha medo de lançar algo imperfeito"
- **Quote:** "Feito é melhor que perfeito" (mostrar na tela)
- **Call to action:**
  - Link 1: Free dev discovery call (primeiros 2 links na descrição)
  - Link 2: Playlist com mais tutoriais de SaaS MVP
- **Despedida:** "Se você assistiu até aqui, você é lenda. Até o próximo!"
- **Easter egg:** Deixar timer visível no canto (mostra 1:06:00 ao final)

---

## RESUMO EXECUTIVO (Para Edição)

**Cortes importantes:**
- 00:00 - Timer começando (criar urgência)
- 10:00 - Supabase rodando (primeira vitória)
- 16:30 - Magic link funcionando (segunda vitória)
- 52:00 - Stripe checkout completo (terceira vitória)
- 1:06:00 - App completo testado (grande final)

**B-roll sugerido:**
- Google AI Studio interface (slides 2)
- Supabase dashboard (slide 3)
- Stripe dashboard com webhooks (slide 4)
- Claude Code escrevendo código em tempo real (slide 5)
- Teste completo do app funcionando (slide 6)

**Pontos de ênfase:**
- Multimodalidade (Google vs Claude)
- Velocidade (1 hora, não 1 semana)
- Imperfeição é OK (bugs mostrados, não escondidos)
- Validação > Perfeição

**Tom geral:**
Didático mas real. Mostrar sucessos E erros. Não vender sonho ("fique rico rápido"), mas empoderar ("você PODE fazer isso").

---

**FIM DO ROTEIRO**
