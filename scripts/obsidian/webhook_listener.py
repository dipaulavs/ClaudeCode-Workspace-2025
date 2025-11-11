#!/usr/bin/env python3
"""
🌐 Webhook listener for Obsidian → Claude Code
Servidor local que recebe comandos do Obsidian

Uso:
    python3 webhook_listener.py

Endpoints:
    POST /obsidian/process - Processar nota
    POST /obsidian/task - Criar tarefa
    GET /status - Status do servidor
"""

from flask import Flask, request, jsonify
from pathlib import Path
import json
from datetime import datetime

app = Flask(__name__)

WORKSPACE = Path("/Users/felipemdepaula/Desktop/ClaudeCode-Workspace")
TEMP_DIR = WORKSPACE / "temp" / "obsidian"
TASKS_FILE = WORKSPACE / "QUICK_TASKS.txt"

# Criar diretórios
TEMP_DIR.mkdir(parents=True, exist_ok=True)

@app.route('/status', methods=['GET'])
def status():
    """Status do servidor"""
    return jsonify({
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "workspace": str(WORKSPACE)
    })

@app.route('/obsidian/process', methods=['POST'])
def process_note():
    """Processar nota do Obsidian"""
    data = request.json

    if not data or 'file' not in data:
        return jsonify({"error": "Campo 'file' obrigatório"}), 400

    file_path = data['file']
    content = data.get('content', '')

    # Salvar no workspace
    filename = Path(file_path).name
    temp_file = TEMP_DIR / filename

    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(content if content else open(file_path, 'r').read())

    print(f"✅ Nota processada: {filename}")

    return jsonify({
        "success": True,
        "message": f"Nota '{filename}' recebida",
        "saved_to": str(temp_file)
    })

@app.route('/obsidian/task', methods=['POST'])
def add_task():
    """Adicionar tarefa rápida"""
    data = request.json

    if not data or 'task' not in data:
        return jsonify({"error": "Campo 'task' obrigatório"}), 400

    task = data['task']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Adicionar tarefa
    with open(TASKS_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {task}\n")

    print(f"✅ Tarefa adicionada: {task}")

    return jsonify({
        "success": True,
        "message": "Tarefa adicionada",
        "task": task
    })

if __name__ == "__main__":
    print("🌐 Webhook Obsidian → Claude Code")
    print(f"📁 Workspace: {WORKSPACE}")
    print(f"🔗 URL: http://localhost:8000")
    print("\nEndpoints:")
    print("  • GET  /status")
    print("  • POST /obsidian/process")
    print("  • POST /obsidian/task")
    print("\n🚀 Servidor iniciando...\n")

    app.run(host='0.0.0.0', port=8000, debug=True)
