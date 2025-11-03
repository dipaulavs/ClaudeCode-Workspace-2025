# 📸 Fotos Base para Thumbnails

## Como Usar

**Adicione suas 4 fotos aqui:**

```
scripts/thumbnail-creation/templates/fotos/
├── foto1.jpg
├── foto2.jpg
├── foto3.jpg
└── foto4.jpg
```

## Especificações das Fotos

### Formato
- **Extensão:** `.jpg` ou `.png`
- **Nomes:** `foto1.jpg`, `foto2.jpg`, `foto3.jpg`, `foto4.jpg`

### Qualidade
- **Resolução mínima:** 1920x1080 (Full HD)
- **Recomendado:** 4K (3840x2160)
- **Orientação:** Qualquer (portrait, landscape, quadrado)

### Conteúdo
- **Expressões variadas:** Neutra, sorrindo, surpreso, sério
- **Fundo:** Pode ter (Nano Banana Edit remove automaticamente)
- **Enquadramento:** Busto ou rosto (melhor para thumbnails)

## Como Funciona

Quando você solicitar thumbnails, a skill:

1. **Escolhe aleatoriamente** uma das 4 fotos
2. **Gera 4 variações** de thumbnail com estilos diferentes:
   - Mr Beast Style (vibrante, setas, expressivo)
   - Tech Minimal (gradiente, profissional, clean)
   - Contraste Alto (preto, neon, glitch)
   - Split Screen (foto + visual relacionado)
3. **Usa Nano Banana Edit** para composição
4. **Salva em** `output/thumbnails/`

## Dicas para Melhores Thumbnails

✅ **Faça:**
- Use expressões faciais marcantes
- Boa iluminação (rosto bem iluminado)
- Roupas neutras ou que combinem com marca

❌ **Evite:**
- Fotos borradas ou pixeladas
- Muitos elementos no fundo
- Iluminação muito escura

---

**Status:** 🟡 Aguardando suas 4 fotos
**Depois:** A skill escolherá aleatoriamente uma foto por geração
