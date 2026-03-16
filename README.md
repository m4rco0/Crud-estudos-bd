# Loja DB - CRUD de Estudos para Banco de Dados

## Tecnologias Utilizadas
- **FastAPI**:
- **SQLAlchemy**
- **PostgreSQL**
- **Pydantic**
- **Poetry**
- **Pytest**
- **AWS**

## Estrutura do Projeto
```
.
├── loja_db/           # Núcleo da aplicação
│   ├── app.py         # Endpoints e rotas da API
│   ├── database.py    # Configuração da Engine e Sessão
│   ├── models.py      # Modelos do SQLAlchemy (Tabelas)
│   ├── schemas.py     # Modelos do Pydantic (Validação/DTOs)
│   └── settings.py    # Configurações de ambiente (Pydantic Settings)
├── migrations/        # Histórico de versões do banco (Alembic)
├── tests/             # Testes de integração e unitários
├── htmlcov/           # Relatórios de cobertura de testes (Coverage)
├── .env               # Cole sua .env aqui
├── pyproject.toml     # Dependências do Poetry
└── alembic.ini        # Configuração do Alembic
```

## Como Instalar e Rodar
Pre-requisito de configuração de ambiente:
[poetry](https://python-poetry.org/)
1. Clonar repositório
```Bash
git clone https://github.com/seu-usuario/loja-db.git
cd loja-db
```
2. Criando .env
```
# --- Template de configuração (Copie para .env e preencha) ---
DB_USER=""
DB_PASSWD=""
RDS_ENDPOINT=""
RDS_PORT=5432
DB_NAME="postgres"
DATABASE_URL="postgresql+psycopg2://${DB_USER}:${DB_PASSWD}@${RDS_ENDPOINT}:${RDS_PORT}/${DB_NAME}"
```

2. Configurar o ambiente com Poetry
```Bash
poetry install
```
3. Executando a API
```Bash
poetry run task run     # Rodar o backend
poetry run task lint    # Verificar a syntax
poetry run task test    # Executar testes unitarios
```

Acesse a documentação interavia em: http://127.0.0.1:8000/docs


