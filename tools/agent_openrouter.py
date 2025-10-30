#!/usr/bin/env python3
"""
Gerenciador de Agentes via OpenRouter API
Permite criar e usar subagentes especializados sem carregar instruções no Claude Code
"""

import json
import requests
import sys
import os
from pathlib import Path

class OpenRouterAgent:
    def __init__(self, config_path=None):
        """Inicializa o agente com configurações da OpenRouter"""
        if config_path is None:
            workspace = Path(__file__).parent.parent
            config_path = workspace / "agentes" / "openrouter" / "config.json"

        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.api_key = self.config['api_key']
        self.api_endpoint = self.config['api_endpoint']
        self.default_model = self.config.get('default_model', 'anthropic/claude-3.5-sonnet')
        self.site_url = self.config.get('site_url', '')
        self.site_name = self.config.get('site_name', 'Claude Code Workspace')

    def load_agent_instructions(self, agent_name):
        """Carrega as instruções de um agente específico"""
        workspace = Path(__file__).parent.parent
        agent_path = workspace / "agentes" / "openrouter" / f"{agent_name}.md"

        if not agent_path.exists():
            raise FileNotFoundError(f"Agente '{agent_name}' não encontrado em: {agent_path}")

        with open(agent_path, 'r', encoding='utf-8') as f:
            return f.read()

    def call_agent(self, agent_name, user_input, model=None, temperature=0.7, max_tokens=8000):
        """
        Chama um agente específico via OpenRouter

        Args:
            agent_name: Nome do arquivo do agente (sem .md)
            user_input: Input/tarefa do usuário
            model: Modelo a usar (opcional, usa default do config)
            temperature: Criatividade (0-1)
            max_tokens: Máximo de tokens na resposta

        Returns:
            Resposta do agente
        """
        # Carrega as instruções do sistema do agente
        system_instructions = self.load_agent_instructions(agent_name)

        # Prepara os headers
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Adiciona headers opcionais para atribuição
        if self.site_url:
            headers["HTTP-Referer"] = self.site_url
        if self.site_name:
            headers["X-Title"] = self.site_name

        # Prepara a requisição
        payload = {
            "model": model or self.default_model,
            "messages": [
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": user_input}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        # Faz a chamada à API
        try:
            response = requests.post(
                self.api_endpoint,
                headers=headers,
                json=payload,
                timeout=300
            )
            response.raise_for_status()

            result = response.json()
            return result['choices'][0]['message']['content']

        except requests.exceptions.RequestException as e:
            return f"Erro na chamada da API: {str(e)}"
        except (KeyError, IndexError) as e:
            return f"Erro ao processar resposta: {str(e)}\nResposta completa: {result}"

def list_agents():
    """Lista todos os agentes disponíveis"""
    workspace = Path(__file__).parent.parent
    agents_dir = workspace / "agentes" / "openrouter"

    agents = [f.stem for f in agents_dir.glob("*.md") if f.stem != "README"]
    return agents

def main():
    # Lista agentes se solicitado (verificar antes de validar argumentos)
    if '--list' in sys.argv:
        agents = list_agents()
        print("\n📋 Agentes disponíveis:")
        for agent in agents:
            print(f"  • {agent}")
        print(f"\nTotal: {len(agents)} agentes")
        sys.exit(0)

    # Validar argumentos
    if len(sys.argv) < 3:
        # Carrega config para mostrar modelos favoritos
        try:
            workspace = Path(__file__).parent.parent
            config_path = workspace / "agentes" / "openrouter" / "config.json"
            with open(config_path, 'r') as f:
                config = json.load(f)
            default_model = config.get('default_model', 'anthropic/claude-haiku-4.5')
            favorite_models = config.get('favorite_models', [])
        except:
            default_model = 'anthropic/claude-haiku-4.5'
            favorite_models = []

        print("Uso: python3 agent_openrouter.py <agente> <input> [--model MODEL] [--temp TEMP]")
        print("\nExemplo:")
        print('  python3 agent_openrouter.py copywriter-vendas "Crie um título para produto de emagrecimento"')
        print('\nOpções:')
        print('  --model    Modelo a usar')
        print('  --temp     Temperature 0-1 (default: 0.7)')
        print('  --list     Lista agentes disponíveis')

        if favorite_models:
            print(f'\nSeus modelos favoritos (default: {default_model}):')
            for model in favorite_models:
                if model == default_model:
                    print(f'  • {model} ⭐')
                else:
                    print(f'  • {model}')

        sys.exit(1)

    agent_name = sys.argv[1]
    user_input = sys.argv[2]

    # Parse argumentos opcionais
    model = None
    temperature = 0.7

    if '--model' in sys.argv:
        idx = sys.argv.index('--model')
        model = sys.argv[idx + 1]

    if '--temp' in sys.argv:
        idx = sys.argv.index('--temp')
        temperature = float(sys.argv[idx + 1])

    # Inicializa e chama o agente
    try:
        agent = OpenRouterAgent()
        print(f"\n🤖 Chamando agente '{agent_name}'...")
        print(f"📝 Modelo: {model or agent.default_model}")
        print(f"🌡️  Temperature: {temperature}\n")
        print("─" * 60)

        response = agent.call_agent(agent_name, user_input, model, temperature)

        print(response)
        print("─" * 60)
        print(f"\n✅ Resposta concluída")

    except FileNotFoundError as e:
        print(f"\n❌ Erro: {e}")
        print("\nAgentes disponíveis:")
        for agent in list_agents():
            print(f"  • {agent}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
