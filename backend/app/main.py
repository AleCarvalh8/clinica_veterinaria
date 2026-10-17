import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, field_validator

app = FastAPI(
    title="Pet & Gatô - Sistema de Gestão Veterinária",
    version="3.0.0",
    description="API REST para controle clínico, cadastros, agendamentos, internações e plantão veterinário."
)

# Converte erros de validação Pydantic no padrão esperado pelo CT02
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
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
banco_prontuarios: Dict[int, list] = {}
banco_vacinacoes: Dict[int, list] = {}
banco_internacoes: Dict[int, dict] = {}
banco_plantoes: Dict[int, list] = {}

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


class ProntuarioCadastro(BaseModel):
    crmv: int
    id_animal: int
    id_tutor: int
    peso_atual: float
    queixa: str
    anamnese: Optional[str] = None
    diagnostico: str
    receita: Optional[str] = None
    vacina: Optional[str] = None
    data_vacinacao: Optional[datetime] = None
    lote_vacina: Optional[str] = None
    data_proxima_dose: Optional[str] = None


class InternacaoCadastro(BaseModel):
    id_animal: int
    crmv: int
    nivel_gravidade: str  # 'Baixa', 'Medio', 'Alta', 'Critica'
    motivo: str
    observacoes: Optional[str] = None


class StatusInternacaoUpdate(BaseModel):
    status_internacao: str  # 'Internado', 'Em Observação', 'Alta Médica', 'Óbito'
    observacoes: Optional[str] = None


class PlantaoCadastro(BaseModel):
    id_animal: Optional[int] = None
    id_tutor: Optional[int] = None
    crmv: int
    evolucao_plantao: Optional[str] = None


# ==============================================================================
# FUNÇÕES AUXILIARES DE NEGÓCIO
# ==============================================================================

def obter_identificador_plantao_atual(dt: datetime) -> str:
    """
    Define o plantão do dia:
    - Diurno: 07:00 às 18:59:59 ('YYYY-MM-DD_DIURNO')
    - Noturno: 19:00 às 06:59:59 do dia seguinte ('YYYY-MM-DD_NOTURNO')
    """
    data_str = dt.strftime("%Y-%m-%d")
    if 7 <= dt.hour < 19:
        return f"{data_str}_DIURNO"
    if dt.hour < 7:
        ontem = (dt - timedelta(days=1)).strftime("%Y-%m-%d")
        return f"{ontem}_NOTURNO"
    return f"{data_str}_NOTURNO"


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


@app.get("/tutores", status_code=status.HTTP_200_OK, tags=["Tutores"])
def listar_tutores():
    return list(banco_tutores.values())


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


# ==============================================================================
# ROTAS - SPRINT 3
# ==============================================================================

@app.post("/prontuarios", status_code=status.HTTP_201_CREATED, tags=["Prontuários"])
def criar_prontuario(prontuario: ProntuarioCadastro, request: Request):
    """
    História 4: Veterinário atualiza prontuário e dados de vacinação.
    História 9: Restrito ao perfil de Veterinário (Header 'X-Perfil').
    """
    x_perfil = request.headers.get("x-perfil", "").strip().lower()
    if x_perfil != "veterinario":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas veterinários podem editar prontuários e registros clínicos."
        )

    if prontuario.id_animal not in banco_animais:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal não encontrado.")
    
    if prontuario.peso_atual <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O peso atual deve ser maior que zero.")

    novo_id = len(banco_prontuarios) + 1
    registro = {
        "id_prontuario": novo_id,
        "crmv": prontuario.crmv,
        "id_animal": prontuario.id_animal,
        "id_tutor": prontuario.id_tutor,
        "data_abertura": datetime.now(),
        "peso_atual": prontuario.peso_atual,
        "queixa": prontuario.queixa,
        "anamnese": prontuario.anamnese,
        "diagnostico": prontuario.diagnostico,
        "receita": prontuario.receita,
        "vacina": prontuario.vacina
    }

    if prontuario.id_animal not in banco_prontuarios:
        banco_prontuarios[prontuario.id_animal] = []
    banco_prontuarios[prontuario.id_animal].append(registro)

    if prontuario.vacina or prontuario.data_vacinacao:
        dados_vacina = {
            "data_aplicacao": prontuario.data_vacinacao or datetime.now(),
            "crmv": prontuario.crmv,
            "id_prontuario": novo_id,
            "nome_vacina": prontuario.vacina or "Vacina Padrão",
            "lote_vacina": prontuario.lote_vacina or "LOTE-000",
            "data_proxima_dose": prontuario.data_proxima_dose
        }
        if prontuario.id_animal not in banco_vacinacoes:
            banco_vacinacoes[prontuario.id_animal] = []
        banco_vacinacoes[prontuario.id_animal].append(dados_vacina)

    return {"mensagem": "Prontuário criado com sucesso", "prontuario": registro}


@app.get("/animais/{id_animal}/prontuarios", status_code=status.HTTP_200_OK, tags=["Prontuários"])
def listar_prontuarios_animal(id_animal: int):
    """Consulta o histórico de prontuários e vacinações do animal."""
    if id_animal not in banco_animais:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal não encontrado.")
    return {
        "id_animal": id_animal,
        "prontuarios": banco_prontuarios.get(id_animal, []),
        "vacinacoes": banco_vacinacoes.get(id_animal, [])
    }


# ------------------------------------------------------------------------------
# HISTÓRIA 13: Anotações de Evolução de Plantão (SHOULD)
# Critério: "Somente uma atualização por plantão. Uma anotação para cada animal."
# ------------------------------------------------------------------------------

@app.post("/plantao", status_code=status.HTTP_201_CREATED, tags=["Plantão"])
def registrar_plantao(plantao: PlantaoCadastro, request: Request):
    """
    História 13: Registra evolução clínica no plantão.
    Validação de Negócio: Bloqueia mais de uma anotação por animal no mesmo plantão.
    """
    x_perfil = request.headers.get("x-perfil", "").strip().lower()
    if x_perfil != "veterinario":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas veterinários podem realizar anotações de plantão."
        )

    if not plantao.id_animal or plantao.id_animal not in banco_animais:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal não encontrado para registro de plantão."
        )

    agora = datetime.now()
    plantao_atual = obter_identificador_plantao_atual(agora)

    # Bloqueio de regra de negócio: 1 anotação por animal por plantão
    historico_animal = banco_plantoes.get(plantao.id_animal, [])
    for registro in historico_animal:
        if registro.get("turno_plantao") == plantao_atual:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Bloqueio de Regra: O animal já possui evolução registrada neste plantão ({plantao_atual})."
            )

    animal = banco_animais[plantao.id_animal]
    id_tutor = plantao.id_tutor or animal.get("id_tutor")

    novo_id = len(banco_plantoes) + 1
    dados = {
        "id_plantao": novo_id,
        "id_animal": plantao.id_animal,
        "nome_animal": animal.get("nome"),
        "id_tutor": id_tutor,
        "crmv": plantao.crmv,
        "chegada_plantao": agora,
        "turno_plantao": plantao_atual,
        "status_plantao": "Em analise",
        "evolucao_plantao": plantao.evolucao_plantao
    }

    if plantao.id_animal not in banco_plantoes:
        banco_plantoes[plantao.id_animal] = []
    banco_plantoes[plantao.id_animal].append(dados)

    return {
        "mensagem": "Anotação de plantão registrada com sucesso.",
        "plantao": dados
    }


@app.get("/plantao/{id_animal}", status_code=status.HTTP_200_OK, tags=["Plantão"])
def listar_plantoes_animal(id_animal: int):
    """Lista as evoluções de plantão registradas para um determinado animal."""
    if id_animal not in banco_animais:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal não encontrado.")
    return banco_plantoes.get(id_animal, [])


# ------------------------------------------------------------------------------
# HISTÓRIA 14: Gestão de Internações e Nível de Gravidade (SHOULD)
# Critério: "Identificação do Animal e Tutor, status atualizado,
# lista por nível de gravidade e detalhamento do caso."
# ------------------------------------------------------------------------------

@app.post("/internacoes", status_code=status.HTTP_201_CREATED, tags=["Internações"])
def criar_internacao(internacao: InternacaoCadastro):
    """Cria uma nova internação classificando gravidade e vinculando pet e tutor."""
    if internacao.id_animal not in banco_animais:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal não encontrado.")

    niveis_validos = ["Baixa", "Medio", "Alta", "Critica"]
    gravidade_capitalizada = internacao.nivel_gravidade.capitalize()
    if gravidade_capitalizada not in niveis_validos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Nível de gravidade inválido. Valores aceitos: {niveis_validos}"
        )

    # Impede internação duplicada se o pet já estiver internado
    for inter in banco_internacoes.values():
        if inter["id_animal"] == internacao.id_animal and inter["status_internacao"] == "Internado":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="O animal informado já consta como atualmente internado."
            )

    animal = banco_animais[internacao.id_animal]
    tutor = banco_tutores.get(animal["id_tutor"], {})

    novo_id = len(banco_internacoes) + 1
    dados = {
        "id_internacao": novo_id,
        "id_animal": internacao.id_animal,
        "animal_nome": animal.get("nome"),
        "especie": animal.get("tipo_animal"),
        "id_tutor": animal.get("id_tutor"),
        "tutor_nome": tutor.get("nome"),
        "tutor_contato": tutor.get("telefone"),
        "crmv": internacao.crmv,
        "data_internacao": datetime.now(),
        "nivel_gravidade": gravidade_capitalizada,
        "status_internacao": "Internado",
        "motivo": internacao.motivo,
        "observacoes": internacao.observacoes
    }
    banco_internacoes[novo_id] = dados
    return {"mensagem": "Internação registrada com sucesso.", "internacao": dados}


@app.get("/internacoes", status_code=status.HTTP_200_OK, tags=["Internações"])
def listar_internacoes(
    nivel_gravidade: Optional[str] = None,
    status_internacao: Optional[str] = None
):
    """Lista internações permitindo filtrar por nível de gravidade e/ou status."""
    resultado = list(banco_internacoes.values())

    if nivel_gravidade:
        resultado = [
            i for i in resultado
            if i["nivel_gravidade"].lower() == nivel_gravidade.lower()
        ]

    if status_internacao:
        resultado = [
            i for i in resultado
            if i["status_internacao"].lower() == status_internacao.lower()
        ]

    return resultado


@app.get("/internacoes/{id_internacao}", status_code=status.HTTP_200_OK, tags=["Internações"])
def buscar_detalhes_internacao(id_internacao: int):
    """Traz informações detalhadas do caso de internação, histórico de plantão, pet e tutor."""
    if id_internacao not in banco_internacoes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Internação não encontrada.")

    internacao = banco_internacoes[id_internacao]
    id_animal = internacao["id_animal"]

    return {
        "internacao": internacao,
        "detalhes_animal": banco_animais.get(id_animal, {}),
        "historico_evolucoes_plantao": banco_plantoes.get(id_animal, [])
    }


@app.patch("/internacoes/{id_internacao}/status", status_code=status.HTTP_200_OK, tags=["Internações"])
def atualizar_status_internacao(id_internacao: int, dados: StatusInternacaoUpdate):
    """Atualiza o status clínico da internação (ex: Alta Médica, Em Observação)."""
    if id_internacao not in banco_internacoes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Internação não encontrada.")

    banco_internacoes[id_internacao]["status_internacao"] = dados.status_internacao
    if dados.observacoes:
        banco_internacoes[id_internacao]["observacoes"] = dados.observacoes

    return {
        "mensagem": "Status da internação atualizado com sucesso.",
        "internacao": banco_internacoes[id_internacao]
    }


# ------------------------------------------------------------------------------
# HISTÓRIA 15: Resumo do Dashboard (SHOULD)
# Critério: "Resumo dos clientes cadastrados, agendamentos e internações em tempo real."
# ------------------------------------------------------------------------------

@app.get("/dashboard", status_code=status.HTTP_200_OK, tags=["Dashboard"])
def obter_dashboard():
    """Retorna os indicadores consolidados para o Dashboard em tempo real."""
    internacoes_ativas = [
        i for i in banco_internacoes.values()
        if i["status_internacao"].lower() in ["internado", "em observação"]
    ]

    return {
        "total_tutores": len(banco_tutores),
        "total_animais": len(banco_animais),
        "total_agendamentos": len(banco_agendamentos),
        "total_internacoes_ativas": len(internacoes_ativas),
        "resumo_gravidade_internacoes": {
            "Critica": len([i for i in internacoes_ativas if i["nivel_gravidade"] == "Critica"]),
            "Alta": len([i for i in internacoes_ativas if i["nivel_gravidade"] == "Alta"]),
            "Medio": len([i for i in internacoes_ativas if i["nivel_gravidade"] == "Medio"]),
            "Baixa": len([i for i in internacoes_ativas if i["nivel_gravidade"] == "Baixa"])
        },
        "agendamentos_recentes": list(banco_agendamentos.values())[-5:],
        "internacoes_ativas": internacoes_ativas
    }
