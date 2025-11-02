#!/usr/bin/env python3
"""
Script para enviar conteúdo sobre Brino via WhatsApp
"""

import sys
sys.path.append('/Users/felipemdepaula/Desktop/ClaudeCode-Workspace/evolution-api-integration')

from whatsapp_helper import WhatsAppHelper

def main():
    # Inicializa o helper
    whatsapp = WhatsAppHelper()

    # Número do destinatário
    numero = "5531989177023"

    # Mensagem de texto
    mensagem = """🎮 *CONHEÇA O BRINO!* 🤣

*Quem é o Brino?*

Sabe quando você tá assistindo um vídeo engraçado no TikTok e não para de rir? Então, o Brino faz EXATAMENTE isso, mas como trabalho!

Ele é um cara super legal de 27 anos que fica sentado na frente do computador assistindo vídeos da internet - tipo pessoas fazendo comida horrível, pegadinhas malucas e coisas esquisitas - e ele fica fazendo umas caretas HILARIANTES e soltando piadas super rápidas!

É tipo aquele amigo engraçado que comenta tudo e faz você rir mais ainda. E sabe o melhor? MILHÕES de pessoas assistem ele fazer isso! Ele tem quase 6 MILHÕES de seguidores só no YouTube! 🤯

---

😂 *PIADA DO BRINO:*

"O Brino é TÃO bom em reagir a vídeos que quando ele vai ao cinema, as pessoas compram ingresso só pra ver as caretas dele em vez do filme! E olha que a pipoca tá cara, hein! 🍿😅"

---

🎨 Olha só a imagem dele que eu fiz! 👇"""

    # URL da imagem (URL temporária da Kie.ai)
    imagem_url = "https://tempfile.aiquickdraw.com/s/c4c8598c34d029fdf0aa13574ba23c63_0_1762025769_6775.png"

    print("📱 Enviando conteúdo para WhatsApp...")
    print(f"📞 Destinatário: {numero}\n")

    # Enviar mensagem de texto (já enviada, comentado)
    # print("📝 Enviando texto...")
    # whatsapp.send_message(numero, mensagem)

    # Pequena pausa
    import time
    # time.sleep(2)

    # Enviar imagem
    print("🖼️ Enviando imagem...")
    whatsapp.send_image(numero, imagem_url, "Desenho divertido do Brino! 🎨")

    print("\n✅ Tudo enviado com sucesso!")

if __name__ == "__main__":
    main()
