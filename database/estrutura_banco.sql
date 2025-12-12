-- ============================
-- Tabela de usuários
-- ============================
CREATE TABLE usuario (
    id CHAR(36) PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role ENUM('cliente', 'especialista', 'admin') NOT NULL,
    foto_url TEXT,
    telefone VARCHAR(20),
    status_aprovacao ENUM('pendente', 'aprovado', 'rejeitado') DEFAULT 'pendente',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ============================
-- Perfil Cliente
-- ============================
CREATE TABLE perfil_cliente (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    telefone VARCHAR(20),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- ============================
-- Perfil Especialista
-- ============================
CREATE TABLE perfil_especialista (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    area_profissional VARCHAR(30),
    bio TEXT,
    formacao VARCHAR(50),
    registro_prof VARCHAR(40),
    rating DECIMAL(3,2) DEFAULT 0.00,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- ============================
-- Admin Logs
-- ============================
CREATE TABLE admin (
    id CHAR(36) PRIMARY KEY,
    admin_id CHAR(36) NOT NULL,
    acao TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- ============================
-- Triagem
-- ============================
CREATE TABLE triagem (
    id CHAR(36) PRIMARY KEY,
    cliente_id CHAR(36) NOT NULL,
    status_triagem_status ENUM('iniciada', 'respondendo', 'concluida') DEFAULT 'iniciada',
    resumo_problema TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- ============================
-- Perguntas da triagem
-- ============================
CREATE TABLE perguntas_triagem (
    id CHAR(36) PRIMARY KEY,
    pergunta TEXT NOT NULL,
    resposta_padrao TEXT,
    categoria VARCHAR(30),
    ordem_pergunta INT,
    ativo BOOLEAN DEFAULT TRUE
);

-- ============================
-- Respostas da Triagem
-- ============================
CREATE TABLE triagem_resposta (
    id CHAR(36) PRIMARY KEY,
    triagem_id CHAR(36) NOT NULL,
    pergunta_triagem_id CHAR(36) NOT NULL,
    resposta_cliente TEXT,
    respondido_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (triagem_id) REFERENCES triagem(id) ON DELETE CASCADE,
    FOREIGN KEY (pergunta_triagem_id) REFERENCES perguntas_triagem(id) ON DELETE CASCADE
);

-- ============================
-- Tickets
-- ============================
CREATE TABLE ticket (
    id CHAR(36) PRIMARY KEY,
    cliente_id CHAR(36) NOT NULL,
    especialista_id CHAR(36),
    triagem_id CHAR(36),
    titulo VARCHAR(100) NOT NULL,
    descricao TEXT,
    status ENUM('aberto', 'aguardando', 'em_atendimento', 'concluido') DEFAULT 'aberto',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (especialista_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    FOREIGN KEY (triagem_id) REFERENCES triagem(id) ON DELETE SET NULL
);

-- ============================
-- Mensagens do Ticket
-- ============================
CREATE TABLE mensagens (
    id CHAR(36) PRIMARY KEY,
    ticket_id CHAR(36) NOT NULL,
    sender_id CHAR(36) NOT NULL,
    mensagem TEXT NOT NULL,
    tipo ENUM('texto', 'imagem', 'arquivo', 'audio') DEFAULT 'texto',
    enviado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES ticket(id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES usuarios(id) ON DELETE CASCADE
);
