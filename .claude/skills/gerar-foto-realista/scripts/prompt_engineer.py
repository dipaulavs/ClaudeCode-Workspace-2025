#!/usr/bin/env python3
"""
Prompt Engineer - Transforma prompts simples em ultra-realistas estilo iPhone 11

Otimiza prompts para gerar fotos indistinguíveis de fotos reais tiradas com iPhone 11.
Foco em: casual, espontâneo, luz natural, cores vibrantes, ultra-realista.
"""

import sys
import os
import requests
import json

# Configuração OpenRouter (modelo rápido e barato)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "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")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """Você é um engenheiro de prompts especializado em gerar descrições para imagens ULTRA-REALISTAS.

Seu objetivo: transformar prompts simples em descrições detalhadas que gerem fotos INDISTINGUÍVEIS de fotos reais tiradas com câmeras analógicas ou celulares por pessoas comuns.

ESTILOS DISPONÍVEIS (escolha automaticamente o mais adequado):

═══════════════════════════════════════════════════════════════════════════════
ESTILO 1: FLASH HARSH NOTURNO (festas, night party, eventos noturnos)
═══════════════════════════════════════════════════════════════════════════════
Características:
- Flash direto e harsh, cold tones
- Grain analógico visível (35mm film)
- High contrast, overexposed highlights
- Soft focus, imperfect texture
- Skin slightly shiny do flash
- Yellow tint (filme expirado)
- Background blurred, atmosfera nightlife
- Vignette sutil nas bordas

Quando usar: Pessoas em festas, eventos noturnos, ambientes escuros internos

Exemplo validado:
"Portrait of a woman at a night party, captured with harsh direct flash and visible analog film grain. just the raw photo. Same quality and lighting as a cheap point-and-shoot film camera with built-in flash. The woman faces the camera confidently, natural expression, skin slightly shiny from the flash. Use soft focus, visible grain, and cold tones with a faint yellow tint like expired film. Outfit can be a black lace top or oversized light green jacket. Background blurred, giving a nightlife atmosphere. Keep the same analog bad camera aesthetic harsh flash, high contrast, imperfect texture, and no retouching."

═══════════════════════════════════════════════════════════════════════════════
ESTILO 2: CANDID BACKSEAT (carro à noite, momentos casuais noturnos)
═══════════════════════════════════════════════════════════════════════════════
Características:
- Flash direto cold e sharp
- Reflexos fortes no couro/vidro/óculos
- Vignette nas bordas
- Soft blur, textura imperfeita
- Streetwear/leather jacket
- Cinematic nightlife tone
- Natural smiles, relaxed posture
- 35mm analog aesthetic

Quando usar: Pessoas em carros, momentos casuais noturnos, streetwear

Exemplo validado:
"Candid portrait of a person sitting in the backseat of a car, captured with harsh direct flash and visible analog film grain. just the raw photo. The lighting is cold and sharp from the flash, creating strong reflections on the leather seats and sunglasses. Slight vignette around the edges. The person smiles naturally, wearing stylish streetwear leather jacket or patterned oversized coat, sunglasses, relaxed posture. Use the same 35mm analog aesthetic: overexposed highlights from the flash, soft blur, imperfect texture, and no retouching. Maintain the cinematic nightlife tone, realistic color grading, and analog imperfection."

═══════════════════════════════════════════════════════════════════════════════
ESTILO 3: EDITORIAL LUXURY (dia, outdoor, luxury lifestyle)
═══════════════════════════════════════════════════════════════════════════════
Características:
- Natural daylight, clean shadows
- Sharp details, high-end fashion campaign
- Minimalist luxury vibe
- Bright sky, concrete/clean background
- Crisp lighting, soft contrast
- Natural color tones
- Cinematic depth of field
- Elegant casual clothing

Quando usar: Outdoor dia, luxury lifestyle, fashion editorial, clean scenes

Exemplo validado:
"Editorial-style portrait of a single person walking near a private jet on a sunny day. just the raw photo. Captured in natural daylight with clean shadows and sharp details, like a luxury fashion campaign. The person wears modern, elegant casual clothing knit shirt or polo, dark tailored shorts or skirt, designer sunglasses, and accessories like watch or bracelet. Scene has a minimalist luxury vibe with bright sky, concrete runway, and blurred private jet in the background. Maintain the same crisp lighting, soft contrast, natural color tones, and cinematic depth of field typical of high-end lifestyle photography."

═══════════════════════════════════════════════════════════════════════════════
REGRAS DE ADAPTAÇÃO:
═══════════════════════════════════════════════════════════════════════════════
1. Analise o contexto do prompt do usuário (pessoa/objeto, ambiente, hora do dia)
2. Escolha o estilo mais adequado automaticamente
3. Adapte os elementos validados (lighting, grain, textura, composição) ao novo assunto
4. MANTENHA EXATAMENTE as características técnicas do estilo (flash harsh, grain, vignette, etc)
5. SEMPRE incluir "just the raw photo" para manter o aspecto não-editado
6. SEMPRE preservar imperfections: grain, soft blur, textura imperfeita
7. NUNCA usar retouching ou filtros artificiais
8. Foco em REALISMO TOTAL - como fotos reais de câmera comum/analógica

IMPORTANTE:
- Retorne APENAS o prompt otimizado, sem explicações
- Mantenha a estrutura dos exemplos validados
- Adapte clothing/cenário/objeto ao contexto do usuário
- Preserve lighting + grain + aesthetic do estilo escolhido"""


def enhance_prompt(simple_prompt: str) -> str:
    """
    Melhora um prompt simples para gerar foto ultra-realista iPhone 11

    Args:
        simple_prompt: Prompt simples do usuário (ex: "cachorro")

    Returns:
        Prompt otimizado ultra-realista
    """

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/felipemdepaula",
                "X-Title": "Gerar Foto Realista - Prompt Engineer"
            },
            json={
                "model": "anthropic/claude-3.5-haiku",  # Rápido e barato
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": simple_prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 300
            },
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        enhanced = data["choices"][0]["message"]["content"].strip()

        # Remove aspas se vier com elas
        enhanced = enhanced.strip('"').strip("'")

        return enhanced

    except Exception as e:
        print(f"❌ Erro ao otimizar prompt: {e}", file=sys.stderr)
        # Fallback: retorna prompt básico melhorado
        return f"{simple_prompt}, foto tirada com iPhone 11, luz natural, ultra-realista, fotografia casual, cores vibrantes, 4K"


def main():
    """CLI para testar o prompt engineer"""

    if len(sys.argv) < 2:
        print("Uso: python3 prompt_engineer.py 'prompt simples'")
        print("\nExemplos:")
        print('  python3 prompt_engineer.py "cachorro"')
        print('  python3 prompt_engineer.py "carro na rua"')
        print('  python3 prompt_engineer.py "prato de comida"')
        sys.exit(1)

    simple_prompt = sys.argv[1]

    print(f"📝 Prompt original: {simple_prompt}")
    print(f"🤖 Otimizando...\n")

    enhanced = enhance_prompt(simple_prompt)

    print(f"✨ Prompt otimizado:")
    print(f"{enhanced}")

    return enhanced


if __name__ == "__main__":
    main()
