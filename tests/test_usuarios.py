def test_criar_usuario_email_duplicado(client):
    client.post("/usuarios/", json={
        "nome": "Teste",
        "email": "teste@example.com",
        "senha": "senha123"
    })

    resposta = client.post("/usuarios/", json={
        "nome": "Outro",
        "email": "teste@example.com",
        "senha": "outrasenha"
    })

    assert resposta.status_code == 400
    assert resposta.json()["detail"] == "Email já cadastrado"


def test_login_sucesso(client):
    client.post("/usuarios/", json={
        "nome": "Teste",
        "email": "teste@example.com",
        "senha": "senha123"
    })

    resposta = client.post("/login", json={
        "email": "teste@example.com",
        "senha": "senha123"
    })

    assert resposta.status_code == 200
    dados = resposta.json()
    assert "access_token" in dados
    assert dados["token_type"] == "bearer"


def test_login_senha_errada(client):
    client.post("/usuarios/", json={
        "nome": "Teste",
        "email": "teste@example.com",
        "senha": "senha123"
    })

    resposta = client.post("/login", json={
        "email": "teste@example.com",
        "senha": "senhaerrada"
    })

    assert resposta.status_code == 401