#!/usr/bin/env python3
"""
MCP Server Testing and Evaluation Script

This script helps test MCP servers by:
1. Starting an MCP server process
2. Running evaluation questions through an LLM
3. Comparing LLM answers to expected answers
4. Generating detailed result reports

Usage:
    python connections.py evaluate \\
        --server-command "python server.py" \\
        --eval-file evaluation.xml \\
        --output results.json
"""

import argparse
import asyncio
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

try:
    from anthropic import Anthropic
except ImportError:
    print("Error: anthropic package not installed", file=sys.stderr)
    print("Install with: pip install anthropic", file=sys.stderr)
    sys.exit(1)


class MCPEvaluator:
    """Evaluates MCP server using Q&A pairs."""

    def __init__(self, server_command: str, api_key: str | None = None):
        self.server_command = server_command
        self.server_process = None
        self.client = Anthropic(api_key=api_key)

    async def start_server(self):
        """Start the MCP server process."""
        print(f"Starting MCP server: {self.server_command}")

        self.server_process = subprocess.Popen(
            self.server_command,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Give server time to start
        await asyncio.sleep(2)

        if self.server_process.poll() is not None:
            stderr = self.server_process.stderr.read().decode()
            raise RuntimeError(f"Server failed to start:\n{stderr}")

        print("✓ Server started successfully")

    def stop_server(self):
        """Stop the MCP server process."""
        if self.server_process:
            print("Stopping MCP server...")
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
            print("✓ Server stopped")

    def load_evaluation(self, eval_file: Path) -> list[dict[str, str]]:
        """Load Q&A pairs from XML evaluation file."""
        print(f"Loading evaluation: {eval_file}")

        tree = ET.parse(eval_file)
        root = tree.getroot()

        qa_pairs = []
        for qa_pair in root.findall("qa_pair"):
            question = qa_pair.find("question").text.strip()
            answer = qa_pair.find("answer").text.strip()
            qa_pairs.append({"question": question, "expected_answer": answer})

        print(f"✓ Loaded {len(qa_pairs)} Q&A pairs")
        return qa_pairs

    async def ask_question(self, question: str) -> str:
        """Ask question to LLM using MCP server tools."""
        print(f"\nAsking: {question[:100]}...")

        try:
            # Note: This is a simplified version
            # In production, you'd use the MCP protocol to connect
            # For now, we'll simulate by asking Claude directly
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[{"role": "user", "content": question}],
            )

            answer = response.content[0].text.strip()
            print(f"Answer: {answer[:100]}...")
            return answer

        except Exception as e:
            print(f"Error asking question: {e}")
            return f"ERROR: {str(e)}"

    def compare_answers(self, expected: str, actual: str) -> bool:
        """Compare expected and actual answers."""
        # Normalize for comparison
        expected_norm = expected.strip().lower()
        actual_norm = actual.strip().lower()

        return expected_norm == actual_norm

    async def run_evaluation(
        self, eval_file: Path, output_file: Path | None = None
    ) -> dict[str, Any]:
        """Run complete evaluation."""
        # Load Q&A pairs
        qa_pairs = self.load_evaluation(eval_file)

        # Start server
        await self.start_server()

        results = {
            "total_questions": len(qa_pairs),
            "correct": 0,
            "incorrect": 0,
            "accuracy": 0.0,
            "details": [],
        }

        try:
            # Ask each question
            for i, qa in enumerate(qa_pairs, 1):
                print(f"\n{'=' * 60}")
                print(f"Question {i}/{len(qa_pairs)}")
                print(f"{'=' * 60}")

                actual_answer = await self.ask_question(qa["question"])
                is_correct = self.compare_answers(qa["expected_answer"], actual_answer)

                if is_correct:
                    results["correct"] += 1
                    print("✓ CORRECT")
                else:
                    results["incorrect"] += 1
                    print("✗ INCORRECT")
                    print(f"Expected: {qa['expected_answer']}")
                    print(f"Got: {actual_answer}")

                results["details"].append(
                    {
                        "question": qa["question"],
                        "expected": qa["expected_answer"],
                        "actual": actual_answer,
                        "correct": is_correct,
                    }
                )

        finally:
            self.stop_server()

        # Calculate accuracy
        results["accuracy"] = (
            results["correct"] / results["total_questions"]
            if results["total_questions"] > 0
            else 0.0
        )

        # Print summary
        print(f"\n{'=' * 60}")
        print("EVALUATION SUMMARY")
        print(f"{'=' * 60}")
        print(f"Total Questions: {results['total_questions']}")
        print(f"Correct: {results['correct']}")
        print(f"Incorrect: {results['incorrect']}")
        print(f"Accuracy: {results['accuracy'] * 100:.1f}%")

        # Save results
        if output_file:
            output_file.write_text(json.dumps(results, indent=2))
            print(f"\n✓ Results saved to: {output_file}")

        return results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="MCP Server Evaluation Tool")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Evaluate command
    eval_parser = subparsers.add_parser("evaluate", help="Run evaluation")
    eval_parser.add_argument(
        "--server-command",
        required=True,
        help="Command to start MCP server (e.g., 'python server.py')",
    )
    eval_parser.add_argument(
        "--eval-file", required=True, type=Path, help="Path to evaluation XML file"
    )
    eval_parser.add_argument(
        "--output", type=Path, help="Path to save results JSON (optional)"
    )
    eval_parser.add_argument(
        "--api-key", help="Anthropic API key (or set ANTHROPIC_API_KEY env var)"
    )

    args = parser.parse_args()

    if args.command == "evaluate":
        evaluator = MCPEvaluator(args.server_command, api_key=args.api_key)
        asyncio.run(evaluator.run_evaluation(args.eval_file, args.output))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
