from fastapi import FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, timedelta
import re

app = FastAPI(
    title="Pet & Gatô - Sistema de Gestão Veterinária",
    description="API do MVP - Sprint 1 e Sprint 2 (Tutores, Animais, Usuários e Agendamentos)",
    version="2.0.0"
)

# Libera acesso para a aplicação React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de dados em memória
banco_usuarios = {}
banco_tutores = {}
banco_animais = {}
banco_agendamentos = {}
banco_vacinas_aplicadas = {}

# --- Modelos de Dados (Sprint 1) ---
class UsuarioCadastro(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    perfil: str
    registro_profissional: Optional[str] = None

class TutorCadastro(BaseModel):
    nome: str
    cpf: str
    cidade: str
    email: EmailStr
    telefone: str
    observacoes: Optional[str] = None

class AnimalCadastro(BaseModel):
    id_tutor: int
    nome: str
    tipo_animal: str
    raca: str
    sexo: str
    data_nascimento: str

# --- Modelos de Dados (Sprint 2) ---
class AgendamentoCadastro(BaseModel):
    id_animal: int
    id_tutor: int
    veterinario: str
    data_hora: datetime
    tipo_servico: str
    nome_vacina: Optional[str] = None
    observacoes: Optional[str] = None

# --- Funções de validação ---
def validar_senha_forte(senha: str):
    pendencias = []
    if len(senha) < 8:
        pendencias.append("Mínimo de 8 caracteres")
    if not re.search(r"[A-Z]", senha):
        pendencias.append("Ao menos uma letra maiúscula")
    if not re.search(r"[a-z]", senha):
        pendencias.append("Ao menos uma letra minúscula")
    if not re.search(r"[0-9]", senha):
        pendencias.append("Ao menos um número")
    if not re.search(r"[@$!%*?&#]", senha):
        pendencias.append("Ao menos um caractere especial (@$!%*?&#)")
    return pendencias

def limpar_cpf(cpf: str) -> str:
    return re.sub(r"\D", "", cpf)

# --- Endpoints Base e Sprint 1 ---
@app.get("/")
def home():
    return {
        "sistema": "Clínica Veterinária Pet & Gatô",
        "status": "Online",
        "sprint": "Sprint 2",
        "docs": "Acesse /docs para documentação interativa"
    }

@app.post("/usuarios", status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(usuario: UsuarioCadastro):
    if usuario.perfil not in ["Recepcao", "Veterinario"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Perfil inválido. Deve ser 'Recepcao' ou 'Veterinario'."
        )

    erros_senha = validar_senha_forte(usuario.senha)
    if erros_senha:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"mensagem": "Senha fraca. Não atende aos requisitos de segurança.", "pendencias": erros_senha}
        )

    novo_id = len(banco_usuarios) + 1
    usuario_salvo = usuario.model_dump()
    usuario_salvo["id_usuario"] = novo_id
    usuario_salvo["senha"] = "hash_seguro_" + usuario.senha[-3:]
    banco_usuarios[novo_id] = usuario_salvo

    return {"mensagem": "Usuário criado com sucesso", "usuario": usuario_salvo}

@app.post("/tutores", status_code=status.HTTP_201_CREATED)
def cadastrar_tutor(tutor: TutorCadastro):
    cpf_limpo = limpar_cpf(tutor.cpf)
    if len(cpf_limpo) != 11:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF inválido. Deve conter 11 dígitos numéricos."
        )

    for t in banco_tutores.values():
        if t["cpf"] == cpf_limpo:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="CPF já cadastrado no sistema."
            )

    novo_id = len(banco_tutores) + 1
    tutor_salvo = tutor.model_dump()
    tutor_salvo["id_tutor"] = novo_id
    tutor_salvo["cpf"] = cpf_limpo
    banco_tutores[novo_id] = tutor_salvo

    return {"mensagem": "Tutor cadastrado com sucesso", "tutor": tutor_salvo}

@app.get("/tutores")
def listar_tutores():
    return list(banco_tutores.values())

@app.post("/animais", status_code=status.HTTP_201_CREATED)
def cadastrar_animal(animal: AnimalCadastro):
    if animal.id_tutor not in banco_tutores:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tutor com ID {animal.id_tutor} não encontrado no sistema. O animal precisa de um tutor válido."
        )

    if animal.sexo.upper() not in ["M", "F"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sexo inválido. Utilize 'M' para macho ou 'F' para fêmea."
        )

    novo_id = len(banco_animais) + 1
    animal_salvo = animal.model_dump()
    animal_salvo["id_animal"] = novo_id
    animal_salvo["sexo"] = animal.sexo.upper()
    banco_animais[novo_id] = animal_salvo

    return {"mensagem": "Animal cadastrado com sucesso", "animal": animal_salvo}

@app.get("/animais")
def listar_animais():
    return list(banco_animais.values())

# --- Endpoints Sprint 2 (Agendamentos e Vacinação) ---
@app.post("/agendamentos", status_code=status.HTTP_201_CREATED)
def criar_agendamento(agendamento: AgendamentoCadastro):
    if agendamento.id_tutor not in banco_tutores:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tutor com ID {agendamento.id_tutor} não encontrado."
        )
    if agendamento.id_animal not in banco_animais:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Animal com ID {agendamento.id_animal} não encontrado."
        )

    agora = datetime.now()
    data_comparacao = agendamento.data_hora.replace(tzinfo=None) if agendamento.data_hora.tzinfo else agendamento.data_hora
    if data_comparacao < agora:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é permitido realizar agendamentos em datas retroativas."
        )

    for ag in banco_agendamentos.values():
        if ag["status"] != "CANCELADO" and ag["veterinario"].lower() == agendamento.veterinario.lower():
            ag_data = ag["data_hora"].replace(tzinfo=None) if ag["data_hora"].tzinfo else ag["data_hora"]
            if ag_data == data_comparacao:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Horário indisponível. O veterinário {agendamento.veterinario} já possui consulta marcada neste horário."
                )

    if agendamento.tipo_servico.lower() == "vacina":
        if not agendamento.nome_vacina:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O nome da vacina é obrigatório para agendamentos do tipo 'Vacina'."
            )
        historico_animal = banco_vacinas_aplicadas.get(agendamento.id_animal, [])
        for vac in historico_animal:
            if vac["nome_vacina"].lower() == agendamento.nome_vacina.lower():
                diferenca_dias = (data_comparacao.date() - vac["data_aplicacao"].date()).days
                if diferenca_dias < 21:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Intervalo mínimo inválido. A vacina {agendamento.nome_vacina} exige no mínimo 21 dias de intervalo entre doses (última dose aplicada há {diferenca_dias} dias)."
                    )

    novo_id = len(banco_agendamentos) + 1
    agendamento_salvo = agendamento.model_dump()
    agendamento_salvo["id_agendamento"] = novo_id
    agendamento_salvo["status"] = "AGENDADO"
    banco_agendamentos[novo_id] = agendamento_salvo

    return {"mensagem": "Agendamento realizado com sucesso", "agendamento": agendamento_salvo}

@app.get("/agendamentos")
def listar_agendamentos(
    veterinario: Optional[str] = Query(None, description="Filtrar por nome do veterinário"),
    status_filtro: Optional[str] = Query(None, description="Filtrar por status: AGENDADO, CANCELADO, CONCLUIDO")
):
    resultado = list(banco_agendamentos.values())
    if veterinario:
        resultado = [ag for ag in resultado if ag["veterinario"].lower() == veterinario.lower()]
    if status_filtro:
        resultado = [ag for ag in resultado if ag["status"].upper() == status_filtro.upper()]
    return resultado

@app.patch("/agendamentos/{id_agendamento}/cancelar")
def cancelar_agendamento(id_agendamento: int):
    if id_agendamento not in banco_agendamentos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agendamento com ID {id_agendamento} não encontrado."
        )

    banco_agendamentos[id_agendamento]["status"] = "CANCELADO"
    return {
        "mensagem": "Agendamento cancelado com sucesso",
        "agendamento": banco_agendamentos[id_agendamento]
    }
