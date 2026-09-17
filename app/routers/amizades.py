from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Usuario, Amizade
from app.schemas import AmizadeResponse
from app.routers.usuarios import pegar_usuario_atual

router = APIRouter()


@router.post("/amigos/{usuario_id}")
def enviar_pedido_amizade(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(pegar_usuario_atual)
):
    if usuario_id == usuario_atual.id:
        raise HTTPException(status_code=400, detail="Você não pode adicionar a si mesmo")

    destinatario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if destinatario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    pedido_existente = db.query(Amizade).filter(
        ((Amizade.solicitante_id == usuario_atual.id) & (Amizade.destinatario_id == usuario_id)) |
        ((Amizade.solicitante_id == usuario_id) & (Amizade.destinatario_id == usuario_atual.id))
    ).first()
    

    if pedido_existente is not None:
        raise HTTPException(status_code=400, detail="Já existe um pedido ou amizade entre vocês")

    novo_pedido = Amizade(
        solicitante_id=usuario_atual.id,
        destinatario_id=usuario_id,
        status="pendente"
    )

    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)

    return {"detail": "Pedido de amizade enviado", "pedido": AmizadeResponse.model_validate(novo_pedido)}


@router.get("/amigos/pendentes", response_model=list[AmizadeResponse])
def listar_pedidos_pendentes(
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(pegar_usuario_atual)
):
    pedidos = db.query(Amizade).filter(
        Amizade.destinatario_id == usuario_atual.id,
        Amizade.status == "pendente"
    ).all()

    return pedidos


@router.put("/amigos/{pedido_id}/aceitar")
def aceitar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(pegar_usuario_atual)
):
    pedido = db.query(Amizade).filter(
        Amizade.id == pedido_id,
        Amizade.destinatario_id == usuario_atual.id
    ).first()
    

    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    pedido.status = "aceito"
    db.commit()

    return {"detail": "Pedido de amizade aceito"}


@router.put("/amigos/{pedido_id}/recusar")
def recusar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(pegar_usuario_atual)
):
    pedido = db.query(Amizade).filter(
        Amizade.id == pedido_id,
        Amizade.destinatario_id == usuario_atual.id
    ).first()

    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    pedido.status = "recusado"
    db.commit()

    return {"detail": "Pedido de amizade recusado"}


@router.get("/amigos")
def listar_amigos(
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(pegar_usuario_atual)
):
    amizades = db.query(Amizade).filter(
        ((Amizade.solicitante_id == usuario_atual.id) | (Amizade.destinatario_id == usuario_atual.id)),
        Amizade.status == "aceito"
    ).all()
    

    amigos_ids = [
        amizade.destinatario_id if amizade.solicitante_id == usuario_atual.id else amizade.solicitante_id
        for amizade in amizades
    ]
    

    amigos = db.query(Usuario).filter(Usuario.id.in_(amigos_ids)).all()

    return [{"id": amigo.id, "nome": amigo.nome} for amigo in amigos]

@router.delete("/amigos/{usuario_id}")
def desfazer_amizade(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(pegar_usuario_atual)
):
    amizade = db.query(Amizade).filter(
        ((Amizade.solicitante_id == usuario_atual.id) & (Amizade.destinatario_id == usuario_id)) |
        ((Amizade.solicitante_id == usuario_id) & (Amizade.destinatario_id == usuario_atual.id)),
        Amizade.status == "aceito"
    ).first()
    # busca a amizade aceita entre os dois, em qualquer direção

    if amizade is None:
        raise HTTPException(status_code=404, detail="Amizade não encontrada")

    db.delete(amizade)
    db.commit()

    return {"detail": "Amizade desfeita com sucesso"}