import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import app, banco_tutores, banco_animais, banco_usuarios

import pytest
from fastapi.testclient import TestClient

try:
    from app.main import app, banco_tutores, banco_animais, banco_usuarios
except ImportError:
    from main import app, banco_tutores, banco_animais, banco_usuarios

client = TestClient(app)

@pytest.fixture(autouse=True)
def resetar_banco():
    banco_usuarios.clear()
    banco_tutores.clear()
    banco_animais.clear()

def test_ct02_senha_fraca_recusada():
    payload = {
        "nome": "Maria Silva",
        "email": "maria@petgato.com.br",
        "senha": "fraca",
        "perfil": "Recepcao"
    }
    response = client.post("/usuarios", json=payload)
    assert response.status_code == 400
    assert "Senha fraca" in response.json()["detail"]["mensagem"]

def test_ct02_senha_forte_aceita():
    payload = {
        "nome": "Dr. Carlos",
        "email": "carlos@petgato.com.br",
        "senha": "SenhaForte@2026",
        "perfil": "Veterinario"
    }
    response = client.post("/usuarios", json=payload)
    assert response.status_code == 201

def test_ct03_cadastro_tutor_sucesso():
    payload = {
        "nome": "Ana Paula",
        "cpf": "123.456.789-01",
        "cidade": "Ribeirão Preto",
        "email": "ana@gmail.com",
        "telefone": "16999991111"
    }
    response = client.post("/tutores", json=payload)
    assert response.status_code == 201
    assert response.json()["tutor"]["cpf"] == "12345678901"

def test_ct01_cadastro_tutor_cpf_duplicado():
    payload = {
        "nome": "João Pedro",
        "cpf": "000.000.001-00",
        "cidade": "Ribeirão Preto",
        "email": "joao@gmail.com",
        "telefone": "16988882222"
    }
    resp1 = client.post("/tutores", json=payload)
    assert resp1.status_code == 201

    resp2 = client.post("/tutores", json=payload)
    assert resp2.status_code == 409
    assert "CPF já cadastrado" in resp2.json()["detail"]

def test_ct06_cadastro_animal_com_tutor_existente():
    tutor_payload = {
        "nome": "Lucas Lima",
        "cpf": "222.333.444-55",
        "cidade": "Ribeirão Preto",
        "email": "lucas@gmail.com",
        "telefone": "16977773333"
    }
    resp_tutor = client.post("/tutores", json=tutor_payload)
    id_tutor = resp_tutor.json()["tutor"]["id_tutor"]

    animal_payload = {
        "id_tutor": id_tutor,
        "nome": "Mingau",
        "tipo_animal": "Gato",
        "raca": "Siamês",
        "sexo": "M",
        "data_nascimento": "2023-01-10"
    }
    resp_animal = client.post("/animais", json=animal_payload)
    assert resp_animal.status_code == 201
    assert resp_animal.json()["animal"]["id_tutor"] == id_tutor

def test_ct07_cadastro_animal_tutor_inexistente():
    animal_payload = {
        "id_tutor": 9999,
        "nome": "Thor",
        "tipo_animal": "Cão",
        "raca": "Labrador",
        "sexo": "M",
        "data_nascimento": "2022-05-20"
    }
    response = client.post("/animais", json=animal_payload)
    assert response.status_code == 404
    assert "não encontrado" in response.json()["detail"]
