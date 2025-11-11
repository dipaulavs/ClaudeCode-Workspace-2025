---
name: login-google
description: Implementar autenticação Google OAuth 2.0 em aplicações web (Flask, Node, etc.) com configuração completa do Google Cloud Console, rotas OAuth, proteção de páginas e UI de login. Auto-invoca quando usuário pede para criar sistema de login/registro com Google.
---

# Login Google OAuth 2.0

Implementar autenticação "Entrar com Google" (OAuth 2.0) em qualquer aplicação web, garantindo que funcione de primeira sem erros de redirect_uri_mismatch.

## Quando Usar Esta Skill

Auto-invocar quando usuário solicita:
- "Criar sistema de login com Google"
- "Implementar autenticação OAuth"
- "Adicionar botão Entrar com Google"
- "Sistema de registro com conta Google"
- Qualquer menção a OAuth 2.0 + Google

## Diferença: Service Account vs OAuth Client

**IMPORTANTE:** Entender a diferença antes de começar.

```
Service Account (acesso app-to-app)
├─> Identidade da APLICAÇÃO
├─> Sem consentimento do usuário
├─> Para APIs server-to-server (Sheets, Drive)
└─> NÃO serve para login de usuários

OAuth Client ID (login de usuários)
├─> Identidade dos USUÁRIOS
├─> Requer consentimento ("Permitir acesso")
├─> Para "Entrar com Google"
└─> É isso que precisamos criar
```

**Para login de usuários = OAuth Client ID** (não Service Account!)

## Workflow Completo

### Etapa 1: Configurar Google Cloud Console

**CRÍTICO:** Configurar corretamente no Google Console ANTES de escrever código.

#### 1.1 Acessar Google Console

1. https://console.cloud.google.com
2. Selecionar projeto (ou criar novo)
3. Menu: **APIs & Services → Credentials**

#### 1.2 Configurar OAuth Consent Screen

**Se já configurado, pular para 1.3**

1. Aba **"OAuth consent screen"**
2. User Type: **External** → CREATE
3. Preencher:
   - App name: Nome do app (ex: "Dashboard LF Imóveis")
   - User support email: Seu email
   - Application home page: URL produção (ex: https://app.example.com)
   - Authorized domains: Domínio raiz (ex: example.com)
   - Developer contact: Seu email
4. SAVE AND CONTINUE

5. **Scopes:** ADD OR REMOVE SCOPES
   - Marcar: `openid`
   - Marcar: `../auth/userinfo.email`
   - Marcar: `../auth/userinfo.profile`
   - UPDATE → SAVE AND CONTINUE

6. **Test users:** ADD USERS
   - Adicionar emails autorizados (importante em modo Testing)
   - ADD → SAVE AND CONTINUE

7. BACK TO DASHBOARD

#### 1.3 Criar OAuth Client ID

1. Aba **"Credentials"** → **+ CREATE CREDENTIALS**
2. Selecionar: **OAuth client ID**
3. Application type: **Web application**
4. Name: Nome descritivo (ex: "Dashboard OAuth Client")

5. **Authorized JavaScript origins:**
   - Adicionar URL produção: `https://seu-dominio.com`
   - Adicionar URL dev (opcional): `http://localhost:8000`

6. **Authorized redirect URIs:**
   ```
   https://seu-dominio.com/authorize
   http://localhost:8000/authorize  (opcional, dev)
   ```

   **CRÍTICO:** A URI EXATA que o código vai usar. Sem trailing slash!

7. CREATE

8. **COPIAR CREDENCIAIS:**
   - Client ID: `123456-abc.apps.googleusercontent.com`
   - Client Secret: `GOCSPX-abc123`

   **Salvar em local seguro!**

### Etapa 2: Estrutura do Código (Flask)

Criar estrutura modular para autenticação:

```
app/
├── auth/
│   ├── __init__.py
│   ├── google_oauth.py      # Config Authlib
│   ├── decorators.py         # @login_required
│   └── models.py             # User model (SQLite)
├── config/
│   └── oauth_credentials.json  # Credenciais OAuth (GITIGNORE!)
├── static/
│   └── login.html            # Página de login
├── app.py                    # Flask app principal
└── .gitignore                # NUNCA commitar credenciais!
```

### Etapa 3: Implementação Backend (Flask + Authlib)

#### 3.1 Instalar Dependências

```bash
pip install Authlib Flask
```

Atualizar `requirements.txt`:
```
Flask==3.0.0
Authlib==1.3.0
```

#### 3.2 Salvar Credenciais OAuth

Criar `config/oauth_credentials.json`:

```json
{
  "web": {
    "client_id": "SEU_CLIENT_ID.apps.googleusercontent.com",
    "client_secret": "GOCSPX-SEU_CLIENT_SECRET",
    "redirect_uris": [
      "https://seu-dominio.com/authorize"
    ]
  }
}
```

**Adicionar ao `.gitignore`:**
```gitignore
# OAuth Credentials (NUNCA COMMITAR!)
config/oauth_credentials.json
```

#### 3.3 Criar Módulo de Autenticação

**auth/__init__.py:**
```python
from .google_oauth import init_oauth
from .decorators import login_required
from .models import UserModel

__all__ = ['init_oauth', 'login_required', 'UserModel']
```

**auth/google_oauth.py:**
```python
from authlib.integrations.flask_client import OAuth
from flask import Flask
import json
from pathlib import Path

def init_oauth(app: Flask):
    # Carregar credenciais
    config_path = Path(__file__).parent.parent / 'config' / 'oauth_credentials.json'
    with open(config_path, 'r') as f:
        credentials = json.load(f)['web']

    app.config['GOOGLE_CLIENT_ID'] = credentials['client_id']
    app.config['GOOGLE_CLIENT_SECRET'] = credentials['client_secret']

    oauth = OAuth(app)
    google = oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )

    return google
```

**auth/decorators.py:**
```python
from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
```

**auth/models.py:**

Ver `references/user_model.md` para implementação completa do modelo de usuário SQLite.

#### 3.4 Configurar Flask App

**app.py:**
```python
from flask import Flask, session, redirect, url_for, send_from_directory
import secrets
from auth import init_oauth, login_required, UserModel
from database import Database

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Configurações de sessão segura
app.config.update(
    SESSION_COOKIE_SECURE=True,  # HTTPS apenas
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=86400  # 24h
)

# Inicializar OAuth
google_oauth = init_oauth(app)

# Inicializar banco
db = Database()
user_model = UserModel(db)

# ==================== ROTAS DE AUTENTICAÇÃO ====================

@app.route('/login')
def login():
    """Página de login - redireciona se já logado"""
    if 'user' in session:
        return redirect('/')
    return send_from_directory('static', 'login.html')


@app.route('/auth/google')
def auth_google():
    """Inicia fluxo OAuth com Google"""
    # CRÍTICO: URL EXATA configurada no Google Console
    redirect_uri = 'https://seu-dominio.com/authorize'
    return google_oauth.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    """Callback do OAuth Google"""
    try:
        # Troca código por token
        token = google_oauth.authorize_access_token()
        user_info = token.get('userinfo')

        if not user_info:
            return {'error': 'Falha ao obter informações'}, 400

        # Salva usuário no banco
        resultado = user_model.criar_ou_atualizar(user_info, token)

        if not resultado['success']:
            return {'error': resultado['error']}, 500

        # Salva na sessão
        session.permanent = True
        session['user'] = {
            'id': resultado['user_id'],
            'google_id': user_info['sub'],
            'email': user_info['email'],
            'name': user_info.get('name', ''),
            'picture': user_info.get('picture', '')
        }

        return redirect('/')

    except Exception as e:
        return {'error': f'Erro na autenticação: {str(e)}'}, 500


@app.route('/logout')
def logout():
    """Faz logout"""
    session.pop('user', None)
    return redirect('/login')


# ==================== ROTAS PROTEGIDAS ====================

@app.route('/')
@login_required
def dashboard():
    """Dashboard (requer autenticação)"""
    user = session.get('user')
    return f"Olá, {user['name']}!"
```

### Etapa 4: Frontend - Página de Login

Ver `assets/login_template.html` para template completo da página de login.

### Etapa 5: Deploy e Validação

#### 5.1 Deploy na VPS

```bash
# Commit código (SEM credenciais!)
git add .
git commit -m "feat: implementar login Google OAuth"
git push origin main

# Copiar credenciais OAuth para VPS (SCP)
scp config/oauth_credentials.json user@vps:/path/to/app/config/

# Deploy
ssh user@vps "cd /path/to/app && git pull && docker service update --force app"
```

#### 5.2 Validar Funcionamento

1. **Testar redirect:**
   ```bash
   curl -I https://seu-dominio.com/
   # Deve retornar: Location: /login
   ```

2. **Testar página de login:**
   ```bash
   curl -I https://seu-dominio.com/login
   # Deve retornar: 200 OK
   ```

3. **Testar botão "Entrar com Google":**
   - Acessar https://seu-dominio.com/login
   - Clicar em "Entrar com Google"
   - Deve abrir tela de login do Google
   - Após login, redirecionar para dashboard

#### 5.3 Troubleshooting

**Erro: redirect_uri_mismatch**

```
Causa: URI no código ≠ URI no Google Console
Fix:
1. Verificar URL EXATA em app.py (linha do redirect_uri)
2. Acessar Google Console → OAuth Client → Edit
3. Adicionar URI EXATA em "Authorized redirect URIs"
4. Salvar e testar novamente
```

**Erro: ModuleNotFoundError: authlib**

```
Causa: Authlib não instalado no container
Fix:
1. Verificar requirements.txt tem Authlib==1.3.0
2. Rebuild container ou docker service update --force
```

**Erro: SSL Certificate Error**

```
Causa: Traefik não provisionou SSL
Fix:
1. Verificar labels Traefik no docker-compose.yml
2. Ver references/traefik_ssl.md
```

## Checklist de Validação

Antes de considerar completo, verificar:

- [ ] OAuth Client ID criado no Google Console
- [ ] Consent Screen configurado (External, scopes corretos)
- [ ] Redirect URIs configuradas EXATAMENTE como no código
- [ ] Credenciais salvas em `config/oauth_credentials.json`
- [ ] Arquivo adicionado ao `.gitignore`
- [ ] Authlib instalado (`requirements.txt`)
- [ ] Módulo `auth/` criado com todos arquivos
- [ ] Rotas `/login`, `/auth/google`, `/authorize`, `/logout` implementadas
- [ ] Decorator `@login_required` aplicado em rotas protegidas
- [ ] Página de login criada e funcionando
- [ ] Credenciais copiadas para VPS (SCP)
- [ ] Deploy realizado com sucesso
- [ ] Teste manual: Login funciona end-to-end
- [ ] Teste manual: Logout funciona
- [ ] Teste manual: Rotas protegidas redirecionam para login

## Referências

- `references/user_model.md` - Implementação completa do modelo User com SQLite
- `references/oauth_flow.md` - Diagrama técnico do fluxo OAuth 2.0
- `assets/login_template.html` - Template completo da página de login bonita

## Auto-Correction System

This skill includes an automatic error correction system that learns from mistakes and prevents them from happening again.

### How It Works

When a script or command in this skill fails:

1. **Detect the error** - The system identifies what went wrong
2. **Fix automatically** - Updates the skill's code/instructions
3. **Log the learning** - Records the fix in LEARNINGS.md
4. **Prevent recurrence** - Same error won't happen again

### Using Auto-Correction

**Scripts available:**

```bash
# Fix a problem in this skill's SKILL.md
python3 scripts/update_skill.py <old_text> <new_text>

# Log what was learned
python3 scripts/log_learning.py <error_description> <fix_description> [line]
```

**Example workflow when error occurs:**

```bash
# 1. Fix the error in SKILL.md
python3 scripts/update_skill.py \
    "redirect_uri = url_for('authorize', _external=True)" \
    "redirect_uri = 'https://seu-dominio.com/authorize'"

# 2. Log the learning
python3 scripts/log_learning.py \
    "redirect_uri_mismatch porque url_for() gerava URL errada" \
    "Usar URL hardcoded EXATA configurada no Google Console" \
    "SKILL.md:245"
```

### LEARNINGS.md

All fixes are automatically recorded in `LEARNINGS.md`:

```markdown
### 2025-01-10 - redirect_uri_mismatch error

**Problema:** url_for() gerava URL diferente da configurada no Google Console
**Correção:** Usar URL hardcoded: redirect_uri = 'https://dominio.com/authorize'
**Linha afetada:** SKILL.md:245
**Status:** ✅ Corrigido
```

This creates a history of improvements and ensures mistakes don't repeat.
