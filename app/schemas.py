from pydantic import BaseModel, EmailStr
from datetime import datetime

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str 


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    is_admin: bool
    criado_em: datetime

    class Config:
        from_attributes = True


class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str


class ExercicioCreate(BaseModel):
    nome: str
    grupo_muscular: str
    sinergistas: list[str] = []


class ExercicioResponse(BaseModel):
    id: int
    nome: str
    grupo_muscular: str
    sinergistas: list[str] = []

    class Config:
        from_attributes = True


class ExercicioUpdate(BaseModel):
    nome: str | None = None
    grupo_muscular: str | None = None
    sinergistas: list[str] | None = None



class FichaTreinoCreate(BaseModel):
    nome: str


class FichaTreinoResponse(BaseModel):
    id: int
    nome: str
    
    class Config:
        from_attributes=True

class FichaTreinoUpdate(BaseModel):
    nome: str | None = None



class FichaExercicioCreate(BaseModel):
    exercicio_id: int
    tecnica_id: int | None = None
    series: int
    repeticoes: int
    carga: float | None = None
    ordem: int

class FichaExercicioResponse(BaseModel):
    id: int
    exercicio_id: int
    tecnica_id: int | None
    series: int
    repeticoes: int
    carga: float | None
    ordem: int

    class Config:
        from_attributes = True


class FichaExercicioUpdate(BaseModel):
    tecnica_id: int | None = None
    series: int | None = None
    repeticoes: int | None = None
    carga: float | None = None
    ordem: int | None = None



class RegistroTreinoCreate(BaseModel):
    series_realizadas: int
    repeticoes_realizadas: int
    carga_realizada: float | None = None


class RegistroTreinoResponse(BaseModel):
    id: int
    ficha_exercicio_id: int
    data_execucao: datetime
    series_realizadas: int
    repeticoes_realizadas: int
    carga_realizada: float | None

    class Config:
        from_attributes = True 

class AmizadeResponse(BaseModel):
    id: int
    solicitante_id: int
    destinatario_id: int
    status: str
    criado_em: datetime

    class Config:
        from_attributes = True


class MensagemResponse(BaseModel):
    detail: str


class PedidoAmizadeResponse(BaseModel):
    detail: str
    pedido: AmizadeResponse


class AmigoResumoResponse(BaseModel):
    id: int
    nome: str

class CompartilhamentoResponse(BaseModel):
    id: int
    ficha_id: int
    compartilhado_com_id: int
    criado_em: datetime

    class Config:
        from_attributes = True