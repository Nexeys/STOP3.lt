DROP TABLE IF EXISTS month_history;
DROP TABLE IF EXISTS history;
DROP TABLE IF EXISTS portfolios;
DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS random_events;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS users;

-- ==========================================
-- GENRES CONFIGURATION (BALANCED YIELDS)
-- ==========================================
CREATE TABLE genres (
    name TEXT PRIMARY KEY,
    base_cost INTEGER NOT NULL,
    base_subscriber_yield INTEGER NOT NULL
);

INSERT INTO genres (name, base_cost, base_subscriber_yield)
VALUES
    ('Sci-Fi', 1400000000, 180000),       
    ('True Crime', 750000000, 90000),   
    ('Anime', 450000000, 55000),         
    ('Sitcom', 250000000, 35000),        
    ('Reality TV', 100000000, 15000);     

CREATE TABLE random_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL, 
    modifier_pct INTEGER NOT NULL,
    specific_genre TEXT DEFAULT NULL,
    FOREIGN KEY (specific_genre) REFERENCES genres (name)
);

INSERT INTO random_events (title, description, modifier_pct, specific_genre)
VALUES  
    -- --- ORIGINAL BALANCED EVENTS ---
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
    ),

    -- --- NEW HIGH-VOLATILITY & EXPANSION EVENTS ---
    (
        'Cannes Sci-Fi Masterpiece',
        'Your flagship Sci-Fi show receives a 10-minute standing ovation at a prestigious festival. Sci-Fi yields explode to 180%!',
        180, 'Sci-Fi'
    ),
    (
        'Cold Case Solved',
        'A breakthrough in a real-world case heavily featured in your production drives massive curiosity traffic. True Crime spikes to 175%.',
        175, 'True Crime'
    ),
    (
        'Trashy Reality Super-Fan',
        'An A-list pop star tweets a meme praising your trashiest reality drama, causing a massive wave of casual sign-ups. Reality TV spikes to 200%!',
        200, 'Reality TV'
    ),
    (
        'The Great Meme format',
        'A single reaction face from your main sitcom becomes the definitive internet format of the month. Sitcom yields surge to 150%.',
        150, 'Sitcom'
    ),
    (
        'Competitor Platform Fails',
        'A rival network suffers a disastrous application update, driving disgruntled cord-cutters straight to you. Global gains rise to 130%.',
        130, NULL
    ),
    (
        'Holiday Smart-TV Bundling',
        'Your platform comes pre-installed on all top-selling smart TVs during a major holiday rush. Global conversions jump to 125%.',
        125, NULL
    ),
    (
        'Celebrity Defamation Lawsuit',
        'An individual featured in a documentary files a massive injunction, freezing all active marketing assets. True Crime hits a floor of 20%.',
        20, 'True Crime'
    ),
    (
        'Beloved Showrunner Fired',
        'PR fallout after a high-profile firing causes angry core fans to cancel accounts or boycott features. Global acquisition drops to 70%.',
        70, NULL
    ),
    (
        'AI Translation Breakthrough',
        'Instant, flawless auto-dubbing opens up massive immediate markets in Asia and Latin America. Anime yields skyrocket to 190%.',
        190, 'Anime'
    ),
    (
        'Syndication Bidding War',
        'Cable networks desperately try to license old episodes, giving your catalog massive free prestige and attention. Sitcom yields rise to 135%.',
        135, 'Sitcom'
    ),
    (
        'Unscripted Cast Walkout',
        'The eccentric cast of your top unscripted show refuses to film without massive raises, killing seasonal momentum. Reality TV drops to 10%.',
        10, 'Reality TV'
    ),
    (
        'Sub-Orbital Marketing Stunt',
        'A wild promotional stunt involving an actual weather satellite goes wrong, resulting in terrible tech press. Sci-Fi yields drop to 50%.',
        50, 'Sci-Fi'
    ),
    (
        'Cyberpunk Hype Train',
        'A major sci-fi video game release sparks a massive global craving for neon futuristic aesthetics. Sci-Fi yields increase to 145%.',
        145, 'Sci-Fi'
    ),
    (
        'Internet Service Provider Throttle',
        'A major telecom company begins throttling high-bandwidth video streams during peak hours, causing subscriber friction. Global growth sinks to 80%.',
        80, NULL
    ),
    (
        'Database Inflation Bug',
        'A backend bug duplicates thousands of accounts, forcing a highly publicized manual rollback that slows down sign-up verification. Global metrics stall at 65%.',
        65, NULL
    ),
    (
        'Late-Night Show Spotlight',
        'A popular late-night host does a whole comedy segment parodying your newest anime series, driving mainstream awareness. Anime yields bump to 130%.',
        130, 'Anime'
    );

-- ==========================================
-- ACTIVE SYSTEM PROFILES
-- ==========================================
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    last_game INTEGER
);

CREATE TABLE games (
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

CREATE TABLE portfolios (
    game_id INTEGER NOT NULL,
    genre TEXT NOT NULL,
    episodes_produced INTEGER DEFAULT 0,
    PRIMARY KEY (game_id, genre),
    FOREIGN KEY (game_id) REFERENCES games (id) ON DELETE CASCADE,
    FOREIGN KEY (genre) REFERENCES genres (name)
);

-- ==========================================
-- HISTORICAL RUN LOGS
-- ==========================================
CREATE TABLE history (
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

CREATE TABLE month_history (
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