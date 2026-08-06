from app.database import SessionLocal
from app.models import Usuario, Exercicio, ExercicioSinergista

db = SessionLocal()

# apaga TODOS os usuários da tabela
# db.query(Usuario).delete()
db.query(ExercicioSinergista).delete()
db.query(Exercicio).delete()
db.commit()

print("Usuários apagados com sucesso!")
db.close()