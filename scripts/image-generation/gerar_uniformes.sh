#!/bin/bash
#
# Script: Gerar Imagens de Uniformes em Paralelo
# Usa OpenRouter Nano Banana para gerar 6 imagens realistas de uniformes profissionais
#

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🍌 Gerador de Uniformes - Nano Banana via OpenRouter${NC}"
echo "============================================================"

# Verifica se a chave está configurada
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo -e "${RED}❌ OPENROUTER_API_KEY não configurada${NC}"
    echo ""
    echo "Configure com:"
    echo "  export OPENROUTER_API_KEY='sk-or-v1-sua-chave'"
    echo ""
    echo "Ou adicione no ~/.zshrc:"
    echo "  echo 'export OPENROUTER_API_KEY=\"sk-or-v1-sua-chave\"' >> ~/.zshrc"
    echo "  source ~/.zshrc"
    exit 1
fi

# Diretório de saída
OUTPUT_DIR="$HOME/Downloads/uniformes_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR"

echo -e "${GREEN}✅ Chave OpenRouter configurada${NC}"
echo -e "${GREEN}📂 Saída: $OUTPUT_DIR${NC}"
echo ""

# Array de prompts
prompts=(
    "Professional male worker model wearing industrial safety uniform with hard hat, reflective vest and steel-toe work boots standing in modern factory, full body portrait, studio lighting, realistic professional photography, high quality, 4k"

    "Female healthcare professional model wearing clean blue medical scrubs and white coat with stethoscope in modern hospital setting, full body portrait, studio lighting, realistic professional photography, high quality, 4k"

    "Male security guard model wearing professional black security uniform with badge, utility belt and radio in confident stance, full body portrait, studio lighting, realistic professional photography, high quality, 4k"

    "Female retail employee model wearing branded red polo shirt uniform with name tag and black pants in modern retail store, full body portrait, studio lighting, realistic professional photography, high quality, 4k"

    "Male service worker model wearing professional blue service uniform with company logo patch and tool belt standing confidently, full body portrait, studio lighting, realistic professional photography, high quality, 4k"

    "Male electrical technician model wearing arc flash protective uniform with orange flame-resistant jacket, hard hat, safety glasses and electrical testing equipment, full body portrait, studio lighting, realistic professional photography, high quality, 4k"
)

# Nomes descritivos para cada categoria
categorias=(
    "01_industria"
    "02_saude"
    "03_seguranca"
    "04_varejo"
    "05_servicos"
    "06_arco_eletrico"
)

# Diretório do script Python
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/generate_openrouter_nanobanana.py"

# Verifica se o script Python existe
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo -e "${RED}❌ Script Python não encontrado: $PYTHON_SCRIPT${NC}"
    exit 1
fi

echo -e "${BLUE}🚀 Gerando ${#prompts[@]} imagens em paralelo...${NC}"
echo ""

# Função para gerar uma imagem
gerar_imagem() {
    local index=$1
    local prompt=$2
    local categoria=$3
    local output_dir=$4

    echo -e "${BLUE}[$index] 🚀 Iniciando: $categoria${NC}"

    # Gera a imagem
    python3 "$PYTHON_SCRIPT" "$prompt" --ratio 2:3 --output "$output_dir" 2>&1 | sed "s/^/[$index] /"

    local exit_code=$?

    if [ $exit_code -eq 0 ]; then
        # Renomeia o arquivo para ter nome mais descritivo
        local latest_file=$(ls -t "$output_dir"/*.png 2>/dev/null | head -1)
        if [ -n "$latest_file" ]; then
            local new_name="$output_dir/${categoria}.png"
            mv "$latest_file" "$new_name" 2>/dev/null
            echo -e "${GREEN}[$index] ✅ Concluído: $categoria.png${NC}"
        fi
    else
        echo -e "${RED}[$index] ❌ Falhou: $categoria${NC}"
    fi
}

# Exporta a função para subshells
export -f gerar_imagem
export PYTHON_SCRIPT
export GREEN
export BLUE
export RED
export NC

# Inicia geração em paralelo (máximo 3 por vez)
MAX_PARALLEL=3
pids=()

for i in "${!prompts[@]}"; do
    # Espera se já temos MAX_PARALLEL processos rodando
    while [ ${#pids[@]} -ge $MAX_PARALLEL ]; do
        for pid in "${pids[@]}"; do
            if ! kill -0 "$pid" 2>/dev/null; then
                # Remove PID da lista
                pids=("${pids[@]/$pid}")
            fi
        done
        sleep 1
    done

    # Inicia novo processo em background
    gerar_imagem $((i+1)) "${prompts[$i]}" "${categorias[$i]}" "$OUTPUT_DIR" &
    pids+=($!)
done

# Aguarda todos os processos terminarem
echo ""
echo -e "${BLUE}⏳ Aguardando conclusão de todas as imagens...${NC}"
wait

# Resumo final
echo ""
echo "============================================================"
echo -e "${GREEN}✅ Processo concluído!${NC}"
echo ""
echo -e "📂 Imagens salvas em:"
echo -e "   ${BLUE}$OUTPUT_DIR${NC}"
echo ""
echo "📊 Arquivos gerados:"
ls -lh "$OUTPUT_DIR"/*.png 2>/dev/null | awk '{print "   " $9 " - " $5}'

# Conta quantas foram geradas
total=$(ls "$OUTPUT_DIR"/*.png 2>/dev/null | wc -l | tr -d ' ')
echo ""
echo -e "${GREEN}Total: $total/${#prompts[@]} imagens${NC}"

# Abre o diretório no Finder (macOS)
if command -v open &> /dev/null; then
    echo ""
    echo -e "${BLUE}🖼️  Abrindo pasta no Finder...${NC}"
    open "$OUTPUT_DIR"
fi
