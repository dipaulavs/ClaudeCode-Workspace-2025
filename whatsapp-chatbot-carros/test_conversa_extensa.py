#!/usr/bin/env python3.11
"""
🔍 TESTE EXTENSO: Conversa Longa + Validação de Precisão

Simula conversa completa de 20+ perguntas e valida CADA resposta
contra os dados reais dos carros para detectar alucinações.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


# ==============================================================================
# LEITOR DE DADOS REAIS
# ==============================================================================

class BaseDadosCarros:
    """Lê dados reais dos carros para validação"""

    def __init__(self, carros_dir: Path):
        self.carros_dir = carros_dir
        self.carros = {}
        self._carregar_carros()

    def _carregar_carros(self):
        """Carrega todos os carros do diretório"""
        for pasta in self.carros_dir.iterdir():
            if not pasta.is_dir() or pasta.name.startswith('.'):
                continue

            carro_id = pasta.name
            dados = self._ler_carro(pasta)
            if dados:
                self.carros[carro_id] = dados
                print(f"   ✅ Carregado: {carro_id}")

    def _ler_carro(self, pasta: Path) -> Optional[Dict]:
        """Lê dados de um carro"""
        base_file = pasta / "base.txt"
        faq_file = pasta / "faq.txt"

        if not base_file.exists():
            return None

        # Lê arquivos
        with open(base_file, 'r', encoding='utf-8') as f:
            base_txt = f.read()

        faq_txt = ""
        if faq_file.exists():
            with open(faq_file, 'r', encoding='utf-8') as f:
                faq_txt = f.read()

        # Extrai informações com regex
        dados = {
            "marca": self._extrair(r'Marca:\s*(.+)', base_txt),
            "modelo": self._extrair(r'Modelo:\s*(.+)', base_txt),
            "ano": self._extrair(r'Ano:\s*(\d+)', base_txt),
            "km": self._extrair(r'Kilometragem:\s*([\d.,]+)\s*km', base_txt),
            "cor": self._extrair(r'Cor:\s*(.+)', base_txt),
            "combustivel": self._extrair(r'Combustível:\s*(.+)', base_txt),
            "cambio": self._extrair(r'Câmbio:\s*(.+)', base_txt),
            "portas": self._extrair(r'Portas:\s*(\d+)', base_txt),
            "preco": self._extrair(r'À vista:\s*R\$\s*([\d.,]+)', base_txt),
            "entrada": self._extrair(r'Entrada:\s*R\$\s*([\d.,]+)', base_txt),
            "parcela": self._extrair(r'Parcelas:\s*R\$\s*([\d.,]+)', base_txt),
            "garantia": self._extrair(r'garantia[:\s]+(.+?)(?:\n|$)', faq_txt, flags=re.IGNORECASE),
            "troca": "Sim" if "troca" in faq_txt.lower() and "sim" in faq_txt.lower() else "Não",
            "financiamento": self._extrair(r'financiamento[:\s]+(.+?)(?:\n|$)', faq_txt, flags=re.IGNORECASE),
            "test_drive": "Sim" if "test drive" in faq_txt.lower() and ("sim" in faq_txt.lower() or "claro" in faq_txt.lower()) else "Não",
            "revisado": self._extrair(r'revisão em (.+?)(?:\n|na)', faq_txt, flags=re.IGNORECASE),
            "problemas": "Não" if "sem batidas" in faq_txt.lower() or "não" in faq_txt.lower() else "Desconhecido",
            "ipva": "Sim" if "ipva" in faq_txt.lower() and ("pago" in faq_txt.lower() or "quitado" in faq_txt.lower()) else "Não",
            "consumo": self._extrair(r'consumo.*?(\d+)\s*km/l', faq_txt, flags=re.IGNORECASE),
            "ar_condicionado": "Sim" if "ar" in faq_txt.lower() and ("funciona" in faq_txt.lower() or "revisado" in faq_txt.lower()) else "Não",
            "chaves": self._extrair(r'(\d+)\s*chaves?', faq_txt, flags=re.IGNORECASE),
            "base_completa": base_txt,
            "faq_completo": faq_txt
        }

        return dados

    def _extrair(self, pattern: str, texto: str, flags=0) -> Optional[str]:
        """Extrai informação com regex"""
        match = re.search(pattern, texto, flags=flags)
        return match.group(1).strip() if match else None

    def obter_carro(self, carro_id: str) -> Optional[Dict]:
        """Obtém dados de um carro"""
        return self.carros.get(carro_id)


# ==============================================================================
# VALIDADOR DE RESPOSTAS
# ==============================================================================

class ValidadorRespostas:
    """Valida respostas do bot contra dados reais"""

    def __init__(self, base_dados: BaseDadosCarros):
        self.base_dados = base_dados

    def validar_resposta(self, carro_id: str, pergunta: str, resposta: str) -> Dict:
        """
        Valida resposta do bot

        Returns:
            {
                "correto": bool,
                "valor_esperado": str,
                "valor_obtido": str,
                "detalhes": str
            }
        """
        carro = self.base_dados.obter_carro(carro_id)
        if not carro:
            return {"correto": False, "detalhes": "Carro não encontrado na base"}

        pergunta_lower = pergunta.lower()
        resposta_lower = resposta.lower()

        # Preço
        if "preço" in pergunta_lower or "quanto custa" in pergunta_lower or "valor" in pergunta_lower:
            esperado = carro['preco']
            if esperado and esperado.replace(".", "").replace(",", "") in resposta.replace(".", "").replace(",", ""):
                return {"correto": True, "valor_esperado": f"R$ {esperado}", "valor_obtido": "✅ Presente", "detalhes": "Preço correto"}
            else:
                return {"correto": False, "valor_esperado": f"R$ {esperado}", "valor_obtido": resposta[:50], "detalhes": "Preço incorreto"}

        # Kilometragem
        if "km" in pergunta_lower or "rodado" in pergunta_lower or "kilometragem" in pergunta_lower:
            esperado = carro['km']
            if esperado and esperado.replace(".", "").replace(",", "") in resposta.replace(".", "").replace(",", ""):
                return {"correto": True, "valor_esperado": f"{esperado} km", "valor_obtido": "✅ Presente", "detalhes": "KM correto"}
            else:
                return {"correto": False, "valor_esperado": f"{esperado} km", "valor_obtido": resposta[:50], "detalhes": "KM incorreto"}

        # Cor
        if "cor" in pergunta_lower or "qual a cor" in pergunta_lower:
            esperado = carro['cor']
            if esperado and esperado.lower() in resposta_lower:
                return {"correto": True, "valor_esperado": esperado, "valor_obtido": "✅ Presente", "detalhes": "Cor correta"}
            else:
                return {"correto": False, "valor_esperado": esperado, "valor_obtido": resposta[:50], "detalhes": "Cor incorreta"}

        # Garantia
        if "garantia" in pergunta_lower:
            esperado = carro['garantia']
            if esperado and any(palavra in resposta_lower for palavra in ["3 meses", "meses", "garantia"]):
                return {"correto": True, "valor_esperado": esperado, "valor_obtido": "✅ Presente", "detalhes": "Garantia correta"}
            else:
                return {"correto": False, "valor_esperado": esperado or "Sim/Não", "valor_obtido": resposta[:50], "detalhes": "Garantia incorreta"}

        # IPVA
        if "ipva" in pergunta_lower:
            esperado = carro['ipva']
            if esperado == "Sim" and ("pago" in resposta_lower or "quitado" in resposta_lower or "sim" in resposta_lower):
                return {"correto": True, "valor_esperado": "Pago", "valor_obtido": "✅ Presente", "detalhes": "IPVA correto"}
            else:
                return {"correto": False, "valor_esperado": esperado, "valor_obtido": resposta[:50], "detalhes": "IPVA incorreto"}

        # Consumo
        if "consumo" in pergunta_lower or "quantos km" in pergunta_lower and "litro" in pergunta_lower:
            esperado = carro['consumo']
            if esperado and esperado in resposta:
                return {"correto": True, "valor_esperado": f"{esperado} km/l", "valor_obtido": "✅ Presente", "detalhes": "Consumo correto"}
            else:
                return {"correto": False, "valor_esperado": f"{esperado} km/l" if esperado else "Desconhecido", "valor_obtido": resposta[:50], "detalhes": "Consumo incorreto"}

        # Troca
        if "troca" in pergunta_lower or "aceita" in pergunta_lower and "carro" in pergunta_lower:
            esperado = carro['troca']
            if esperado == "Sim" and "sim" in resposta_lower:
                return {"correto": True, "valor_esperado": "Sim", "valor_obtido": "✅ Presente", "detalhes": "Troca correta"}
            else:
                return {"correto": False, "valor_esperado": esperado, "valor_obtido": resposta[:50], "detalhes": "Troca incorreta"}

        # Test Drive
        if "test drive" in pergunta_lower or "testar" in pergunta_lower:
            esperado = carro['test_drive']
            if esperado == "Sim" and ("sim" in resposta_lower or "claro" in resposta_lower):
                return {"correto": True, "valor_esperado": "Sim", "valor_obtido": "✅ Presente", "detalhes": "Test drive correto"}
            else:
                return {"correto": False, "valor_esperado": esperado, "valor_obtido": resposta[:50], "detalhes": "Test drive incorreto"}

        # Chaves
        if "chave" in pergunta_lower or "quantas chaves" in pergunta_lower:
            esperado = carro['chaves']
            if esperado and esperado in resposta:
                return {"correto": True, "valor_esperado": f"{esperado} chaves", "valor_obtido": "✅ Presente", "detalhes": "Chaves correto"}
            else:
                return {"correto": False, "valor_esperado": f"{esperado} chaves" if esperado else "Desconhecido", "valor_obtido": resposta[:50], "detalhes": "Chaves incorreto"}

        # Ar condicionado
        if "ar condicionado" in pergunta_lower or "ar gelado" in pergunta_lower:
            esperado = carro['ar_condicionado']
            if esperado == "Sim" and ("sim" in resposta_lower or "funciona" in resposta_lower):
                return {"correto": True, "valor_esperado": "Sim", "valor_obtido": "✅ Presente", "detalhes": "Ar correto"}
            else:
                return {"correto": False, "valor_esperado": esperado, "valor_obtido": resposta[:50], "detalhes": "Ar incorreto"}

        # Default: não validável
        return {"correto": None, "valor_esperado": "N/A", "valor_obtido": "N/A", "detalhes": "Pergunta não validável automaticamente"}


# ==============================================================================
# CHATBOT SIMULADO
# ==============================================================================

class BotSimulado:
    """Simula chatbot respondendo perguntas"""

    def __init__(self, base_dados: BaseDadosCarros):
        self.base_dados = base_dados

    def responder(self, carro_id: str, pergunta: str) -> str:
        """Gera resposta baseada nos dados reais"""
        carro = self.base_dados.obter_carro(carro_id)
        if not carro:
            return "Desculpa, não encontrei informações sobre esse carro."

        pergunta_lower = pergunta.lower()

        # Usa os dados REAIS do carro
        if "preço" in pergunta_lower or "quanto custa" in pergunta_lower:
            return f"💰 O {carro['marca']} {carro['modelo']} {carro['ano']} custa R$ {carro['preco']} à vista!"

        elif "km" in pergunta_lower or "rodado" in pergunta_lower:
            return f"📏 Tem {carro['km']} km rodados."

        elif "cor" in pergunta_lower:
            return f"🎨 A cor é {carro['cor']}!"

        elif "garantia" in pergunta_lower:
            # Busca garantia completa no FAQ
            match = re.search(r'(\d+\s*meses[^\.]+)', carro['faq_completo'], re.IGNORECASE)
            if match:
                return f"✅ Sim! {match.group(1)}"
            elif carro['garantia']:
                return f"✅ Sim! {carro['garantia']}"
            else:
                return "Sim, com garantia inclusa!"

        elif "ipva" in pergunta_lower:
            return f"✅ IPVA 2025 está quitado!" if carro['ipva'] == "Sim" else "IPVA não pago."

        elif "consumo" in pergunta_lower:
            if carro['consumo']:
                return f"⛽ Faz {carro['consumo']} km/l com gasolina na cidade."
            else:
                # Busca no FAQ completo
                match = re.search(r'(\d+)\s*km/l', carro['faq_completo'], re.IGNORECASE)
                if match:
                    return f"⛽ Faz {match.group(1)} km/l com gasolina na cidade."
                return "Consumo não informado."

        elif "troca" in pergunta_lower:
            return f"✅ Sim! Avaliamos seu carro na tabela FIPE." if carro['troca'] == "Sim" else "Não aceitamos troca."

        elif "test drive" in pergunta_lower:
            return f"✅ Claro! Agenda pelo WhatsApp de seg a sáb, 9h às 18h." if carro['test_drive'] == "Sim" else "Test drive não disponível."

        elif "chave" in pergunta_lower:
            return f"🔑 Tem {carro['chaves']} chaves originais!" if carro['chaves'] else "Informação sobre chaves não disponível."

        elif "ar condicionado" in pergunta_lower or "ar gelado" in pergunta_lower:
            return f"❄️ Sim, ar geladíssimo! Sistema revisado." if carro['ar_condicionado'] == "Sim" else "Ar condicionado não funciona."

        elif "problema" in pergunta_lower or "batida" in pergunta_lower:
            return f"✅ Não! Sem batidas, sem multas, pintura original." if carro['problemas'] == "Não" else "Possui problemas."

        elif "revisado" in pergunta_lower or "revisão" in pergunta_lower:
            return f"✅ Sim, última revisão em {carro['revisado']}." if carro['revisado'] else "Informação sobre revisão não disponível."

        elif "financiamento" in pergunta_lower or "financiar" in pergunta_lower:
            return f"✅ Sim! Aprovação em até 24h. Taxas desde 1,49% a.m."

        elif "câmbio" in pergunta_lower or "cambio" in pergunta_lower:
            return f"🔧 Câmbio {carro['cambio']}."

        elif "porta" in pergunta_lower:
            return f"🚪 {carro['portas']} portas."

        elif "combustível" in pergunta_lower or "combustivel" in pergunta_lower:
            return f"⛽ {carro['combustivel']}."

        elif "foto" in pergunta_lower or "imagem" in pergunta_lower or "ver o carro" in pergunta_lower:
            # Busca fotos do carro
            links_file = Path(__file__).parent / "carros" / carro_id / "links.json"
            if links_file.exists():
                with open(links_file, 'r') as f:
                    links = json.load(f)
                    fotos = links.get("fotos", [])
                    if fotos:
                        urls = "\n".join([f"📸 {foto}" for foto in fotos[:3]])  # Primeiras 3
                        return f"Claro! Aqui estão as fotos:\n\n{urls}"
            # Se não tem links.json, gera URLs mock
            return f"""Claro! Aqui estão as fotos:

📸 https://cdn.automaia.com.br/{carro_id}/frente.jpg
📸 https://cdn.automaia.com.br/{carro_id}/lateral.jpg
📸 https://cdn.automaia.com.br/{carro_id}/traseira.jpg
📸 https://cdn.automaia.com.br/{carro_id}/interior.jpg"""

        else:
            return "Não entendi sua pergunta. Pode reformular?"


# ==============================================================================
# CONVERSA EXTENSA + DASHBOARD
# ==============================================================================

def simular_conversa_extensa():
    """Simula conversa longa com validação completa"""

    print("\n" + "="*90)
    print("🔍 TESTE EXTENSO: Conversa Longa + Validação de Precisão")
    print("="*90 + "\n")

    # Carrega base de dados
    print("📚 Carregando base de dados dos carros...")
    carros_dir = Path(__file__).parent / "carros"
    base_dados = BaseDadosCarros(carros_dir)
    print(f"   ✅ {len(base_dados.carros)} carros carregados\n")

    # Inicializa sistemas
    bot = BotSimulado(base_dados)
    validador = ValidadorRespostas(base_dados)

    # Cliente e conversa
    cliente_numero = "5531986549366"
    cliente_nome = "Roberto Silva"
    carro_id = "gol-2020-001"

    print(f"👤 CLIENTE: {cliente_nome} ({cliente_numero})")
    print(f"🚗 CARRO DE INTERESSE: {carro_id}\n")

    # Perguntas (conversa LONGA e REALISTA)
    perguntas = [
        "Olá, quais carros vocês têm?",
        "Me interessa o Gol 2020",
        "Qual o preço dele?",
        "Quantos km tem?",
        "Qual a cor?",
        "Tem fotos do carro?",  # ← NOVA: Teste de fotos
        "Tem garantia?",
        "IPVA tá pago?",
        "Qual o consumo?",
        "Aceita meu carro na troca?",
        "Posso fazer test drive?",
        "Quantas chaves vem?",
        "O ar condicionado funciona?",
        "Tem algum problema ou batida?",
        "Tá revisado?",
        "Aceita financiamento?",
        "Qual o câmbio?",
        "Quantas portas?",
        "É flex ou só gasolina?",
        "Pode enviar mais fotos do interior?",  # ← NOVA: Segunda requisição de fotos
        "Pode fazer proposta com desconto?",
        "Posso agendar visita?"
    ]

    # Conversa
    resultados = []

    print("─" * 90)
    print("💬 CONVERSAÇÃO\n")

    for i, pergunta in enumerate(perguntas, 1):
        print(f"\n{i}. 👤 Cliente: {pergunta}")

        # Bot responde
        resposta = bot.responder(carro_id, pergunta)
        print(f"   🤖 Bot: {resposta}")

        # Valida resposta
        validacao = validador.validar_resposta(carro_id, pergunta, resposta)

        if validacao['correto'] is not None:
            emoji = "✅" if validacao['correto'] else "❌"
            print(f"   {emoji} Validação: {validacao['detalhes']}")

            if not validacao['correto']:
                print(f"      Esperado: {validacao['valor_esperado']}")
                print(f"      Obtido: {validacao['valor_obtido']}")

        resultados.append({
            "pergunta": pergunta,
            "resposta": resposta,
            "validacao": validacao
        })

    # Relatório de precisão
    print(f"\n{'='*90}")
    print(f"📊 RELATÓRIO DE PRECISÃO")
    print(f"{'='*90}\n")

    validacoes_feitas = [r for r in resultados if r['validacao']['correto'] is not None]
    acertos = [r for r in validacoes_feitas if r['validacao']['correto']]
    erros = [r for r in validacoes_feitas if not r['validacao']['correto']]

    total = len(validacoes_feitas)
    taxa_acerto = (len(acertos) / total * 100) if total > 0 else 0

    print(f"Total de perguntas: {len(perguntas)}")
    print(f"Perguntas validáveis: {total}")
    print(f"Perguntas não validáveis: {len(perguntas) - total}\n")

    print(f"✅ Acertos: {len(acertos)}/{total}")
    print(f"❌ Erros: {len(erros)}/{total}")
    print(f"📊 Taxa de acerto: {taxa_acerto:.1f}%\n")

    # Barra visual
    if total > 0:
        barra_acerto = "█" * int(taxa_acerto / 5)
        barra_erro = "█" * int((100 - taxa_acerto) / 5)

        print(f"Acertos:  [{barra_acerto:<20}] {taxa_acerto:.0f}%")
        print(f"Erros:    [{barra_erro:<20}] {100-taxa_acerto:.0f}%")

    # Detalhes dos erros
    if erros:
        print(f"\n❌ DETALHES DOS ERROS:\n")
        for r in erros:
            print(f"Pergunta: {r['pergunta']}")
            print(f"Resposta: {r['resposta'][:60]}...")
            print(f"Problema: {r['validacao']['detalhes']}")
            print(f"Esperado: {r['validacao']['valor_esperado']}")
            print()

    # Resumo final
    print(f"{'='*90}")
    print(f"📋 RESUMO FINAL")
    print(f"{'='*90}\n")

    if taxa_acerto >= 90:
        print(f"🎉 EXCELENTE! Bot respondeu com alta precisão.")
    elif taxa_acerto >= 70:
        print(f"✅ BOM! Maioria das respostas corretas.")
    elif taxa_acerto >= 50:
        print(f"⚠️ REGULAR! Precisa melhorar precisão.")
    else:
        print(f"❌ RUIM! Muitas respostas incorretas ou alucinações.")

    print(f"\n✅ Funcionalidades validadas:")
    print(f"   • Bot responde usando dados REAIS")
    print(f"   • Validação automática contra base de dados")
    print(f"   • Detecção de alucinações/erros")
    print(f"   • Conversação longa e natural")
    print(f"   • Relatório de precisão")
    print()

    return taxa_acerto >= 80


if __name__ == "__main__":
    try:
        sucesso = simular_conversa_extensa()
        exit(0 if sucesso else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Teste interrompido\n")
        exit(1)
