## 📂 api

Onde ficam os endpoints (rotas HTTP).
Normalmente cada arquivo dentro dessa pasta corresponde a um “módulo” ou “recurso” da API (ex: users.py, animals.py, auth.py).
Aqui você só declara as rotas, valida inputs (via schemas) e chama a lógica de negócio (via crud ou services).

## 📂 crud

CRUD = Create, Read, Update, Delete.
Contém funções diretas de acesso ao banco de dados.
É o nível que traduz chamadas da API em queries de banco.
Exemplo: get_user_by_id(db, user_id), create_animal(db, data) etc.
Se você estivesse usando Mongo, aqui entrariam os find, insert_one, update_one, etc.

## 📂 models

Representa a estrutura dos dados no banco.
No caso de SQLAlchemy, são as classes que mapeiam tabelas.
Com Mongo (e Motor/Pydantic), você pode ter dataclasses ou pydantic.BaseModel que descrevem os documentos.
A ideia é: “como o dado existe dentro do banco”.

## 📂 schemas

Define os modelos Pydantic usados para validar entrada e saída de dados.
Diferente de models, que é banco, aqui é API.
Exemplo: UserCreate, UserResponse.
Ajuda a separar regras de banco vs. regras de exposição na API.

## 📂 services

Camada de lógica de negócio.
Fica entre api e crud.
Exemplo: ao cadastrar um animal, pode precisar:
validar se o usuário tem permissão,
chamar crud para salvar,
enviar notificação.
Essa lógica não deveria estar nem no api (que só roteia) nem no crud (que só fala com banco), por isso nasce o services.

## 🚀 Em resumo:

- _api_ → define os endpoints
- _schemas_ → valida entrada/saída da API
- _services_ → lógica de negócio
- _crud_ → conversa com banco
- _models_ → descreve os dados no banco

É um padrão chamado de camadas (layered architecture) → ajuda a manter o código limpo, testável e escalável.

```
vet_plus_backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   │
│   ├── api/                 ← Endpoints/rotas
│   │   ├── __init__.py
│   │   ├── users.py
│   │   ├── animals.py
│   │   └── auth.py
│   │
│   ├── crud/                ← Operações de banco
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── animals.py
│   │
│   ├── models/              ← Estrutura dos dados
│   │   ├── __init__.py
│   │   ├── users.py
│   │   ├── animals.py
│   │   └── appointment.py
│   │
│   ├── schemas/             ← Validação API (Pydantic)
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── animals.py
│   │
│   ├── services/            ← Lógica de negócio
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── animal_service.py
│   │
│   ├── core/            ← core functions
│   │   ├── __init__.py
│   │   └── db_setup.py
│
├── requirements.txt
└── .env
```