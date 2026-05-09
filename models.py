from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from enum import Enum
from datetime import datetime

# ENUMS (Tipos de dados fixos)

class TipoUsuario(str, Enum):
    PROFESSOR = "professor"
    ALUNO = "aluno"

class StatusAtividade(str, Enum):
    A_FAZER = "A_FAZER"
    FAZENDO = "FAZENDO"
    PRONTO = "PRONTO"

class Prioridade(str, Enum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"

# MODELOS DE ENTRADA (Request)

class UsuarioCreate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    tipo: TipoUsuario
    email: EmailStr
    senha: str = Field(..., min_length=6)

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None

class DisciplinaCreate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    professor_id: int
    descricao: Optional[str] = None

class DisciplinaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None

class AtividadeCreate(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=200)
    descricao: Optional[str] = None
    data_entrega: str  # Formato: "YYYY-MM-DD"
    disciplina_id: int
    prioridade: Prioridade = Prioridade.MEDIA
    
    @field_validator('data_entrega')
    @classmethod
    def validar_data_entrega(cls, v):
        try:
            data_entrega = datetime.strptime(v, "%Y-%m-%d").date()
            data_hoje = datetime.now().date()
            
            if data_entrega < data_hoje:
                raise ValueError(f"Data de entrega não pode ser no passado. Data mínima: {data_hoje.strftime('%Y-%m-%d')}")
            
            return v
        except ValueError as e:
            if "does not match format" in str(e):
                raise ValueError("Formato de data inválido. Use YYYY-MM-DD (ex: 2026-05-12)")
            raise

class AtividadeUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    data_entrega: Optional[str] = None
    prioridade: Optional[Prioridade] = None

class ProgressoCreate(BaseModel):
    aluno_id: int
    atividade_id: int
    status: StatusAtividade = StatusAtividade.A_FAZER

class ProgressoUpdate(BaseModel):
    status: StatusAtividade

# MODELOS DE SAÍDA (Response)

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    tipo: TipoUsuario
    email: str

class DisciplinaResponse(BaseModel):
    id: int
    nome: str
    professor_id: int
    alunos_matriculados: List[int] = []

class AtividadeResponse(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str]
    data_entrega: str
    disciplina_id: int
    prioridade: Prioridade

class ProgressoResponse(BaseModel):
    id: int
    aluno_id: int
    atividade_id: int
    status: StatusAtividade
    data_atualizacao: Optional[str] = None
