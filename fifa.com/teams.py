from database import Database as DB
from utils import fetch_json


start, end = 2002, 2026
men, women = 1, 2
base_url = "https://inside.fifa.com/"


if __name__ == "__main__":
    with DB("fifa.sqlite") as db:
        tournaments_str_sql = """
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER NOT NULL,
            gender INTEGER NOT NULL,
            associationId INTEGER NOT NULL,
            name TEXT NOT NULL,
            slug TEXT NOT NULL,
            status TEXT NOT NULL,
        PRIMARY KEY (id, gender, name)
        );
        """

        db.execute(tournaments_str_sql)

        for gender in (women, men):
            teams = fetch_json(
                    f"{base_url}/api/data-centre/matches/teams?gender={gender}&language=en",
                    verify_ssl=False
                )
            rows = []
            for team in teams:
                team.pop("confederation")
                team.pop("flagUrl")
                rows.append(team)
            db.insert_or_ignore("teams", rows)