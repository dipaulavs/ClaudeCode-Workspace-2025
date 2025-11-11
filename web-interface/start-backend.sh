#!/bin/bash
echo "🚀 Iniciando Backend API (porta 8000)..."
cd "$(dirname "$0")/backend"
source venv/bin/activate
python3 main.py
