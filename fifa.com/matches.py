from database import Database as DB
from utils import fetch_json, timer, clean_data

base_url = "https://inside.fifa.com/"

headers = {
    "Referer": f"{base_url}/data-centre/matches",
    "Origin": base_url,
}


if __name__ == "__main__":
    with DB("fifa.sqlite") as db:
        matches_str_sql = """
        CREATE TABLE IF NOT EXISTS matches (
            id_match TEXT,
            id_match_ifes INTEGER,
            id_competition INTEGER,
            id_season INTEGER,
            id_stage TEXT,

            competition_name TEXT,
            season_name TEXT,
            stage_name TEXT,
            match_date DATE,

            team_A_id INTEGER,
            team_B_id INTEGER,
            team_A_name TEXT,
            team_B_name TEXT,

            team_A_country_code TEXT,
            team_B_country_code TEXT,

            team_A_score INTEGER,
            team_B_score INTEGER,
            team_A_penalty_score INTEGER,
            team_B_penalty_score INTEGER,

            result_type INTEGER,
            winner INTEGER,
            has_penalties BOOLEAN,

            PRIMARY KEY (id_match_ifes)
        );
        """
        db.execute(matches_str_sql)

        tournaments = [dict(row) for row in db.execute("SELECT * FROM tournaments;").fetchall()]

        for tournament in tournaments:
            with timer(f"Processing tournament {tournament.get('name')} of {tournament.get('year')}"):
                matches = fetch_json(
                    f"https://inside.fifa.com/api/data-centre/matches?gender={tournament.get('gender')}&competitionClassificationCode={tournament.get('competitionClassificationCode')}&year={tournament.get('year')}&language=en&count=500",
                    verify_ssl=False
                )
                if matches:
                    _matches = []
                    for match in matches:
                        _matches.append(clean_data(match))
                    db.insert_or_ignore("matches", _matches)
