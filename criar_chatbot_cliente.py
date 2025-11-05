#!/usr/bin/env python3
"""
🤖 GERADOR DE CHATBOT - Framework Universal
Clona estrutura Automaia e adapta para qualquer nicho

USO:
    python3 criar_chatbot_cliente.py
"""

import os
import shutil
import json
import re
from pathlib import Path
from typing import Dict, List

class GeradorChatbot:
    """Gera chatbot completo a partir do template"""

    TEMPLATE_DIR = Path(__file__).parent / "chatbot-template"

    # Nichos pré-configurados
    NICHOS = {
        "1": {
            "nome": "Imobiliária",
            "pasta_itens": "imoveis",
            "item_singular": "imóvel",
            "item_plural": "imóveis",
            "campos_item": ["base.txt", "detalhes.txt", "faq.txt", "legal.txt", "financiamento.txt", "links.json"],
            "tom": "profissional e consultivo",
            "exemplo_item": "apartamento-leblon-001"
        },
        "2": {
            "nome": "Loja/E-commerce",
            "pasta_itens": "produtos",
            "item_singular": "produto",
            "item_plural": "produtos",
            "campos_item": ["base.txt", "detalhes.txt", "faq.txt", "garantia.txt", "especificacoes.txt", "links.json"],
            "tom": "amigável e prestativo",
            "exemplo_item": "notebook-dell-001"
        },
        "3": {
            "nome": "Seminovos (Carros)",
            "pasta_itens": "carros",
            "item_singular": "carro",
            "item_plural": "carros",
            "campos_item": ["base.txt", "detalhes.txt", "faq.txt", "historico.txt", "financiamento.txt", "links.json"],
            "tom": "direto e transparente",
            "exemplo_item": "civic-2018-001"
        },
        "4": {
            "nome": "Telemarketing/Serviços",
            "pasta_itens": "servicos",
            "item_singular": "serviço",
            "item_plural": "serviços",
            "campos_item": ["base.txt", "detalhes.txt", "faq.txt", "planos.txt", "diferenciais.txt"],
            "tom": "persuasivo e profissional",
            "exemplo_item": "plano-internet-001"
        },
        "5": {
            "nome": "Personalizado",
            "pasta_itens": None,  # Pede ao usuário
            "item_singular": None,
            "item_plural": None,
            "campos_item": None,
            "tom": None,
            "exemplo_item": None
        }
    }

    def __init__(self):
        self.config = {}

    def coletar_informacoes(self) -> Dict:
        """Coleta informações interativas do usuário"""

        print("\n" + "="*60)
        print("🤖 GERADOR DE CHATBOT - Framework Universal")
        print("="*60)
        print()

        # Nome do cliente
        print("📝 Nome do cliente/empresa:")
        nome_cliente = input("   → ").strip()

        # Slug (identificador técnico)
        slug = re.sub(r'[^a-z0-9]+', '-', nome_cliente.lower()).strip('-')
        print(f"   ✅ Slug técnico: {slug}")

        # Escolher nicho
        print("\n🎯 Escolha o nicho:")
        for key, nicho in self.NICHOS.items():
            print(f"   {key}. {nicho['nome']}")

        escolha = input("\n   → ").strip()
        nicho = self.NICHOS.get(escolha, self.NICHOS["5"])

        # Se personalizado, pedir detalhes
        if nicho["nome"] == "Personalizado":
            print("\n🔧 Configuração Personalizada:")
            nicho["pasta_itens"] = input("   Nome da pasta de itens (ex: produtos): ").strip()
            nicho["item_singular"] = input("   Item no singular (ex: produto): ").strip()
            nicho["item_plural"] = input("   Item no plural (ex: produtos): ").strip()
            nicho["tom"] = input("   Tom de conversa: ").strip()
            nicho["exemplo_item"] = input("   Exemplo de ID (ex: item-001): ").strip()

            print("\n   Campos do item (separados por vírgula):")
            print("   Ex: base.txt, detalhes.txt, faq.txt, links.json")
            campos = input("   → ").strip()
            nicho["campos_item"] = [c.strip() for c in campos.split(",")]

        # Descrição do negócio
        print(f"\n📋 Descrição breve do negócio ({nome_cliente}):")
        descricao = input("   → ").strip()

        # Número WhatsApp vendedor
        print("\n📱 WhatsApp do vendedor (DDI+DDD+número):")
        print("   Ex: 5531999887766")
        whatsapp_vendedor = input("   → ").strip()

        # Porta
        print("\n🔌 Porta do bot (padrão: 5005):")
        porta_bot = input("   → ").strip() or "5005"
        porta_middleware = str(int(porta_bot) + 1)

        return {
            "nome_cliente": nome_cliente,
            "slug": slug,
            "nicho": nicho,
            "descricao": descricao,
            "whatsapp_vendedor": whatsapp_vendedor,
            "porta_bot": porta_bot,
            "porta_middleware": porta_middleware,
            "dir_destino": Path(__file__).parent / f"whatsapp-chatbot-{slug}"
        }

    def criar_estrutura(self, config: Dict):
        """Copia template e cria estrutura"""

        print("\n" + "="*60)
        print("📁 Criando estrutura do projeto...")
        print("="*60)

        destino = config["dir_destino"]

        # Copiar template
        print(f"\n1️⃣ Copiando template...")
        if destino.exists():
            resp = input(f"   ⚠️ {destino} já existe. Sobrescrever? (s/n): ")
            if resp.lower() != 's':
                print("   ❌ Operação cancelada")
                return False
            shutil.rmtree(destino)

        shutil.copytree(self.TEMPLATE_DIR, destino)
        print(f"   ✅ Copiado para: {destino}")

        # Renomear pasta de itens
        print("\n2️⃣ Adaptando estrutura de itens...")
        pasta_antiga = destino / "carros"
        pasta_nova = destino / config["nicho"]["pasta_itens"]

        if pasta_antiga.exists() and pasta_antiga != pasta_nova:
            pasta_antiga.rename(pasta_nova)
            print(f"   ✅ carros/ → {config['nicho']['pasta_itens']}/")

        # Criar item exemplo
        item_exemplo = pasta_nova / config["nicho"]["exemplo_item"]
        if not item_exemplo.exists():
            item_exemplo.mkdir(parents=True)
            for campo in config["nicho"]["campos_item"]:
                if campo.endswith(".json"):
                    (item_exemplo / campo).write_text('{"fotos": []}')
                else:
                    (item_exemplo / campo).write_text(f"# {campo}\n\nPreencher informações aqui")
            print(f"   ✅ Item exemplo criado: {item_exemplo.name}")

        return True

    def adaptar_codigo(self, config: Dict):
        """Find/replace em todos arquivos Python/Shell/JSON"""

        print("\n3️⃣ Adaptando código...")

        destino = config["dir_destino"]

        # Mapeamento de substituições
        substituicoes = {
            # Nomes
            "automaia": config["slug"],
            "Automaia": config["nome_cliente"],
            "AUTOMAIA": config["slug"].upper(),

            # Itens
            "carros": config["nicho"]["pasta_itens"],
            "carro": config["nicho"]["item_singular"],

            # Portas
            "5003": config["porta_bot"],
            "5004": config["porta_middleware"],

            # Descrição
            "Agência de Carros Seminovos": config["descricao"],
            "seminovos": config["nicho"]["item_plural"]
        }

        # Arquivos a modificar
        extensoes = [".py", ".sh", ".json", ".md"]
        arquivos_modificados = 0

        for ext in extensoes:
            for arquivo in destino.rglob(f"*{ext}"):
                if "__pycache__" in str(arquivo) or ".git" in str(arquivo):
                    continue

                try:
                    conteudo = arquivo.read_text()
                    conteudo_novo = conteudo

                    for antigo, novo in substituicoes.items():
                        conteudo_novo = conteudo_novo.replace(antigo, novo)

                    if conteudo != conteudo_novo:
                        arquivo.write_text(conteudo_novo)
                        arquivos_modificados += 1

                except Exception as e:
                    print(f"   ⚠️  Erro em {arquivo.name}: {e}")

        print(f"   ✅ {arquivos_modificados} arquivos adaptados")

        # Renomear arquivos principais
        renames = [
            (destino / "chatbot_automaia_v4.py", destino / f"chatbot_{config['slug']}_v4.py"),
            (destino / "webhook_middleware_automaia.py", destino / f"webhook_middleware_{config['slug']}.py"),
            (destino / "chatwoot_config_automaia.json", destino / f"chatwoot_config_{config['slug']}.json"),
            (destino / "INICIAR_COM_NGROK.sh", destino / "INICIAR_COM_NGROK.sh"),  # Mantém nome
            (destino / "PARAR_BOT_AUTOMAIA.sh", destino / f"PARAR_BOT_{config['slug'].upper()}.sh")
        ]

        for old_path, new_path in renames:
            if old_path.exists() and old_path != new_path:
                old_path.rename(new_path)

        print("   ✅ Arquivos principais renomeados")

    def criar_config(self, config: Dict):
        """Gera chatwoot_config_<slug>.json"""

        print("\n4️⃣ Criando configuração...")

        config_file = config["dir_destino"] / f"chatwoot_config_{config['slug']}.json"

        config_data = {
            "chatwoot": {
                "url": "https://chatwoot.loop9.com.br",
                "token": "PREENCHER",
                "account_id": "1",
                "inbox_id": "PREENCHER"
            },
            "evolution": {
                "url": "https://evolution.loop9.com.br",
                "api_key": "PREENCHER",
                "instance": config["slug"]
            },
            "_comment_google_sheet_id": "ID da planilha Google Sheets agenda (criar com OAuth)",
            "google_sheet_id": "",
            "_comment_vendedor": "WhatsApp do vendedor para notificações",
            "whatsapp_vendedor": config["whatsapp_vendedor"]
        }

        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)

        print(f"   ✅ Config criado: {config_file.name}")
        print(f"   ⚠️  PREENCHER: Chatwoot token + inbox_id + Evolution API key")

    def criar_readme(self, config: Dict):
        """Cria README personalizado"""

        print("\n5️⃣ Gerando documentação...")

        readme = config["dir_destino"] / "README.md"

        conteudo = f"""# 🤖 Chatbot {config['nome_cliente']}

**Nicho:** {config['nicho']['nome']}
**Descrição:** {config['descricao']}

## 🚀 Setup Rápido

### 1. Configurar Chatwoot + Evolution

Edite `chatwoot_config_{config['slug']}.json`:
- Chatwoot token + inbox_id
- Evolution API key

### 2. Criar Agenda Google Sheets

```bash
# Autenticar OAuth (1x)
python3 componentes/escalonamento/autenticar_google.py

# Criar planilha
python3 componentes/escalonamento/criar_agenda_publica_oauth.py
```

### 3. Adicionar {config['nicho']['item_plural'].capitalize()}

Estrutura em `{config['nicho']['pasta_itens']}/`:

```
{config['nicho']['pasta_itens']}/
└── {config['nicho']['exemplo_item']}/
    ├── base.txt
    ├── detalhes.txt
    ├── faq.txt
    └── links.json
```

### 4. Iniciar Bot

```bash
./INICIAR_COM_NGROK.sh
```

## 🛠️ Componentes

- ✅ RAG Híbrido (keywords + semântico)
- ✅ 4 Ferramentas (lista_{config['nicho']['pasta_itens']}, consulta_faq, tagueamento, agendar_visita)
- ✅ Follow-ups automáticos
- ✅ Score de leads
- ✅ Escalonamento (notifica vendedor)
- ✅ Agenda Google Sheets
- ✅ Áudio (Whisper) + Imagem (GPT-4o)
- ✅ Métricas e relatórios

## 📊 Portas

- Bot: {config['porta_bot']}
- Middleware: {config['porta_middleware']}

## 🔧 Manutenção

```bash
# Ver logs
tail -f logs/chatbot_{config['slug']}.log

# Parar
./PARAR_BOT_{config['slug'].upper()}.sh && pkill -f ngrok

# Adicionar {config['nicho']['item_singular']}
# 1. Criar pasta em {config['nicho']['pasta_itens']}/
# 2. Preencher arquivos .txt
# 3. Upload fotos: python3 upload_fotos_{config['nicho']['pasta_itens']}.py
```

---

**Framework:** Chatbot Universal v1.0
**Baseado em:** whatsapp-chatbot-carros (Automaia)
"""

        readme.write_text(conteudo)
        print(f"   ✅ README criado")

    def resumo_final(self, config: Dict):
        """Mostra resumo e próximos passos"""

        print("\n" + "="*60)
        print("✅ CHATBOT CRIADO COM SUCESSO!")
        print("="*60)

        print(f"\n📁 Localização: {config['dir_destino']}")
        print(f"🤖 Nome: {config['nome_cliente']}")
        print(f"🎯 Nicho: {config['nicho']['nome']}")
        print(f"📂 Itens: {config['nicho']['pasta_itens']}/")
        print(f"🔌 Portas: {config['porta_bot']} (bot) | {config['porta_middleware']} (middleware)")

        print("\n" + "="*60)
        print("📋 PRÓXIMOS PASSOS:")
        print("="*60)

        print(f"""
1️⃣ Configurar APIs
   cd {config['dir_destino']}
   # Editar: chatwoot_config_{config['slug']}.json

2️⃣ Criar Agenda Google Sheets
   python3 componentes/escalonamento/autenticar_google.py
   python3 componentes/escalonamento/criar_agenda_publica_oauth.py

3️⃣ Adicionar {config['nicho']['item_plural'].capitalize()}
   # Criar pastas em {config['nicho']['pasta_itens']}/
   # Preencher arquivos .txt

4️⃣ Iniciar Bot
   ./INICIAR_COM_NGROK.sh

5️⃣ Verificar
   tail -f logs/chatbot_{config['slug']}.log
""")

        print("="*60)
        print("📖 Ver README.md para mais detalhes")
        print("="*60)
        print()

    def executar(self):
        """Executa todo o processo"""
        try:
            # Coletar informações
            config = self.coletar_informacoes()
            self.config = config

            # Confirmar
            print("\n" + "="*60)
            print("📋 RESUMO:")
            print("="*60)
            print(f"   Cliente: {config['nome_cliente']}")
            print(f"   Slug: {config['slug']}")
            print(f"   Nicho: {config['nicho']['nome']}")
            print(f"   Itens: {config['nicho']['pasta_itens']}/")
            print(f"   Portas: {config['porta_bot']}/{config['porta_middleware']}")
            print()

            confirma = input("Confirmar criação? (s/n): ")
            if confirma.lower() != 's':
                print("❌ Operação cancelada")
                return

            # Criar
            if not self.criar_estrutura(config):
                return

            self.adaptar_codigo(config)
            self.criar_config(config)
            self.criar_readme(config)

            # Resumo
            self.resumo_final(config)

        except KeyboardInterrupt:
            print("\n\n❌ Operação cancelada pelo usuário")
        except Exception as e:
            print(f"\n\n❌ Erro: {e}")
            import traceback
            traceback.print_exc()


def main():
    gerador = GeradorChatbot()
    gerador.executar()


if __name__ == "__main__":
    main()
