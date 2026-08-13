from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Usuario, Exercicio, ExercicioSinergista
from app.schemas import ExercicioCreate, ExercicioUpdate, ExercicioResponse
from app.routers.usuarios import pegar_usuario_atual, exigir_admin

router = APIRouter()


@router.post("/exercicios")
def criar_exercicio(
    exercicio: ExercicioCreate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(exigir_admin)
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

    return {
        "detail": "Exercício criado com sucesso",
        "exercicio": ExercicioResponse(
            id=novo_exercicio.id,
            nome=novo_exercicio.nome,
            grupo_muscular=novo_exercicio.grupo_muscular,
            sinergistas=[sinergista.grupo_muscular for sinergista in novo_exercicio.sinergistas]
        )
    }


@router.get("/exercicios", response_model=list[ExercicioResponse])
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


@router.get("/exercicios/{exercicio_id}", response_model=ExercicioResponse)
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


@router.put("/exercicios/{exercicio_id}")
def editar_exercicio(
    exercicio_id: int,
    dados: ExercicioUpdate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(exigir_admin)
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

    return {
        "detail": "Exercício editado com sucesso",
        "exercicio": ExercicioResponse(
            id=exercicio.id,
            nome=exercicio.nome,
            grupo_muscular=exercicio.grupo_muscular,
            sinergistas=[sinergista.grupo_muscular for sinergista in exercicio.sinergistas]
        )
    }


@router.delete("/exercicios/{exercicio_id}")
def deletar_exercicio(
    exercicio_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(exigir_admin)
):
    exercicio = db.query(Exercicio).filter(Exercicio.id == exercicio_id).first()

    if exercicio is None:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")

    db.query(ExercicioSinergista).filter(ExercicioSinergista.exercicio_id == exercicio_id).delete()
    db.delete(exercicio)
    db.commit()

    return {"detail": "Exercício deletado com sucesso"}