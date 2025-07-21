# Sistema de Gerenciamento de Biblioteca Digital

[![🔥 Siga meu GitHub](https://img.shields.io/badge/👉🏼-GitHub-white)](https://www.github.com/fcardan)  
[![🔥 Siga meu Linkedin](https://img.shields.io/badge/👉🏼-Linkedin-blue)](https://www.linkedin.com/in/fcardan)  
[![⭐ en-us](https://img.shields.io/badge/👉🏼-EnUS-red)](https://github.com/fcardan/api-library-management)
[![⭐ Star](https://img.shields.io/github/stars/fcardan/api-library-management)](https://github.com/fcardan/api-library-management)

## 🔹 Sumário

- [Visão Geral](#visão-geral)  
- [Recursos](#recursos)  
- [Stack de Tecnologias](#stack-de-tecnologias)  
- [Estrutura do Projeto](#estrutura-do-projeto)  
- [Configuração do Banco de Dados](#configuração-do-banco-de-dados)  
- [Instalação & Uso](#instalação--uso)  
- [Endpoints da API](#endpoints-da-api)  

---

## Visão Geral

api-library-management é uma API RESTful em Python criada para gerenciar as operações de um sistema de biblioteca — desde livros até empréstimos — projetada com arquitetura limpa, acesso seguro e escalabilidade em mente.

---

## Recursos

- Gerenciamento de usuários: listar, criar, consultar, atualizar, remover  
- Catálogo de autores: CRUD completo  
- Catálogo de livros: listar, criar, consultar, atualizar, remover; verificação de disponibilidade  
- Ciclo de empréstimos: emprestar, devolver (cálculo de multa), listar ativos/atrasados, histórico do usuário  
- Regras de negócio:  
  - Prazo de empréstimo de 14 dias  
  - Multa de R$ 2,00/dia  
  - Máximo de 3 empréstimos ativos por usuário  
- Extras: paginação, limitação de taxa (rate limiting), logs estruturados, autenticação JWT, Swagger UI

---

## Stack de Tecnologias

| Camada             | Tecnologia / Biblioteca        |
|-------------------:|--------------------------------|
| Linguagem          | Python 3.11+                   |
| Framework          | FastAPI                        |
| Validação          | Pydantic                       |
| ORM                | SQLAlchemy                     |
| Banco de Dados     | MySQL                          |
| Documentação API   | FastAPI OpenAPI / Swagger UI   |
| Rating Limiting    | SlowAPI                        |
| Export PDF         | FPDF                           |
| Logging            | structlog                      |

---

## Estrutura do Projeto

Veja abaixo o layout de pastas e arquivos:

~~~text
library-management/
├── db/
│   ├── 01_create_tables.sql
│   └── 02_create_indexes.sql
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   └── auth.py
│   │   │   └── authors.py
│   │   │   └── books.py
│   │   │   └── loans.py
│   │   │   └── router.py
│   │   │   └── reports.py
│   │   │   └── users.py
│   ├── core/
│   │   ├── .env
│   │   ├── logging.py
│   │   ├── security.py
│   │   ├── settings.py
│   ├── db/
│   │   ├── base.py
│   │   ├── init_db.py
│   │   ├── session.py
│   ├── dependencies/
│   │   └── auth.py
│   ├── models/
│   │   ├── author_model.py
│   │   ├── book_model.py
│   │   └── loan_model.py
│   │   ├── user_model.py
│   ├── schemas/
│   │   ├── author_schema.py
│   │   ├── book_schema.py
│   │   └── loan_schema.py
│   │   ├── user_schema.py
│   ├── services/
│   │   ├── author_service.py
│   │   ├── book_service.py
│   │   └── loan_service.py
│   │   └── report_service.py
│   │   ├── user_service.py
│   ├── utils/
│   │   └── export.py
├── tests/
│   ├── test_user.py
│   ├── test_book.py
│   └── test_loan.py
├── main.py
├── requirements.txt
└── README.md
└── README-ptbr.md
└── LICENSE.md
└── Insomnia_library-api.yaml
~~~

---

## Configuração do Banco de Dados

~~~sql
CREATE DATABASE IF NOT EXISTS library_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- então execute:
-- mysql -u root -p library_db < db/01_create_tables.sql
-- mysql -u root -p library_db < db/02_create_indexes.sql
~~~

---

## Instalação & Uso

~~~bash
git clone https://github.com/fcardan/api-library-management.git
cd api-library-management
# edite o .env com suas credenciais
pip install -r requirements.txt
uvicorn main:app --reload
~~~

Acesse o Swagger UI em `http://localhost:8000/docs`

---

## Endpoints da API

#### Autenticação
- **Login**: `🟢 POST /auth/token`  
  Autentica usuário e senha para obter token Bearer

#### Usuários
- **Criar Usuário**: `🟢 POST /users`  
- **Listar Usuários**: `🟣 GET /users`  
- **Obter Usuário por ID**: `🟣 GET /users/{user_id}`  
- **Listar Empréstimos do Usuário**: `🟣 GET /users/{user_id}/loans`  
- **Atualização Completa do Usuário**: `🟠 PUT /users/{user_id}`  
- **Atualização Parcial do Usuário**: `🟡 PATCH /users/{user_id}`  
- **Remover Usuário**: `🔴 DELETE /users/{user_id}`  

#### Autores
- **Criar Autor**: `🟢 POST /authors`  
- **Listar Autores**: `🟣 GET /authors`  
- **Obter Autor por ID**: `🟣 GET /authors/{author_id}`  
- **Listar Livros do Autor**: `🟣 GET /authors/{author_id}/books`  
- **Atualização Completa do Autor**: `🟠 PUT /authors/{author_id}`  
- **Atualização Parcial do Autor**: `🟡 PATCH /authors/{author_id}`  
- **Remover Autor**: `🔴 DELETE /authors/{author_id}`  

#### Livros
- **Criar Livro**: `🟢 POST /books`  
- **Listar Livros**: `🟣 GET /books`  
- **Obter Livro por ID**: `🟣 GET /books/{book_id}`  
- **Listar Livros por Disponibilidade**: `🟣 GET /books/available?status={boolean}`  
- **Atualização Completa do Livro**: `🟠 PUT /books/{book_id}`  
- **Atualização Parcial do Livro**: `🟡 PATCH /books/{book_id}`  
- **Remover Livro**: `🔴 DELETE /books/{book_id}`  

#### Empréstimos
- **Criar Empréstimo**: `🟢 POST /loans`  
- **Listar Todos os Empréstimos**: `🟣 GET /loans`  
- **Obter Empréstimo por ID**: `🟣 GET /loans/{loan_id}`  
- **Listar Empréstimos Ativos**: `🟣 GET /loans/active/{user_id}`  
- **Listar Empréstimos Atrasados**: `🟣 GET /loans/overdue/{user_id}`  
- **Listar Histórico de Empréstimos**: `🟣 GET /loans/history/{user_id}`  
- **Atualização Completa do Empréstimo**: `🟠 PUT /loans/{loan_id}`  
- **Atualização Parcial do Empréstimo**: `🟡 PATCH /loans/{loan_id}`  
- **Remover Empréstimo**: `🔴 DELETE /loans/{loan_id}`  

#### Relatórios
- **Exportar CSV - Livros**: `🟣 GET /reports/books/csv`  
- **Exportar PDF - Completo**: `🟣 GET /reports/full/pdf`  

### OBSERVAÇÕES:

- **Autenticação**: Todos os endpoints (exceto POST /auth/token) exigem um token Bearer JWT válido no cabeçalho Authorization.

- **Segurança no Login**: O endpoint POST /auth/token é limitado a 10 requisições por minuto por IP para proteger contra ataques de força‑bruta e credential stuffing.

#### Limites de Taxa

- Endpoints GET (listagens) → 50 requisições/minuto por cliente

- POST, PUT, PATCH, DELETE → 20 requisições/minuto por cliente

- **Paginação**: Suportada em GET /books e GET /books/available pelos parâmetros de consulta skip e limit.

- **Ordenação**: Disponível nesses endpoints de listagem via parâmetro order_by (por exemplo, order_by=title, order_by=published_date, order_by=total_copies).

---

### Exemplos de Requisição

#### Requisição de Autenticação
~~~http
POST /auth/token HTTP/1.1
Content-Type: application/x-www-form-urlencoded

username=seuemail&password=suasenha
~~~

#### Criação de Livro
~~~json
{
  "title": "Livro Exemplo",
  "author_id": "003055e6-372f-475d-a6ce-46e7d0def925",
  "published_date": "2023-01-15",
  "total_copies": 5,
  "available_copies": 5
}
~~~

#### Criação de Empréstimo
~~~json
{
  "user_id": "040446ef-7338-4351-955b-c94406332c9b",
  "book_id": "322b0e8b-cb0e-460d-bb5e-0987a3ba6eb3",
  "loan_date": "2025-07-15"
}
~~~

#### Atualização Parcial de Empréstimo
~~~json
{
  "return_date": "2025-07-30"
}
~~~

### Variáveis de Ambiente
~~~text
base_url: http://127.0.0.1:8000/api/v1
token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
user_id: 040446ef-7338-4351-955b-c94406332c9b
book_id: 71c10dad-9ea7-45a1-92a9-1dffeeb9e614
author_id: 003055e6-372f-475d-a6ce-46e7d0def925
loan_id: 841b0c6f-2e6e-4ce3-97a9-336402f2d6c4
~~~

---

### Especificações Técnicas

#### 1. Autenticação
- **Tipo**: Token Bearer (JWT)  
- **Obrigatório**: para todos os endpoints, exceto `/auth/token`  
- **Formato do Header**:  
  `Authorization: Bearer <seu_token>`

#### 2. Formatos de Requisição
| Tipo de Endpoint      | Content-Type                       | Formato do Corpo   |
|-----------------------|------------------------------------|--------------------|
| Maioria dos endpoints | `application/json`                 | JSON               |
| Autenticação          | `application/x-www-form-urlencoded`| Form URL encoded   |

#### 3. Métodos HTTP
| Método  | Uso Típico                         | Exemplos de Endpoints             |
|---------|------------------------------------|-----------------------------------|
| 🟢 POST | Criar novos recursos               | `/users`, `/books`, `/loans`      |
| 🟣 GET  | Recuperar recursos                 | `/users/{id}`, `/books/available` |
| 🟠 PUT  | Atualização completa de recurso    | `/users/{id}`, `/loans/{id}`      |
| 🟡 PATCH| Atualização parcial de recurso     | `/books/{id}`, `/authors/{id}`    |
| 🔴 DELETE| Remover recursos                  | `/authors/{id}`, `/loans/{id}`    |

#### 4. Parâmetros de Consulta
| Parâmetro | Endpoint                       | Valores       | Descrição                         |
|-----------|--------------------------------|---------------|-----------------------------------|
| `status`  | `GET /books/available`         | `true/false`  | Filtrar livros por disponibilidade|

#### 5. Parâmetros de Caminho
| Parâmetro     | Tipo de Recurso | Exemplo de Endpoint                |
|---------------|-----------------|------------------------------------|
| `{user_id}`   | Usuário         | `GET /users/{user_id}/loans`       |
| `{book_id}`   | Livro           | `PATCH /books/{book_id}`           |
| `{author_id}` | Autor           | `GET /authors/{author_id}/books`   |
| `{loan_id}`   | Empréstimo      | `PUT /loans/{loan_id}`             |

#### 6. Formatos de Resposta
- **Sucesso**: Payload JSON com dados do recurso  
- **Erros**: Códigos HTTP padrão (4xx/5xx) com detalhes em JSON  
- **Erros de Validação**: `422 Unprocessable Entity` com mensagens por campo

#### 7. Estrutura da URL Base

`{{base_url}}/api/v1/<caminho_do_endpoint>`

---

### Guia de Importação da Coleção Insomnia (v11.2.0)

#### Passo 1: Baixar o Arquivo RAW
~~~bash
1. Abra o link no GitHub:  
   [Insomnia Collection](https://github.com/fcardan/api-library-management/blob/main/Insomnia_library-api.yaml)  
2. Clique em “Raw” (canto superior direito)  
3. Pressione `Ctrl+S` (Windows/Linux) ou `Cmd+S` (Mac) para salvar  
4. Verifique se o nome do arquivo é `Insomnia_library-api.yaml` (sem extensão .txt)  
~~~

#### Passo 2: Importar no Insomnia
~~~bash
1. Abra o Insomnia v11.2.0+  
2. No workspace ativo:  
   • Selecione Import/Export → Import Data  
~~~

#### Passo 3: Configurar Importação
~~~bash
Na janela de importação:  
1. Selecione a guia “File”  
2. Clique em “Select File” → escolha o .yaml baixado  
3. Clique em “Scan”  
~~~

---

## Obrigado por conferir ❤️

### Gostou do projeto?

- ➡️ **Siga**: [@fcardan](https://github.com/fcardan)  
- ⭐ **Dê uma estrela**: para apoiar futuras atualizações!  
- 🔀 **Faça um fork**: para customizar conforme suas necessidades!

---

## Licença

Este repositório está licenciado. Você pode compartilhar e adaptar este conteúdo para qualquer finalidade, até mesmo comercial, desde que forneça crédito apropriado ao autor original. Para mais detalhes, consulte o arquivo [LICENSE.md](https://github.com/fcardan/api-library-management/blob/main/LICENSE.md).
