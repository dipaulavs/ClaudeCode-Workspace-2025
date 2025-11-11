# OAuth 2.0 Flow - Diagrama Técnico

Fluxo completo do OAuth 2.0 com Google, do clique até o login.

## Diagrama de Sequência

```
[USUÁRIO] ──1──> [FLASK /login]
                     │
                     │ Exibe página login.html
                     ↓
                [Usuário vê botão "Entrar com Google"]
                     │
                     │ 2. Clica no botão
                     │ href="/auth/google"
                     ↓
                [FLASK /auth/google]
                     │
                     │ 3. google_oauth.authorize_redirect(redirect_uri)
                     │ Gera URL do Google com:
                     │ - client_id
                     │ - redirect_uri (https://app.com/authorize)
                     │ - scope (openid email profile)
                     │ - state (CSRF protection)
                     ↓
        [GOOGLE OAuth] https://accounts.google.com/o/oauth2/auth?...
                     │
                     │ 4. Usuário faz login no Google
                     │ 5. Google pede autorização
                     ↓
        ┌────────────┴────────────┐
        │ Permitir acesso?         │
        │ ☑ Email                  │
        │ ☑ Perfil                 │
        └──────────┬───────────────┘
                   │ 6. AUTORIZA
                   ↓
         [Google redireciona com código]
                   │
      7. Redirect: https://app.com/authorize?code=ABC123&state=XYZ
                   ↓
              [FLASK /authorize]
                   │
      8. google_oauth.authorize_access_token()
                   │
          ┌────────┴────────┐
          │ POST /token     │
          │ code=ABC123     │
          │ client_secret   │
          └────────┬────────┘
                   │
         [GOOGLE retorna tokens]
                   │
      9. Response:
         {
           "access_token": "ya29.abc...",
           "refresh_token": "1//xyz...",
           "expires_in": 3600,
           "token_type": "Bearer",
           "scope": "openid email profile",
           "userinfo": {
             "sub": "1234567890",
             "email": "user@gmail.com",
             "name": "User Name",
             "picture": "https://..."
           }
         }
                   ↓
              [FLASK /authorize]
                   │
      10. user_model.criar_ou_atualizar(user_info, token)
                   │
         ┌─────────┴─────────┐
         │ INSERT/UPDATE DB  │
         │ session['user']   │
         └─────────┬─────────┘
                   │
      11. redirect('/')
                   ↓
         [USUÁRIO LOGADO ✅]
```

## Componentes do Fluxo

### 1. Iniciação (Frontend)

```html
<a href="/auth/google">Entrar com Google</a>
```

### 2. Redirect para Google (Backend)

```python
@app.route('/auth/google')
def auth_google():
    redirect_uri = 'https://app.com/authorize'
    return google_oauth.authorize_redirect(redirect_uri)
```

**URL gerada:**
```
https://accounts.google.com/o/oauth2/auth?
  response_type=code&
  client_id=123456.apps.googleusercontent.com&
  redirect_uri=https://app.com/authorize&
  scope=openid+email+profile&
  state=random_csrf_token
```

### 3. Usuário Autoriza no Google

Google mostra tela:
- Login (se não logado)
- Consentimento (primeira vez)
- Redirect automático (após primeira vez)

### 4. Callback com Código

Google redireciona para:
```
https://app.com/authorize?code=4/0AY0e...&state=xyz
```

### 5. Troca Código por Token (Backend)

```python
@app.route('/authorize')
def authorize():
    token = google_oauth.authorize_access_token()
    user_info = token.get('userinfo')
    # Salvar usuário...
```

**Request interno (Authlib faz automaticamente):**
```http
POST https://oauth2.googleapis.com/token
Content-Type: application/x-www-form-urlencoded

code=4/0AY0e...&
client_id=123456.apps.googleusercontent.com&
client_secret=GOCSPX-abc123&
redirect_uri=https://app.com/authorize&
grant_type=authorization_code
```

**Response:**
```json
{
  "access_token": "ya29.a0AfH6SMBx...",
  "refresh_token": "1//0gLy4BQp...",
  "expires_in": 3599,
  "scope": "openid https://www.googleapis.com/auth/userinfo.email ...",
  "token_type": "Bearer",
  "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI..."
}
```

### 6. Decode UserInfo

Authlib decodifica automaticamente o `id_token` (JWT) e retorna:

```python
user_info = {
    'sub': '1234567890',           # Google ID único
    'email': 'user@gmail.com',
    'name': 'User Name',
    'picture': 'https://lh3.googleusercontent.com/...',
    'email_verified': True
}
```

### 7. Persistência

```python
# Salvar no banco
user_model.criar_ou_atualizar(user_info, token)

# Salvar na sessão
session['user'] = {
    'google_id': user_info['sub'],
    'email': user_info['email'],
    'name': user_info['name'],
    'picture': user_info['picture']
}
```

## Segurança

### CSRF Protection (State Parameter)

Authlib gera automaticamente um token `state` aleatório:

1. Salva na sessão ao redirecionar
2. Google retorna o mesmo `state`
3. Authlib valida se são iguais
4. Previne CSRF attacks

### HTTPS Obrigatório

- Redirect URIs devem ser HTTPS em produção
- Google rejeita HTTP (exceto localhost)
- SESSION_COOKIE_SECURE=True

### Scopes Mínimos

```python
scope='openid email profile'
```

- `openid` - Identificador único
- `email` - Endereço de email
- `profile` - Nome e foto

## Erros Comuns

### redirect_uri_mismatch

**Causa:** URI no código ≠ URI no Google Console

**Fix:** Verificar linha EXATA:
```python
redirect_uri = 'https://app.com/authorize'  # SEM trailing slash!
```

### invalid_client

**Causa:** Client ID ou Secret incorretos

**Fix:** Verificar credenciais em `config/oauth_credentials.json`

### access_denied

**Causa:** Usuário clicou "Cancelar" no Google

**Fix:** Implementar tratamento de erro na rota `/authorize`
