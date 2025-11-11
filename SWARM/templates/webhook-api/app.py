#!/usr/bin/env python3
"""
Template: Webhook/API para Docker Swarm + Traefik
Descrição: Servidor HTTP básico para receber webhooks
"""
import os
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Configurações
PORT = int(os.getenv('PORT', 8000))
AUTOMATION_NAME = os.getenv('AUTOMATION_NAME', 'automation')

@app.route('/health', methods=['GET'])
def health():
    """Healthcheck endpoint"""
    return jsonify({
        'status': 'healthy',
        'automation': AUTOMATION_NAME,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Recebe webhooks"""
    try:
        data = request.get_json()

        # Log
        print(f"[{datetime.now()}] Webhook recebido: {data}")

        # Sua lógica aqui
        # ...

        return jsonify({
            'status': 'success',
            'message': 'Webhook processado',
            'automation': AUTOMATION_NAME
        }), 200

    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/', methods=['GET'])
def index():
    """Página inicial"""
    return jsonify({
        'name': AUTOMATION_NAME,
        'status': 'running',
        'endpoints': {
            'health': '/health',
            'webhook': '/webhook (POST)'
        },
        'environment': 'Docker Swarm + Traefik'
    })

if __name__ == '__main__':
    print(f"🚀 {AUTOMATION_NAME} iniciando na porta {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=False)
