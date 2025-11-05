#!/usr/bin/env python3
"""
✅ VALIDADOR DE CONFIGURAÇÃO - chatbot-template/

Verifica se todas as API keys estão configuradas corretamente.
Identifica chaves faltantes, inválidas ou hardcoded.
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

class ValidadorConfig:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.erros = []
        self.avisos = []
        self.sucesso = []

    def linha_separadora(self, title=""):
        print("\n" + "=" * 70)
        if title:
            print(f"  {title}")
            print("=" * 70)

    def validar_json_config(self) -> bool:
        """Valida chatwoot_config_automaia.json"""
        self.linha_separadora("1. Validando chatwoot_config_automaia.json")

        config_file = self.root_dir / "chatwoot_config_automaia.json"

        if not config_file.exists():
            self.erros.append(f"❌ Arquivo não encontrado: {config_file}")
            return False

        try:
            with open(config_file, 'r') as f:
                config = json.load(f)

            # Validar Chatwoot
            print("\n📋 Chatwoot Config:")
            campos_chatwoot = ["url", "token", "account_id", "inbox_id"]
            for campo in campos_chatwoot:
                valor = config.get("chatwoot", {}).get(campo, "")
                if not valor:
                    self.erros.append(f"   ❌ chatwoot.{campo} vazio ou faltando")
                else:
                    self.sucesso.append(f"   ✅ chatwoot.{campo}: OK")

            # Validar Evolution
            print("\n🐳 Evolution Config:")
            campos_evolution = ["url", "api_key", "instance"]
            for campo in campos_evolution:
                valor = config.get("evolution", {}).get(campo, "")
                if not valor:
                    self.erros.append(f"   ❌ evolution.{campo} vazio ou faltando")
                else:
                    self.sucesso.append(f"   ✅ evolution.{campo}: OK")

            # Validar Google Sheet (opcional)
            print("\n📊 Google Sheets Config (OPCIONAL):")
            google_id = config.get("google_sheet_id", "")
            if google_id:
                self.sucesso.append(f"   ✅ google_sheet_id: {google_id}")
            else:
                self.avisos.append("   ⚠️  google_sheet_id não configurado (usando horários MOCK)")

            return len(self.erros) == 0

        except json.JSONDecodeError as e:
            self.erros.append(f"❌ Erro ao parsear JSON: {e}")
            return False
        except Exception as e:
            self.erros.append(f"❌ Erro ao ler arquivo: {e}")
            return False

    def validar_openai_openrouter(self) -> bool:
        """Valida se OpenAI e OpenRouter estão hardcoded"""
        self.linha_separadora("2. Validando OpenAI e OpenRouter")

        chatbot_file = self.root_dir / "chatbot_automaia_v4.py"

        if not chatbot_file.exists():
            self.avisos.append("⚠️  chatbot_automaia_v4.py não encontrado (pode estar deletado)")
            return True

        with open(chatbot_file, 'r') as f:
            content = f.read()

        # Procura por hardcoded keys
        if "OPENAI_API_KEY = \"sk-" in content:
            self.avisos.append("⚠️  OPENAI_API_KEY está HARDCODED em chatbot_automaia_v4.py:41")
            self.avisos.append("   Recomendação: Mover para .env")
        else:
            self.sucesso.append("✅ OPENAI_API_KEY não hardcoded")

        if "OPENROUTER_API_KEY = \"sk-" in content:
            self.avisos.append("⚠️  OPENROUTER_API_KEY está HARDCODED em chatbot_automaia_v4.py:40")
            self.avisos.append("   Recomendação: Mover para .env")
        else:
            self.sucesso.append("✅ OPENROUTER_API_KEY não hardcoded")

        # Procura por Redis hardcoded
        if "Redis(" in content and "url=" in content:
            self.avisos.append("⚠️  Redis credentials podem estar HARDCODED em chatbot_automaia_v4.py:56-57")
            self.avisos.append("   Recomendação: Mover para .env")
        else:
            self.sucesso.append("✅ Redis não aparenta estar hardcoded")

        return True

    def validar_redis_followup(self) -> bool:
        """Valida Redis em sistema_followup.py"""
        self.linha_separadora("3. Validando Redis em sistema_followup.py")

        followup_file = self.root_dir / "componentes/followup/sistema_followup.py"

        if not followup_file.exists():
            self.avisos.append("⚠️  sistema_followup.py não encontrado")
            return True

        with open(followup_file, 'r') as f:
            content = f.read()

        # Procura por hardcoded Redis
        if "REDIS_HOST = " in content and "usw1-popular" in content:
            self.avisos.append("⚠️  Redis credentials HARDCODED em sistema_followup.py:16-22")
            self.avisos.append("   Recomendação: Mover para .env")
        elif "REDIS_HOST = " in content:
            self.avisos.append("⚠️  REDIS_HOST hardcoded (verifique sistema_followup.py:16)")
        else:
            self.sucesso.append("✅ Redis em followup não aparenta estar hardcoded")

        if "EVOLUTION_API_KEY = " in content and "6C60BE7E" in content:
            self.avisos.append("⚠️  Evolution API Key HARDCODED em sistema_followup.py:22")
            self.avisos.append("   Recomendação: Mover para chatwoot_config_automaia.json")

        return True

    def validar_google_credentials(self) -> bool:
        """Valida Google Credentials"""
        self.linha_separadora("4. Validando Google OAuth Credentials")

        google_creds = self.root_dir / "componentes/escalonamento/config/google_credentials.json"

        if not google_creds.exists():
            self.avisos.append("⚠️  google_credentials.json não encontrado")
            self.avisos.append("   Ação: Executar `python3 componentes/escalonamento/autenticar_google.py`")
            return True

        try:
            with open(google_creds, 'r') as f:
                creds = json.load(f)

            required_fields = ["client_id", "client_secret", "auth_uri", "token_uri"]
            web_config = creds.get("web", {})

            for field in required_fields:
                if field in web_config:
                    self.sucesso.append(f"   ✅ Google {field}: OK")
                else:
                    self.erros.append(f"   ❌ Google {field}: faltando")

        except Exception as e:
            self.avisos.append(f"⚠️  Erro ao ler google_credentials.json: {e}")

        return True

    def validar_produtos(self) -> bool:
        """Valida se há dados de produtos"""
        self.linha_separadora("5. Validando Dados dos Produtos")

        produtos_dir = self.root_dir / "carros"

        if not produtos_dir.exists():
            self.avisos.append("⚠️  Diretório 'carros' não encontrado")
            return True

        produtos = [d for d in produtos_dir.iterdir() if d.is_dir()]

        if not produtos:
            self.avisos.append("⚠️  Nenhum produto encontrado em ./carros")
            return True

        self.sucesso.append(f"✅ {len(produtos)} produto(s) encontrado(s) em ./carros")

        for produto in produtos[:3]:  # Validar primeiros 3
            links_file = produto / "links.json"
            if links_file.exists():
                self.sucesso.append(f"   ✅ {produto.name}/links.json: OK")
            else:
                self.avisos.append(f"   ⚠️  {produto.name}/links.json: faltando")

        return True

    def gerar_relatorio(self) -> Dict[str, List]:
        """Gera relatório completo"""
        print("\n")
        self.validar_json_config()
        self.validar_openai_openrouter()
        self.validar_redis_followup()
        self.validar_google_credentials()
        self.validar_produtos()

        return {
            "erros": self.erros,
            "avisos": self.avisos,
            "sucessos": self.sucesso
        }

    def exibir_resumo(self, relatorio: Dict[str, List]):
        """Exibe resumo final"""
        self.linha_separadora("RESUMO FINAL")

        print("\n✅ SUCESSOS:")
        for msg in self.sucesso:
            print(msg)

        if self.avisos:
            print("\n⚠️  AVISOS:")
            for msg in self.avisos:
                print(msg)

        if self.erros:
            print("\n❌ ERROS:")
            for msg in self.erros:
                print(msg)

        # Status final
        print("\n" + "=" * 70)
        if self.erros:
            print("🔴 STATUS: FALHA - Configure os itens com ❌ acima")
            return False
        elif self.avisos:
            print("🟡 STATUS: AVISO - Alguns itens opcionais não configurados")
            return True
        else:
            print("🟢 STATUS: OK - Tudo configurado!")
            return True
        print("=" * 70 + "\n")

    def gerar_json_relatorio(self):
        """Gera relatório em JSON"""
        relatorio = self.gerar_relatorio()

        json_file = self.root_dir / "validacao_config.json"
        with open(json_file, 'w') as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)

        print(f"\n📄 Relatório salvo em: {json_file}")

        return relatorio


def main():
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║        🤖 VALIDADOR DE CONFIGURAÇÃO - chatbot-template         ║
    ║                                                                ║
    ║  Verifica: APIs, Keys, Arquivos de Config, Credenciais       ║
    ╚════════════════════════════════════════════════════════════════╝
    """)

    validador = ValidadorConfig()
    relatorio = validador.gerar_relatorio()
    status = validador.exibir_resumo(relatorio)

    return 0 if status else 1


if __name__ == "__main__":
    sys.exit(main())
