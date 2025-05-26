CREATE TABLE players (
    player_id    SERIAL PRIMARY KEY,
    first_name   VARCHAR(50) NOT NULL,
    last_name    VARCHAR(50) NOT NULL,
    shirt_number SMALLINT    NOT NULL UNIQUE,     -- номер футболки
    position     VARCHAR(20) NOT NULL,            -- амплуа (Goalkeeper, Defender, Midfielder, Forward)
    dob          DATE         NOT NULL,           -- дата рождения
    nationality  VARCHAR(30)                          -- гражданство
);

-- 2. Схема: Матчи команды
CREATE TABLE matches (
    match_id        SERIAL PRIMARY KEY,
    match_date      DATE         NOT NULL,
    opponent        VARCHAR(50)  NOT NULL,         -- соперник
    venue           VARCHAR(10)  NOT NULL CHECK (venue IN ('Home','Away')),
    team_goals      SMALLINT     NOT NULL DEFAULT 0,
    opponent_goals  SMALLINT     NOT NULL DEFAULT 0
);

-- 3. Схема: Участие игрока в матче
CREATE TABLE appearances (
    match_id      INTEGER NOT NULL REFERENCES matches(match_id) ON DELETE CASCADE,
    player_id     INTEGER NOT NULL REFERENCES players(player_id) ON DELETE CASCADE,
    minutes_played SMALLINT    CHECK (minutes_played BETWEEN 0 AND 120),
    goals_scored   SMALLINT    DEFAULT 0,
    assists        SMALLINT    DEFAULT 0,
    cards          VARCHAR(3)  CHECK (cards IN ('Y','Y2','R','YR')) DEFAULT NULL,
    PRIMARY KEY(match_id, player_id)
);

-- 4. Схема: Тренерский штаб (опционально)
CREATE TABLE staff (
    staff_id    SERIAL PRIMARY KEY,
    first_name  VARCHAR(50) NOT NULL,
    last_name   VARCHAR(50) NOT NULL,
    role        VARCHAR(30) NOT NULL,               -- роль (Head Coach, Assistant, etc.)
    dob         DATE         NULL
);
-- Игроки
INSERT INTO players (first_name, last_name, shirt_number, position, dob, nationality) VALUES
('Alisson',  'Becker',   1,  'Goalkeeper', '1992-10-02', 'Brazil'),
('Trent',    'Alexander-Arnold', 66, 'Defender', '1998-10-07', 'England'),
('Mohamed',  'Salah',     11, 'Forward', '1992-06-15', 'Egypt'),
('Jordan',   'Henderson', 14, 'Midfielder', '1990-06-17', 'England'),
('Virgil',   'Van Dijk',   4, 'Defender', '1991-07-08', 'Netherlands');

-- Матчи
INSERT INTO matches (match_date, opponent, venue, team_goals, opponent_goals) VALUES
('2025-08-15', 'Everton', 'Home', 3, 1),
('2025-08-22', 'Chelsea', 'Away', 2, 2),
('2025-08-29', 'Arsenal', 'Home', 1, 0);

-- Участия в матчах
INSERT INTO appearances (match_id, player_id, minutes_played, goals_scored, assists, cards) VALUES
(1, 1, 90, 0, 0, NULL),
(1, 2, 90, 0, 2, NULL),
(1, 3, 80, 2, 0, 'Y'),
(1, 4, 85, 0, 0, NULL),
(2, 1, 90, 0, 0, NULL),
(2, 3, 90, 1, 1, NULL),
(2, 5, 90, 0, 0, 'Y2'),
(3, 1, 90, 0, 0, NULL),
(3, 4, 90, 0, 0, NULL),
(3, 2, 90, 0, 1, NULL);

-- Штат команды
INSERT INTO staff (first_name, last_name, role, dob) VALUES
('Jurgen', 'Klopp',    'Head Coach', '1967-06-16'),
('Pep',    'Lijnders', 'Assistant',  '1983-06-22');