DROP TABLE IF EXISTS history;

DROP TABLE IF EXISTS portfolios;

DROP TABLE IF EXISTS games;

DROP TABLE IF EXISTS genres;

DROP TABLE IF EXISTS users;

CREATE TABLE
    genres (
        name TEXT PRIMARY KEY,
        base_cost INTEGER NOT NULL,
        base_subscriber_yield INTEGER NOT NULL
    );

INSERT INTO
    genres (name, base_cost, base_subscriber_yield)
VALUES
    ('Sci-Fi', 600000000, 150000),
    ('True Crime', 350000000, 65000),
    ('Anime', 250000000, 40000),
    ('Sitcom', 150000000, 20000),
    ('Reality TV', 50000000, 5000);

CREATE TABLE
    users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        hash TEXT NOT NULL
    );

CREATE TABLE
    games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        cash INTEGER DEFAULT 5000000000,
        subscribers INTEGER DEFAULT 1000000,
        current_month INTEGER DEFAULT 1,
        status TEXT DEFAULT ('ACTIVE') CHECK (status IN ('ACTIVE', 'WON', 'BANKRUPT', 'LOST')),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );

CREATE TABLE
    portfolios (
        game_id INTEGER NOT NULL,
        genre TEXT NOT NULL,
        episodes_produced INTEGER DEFAULT 0,
        PRIMARY KEY (game_id, genre),
        FOREIGN KEY (game_id) REFERENCES games (id) ON DELETE CASCADE,
        FOREIGN KEY (genre) REFERENCES genres (name)
    );

CREATE TABLE
    history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_id INTEGER NOT NULL,
        action TEXT NOT NULL CHECK (action IN ('PRODUCE', 'CANCEL')),
        genre TEXT NOT NULL,
        episodes INTEGER NOT NULL,
        cost INTEGER NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (game_id) REFERENCES games (id) ON DELETE CASCADE,
        FOREIGN KEY (genre) REFERENCES genres (name)
    );