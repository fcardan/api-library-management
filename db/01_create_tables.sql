-- 01_create_tables.sql

-- Criação da tabela de usuários
CREATE TABLE IF NOT EXISTS users (
  id CHAR(36)        NOT NULL PRIMARY KEY,        -- UUID do usuário
  name VARCHAR(255)  NOT NULL,                   -- Nome completo do usuário
  email VARCHAR(255) NOT NULL UNIQUE,            -- E‑mail único
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP  -- Data de criação do registro
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Criação da tabela de autores
CREATE TABLE IF NOT EXISTS authors (
  id CHAR(36)       NOT NULL PRIMARY KEY,        -- UUID do autor
  name VARCHAR(255) NOT NULL,                    -- Nome do autor
  bio TEXT                                       -- Biografia ou descrição do autor
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Criação da tabela de livros
CREATE TABLE IF NOT EXISTS books (
  id CHAR(36)            NOT NULL PRIMARY KEY,   -- UUID do livro
  title VARCHAR(255)     NOT NULL,               -- Título do livro
  author_id CHAR(36)     NOT NULL,               -- UUID do autor (FK)
  published_date DATE    NOT NULL,               -- Data de publicação
  available_copies INT   NOT NULL DEFAULT 0,     -- Quantidade de cópias disponíveis
  total_copies INT       NOT NULL DEFAULT 0,     -- Quantidade total de cópias
  CONSTRAINT fk_books_author
    FOREIGN KEY (author_id) REFERENCES authors(id)
    ON DELETE RESTRICT ON UPDATE CASCADE         -- Restrições de integridade referencial
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Criação da tabela de empréstimos
CREATE TABLE IF NOT EXISTS loans (
  id CHAR(36)               NOT NULL PRIMARY KEY,  -- UUID do empréstimo
  user_id CHAR(36)          NOT NULL,             -- UUID do usuário (FK)
  book_id CHAR(36)          NOT NULL,             -- UUID do livro (FK)
  loan_date DATE            NOT NULL,             -- Data de início do empréstimo
  due_date DATE             NOT NULL,             -- Data de vencimento
  return_date DATE,                               -- Data de devolução (nulo se ainda não devolvido)
  fine_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00,-- Valor da multa calculada
  CONSTRAINT fk_loans_user
    FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE RESTRICT ON UPDATE CASCADE,          -- Integridade referencial usuário→empréstimo
  CONSTRAINT fk_loans_book
    FOREIGN KEY (book_id) REFERENCES books(id)
    ON DELETE RESTRICT ON UPDATE CASCADE           -- Integridade referencial livro→empréstimo
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
