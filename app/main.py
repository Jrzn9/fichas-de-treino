from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import get_db
from app.models import Base, Usuario, Exercicio, ExercicioSinergista
from app.schemas import ExercicioResponse, ExercicioUpdate, UsuarioCreate, UsuarioResponse, UsuarioLogin, ExercicioCreate

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

from dotenv import load_dotenv
import os

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI()

def hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha, senha_hash)



def criar_token(dados: dict) -> str:
    dados_para_codificar = dados.copy()
    expira_em = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados_para_codificar.update({"exp": expira_em})
    token = jwt.encode(dados_para_codificar, SECRET_KEY, algorithm=ALGORITHM)
    return token

def pegar_usuario_atual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    excecao_credenciais = HTTPException(
        status_code=401,
        detail = "Não foi possível validar as credenciais",
        headers = {"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        email: str = payload.get("sub")

        if email is None:
            raise excecao_credenciais
    except JWTError:
        raise excecao_credenciais

    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario is None:
        raise excecao_credenciais

    return usuario








@app.post("/usuarios/", response_model=UsuarioResponse)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):

    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()

    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=hash_senha(usuario.senha)
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario 


@app.post("/login")
def login(credenciais: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == credenciais.email).first()

    if not usuario or not verificar_senha(credenciais.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")

    token = criar_token({"sub": usuario.email})

    return {"access_token": token, "token_type": "bearer"}


@app.get("/me", response_model=UsuarioResponse)
def ler_usuario_atual(usuario_atual: Usuario = Depends(pegar_usuario_atual)):
    return usuario_atual


    
@app.post("/exercicios", response_model=ExercicioResponse)
def criar_exercicio(
    exercicio: ExercicioCreate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(pegar_usuario_atual)
):

    novo_exercicio = Exercicio(
        nome=exercicio.nome,
        grupo_muscular=exercicio.grupo_muscular
    )

    db.add(novo_exercicio)
    db.commit()
    db.refresh(novo_exercicio)

    for nome_sinergista in exercicio.sinergistas:
        sinergista = ExercicioSinergista(
            exercicio_id=novo_exercicio.id,
            grupo_muscular=nome_sinergista
        )
        db.add(sinergista)
    db.commit()
    db.refresh(novo_exercicio)

    return ExercicioResponse(
        id=novo_exercicio.id,
        nome=novo_exercicio.nome,
        grupo_muscular=novo_exercicio.grupo_muscular,
        sinergistas=[sinergista.grupo_muscular for sinergista in novo_exercicio.sinergistas]
        )


@app.get("/exercicios", response_model=list[ExercicioResponse])
def listar_exercicios(db: Session = Depends(get_db)):
    exercicios = db.query(Exercicio).all()

    return [
        ExercicioResponse(
            id=exercicio.id,
            nome=exercicio.nome,
            grupo_muscular=exercicio.grupo_muscular,
            sinergistas=[sinergista.grupo_muscular for sinergista in exercicio.sinergistas]
        )
        for exercicio in exercicios
    ]


@app.get("/exercicios/{exercicio_id}", response_model=ExercicioResponse)
def buscar_exercicio(exercicio_id: int, db: Session = Depends(get_db)):
    exercicio = db.query(Exercicio).filter(Exercicio.id == exercicio_id).first()

    if exercicio is None:
        raise HTTPException(status_code=404, detail="Este exercício não foi encontrado")
    
    return ExercicioResponse(
        id=exercicio.id,
        nome=exercicio.nome,
        grupo_muscular=exercicio.grupo_muscular,
        sinergistas=[sinergista.grupo_muscular for sinergista in exercicio.sinergistas]
    )


@app.put("/exercicios/{exercicio_id}", response_model=ExercicioResponse)
def editar_exercicio(
    exercicio_id: int,
    dados: ExercicioUpdate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(pegar_usuario_atual)
):
    exercicio = db.query(Exercicio).filter(Exercicio.id == exercicio_id).first()

    if exercicio is None:
        raise HTTPException(status_code=404, detail="Este exercício não foi encontrado")

    if dados.nome is not None:
        exercicio.nome = dados.nome

    if dados.grupo_muscular is not None:
        exercicio.grupo_muscular = dados.grupo_muscular

    if dados.sinergistas is not None:
        db.query(ExercicioSinergista).filter(ExercicioSinergista.exercicio_id == exercicio_id).delete()

        for nome_sinergista in dados.sinergistas:
            novo_sinergista = ExercicioSinergista(
                exercicio_id=exercicio.id,
                grupo_muscular=nome_sinergista
            )
            db.add(novo_sinergista)

    db.commit()
    db.refresh(exercicio)

    return ExercicioResponse(
        id=exercicio.id,
        nome=exercicio.nome,
        grupo_muscular=exercicio.grupo_muscular,
        sinergistas=[sinergista.grupo_muscular for sinergista in exercicio.sinergistas]
    )

        
    


