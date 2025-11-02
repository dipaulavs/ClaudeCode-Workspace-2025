#!/usr/bin/env python3
import subprocess
import sys

# A imagem será salva como dog_image.png
image_path = "/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/dog_image.png"

print(f"📸 Imagem salva em: {image_path}")
print(f"🚀 Iniciando processo de edição...")

# Executa o script de edição
subprocess.run([
    "python3",
    "tools/edit_image_nanobanana.py",
    image_path,
    "Trocar o cachorro golden retriever por um gato laranja fofo brincando com a mesma bolinha laranja, mantendo o fundo verde desfocado, mesma pose e qualidade fotográfica"
])
