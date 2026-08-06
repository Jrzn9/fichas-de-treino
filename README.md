# API de Fichas de Treino

> ⚠️ Projeto em desenvolvimento ativo. Novas funcionalidades estão sendo adicionadas continuamente.

API REST para gerenciamento de fichas de treino, construída com FastAPI e PostgreSQL, com autenticação segura via JWT.

## Sobre o projeto

Essa API permite que usuários se cadastrem, façam login e montem suas próprias fichas de treino a partir de um catálogo de exercícios — cada exercício já vem com seu grupo muscular principal e os músculos sinergistas associados, sem que o usuário final precise ter conhecimento de anatomia ou biomecânica para montar um treino completo.

## Tecnologias utilizadas

- **FastAPI** — framework web para construção da API
- **PostgreSQL** — banco de dados relacional
- **SQLAlchemy** — ORM para modelagem e comunicação com o banco
- **Pydantic** — validação de dados de entrada e saída
- **JWT (python-jose)** — autenticação baseada em tokens
- **Passlib (bcrypt)** — hash seguro de senhas
- **python-dotenv** — gerenciamento de variáveis de ambiente

## Funcionalidades já implementadas

- ✅ Cadastro de usuário, com senha protegida por hash bcrypt
- ✅ Login com geração de token JWT (expiração de 1h)
- ✅ Rotas protegidas por autenticação
- ✅ CRUD de exercícios (criar, listar, buscar por ID, editar)
  - Cada exercício possui grupo muscular principal e lista de músculos sinergistas

## Funcionalidades planejadas

- 🔜 Exclusão de exercícios (`DELETE`)
- 🔜 CRUD completo de fichas de treino
- 🔜 Vínculo de exercícios a uma ficha (com séries, repetições, carga e ordem)
- 🔜 Autorização por dono — cada usuário só acessa as próprias fichas
- 🔜 Catálogo de exercícios pré-populado
- 🔜 Documentação interativa via Swagger (`/docs`)

## Modelo do banco de dados

O projeto conta com 5 tabelas principais:

- `usuarios`
- `exercicios`
- `exercicio_sinergistas`
- `fichas_treino`
- `ficha_exercicios` (tabela associativa entre fichas e exercícios)

## Segurança

- Senhas nunca são armazenadas em texto puro
- Chaves sensíveis (conexão com banco, chave de assinatura JWT) são gerenciadas via variáveis de ambiente, fora do controle de versão
- Autenticação obrigatória em rotas sensíveis
