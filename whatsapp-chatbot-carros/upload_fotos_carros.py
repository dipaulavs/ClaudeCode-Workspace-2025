#!/usr/bin/env python3
"""
📤 UPLOAD EM LOTE DE FOTOS DE CARROS PARA NEXTCLOUD

Processa fotos da pasta ~/Desktop/fotos de carros/
Organiza por carro e gera links públicos permanentes.

Estrutura esperada:
~/Desktop/fotos de carros/
├── carro-001/
│   ├── foto1.jpg
│   ├── foto2.jpg
│   └── foto3.jpg
├── carro-002/
│   ├── foto1.jpg
│   └── foto2.jpg
└── ...

Uso:
    python3 upload_fotos_carros.py
"""

import os
import sys
import json
from pathlib import Path
sys.path.append('/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/tools')
from upload_to_nextcloud import NextcloudUploader, NEXTCLOUD_URL, NEXTCLOUD_USER, NEXTCLOUD_PASSWORD

# Configurações
FOTOS_DIR = Path.home() / "Desktop" / "fotos de carros"
CARROS_DIR = Path(__file__).parent / "carros"
NEXTCLOUD_FOLDER = "carros"  # Pasta específica para carros

def processar_fotos_carro(carro_dir, uploader):
    """
    Processa todas as fotos de um carro

    Args:
        carro_dir: Path do diretório do carro
        uploader: Instância do NextcloudUploader

    Returns:
        dict: Dicionário com informações e links das fotos
    """
    carro_nome = carro_dir.name
    print(f"\n{'='*70}")
    print(f"📂 Processando: {carro_nome}")
    print(f"{'='*70}")

    # Lista todas as imagens
    extensoes = ['.jpg', '.jpeg', '.png']
    fotos = []

    for ext in extensoes:
        fotos.extend(carro_dir.glob(f'*{ext}'))
        fotos.extend(carro_dir.glob(f'*{ext.upper()}'))

    if not fotos:
        print(f"⚠️  Nenhuma foto encontrada em {carro_nome}")
        return None

    print(f"📸 Encontradas {len(fotos)} foto(s)")

    # Cria estrutura de dados
    carro_data = {
        "id": carro_nome,
        "fotos": []
    }

    # Faz upload de cada foto
    for i, foto in enumerate(sorted(fotos), 1):
        try:
            print(f"\n📤 [{i}/{len(fotos)}] Uploading: {foto.name}")

            # Upload permanente (sem expiração)
            link = uploader.upload_and_share(str(foto), expire_days=None)

            carro_data["fotos"].append({
                "nome": foto.name,
                "link": link,
                "ordem": i
            })

            print(f"✅ Link: {link}")

        except Exception as e:
            print(f"❌ Erro ao processar {foto.name}: {e}")

    return carro_data

def salvar_dados_carro(carro_data):
    """Salva dados do carro no diretório de carros"""
    if not carro_data or not carro_data.get('fotos'):
        return

    carro_id = carro_data['id']
    carro_path = CARROS_DIR / carro_id

    # Cria diretório do carro
    carro_path.mkdir(parents=True, exist_ok=True)

    # Salva links.json
    links_file = carro_path / "links.json"
    with open(links_file, 'w', encoding='utf-8') as f:
        json.dump(carro_data, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Dados salvos em: {links_file}")

    # Cria arquivos template se não existirem
    templates = {
        "base.txt": f"""🚗 {carro_id}

📋 Informações Básicas:
• Marca: [Ex: Volkswagen]
• Modelo: [Ex: Gol 1.0 Flex]
• Ano: [Ex: 2020]
• Kilometragem: [Ex: 35.000 km]
• Cor: [Ex: Prata]
• Combustível: [Ex: Flex]
• Câmbio: [Ex: Manual]

💰 Preço:
• À vista: R$ [valor]
• Entrada: R$ [valor]
• Parcelas: R$ [valor]/mês

📍 Localização:
• Disponível na loja
• Aceita test drive agendado
""",
        "detalhes.txt": f"""🔧 Detalhes Técnicos: {carro_id}

Motor:
• [Ex: 1.0 Flex]
• [Ex: 82 cv]

Opcionais:
✅ [Listar opcionais: ar, direção, vidros, alarme, etc]

Estado:
✅ Revisado
✅ Documentação em dia
✅ [Outros detalhes]

Consumo:
• Cidade: ~[valor] km/l
• Estrada: ~[valor] km/l
""",
        "faq.txt": f"""❓ Perguntas Frequentes: {carro_id}

🔹 Aceita troca?
[Resposta]

🔹 Tem garantia?
[Resposta]

🔹 Aceita financiamento?
[Resposta]

🔹 Pode fazer test drive?
[Resposta]

🔹 O carro está revisado?
[Resposta]
""",
        "historico.txt": f"""📜 Histórico do Veículo: {carro_id}

🔹 Proprietários:
• [Ex: Único dono]

🔹 Acidentes:
• [Ex: Sem acidentes]

🔹 Revisões:
✅ [Listar revisões]

🔹 Multas:
• [Ex: Sem multas pendentes]

🔹 Débitos:
• [Ex: IPVA quitado]
""",
        "financiamento.txt": f"""💳 Opções de Financiamento: {carro_id}

🏦 Plano 1:
• Entrada: R$ [valor]
• Parcelas: [quantidade]x de R$ [valor]

🏦 Plano 2:
• Entrada: R$ [valor]
• Parcelas: [quantidade]x de R$ [valor]

✨ Vantagens:
• [Listar vantagens]

📱 Bancos Parceiros:
• [Listar bancos]
"""
    }

    for filename, content in templates.items():
        filepath = carro_path / filename
        if not filepath.exists():
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"📝 Template criado: {filename}")

def main():
    print("=" * 70)
    print("📤 UPLOAD EM LOTE DE FOTOS DE CARROS")
    print("=" * 70)

    # Verifica se pasta de fotos existe
    if not FOTOS_DIR.exists():
        print(f"\n❌ Erro: Pasta não encontrada!")
        print(f"📂 Crie a pasta: {FOTOS_DIR}")
        print(f"\nEstrutura esperada:")
        print(f"  {FOTOS_DIR}/")
        print(f"  ├── carro-001/")
        print(f"  │   ├── foto1.jpg")
        print(f"  │   └── foto2.jpg")
        print(f"  └── carro-002/")
        print(f"      └── foto1.jpg")
        sys.exit(1)

    # Cria diretório de carros
    CARROS_DIR.mkdir(exist_ok=True)

    # Inicializa uploader
    print(f"\n🔌 Conectando ao Nextcloud...")
    print(f"📡 Servidor: {NEXTCLOUD_URL}")
    print(f"👤 Usuário: {NEXTCLOUD_USER}")
    print(f"📁 Pasta: {NEXTCLOUD_FOLDER}")

    uploader = NextcloudUploader(
        url=NEXTCLOUD_URL,
        username=NEXTCLOUD_USER,
        password=NEXTCLOUD_PASSWORD,
        base_folder=NEXTCLOUD_FOLDER
    )

    # Processa cada diretório de carro
    carros_processados = 0
    total_fotos = 0

    for carro_dir in sorted(FOTOS_DIR.iterdir()):
        if not carro_dir.is_dir():
            continue

        carro_data = processar_fotos_carro(carro_dir, uploader)

        if carro_data:
            salvar_dados_carro(carro_data)
            carros_processados += 1
            total_fotos += len(carro_data['fotos'])

    print("\n" + "=" * 70)
    print("✅ UPLOAD CONCLUÍDO!")
    print("=" * 70)
    print(f"📊 Carros processados: {carros_processados}")
    print(f"📸 Total de fotos: {total_fotos}")
    print(f"💾 Dados salvos em: {CARROS_DIR}")
    print("\n💡 Próximos passos:")
    print("   1. Edite os arquivos .txt em cada pasta de carro")
    print("   2. Inicie o chatbot com: python3 chatbot_automaia_v1.py")

if __name__ == '__main__':
    main()
