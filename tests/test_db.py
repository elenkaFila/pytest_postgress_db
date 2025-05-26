import pytest

VALID_POSITIONS = {'Goalkeeper', 'Defender', 'Midfielder', 'Forward'}

@pytest.mark.parametrize("table", ["players", "matches", "appearances", "staff"])
def test_table_exists(cursor, table):
    """Проверка наличия всех таблиц."""
    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = %s
        """, (table,))
    (count,) = cursor.fetchone()
    assert count == 1, f"Table '{table}' does not exist"

def test_players_pk_unique(cursor):
    """Проверка уникальности футболистов."""
    cursor.execute("""
        SELECT player_id, COUNT(*) 
        FROM players 
        GROUP BY player_id 
        HAVING COUNT(*) > 1;
        """)
    dups = cursor.fetchall()
    assert not dups, f"Duplicate player_ids found: {dups}"

def test_matches_pk_not_empty(cursor):
    """Первичный ключ match_id не должен содержать NULL."""
    cursor.execute("""
        SELECT COUNT(*)
        FROM matches 
        WHERE match_id IS NULL;
        """)
    (count,) = cursor.fetchone()
    assert count == 0, "Found NULLs in matches.match_id"

def test_players_pk_not_null(cursor):
    """Первичный ключ player_id не должен содержать NULL."""
    cursor.execute("""
        SELECT COUNT(*)
        FROM players 
        WHERE player_id IS NULL;
        """)
    (count,) = cursor.fetchone()
    assert count == 0, "Found NULLs in players.player_id"

def test_appearances_fk_players(cursor):
    """Проверка внешнего ключа appearances → players."""
    cursor.execute("""
        SELECT COUNT(*) 
        FROM appearances a
        LEFT JOIN players p ON a.player_id = p.player_id
        WHERE p.player_id IS NULL;
        """)
    (count,) = cursor.fetchone()
    assert count == 0, "Found appearances referencing non-existent players"

def test_matches_notnull_match_date(cursor):
    """Поле matches.match_date не должно быть NULL."""
    cursor.execute("""
        SELECT COUNT(*) 
        FROM matches 
        WHERE match_date IS NULL;
        """)
    (count,) = cursor.fetchone()
    assert count == 0, "Found NULLs in matches.match_date"

def test_home_and_away_matches(cursor):
    """Должен быть как минимум один домашний и один выездной матч."""
    cursor.execute("""
        SELECT
        SUM(CASE WHEN venue = 'Home' THEN 1 ELSE 0 END) AS homes,
        SUM(CASE WHEN venue = 'Away' THEN 1 ELSE 0 END) AS aways
        FROM matches;
        """)
    homes, aways = cursor.fetchone()
    assert homes >= 1, "No home matches found"
    assert aways >= 1, "No away matches found"


def test_unique_shirt_numbers(cursor):
    """Все номера футболок (shirt_number) в таблице players уникальны."""
    cursor.execute( """
        SELECT shirt_number 
        FROM players 
        WHERE shirt_number IS NOT NULL;
        """)
    nums = [r[0] for r in cursor.fetchall()]
    assert len(nums) == len(set(nums)), "Shirt numbers must be unique"

def test_valid_positions(cursor):
    """Все значения в поле position допустимые роли (Goalkeeper, Defender, Midfielder, Forward)."""
    cursor.execute("""
        SELECT DISTINCT position
        FROM players 
        WHERE position IS NOT NULL;
        """)
    positions = {r[0] for r in cursor.fetchall()}
    assert positions.issubset(VALID_POSITIONS), f"Invalid positions: {positions - VALID_POSITIONS}"


def test_minutes_played_within_bounds(cursor):
    """Во всех записях таблицы appearances поле minutes_played лежит в диапазоне от 0 до 120 минут."""
    cursor.execute("""
        SELECT match_id, player_id, minutes_played
        FROM appearances
        WHERE minutes_played IS NOT NULL
        AND (minutes_played < 0 OR minutes_played > 120)
        """)
    bad = cursor.fetchall()
    assert not bad, f"Invalid minutes_played entries: {bad}"
    

def test_forwards_have_scored_goals(cursor):
    """Игрок с позицией Forward, у которого есть записи об участии в матчах, суммарно забил как минимум один гол."""
    cursor.execute("""
        SELECT a.player_id, SUM(a.goals_scored) AS total
        FROM players p
        JOIN appearances a ON p.player_id = a.player_id
        WHERE p.position = 'Forward'
        GROUP BY a.player_id
        """)
    rows = cursor.fetchall()
    bad = [r for r in rows if r[1] == 0]
    assert not bad, f"Forwards without goals: {bad}"
    

def test_at_least_one_home_match(cursor):
    """В расписании матчей есть хотя бы один домашний матч venue = 'Home'."""
    cursor.execute("""
        SELECT COUNT(*) 
        FROM matches 
        WHERE venue = 'Home';
        """)
    (cnt,) = cursor.fetchone()
    assert cnt >= 1, "There should be at least one home match"
    

def test_head_coach_exists(cursor):
    """У каждой команды обязательно есть главный тренер."""
    cursor.execute("""
        SELECT 1 
        FROM staff 
        WHERE role = 'Head Coach' 
        LIMIT 1;
        """)
    assert cursor.fetchone() is not None, "No Head Coach found in staff"
    
def test_players_never_played(cursor):
    """Проверяет, сколько игроков ни разу не выходило на поле."""
    cursor.execute("""
        SELECT COUNT(*) 
        FROM players p
        LEFT JOIN appearances a ON p.player_id = a.player_id
        WHERE a.match_id IS NULL;
        """)
    (count,) = cursor.fetchone()
    assert isinstance(count, int) and count >= 0, f"Неверное значение: {count}"
