"""
Teste rápido para verificar se o context está funcionando
"""
import sys
from pathlib import Path

# Adiciona o caminho do utils ao PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent / "utils"))

from crews.copywriter_crew import run_copywriter_crew

print("=" * 60)
print("🧪 TESTE: Context entre Tasks")
print("=" * 60)
print()

# Input de teste
input_test = {
    'nicho': 'Emagrecimento',
    'tema': 'Exercícios abdominais não funcionam sozinhos',
    'objetivo': 'Gerar 100k+ visualizações no Instagram'
}

print("📋 Input de teste:")
print(f"   Nicho: {input_test['nicho']}")
print(f"   Tema: {input_test['tema']}")
print(f"   Objetivo: {input_test['objetivo']}")
print()

print("⚙️  Executando crew com context configurado...")
print("   (isso pode levar 2-3 minutos)")
print()

try:
    resultado = run_copywriter_crew(input_test)

    print()
    print("=" * 60)
    print("✅ RESULTADO FINAL")
    print("=" * 60)
    print(resultado)
    print()
    print("✅ Teste concluído com sucesso!")

except Exception as e:
    print()
    print("=" * 60)
    print("❌ ERRO")
    print("=" * 60)
    print(f"{type(e).__name__}: {e}")
    print()
    import traceback
    traceback.print_exc()
