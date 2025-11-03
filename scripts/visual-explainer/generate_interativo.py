#!/usr/bin/env python3
"""
Gerador de Apresentações INTERATIVAS
Usa o template notion-interativo.html com todos os elementos clicáveis
"""

import sys
from pathlib import Path

# Importar do generate.py original
sys.path.insert(0, str(Path(__file__).parent))
from generate import ApresentacaoGenerator

roteiro_path = Path("/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/roteiro_claude_code.md")

# Criar gerador
generator = ApresentacaoGenerator(Path(__file__).parent / "templates")

# Processar roteiro
with open(roteiro_path, "r", encoding="utf-8") as f:
    roteiro = f.read()

data = generator.processar_roteiro_notion(roteiro)

# Carregar template INTERATIVO
template_path = Path(__file__).parent / "templates" / "notion-interativo.html"
with open(template_path, "r", encoding="utf-8") as f:
    template = f.read()

# Gerar slides INTERATIVOS
slides_html = ""

for i, slide in enumerate(data["slides"]):
    # Slide 2 - Cards clicáveis para as ferramentas
    if i == 1:  # Slide 2 (As "Mãos" do Claude)
        slides_html += f"""
        <div class="slide" data-slide="{i+1}" data-title="{slide['titulo']}">
            <span class="conceito-badge animate-in">Slide {i+1}</span>
            <p class="conceito-principal animate-in">{slide['conceito']}</p>
            
            <div class="analogia animate-in">
                <div class="analogia-label">💡 Analogia</div>
                <div class="analogia-texto">{slide['analogia']}</div>
            </div>

            <div class="animate-in" style="margin-top: 2rem;">
                <p style="font-size: 1.3rem; color: #c7c7c7; margin-bottom: 1.5rem;">
                    <strong>5 Ferramentas Principais:</strong> (Clique para ver exemplos)
                </p>

                <div class="card-clickable">
                    <div class="card-header">
                        <span class="card-icon">👁️</span>
                        <span>Read (Olhos)</span>
                    </div>
                    <div class="card-preview">Lê arquivos</div>
                    <div class="card-details">
                        <div class="card-details-content">
                            Permite que Claude veja o conteúdo dos seus arquivos. É como dar olhos para ele poder entender o que já existe no seu projeto.
                        </div>
                        <div class="card-example">
                            Você: "Me mostra o código do login"<br>
                            Claude: <em>*usa Read para abrir login.js*</em>
                        </div>
                    </div>
                </div>

                <div class="card-clickable">
                    <div class="card-header">
                        <span class="card-icon">✨</span>
                        <span>Write (Criar)</span>
                    </div>
                    <div class="card-preview">Cria arquivos novos</div>
                    <div class="card-details">
                        <div class="card-details-content">
                            Cria arquivos completamente novos no seu projeto. Perfeito para adicionar novas funcionalidades.
                        </div>
                        <div class="card-example">
                            Você: "Cria um arquivo config.json"<br>
                            Claude: <em>*cria o arquivo com conteúdo*</em>
                        </div>
                    </div>
                </div>

                <div class="card-clickable">
                    <div class="card-header">
                        <span class="card-icon">✏️</span>
                        <span>Edit (Editar)</span>
                    </div>
                    <div class="card-preview">Muda arquivos existentes</div>
                    <div class="card-details">
                        <div class="card-details-content">
                            Modifica arquivos que já existem. Faz substituições exatas e precisas no código.
                        </div>
                        <div class="card-example">
                            Você: "Muda cor do botão de azul pra verde"<br>
                            Claude: <em>*edita styles.css: blue → green*</em>
                        </div>
                    </div>
                </div>

                <div class="card-clickable">
                    <div class="card-header">
                        <span class="card-icon">⚡</span>
                        <span>Bash (Terminal)</span>
                    </div>
                    <div class="card-preview">Roda comandos</div>
                    <div class="card-details">
                        <div class="card-details-content">
                            Executa comandos no terminal. Pode instalar bibliotecas, rodar testes, iniciar servidores, etc.
                        </div>
                        <div class="card-example">
                            Você: "Instala essa biblioteca"<br>
                            Claude: <em>*roda: npm install biblioteca*</em>
                        </div>
                    </div>
                </div>

                <div class="card-clickable">
                    <div class="card-header">
                        <span class="card-icon">🔍</span>
                        <span>Grep (Buscar)</span>
                    </div>
                    <div class="card-preview">Procura coisas no código</div>
                    <div class="card-details">
                        <div class="card-details-content">
                            Busca padrões e texto em múltiplos arquivos. Muito útil para encontrar onde algo está definido.
                        </div>
                        <div class="card-example">
                            Você: "Onde está a função de login?"<br>
                            Claude: <em>*busca e encontra em auth.js:42*</em>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
    
    # Slide 3 - Fluxo com setas
    elif i == 2:  # Slide 3 (Como Funciona)
        slides_html += f"""
        <div class="slide" data-slide="{i+1}" data-title="{slide['titulo']}">
            <span class="conceito-badge animate-in">Slide {i+1}</span>
            <p class="conceito-principal animate-in">{slide['conceito']}</p>
            
            <div class="analogia animate-in">
                <div class="analogia-label">💡 Analogia</div>
                <div class="analogia-texto">{slide['analogia']}</div>
            </div>

            <div style="margin-top: 3rem;">
                <div class="flow-step animate-in">
                    <span class="flow-step-number">1</span>
                    <div style="display: inline-block; vertical-align: top; width: calc(100% - 4rem);">
                        <div class="flow-step-title">Você fala</div>
                        <div class="flow-step-content">"Adiciona dark mode no meu site"</div>
                    </div>
                </div>

                <div class="flow-step animate-in">
                    <span class="flow-step-number">2</span>
                    <div style="display: inline-block; vertical-align: top; width: calc(100% - 4rem);">
                        <div class="flow-step-title">Claude investiga</div>
                        <div class="flow-step-content">Lê seus arquivos → Entende como funciona</div>
                    </div>
                </div>

                <div class="flow-step animate-in">
                    <span class="flow-step-number">3</span>
                    <div style="display: inline-block; vertical-align: top; width: calc(100% - 4rem);">
                        <div class="flow-step-title">Claude mostra o plano</div>
                        <div class="flow-step-content">"Vou criar 3 arquivos e mudar 2 arquivos. Tá ok?"</div>
                    </div>
                </div>

                <div class="flow-step animate-in">
                    <span class="flow-step-number">4</span>
                    <div style="display: inline-block; vertical-align: top; width: calc(100% - 4rem);">
                        <div class="flow-step-title">Você confirma</div>
                        <div class="flow-step-content">"Sim, pode fazer"</div>
                    </div>
                </div>

                <div class="flow-step animate-in">
                    <span class="flow-step-number">5</span>
                    <div style="display: inline-block; vertical-align: top; width: calc(100% - 4rem);">
                        <div class="flow-step-title">Claude executa</div>
                        <div class="flow-step-content">Cria arquivos → Edita código → Testa</div>
                    </div>
                </div>

                <div class="flow-step animate-in">
                    <span class="flow-step-number">6</span>
                    <div style="display: inline-block; vertical-align: top; width: calc(100% - 4rem);">
                        <div class="flow-step-title">Pronto!</div>
                        <div class="flow-step-content">Dark mode funcionando ✓</div>
                    </div>
                </div>
            </div>
        </div>
        """
    
    # Slide 4 - Com quiz
    elif i == 3:  # Slide 4 (Skills)
        slides_html += f"""
        <div class="slide" data-slide="{i+1}" data-title="{slide['titulo']}">
            <span class="conceito-badge animate-in">Slide {i+1}</span>
            <p class="conceito-principal animate-in">{slide['conceito']}</p>
            
            <div class="analogia animate-in">
                <div class="analogia-label">💡 Analogia</div>
                <div class="analogia-texto">{slide['analogia']}</div>
            </div>

            <div class="animate-in" style="margin-top: 2rem;">
                <div class="flow-step">
                    <div class="flow-step-content">Você diz: "Valida essa ideia de app"</div>
                </div>
                <div class="flow-step">
                    <div class="flow-step-content">Claude pensa: "Hmm, ele quer validar ideia..."</div>
                </div>
                <div class="flow-step">
                    <div class="flow-step-content">Claude veste chapéu: <strong style="color: #3b82f6;">idea-validator</strong> (skill ativa!)</div>
                </div>
                <div class="flow-step">
                    <div class="flow-step-content">Claude vira: Especialista em validação de ideias</div>
                </div>
                <div class="flow-step">
                    <div class="flow-step-content">Te dá: Análise profissional (mercado, viabilidade, etc)</div>
                </div>
            </div>

            <div class="quiz animate-in" style="margin-top: 2rem;">
                <div class="quiz-question">🎯 Mini-Quiz: Qual skill usar para criar telas bonitas?</div>
                <div class="quiz-options">
                    <div class="quiz-option" data-correct="false" data-explanation="idea-validator é para validar ideias de negócio, não design!">
                        idea-validator
                    </div>
                    <div class="quiz-option" data-correct="true" data-explanation="Exatamente! product-designer cria telas profissionais.">
                        product-designer
                    </div>
                    <div class="quiz-option" data-correct="false" data-explanation="marketing-writer é para textos de venda, não design visual!">
                        marketing-writer
                    </div>
                </div>
                <div class="quiz-feedback"></div>
            </div>
        </div>
        """
    
    # Outros slides - padrão mais simples
    else:
        conceito_html = f'<p class="conceito-principal animate-in">{slide["conceito"]}</p>' if slide["conceito"] else ""
        explicacao_html = f'<p class="explicacao animate-in">{slide["explicacao"]}</p>' if slide["explicacao"] else ""
        
        analogia_html = ""
        if slide["analogia"]:
            analogia_html = f"""
            <div class="analogia animate-in">
                <div class="analogia-label">💡 Analogia</div>
                <div class="analogia-texto">{slide["analogia"]}</div>
            </div>
            """
        
        pontos_html = ""
        if slide["pontos"]:
            pontos_html = '<ul class="pontos-chave animate-in">'
            for ponto in slide["pontos"]:
                pontos_html += f"<li>{ponto}</li>"
            pontos_html += "</ul>"
        
        slides_html += f"""
        <div class="slide" data-slide="{i+1}" data-title="{slide['titulo']}">
            <span class="conceito-badge animate-in">Slide {i+1}</span>
            {conceito_html}
            {explicacao_html}
            {analogia_html}
            {pontos_html}
        </div>
        """

# Substituir no template
html = template.replace("{{TITULO}}", data["titulo"])
html = html.replace("{{SLIDES}}", slides_html)

# Salvar
output_path = Path("/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/apresentacao_claude_code_INTERATIVA.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\n✅ Apresentação INTERATIVA criada: {output_path}")
print(f"\n🎮 Features ativadas:")
print(f"  ✅ Cards clicáveis (Slide 2 - ferramentas)")
print(f"  ✅ Fluxo com setas (Slide 3 - passo a passo)")
print(f"  ✅ Mini-quiz (Slide 4 - skills)")
print(f"  ✅ Animações sequenciais (todos os slides)")
print(f"  ✅ Hover effects nos elementos")
print(f"  ✅ Sem notas do apresentador")
print(f"\n🎬 Pressione F para fullscreen e comece a gravar! 🚀\n")
