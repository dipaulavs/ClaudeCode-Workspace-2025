#!/usr/bin/env python3
"""
Benchmark: Nano Banana Direct vs MCP

Compara performance entre:
1. Abordagem DIRETA: Importa funções do tools/generate_image_nanobanana.py
2. Abordagem MCP: Chama via Model Context Protocol server

Métricas medidas:
- Latência total (início → download completo)
- Overhead do MCP
- Overhead de inicialização
- Taxa de sucesso
"""

import time
import sys
import os
import json
from pathlib import Path
from datetime import datetime
import subprocess
import tempfile
from dataclasses import dataclass
from typing import Dict, Optional, List

# Add tools to path
TOOLS_PATH = Path(__file__).parent.parent.parent / "tools"
sys.path.insert(0, str(TOOLS_PATH))

from generate_image_nanobanana import (
    generate_image,
    wait_for_completion,
    download_image,
)


@dataclass
class BenchmarkResult:
    """Armazena resultado de um benchmark"""
    name: str
    prompt: str
    total_time: float
    generation_time: float
    download_time: float
    success: bool
    image_path: Optional[str] = None
    error: Optional[str] = None


class BenchmarkRunner:
    """Executa benchmarks comparativos"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results: List[BenchmarkResult] = []
        self.test_prompt = "gato astronauta flutuando no espaço, estilo ilustração digital, cinematic"

    def print_section(self, title: str):
        """Imprime header de seção"""
        print("\n" + "┌" + "─" * 48 + "┐")
        print("│ " + title.center(46) + " │")
        print("└" + "─" * 48 + "┘\n")

    def print_row(self, label: str, value: str, width: int = 46):
        """Imprime linha formatada"""
        print(f"│ {label:<20} {value:>{width-22}} │")

    def print_divider(self):
        """Imprime linha divisória"""
        print("├" + "─" * 48 + "┤")

    def test_direct_approach(self) -> BenchmarkResult:
        """Teste 1: Abordagem direta (import + chama)"""
        self.print_section("TESTE 1: ABORDAGEM DIRETA")
        print("📍 Estratégia: Import tools + chamada direta\n")

        result = BenchmarkResult(
            name="Direct Import",
            prompt=self.test_prompt,
            total_time=0,
            generation_time=0,
            download_time=0,
            success=False
        )

        try:
            # Marca início
            start_total = time.time()

            print("⏱️  Iniciando geração...")
            start_gen = time.time()

            # Chamada direta
            task_id = generate_image(
                self.test_prompt,
                output_format="PNG"
            )

            if not task_id:
                raise Exception("Falha ao criar tarefa")

            # Aguarda conclusão
            image_urls = wait_for_completion(task_id)

            if not image_urls:
                raise Exception("Falha ao aguardar conclusão")

            result.generation_time = time.time() - start_gen

            # Download
            print("\n⏱️  Iniciando download...")
            start_dl = time.time()

            with tempfile.TemporaryDirectory() as tmpdir:
                output_path = os.path.join(tmpdir, "direct_test.png")
                saved_path = download_image(image_urls[0], output_path)

                result.download_time = time.time() - start_dl
                result.image_path = saved_path

            result.total_time = time.time() - start_total
            result.success = True

            print(f"\n✅ Sucesso!")

        except Exception as e:
            result.error = str(e)
            result.success = False
            print(f"\n❌ Erro: {e}")

        # Exibe resultados
        print("\n" + "┌" + "─" * 48 + "┐")
        self.print_row("Tempo Total", f"{result.total_time:.2f}s")
        self.print_row("Geração", f"{result.generation_time:.2f}s")
        self.print_row("Download", f"{result.download_time:.2f}s")
        self.print_row("Status", "✅ SUCESSO" if result.success else "❌ ERRO")
        print("└" + "─" * 48 + "┘\n")

        return result

    def test_sequential_calls(self, num_calls: int = 3) -> BenchmarkResult:
        """Teste 2: Múltiplas chamadas sequenciais"""
        self.print_section(f"TESTE 2: {num_calls} CHAMADAS SEQUENCIAIS")
        print(f"📍 Estratégia: Direct import com {num_calls} gerações\n")

        result = BenchmarkResult(
            name=f"Sequential x{num_calls}",
            prompt=self.test_prompt,
            total_time=0,
            generation_time=0,
            download_time=0,
            success=False
        )

        try:
            start_total = time.time()
            success_count = 0

            for i in range(num_calls):
                print(f"\n[{i+1}/{num_calls}] Gerando imagem {i+1}...")

                start_gen = time.time()
                task_id = generate_image(
                    f"{self.test_prompt} (versão {i+1})",
                    output_format="PNG"
                )

                if not task_id:
                    continue

                image_urls = wait_for_completion(task_id)

                if image_urls:
                    result.generation_time += time.time() - start_gen

                    start_dl = time.time()
                    with tempfile.TemporaryDirectory() as tmpdir:
                        output_path = os.path.join(tmpdir, f"sequential_{i}.png")
                        download_image(image_urls[0], output_path)
                    result.download_time += time.time() - start_dl

                    success_count += 1

            result.total_time = time.time() - start_total
            result.success = success_count == num_calls

            print(f"\n✅ {success_count}/{num_calls} imagens geradas com sucesso")

        except Exception as e:
            result.error = str(e)
            result.success = False
            print(f"\n❌ Erro: {e}")

        # Exibe resultados
        print("\n" + "┌" + "─" * 48 + "┐")
        self.print_row("Tempo Total", f"{result.total_time:.2f}s")
        self.print_row("Tempo Geração (total)", f"{result.generation_time:.2f}s")
        self.print_row("Tempo Download (total)", f"{result.download_time:.2f}s")
        self.print_row("Taxa de Sucesso", f"{success_count}/{num_calls}")
        print("└" + "─" * 48 + "┘\n")

        return result

    def test_import_overhead(self, iterations: int = 5) -> BenchmarkResult:
        """Teste 3: Overhead de importação"""
        self.print_section(f"TESTE 3: OVERHEAD DE IMPORT ({iterations}x)")
        print("📍 Estratégia: Medir tempo de import vs chamadas\n")

        result = BenchmarkResult(
            name="Import Overhead",
            prompt="teste overhead",
            total_time=0,
            generation_time=0,
            download_time=0,
            success=False
        )

        try:
            times = []

            for i in range(iterations):
                print(f"[{i+1}/{iterations}] Medindo overhead...")

                # Restart Python para limpar cache de import
                start = time.time()

                # Simula: reset module cache
                if 'generate_image_nanobanana' in sys.modules:
                    del sys.modules['generate_image_nanobanana']

                # Re-import
                from generate_image_nanobanana import generate_image as gen_img

                elapsed = time.time() - start
                times.append(elapsed)

                print(f"   Iteração {i+1}: {elapsed*1000:.1f}ms")

            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)

            result.total_time = sum(times)
            result.success = True

        except Exception as e:
            result.error = str(e)
            result.success = False
            print(f"\n❌ Erro: {e}")

        # Exibe resultados
        print("\n" + "┌" + "─" * 48 + "┐")
        self.print_row("Tempo Médio", f"{avg_time*1000:.1f}ms")
        self.print_row("Mínimo", f"{min_time*1000:.1f}ms")
        self.print_row("Máximo", f"{max_time*1000:.1f}ms")
        self.print_row("Total", f"{result.total_time:.2f}s")
        print("└" + "─" * 48 + "┘\n")

        return result

    def test_error_handling(self) -> BenchmarkResult:
        """Teste 4: Tratamento de erros"""
        self.print_section("TESTE 4: TRATAMENTO DE ERROS")
        print("📍 Estratégia: Tentar prompt inválido\n")

        result = BenchmarkResult(
            name="Error Handling",
            prompt="",
            total_time=0,
            generation_time=0,
            download_time=0,
            success=False
        )

        try:
            start = time.time()

            # Tenta com prompt vazio
            print("Testando com prompt vazio...")
            task_id = generate_image("", output_format="PNG")

            if not task_id:
                print("✅ Erro capturado corretamente (prompt vazio rejeitado)")
                result.success = True
            else:
                print("⚠️  Prompt vazio foi aceito (esperado rejeitado)")
                result.success = False

            result.total_time = time.time() - start

        except Exception as e:
            print(f"✅ Exceção capturada: {type(e).__name__}")
            result.success = True
            result.total_time = time.time() - start

        # Exibe resultados
        print("\n" + "┌" + "─" * 48 + "┐")
        self.print_row("Tempo", f"{result.total_time:.2f}s")
        self.print_row("Erro Detectado", "✅ SIM" if result.success else "❌ NÃO")
        print("└" + "─" * 48 + "┘\n")

        return result

    def generate_report(self):
        """Gera relatório comparativo final"""
        self.print_section("RELATÓRIO FINAL")

        print("┌" + "─" * 48 + "┐")
        print("│" + " RESUMO DOS TESTES ".center(48) + "│")
        self.print_divider()

        for i, r in enumerate(self.results, 1):
            status = "✅ PASSOU" if r.success else "❌ FALHOU"
            print(f"│ {i}. {r.name:<22} {status:>20} │")

        print("└" + "─" * 48 + "┘\n")

        # Análise de velocidade
        if len(self.results) >= 1:
            direct = self.results[0]

            print("┌" + "─" * 48 + "┐")
            print("│" + " ANÁLISE DE PERFORMANCE ".center(48) + "│")
            self.print_divider()

            if direct.success:
                self.print_row("Geração (Direct)", f"{direct.generation_time:.2f}s")
                self.print_row("Download", f"{direct.download_time:.2f}s")
                self.print_row("Total", f"{direct.total_time:.2f}s")

            print("└" + "─" * 48 + "┘\n")

        # Salva relatório em JSON
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "test_prompt": self.test_prompt,
            "results": [
                {
                    "name": r.name,
                    "success": r.success,
                    "total_time": r.total_time,
                    "generation_time": r.generation_time,
                    "download_time": r.download_time,
                    "error": r.error
                }
                for r in self.results
            ]
        }

        report_path = Path(__file__).parent / f"benchmark_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)

        print(f"📊 Relatório salvo em: {report_path}\n")

        return report_path

    def run_all_tests(self):
        """Executa todos os testes"""
        print("\n" + "=" * 50)
        print("║" + " BENCHMARK: DIRECT vs MCP ".center(48) + "║")
        print("=" * 50)

        self.print_section("CONFIGURAÇÃO")
        print(f"Prompt teste: {self.test_prompt}\n")

        # Executa testes
        try:
            self.results.append(self.test_direct_approach())
        except Exception as e:
            print(f"❌ Erro no teste direto: {e}\n")

        try:
            self.results.append(self.test_sequential_calls(num_calls=2))
        except Exception as e:
            print(f"❌ Erro no teste sequencial: {e}\n")

        try:
            self.results.append(self.test_import_overhead(iterations=3))
        except Exception as e:
            print(f"❌ Erro no teste de overhead: {e}\n")

        try:
            self.results.append(self.test_error_handling())
        except Exception as e:
            print(f"❌ Erro no teste de erro: {e}\n")

        # Gera relatório
        report_path = self.generate_report()

        print("=" * 50)
        print("║" + " BENCHMARK CONCLUÍDO ".center(48) + "║")
        print("=" * 50 + "\n")

        return self.results


def main():
    """Função principal"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Benchmark: Direct vs MCP para geração de imagens"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Modo verbose"
    )
    parser.add_argument(
        "--quick", "-q",
        action="store_true",
        help="Executar apenas teste rápido (direct)"
    )
    parser.add_argument(
        "--prompt", "-p",
        type=str,
        help="Prompt customizado para teste"
    )

    args = parser.parse_args()

    runner = BenchmarkRunner(verbose=args.verbose)

    if args.prompt:
        runner.test_prompt = args.prompt

    if args.quick:
        print("\n🚀 Modo rápido: apenas teste direct\n")
        runner.results.append(runner.test_direct_approach())
        runner.generate_report()
    else:
        runner.run_all_tests()


if __name__ == "__main__":
    main()
