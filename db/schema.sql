DROP TABLE IF EXISTS random_events;

DROP TABLE IF EXISTS month_history;

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
    random_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL UNIQUE,
        description TEXT NOT NULL, 
        modifier_pct INTEGER NOT NULL,
        specific_genre TEXT DEFAULT NULL,
        FOREIGN KEY (specific_genre) REFERENCES genres (name)
    );

INSERT INTO
    random_events (title, description, modifier_pct, specific_genre)
VALUES  
    (
        'Sci-Fi Reshoot Bottleneck', 
        'Heavy VFX rendering errors force extensive reshoots. Active Sci-Fi subscriber yields drop to 25% this month.', 
        25, 'Sci-Fi'
    ),
    (
        'True Crime Backlash', 
        'An ethical controversy surrounding your latest true crime series sparks online debates. True Crime growth drops to 40%.', 
        40, 'True Crime'
    ),
    (
        'Anime Licensing Lock', 
        'International streaming rights disputes temporarily freeze regional expansion. Anime subscriber yields cut to 50%.', 
        50, 'Anime'
    ),
    (
        'Sitcom Writer Strike', 
        'Creative contract disputes halt production rooms, stalling episodic momentum. Sitcom growth drops to 30%.', 
        30, 'Sitcom'
    ),
    (
        'Reality TV Over-Saturation', 
        'Audiences grow tired of repetitive reality formats this month. Viewership acquisition drops to 50%.', 
        50, 'Reality TV'
    ),
    (
        'Core Server Blackout', 
        'Platform outages during a holiday weekend freeze new sign-ups. Monthly subscriber growth drops to 60% globally.', 
        60, NULL
    ),
    (
        'App Store Policy Dispute', 
        'A high-profile feud with mobile storefronts temporarily hides your app from charts. Global growth drops to 75%.', 
        75, NULL
    ),
    (
        'Viral TikTok Audio Trend', 
        'A trending soundbite from one of your anime productions goes viral globally, boosting Anime subscriber returns to 160%!', 
        160, 'Anime'
    ),
    (
        'Retro Sitcom Renaissance', 
        'A beloved classic sitcom gets highly publicized on social media, spiking comfort-watch signups to 140%.', 
        140, 'Sitcom'
    );

CREATE TABLE
    users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        hash TEXT NOT NULL,
        last_game INTEGER
    );

CREATE TABLE
    games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        cash INTEGER DEFAULT 5000000000,
        subscribers INTEGER DEFAULT 1000000,
        current_month INTEGER DEFAULT 1,
        status TEXT DEFAULT ('ACTIVE') CHECK (status IN ('ACTIVE', 'WON', 'LOST')),
        base_cash_per_subscriber INTEGER DEFAULT 15,
        base_cancel_penalty INTEGER DEFAULT 50,
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

CREATE TABLE
    month_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_id INTEGER NOT NULL,
        month INTEGER NOT NULL,
        cash INTEGER NOT NULL,
        subscribers INTEGER NOT NULL,
        event TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (game_id) REFERENCES games (id) ON DELETE CASCADE,
        FOREIGN KEY (event) REFERENCES random_events (title)
    );