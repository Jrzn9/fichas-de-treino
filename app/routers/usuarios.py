from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

from app.database import get_db
from app.models import Usuario
from app.schemas import UsuarioCreate, UsuarioResponse, UsuarioLogin

load_dotenv()

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def usuario_esta_online(ultima_atividade: datetime) -> bool:
    agora = datetime.now(timezone.utc)

    if ultima_atividade.tzinfo is None:
        ultima_atividade = ultima_atividade.replace(tzinfo=timezone.utc)

    return (agora - ultima_atividade) < timedelta(minutes=5)

def montar_resposta_usuario(usuario: Usuario) -> UsuarioResponse:
    return UsuarioResponse(
        id=usuario.id,
        nome=usuario.nome,
        email=usuario.email,
        is_admin=usuario.is_admin,
        criado_em=usuario.criado_em,
        aceita_compartilhamento=usuario.aceita_compartilhamento,
        ultima_atividade=usuario.ultima_atividade,
        online=usuario_esta_online(usuario.ultima_atividade)
    )


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
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"}
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

    usuario.ultima_atividade = datetime.now(timezone.utc)
    db.commit()

    return usuario

def exigir_admin(usuario_atual: Usuario = Depends(pegar_usuario_atual)) -> Usuario:
    if not usuario_atual.is_admin:
        raise HTTPException(status_code=403, detail="Apenas administradores podem realizar esta ação")
    return usuario_atual


@router.post("/usuarios/", response_model=UsuarioResponse)
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

    return montar_resposta_usuario(novo_usuario)


@router.post("/login")
def login(credenciais: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == credenciais.email).first()

    if not usuario or not verificar_senha(credenciais.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")

    token = criar_token({"sub": usuario.email})

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UsuarioResponse)
def ler_usuario_atual(usuario_atual: Usuario = Depends(pegar_usuario_atual)):
    return montar_resposta_usuario(usuario_atual)


@router.get("/usuarios/buscar", response_model=list[UsuarioResponse])
def buscar_usuarios(
    nome: str | None = None,
    email: str | None = None,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(pegar_usuario_atual)
):
    query = db.query(Usuario)

    if nome:
        query = query.filter(Usuario.nome.ilike(f"%{nome}%"))
    if email:
        query = query.filter(Usuario.email.ilike(f"%{email}%"))

    return query.limit(20).all()

@router.put("/me/preferencias", response_model=UsuarioResponse)
def atualizar_preferencias(
    aceita_compartilhamento: bool,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(pegar_usuario_atual)
):
    usuario_atual.aceita_compartilhamento = aceita_compartilhamento
    db.commit()
    db.refresh(usuario_atual)

    return montar_resposta_usuario(usuario_atual)