from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Usuario, FichaTreino, FichaExercicio, Exercicio, Tecnica
from app.schemas import FichaTreinoCreate, FichaTreinoResponse, FichaTreinoUpdate, FichaExercicioCreate, FichaExercicioResponse, FichaExercicioUpdate
from app.routers.usuarios import pegar_usuario_atual

router = APIRouter()


@router.post("/fichas")
def criar_ficha(
    ficha: FichaTreinoCreate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(pegar_usuario_atual)
):
    nova_ficha = FichaTreino(
        nome=ficha.nome,
        usuario_id=usuario_atual.id,
    )

    db.add(nova_ficha)
    db.commit()
    db.refresh(nova_ficha)

    return{
        "detail":"Ficha criada com sucesso",
        "ficha": FichaTreinoResponse(id=nova_ficha.id, nome=nova_ficha.nome)
    }

@router.get("/fichas", response_model=list[FichaTreinoResponse])
def listar_fichas(
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(pegar_usuario_atual)
):

    fichas = db.query(FichaTreino).filter(FichaTreino.usuario_id == usuario_atual.id).all()

    return fichas


@router.get("/fichas/{ficha_id}", response_model=FichaTreinoResponse)
def buscar_ficha(
    ficha_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(pegar_usuario_atual)
):

    ficha = db.query(FichaTreino).filter(
        FichaTreino.id == ficha_id,
        FichaTreino.usuario_id == usuario_atual.id
    ).first()

    if ficha is None:
        raise HTTPException(status_code=404, detail="Ficha não encontrada")

    return ficha


@router.put("/fichas/{ficha_id}")
def editar_ficha(
    ficha_id: int,
    dados: FichaTreinoUpdate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(pegar_usuario_atual)
):

    ficha = db.query(FichaTreino).filter(
        FichaTreino.id == ficha_id,
        FichaTreino.usuario_id == usuario_atual.id
    ).first()

    if ficha is None:
        raise HTTPException(status_code=404, detail="Ficha não encontrada")

    if dados.nome is not None:
        ficha.nome = dados.nome

    db.commit()
    db.refresh(ficha)

    return{
        "detail": "Ficha editada com sucesso",
        "ficha": FichaTreinoResponse(id=ficha.id, nome=ficha.nome)
    }


@router.delete("/fichas/{ficha_id}")
def deletar_ficha(
    ficha_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(pegar_usuario_atual)
):

    ficha = db.query(FichaTreino).filter(
    FichaTreino.id == ficha_id,
    FichaTreino.usuario_id == usuario_atual.id
    ).first()

    if ficha is None:
        raise HTTPException(status_code=404, detail="Ficha não encontrada")

    db.delete(ficha)
    db.commit()

    return {"detail": "Ficha deletada com sucesso"}

@router.post("/fichas/{ficha_id}/exercicios")
def adicionar_exercicio_na_ficha(
    ficha_id: int,
    dados: FichaExercicioCreate,
    db: Session = Depends (get_db),
    usuario_atual: Usuario = Depends (pegar_usuario_atual)
):
    ficha = db.query(FichaTreino).filter(
        FichaTreino.id == ficha_id,
        FichaTreino.usuario_id == usuario_atual.id).first()

    if ficha is None:
        raise HTTPException(status_code=404, detail="Ficha não encontrada")

    exercicio = db.query(Exercicio).filter(Exercicio.id == dados.exercicio_id).first()

    if exercicio is None:
        raise HTTPException(status_code=404, detail="Exercício não encontrado no catálogo")

    if dados.tecnica_id is not None:
        tecnica =db.query(Tecnica).filter(Tecnica.id == dados.tecnica_id).first()
        if tecnica is None:
            raise HTTPException(status_code=404, detail="Técnica não encontrada")

    novo_vinculo = FichaExercicio(
        ficha_id=ficha_id,
        exercicio_id=dados.exercicio_id,
        tecnica_id=dados.tecnica_id,
        series=dados.series,
        repeticoes=dados.repeticoes,
        carga=dados.carga,
        ordem=dados.ordem
    )

    db.add(novo_vinculo)
    db.commit()
    db.refresh(novo_vinculo)

    return{
        "detail":"Exercício adicionado à ficha com sucesso",
        "ficha_exercicio": FichaExercicioResponse(
            id=novo_vinculo.id,
            exercicio_id=novo_vinculo.exercicio_id,
            tecnica_id=novo_vinculo.tecnica_id,
            series=novo_vinculo.series,
            repeticoes=novo_vinculo.repeticoes,
            carga=novo_vinculo.carga,
            ordem=novo_vinculo.ordem
        )
    }
        
            
@router.get("/fichas/{ficha_id}/exercicios", response_model=list[FichaExercicioResponse])
def listar_exercicios_de_ficha(
    ficha_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(pegar_usuario_atual)
):
    ficha = db.query(FichaTreino).filter(
        FichaTreino.id == ficha_id,
        FichaTreino.usuario_id == usuario_atual.id      
    ).first()

    if ficha is None:
        raise HTTPException(status_code=404, detail="Ficha não encontrada")

    exercicios_da_ficha = db.query(FichaExercicio).filter(FichaExercicio.ficha_id == ficha_id).all()

    return exercicios_da_ficha

@router.put("/fichas/{ficha_id}/exercicios/{ficha_exercicio_id}")
def editar_exercicio_da_ficha(
    ficha_id: int,
    ficha_exercicio_id: int,
    dados: FichaExercicioUpdate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(pegar_usuario_atual)
):
    ficha = db.query(FichaTreino).filter(
        FichaTreino.id == ficha_id,
        FichaTreino.usuario_id == usuario_atual.id
    ).first()

    if ficha is None:
        raise HTTPException(status_code=404, detail="Ficha não encontrada")

    vinculo = db.query(FichaExercicio).filter(
        FichaExercicio.id == ficha_exercicio_id,
        FichaExercicio.ficha_id == ficha_id
    ).first()

    if vinculo is None:
        raise HTTPException(status_code=404, detail="Exercício não encontrada nessa ficha")

    if dados.tecnica_id is not None:
        vinculo.tecnica_id = dados.tecnica_id
    if dados.series is not None:
        vinculo.series = dados.series
    if dados.repeticoes is not None:
        vinculo.repeticoes = dados.repeticoes
    if dados.carga is not None:
        vinculo.carga = dados.carga
    if dados.ordem is not None:
        vinculo.ordem = dados.ordem

    db.commit()
    db.refresh(vinculo)

    return {
        "detail": "Exercício da ficha foi editado com sucesso",
        "ficha_exercicio": FichaExercicioResponse(
            id=vinculo.id,
            exercicio_id=vinculo.exercicio_id,
            tecnica_id=vinculo.tecnica_id,
            series=vinculo.series,
            repeticoes=vinculo.repeticoes,
            carga=vinculo.carga,
            ordem=vinculo.ordem
        )
    }

@router.delete("/fichas/{ficha_id}/exercicios/{ficha_exercicio_id}")
def remover_exercicio_da_ficha(
    ficha_id: int,
    ficha_exercicio_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(pegar_usuario_atual)
):
    ficha = db.query(FichaTreino).filter(
        FichaTreino.id == ficha_id,
        FichaTreino.usuario_id == usuario_atual.id
    ).first()

    if ficha is None:
        raise HTTPException(status_code=404, detail="Ficha não encontrada")

    vinculo = db.query(FichaExercicio).filter(
        FichaExercicio.id == ficha_exercicio_id,
        FichaExercicio.ficha_id == ficha_id
    ).first()

    if vinculo is None:
        raise HTTPException(status_code=404, detail="Exercício não encontrado nessa ficha")

    db.delete(vinculo)
    db.commit()

    return {"detail": "Exercício removido da ficha com sucesso"}

    
    
    