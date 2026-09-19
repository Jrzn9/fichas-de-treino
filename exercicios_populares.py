from app.database import SessionLocal
from app.models import Exercicio, ExercicioSinergista

db = SessionLocal()

exercicios = [
    # =========================================================
    # PEITO
    # =========================================================
    {"nome": "Supino Reto (barra)", "grupo_muscular": "Peito", "sinergistas": ["Ombros", "Triceps"]},
    {"nome": "Supino Inclinado (barra)", "grupo_muscular": "Peito", "sinergistas": ["Ombros", "Triceps"]},
    {"nome": "Supino Declinado", "grupo_muscular": "Peito", "sinergistas": ["Triceps"]},
    {"nome": "Supino Reto (halteres)", "grupo_muscular": "Peito", "sinergistas": ["Ombros", "Triceps"]},
    {"nome": "Supino Inclinado (halteres)", "grupo_muscular": "Peito", "sinergistas": ["Ombros", "Triceps"]},
    {"nome": "Crucifixo Reto", "grupo_muscular": "Peito", "sinergistas": ["Ombros"]},
    {"nome": "Crossover (polia)", "grupo_muscular": "Peito", "sinergistas": ["Ombros"]},
    {"nome": "Peck Deck (voador)", "grupo_muscular": "Peito", "sinergistas": ["Ombros"]},
    {"nome": "Paralelas (foco peito)", "grupo_muscular": "Peito", "sinergistas": ["Triceps", "Ombros"]},
    {"nome": "Flexao de Braco", "grupo_muscular": "Peito", "sinergistas": ["Ombros", "Triceps"]},

    {"nome": "Supino Maquina", "grupo_muscular": "Peito", "sinergistas": ["Ombros", "Triceps"]},
    {"nome": "Supino Inclinado Maquina", "grupo_muscular": "Peito", "sinergistas": ["Ombros", "Triceps"]},
    {"nome": "Chest Press", "grupo_muscular": "Peito", "sinergistas": ["Ombros", "Triceps"]},
    {"nome": "Crucifixo na Maquina", "grupo_muscular": "Peito", "sinergistas": ["Ombros"]},
    {"nome": "Crossover de Baixo para Cima", "grupo_muscular": "Peito", "sinergistas": ["Ombros"]},

    # =========================================================
    # COSTAS
    # =========================================================
    {"nome": "Puxada Aberta (pulldown)", "grupo_muscular": "Costas", "sinergistas": ["Biceps"]},
    {"nome": "Puxada Fechada (triangulo)", "grupo_muscular": "Costas", "sinergistas": ["Biceps"]},
    {"nome": "Barra Fixa (pull-up)", "grupo_muscular": "Costas", "sinergistas": ["Biceps", "Antebraco"]},
    {"nome": "Remada Curvada (barra)", "grupo_muscular": "Costas", "sinergistas": ["Biceps", "Lombar"]},
    {"nome": "Remada Baixa (polia)", "grupo_muscular": "Costas", "sinergistas": ["Biceps"]},
    {"nome": "Remada Unilateral (halter)", "grupo_muscular": "Costas", "sinergistas": ["Biceps", "Lombar"]},
    {"nome": "Levantamento Terra", "grupo_muscular": "Costas", "sinergistas": ["Gluteos", "Posterior de coxa", "Lombar"]},
    {"nome": "Encolhimento (shrug)", "grupo_muscular": "Costas", "sinergistas": ["Antebraco"]},
    {"nome": "Hiperextensao Lombar", "grupo_muscular": "Costas", "sinergistas": ["Gluteos"]},

    {"nome": "Remada Baixa Maquina", "grupo_muscular": "Costas", "sinergistas": ["Biceps"]},
    {"nome": "Remada Maquina com Apoio no Peito", "grupo_muscular": "Costas", "sinergistas": ["Biceps"]},
    {"nome": "Remada Articulada", "grupo_muscular": "Costas", "sinergistas": ["Biceps"]},
    {"nome": "Puxada Neutra", "grupo_muscular": "Costas", "sinergistas": ["Biceps"]},
    {"nome": "Puxada Unilateral", "grupo_muscular": "Costas", "sinergistas": ["Biceps"]},
    {"nome": "Pullover na Maquina", "grupo_muscular": "Costas", "sinergistas": []},
    {"nome": "Pullover na Polia", "grupo_muscular": "Costas", "sinergistas": []},

    # =========================================================
    # QUADRICEPS
    # =========================================================
    {"nome": "Agachamento Livre", "grupo_muscular": "Quadriceps", "sinergistas": ["Gluteos", "Posterior de coxa"]},
    {"nome": "Leg Press 45", "grupo_muscular": "Quadriceps", "sinergistas": ["Gluteos"]},
    {"nome": "Cadeira Extensora", "grupo_muscular": "Quadriceps", "sinergistas": []},
    {"nome": "Agachamento Bulgaro", "grupo_muscular": "Quadriceps", "sinergistas": ["Gluteos", "Posterior de coxa"]},
    {"nome": "Afundo (lunge)", "grupo_muscular": "Quadriceps", "sinergistas": ["Gluteos", "Posterior de coxa"]},
    {"nome": "Agachamento Frontal", "grupo_muscular": "Quadriceps", "sinergistas": ["Gluteos"]},
    {"nome": "Agachamento Sumo", "grupo_muscular": "Quadriceps", "sinergistas": ["Gluteos"]},

    {"nome": "Hack Squat", "grupo_muscular": "Quadriceps", "sinergistas": ["Gluteos", "Posterior de coxa"]},
    {"nome": "Agachamento no Smith", "grupo_muscular": "Quadriceps", "sinergistas": ["Gluteos", "Posterior de coxa"]},
    {"nome": "Leg Press Horizontal", "grupo_muscular": "Quadriceps", "sinergistas": ["Gluteos"]},
    {"nome": "Cadeira Extensora Unilateral", "grupo_muscular": "Quadriceps", "sinergistas": []},
    {"nome": "Sissy Squat", "grupo_muscular": "Quadriceps", "sinergistas": []},

    # =========================================================
    # OMBROS
    # =========================================================
    {"nome": "Desenvolvimento Militar (barra)", "grupo_muscular": "Ombros", "sinergistas": ["Triceps"]},
    {"nome": "Elevacao Lateral", "grupo_muscular": "Ombros", "sinergistas": []},
    {"nome": "Elevacao Frontal", "grupo_muscular": "Ombros", "sinergistas": []},
    {"nome": "Crucifixo Invertido", "grupo_muscular": "Ombros", "sinergistas": ["Trapezio"]},
    {"nome": "Desenvolvimento com Halteres", "grupo_muscular": "Ombros", "sinergistas": ["Triceps"]},

    {"nome": "Desenvolvimento na Maquina", "grupo_muscular": "Ombros", "sinergistas": ["Triceps"]},
    {"nome": "Elevacao Lateral na Maquina", "grupo_muscular": "Ombros", "sinergistas": []},
    {"nome": "Elevacao Lateral na Polia", "grupo_muscular": "Ombros", "sinergistas": []},
    {"nome": "Face Pull", "grupo_muscular": "Ombros", "sinergistas": ["Trapezio"]},

    # =========================================================
    # BICEPS
    # =========================================================
    {"nome": "Rosca Direta (barra W)", "grupo_muscular": "Biceps", "sinergistas": ["Antebraco"]},
    {"nome": "Rosca Alternada (halteres)", "grupo_muscular": "Biceps", "sinergistas": ["Antebraco"]},
    {"nome": "Rosca Scott", "grupo_muscular": "Biceps", "sinergistas": []},
    {"nome": "Rosca Martelo", "grupo_muscular": "Biceps", "sinergistas": ["Braquial", "Antebraco"]},
    {"nome": "Rosca Inversa", "grupo_muscular": "Biceps", "sinergistas": ["Braquiorradial", "Antebraco"]},
    {"nome": "Rosca no Cabo (polia)", "grupo_muscular": "Biceps", "sinergistas": ["Antebraco"]},

    {"nome": "Rosca Scott na Maquina", "grupo_muscular": "Biceps", "sinergistas": []},
    {"nome": "Rosca Bayesian (polia)", "grupo_muscular": "Biceps", "sinergistas": ["Antebraco"]},
    {"nome": "Rosca Unilateral na Polia", "grupo_muscular": "Biceps", "sinergistas": ["Antebraco"]},
    {"nome": "Rosca Concentrada na Maquina", "grupo_muscular": "Biceps", "sinergistas": []},

    # =========================================================
    # TRICEPS
    # =========================================================
    {"nome": "Triceps Testa (barra W)", "grupo_muscular": "Triceps", "sinergistas": []},
    {"nome": "Triceps Pulley (barra V)", "grupo_muscular": "Triceps", "sinergistas": []},
    {"nome": "Mergulho em Paralelas", "grupo_muscular": "Triceps", "sinergistas": ["Peito", "Ombros"]},
    {"nome": "Supino Fechado", "grupo_muscular": "Triceps", "sinergistas": ["Peito", "Ombros"]},
    {"nome": "JM Press", "grupo_muscular": "Triceps", "sinergistas": ["Peito"]},

    {"nome": "Triceps Frances na Polia", "grupo_muscular": "Triceps", "sinergistas": []},
    {"nome": "Triceps Unilateral na Polia", "grupo_muscular": "Triceps", "sinergistas": []},
    {"nome": "Triceps acima da Cabeca na Polia", "grupo_muscular": "Triceps", "sinergistas": []},
    {"nome": "Triceps na Maquina", "grupo_muscular": "Triceps", "sinergistas": []},

    # =========================================================
    # ANTEBRACO
    # =========================================================
    {"nome": "Rosca de Punho (flexao)", "grupo_muscular": "Antebraco", "sinergistas": []},
    {"nome": "Rosca de Punho Invertida (extensao)", "grupo_muscular": "Antebraco", "sinergistas": []},
    {"nome": "Farmers Walk", "grupo_muscular": "Antebraco", "sinergistas": ["Trapezio"]},

    # =========================================================
    # BRAQUIAL
    # =========================================================
    {"nome": "Rosca Martelo (foco braquial)", "grupo_muscular": "Braquial", "sinergistas": ["Biceps", "Braquiorradial"]},
    {"nome": "Rosca Cross-Body", "grupo_muscular": "Braquial", "sinergistas": ["Biceps", "Braquiorradial"]},

    # =========================================================
    # POSTERIOR DE COXA
    # =========================================================
    {"nome": "RDL (Romanian Dead Lift)", "grupo_muscular": "Posterior de coxa", "sinergistas": ["Gluteos", "Lombar"]},
    {"nome": "Mesa Flexora", "grupo_muscular": "Posterior de coxa", "sinergistas": []},
    {"nome": "Stiff", "grupo_muscular": "Posterior de coxa", "sinergistas": ["Gluteos", "Lombar"]},

    {"nome": "Flexora Sentada", "grupo_muscular": "Posterior de coxa", "sinergistas": []},
    {"nome": "Flexora Deitada", "grupo_muscular": "Posterior de coxa", "sinergistas": []},
    {"nome": "Flexora Unilateral", "grupo_muscular": "Posterior de coxa", "sinergistas": []},
    {"nome": "Good Morning", "grupo_muscular": "Posterior de coxa", "sinergistas": ["Gluteos", "Lombar"]},

    # =========================================================
    # GLUTEOS
    # =========================================================
    {"nome": "Hip Thrust", "grupo_muscular": "Gluteos", "sinergistas": ["Posterior de coxa"]},
    {"nome": "Elevacao Pelvica (ponte)", "grupo_muscular": "Gluteos", "sinergistas": ["Posterior de coxa"]},
    {"nome": "Abducao de Quadril (maquina)", "grupo_muscular": "Gluteos", "sinergistas": []},
    {"nome": "Agachamento Bulgaro (foco gluteo)", "grupo_muscular": "Gluteos", "sinergistas": ["Quadriceps", "Posterior de coxa"]},

    {"nome": "Gluteo na Maquina", "grupo_muscular": "Gluteos", "sinergistas": ["Posterior de coxa"]},
    {"nome": "Gluteo na Polia", "grupo_muscular": "Gluteos", "sinergistas": ["Posterior de coxa"]},
    {"nome": "Coice na Maquina", "grupo_muscular": "Gluteos", "sinergistas": ["Posterior de coxa"]},
    {"nome": "Passada no Smith", "grupo_muscular": "Gluteos", "sinergistas": ["Quadriceps", "Posterior de coxa"]},

    # =========================================================
    # PANTURRILHAS
    # =========================================================
    {"nome": "Panturrilha em Pe (gemeos)", "grupo_muscular": "Panturrilhas", "sinergistas": []},
    {"nome": "Panturrilha Sentado", "grupo_muscular": "Panturrilhas", "sinergistas": []},
    {"nome": "Panturrilha no Leg Press", "grupo_muscular": "Panturrilhas", "sinergistas": []},

    {"nome": "Panturrilha Sentado na Maquina", "grupo_muscular": "Panturrilhas", "sinergistas": []},
    {"nome": "Panturrilha em Pe na Maquina", "grupo_muscular": "Panturrilhas", "sinergistas": []},
    {"nome": "Panturrilha Unilateral", "grupo_muscular": "Panturrilhas", "sinergistas": []},

    # =========================================================
    # ABDOMEN
    # =========================================================
    {"nome": "Abdominal Crunch", "grupo_muscular": "Abdomen", "sinergistas": []},
    {"nome": "Elevacao de Pernas (leg raise)", "grupo_muscular": "Abdomen", "sinergistas": ["Flexores de quadril"]},
    {"nome": "Prancha (plank)", "grupo_muscular": "Abdomen", "sinergistas": ["Lombar", "Gluteos"]},
    {"nome": "Roda Abdominal (ab wheel)", "grupo_muscular": "Abdomen", "sinergistas": ["Ombros"]},
    {"nome": "Abdominal na Polia (cable crunch, ajoelhado)", "grupo_muscular": "Abdomen", "sinergistas": []},

    {"nome": "Abdominal na Maquina", "grupo_muscular": "Abdomen", "sinergistas": []},
    {"nome": "Abdominal na Polia em Pe", "grupo_muscular": "Abdomen", "sinergistas": []},
    {"nome": "Abdominal Reverse Crunch", "grupo_muscular": "Abdomen", "sinergistas": ["Flexores de quadril"]},
]


# =========================================================
# CADASTRO SEGURO
# =========================================================

cadastrados = 0
ignorados = 0

for dados_exercicio in exercicios:

    # Verifica se o exercício já existe pelo nome
    exercicio_existente = (
        db.query(Exercicio)
        .filter(Exercicio.nome == dados_exercicio["nome"])
        .first()
    )

    if exercicio_existente:
        print(f"[IGNORADO] Já existe: {dados_exercicio['nome']}")
        ignorados += 1
        continue

    # Cria o exercício
    novo_exercicio = Exercicio(
        nome=dados_exercicio["nome"],
        grupo_muscular=dados_exercicio["grupo_muscular"]
    )

    db.add(novo_exercicio)
    db.flush()

    # Adiciona os sinergistas
    for nome_sinergista in dados_exercicio["sinergistas"]:

        sinergista_existente = (
            db.query(ExercicioSinergista)
            .filter(
                ExercicioSinergista.exercicio_id == novo_exercicio.id,
                ExercicioSinergista.grupo_muscular == nome_sinergista
            )
            .first()
        )

        if not sinergista_existente:
            sinergista = ExercicioSinergista(
                exercicio_id=novo_exercicio.id,
                grupo_muscular=nome_sinergista
            )

            db.add(sinergista)

    cadastrados += 1
    print(f"[CADASTRADO] {dados_exercicio['nome']}")


# Salva tudo de uma vez
db.commit()

print("\n========================================")
print("CADASTRO FINALIZADO")
print("========================================")
print(f"Novos exercícios cadastrados: {cadastrados}")
print(f"Exercícios já existentes: {ignorados}")
print(f"Total na lista: {len(exercicios)}")
print("========================================")

db.close()