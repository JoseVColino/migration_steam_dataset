-- Criação da tabela principal
CREATE TABLE game (
    appid INT PRIMARY KEY,
    name VARCHAR(255),
    release_date VARCHAR(50),
    estimated_owners_min INT,
    estimated_owners_max INT,
    peak_ccu INT,
    required_age INT,
    price NUMERIC(10, 2),
    discount INT,
    dlc_count INT,
    about_the_game TEXT,
    website TEXT,
    achievements INT,
    recommendations INT,
    support_email TEXT,
    support_url TEXT,
    notes TEXT,
    score_rank INT,
    header_image TEXT,
    median_playtime_forever INT,
    median_playtime_two_weeks INT,
    average_playtime_forever INT,
    average_playtime_two_weeks INT
);
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


-- Criação da tabela de domínio (Tags)
CREATE TABLE tags (
    id INT PRIMARY KEY,
    name VARCHAR(255)
);

-- Criação da tabela de relacionamento (Game_Tag)
CREATE TABLE game_tag (
    id_game INT,
    id_tag INT,
    PRIMARY KEY (id_game, id_tag),
    FOREIGN KEY (id_game) REFERENCES game(appid),
    FOREIGN KEY (id_tag) REFERENCES tags(id)
);


CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    movie_url TEXT NOT NULL,
    jogo_id INT REFERENCES game(appid) NOT NULL
);

CREATE TABLE company (
     id SERIAL PRIMARY KEY,
     name TEXT NOT NULL
);

CREATE TABLE game_company (
    id SERIAL PRIMARY KEY,
    id_game INT REFERENCES game(appid) NOT NULL,
    id_company INT REFERENCES company(id) NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('developer', 'publisher'))
);

CREATE TABLE generos (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE game_generos (
    id SERIAL PRIMARY KEY,
    id_game INT REFERENCES game(appid) NOT NULL,
    id_genero INT REFERENCES generos(id) NOT NULL
);

CREATE TABLE languages (
    id BIGSERIAL PRIMARY KEY,
    language_name VARCHAR(255) NOT NULL
);

CREATE TABLE game_languages (
    id BIGSERIAL PRIMARY KEY,
    appid INT REFERENCES game(appid) NOT NULL,
    id_language BIGINT REFERENCES languages(id) NOT NULL,
    support_type TEXT NOT NULL CHECK (support_type IN ('supported', 'audio'))
);

CREATE TABLE operating_system (
    id BIGSERIAL PRIMARY KEY,
    name varchar(255) NOT NULL
);


CREATE TABLE game_operating_system (
    id BIGSERIAL PRIMARY KEY,
    appid INT REFERENCES game(appid) NOT NULL,
    id_operating_system BIGINT REFERENCES operating_system(id) NOT NULL
)

CREATE TABLE screenshots (
    id SERIAL PRIMARY KEY,
    screenshot_url TEXT NOT NULL,
    appid INT REFERENCES game(appid) NOT NULL
);