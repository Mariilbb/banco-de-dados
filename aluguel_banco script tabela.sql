create DATABASE aluguel_bancos;

use aluguel_banco;

CREATE TABLE pessoas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(100),
    endereco VARCHAR(255)
);

CREATE TABLE corretores (
    id INT PRIMARY KEY,
    creci VARCHAR(20) UNIQUE NOT NULL,
    FOREIGN KEY (id) REFERENCES pessoas(id) ON DELETE CASCADE
);

CREATE TABLE proprietarios (
    id INT PRIMARY KEY,
    FOREIGN KEY (id) REFERENCES pessoas(id) ON DELETE CASCADE
);

CREATE TABLE inquilinos (
    id INT PRIMARY KEY,
    FOREIGN KEY (id) REFERENCES pessoas(id) ON DELETE CASCADE
);

CREATE TABLE imoveis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(255),
    endereco VARCHAR(255),
    valor FLOAT,
    tipo VARCHAR(50),
    proprietario_id INT,
    inquilino_id INT,
    FOREIGN KEY (proprietario_id) REFERENCES proprietarios(id) ON DELETE SET NULL,
    FOREIGN KEY (inquilino_id) REFERENCES inquilinos(id) ON DELETE SET NULL
);
