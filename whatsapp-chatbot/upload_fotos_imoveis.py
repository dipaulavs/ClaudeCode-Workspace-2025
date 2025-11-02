#!/usr/bin/env python3
"""
📤 UPLOAD EM LOTE DE FOTOS DE IMÓVEIS PARA NEXTCLOUD

Processa fotos da pasta ~/Desktop/fotos de imoveis/
Organiza por imóvel e gera links públicos permanentes.

Estrutura esperada:
~/Desktop/fotos de imoveis/
├── imovel-001/
│   ├── foto1.jpg
│   ├── foto2.jpg
│   └── foto3.jpg
├── imovel-002/
│   ├── foto1.jpg
│   └── foto2.jpg
└── ...

Uso:
    python3 upload_fotos_imoveis.py
"""

import os
import sys
import json
from pathlib import Path
sys.path.append('/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/tools')
from upload_to_nextcloud import NextcloudUploader, NEXTCLOUD_URL, NEXTCLOUD_USER, NEXTCLOUD_PASSWORD

# Configurações
FOTOS_DIR = Path.home() / "Desktop" / "fotos imoveis"  # Corrigido: sem "de"
IMOVEIS_DIR = Path(__file__).parent / "imoveis"
NEXTCLOUD_FOLDER = "imoveis"  # Pasta específica para imóveis

def processar_fotos_imovel(imovel_dir, uploader):
    """
    Processa todas as fotos de um imóvel

    Args:
        imovel_dir: Path do diretório do imóvel
        uploader: Instância do NextcloudUploader

    Returns:
        dict: Dicionário com informações e links das fotos
    """
    imovel_nome = imovel_dir.name
    print(f"\n{'='*70}")
    print(f"📂 Processando: {imovel_nome}")
    print(f"{'='*70}")

    # Lista todas as imagens
    extensoes = ['.jpg', '.jpeg', '.png']
    fotos = []

    for ext in extensoes:
        fotos.extend(imovel_dir.glob(f'*{ext}'))
        fotos.extend(imovel_dir.glob(f'*{ext.upper()}'))

    if not fotos:
        print(f"⚠️  Nenhuma foto encontrada em {imovel_nome}")
        return None

    print(f"📸 Encontradas {len(fotos)} foto(s)")

    # Cria estrutura de dados
    imovel_data = {
        "id": imovel_nome,
        "fotos": []
    }

    # Faz upload de cada foto
    for i, foto in enumerate(sorted(fotos), 1):
        try:
            print(f"\n📤 [{i}/{len(fotos)}] Uploading: {foto.name}")

            # Upload permanente (sem expiração)
            link = uploader.upload_and_share(str(foto), expire_days=None)

            imovel_data["fotos"].append({
                "nome": foto.name,
                "link": link,
                "ordem": i
            })

            print(f"✅ Link: {link}")

        except Exception as e:
            print(f"❌ Erro ao processar {foto.name}: {e}")

    return imovel_data

def salvar_dados_imovel(imovel_data):
    """Salva dados do imóvel no diretório de imóveis"""
    if not imovel_data or not imovel_data.get('fotos'):
        return

    imovel_id = imovel_data['id']
    imovel_path = IMOVEIS_DIR / imovel_id

    # Cria diretório do imóvel
    imovel_path.mkdir(parents=True, exist_ok=True)

    # Salva links.json
    links_file = imovel_path / "links.json"
    with open(links_file, 'w', encoding='utf-8') as f:
        json.dump(imovel_data, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Dados salvos em: {links_file}")

    # Cria arquivos template se não existirem
    templates = {
        "descricao.txt": f"# DESCRIÇÃO DO IMÓVEL: {imovel_id}\n\n[Adicione aqui a descrição completa do imóvel]\n\nCaracterísticas:\n- \n- \n- \n",
        "localizacao.txt": f"# LOCALIZAÇÃO: {imovel_id}\n\n[Adicione aqui o endereço completo]\n\nEndereço:\nBairro:\nCidade:\nCEP:\n",
        "faq.txt": f"# FAQ: {imovel_id}\n\n## Perguntas Frequentes\n\n### Qual o valor?\n[Resposta]\n\n### Aceita financiamento?\n[Resposta]\n\n### Tem vaga de garagem?\n[Resposta]\n"
    }

    for filename, content in templates.items():
        filepath = imovel_path / filename
        if not filepath.exists():
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"📝 Template criado: {filename}")

def main():
    print("=" * 70)
    print("📤 UPLOAD EM LOTE DE FOTOS DE IMÓVEIS")
    print("=" * 70)

    # Verifica se pasta de fotos existe
    if not FOTOS_DIR.exists():
        print(f"\n❌ Erro: Pasta não encontrada!")
        print(f"📂 Crie a pasta: {FOTOS_DIR}")
        print(f"\nEstrutura esperada:")
        print(f"  {FOTOS_DIR}/")
        print(f"  ├── imovel-001/")
        print(f"  │   ├── foto1.jpg")
        print(f"  │   └── foto2.jpg")
        print(f"  └── imovel-002/")
        print(f"      └── foto1.jpg")
        sys.exit(1)

    # Cria diretório de imóveis
    IMOVEIS_DIR.mkdir(exist_ok=True)

    # Inicializa uploader
    print(f"\n🔌 Conectando ao Nextcloud...")
    print(f"📡 Servidor: {NEXTCLOUD_URL}")
    print(f"👤 Usuário: {NEXTCLOUD_USER}")
    print(f"📁 Pasta: {NEXTCLOUD_FOLDER}")

    uploader = NextcloudUploader(
        NEXTCLOUD_URL,
        NEXTCLOUD_USER,
        NEXTCLOUD_PASSWORD,
        NEXTCLOUD_FOLDER
    )

    # Lista diretórios de imóveis
    imoveis = [d for d in FOTOS_DIR.iterdir() if d.is_dir()]

    if not imoveis:
        print(f"\n⚠️  Nenhum imóvel encontrado em: {FOTOS_DIR}")
        print(f"\nCrie subpastas com fotos dos imóveis:")
        print(f"  mkdir '{FOTOS_DIR}/imovel-001'")
        sys.exit(1)

    print(f"\n📊 Encontrados {len(imoveis)} imóvel(is)")

    # Confirma antes de processar
    print(f"\n⚠️  ATENÇÃO:")
    print(f"   - Isso vai fazer upload de TODAS as fotos para o Nextcloud")
    print(f"   - Links serão PERMANENTES (não expiram)")
    print(f"   - Dados serão salvos em: {IMOVEIS_DIR}")

    resposta = input(f"\n🤔 Deseja continuar? (s/N): ").strip().lower()

    if resposta != 's':
        print("\n❌ Operação cancelada!")
        sys.exit(0)

    # Processa cada imóvel
    resultados = []

    for imovel_dir in sorted(imoveis):
        try:
            imovel_data = processar_fotos_imovel(imovel_dir, uploader)

            if imovel_data:
                salvar_dados_imovel(imovel_data)
                resultados.append(imovel_data)

        except Exception as e:
            print(f"\n❌ Erro ao processar {imovel_dir.name}: {e}")
            import traceback
            traceback.print_exc()

    # Resumo final
    print(f"\n{'='*70}")
    print(f"✅ PROCESSAMENTO CONCLUÍDO!")
    print(f"{'='*70}")
    print(f"\n📊 Estatísticas:")
    print(f"   • Imóveis processados: {len(resultados)}")

    total_fotos = sum(len(r['fotos']) for r in resultados)
    print(f"   • Total de fotos: {total_fotos}")
    print(f"   • Dados salvos em: {IMOVEIS_DIR}")

    print(f"\n📝 Próximos passos:")
    print(f"   1. Edite os arquivos descricao.txt de cada imóvel")
    print(f"   2. Edite os arquivos localizacao.txt")
    print(f"   3. Edite os arquivos faq.txt")
    print(f"   4. Reinicie o bot para carregar os dados")

    print(f"\n🤖 Para reiniciar o bot:")
    print(f"   ./PARAR_BOT_V4.sh && ./INICIAR_BOT_V4.sh")

    print(f"\n{'='*70}\n")

if __name__ == "__main__":
    main()
