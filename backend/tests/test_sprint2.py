import sys
from pathlib import Path
from datetime import datetime, timedelta
import pytest
from fastapi.testclient import TestClient

# Garante a resolução correta dos módulos tanto localmente quanto no CI
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import app, banco_tutores, banco_animais, banco_agendamentos, banco_vacinas_aplicadas

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_dados_teste():
    """Configura um estado limpo e controlado antes de cada teste."""
    banco_tutores.clear()
    banco_animais.clear()
    banco_agendamentos.clear()
    banco_vacinas_aplicadas.clear()

    # Criação de um Tutor base (ID: 1)
    banco_tutores[1] = {
        "id_tutor": 1,
        "nome": "Carlos Eduardo",
        "cpf": "12345678901",
        "cidade": "Ribeirão Preto",
        "email": "carlos@teste.com",
        "telefone": "16999998888",
        "observacoes": None
    }

    # Criação de um Animal base (ID: 1)
    banco_animais[1] = {
        "id_animal": 1,
        "id_tutor": 1,
        "nome": "Rex",
        "tipo_animal": "Cachorro",
        "raca": "Labrador",
        "sexo": "M",
        "data_nascimento": "2022-05-10"
    }


# CT11: Agendamento de consulta com dados válidos e horário livre
def test_ct11_agendamento_sucesso():
    data_futura = (datetime.now() + timedelta(days=2)).replace(microsecond=0).isoformat()
    payload = {
        "id_animal": 1,
        "id_tutor": 1,
        "veterinario": "Dra. Paula",
        "data_hora": data_futura,
        "tipo_servico": "Consulta",
        "observacoes": "Check-up de rotina"
    }

    response = client.post("/agendamentos", json=payload)
    assert response.status_code == 201
    dados = response.json()
    assert dados["mensagem"] == "Agendamento realizado com sucesso"
    assert dados["agendamento"]["id_agendamento"] == 1
    assert dados["agendamento"]["status"] == "AGENDADO"


# CT12: Tentativa de agendamento em horário já ocupado para o mesmo veterinário (Conflito)
def test_ct12_conflito_horario_mesmo_veterinario():
    data_futura = (datetime.now() + timedelta(days=3)).replace(microsecond=0).isoformat()
    payload1 = {
        "id_animal": 1,
        "id_tutor": 1,
        "veterinario": "Dr. Marcos",
        "data_hora": data_futura,
        "tipo_servico": "Consulta"
    }
    # Primeiro agendamento: Sucesso
    resp1 = client.post("/agendamentos", json=payload1)
    assert resp1.status_code == 201

    # Segundo agendamento no mesmo horário com o mesmo profissional: Conflito 409
    payload2 = {
        "id_animal": 1,
        "id_tutor": 1,
        "veterinario": "Dr. Marcos",
        "data_hora": data_futura,
        "tipo_servico": "Retorno"
    }
    resp2 = client.post("/agendamentos", json=payload2)
    assert resp2.status_code == 409
    assert "Horário indisponível" in resp2.json()["detail"]


# CT13: Agendamento vinculado a animal ou tutor inexistente
def test_ct13_agendamento_entidade_inexistente():
    data_futura = (datetime.now() + timedelta(days=1)).isoformat()
    # Tutor 999 inexistente
    payload_tutor_invalido = {
        "id_animal": 1,
        "id_tutor": 999,
        "veterinario": "Dra. Paula",
        "data_hora": data_futura,
        "tipo_servico": "Consulta"
    }
    resp_tutor = client.post("/agendamentos", json=payload_tutor_invalido)
    assert resp_tutor.status_code == 404
    assert "Tutor com ID 999 não encontrado" in resp_tutor.json()["detail"]

    # Animal 999 inexistente
    payload_animal_invalido = {
        "id_animal": 999,
        "id_tutor": 1,
        "veterinario": "Dra. Paula",
        "data_hora": data_futura,
        "tipo_servico": "Consulta"
    }
    resp_animal = client.post("/agendamentos", json=payload_animal_invalido)
    assert resp_animal.status_code == 404
    assert "Animal com ID 999 não encontrado" in resp_animal.json()["detail"]


# CT14: Agendamento em data/hora retroativa (Passado)
def test_ct14_agendamento_data_retroativa():
    data_passada = (datetime.now() - timedelta(days=1)).isoformat()
    payload = {
        "id_animal": 1,
        "id_tutor": 1,
        "veterinario": "Dra. Paula",
        "data_hora": data_passada,
        "tipo_servico": "Consulta"
    }
    response = client.post("/agendamentos", json=payload)
    assert response.status_code == 400
    assert "datas retroativas" in response.json()["detail"]


# CT15: Cancelamento de agendamento existente
def test_ct15_cancelamento_sucesso():
    data_futura = (datetime.now() + timedelta(days=5)).isoformat()
    payload = {
        "id_animal": 1,
        "id_tutor": 1,
        "veterinario": "Dr. Roberto",
        "data_hora": data_futura,
        "tipo_servico": "Consulta"
    }
    resp_criacao = client.post("/agendamentos", json=payload)
    id_agendamento = resp_criacao.json()["agendamento"]["id_agendamento"]

    # Cancela o agendamento
    resp_cancela = client.patch(f"/agendamentos/{id_agendamento}/cancelar")
    assert resp_cancela.status_code == 200
    assert resp_cancela.json()["agendamento"]["status"] == "CANCELADO"


# CT16: Tentativa de cancelamento de agendamento inexistente
def test_ct16_cancelamento_inexistente():
    response = client.patch("/agendamentos/9999/cancelar")
    assert response.status_code == 404
    assert "não encontrado" in response.json()["detail"]


# CT17: Listagem de agendamentos com filtro por veterinário e status
def test_ct17_listagem_filtros():
    data_futura1 = (datetime.now() + timedelta(days=1)).isoformat()
    data_futura2 = (datetime.now() + timedelta(days=2)).isoformat()

    client.post("/agendamentos", json={
        "id_animal": 1, "id_tutor": 1, "veterinario": "Dra. Camila",
        "data_hora": data_futura1, "tipo_servico": "Consulta"
    })
    client.post("/agendamentos", json={
        "id_animal": 1, "id_tutor": 1, "veterinario": "Dr. Fernando",
        "data_hora": data_futura2, "tipo_servico": "Consulta"
    })

    # Filtrar por veterinário Camila
    resp = client.get("/agendamentos?veterinario=Dra. Camila")
    assert resp.status_code == 200
    dados = resp.json()
    assert len(dados) == 1
    assert dados[0]["veterinario"] == "Dra. Camila"


# CT18: Validação de intervalo mínimo entre doses da mesma vacina (regra de 21 dias)
def test_ct18_validacao_intervalo_vacina():
    # Simula que o animal 1 tomou a vacina V8 há 10 dias
    data_aplicacao_anterior = datetime.now() - timedelta(days=10)
    banco_vacinas_aplicadas[1] = [
        {"nome_vacina": "V8 Canina", "data_aplicacao": data_aplicacao_anterior}
    ]

    # Tentativa de agendar a próxima dose para amanhã (apenas 11 dias de intervalo) -> Deve falhar
    data_proxima_dose = (datetime.now() + timedelta(days=1)).isoformat()
    payload_invalido = {
        "id_animal": 1,
        "id_tutor": 1,
        "veterinario": "Dra. Paula",
        "data_hora": data_proxima_dose,
        "tipo_servico": "Vacina",
        "nome_vacina": "V8 Canina"
    }
    resp_invalida = client.post("/agendamentos", json=payload_invalido)
    assert resp_invalida.status_code == 400
    assert "no mínimo 21 dias de intervalo" in resp_invalida.json()["detail"]

    # Tentativa de agendar a próxima dose para daqui a 15 dias (totalizando 25 dias de intervalo) -> Deve permitir
    data_permitida = (datetime.now() + timedelta(days=15)).isoformat()
    payload_valido = {
        "id_animal": 1,
        "id_tutor": 1,
        "veterinario": "Dra. Paula",
        "data_hora": data_permitida,
        "tipo_servico": "Vacina",
        "nome_vacina": "V8 Canina"
    }
    resp_valida = client.post("/agendamentos", json=payload_valido)
    assert resp_valida.status_code == 201
    assert resp_valida.json()["agendamento"]["status"] == "AGENDADO"
