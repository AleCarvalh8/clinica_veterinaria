from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List
import re

app = FastAPI(
    title="Pet & Gatô - Sistema de Gestão Veterinária",
    description="API do MVP - Sprint 1 (Tutores, Animais e Autenticação)",
    version="1.0.0"
)

# Libera acesso para a aplicação React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de dados em memória para a Sprint 1
banco_usuarios = {}
banco_tutores = {}
banco_animais = {}

# Modelos de Dados
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

# Funções de validação
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

# Endpoints
@app.get("/")
def home():
    return {
        "sistema": "Clínica Veterinária Pet & Gatô",
        "status": "Online",
        "sprint": "Sprint 1",
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
