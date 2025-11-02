#!/bin/bash
echo "🌐 Iniciando Frontend Web (porta 3000)..."
cd "$(dirname "$0")/frontend"
python3 server.py
