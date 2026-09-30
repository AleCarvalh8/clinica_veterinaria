import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, field_validator

app = FastAPI(
    title="Pet & Gatô - Sistema de Gestão Veterinária",
    version="2.0.0",
    description="API REST para controle clínico, cadastros e agendamentos veterinários."
)

# Converte erros de validação Pydantic no padrão esperado pelo CT02
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Se o erro for de senha
    for err in exc.errors():
        loc = err.get("loc", ())
        if "senha" in loc:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": {"mensagem": "Senha fraca. A senha deve ter no mínimo 6 caracteres."}}
            )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": {"mensagem": "Erro de validação nos campos."}}
    )

# ==============================================================================
# BANCO DE DADOS EM MEMÓRIA (Dicionários indexados por ID)
# ==============================================================================
banco_usuarios: Dict[int, dict] = {}
banco_tutores: Dict[int, dict] = {}
banco_animais: Dict[int, dict] = {}
banco_agendamentos: Dict[int, dict] = {}
banco_vacinas_aplicadas: Dict[int, list] = {}

# Atalhos de compatibilidade
db_usuarios = banco_usuarios
db_tutores = banco_tutores
db_animais = banco_animais
db_agendamentos = banco_agendamentos


# ==============================================================================
# MODELOS DE DADOS (PYDANTIC)
# ==============================================================================

class UsuarioCadastro(BaseModel):
    nome: Optional[str] = None
    email: EmailStr
    senha: str
    perfil: Optional[str] = "Recepcao"

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, v: str):
        if len(v) < 6:
            raise ValueError("Senha fraca: a senha deve possuir ao menos 6 caracteres.")
        return v


class TutorCadastro(BaseModel):
    nome: str
    cpf: str
    telefone: str
    email: EmailStr
    cidade: Optional[str] = None
    observacoes: Optional[str] = None


class AnimalCadastro(BaseModel):
    id_tutor: int
    nome: str
    tipo_animal: Optional[str] = None
    especie: Optional[str] = None
    raca: Optional[str] = None
    sexo: Optional[str] = None
    idade: Optional[int] = None
    data_nascimento: Optional[str] = None


class AgendamentoCadastro(BaseModel):
    id_animal: int
    id_tutor: int
    veterinario: str
    data_hora: datetime
    tipo_servico: str
    nome_vacina: Optional[str] = None
    observacoes: Optional[str] = None

    @field_validator("data_hora", mode="before")
    @classmethod
    def parse_data_hora(cls, v):
        if isinstance(v, datetime):
            return v
        if isinstance(v, str):
            for fmt in ("%d/%m/%Y %H:%M", "%d/%m/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
                try:
                    return datetime.strptime(v.strip(), fmt)
                except ValueError:
                    pass
            try:
                return datetime.fromisoformat(v.strip())
            except ValueError:
                pass
        raise ValueError("Formato de data inválido. Use 'DD/MM/YYYY HH:MM' ou formato ISO.")


# ==============================================================================
# ROTAS - SPRINT 1
# ==============================================================================

@app.post("/usuarios", status_code=status.HTTP_201_CREATED, tags=["Usuários"])
def cadastrar_usuario(usuario: UsuarioCadastro):
    for u in banco_usuarios.values():
        if u["email"] == usuario.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"mensagem": "E-mail já cadastrado no sistema."}
            )
    novo_id = len(banco_usuarios) + 1
    novo_usuario = {
        "id_usuario": novo_id,
        "nome": usuario.nome,
        "email": usuario.email,
        "perfil": usuario.perfil
    }
    banco_usuarios[novo_id] = novo_usuario
    return {"usuario": novo_usuario, "mensagem": "Usuário criado com sucesso"}


@app.post("/tutores", status_code=status.HTTP_201_CREATED, tags=["Tutores"])
def cadastrar_tutor(tutor: TutorCadastro):
    cpf_limpo = re.sub(r"\D", "", tutor.cpf)
    
    for t in banco_tutores.values():
        t_cpf_limpo = re.sub(r"\D", "", str(t.get("cpf", "")))
        if t_cpf_limpo == cpf_limpo:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="CPF já cadastrado no sistema."
            )
            
    novo_id = len(banco_tutores) + 1
    novo_tutor = {
        "id_tutor": novo_id,
        "nome": tutor.nome,
        "cpf": cpf_limpo,
        "telefone": tutor.telefone,
        "email": tutor.email,
        "cidade": tutor.cidade,
        "observacoes": tutor.observacoes
    }
    banco_tutores[novo_id] = novo_tutor
    return {"tutor": novo_tutor, "mensagem": "Tutor cadastrado com sucesso"}


@app.get("/tutores/{id_tutor}", status_code=status.HTTP_200_OK, tags=["Tutores"])
def buscar_tutor(id_tutor: int):
    if id_tutor in banco_tutores:
        return {"tutor": banco_tutores[id_tutor]}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tutor com ID {id_tutor} não encontrado.")


@app.post("/animais", status_code=status.HTTP_201_CREATED, tags=["Animais"])
def cadastrar_animal(animal: AnimalCadastro):
    if animal.id_tutor not in banco_tutores:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tutor com ID {animal.id_tutor} não encontrado."
        )

    novo_id = len(banco_animais) + 1
    novo_animal = {
        "id_animal": novo_id,
        "id_tutor": animal.id_tutor,
        "nome": animal.nome,
        "tipo_animal": animal.tipo_animal or animal.especie,
        "raca": animal.raca,
        "sexo": animal.sexo,
        "idade": animal.idade,
        "data_nascimento": animal.data_nascimento
    }
    banco_animais[novo_id] = novo_animal
    return {"animal": novo_animal, "mensagem": "Animal cadastrado com sucesso"}


@app.get("/animais", status_code=status.HTTP_200_OK, tags=["Animais"])
def listar_animais():
    return list(banco_animais.values())


# ==============================================================================
# ROTAS - SPRINT 2
# ==============================================================================

@app.post("/agendamentos", status_code=status.HTTP_201_CREATED, tags=["Agendamentos"])
def criar_agendamento(agendamento: AgendamentoCadastro):
    agora = datetime.now()
    if agendamento.data_hora < agora:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é permitido realizar agendamentos em datas retroativas."
        )

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

    for ag in banco_agendamentos.values():
        if (
            ag["veterinario"].strip().lower() == agendamento.veterinario.strip().lower()
            and ag["data_hora"] == agendamento.data_hora
            and ag["status"] != "CANCELADO"
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Horário indisponível para {agendamento.veterinario}."
            )

    tipo_servico_lower = agendamento.tipo_servico.lower()
    if "vacina" in tipo_servico_lower:
        intervalo_minimo = timedelta(days=21)
        
        # 1. Histórico prévio de vacinas aplicadas
        historico_animal = banco_vacinas_aplicadas.get(agendamento.id_animal, [])
        for vacina_passada in historico_animal:
            data_passada = vacina_passada.get("data_aplicacao")
            if data_passada:
                diferenca = abs(agendamento.data_hora - data_passada)
                if diferenca < intervalo_minimo:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="É necessário respeitar no mínimo 21 dias de intervalo entre aplicações de vacina."
                    )

        # 2. Outros agendamentos de vacina já existentes
        for ag in banco_agendamentos.values():
            if (
                ag["id_animal"] == agendamento.id_animal
                and "vacina" in ag["tipo_servico"].lower()
                and ag["status"] != "CANCELADO"
            ):
                diferenca = abs(agendamento.data_hora - ag["data_hora"])
                if diferenca < intervalo_minimo:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="É necessário respeitar no mínimo 21 dias de intervalo entre aplicações de vacina."
                    )

    novo_id = len(banco_agendamentos) + 1
    dados_agendamento = {
        "id_agendamento": novo_id,
        "id": novo_id,
        "id_animal": agendamento.id_animal,
        "id_tutor": agendamento.id_tutor,
        "veterinario": agendamento.veterinario,
        "data_hora": agendamento.data_hora,
        "tipo_servico": agendamento.tipo_servico,
        "nome_vacina": agendamento.nome_vacina,
        "observacoes": agendamento.observacoes,
        "status": "AGENDADO",
        "criado_em": agora
    }
    banco_agendamentos[novo_id] = dados_agendamento
    return {
        "mensagem": "Agendamento realizado com sucesso",
        "agendamento": dados_agendamento,
        "id_agendamento": novo_id,
        "id": novo_id,
        "status": "AGENDADO"
    }


@app.get("/agendamentos", status_code=status.HTTP_200_OK, tags=["Agendamentos"])
def listar_agendamentos(
    veterinario: Optional[str] = None,
    status_consulta: Optional[str] = None
):
    resultado = list(banco_agendamentos.values())

    if veterinario:
        resultado = [
            ag for ag in resultado
            if ag["veterinario"].strip().lower() == veterinario.strip().lower()
        ]

    if status_consulta:
        resultado = [
            ag for ag in resultado
            if ag["status"].strip().upper() == status_consulta.strip().upper()
        ]

    return resultado


@app.patch("/agendamentos/{id_agendamento}/cancelar", status_code=status.HTTP_200_OK, tags=["Agendamentos"])
def cancelar_agendamento(id_agendamento: int):
    if id_agendamento in banco_agendamentos:
        banco_agendamentos[id_agendamento]["status"] = "CANCELADO"
        return {
            "agendamento": banco_agendamentos[id_agendamento],
            "id_agendamento": id_agendamento,
            "status": "CANCELADO",
            "mensagem": "Agendamento cancelado com sucesso."
        }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Agendamento não encontrado para cancelamento."
    )
