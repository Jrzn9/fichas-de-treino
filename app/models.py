from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Usuario (Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    senha_hash = Column(String, nullable=False)
    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    fichas_treino=relationship("FichaTreino", back_populates="usuario")


class Exercicio(Base):
    __tablename__="exercicio"

    id =Column(Integer, primary_key=True, index=True)
    nome =Column(String, nullable=False)
    grupo_muscular=Column(String, nullable=False)

    ficha_exercicios = relationship("FichaExercicio", back_populates="exercicio")
    sinergistas = relationship("ExercicioSinergista", back_populates="exercicio")

class ExercicioSinergista(Base):
    __tablename__="exerciciosinergista"

    id =Column(Integer, primary_key=True, index=True)
    exercicio_id = Column(Integer, ForeignKey("exercicio.id"))
    grupo_muscular = Column(String, nullable=False)

    exercicio = relationship("Exercicio", back_populates="sinergistas")

class  FichaTreino (Base):
    __tablename__ ="ficha_treino"
    id =Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    nome =Column(String, nullable=False)
    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    usuario = relationship("Usuario", back_populates="fichas_treino")
    ficha_exercicios = relationship("FichaExercicio", back_populates="ficha")

class FichaExercicio (Base):
    __tablename__ ="ficha_exercicios"
    id =Column(Integer, primary_key=True, index=True)
    ficha_id = Column(Integer, ForeignKey("ficha_treino.id"))
    exercicio_id = Column(Integer, ForeignKey("exercicio.id"))
    series = Column(Integer, nullable=False)
    repeticoes = Column(Integer, nullable=False)
    carga = Column(Float, nullable=True)
    ordem = Column(Integer, nullable=False)

    ficha = relationship("FichaTreino", back_populates="ficha_exercicios")
    exercicio = relationship("Exercicio", back_populates="ficha_exercicios")







