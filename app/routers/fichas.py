from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Usuario, FichaTreino, FichaExercicio, Exercicio, Tecnica, RegistroTreino
from app.schemas import FichaTreinoCreate, FichaTreinoResponse, FichaTreinoUpdate, FichaExercicioCreate, FichaExercicioResponse, FichaExercicioUpdate, RegistroTreinoCreate, RegistroTreinoResponse, MensagemResponse
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


@router.post("/fichas/{ficha_id}/exercicios/{ficha_exercicio_id}/registros")
def registrar_execucao(
    ficha_id: int,
    ficha_exercicio_id: int,
    dados: RegistroTreinoCreate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends (pegar_usuario_atual)
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
        raise HTTPException(status_code=404, detail="Exercício não encotrado nessa ficha")

    novo_registro = RegistroTreino(
        ficha_exercicio_id=ficha_exercicio_id,
        series_realizadas=dados.series_realizadas,
        repeticoes_realizadas=dados.repeticoes_realizadas,
        carga_realizada=dados.carga_realizada
    )

    db.add(novo_registro)
    db.commit()
    db.refresh(novo_registro)

    return {
        "detail": "Execução registrada com sucesso",
        "registro": RegistroTreinoResponse(
            id=novo_registro.id,
            ficha_exercicio_id=novo_registro.ficha_exercicio_id,
            data_execucao=novo_registro.data_execucao,
            series_realizadas=novo_registro.series_realizadas,
            repeticoes_realizadas=novo_registro.repeticoes_realizadas,
            carga_realizada=novo_registro.carga_realizada
        )
    }

@router.get("/fichas/{ficha_id}/exercicios/{ficha_exercicio_id}/registros", response_model=list[RegistroTreinoResponse])
def listar_registros(
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

    registros = db.query(RegistroTreino).filter(
        RegistroTreino.ficha_exercicio_id == ficha_exercicio_id
    ).all()

    return registros

@router.delete("/fichas/{ficha_id}/exercicios/{ficha_exercicio_id}/registros/{registro_id}")
def deletar_registro(
    ficha_id: int,
    ficha_exercicio_id: int,
    registro_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(pegar_usuario_atual)
):
    ficha = db.query(FichaTreino).filter(
        FichaTreino.id == ficha_id,
        FichaTreino.usuario_id == usuario_atual.id
    ).first()

    if ficha is None:
        raise HTTPException(status_code=404, detail="Ficha não encotnrada")

    vinculo = db.query(FichaExercicio).filter(
        FichaExercicio.id == ficha_exercicio_id,
        FichaExercicio.ficha_id == ficha_id 
    ).first

    if vinculo is None:
        raise HTTPException(status_code=404, detail="Exercício não encontrado nessa ficha")

    registro = db.query(RegistroTreino).filter(
        RegistroTreino.id == registro_id,
        RegistroTreino.ficha_exercicio_id == ficha_exercicio_id
    ).first()

    if registro is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado")


    db.delete(registro)
    db.commit()

    return {"detail": "Registro deletado com sucesso"}

@router.post("/fichas/{ficha_id}/compartilhar/{amigo_id}", response_model=MensagemResponse)
def compartilhar_ficha(
    ficha_id: int,
    amigo_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(pegar_usuario_atual)
):
    from app.models import Amizade, CompartilhamentoFicha

    ficha = db.query(FichaTreino).filter(
        FichaTreino.id == ficha_id,
        FichaTreino.usuario_id == usuario_atual.id
    ).first()

    if ficha is None:
        raise HTTPException(status_code=404, detail="Ficha não encontrada")

    sao_amigos = db.query(Amizade).filter(
        ((Amizade.solicitante_id == usuario_atual.id) & (Amizade.destinatario_id == amigo_id)) |
        ((Amizade.solicitante_id == amigo_id) & (Amizade.destinatario_id == usuario_atual.id)),
        Amizade.status == "aceito"
    ).first()

    if sao_amigos is None:
        raise HTTPException(status_code=403, detail="Vocês não são amigos")

    ja_compartilhado = db.query(CompartilhamentoFicha).filter(
        CompartilhamentoFicha.ficha_id == ficha_id,
        CompartilhamentoFicha.compartilhado_com_id == amigo_id
    ).first()

    if ja_compartilhado is not None:
        raise HTTPException(status_code=400, detail="Ficha já compartilhada com esse amigo")

    novo_compartilhamento = CompartilhamentoFicha(
        ficha_id=ficha_id,
        compartilhado_com_id=amigo_id
    )

    db.add(novo_compartilhamento)
    db.commit()

    return {"detail": "Ficha compartilhada com sucesso"}


@router.get("/fichas/compartilhadas-comigo", response_model=list[FichaTreinoResponse])
def listar_fichas_compartilhadas(
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(pegar_usuario_atual)
):
    from app.models import CompartilhamentoFicha

    compartilhamentos = db.query(CompartilhamentoFicha).filter(
        CompartilhamentoFicha.compartilhado_com_id == usuario_atual.id
    ).all()

    fichas_ids = [c.ficha_id for c in compartilhamentos]

    return db.query(FichaTreino).filter(FichaTreino.id.in_(fichas_ids)).all()