def test_criar_exercicio_sem_login_falha(client):
    resposta = client.post("/exercicios", json={
        "nome": "Supino Reto",
        "grupo_muscular": "Peito",
        "sinergistas": ["Ombros", "Triceps"]
    })
    assert resposta.status_code == 401


def test_criar_exercicio_usuario_comum_falha(client):
    client.post("/usuarios/", json={
        "nome": "Comum",
        "email": "comum@example.com",
        "senha": "senha123"
    })
    login = client.post("/login", json={"email": "comum@example.com", "senha": "senha123"})
    token = login.json()["access_token"]

    resposta = client.post(
        "/exercicios",
        json={"nome": "Supino Reto", "grupo_muscular": "Peito", "sinergistas": []},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resposta.status_code == 403


def test_criar_exercicio_admin_sucesso(client, admin_token):
    resposta = client.post(
        "/exercicios",
        json={"nome": "Supino Reto", "grupo_muscular": "Peito", "sinergistas": ["Ombros", "Triceps"]},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resposta.status_code == 200
    dados = resposta.json()["exercicio"]
    assert dados["nome"] == "Supino Reto"
    assert "Ombros" in dados["sinergistas"]


def test_listar_exercicios(client, admin_token):
    client.post(
        "/exercicios",
        json={"nome": "Supino Reto", "grupo_muscular": "Peito", "sinergistas": []},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    resposta = client.get("/exercicios")
    assert resposta.status_code == 200
    assert len(resposta.json()) == 1