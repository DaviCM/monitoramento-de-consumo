# <div align="center">API de Monitoramento de Consumo Liqua Monitor</div>

<div style="text-align:center; width:auto; height:auto">
    <img style="align:center; width:25%; height:auto" src="https://i.imgur.com/iB3ZRvo.png" >
</div>

Uma API desenvolvida com o objeto de fornecer um backend para o aplicativo móvel Liqua, um monitorador de consumos domésticos centrado na construção de um histórico de consumo visualizável para economia de água, luz e gás. 

Esse aplicativo foi construido para fins educacionais por alunos do 3º ano do Novo Ensino Médio, ao longo das aulas do curso Técnico em Desenvolvimento de Sistemas, realizado no SESI/SENAI-DF.

Como esse backend é exposto na forma de uma API standalone, ele não é dependente do frontend Liqua para sua execução. Excluindo casos de ambiente de desenvolvimento em que o link principal é desativado, você pode nos encontrar em https://liquamonitor.dev, ou [clicando aqui.](https://liquamonitor.dev)

Para visualizar o repositório da aplicação mobile Liqua Monitor para qualquer fim, [acesse esse link.](https://github.com/Pedro-D753/monitoramento-consumo-frontend) A interface, apesar de desacoplada, foi desenvolvida ao redor do padrão de resposta da API de Monitoramento de Consumo Liqua Monitor, e não funcionará caso o endereço da API estiver fora do ar, bem como se houver alteração nos endereços de query da interface.

## Features
- Cadastro, autenticação e edição de usuários;
- Manipulação completa de histórico de consumos reais, simulações e metas autoimpostas;
- Distribuição de Dicas Sutentáveis instanciadas diretamente via JSON;
- Validação de dados e tipagem com Pydantic para integridade do sistema;
- Exposição de endpoints consistentes de API para conexão com frontend;
- Envio de E-mail para recuperação de senha por meio de token Recovery JWT;
- Persistência de dados em banco remoto e versionamento de base de dados com Alembic.

## Principais Tecnologias Utilizadas
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17.9-4169E1?style=plastic&logo=postgresql)

![Redis](https://img.shields.io/badge/Redis-8.6.2-FF4438?style=plastic&logo=redis)

![Python](https://img.shields.io/badge/Python-3.13.13-3776AB?style=plastic&logo=python)

![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.46-D71F00?style=plastic&logo=sqlalchemy)

![Pydantic](https://img.shields.io/badge/Pydantic-2.12.5-E92063?style=plastic&logo=pydantic&logoColor=E92063)

![FastAPI](https://img.shields.io/badge/FastAPI-0.128.2-009688?style=plastic&logo=fastapi)

![JWT](https://img.shields.io/badge/JSON_Web_Token-RFC_7519-F7DF1E?style=plastic&logo=javascript)

![Caddy](https://img.shields.io/badge/Caddy-2.11.2-1F88C0?style=plastic&logo=caddy)

## Arquitetura do Sistema (em ambiente de desenvolvimento padrão)
```
.
└── monitoramento-de-consumo/
    ├── .venv/
    ├── alembic/
    ├── docs/
    ├── infra/
    │   ├── caddy/
    │   ├── docker/
    │   └── redis/
    ├── src/
    │   ├── api/
    │   ├── auth/
    │   ├── clients/
    │   ├── controllers/
    │   ├── database/
    │   ├── errors/
    │   ├── models/
    │   ├── schemas/
    │   ├── seeds/
    │   ├── templates/
    │   ├── validators/
    │   ├── __init__.py
    │   └── main.py
    ├── .env
    ├── .env.EXAMPLE
    ├── .gitignore
    ├── alembic.ini
    ├── README.md
    └── requirements.txt
```

## Documentação completa
A documentação completa desse sistema está disponível na pasta /docs, envolvendo diagramas de classe, caso de uso, banco de dados e a documentação completa do comportamento da API.

## Equipe Responsável pelo Projeto Liqua Monitor
### Desenvolvedores Backend
[Pedro Domiense](https://github.com/Pedro-D753)

[Davi Coelho](https://github.com/DaviCM/)

### Desenvolvedor Frontend
[Thiago Lucindo](https://github.com/Thiagoluma)

### Responsável pela Documentação
[Paulo Demeris](https://github.com/PauloD13)

