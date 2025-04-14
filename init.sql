CREATE TABLE IF NOT EXISTS Usuario (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(100) NOT NULL,
    nivel INTEGER DEFAULT 1,
    experiencia INTEGER DEFAULT 0,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_usuario_email ON Usuario(email);

CREATE TABLE IF NOT EXISTS UsuarioInventario (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES Usuario(id),
    item_id INTEGER NOT NULL,
    quantidade INTEGER DEFAULT 1,
    data_adicao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_inventario_usuario_id ON UsuarioInventario(usuario_id);

-- Inserir usuário de teste, caso não exista
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM Usuario WHERE email = 'teste@email.com'
    ) THEN
        INSERT INTO Usuario (nome, email, senha)
        VALUES ('Usuário Teste', 'teste@email.com', 'senha123');
    END IF;
END;
$$;