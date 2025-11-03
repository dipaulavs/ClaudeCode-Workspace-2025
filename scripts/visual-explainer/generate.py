#!/usr/bin/env python3
"""
Visual Explainer - Gerador de Apresentações Interativas

Gera apresentações HTML dark mode interativas para gravação de vídeos educativos.
Escolhe automaticamente entre 3 templates: Notion, Mapa Mental ou Tech Futurista.

Uso:
    python3 generate.py --roteiro roteiro.md
    python3 generate.py --roteiro roteiro.md --template notion
    python3 generate.py --roteiro roteiro.md --output apresentacao.html
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Literal

TemplateType = Literal["notion", "mapa-mental", "tech-futurista", "auto"]


class ApresentacaoGenerator:
    """Gerador de apresentações HTML interativas"""

    def __init__(self, template_dir: Path):
        self.template_dir = template_dir
        self.templates = {
            "notion": template_dir / "notion.html",
            "mapa-mental": template_dir / "mapa-mental.html",
            "tech-futurista": template_dir / "tech-futurista.html",
        }

    def analisar_conteudo(self, roteiro: str) -> TemplateType:
        """
        Analisa o roteiro e decide qual template usar.

        Lógica:
        - Mapa Mental: se menciona arquitetura, componentes, sistema, relações
        - Tech Futurista: se menciona lançamento, novidade, anúncio, impacto
        - Notion: padrão para explicações estruturadas
        """
        roteiro_lower = roteiro.lower()

        # Keywords para Mapa Mental
        mapa_mental_keywords = [
            "arquitetura",
            "componentes",
            "sistema",
            "relações",
            "conexões",
            "fluxo",
            "diagrama",
        ]

        # Keywords para Tech Futurista
        tech_keywords = [
            "lançamento",
            "lançado",
            "novidade",
            "anúncio",
            "impacto",
            "revolução",
            "mudança",
            "antes",
            "agora",
        ]

        mapa_score = sum(1 for kw in mapa_mental_keywords if kw in roteiro_lower)
        tech_score = sum(1 for kw in tech_keywords if kw in roteiro_lower)

        if mapa_score >= 2:
            return "mapa-mental"
        elif tech_score >= 2:
            return "tech-futurista"
        else:
            return "notion"

    def processar_roteiro_notion(self, roteiro: str) -> Dict:
        """Processa roteiro para template Notion"""
        slides = []
        titulo_geral = "Apresentação"

        # Extrair título (primeira linha ou # Título)
        lines = roteiro.strip().split("\n")
        if lines and (lines[0].startswith("#") or not lines[0].startswith("##")):
            titulo_geral = lines[0].strip("# ")
            lines = lines[1:]

        # Dividir em slides (## marca novo slide)
        current_slide = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith("## "):
                # Novo slide
                if current_slide:
                    slides.append(current_slide)

                current_slide = {
                    "titulo": line.strip("# "),
                    "conceito": "",
                    "explicacao": "",
                    "analogia": "",
                    "pontos": [],
                    "detalhes": "",
                    "notas": "",
                }

            elif line.startswith("**Conceito:**") or line.startswith("**Conceito Principal:**"):
                if current_slide:
                    current_slide["conceito"] = line.split(":", 1)[1].strip()

            elif line.startswith("**Analogia:**"):
                if current_slide:
                    current_slide["analogia"] = line.split(":", 1)[1].strip()

            elif line.startswith("**Notas:**") or line.startswith("**Notas do Apresentador:**"):
                if current_slide:
                    current_slide["notas"] = line.split(":", 1)[1].strip()

            elif line.startswith("✓") or line.startswith("- "):
                if current_slide:
                    current_slide["pontos"].append(line.lstrip("✓- ").strip())

            elif current_slide and not current_slide["explicacao"]:
                current_slide["explicacao"] = line

        if current_slide:
            slides.append(current_slide)

        return {"titulo": titulo_geral, "slides": slides}

    def gerar_html_notion(self, data: Dict) -> str:
        """Gera HTML usando template Notion"""
        template_path = self.templates["notion"]
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()

        slides_html = ""
        for i, slide in enumerate(data["slides"]):
            conceito_html = (
                f'<p class="conceito-principal">{slide["conceito"]}</p>'
                if slide["conceito"]
                else ""
            )

            explicacao_html = (
                f'<p class="explicacao">{slide["explicacao"]}</p>'
                if slide["explicacao"]
                else ""
            )

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

            notas = slide["notas"] or "Sem notas para este slide."

            slides_html += f"""
            <div class="slide" data-slide="{i+1}" data-title="{slide['titulo']}" data-notas="{notas}">
                <span class="conceito-badge">Slide {i+1}</span>
                {conceito_html}
                {explicacao_html}
                {analogia_html}
                {pontos_html}
            </div>
            """

        html = template.replace("{{TITULO}}", data["titulo"])
        html = html.replace("{{SLIDES}}", slides_html)
        html = html.replace("{{NOTAS_INICIAL}}", data["slides"][0]["notas"] if data["slides"] else "")

        return html

    def processar_roteiro_mapa(self, roteiro: str) -> Dict:
        """Processa roteiro para template Mapa Mental"""
        nodos = []
        titulo_geral = "Apresentação"

        lines = roteiro.strip().split("\n")
        if lines and lines[0].startswith("#") and not lines[0].startswith("##"):
            titulo_geral = lines[0].strip("# ")
            lines = lines[1:]

        nodo_id = 0
        current_nodo = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith("## "):
                # Novo nodo principal
                if current_nodo:
                    nodos.append(current_nodo)

                nodo_id += 1
                current_nodo = {
                    "id": f"nodo-{nodo_id}",
                    "titulo": line.strip("# "),
                    "conceito": "",
                    "bullets": [],
                    "notas": "",
                    "tipo": "principal"
                }

            elif line.startswith("**Conceito:**"):
                if current_nodo:
                    conceito_texto = line.split(":", 1)[1].strip()
                    # Remover ** se existir
                    conceito_texto = conceito_texto.strip("** ")
                    current_nodo["conceito"] = conceito_texto

            elif line.startswith("**Notas:**"):
                if current_nodo:
                    notas_texto = line.split(":", 1)[1].strip()
                    # Remover ** se existir
                    notas_texto = notas_texto.strip("** ")
                    current_nodo["notas"] = notas_texto

            elif line.startswith("- ") or line.startswith("✅"):
                if current_nodo:
                    current_nodo["bullets"].append(line.lstrip("- ✅").strip())

        if current_nodo:
            nodos.append(current_nodo)

        return {"titulo": titulo_geral, "nodos": nodos}

    def processar_roteiro_tech(self, roteiro: str) -> Dict:
        """Processa roteiro para template Tech Futurista"""
        slides = []
        titulo_geral = "Apresentação"

        lines = roteiro.strip().split("\n")
        if lines and lines[0].startswith("#"):
            titulo_geral = lines[0].strip("# ")
            lines = lines[1:]

        current_slide = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith("## "):
                if current_slide:
                    slides.append(current_slide)

                current_slide = {
                    "titulo": line.strip("# "),
                    "subtitulo": "",
                    "bullets": [],
                    "icon": "🚀",
                    "notas": "",
                }

            elif line.startswith("**Subtítulo:**"):
                if current_slide:
                    current_slide["subtitulo"] = line.split(":", 1)[1].strip()

            elif line.startswith("**Ícone:**"):
                if current_slide:
                    current_slide["icon"] = line.split(":", 1)[1].strip()

            elif line.startswith("**Notas:**"):
                if current_slide:
                    current_slide["notas"] = line.split(":", 1)[1].strip()

            elif line.startswith("→") or line.startswith("- "):
                if current_slide:
                    current_slide["bullets"].append(line.lstrip("→- ").strip())

            elif current_slide and not current_slide["subtitulo"]:
                current_slide["subtitulo"] = line

        if current_slide:
            slides.append(current_slide)

        return {"titulo": titulo_geral, "slides": slides}

    def gerar_html_mapa(self, data: Dict) -> str:
        """Gera HTML usando template Mapa Mental"""
        template_path = self.templates["mapa-mental"]
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()

        # Gerar SVG dos nodos e conexões
        nodos_svg = ""
        conexoes_svg = ""

        total_nodos = len(data["nodos"])
        width = 1600
        height = 900

        # Layout: nodos distribuídos horizontalmente com espaçamento
        spacing_x = width // (total_nodos + 1)
        y_center = height // 2

        # Dados dos nodos para JavaScript (modal interativo)
        nodos_data_js = []

        for i, nodo in enumerate(data["nodos"]):
            x = spacing_x * (i + 1)
            y = y_center

            # Criar retângulo do nodo
            nodo_width = 220
            nodo_height = 90
            color = "#3b82f6" if i == 0 else "#8b5cf6"  # Primeiro nodo azul, resto roxo

            # Quebrar título em múltiplas linhas se necessário
            titulo = nodo['titulo']
            titulo_line1 = titulo[:25]
            titulo_line2 = titulo[25:50] if len(titulo) > 25 else ""

            nodos_svg += f"""
            <g class="nodo" data-nodo-id="{nodo['id']}" onclick="openNodeModal('{nodo['id']}')">
                <rect x="{x - nodo_width/2}" y="{y - nodo_height/2}"
                      width="{nodo_width}" height="{nodo_height}"
                      rx="12" fill="{color}" stroke="#475569" stroke-width="2"/>
                <text x="{x}" y="{y - 10 if titulo_line2 else y}" text-anchor="middle"
                      dominant-baseline="middle" fill="#ffffff"
                      font-size="14" font-weight="600">
                    {titulo_line1}
                </text>
            """

            if titulo_line2:
                nodos_svg += f"""
                <text x="{x}" y="{y + 12}" text-anchor="middle"
                      dominant-baseline="middle" fill="#ffffff"
                      font-size="14" font-weight="600">
                    {titulo_line2}
                </text>
                """

            nodos_svg += "</g>"

            # Criar conexão com próximo nodo (seta horizontal)
            if i < total_nodos - 1:
                next_x = spacing_x * (i + 2)
                conexoes_svg += f"""
                <path class="conexao" d="M {x + nodo_width/2} {y} L {next_x - nodo_width/2} {y}"
                      stroke="#64748b" stroke-width="2" fill="none" marker-end="url(#arrowhead)"/>
                """

            # Preparar dados para JavaScript
            bullets_list = nodo["bullets"]
            nodos_data_js.append({
                "id": nodo["id"],
                "titulo": nodo["titulo"],
                "conceito": nodo["conceito"],
                "bullets": bullets_list,
                "notas": nodo["notas"]
            })

        # Converter dados para JSON
        nodos_data_json = json.dumps(nodos_data_js, ensure_ascii=False)

        notas_inicial = data["nodos"][0]["notas"] if data["nodos"] else "Clique nos nodos para navegar pelo workflow"

        html = template.replace("{{TITULO}}", data["titulo"])
        html = html.replace("{{CONEXOES}}", conexoes_svg)
        html = html.replace("{{NODOS}}", nodos_svg)
        html = html.replace("{{NOTAS}}", notas_inicial)
        html = html.replace("{{NODOS_DATA}}", nodos_data_json)

        return html

    def gerar_html_tech(self, data: Dict) -> str:
        """Gera HTML usando template Tech Futurista"""
        template_path = self.templates["tech-futurista"]
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()

        slides_html = ""
        for i, slide in enumerate(data["slides"]):
            subtitulo_html = (
                f'<p class="hero-subtitle">{slide["subtitulo"]}</p>'
                if slide["subtitulo"]
                else ""
            )

            visual_html = f"""
            <div class="visual-hero">
                <div class="visual-content">{slide["icon"]}</div>
            </div>
            """

            bullets_html = ""
            if slide["bullets"]:
                bullets_html = '<div class="bullets">'
                for bullet in slide["bullets"]:
                    bullets_html += f'<div class="bullet">{bullet}</div>'
                bullets_html += "</div>"

            notas = slide["notas"] or "Sem notas para este slide."

            slides_html += f"""
            <div class="slide" data-slide="{i+1}" data-notas="{notas}">
                <h1 class="hero-title">{slide['titulo']}</h1>
                {subtitulo_html}
                {visual_html}
                {bullets_html}
            </div>
            """

        html = template.replace("{{TITULO}}", data["titulo"])
        html = html.replace("{{SLIDES}}", slides_html)
        html = html.replace("{{NOTAS_INICIAL}}", data["slides"][0]["notas"] if data["slides"] else "")

        return html

    def gerar_apresentacao(
        self,
        roteiro_path: Path,
        template_type: TemplateType = "auto",
        output_path: Path = None,
    ) -> Path:
        """
        Gera apresentação HTML a partir de roteiro

        Args:
            roteiro_path: Caminho para arquivo de roteiro (.md ou .txt)
            template_type: Tipo de template (auto, notion, mapa-mental, tech-futurista)
            output_path: Caminho de saída (opcional, gera automaticamente se None)

        Returns:
            Path do arquivo HTML gerado
        """
        # Ler roteiro
        with open(roteiro_path, "r", encoding="utf-8") as f:
            roteiro = f.read()

        # Decidir template
        if template_type == "auto":
            template_type = self.analisar_conteudo(roteiro)
            print(f"📊 Template detectado automaticamente: {template_type}")
        else:
            print(f"📊 Template escolhido manualmente: {template_type}")

        # Processar roteiro
        if template_type == "notion":
            data = self.processar_roteiro_notion(roteiro)
            html = self.gerar_html_notion(data)
        elif template_type == "tech-futurista":
            data = self.processar_roteiro_tech(roteiro)
            html = self.gerar_html_tech(data)
        elif template_type == "mapa-mental":
            data = self.processar_roteiro_mapa(roteiro)
            html = self.gerar_html_mapa(data)
        else:
            raise ValueError(f"Template desconhecido: {template_type}")

        # Definir output path
        if output_path is None:
            nome_base = roteiro_path.stem
            output_path = roteiro_path.parent / f"apresentacao_{nome_base}.html"

        # Salvar HTML
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        # Calcular métricas baseadas no tipo de template
        if template_type == "mapa-mental":
            total_slides = len(data["nodos"])
            slide_label = "nodos"
        else:
            total_slides = len(data["slides"])
            slide_label = "slides"

        duracao_estimada = total_slides * 90  # 90 segundos por slide/nodo

        print(f"\n✅ Apresentação criada: {output_path}")
        print(f"\n📊 Template: {template_type.upper()}")
        print(f"📍 Total de {slide_label}: {total_slides}")
        print(f"⏱️  Estimativa: {duracao_estimada // 60} minutos")
        print(f"\n🎬 Como usar:")
        print(f"  • Pressione F para fullscreen")
        print(f"  • Setas ← → para navegar")
        if template_type == "mapa-mental":
            print(f"  • Clique nos nodos para ver detalhes")
            print(f"  • Use zoom +/- na toolbar")
        else:
            print(f"  • Notas aparecem na parte inferior")
            print(f"  • Timer no canto superior direito")
        print(f"\nPronto para gravar! 🚀\n")

        return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Gera apresentações HTML interativas para vídeos educativos"
    )
    parser.add_argument(
        "--roteiro", "-r", type=str, required=True, help="Caminho para arquivo de roteiro (.md ou .txt)"
    )
    parser.add_argument(
        "--template",
        "-t",
        type=str,
        default="auto",
        choices=["auto", "notion", "mapa-mental", "tech-futurista"],
        help="Template a usar (padrão: auto - detecta automaticamente)",
    )
    parser.add_argument(
        "--output", "-o", type=str, help="Caminho de saída (opcional, gera automaticamente se não especificado)"
    )
    parser.add_argument(
        "--no-open", action="store_true", help="Não abrir automaticamente no navegador"
    )

    args = parser.parse_args()

    # Validar roteiro existe
    roteiro_path = Path(args.roteiro).expanduser().resolve()
    if not roteiro_path.exists():
        print(f"❌ Erro: Roteiro não encontrado: {roteiro_path}", file=sys.stderr)
        sys.exit(1)

    # Definir output
    output_path = Path(args.output).expanduser().resolve() if args.output else None

    # Gerar apresentação
    script_dir = Path(__file__).parent
    template_dir = script_dir / "templates"

    generator = ApresentacaoGenerator(template_dir)
    html_path = generator.gerar_apresentacao(roteiro_path, args.template, output_path)

    # Abrir no navegador
    if not args.no_open:
        try:
            if sys.platform == "darwin":  # macOS
                subprocess.run(["open", str(html_path)])
            elif sys.platform == "linux":
                subprocess.run(["xdg-open", str(html_path)])
            elif sys.platform == "win32":
                subprocess.run(["start", str(html_path)], shell=True)
        except Exception as e:
            print(f"⚠️  Não foi possível abrir automaticamente: {e}")
            print(f"   Abra manualmente: {html_path}")


if __name__ == "__main__":
    main()
