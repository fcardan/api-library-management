-- 02_create_indexes.sql

-- Índice para acelerar buscas de empréstimos por usuário
CREATE INDEX idx_loans_user_id ON loans(user_id);

-- Índice para acelerar buscas de empréstimos por livro
CREATE INDEX idx_loans_book_id ON loans(book_id);

-- Índice para consultas de disponibilidade de livros
CREATE INDEX idx_books_available ON books(available_copies);

-- Índice composto para otimizar consultas de empréstimos vencidos
CREATE INDEX idx_loans_overdue ON loans(due_date, return_date);
