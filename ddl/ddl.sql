-- Tabela: reviews (Originada das colunas 'Reviews', 'Positive' e 'Negative')
CREATE TABLE reviews (
    id BIGSERIAL PRIMARY KEY,
    appid BIGINT NOT NULL,
    review_text TEXT,
    positive INT DEFAULT 0 CHECK (positive >= 0),
    negative INT DEFAULT 0 CHECK (negative >= 0)
    -- Descomentar linha abaixo quando a tabela principal 'game' for criada pela equipe
    -- CONSTRAINT fk_reviews_game FOREIGN KEY (appid) REFERENCES game(appid)  # PESQUISAR O QUE ESSA LINHA FAZ
);

-- Tabela: metacritic (Originada das colunas 'Metacritic url' e 'Metacritic score')
CREATE TABLE metacritic (
    id BIGSERIAL PRIMARY KEY,
    appid BIGINT NOT NULL,
    metacritic_url TEXT,
    metacritic_score NUMERIC CHECK (metacritic_score >= 0 AND metacritic_score <= 100)
    -- Descomentar a linha abaixo quando a tabela principal 'game' for criada pela equipe
    -- CONSTRAINT fk_metacritic_game FOREIGN KEY (appid) REFERENCES game(appid)
);


-- Tabela: categories (Nome da coluna do CSV em minúsculo)
CREATE TABLE categories (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- Tabela: game_categories
CREATE TABLE game_categories (
    id BIGSERIAL PRIMARY KEY,
    appid BIGINT NOT NULL, -- (BATE COM REVIEWS E METACRITIC)
    category_id BIGINT NOT NULL,
    CONSTRAINT fk_gc_categories FOREIGN KEY (category_id) REFERENCES categories(id)
    -- CONSTRAINT fk_gc_game FOREIGN KEY (appid) REFERENCES games(appid)
);

-- Criação de Índices para Performance
CREATE INDEX idx_reviews_appid ON reviews(appid);
CREATE INDEX idx_metacritic_appid ON metacritic(appid);
CREATE INDEX idx_game_categories_appid ON game_categories(appid);