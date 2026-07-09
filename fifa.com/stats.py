from database import Database as DB
from utils import fetch_json

# There is no statistics for other tournament than World Cup and no older than 2022
# id_competitions = [17, 103, 521] # World Cup men and women, women qualifiers
# id_seasons = [255711, 285023, 286462] # FIFA Men World Cup Qatar 2022, FIFA Men World Cup 2026, FIFA Women’s World Cup Australia & New Zealand 2023, FIFA WWC 2023 Prel. Comp. Play-off tournament

base_url = "https://inside.fifa.com/"

headers = {
    "Referer": f"{base_url}/data-centre/matches",
    "Origin": base_url,
}

if __name__ == "__main__":
    with DB("fifa.sqlite") as db:
        stats_str_sql = """
        CREATE TABLE IF NOT EXISTS fifa_team_statistics (
            id INTEGER PRIMARY KEY,

            -- Reference to your matches table
            match_id INTEGER NOT NULL,

            -- FIFA team id (e.g. 1882882, 1883725)
            team_id INTEGER NOT NULL,

            -- Statistic name
            statistic_name VARCHAR(100) NOT NULL,

            -- Statistic value
            statistic_value NUMERIC(18,6),

            -- Boolean flag from the API
            is_available BOOLEAN NOT NULL DEFAULT TRUE,

            -- Prevent duplicate statistics for a team in a match
            CONSTRAINT uq_fifa_team_stat
                UNIQUE (match_id, team_id, statistic_name)

            -- Optional FK
            -- ,CONSTRAINT fk_match
            --     FOREIGN KEY (match_id)
            --     REFERENCES matches(id)
        );

        CREATE INDEX IF NOT EXISTS idx_fifa_team_statistics_match
            ON fifa_team_statistics(match_id);

        CREATE INDEX IF NOT EXISTS idx_fifa_team_statistics_team
            ON fifa_team_statistics(team_id);

        CREATE INDEX IF NOT EXISTS idx_fifa_team_statistics_name
            ON fifa_team_statistics(statistic_name);

        CREATE TABLE IF NOT EXISTS fifa_match_statistics (
            match_id BIGINT NOT NULL,
            statistic_name VARCHAR(100) NOT NULL,
            statistic_value NUMERIC(18,6) NOT NULL,
            PRIMARY KEY (match_id, statistic_name)
        );
        """
        db.executescript(stats_str_sql)

        # Events with statistics
        matches_str_sql = """
        SELECT id_match_ifes
        FROM matches
        WHERE id_competition IN (17,103,521)
        AND id_season IN (255711,285023,286462);
        """
        matches = [dict(row) for row in db.execute(matches_str_sql).fetchall()]
    
        for match in matches:
            stats = fetch_json(
                f"https://fdh-api.fifa.com/v1/stats/match/{match.get('id_match_ifes')}/teams.json",
                verify_ssl=False,
                ignore_status_codes={404}
            )

            if not stats:
                continue

            team_ids = [k for k in stats if k != "-1"]

            if len(team_ids) != 2:
                print(f"Unexpected team count for match {match_id}")
                continue

            home_team_id, away_team_id = team_ids
            match_id = match["id_match_ifes"]

            rows = []

            for team_id in (home_team_id, away_team_id):
                for name, value, available in stats[team_id]:
                    rows.append((match_id, int(team_id), name, value, available))
            
            db.executemany("""
                INSERT OR REPLACE INTO fifa_team_statistics
                (match_id, team_id, statistic_name, statistic_value, is_available)
                VALUES (?, ?, ?, ?, ?)
            """, rows)

            if stats.get("-1"):
                continue
                try:
                    match_rows = [
                        (match_id, name, value)
                        for name, value, available in stats["-1"]
                    ]
                except:
                    import pdb; pdb.set_trace()

                db.executemany("""
                    INSERT OR REPLACE INTO fifa_match_statistics
                        (match_id, statistic_name, statistic_value)
                    VALUES (?, ?, ?)
                """, match_rows)
            else:
                print(f"Stats of match for match {match.get('id_match_ifes')} not fount")

            db.conn.commit()
