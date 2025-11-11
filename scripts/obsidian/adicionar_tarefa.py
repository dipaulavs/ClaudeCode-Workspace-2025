#!/usr/bin/env python3
"""
Script para adicionar tarefas no Obsidian com data automática
Uso: python3 adicionar_tarefa.py "Texto da tarefa"
"""

import sys
import os
from datetime import datetime
from pathlib import Path

# Configuração
OBSIDIAN_VAULT = Path.home() / "Documents/Obsidian/Claude-code-ios"
TAREFAS_DIR = OBSIDIAN_VAULT / "📋 Tarefas"
TAREFAS_INDEX = OBSIDIAN_VAULT / "📊 Tarefas.md"

def criar_slug(texto):
    """Cria slug do título para nome do arquivo"""
    import re
    texto = texto.lower()
    texto = re.sub(r'[^\w\s-]', '', texto)
    texto = re.sub(r'[-\s]+', '-', texto)
    return texto[:50]  # Limita tamanho

def adicionar_tarefa(descricao):
    """Adiciona nova tarefa com data automática"""

    # Data/hora atual
    agora = datetime.now()
    data_hora = agora.strftime("%d/%m %Hh")
    data_completa = agora.strftime("%d/%m/%Y %H:%M")

    # Nome do arquivo
    slug = criar_slug(descricao)
    timestamp = agora.strftime("%Y%m%d-%H%M%S")
    nome_arquivo = f"{timestamp}-{slug}.md"

    # Caminho completo
    caminho_tarefa = TAREFAS_DIR / nome_arquivo

    # Conteúdo da tarefa
    conteudo = f"""---
criada: {data_completa}
status: aberta
---

# {descricao}

## 📝 Detalhes



## ✅ Checklist
- [ ]

"""

    # Criar pasta se não existir
    TAREFAS_DIR.mkdir(parents=True, exist_ok=True)

    # Criar arquivo da tarefa
    caminho_tarefa.write_text(conteudo, encoding='utf-8')

    # Adicionar entrada no índice
    if TAREFAS_INDEX.exists():
        conteudo_index = TAREFAS_INDEX.read_text(encoding='utf-8')

        # Procurar seção "Última Tarefa Adicionada"
        if "## 🔥 Última Tarefa Adicionada" not in conteudo_index:
            # Adicionar seção após o título
            linhas = conteudo_index.split('\n')
            nova_secao = f"""
## 🔥 Última Tarefa Adicionada

**{data_hora}** - [[📋 Tarefas/{nome_arquivo.replace('.md', '')}|{descricao}]]

---
"""
            # Inserir após a primeira linha de "---"
            for i, linha in enumerate(linhas):
                if linha.strip() == '---' and i > 0:
                    linhas.insert(i + 1, nova_secao)
                    break

            conteudo_index = '\n'.join(linhas)
            TAREFAS_INDEX.write_text(conteudo_index, encoding='utf-8')
        else:
            # Atualizar seção existente
            linhas = conteudo_index.split('\n')
            nova_entrada = f"**{data_hora}** - [[📋 Tarefas/{nome_arquivo.replace('.md', '')}|{descricao}]]"

            for i, linha in enumerate(linhas):
                if linha.startswith("## 🔥 Última Tarefa Adicionada"):
                    # Substituir próxima linha não vazia
                    for j in range(i + 1, len(linhas)):
                        if linhas[j].strip() and not linhas[j].startswith('---'):
                            linhas[j] = nova_entrada
                            break
                    break

            conteudo_index = '\n'.join(linhas)
            TAREFAS_INDEX.write_text(conteudo_index, encoding='utf-8')

    print(f"✅ Tarefa criada: {nome_arquivo}")
    print(f"📍 Caminho: {caminho_tarefa}")
    print(f"🔗 Link: [[📋 Tarefas/{nome_arquivo.replace('.md', '')}|{descricao}]]")

    return caminho_tarefa

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 adicionar_tarefa.py \"Texto da tarefa\"")
        print("\nExemplo:")
        print("  python3 adicionar_tarefa.py \"Revisar código do chatbot\"")
        sys.exit(1)

    descricao = ' '.join(sys.argv[1:])
    adicionar_tarefa(descricao)

if __name__ == "__main__":
    main()
