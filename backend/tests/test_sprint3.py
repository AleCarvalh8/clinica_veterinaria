import sys
from pathlib import Path
from datetime import datetime, timedelta
import pytest
from fastapi.testclient import TestClient

# Garante que a pasta backend está acessível nos módulos do Python
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import (
    app,
    banco_usuarios,
    banco_tutores,
    banco_animais,
    banco_agendamentos,
    banco_internacoes,
    banco_plantoes,
)

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_dados_teste():
    """Configura um estado limpo e controlado antes de cada teste."""
    banco_usuarios.clear()
    banco_tutores.clear()
    banco_animais.clear()
    banco_agendamentos.clear()
    banco_internacoes.clear()
    banco_plantoes.clear()

    # Criação de um Tutor e Animal base
    banco_tutores[1] = {
        "id_tutor": 1,
        "nome": "Carlos Silva",
        "cpf": "11122233344",
        "telefone": "16999990000",
        "email": "carlos@email.com",
        "cidade": "Ribeirão Preto",
    }
    banco_animais[1] = {
        "id_animal": 1,
        "id_tutor": 1,
        "nome": "Rex",
        "tipo_animal": "Cão",
        "raca": "Labrador",
        "sexo": "M",
        "idade": 3,
    }


# ==============================================================================
# TESTES SPRINT 3 (HISTÓRIAS SHOULD: 13, 14 E 15)
# ==============================================================================

# CT19: Entrada de Internação com Sucesso
def test_ct19_internacao_sucesso():
    payload = {
        "id_animal": 1,
        "crmv": 12345,
        "nivel_gravidade": "Alta",
        "motivo": "Intoxicação alimentar severa",
        "observacoes": "Pet em soroterapia",
    }
    response = client.post("/internacoes", json=payload)
    assert response.status_code == 201
    dados = response.json()
    assert dados["internacao"]["animal_nome"] == "Rex"
    assert dados["internacao"]["nivel_gravidade"] == "Alta"
    assert dados["internacao"]["status_internacao"] == "Internado"


# CT20: Validação de Nível de Gravidade Inválido
def test_ct20_internacao_gravidade_invalida():
    payload = {
        "id_animal": 1,
        "crmv": 12345,
        "nivel_gravidade": "Extrema",  # Inválido
        "motivo": "Emergência",
    }
    response = client.post("/internacoes", json=payload)
    assert response.status_code == 400
    assert "Nível de gravidade inválido" in response.json()["detail"]


# CT21: Bloqueio de Animal Já Internado
def test_ct21_internacao_duplicada():
    payload = {
        "id_animal": 1,
        "crmv": 12345,
        "nivel_gravidade": "Medio",
        "motivo": "Cirurgia eletiva",
    }
    res1 = client.post("/internacoes", json=payload)
    assert res1.status_code == 201

    res2 = client.post("/internacoes", json=payload)
    assert res2.status_code == 409
    assert "já consta como atualmente internado" in res2.json()["detail"]


# CT22: Listagem e Filtro por Gravidade
def test_ct22_listagem_filtros_internacao():
    client.post(
        "/internacoes",
        json={"id_animal": 1, "crmv": 12345, "nivel_gravidade": "Critica", "motivo": "Trauma"},
    )
    res_critica = client.get("/internacoes?nivel_gravidade=Critica")
    assert res_critica.status_code == 200
    assert len(res_critica.json()) == 1

    res_baixa = client.get("/internacoes?nivel_gravidade=Baixa")
    assert res_baixa.status_code == 200
    assert len(res_baixa.json()) == 0


# CT23: Detalhes do Caso Clínico
def test_ct23_detalhes_caso_internacao():
    res_post = client.post(
        "/internacoes",
        json={"id_animal": 1, "crmv": 12345, "nivel_gravidade": "Baixa", "motivo": "Observação pós-vacina"},
    )
    id_internacao = res_post.json()["internacao"]["id_internacao"]

    res_get = client.get(f"/internacoes/{id_internacao}")
    assert res_get.status_code == 200
    detalhes = res_get.json()
    assert detalhes["internacao"]["id_internacao"] == id_internacao
    assert detalhes["detalhes_animal"]["nome"] == "Rex"


# CT24: Evolução de Plantão com Perfil Veterinário
def test_ct24_plantao_sucesso():
    payload = {
        "id_animal": 1,
        "crmv": 12345,
        "evolucao_plantao": "Paciente estável e responsivo.",
    }
    headers = {"X-Perfil": "veterinario"}
    response = client.post("/plantao", json=payload, headers=headers)
    assert response.status_code == 201
    assert "plantao" in response.json()
    assert "turno_plantao" in response.json()["plantao"]


# CT25: Bloqueio de Mais de Uma Anotação por Animal no Mesmo Plantão
def test_ct25_bloqueio_plantao_duplicado():
    payload = {
        "id_animal": 1,
        "crmv": 12345,
        "evolucao_plantao": "Primeira checagem.",
    }
    headers = {"X-Perfil": "veterinario"}
    res1 = client.post("/plantao", json=payload, headers=headers)
    assert res1.status_code == 201

    res2 = client.post("/plantao", json=payload, headers=headers)
    assert res2.status_code == 409
    assert "já possui evolução registrada neste plantão" in res2.json()["detail"]


# CT26: Resumo do Dashboard com Métricas em Tempo Real
def test_ct26_dashboard_tempo_real():
    client.post(
        "/internacoes",
        json={"id_animal": 1, "crmv": 12345, "nivel_gravidade": "Alta", "motivo": "Tratamento intensivo"},
    )
    response = client.get("/dashboard")
    assert response.status_code == 200
    dash = response.json()
    assert dash["total_tutores"] == 1
    assert dash["total_animais"] == 1
    assert dash["total_internacoes_ativas"] == 1
    assert dash["resumo_gravidade_internacoes"]["Alta"] == 1
