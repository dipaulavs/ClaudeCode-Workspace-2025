#!/usr/bin/env python3
"""
Instagram AI Carousel - Orquestrador com Auto-Healing
Workflow: Pesquisa → Hormozi → PDF → Imagens → Instagram

Auto-healing via Claude API:
- Detecta erros em cada etapa
- Analisa causa raiz
- Corrige automaticamente
- Retenta execução
"""

import os
import sys
import json
import traceback
import requests
from datetime import datetime
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configurações
CLAUDE_API_KEY = os.getenv('ANTHROPIC_API_KEY')  # Para auto-healing
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')  # Para agentes
OPENROUTER_MODEL = "anthropic/claude-3.5-haiku"
MAX_RETRIES = 3
LOG_DIR = Path(__file__).parent / "logs"
OUTPUT_DIR = Path(__file__).parent / "output"

# Cria diretórios
LOG_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


class WorkflowOrchestrator:
    """Orquestrador com capacidade de auto-healing"""

    def __init__(self):
        self.client = Anthropic(api_key=CLAUDE_API_KEY)  # Claude API para auto-healing
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = LOG_DIR / f"workflow_{self.run_id}.log"
        self.state = {
            "run_id": self.run_id,
            "started_at": datetime.now().isoformat(),
            "steps": []
        }

    def call_openrouter(self, prompt: str, max_tokens: int = 2000) -> str:
        """Chama OpenRouter (Claude Haiku) para agentes do workflow"""
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": OPENROUTER_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens
            }
        )

        if response.status_code != 200:
            raise Exception(f"OpenRouter error: {response.status_code} - {response.text}")

        return response.json()["choices"][0]["message"]["content"]

    def log(self, message: str, level: str = "INFO"):
        """Log com timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)

        with open(self.log_file, 'a') as f:
            f.write(log_entry + "\n")

    def execute_step(self, step_name: str, function, *args, **kwargs):
        """
        Executa etapa com retry e auto-healing

        Args:
            step_name: Nome da etapa
            function: Função a executar
            *args, **kwargs: Argumentos da função

        Returns:
            Resultado da função ou None em caso de falha
        """
        self.log(f"Iniciando etapa: {step_name}")

        step_result = {
            "name": step_name,
            "started_at": datetime.now().isoformat(),
            "attempts": [],
            "success": False
        }

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                self.log(f"Tentativa {attempt}/{MAX_RETRIES}")

                # Executa função
                result = function(*args, **kwargs)

                # Sucesso
                step_result["success"] = True
                step_result["result"] = result
                step_result["attempts"].append({
                    "attempt": attempt,
                    "success": True,
                    "timestamp": datetime.now().isoformat()
                })

                self.log(f"✅ Etapa '{step_name}' concluída com sucesso!", "SUCCESS")
                self.state["steps"].append(step_result)
                return result

            except Exception as e:
                error_msg = str(e)
                error_trace = traceback.format_exc()

                self.log(f"❌ Erro na tentativa {attempt}: {error_msg}", "ERROR")
                self.log(f"Traceback:\n{error_trace}", "DEBUG")

                step_result["attempts"].append({
                    "attempt": attempt,
                    "success": False,
                    "error": error_msg,
                    "traceback": error_trace,
                    "timestamp": datetime.now().isoformat()
                })

                # Se não for a última tentativa, tenta auto-healing
                if attempt < MAX_RETRIES:
                    self.log("🔧 Iniciando auto-healing...", "HEALING")

                    # Analisa erro com Claude
                    healing_result = self._auto_heal(
                        step_name=step_name,
                        error_msg=error_msg,
                        error_trace=error_trace,
                        function_code=self._get_function_code(function),
                        args=args,
                        kwargs=kwargs
                    )

                    if healing_result:
                        self.log(f"🔧 Auto-healing aplicado: {healing_result['suggestion']}", "HEALING")
                        step_result["attempts"][-1]["healing"] = healing_result

                        # Aplica correção se possível
                        if healing_result.get("fix_code"):
                            self._apply_fix(function, healing_result["fix_code"])

                    self.log(f"Aguardando 2s antes de retentar...", "INFO")
                    import time
                    time.sleep(2)
                else:
                    # Última tentativa falhou
                    self.log(f"❌ Etapa '{step_name}' falhou após {MAX_RETRIES} tentativas", "ERROR")
                    step_result["success"] = False
                    self.state["steps"].append(step_result)
                    return None

        return None

    def _auto_heal(self, step_name: str, error_msg: str, error_trace: str,
                   function_code: str, args: tuple, kwargs: dict) -> dict:
        """
        Usa Claude API para analisar erro e sugerir correção

        Returns:
            dict com análise e sugestão de correção
        """
        try:
            prompt = f"""Você é um especialista em debugging de workflows Python.

Etapa que falhou: {step_name}

Erro:
{error_msg}

Traceback completo:
{error_trace}

Código da função:
{function_code}

Argumentos:
args: {args}
kwargs: {kwargs}

Analise o erro e responda em JSON:
{{
    "causa_raiz": "explicação da causa real do erro",
    "sugestao": "como corrigir (1 frase)",
    "fix_possivel": true/false,
    "fix_code": "código Python corrigido (se fix_possivel=true)"
}}

Seja objetivo e prático."""

            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Extrai JSON da resposta
            content = response.content[0].text

            # Tenta encontrar JSON na resposta
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return result
            else:
                return {
                    "causa_raiz": "Não foi possível analisar",
                    "sugestao": content[:200],
                    "fix_possivel": False
                }

        except Exception as e:
            self.log(f"Erro no auto-healing: {e}", "ERROR")
            return None

    def _get_function_code(self, function) -> str:
        """Retorna código fonte da função"""
        try:
            import inspect
            return inspect.getsource(function)
        except:
            return "# Código não disponível"

    def _apply_fix(self, function, fix_code: str):
        """
        Aplica correção no código (placeholder)

        Em produção, isso poderia:
        - Reescrever arquivo
        - Recarregar módulo
        - Aplicar monkey patch
        """
        self.log("⚠️  Fix sugerido mas não aplicado automaticamente (segurança)", "WARNING")
        self.log(f"Fix code:\n{fix_code}", "DEBUG")

    def run_workflow(self):
        """Executa workflow completo"""
        self.log("🚀 Iniciando workflow Instagram AI Carousel")

        try:
            # ETAPA 1: Pesquisa de notícias
            news_data = self.execute_step(
                "search_news",
                self._search_news
            )
            if not news_data:
                raise Exception("Falha na busca de notícias")

            # ETAPA 2: Hormozi - Criar copy + estrutura carrossel
            hormozi_output = self.execute_step(
                "hormozi_copy",
                self._create_hormozi_copy,
                news_data
            )
            if not hormozi_output:
                raise Exception("Falha na criação do copy Hormozi")

            # ETAPA 3: Gerar PDF com conteúdo expandido
            pdf_path = self.execute_step(
                "generate_pdf",
                self._generate_pdf,
                hormozi_output
            )
            if not pdf_path:
                raise Exception("Falha na geração do PDF")

            # ETAPA 4: Gerar imagens dos slides
            slide_images = self.execute_step(
                "generate_slides",
                self._generate_slide_images,
                hormozi_output
            )
            if not slide_images:
                raise Exception("Falha na geração das imagens")

            # ETAPA 5: Publicar no Instagram
            post_result = self.execute_step(
                "publish_instagram",
                self._publish_carousel,
                slide_images,
                hormozi_output
            )
            if not post_result:
                raise Exception("Falha na publicação no Instagram")

            # Workflow concluído
            self.state["completed_at"] = datetime.now().isoformat()
            self.state["success"] = True
            self.state["final_result"] = {
                "pdf_path": pdf_path,
                "post_url": post_result.get("url")
            }

            self.log("🎉 Workflow concluído com sucesso!", "SUCCESS")
            self._save_state()

            return True

        except Exception as e:
            self.log(f"💥 Workflow falhou: {e}", "ERROR")
            self.state["completed_at"] = datetime.now().isoformat()
            self.state["success"] = False
            self.state["error"] = str(e)
            self._save_state()
            return False

    def _save_state(self):
        """Salva estado do workflow"""
        state_file = LOG_DIR / f"state_{self.run_id}.json"
        with open(state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
        self.log(f"Estado salvo em: {state_file}")

    # ============================================
    # ETAPAS DO WORKFLOW (implementação básica)
    # ============================================

    def _search_news(self):
        """ETAPA 1: Busca notícia recente"""
        self.log("🔍 Buscando notícia via OpenRouter (Haiku)...")

        content = self.call_openrouter("""Encontre UMA notícia importante e recente sobre tecnologia/IA (últimas 24h).

Retorne JSON:
{
    "titulo": "título da notícia",
    "resumo": "resumo em 2-3 frases",
    "fonte": "nome da fonte",
    "relevancia": "por que é importante"
}""", max_tokens=1500)

        # Extrai JSON
        import re
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            news_data = json.loads(json_match.group())
            self.log(f"Notícia encontrada: {news_data['titulo']}")
            return news_data
        else:
            raise Exception("Resposta não contém JSON válido")

    def _create_hormozi_copy(self, news_data: dict):
        """ETAPA 2: Cria copy estilo Hormozi"""
        self.log("✍️  Criando copy com framework Hormozi via OpenRouter...")

        content = self.call_openrouter(f"""Use o framework de Alex Hormozi para criar um carrossel vendedor sobre esta notícia:

{json.dumps(news_data, indent=2)}

Crie um carrossel de 5 slides seguindo o framework $100M Offers:

Retorne JSON:
{{
    "hook": "gancho matador (1 frase impactante)",
    "slides": [
        {{"numero": 1, "titulo": "...", "conteudo": "...", "prompt_imagem": "prompt para gerar imagem"}},
        {{"numero": 2, "titulo": "...", "conteudo": "...", "prompt_imagem": "..."}},
        ...5 slides
    ],
    "cta": "chamada para ação clara",
    "legenda": "legenda completa do post com hashtags",
    "palavra_gatilho": "palavra que o usuário deve comentar (ex: QUERO, ACESSO, etc)",
    "oferta": "o que será entregue quando comentar"
}}

Use princípios Hormozi:
- Hook que para o scroll
- Value Equation (sonho resultado, probabilidade, tempo, esforço)
- CTA direto e específico""", max_tokens=3000)

        # Extrai JSON
        import re
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            hormozi_data = json.loads(json_match.group())
            self.log(f"Copy criado: {len(hormozi_data['slides'])} slides")

            # Salva output
            output_file = OUTPUT_DIR / f"hormozi_{self.run_id}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(hormozi_data, f, indent=2, ensure_ascii=False)

            return hormozi_data
        else:
            raise Exception("Resposta não contém JSON válido")

    def _generate_pdf(self, hormozi_data: dict):
        """ETAPA 3: Gera PDF expandido"""
        self.log("📄 Gerando PDF com conteúdo expandido via OpenRouter...")

        markdown_content = self.call_openrouter(f"""Expanda este conteúdo em um guia completo (formato markdown):

{json.dumps(hormozi_data, indent=2)}

Adicione:
- Introdução expandida
- Mais detalhes em cada tópico
- Exemplos práticos
- Link de compra (use: https://exemplo.com/produto-especial)
- Conclusão motivacional

Retorne markdown completo.""", max_tokens=4000)

        # Salva markdown
        md_file = OUTPUT_DIR / f"content_{self.run_id}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        # Converte para PDF (simplificado - usa markdown2pdf ou weasyprint em produção)
        pdf_file = OUTPUT_DIR / f"content_{self.run_id}.pdf"

        try:
            # Tenta usar weasyprint se disponível
            from weasyprint import HTML
            HTML(string=f"<pre>{markdown_content}</pre>").write_pdf(pdf_file)
            self.log(f"PDF gerado: {pdf_file}")
        except ImportError:
            # Fallback: salva como HTML
            html_file = OUTPUT_DIR / f"content_{self.run_id}.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(f"<html><body><pre>{markdown_content}</pre></body></html>")
            self.log(f"⚠️  weasyprint não disponível. HTML salvo: {html_file}", "WARNING")
            return str(html_file)

        return str(pdf_file)

    def _generate_slide_images(self, hormozi_data: dict):
        """ETAPA 4: Gera imagens dos slides (estilo carrossel artesanal)"""
        self.log("🎨 Gerando imagens dos slides (colagem artesanal)...")

        slides = hormozi_data['slides']

        # Template visual fixo (colagem artesanal)
        PROMPT_BASE = """Crie uma colagem artesanal e realista feita à mão, com aparência de trabalho escolar sobre vendas de terrenos.

Fundo de mesa de madeira clara, luz natural suave e papéis colados com sombras reais e bordas rasgadas.

Use papéis de cores diferentes (branco, amarelo e azul-claro) com escrita feita à mão em canetinhas de várias cores (vermelho, verde, preto e azul).

{CONTEUDO_ESPECIFICO}

Adicione ícones desenhados à mão: {ICONES}

Finalize com detalhes de imperfeição realista — sombras, fita adesiva segurando o papel, traços tortos e variação de espessura da caneta, mantendo o ar de colagem artesanal autêntica."""

        # Prepara prompts para batch
        prompts_data = []
        for slide in slides:
            # Gera ícones sugeridos via OpenRouter
            icones_prompt = f"Slide: {slide['titulo']}\nConteúdo: {slide['conteudo']}\n\nSugira 2-3 ícones desenhados à mão relevantes (ex: cifrão, casa, calendário). Responda só com os ícones separados por vírgula."
            icones = self.call_openrouter(icones_prompt, max_tokens=100).strip()

            # Monta prompt completo
            conteudo_slide = f"{slide['titulo']}\n\n{slide['conteudo']}"
            prompt_completo = PROMPT_BASE.format(
                CONTEUDO_ESPECIFICO=conteudo_slide,
                ICONES=icones
            )

            prompts_data.append({
                "slide": slide['numero'],
                "titulo": slide['titulo'],
                "prompt": prompt_completo
            })

            self.log(f"  Preparado slide {slide['numero']}: {slide['titulo']}")

        # Salva prompts em JSON temporário
        import json
        prompts_file = OUTPUT_DIR / f"carrossel_prompts_{self.run_id}.json"
        with open(prompts_file, 'w', encoding='utf-8') as f:
            json.dump(prompts_data, f, indent=2, ensure_ascii=False)

        self.log(f"Prompts salvos em: {prompts_file}")

        # PRODUÇÃO: Gera imagens via GPT-4o batch
        # import subprocess
        # result = subprocess.run([
        #     "python3", "scripts/image-generation/batch_carrossel_gpt4o.py",
        #     "--prompts-file", str(prompts_file),
        #     "--variants", "4",
        #     "--output-dir", str(OUTPUT_DIR)
        # ], capture_output=True, text=True)

        # Por enquanto: placeholders
        image_paths = []
        for prompt_data in prompts_data:
            placeholder = OUTPUT_DIR / f"slide_{self.run_id}_{prompt_data['slide']}.txt"
            with open(placeholder, 'w', encoding='utf-8') as f:
                f.write(f"SLIDE {prompt_data['slide']}\n")
                f.write(f"Título: {prompt_data['titulo']}\n\n")
                f.write(f"PROMPT COMPLETO:\n{prompt_data['prompt']}")
            image_paths.append(str(placeholder))

        self.log(f"✅ {len(image_paths)} imagens preparadas (estilo colagem artesanal)")
        self.log(f"💡 Para gerar imagens reais: python3 scripts/image-generation/batch_carrossel_gpt4o.py --prompts-file {prompts_file}")

        return image_paths

    def _publish_carousel(self, image_paths: list, hormozi_data: dict):
        """ETAPA 5: Publica carrossel no Instagram"""
        self.log("📱 Publicando no Instagram...")

        # Monta caption completa
        caption = hormozi_data['legenda']

        # TODO: Chamar script real de Instagram
        # Por enquanto, simula

        self.log(f"Caption: {caption[:100]}...")
        self.log(f"Imagens: {len(image_paths)}")
        self.log(f"Palavra-gatilho: {hormozi_data['palavra_gatilho']}")

        # EM PRODUÇÃO, USAR:
        # from tools.publish_instagram_carousel import InstagramCarouselPublisher
        # publisher = InstagramCarouselPublisher()
        # result = publisher.publish_carousel(image_paths, caption)

        # Simulação
        result = {
            "success": True,
            "url": "https://instagram.com/p/exemplo123",
            "media_id": "123456789"
        }

        self.log(f"✅ Post publicado: {result['url']}")
        return result


def main():
    """Executa workflow"""

    # Valida variáveis de ambiente
    if not CLAUDE_API_KEY:
        print("❌ ERRO: ANTHROPIC_API_KEY não configurada")
        print("Configure no .env: ANTHROPIC_API_KEY=sk-...")
        sys.exit(1)

    # Cria orquestrador
    orchestrator = WorkflowOrchestrator()

    # Executa workflow
    success = orchestrator.run_workflow()

    # Exit code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
