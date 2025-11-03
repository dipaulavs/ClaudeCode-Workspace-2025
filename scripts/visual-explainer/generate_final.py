#!/usr/bin/env python3
"""Gerador Final - Com Slide de Resumo + CTA"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from generate import ApresentacaoGenerator

roteiro_path = Path("/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/roteiro_claude_code.md")
generator = ApresentacaoGenerator(Path(__file__).parent / "templates")

with open(roteiro_path, "r", encoding="utf-8") as f:
    roteiro = f.read()

data = generator.processar_roteiro_notion(roteiro)

template_path = Path(__file__).parent / "templates" / "notion-interativo.html"
with open(template_path, "r", encoding="utf-8") as f:
    template = f.read()

slides_html = ""

for i, slide in enumerate(data["slides"]):
    if i == 1:  # Slide 2 - Cards clicáveis
        slides_html += f"""
        <div class="slide" data-slide="{i+1}" data-title="{slide['titulo']}">
            <span class="conceito-badge">Slide {i+1}</span>
            <p class="conceito-principal">{slide['conceito']}</p>
            
            <div class="analogia">
                <div class="analogia-label">💡 Analogia</div>
                <div class="analogia-texto">{slide['analogia']}</div>
            </div>

            <div style="margin-top: 2rem;">
                <p style="font-size: 1.3rem; color: #c7c7c7; margin-bottom: 1.5rem;">
                    <strong>5 Ferramentas Principais:</strong> (Clique para detalhes)
                </p>

                <div class="card-clickable">
                    <div class="card-header"><span class="card-icon">👁️</span><span>Read (Leitura)</span></div>
                    <div class="card-preview">Acessa e interpreta arquivos do projeto</div>
                    <div class="card-details">
                        <div class="card-details-content">Permite que Claude veja o conteúdo dos seus arquivos para entender a estrutura e lógica do projeto.</div>
                        <div class="card-example">Você: "Mostra o código de autenticação"<br>Claude: <em>*usa Read para abrir auth.js*</em></div>
                    </div>
                </div>

                <div class="card-clickable">
                    <div class="card-header"><span class="card-icon">✨</span><span>Write (Criação)</span></div>
                    <div class="card-preview">Gera novos arquivos no projeto</div>
                    <div class="card-details">
                        <div class="card-details-content">Cria arquivos completamente novos com conteúdo estruturado.</div>
                        <div class="card-example">Você: "Cria um arquivo de configuração"<br>Claude: <em>*cria config.json com estrutura*</em></div>
                    </div>
                </div>

                <div class="card-clickable">
                    <div class="card-header"><span class="card-icon">✏️</span><span>Edit (Modificação)</span></div>
                    <div class="card-preview">Altera arquivos existentes com precisão</div>
                    <div class="card-details">
                        <div class="card-details-content">Modifica código existente fazendo substituições exatas e controladas.</div>
                        <div class="card-example">Você: "Muda cor primária de azul para verde"<br>Claude: <em>*edita styles.css: #0066ff → #00ff66*</em></div>
                    </div>
                </div>

                <div class="card-clickable">
                    <div class="card-header"><span class="card-icon">⚡</span><span>Bash (Terminal)</span></div>
                    <div class="card-preview">Executa comandos do sistema</div>
                    <div class="card-details">
                        <div class="card-details-content">Roda comandos no terminal - instalação de pacotes, testes, build, etc.</div>
                        <div class="card-example">Você: "Instala React Query"<br>Claude: <em>*executa: npm install @tanstack/react-query*</em></div>
                    </div>
                </div>

                <div class="card-clickable">
                    <div class="card-header"><span class="card-icon">🔍</span><span>Grep (Busca)</span></div>
                    <div class="card-preview">Localiza padrões no código</div>
                    <div class="card-details">
                        <div class="card-details-content">Busca texto e padrões em múltiplos arquivos rapidamente.</div>
                        <div class="card-example">Você: "Onde está definida a função de login?"<br>Claude: <em>*busca e encontra em auth.js:42*</em></div>
                    </div>
                </div>
            </div>
        </div>
        """
    
    elif i == 2:  # Slide 3 - Fluxo com setas
        slides_html += f"""
        <div class="slide" data-slide="{i+1}" data-title="{slide['titulo']}">
            <span class="conceito-badge">Slide {i+1}</span>
            <p class="conceito-principal">{slide['conceito']}</p>
            
            <div class="analogia">
                <div class="analogia-label">💡 Analogia</div>
                <div class="analogia-texto">{slide['analogia']}</div>
            </div>

            <div style="margin-top: 3rem;">
                <div class="flow-step">
                    <span class="flow-step-number">1</span>
                    <div style="display: inline-block; vertical-align: top; width: calc(100% - 4rem);">
                        <div class="flow-step-title">Solicitação</div>
                        <div class="flow-step-content">"Implementa dark mode no site"</div>
                    </div>
                </div>

                <div class="flow-step">
                    <span class="flow-step-number">2</span>
                    <div style="display: inline-block; vertical-align: top; width: calc(100% - 4rem);">
                        <div class="flow-step-title">Análise</div>
                        <div class="flow-step-content">Claude lê arquivos relevantes e entende a estrutura</div>
                    </div>
                </div>

                <div class="flow-step">
                    <span class="flow-step-number">3</span>
                    <div style="display: inline-block; vertical-align: top; width: calc(100% - 4rem);">
                        <div class="flow-step-title">Planejamento</div>
                        <div class="flow-step-content">"Vou criar ThemeProvider.js, modificar App.js e adicionar estilos CSS. Confirma?"</div>
                    </div>
                </div>

                <div class="flow-step">
                    <span class="flow-step-number">4</span>
                    <div style="display: inline-block; vertical-align: top; width: calc(100% - 4rem);">
                        <div class="flow-step-title">Aprovação</div>
                        <div class="flow-step-content">Você valida ou ajusta o plano</div>
                    </div>
                </div>

                <div class="flow-step">
                    <span class="flow-step-number">5</span>
                    <div style="display: inline-block; vertical-align: top; width: calc(100% - 4rem);">
                        <div class="flow-step-title">Implementação</div>
                        <div class="flow-step-content">Claude executa todas as mudanças</div>
                    </div>
                </div>

                <div class="flow-step">
                    <span class="flow-step-number">6</span>
                    <div style="display: inline-block; vertical-align: top; width: calc(100% - 4rem);">
                        <div class="flow-step-title">Validação</div>
                        <div class="flow-step-content">Dark mode funcionando ✓</div>
                    </div>
                </div>
            </div>
        </div>
        """
    
    elif i == 3:  # Slide 4 - Quiz
        slides_html += f"""
        <div class="slide" data-slide="{i+1}" data-title="{slide['titulo']}">
            <span class="conceito-badge">Slide {i+1}</span>
            <p class="conceito-principal">{slide['conceito']}</p>
            
            <div class="analogia">
                <div class="analogia-label">💡 Analogia</div>
                <div class="analogia-texto">{slide['analogia']}</div>
            </div>

            <div style="margin-top: 2rem;">
                <div class="flow-step">
                    <div class="flow-step-content">Você: "Valida essa ideia de aplicativo"</div>
                </div>
                <div class="flow-step">
                    <div class="flow-step-content">Claude detecta contexto: Validação de produto</div>
                </div>
                <div class="flow-step">
                    <div class="flow-step-content">Ativa skill: <strong style="color: #3b82f6;">idea-validator</strong></div>
                </div>
                <div class="flow-step">
                    <div class="flow-step-content">Assume papel: Especialista em análise de mercado</div>
                </div>
                <div class="flow-step">
                    <div class="flow-step-content">Entrega: Análise de viabilidade, saturação, monetização</div>
                </div>
            </div>

            <div class="quiz" style="margin-top: 2rem;">
                <div class="quiz-question">🎯 Teste Rápido: Qual skill usar para criar interfaces?</div>
                <div class="quiz-options">
                    <div class="quiz-option" data-correct="false" data-explanation="idea-validator é para análise de negócio, não design visual.">
                        idea-validator
                    </div>
                    <div class="quiz-option" data-correct="true" data-explanation="Correto! product-designer cria interfaces profissionais.">
                        product-designer
                    </div>
                    <div class="quiz-option" data-correct="false" data-explanation="marketing-writer produz conteúdo textual, não interfaces.">
                        marketing-writer
                    </div>
                </div>
                <div class="quiz-feedback"></div>
            </div>
        </div>
        """
    
    elif i == 7:  # Slide 8 - Resumo Final
        slides_html += f"""
        <div class="slide" data-slide="{i+1}" data-title="{slide['titulo']}">
            <span class="conceito-badge">Resumo Final</span>
            <p class="conceito-principal" style="text-align: center; font-size: 2.2rem; margin-bottom: 2rem;">{slide['conceito']}</p>
            
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; margin: 3rem 0;">
                
                <div style="background: #1a1a1a; border: 2px solid #3b82f6; border-radius: 12px; padding: 2rem; text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
                    <h3 style="color: #3b82f6; font-size: 1.4rem; margin-bottom: 1rem;">O QUE É</h3>
                    <ul style="list-style: none; padding: 0; text-align: left; color: #c7c7c7; font-size: 1.1rem; line-height: 1.8;">
                        <li>→ Assistente IA com acesso direto ao sistema</li>
                        <li>→ Executa modificações reais</li>
                        <li>→ 5 ferramentas principais</li>
                    </ul>
                </div>

                <div style="background: #1a1a1a; border: 2px solid #8b5cf6; border-radius: 12px; padding: 2rem; text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
                    <h3 style="color: #8b5cf6; font-size: 1.4rem; margin-bottom: 1rem;">COMO FUNCIONA</h3>
                    <ul style="list-style: none; padding: 0; text-align: left; color: #c7c7c7; font-size: 1.1rem; line-height: 1.8;">
                        <li>→ Fluxo de 6 passos</li>
                        <li>→ Você mantém controle total</li>
                        <li>→ Skills especializadas</li>
                    </ul>
                </div>

                <div style="background: #1a1a1a; border: 2px solid #10b981; border-radius: 12px; padding: 2rem; text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🚀</div>
                    <h3 style="color: #10b981; font-size: 1.4rem; margin-bottom: 1rem;">POR QUE USAR</h3>
                    <ul style="list-style: none; padding: 0; text-align: left; color: #c7c7c7; font-size: 1.1rem; line-height: 1.8;">
                        <li>→ Velocidade 10x</li>
                        <li>→ Código consistente</li>
                        <li>→ Aprendizado contínuo</li>
                    </ul>
                </div>

            </div>

            <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border: 2px solid #3b82f6; border-radius: 12px; padding: 2rem; margin-top: 2rem;">
                <h3 style="color: #3b82f6; font-size: 1.5rem; margin-bottom: 1.5rem; text-align: center;">PRÓXIMOS PASSOS</h3>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; color: #c7c7c7; font-size: 1.1rem;">
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">✓</div>
                        Experimente com tarefa simples
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">✓</div>
                        Configure CLAUDE.md
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">✓</div>
                        Explore skills disponíveis
                    </div>
                </div>
            </div>

            <div style="text-align: center; margin-top: 3rem; font-size: 1.5rem; color: #3b82f6; font-weight: 600;">
                💡 Você é o arquiteto, Claude é o executor.
            </div>
        </div>
        """
    
    elif i == 8:  # Slide 9 - CTA (Obrigado)
        slides_html += f"""
        <div class="slide" data-slide="{i+1}" data-title="Obrigado!">
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 80vh; text-align: center;">
                
                <h1 style="font-size: 4rem; font-weight: 800; color: #3b82f6; margin-bottom: 2rem;">
                    Obrigado! 🚀
                </h1>

                <p style="font-size: 1.8rem; color: #c7c7c7; margin-bottom: 4rem;">
                    Gostou do conteúdo? Apoie o canal!
                </p>

                <div style="display: grid; gap: 2.5rem; max-width: 800px; width: 100%;">
                    
                    <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border: 2px solid #3b82f6; border-radius: 16px; padding: 2rem; transition: all 300ms ease;">
                        <div style="font-size: 4rem; margin-bottom: 1rem;">👍</div>
                        <h3 style="color: #3b82f6; font-size: 1.8rem; margin-bottom: 0.5rem; font-weight: 700;">DEIXE SEU LIKE</h3>
                        <p style="color: #a0a0a0; font-size: 1.2rem;">Se o vídeo foi útil para você</p>
                    </div>

                    <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border: 2px solid #ef4444; border-radius: 16px; padding: 2rem; transition: all 300ms ease;">
                        <div style="font-size: 4rem; margin-bottom: 1rem;">🔔</div>
                        <h3 style="color: #ef4444; font-size: 1.8rem; margin-bottom: 0.5rem; font-weight: 700;">INSCREVA-SE NO CANAL</h3>
                        <p style="color: #a0a0a0; font-size: 1.2rem;">Para mais conteúdo sobre IA e programação</p>
                    </div>

                    <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border: 2px solid #8b5cf6; border-radius: 16px; padding: 2rem; transition: all 300ms ease;">
                        <div style="font-size: 4rem; margin-bottom: 1rem;">📱</div>
                        <h3 style="color: #8b5cf6; font-size: 1.8rem; margin-bottom: 0.5rem; font-weight: 700;">SIGA NO INSTAGRAM</h3>
                        <p style="color: #a0a0a0; font-size: 1.4rem; font-weight: 600; margin-top: 0.75rem;">@eusoupromptus</p>
                        <p style="color: #94a3b8; font-size: 1.1rem; margin-top: 0.5rem;">Bastidores, dicas rápidas e novidades</p>
                    </div>

                </div>

                <p style="font-size: 2rem; color: #3b82f6; margin-top: 4rem; font-weight: 600;">
                    Até o próximo vídeo! 🎬
                </p>

            </div>
        </div>
        """
    
    else:
        conceito_html = f'<p class="conceito-principal">{slide["conceito"]}</p>' if slide["conceito"] else ""
        explicacao_html = f'<p class="explicacao">{slide["explicacao"]}</p>' if slide["explicacao"] else ""
        
        analogia_html = ""
        if slide["analogia"]:
            analogia_html = f"""
            <div class="analogia">
                <div class="analogia-label">💡 Analogia</div>
                <div class="analogia-texto">{slide["analogia"]}</div>
            </div>
            """
        
        pontos_html = ""
        if slide["pontos"]:
            pontos_html = '<ul class="pontos-chave">'
            for ponto in slide["pontos"]:
                pontos_html += f"<li>{ponto}</li>"
            pontos_html += "</ul>"
        
        slides_html += f"""
        <div class="slide" data-slide="{i+1}" data-title="{slide['titulo']}">
            <span class="conceito-badge">Slide {i+1}</span>
            {conceito_html}
            {explicacao_html}
            {analogia_html}
            {pontos_html}
        </div>
        """

html = template.replace("{{TITULO}}", data["titulo"])
html = html.replace("{{SLIDES}}", slides_html)

output_path = Path("/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/apresentacao_claude_code_FINAL.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\n✅ Apresentação COMPLETA criada: {output_path}")
print(f"\n✨ Características:")
print(f"  ✅ 9 slides totais")
print(f"  ✅ Slide 8: Resumo visual em 3 colunas")
print(f"  ✅ Slide 9: CTA (Like + Inscrição + Instagram @eusoupromptus)")
print(f"  ✅ Sem animações (performance otimizada)")
print(f"  ✅ Sem timer")
print(f"  ✅ Cards clicáveis (Slide 2)")
print(f"  ✅ Fluxo visual (Slide 3)")
print(f"  ✅ Quiz interativo (Slide 4)")
print(f"\n🎬 Pressione F para fullscreen! 🚀\n")
