from app.database import SessionLocal
from app.models import Tecnica

db = SessionLocal()

tecnicas = [
    Tecnica (
        nome="Cluster-set",
        descricao="Divide uma série normal em pequenos blocos de repetições, com pausas curtas (10-20s) entre eles. Isso permite manter a velocidade e a qualidade de cada repetição, evitando o acúmulo de fadiga que ocorre numa série contínua. Mais indicada para foco em força e potência, já que evita chegar perto da falha.",
        exemplo="Exemplo: em vez de fazer 8 repetições seguidas numa puxada aberta , você faz 4 repetições, descansa 15 segundos, faz mais 4, descansa 15 segundos, e faz as últimas 4 — mantendo a velocidade alta em cada repetição."
    ),
    Tecnica (
        nome="Myo-reps",
        descricao="Uma série inicial é feita até perto da falha (ou até a falha), seguida de mini-séries curtas (3-5 repetições) com pausas bem curtas (cerca de 20s) entre elas. O objetivo é acumular o máximo de repetições efetivas, próximas da falha, de forma mais rápida que num treino tradicional, otimizando o tempo de treino sem perder estímulo de hipertrofia e também uma forma de não aumentar o volume do treino.",
        exemplo="Exemplo: você faz uma série de 12 repetições até perto da falha, descansa 20 segundos, faz mais 4 repetições, descansa 20 segundos, faz mais 3 repetições, e repete até sentir que não consegue mais manter a técnica."
    ),
    Tecnica (
        nome="Back-off",
        descricao="Depois das séries principais feitas com carga mais pesada, reduz-se o peso (geralmente 10-20%) e faz-se uma ou mais séries adicionais com essa carga menor. O objetivo é acumular volume extra de treino sem o desgaste de manter a carga máxima, sendo bastante usada em programas de força que também buscam algum ganho de hipertrofia.",
        exemplo="Exemplo: você faz 3 séries de agachamento com 100kg, e depois reduz pra 80kg (20% a menos) pra fazer mais 1-2 séries adicionais com mais repetições."
    )
]

db.add_all(tecnicas)
db.commit()

print("Técnicas cadastradas com sucesso!")
db.close()