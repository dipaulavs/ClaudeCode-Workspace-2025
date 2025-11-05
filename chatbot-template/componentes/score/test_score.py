"""
Testes para Sistema de Score + Tags + Origem
"""
import json
import time
import redis
from sistema_score import SistemaScore
from sistema_tags import SistemaTags
from deteccao_origem import DeteccaoOrigem
from integrador import IntegradorScore


# Config de teste
REDIS_CONFIG = {
    "host": "localhost",
    "port": 6379,
    "db": 1,  # DB de teste
    "decode_responses": True
}

CHATWOOT_CONFIG = {
    "url": "https://chatwoot.loop9.com.br",
    "token": "xp1AcWvf6F2p2ZypabNWHfW6",
    "account_id": 1,
    "inbox_id": 40
}


def limpar_redis_teste(redis_client, cliente_numero):
    """Limpa dados de teste do Redis"""
    keys = [
        f"score:{cliente_numero}",
        f"score_history:{cliente_numero}",
        f"estado:{cliente_numero}",
        f"origem:{cliente_numero}",
        f"tags_aplicadas:{cliente_numero}",
        f"conversao:{cliente_numero}",
        f"chatwoot:conv_id:{cliente_numero}"
    ]
    for key in keys:
        redis_client.delete(key)


def test_cenario_1_calculo_score():
    """
    Cenário 1: Cálculo de score
    Cliente novo diz: "Quero apartamento 2 quartos Savassi até 2000"
    Deve ganhar: tipo_definido(10) + regiao_definida(10) + orcamento_definido(20) = 40
    """
    print("\n" + "="*60)
    print("CENÁRIO 1: Cálculo de Score")
    print("="*60)

    # Setup
    redis_client = redis.Redis(**REDIS_CONFIG)
    cliente_numero = "5531999999001"
    limpar_redis_teste(redis_client, cliente_numero)

    score_system = SistemaScore(redis_client)

    # Cliente novo
    score_inicial = score_system.get_score(cliente_numero)
    print(f"✅ Score inicial: {score_inicial}")
    assert score_inicial == 0, f"Score inicial deveria ser 0, mas é {score_inicial}"

    # Cliente envia mensagem
    mensagem = "Quero apartamento 2 quartos Savassi até 2000"
    estado = {
        "tem_tipo_definido": False,
        "tem_regiao_definida": False,
        "tem_orcamento_definido": False,
        "pediu_fotos": False,
        "fez_perguntas": False,
        "mencionou_prazo": False,
        "respondeu_rapido": False,
        "tem_urgencia": None,
        "ultima_mensagem_timestamp": None
    }

    delta = score_system.calcular_delta(mensagem, estado)
    print(f"✅ Delta calculado: {delta}")
    assert delta == 40, f"Delta deveria ser 40, mas é {delta}"

    # Atualizar score
    novo_score = score_system.atualizar_score(cliente_numero, delta)
    print(f"✅ Novo score: {novo_score}")
    assert novo_score == 40, f"Novo score deveria ser 40, mas é {novo_score}"

    # Classificação
    classificacao = score_system.classificar_lead(novo_score)
    print(f"✅ Classificação: {classificacao}")
    assert classificacao == "MORNO", f"Classificação deveria ser MORNO, mas é {classificacao}"

    # Limpar
    limpar_redis_teste(redis_client, cliente_numero)
    redis_client.close()

    print("✅ CENÁRIO 1 PASSOU!\n")


def test_cenario_2_tags_automaticas():
    """
    Cenário 2: Tags automáticas
    Cliente diz: "Quero ver fotos do apartamento que aceita pet"
    Deve detectar: visual, tem_pet
    """
    print("\n" + "="*60)
    print("CENÁRIO 2: Tags Automáticas")
    print("="*60)

    # Setup
    redis_client = redis.Redis(**REDIS_CONFIG)
    cliente_numero = "5531999999002"
    limpar_redis_teste(redis_client, cliente_numero)

    tags_system = SistemaTags(redis_client, CHATWOOT_CONFIG)

    # Cliente envia mensagem
    mensagem = "Quero ver fotos do apartamento que aceita pet"
    score = 50

    tags = tags_system.detectar_tags(mensagem, score)
    print(f"✅ Tags detectadas: {tags}")

    assert "visual" in tags, "Tag 'visual' deveria estar presente"
    assert "tem_pet" in tags, "Tag 'tem_pet' deveria estar presente"
    assert "interessado" in tags, "Tag 'interessado' deveria estar presente"
    assert "lead_morno" in tags, "Tag 'lead_morno' deveria estar presente (score=50)"

    # Limpar
    limpar_redis_teste(redis_client, cliente_numero)
    redis_client.close()

    print("✅ CENÁRIO 2 PASSOU!\n")


def test_cenario_3_deteccao_origem():
    """
    Cenário 3: Detecção de origem
    Link: https://wa.me/5531980160822?text=oi&utm_source=facebook&imovel=apto-savassi-001
    Deve extrair: origem=facebook, imovel_id=apto-savassi-001
    """
    print("\n" + "="*60)
    print("CENÁRIO 3: Detecção de Origem")
    print("="*60)

    # Setup
    redis_client = redis.Redis(**REDIS_CONFIG)
    cliente_numero = "5531999999003"
    limpar_redis_teste(redis_client, cliente_numero)

    tags_system = SistemaTags(redis_client, CHATWOOT_CONFIG)
    origem_system = DeteccaoOrigem(redis_client, tags_system)

    # Simular link com UTM
    link_params = {
        "utm_source": "facebook",
        "imovel": "apto-savassi-001"
    }

    origem_data = origem_system.extrair_origem_inicial("oi", link_params)
    print(f"✅ Origem detectada: {origem_data}")

    assert origem_data["utm_source"] == "facebook", f"utm_source deveria ser 'facebook', mas é {origem_data['utm_source']}"
    assert origem_data["imovel_id"] == "apto-savassi-001", f"imovel_id deveria ser 'apto-savassi-001', mas é {origem_data['imovel_id']}"

    # Salvar origem
    origem_system.salvar_origem(cliente_numero, origem_data)

    # Verificar se salvou
    origem_salva = origem_system.get_origem(cliente_numero)
    print(f"✅ Origem salva no Redis: {origem_salva}")
    assert origem_salva["utm_source"] == "facebook"

    # Limpar
    limpar_redis_teste(redis_client, cliente_numero)
    redis_client.close()

    print("✅ CENÁRIO 3 PASSOU!\n")


def test_cenario_4_pipeline_completo():
    """
    Cenário 4: Pipeline completo
    Simula conversa completa:
    1. Primeira mensagem com UTM
    2. Cliente diz o que quer
    3. Cliente pede fotos
    4. Cliente diz que é urgente
    Score final esperado: 70+ (QUENTE)
    """
    print("\n" + "="*60)
    print("CENÁRIO 4: Pipeline Completo")
    print("="*60)

    # Setup
    redis_client = redis.Redis(**REDIS_CONFIG)
    cliente_numero = "5531999999004"
    limpar_redis_teste(redis_client, cliente_numero)

    integrador = IntegradorScore(redis_client, CHATWOOT_CONFIG)

    # 1. Primeira mensagem com UTM
    print("\n--- Mensagem 1: Primeira mensagem com UTM ---")
    resultado1 = integrador.processar_mensagem(
        cliente_numero,
        "Oi, tudo bem?",
        eh_primeira_msg=True,
        link_params={"utm_source": "facebook", "imovel": "apto-savassi-001"}
    )
    print(f"Score: {resultado1['score']}, Classificação: {resultado1['classificacao']}, Tags: {resultado1['tags_aplicadas']}")
    assert resultado1["origem"] == "facebook"

    # 2. Cliente diz o que quer
    print("\n--- Mensagem 2: Cliente define preferências ---")
    resultado2 = integrador.processar_mensagem(
        cliente_numero,
        "Quero apartamento 2 quartos Savassi até 2000"
    )
    print(f"Score: {resultado2['score']}, Classificação: {resultado2['classificacao']}, Tags: {resultado2['tags_aplicadas']}")
    assert resultado2["score"] >= 40  # tipo + região + orçamento

    # 3. Cliente pede fotos
    print("\n--- Mensagem 3: Cliente pede fotos ---")
    resultado3 = integrador.processar_mensagem(
        cliente_numero,
        "Pode me enviar fotos?"
    )
    print(f"Score: {resultado3['score']}, Classificação: {resultado3['classificacao']}, Tags: {resultado3['tags_aplicadas']}")
    assert resultado3["score"] >= 50  # anterior + pediu_fotos

    # 4. Cliente diz que é urgente
    print("\n--- Mensagem 4: Cliente indica urgência ---")
    resultado4 = integrador.processar_mensagem(
        cliente_numero,
        "É urgente, preciso pra hoje"
    )
    print(f"Score: {resultado4['score']}, Classificação: {resultado4['classificacao']}, Tags: {resultado4['tags_aplicadas']}")
    assert resultado4["score"] >= 70  # anterior + urgente
    assert resultado4["classificacao"] == "QUENTE"

    # Resumo final
    print("\n--- Resumo Final ---")
    resumo = integrador.get_resumo_cliente(cliente_numero)
    print(f"Score final: {resumo['score']}")
    print(f"Classificação: {resumo['classificacao']}")
    print(f"Origem: {resumo['origem']['utm_source']}")
    print(f"Imóvel interesse: {resumo['origem']['imovel_id']}")
    print(f"Tags: {resumo['tags']}")

    # Limpar
    limpar_redis_teste(redis_client, cliente_numero)
    redis_client.close()

    print("✅ CENÁRIO 4 PASSOU!\n")


def test_cenario_5_estatisticas():
    """
    Cenário 5: Estatísticas gerais
    Cria múltiplos leads e verifica estatísticas
    """
    print("\n" + "="*60)
    print("CENÁRIO 5: Estatísticas Gerais")
    print("="*60)

    # Setup
    redis_client = redis.Redis(**REDIS_CONFIG)
    integrador = IntegradorScore(redis_client, CHATWOOT_CONFIG)

    # Criar 3 leads com diferentes scores
    leads = [
        {"numero": "5531999999101", "score": 80},  # QUENTE
        {"numero": "5531999999102", "score": 50},  # MORNO
        {"numero": "5531999999103", "score": 20}   # FRIO
    ]

    for lead in leads:
        limpar_redis_teste(redis_client, lead["numero"])
        # Simular score
        integrador.score.atualizar_score(lead["numero"], lead["score"])

    # Buscar estatísticas
    stats = integrador.get_estatisticas()
    print(f"\n✅ Estatísticas:")
    print(f"   Total leads: {stats['total_leads']}")
    print(f"   Leads quentes: {stats['leads_quentes']}")
    print(f"   Leads mornos: {stats['leads_mornos']}")
    print(f"   Leads frios: {stats['leads_frios']}")
    print(f"   Score médio: {stats['score_medio']:.1f}")

    assert stats['total_leads'] >= 3
    assert stats['leads_quentes'] >= 1
    assert stats['leads_mornos'] >= 1
    assert stats['leads_frios'] >= 1

    # Limpar
    for lead in leads:
        limpar_redis_teste(redis_client, lead["numero"])
    redis_client.close()

    print("✅ CENÁRIO 5 PASSOU!\n")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("TESTES - SISTEMA DE SCORE + TAGS + ORIGEM")
    print("="*60)

    try:
        # Verificar conexão Redis
        redis_client = redis.Redis(**REDIS_CONFIG)
        redis_client.ping()
        redis_client.close()
        print("✅ Redis conectado\n")
    except Exception as e:
        print(f"❌ Erro ao conectar no Redis: {e}")
        print("⚠️ Certifique-se que o Redis está rodando na porta 6379")
        exit(1)

    # Executar testes
    try:
        test_cenario_1_calculo_score()
        test_cenario_2_tags_automaticas()
        test_cenario_3_deteccao_origem()
        test_cenario_4_pipeline_completo()
        test_cenario_5_estatisticas()

        print("\n" + "="*60)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("="*60 + "\n")

    except AssertionError as e:
        print(f"\n❌ TESTE FALHOU: {e}\n")
        exit(1)
    except Exception as e:
        print(f"\n❌ ERRO NOS TESTES: {e}\n")
        import traceback
        traceback.print_exc()
        exit(1)
