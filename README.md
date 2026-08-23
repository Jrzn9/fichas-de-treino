# API de Fichas de Treino

> ⚠️ Projeto em desenvolvimento ativo. Novas funcionalidades estão sendo adicionadas continuamente.

API REST para gerenciamento de fichas de treino, construída com FastAPI e PostgreSQL, com autenticação segura via JWT.

## Sobre o projeto

Essa API permite que usuários se cadastrem, façam login e montem suas próprias fichas de treino a partir de um catálogo de exercícios — cada exercício já vem com seu grupo muscular principal e os músculos sinergistas associados, sem que o usuário final precise ter conhecimento de anatomia ou biomecânica para montar um treino completo.

O projeto nasce da observação de que muitas pessoas treinam de forma ineficiente — não necessariamente errada — e que exercícios fundamentais, bem executados e aplicados com consistência, são mais seguros e eficazes a longo prazo do que variações de efeito duvidoso. Por isso, o catálogo de exercícios é curado, priorizando movimentos com respaldo científico.

## Tecnologias utilizadas

- **FastAPI** — framework web para construção da API
- **PostgreSQL** — banco de dados relacional
- **SQLAlchemy** — ORM para modelagem e comunicação com o banco
- **Pydantic** — validação de dados de entrada e saída
- **JWT (python-jose)** — autenticação baseada em tokens
- **Passlib (bcrypt)** — hash seguro de senhas
- **python-dotenv** — gerenciamento de variáveis de ambiente
- **Pytest** — testes automatizados

## Funcionalidades já implementadas

- ✅ Cadastro de usuário, com senha protegida por hash bcrypt
- ✅ Login com geração de token JWT (expiração de 1h)
- ✅ Controle de acesso por papel (usuário comum vs. administrador)
- ✅ CRUD completo de exercícios (catálogo, restrito a administradores)
  - Cada exercício possui grupo muscular principal e lista de músculos sinergistas
- ✅ Catálogo de técnicas de treino (Cluster-set, Myo-reps, Back-off), com descrição e exemplo prático
- ✅ CRUD completo de fichas de treino (por usuário)
- ✅ Vínculo de exercícios a uma ficha, com séries, repetições, carga, ordem e técnica opcional
- ✅ Histórico de execuções de treino (registro real de séries/repetições/carga por sessão)
- ✅ Autorização por dono — cada usuário só acessa as próprias fichas
- ✅ Arquitetura organizada em routers (usuários, exercícios, fichas)
- ✅ Suíte de testes automatizados com pytest, cobrindo autenticação, autorização e o fluxo completo da API

## Funcionalidades planejadas

- 🔜 Objetivo de treino do usuário (hipertrofia/força, emagrecimento, manutenção, resistência/saúde)
- 🔜 Sugestão de progressão de carga (sobrecarga progressiva), adaptável ao objetivo do usuário
- 🔜 Perfil físico do usuário
- 🔜 Estatísticas de treino
- 🔜 Favoritar exercícios
- 🔜 Expansão do catálogo, incluindo exercícios voltados à saúde articular (ex: isometria)
- 🔜 Front-end (web e/ou mobile)
- 🔜 Automação com n8n (lembretes de treino via Telegram)
- 🔜 Suporte a treinos adaptados para condições específicas de saúde

## Modelo do banco de dados

O projeto conta com 7 tabelas principais:

- `usuarios`
- `exercicios`
- `exercicio_sinergistas`
- `tecnicas`
- `fichas_treino`
- `ficha_exercicios` (tabela associativa entre fichas e exercícios, com técnica opcional)
- `registros_treino` (histórico de execuções reais de treino)

## Segurança

- Senhas nunca são armazenadas em texto puro
- Chaves sensíveis (conexão com banco, chave de assinatura JWT) são gerenciadas via variáveis de ambiente, fora do controle de versão
- Autenticação obrigatória em rotas sensíveis
- Controle de acesso por papel, restringindo operações administrativas
