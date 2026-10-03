# Controle de Estoque — Flask + PostgreSQL

CRUD simples de produtos com Flask, frontend monolítico (Jinja + HTML + CSS + JS)
e arquitetura em camadas **controller → service → repository**.

## Responsabilidade de cada camada

| Camada         | Faz                                                                                    | Não faz                  |
| -------------- | -------------------------------------------------------------------------------------- | ------------------------ |
| **Controller** | Recebe a requisição, chama o service, renderiza template / redireciona                 | Regras de negócio, SQL   |
| **Service**    | Valida dados, aplica regras (nome único, preço > 0, quantidade ≥ 0, resumo do estoque) | Acessar `db.session`     |
| **Repository** | Consultas e gravações com Flask-SQLAlchemy                                             | Validar regra de negócio |

## Como rodar

### 1. Subir o PostgreSQL

Com Docker:

```bash
docker compose up -d
```

Ou use um PostgreSQL instalado localmente e crie o banco:

```sql
CREATE DATABASE loja;
```

### 2. Ambiente Python

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env      # ajuste usuário/senha se necessário
```

### 3. Executar

```powershell
python run.py
```

Acesse http://127.0.0.1:5000

## Rotas

| Método   | Rota                     | Descrição                          |
| -------- | ------------------------ | ---------------------------------- |
| GET      | `/produtos/`             | Lista produtos + resumo do estoque |
| GET/POST | `/produtos/novo`         | Cadastra produto                   |
| GET/POST | `/produtos/<id>/editar`  | Edita produto                      |
| POST     | `/produtos/<id>/excluir` | Exclui produto                     |
