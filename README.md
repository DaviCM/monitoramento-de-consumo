# API de Monitoramento de Consumo do Liqua

Uma API desenvolvida com o objeto de fornecer um backend para o aplicativo móvel Liqua, um monitorador de consumos domésticos centrado na construção de um histórico de consumo visualizável para economia de água, luz e gás. 

Esse aplicativo foi construido para fins educacionais por alunos do 3º ano do Novo Ensino Médio, ao longo das aulas do curso Técnico em Desenvolvimento de Sistemas, realizado no SESI/SENAI-DF.

Essa aplicação é standalone como API, e não é dependente do frontend Liqua para sua execução.

## Features
- Cadastro e autenticação de usuários;
- Manipulação completa de histórico de consumos reais, simulações e metas autoimpostas;
- Distribuição de Dicas Sutentáveis instanciadas diretamente via JSON;
- Validação de dados e tipagem com Pydantic para integridade do sistema;
- Exposição de endpoints consistentes de API para conexão com frontend;
- Envio de E-mail para recuperação de senha por meio de token Recovery JWT;
- Persistência de dados em banco remoto e versionamento de base de dados com Alembic.

## Principais Tecnologias Utilizadas
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17.8-4169E1?style=plastic&logo=postgresql)

![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.46-D71F00?style=plastic&logo=sqlalchemy)

![Python](https://img.shields.io/badge/Python-3.13.5-3776AB?style=plastic&logo=python)

![Pydantic](https://img.shields.io/badge/Pydantic-2.12.5-E92063?style=plastic&logo=pydantic&logoColor=E92063)

![FastAPI](https://img.shields.io/badge/FastAPI-0.128.2-009688?style=plastic&logo=fastapi)

![JWT](https://img.shields.io/badge/JSON_Web_Token-RFC_7519-F7DF1E?style=plastic&logo=javascript)

## Arquitetura do Sistema (em ambiente de desenvolvimento padrão)
```
└── monitoramento-de-consumo/
    ├── .venv/
    ├── alembic/
    ├── src/
    │   ├── api/
    │   ├── auth/
    │   ├── controllers/
    │   ├── database/
    │   ├── editors/
    │   ├── errors/
    │   ├── models/
    │   ├── schemas/
    │   ├── validators/
    │   ├── __init__.py
    │   └── main.py
    ├── .env
    ├── .env.EXAMPLE
    ├── .gitignore
    ├── alembic.ini
    └── requirements.txt
```

## Documentação completa
A documentação completa desse sistema estará disponível na pasta [/docs](/docs) ao final do desenvolvimento.

## Equipe Responsável pelo Projeto Liqua
### Desenvolvedores Backend
[Pedro Domiense](https://github.com/Pedro-D753)

[Davi Coelho](https://github.com/DaviCM/)

### Desenvolvedor Frontend
[Thiago Lucindo](https://github.com/Thiagoluma)

### Responsável pela Documentação
[Paulo Demeris](https://github.com/PauloD13)

