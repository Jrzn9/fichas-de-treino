from pydantic import BaseModel, EmailStr

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str 


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr

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