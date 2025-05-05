-- jamdate.sql for Jam-Date Application

-- 1) Users table
CREATE TABLE users (
    id            SERIAL PRIMARY KEY,
    username      VARCHAR(80)  UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    name          VARCHAR(120) NOT NULL,
    email         VARCHAR(120) UNIQUE NOT NULL,
    photo         VARCHAR(200),
    date_joined   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

-- 2) Profiles table
CREATE TABLE profiles (
    id                 SERIAL PRIMARY KEY,
    user_id            INTEGER     NOT NULL
                             REFERENCES users(id) ON DELETE CASCADE,
    description        VARCHAR(500) NOT NULL,
    parish             VARCHAR(100) NOT NULL,
    biography          VARCHAR(1000),
    sex                VARCHAR(10),
    race               VARCHAR(50),
    birth_year         INTEGER,
    height             REAL,
    fav_cuisine        VARCHAR(100),
    fav_colour         VARCHAR(50),
    fav_school_subject VARCHAR(100),
    political          BOOLEAN     DEFAULT FALSE,
    religious          BOOLEAN     DEFAULT FALSE,
    family_oriented    BOOLEAN     DEFAULT FALSE,
    photo_filename     VARCHAR(200)
);

-- 3) Favourites table
CREATE TABLE favourites (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL
                          REFERENCES users(id)    ON DELETE CASCADE,
    profile_id  INTEGER NOT NULL
                          REFERENCES profiles(id) ON DELETE CASCADE,
    timestamp   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, profile_id)
);

-- 4) Messages table (optional)
CREATE TABLE messages (
    id           SERIAL PRIMARY KEY,
    sender_id    INTEGER NOT NULL
                           REFERENCES users(id) ON DELETE CASCADE,
    recipient_id INTEGER NOT NULL
                           REFERENCES users(id) ON DELETE CASCADE,
    content      TEXT    NOT NULL,
    timestamp    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_profiles_user     ON profiles(user_id);
CREATE INDEX idx_fav_by_user       ON favourites(user_id);
CREATE INDEX idx_fav_by_profile    ON favourites(profile_id);
CREATE INDEX idx_messages_conv     ON messages(sender_id, recipient_id);
