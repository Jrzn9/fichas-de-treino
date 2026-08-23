def criar_usuario_e_logar(client, email="user@example.com"):
    client.post("/usuarios/", json={"nome": "User", "email": email, "senha": "senha123"})
    login = client.post("/login", json={"email": email, "senha": "senha123"})
    return login.json()["access_token"]


def test_criar_e_listar_ficha(client):
    token = criar_usuario_e_logar(client)
    headers = {"Authorization": f"Bearer {token}"}

    resposta = client.post("/fichas", json={"nome": "Treino A"}, headers=headers)
    assert resposta.status_code == 200

    resposta = client.get("/fichas", headers=headers)
    assert resposta.status_code == 200
    assert len(resposta.json()) == 1


def test_usuario_nao_ve_ficha_de_outro(client):
    token_a = criar_usuario_e_logar(client, email="userA@example.com")
    token_b = criar_usuario_e_logar(client, email="userB@example.com")

    client.post("/fichas", json={"nome": "Treino do A"}, headers={"Authorization": f"Bearer {token_a}"})

    resposta = client.get("/fichas", headers={"Authorization": f"Bearer {token_b}"})
    assert resposta.status_code == 200
    assert len(resposta.json()) == 0
    # usuário B não vê a ficha do usuário A — confirma a autorização por dono


def test_fluxo_completo_ficha_exercicio_registro(client, admin_token):
    exercicio_resp = client.post(
        "/exercicios",
        json={"nome": "Supino Reto", "grupo_muscular": "Peito", "sinergistas": []},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    exercicio_id = exercicio_resp.json()["exercicio"]["id"]

    token = criar_usuario_e_logar(client, email="atleta@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    ficha_resp = client.post("/fichas", json={"nome": "Treino A"}, headers=headers)
    ficha_id = ficha_resp.json()["ficha"]["id"]

    vinculo_resp = client.post(
        f"/fichas/{ficha_id}/exercicios",
        json={"exercicio_id": exercicio_id, "series": 4, "repeticoes": 10, "carga": 60, "ordem": 1},
        headers=headers
    )
    assert vinculo_resp.status_code == 200
    vinculo_id = vinculo_resp.json()["ficha_exercicio"]["id"]

    registro_resp = client.post(
        f"/fichas/{ficha_id}/exercicios/{vinculo_id}/registros",
        json={"series_realizadas": 4, "repeticoes_realizadas": 10, "carga_realizada": 62.5},
        headers=headers
    )
    assert registro_resp.status_code == 200
    assert registro_resp.json()["registro"]["carga_realizada"] == 62.5