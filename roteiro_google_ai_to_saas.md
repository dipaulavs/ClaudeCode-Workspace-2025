# Google AI Studio → SaaS MVP Workflow

## Introdução: O Desafio
**Conceito:** Transformar projetos do Google AI Studio em aplicações SaaS prontas para produção
**Notas:** Enfatizar que o processo é rápido (1h06min no total) e utiliza ferramentas modernas

- Projeto inicial no Google AI Studio é apenas MVP/frontend
- Falta backend, autenticação, banco de dados e pagamentos
- Objetivo: workflow completo e replicável

## Stack Tecnológica
**Conceito:** Ferramentas escolhidas para máxima velocidade de desenvolvimento

- Google AI Studio (Gemini SDK multimodal)
- Supabase (Database + Auth via Magic Link)
- Stripe (Pagamentos + CLI para webhooks)
- Claude Code (Automação de desenvolvimento)
**Notas:** Mencionar que Gemini SDK é multimodal (imagens, vídeos, texto, scraping) em uma única API

## Etapa 1: Criar o Protótipo AI (Google AI Studio)
**Conceito:** Usar interface visual do Google AI Studio para prototipar funcionalidade core

- Build → Descrever funcionalidade desejada
- Exemplo: "Upload image → Extract keywords → Generate 4 thumbnail assets"
- Google gera frontend + lógica de IA
- Download do projeto inicial
**Notas:** Esta etapa gera apenas frontend puro. Não tem backend ainda.

## Etapa 2: Setup do Banco de Dados (Supabase)
**Conceito:** Configurar Supabase local para armazenar dados de usuários e gerações

- Comando: `supabase init` (requer Supabase CLI)
- Schema automático: users, image_generations, subscription_status
- Database local para testes
- Variáveis .env para trocar depois
**Notas:** Supabase permite desenvolvimento 100% local antes de deploy

## Etapa 3: Autenticação Magic Link (Supabase Auth)
**Conceito:** Sistema de login sem senha usando links mágicos por email

- Magic Link = email com token único
- Usuário clica → Login automático
- Integração nativa com Supabase
- UI: Header com "Create Account" e "Sign In"
**Notas:** Testar criação de conta + login antes de avançar

## Etapa 4: Integração Stripe (Pagamentos)
**Conceito:** Sistema de créditos com plano Free e Pro

- Stripe CLI: `stripe login` + webhook listener local
- 2 planos: Free (50 imagens/mês) | Pro ($29.99 = 500 imagens/mês)
- Stripe Checkout para upgrade
- Webhooks processam confirmação de pagamento
**Notas:** Webhooks DEVEM rodar na URL correta (conferir listener antes de testar)

## Etapa 5: Backend com Edge Functions (Supabase)
**Conceito:** Backend serverless usando Supabase Edge Functions (Deno)

- Edge Functions = código rodando no edge (sem servidor tradicional)
- Processa webhooks do Stripe
- Atualiza créditos do usuário
- Valida limites de uso
**Notas:** Alternativa ao FastAPI ou Express. Puramente serverless.

## Etapa 6: Sistema de Créditos
**Conceito:** Tracking de uso por usuário com UI visual

- Cada geração consome 1 crédito
- UI mostra créditos restantes
- Bloqueia geração se créditos = 0
- Webhook do Stripe adiciona créditos após pagamento
**Notas:** Testar fluxo completo: Free → Upgrade → Pro → Gerar imagem

## Resumo Final: Resultado em 1h06min
**Conceito:** De zero a SaaS funcional em tempo recorde

**O Que Temos:**
- ✅ AI funcional (geração de thumbnails)
- ✅ Auth (Magic Link)
- ✅ Database (Supabase local)
- ✅ Pagamentos (Stripe + créditos)
- ✅ Backend serverless (Edge Functions)

**Como Funciona:**
1. Usuário cria conta (Magic Link)
2. Ganha 50 créditos grátis
3. Faz upgrade para Pro ($29.99)
4. Ganha 500 créditos
5. Usa créditos para gerar assets

**Por Que Funciona:**
- Gemini SDK multimodal = menos APIs
- Supabase = DB + Auth + Backend em um só
- Stripe CLI = webhooks locais instantâneos
- Claude Code = automação de tarefas repetitivas

**Próximos Passos (não coberto no vídeo):**
- Deploy no DigitalOcean via CLI
- Push para GitHub
- Configurar variáveis de produção

## Call to Action
**Se você chegou até aqui, você é uma LENDA! 🚀**

👍 Dá um LIKE no vídeo
🔔 INSCREVA-SE no canal
📸 Me segue no Instagram: @eusoupromptus

_Próximo vídeo: Deploy completo no DigitalOcean!_
