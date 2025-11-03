# YouTube Thumbnail - Troubleshooting

Guia de resolução de problemas comuns.

---

## 🔍 Diagnóstico Rápido

| Sintoma | Causa Provável | Seção |
|---------|----------------|-------|
| Texto ilegível/pequeno | Template mal formatado | [#1](#problema-1-texto-ilegível-ou-muito-pequeno) |
| Foto não aparece | URL inválida | [#2](#problema-2-foto-base-não-aparece) |
| Cores erradas | Paleta modificada | [#3](#problema-3-cores-diferentes-do-esperado) |
| Layout invertido | Posição texto/foto trocada | [#4](#problema-4-layout-invertido-texto-direita) |
| Timeout/demora muito | API lenta ou muitas tasks | [#5](#problema-5-timeout-ou-processamento-muito-lento) |
| Split lighting fraco | Iluminação mal descrita | [#6](#problema-6-split-lighting-não-aparece) |
| Script não executa | Dependências faltando | [#7](#problema-7-script-não-executa) |
| 0/5 thumbnails geradas | API key inválida | [#8](#problema-8-nenhuma-thumbnail-gerada) |

---

## Problema 1: Texto Ilegível ou Muito Pequeno

### Sintoma
Texto aparece pequeno demais, cortado, ou ilegível na thumbnail.

### Causa
- Título muito longo (mais de 20 caracteres)
- Subtítulo muito longo (mais de 25 caracteres)
- Formato de texto incorreto

### Solução

✅ **Mantenha textos curtos:**

**Bom:**
```
Título: "PRODUTIVIDADE 10X"       ← 16 caracteres
Subtítulo: "MÉTODO COMPROVADO"    ← 17 caracteres
```

**Ruim:**
```
Título: "COMO AUMENTAR SUA PRODUTIVIDADE"  ← 32 caracteres (muito longo!)
Subtítulo: "O MELHOR MÉTODO DO MUNDO TODO"  ← 31 caracteres (muito longo!)
```

✅ **Use abreviações estratégicas:**
- "INTELIGÊNCIA ARTIFICIAL" → "IA REVOLUCIONÁRIA"
- "PRODUTIVIDADE MÁXIMA" → "PRODUTIVIDADE 10X"
- "MARKETING DIGITAL" → "MARKETING 3.0"

✅ **Teste em tamanho reduzido:**
Visualize a thumbnail em 120x68px (tamanho real no feed do YouTube) para garantir legibilidade.

---

## Problema 2: Foto Base Não Aparece

### Sintoma
Thumbnail gerada sem a foto, ou com foto diferente.

### Causa
- URL da foto base incorreta ou expirada
- Formato de URL inválido

### Solução

✅ **Use a URL correta:**
```
https://media.loop9.com.br/s/C9WLo3EytYjNKwm/download/foto1.jpg
```

✅ **Verifique se URL está acessível:**
```bash
curl -I https://media.loop9.com.br/s/C9WLo3EytYjNKwm/download/foto1.jpg
```

✅ **Se URL expirou:**
1. Fazer novo upload da foto para Nextcloud
2. Gerar novo link público (1-7 dias validade)
3. Atualizar `BASE_IMAGE_URL` no script

**Código para atualizar:**
```python
# tools/batch_edit_thumbnails.py (linha 17)
BASE_IMAGE_URL = "https://[nova-url-nextcloud]/foto1.jpg"
```

---

## Problema 3: Cores Diferentes do Esperado

### Sintoma
Paleta de cores não segue o padrão (preto, dourado, azul-ciano).

### Causa
- Template modificado incorretamente
- Descrição de cor ambígua

### Solução

✅ **Use sempre a frase exata:**
```
Estilo Geral: A imagem deve ter um clima profissional, tecnológico e de alto impacto,
com uma paleta de cores focada em preto, dourado e o contraste do azul-ciano.
```

❌ **NUNCA modifique esta linha.**

✅ **Cores fixas obrigatórias:**
- **Fundo:** Preto e escuro
- **Texto principal:** Dourado com contorno
- **Barra:** Dourada sólida
- **Data:** Branca
- **Iluminação:** Azul-ciano fria
- **Reflexo óculos:** Laranja vibrante

---

## Problema 4: Layout Invertido (Texto Direita)

### Sintoma
Texto aparece do lado direito e foto do lado esquerdo (layout errado).

### Causa
- Template usando "lado direito" para texto

### Solução

✅ **Use sempre:**
```
Texto e Gráficos (no lado esquerdo da imagem): ...
Foto Principal: ... O meu rosto deve ocupar a metade direita da imagem ...
```

❌ **NUNCA use:**
```
Texto e Gráficos (no lado direito da imagem): ...  ← ERRADO!
```

---

## Problema 5: Timeout ou Processamento Muito Lento

### Sintoma
Script demora mais de 2 minutos ou retorna erro de timeout.

### Causa
- API Kie.ai sobrecarregada
- Muitas tarefas simultâneas
- Conexão de internet lenta

### Solução

✅ **Aumentar timeout:**
```python
# tools/batch_edit_thumbnails.py (linha 131)
max_wait = 300  # Padrão: 300s (5min)
max_wait = 600  # Aumentar para 600s (10min)
```

✅ **Reduzir paralelismo:**
```python
# tools/batch_edit_thumbnails.py (linha 213)
with ThreadPoolExecutor(max_workers=len(tasks)):  # Padrão: 5 workers
with ThreadPoolExecutor(max_workers=3):           # Reduzir para 3 workers
```

✅ **Verificar conexão:**
```bash
ping api.kie.ai
```

### Tempo Esperado

| Thumbnails | Tempo Normal | Timeout |
|-----------|--------------|---------|
| 1 | 20-30s | 300s |
| 3 | 60-90s | 300s |
| 5 | 90-120s | 300s |

---

## Problema 6: Split Lighting Não Aparece

### Sintoma
Iluminação uniforme, sem o efeito dramático de metade sombra/metade luz.

### Causa
- Descrição de iluminação omitida ou modificada

### Solução

✅ **Use sempre a frase completa:**
```
Iluminação: Aplique uma iluminação de estúdio dramática com o estilo 'split lighting'.
Metade do meu rosto deve estar em sombra profunda, enquanto a outra metade é iluminada
por uma luz azul-ciano fria. Se eu estiver usando óculos, adicione um reflexo laranja
vibrante nas lentes.
```

❌ **NUNCA simplifique para:**
```
Iluminação: Boa iluminação  ← ERRADO! Muito vago
```

✅ **Elementos obrigatórios:**
- "split lighting" (termo técnico)
- "metade sombra profunda"
- "luz azul-ciano fria"
- "reflexo laranja nas lentes"

---

## Problema 7: Script Não Executa

### Sintoma
Erro ao rodar `python3 tools/batch_edit_thumbnails.py`

### Possíveis Erros

#### Erro 1: `ModuleNotFoundError: No module named 'requests'`

**Causa:** Biblioteca `requests` não instalada

**Solução:**
```bash
pip3 install requests
```

#### Erro 2: `Permission denied`

**Causa:** Script sem permissão de execução

**Solução:**
```bash
chmod +x tools/batch_edit_thumbnails.py
```

#### Erro 3: `FileNotFoundError: [Errno 2] No such file or directory`

**Causa:** Executando do diretório errado

**Solução:**
```bash
# Ir para raiz do workspace
cd ~/Desktop/ClaudeCode-Workspace

# Executar script
python3 tools/batch_edit_thumbnails.py
```

---

## Problema 8: Nenhuma Thumbnail Gerada (0/5)

### Sintoma
```
❌ Falhas: 5
   ⚠️  [prompt] - Generation failed
```

### Causa Provável
- API key inválida ou expirada
- Foto base inacessível
- Prompt malformado

### Diagnóstico

✅ **1. Verificar API key:**
```python
# tools/batch_edit_thumbnails.py (linha 16)
API_KEY = "fa32b7ea4ff0e9b5acce83abe09d2b06"
```

**Testar API key:**
```bash
curl -H "Authorization: Bearer fa32b7ea4ff0e9b5acce83abe09d2b06" \
     https://api.kie.ai/api/v1/jobs/createTask
```

✅ **2. Verificar foto base:**
```bash
curl -I https://media.loop9.com.br/s/C9WLo3EytYjNKwm/download/foto1.jpg
# Deve retornar: HTTP/1.1 200 OK
```

✅ **3. Testar com prompt simples:**
```python
# Editar script temporariamente para usar prompt minimalista
test_prompts = [
    "Crie uma thumbnail simples com minha foto e texto TESTE"
]
```

Se funcionar com prompt simples → problema no template complexo.

---

## Problema 9: Thumbnails Muito Diferentes Entre Si

### Sintoma
5 thumbnails geradas, mas com estilos visuais muito diferentes (cores, layout, fontes variadas).

### Causa
- Variáveis modificando partes fixas do template
- Inconsistência nos prompts

### Solução

✅ **Mantenha estrutura idêntica:**

**Copie o template base 5 vezes** e modifique APENAS:
- `{{TEMA}}`
- `{{TÍTULO}}`
- `{{SUBTÍTULO}}`
- `{{DATA}}`
- `{{SELO}}`

**NUNCA modifique:**
- Layout (texto esquerda / foto direita)
- Iluminação (split lighting)
- Paleta de cores (preto, dourado, azul-ciano)
- Fundo (preto escuro)
- Estilo geral

✅ **Checklist antes de gerar:**
- [ ] Todas as 5 variações têm mesma estrutura de frases?
- [ ] Só os valores entre aspas mudam?
- [ ] Iluminação idêntica em todas?
- [ ] Paleta de cores idêntica em todas?

---

## Problema 10: Texto Cortado ou Fora da Área

### Sintoma
Título ou subtítulo aparecem cortados nas bordas da thumbnail.

### Causa
- Texto muito longo para o espaço disponível
- IA não conseguiu ajustar o tamanho da fonte

### Solução

✅ **Reduza o texto:**

**Antes (cortado):**
```
Título: "PRODUTIVIDADE MÁXIMA GARANTIDA"  ← 30 caracteres
```

**Depois (cabe):**
```
Título: "PRODUTIVIDADE 10X"  ← 16 caracteres
```

✅ **Use quebras estratégicas:**

Se precisar de texto longo, divida entre título e subtítulo:

**Ao invés de:**
```
Título: "MARKETING DIGITAL COMPLETO"
Subtítulo: "VENDA MAIS"
```

**Use:**
```
Título: "MARKETING DIGITAL"
Subtítulo: "VENDAS COMPLETAS"
```

---

## 🆘 Suporte Adicional

### Se nenhuma solução acima funcionou:

1. **Verificar logs do script:**
   ```bash
   python3 tools/batch_edit_thumbnails.py 2>&1 | tee debug.log
   ```

2. **Testar com 1 thumbnail apenas:**
   - Editar script para gerar só 1 variação
   - Isolar o problema

3. **Validar foto base manualmente:**
   - Baixar foto da URL
   - Fazer upload novamente para Nextcloud
   - Gerar novo link público

4. **Consultar status da API:**
   ```bash
   curl https://api.kie.ai/health
   ```

5. **Ver outros exemplos:**
   - Consultar `EXAMPLES.md` para casos reais funcionais
   - Copiar um exemplo completo e testar

---

## 📊 Logs de Erro Comuns

### Erro: `HTTPError: 401 Unauthorized`

**Causa:** API key inválida

**Solução:**
```python
# Atualizar API key em tools/batch_edit_thumbnails.py
API_KEY = "[sua-nova-key]"
```

### Erro: `HTTPError: 400 Bad Request`

**Causa:** Payload malformado (prompt com caracteres especiais)

**Solução:**
- Remover emojis do prompt
- Escapar aspas duplas: `"` → `\"`
- Verificar JSON válido

### Erro: `ConnectionError: Max retries exceeded`

**Causa:** API offline ou firewall bloqueando

**Solução:**
```bash
# Verificar conectividade
ping api.kie.ai

# Testar com curl
curl https://api.kie.ai
```

---

## 🔧 Comandos Úteis de Debug

### Ver foto base:
```bash
open https://media.loop9.com.br/s/C9WLo3EytYjNKwm/download/foto1.jpg
```

### Testar API key:
```bash
curl -H "Authorization: Bearer [API_KEY]" \
     -H "Content-Type: application/json" \
     https://api.kie.ai/api/v1/jobs/createTask
```

### Verificar espaço em Downloads:
```bash
df -h ~/Downloads
```

### Listar thumbnails geradas:
```bash
ls -lht ~/Downloads/thumbnail_*.png | head -10
```

---

## ✅ Checklist de Prevenção

Antes de executar a skill:

- [ ] Foto base acessível (testar URL)
- [ ] API key válida
- [ ] Template completo (não faltam seções)
- [ ] Títulos curtos (máx 20 chars)
- [ ] Subtítulos curtos (máx 25 chars)
- [ ] Paleta de cores não modificada
- [ ] Layout correto (texto esquerda, foto direita)
- [ ] Internet estável
- [ ] Espaço em ~/Downloads (mín 10MB)

---

## 📚 Recursos Relacionados

- **SKILL.md** → Workflow completo
- **REFERENCE.md** → Anatomia do template
- **EXAMPLES.md** → 5 casos reais funcionais
- **Script** → `tools/batch_edit_thumbnails.py`
