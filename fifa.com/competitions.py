from database import Database as DB
from utils import fetch_json, timer


start, end = 2002, 2026
men, women = 1, 2
base_url = "https://inside.fifa.com/"


if __name__ == "__main__":
    with DB("fifa.sqlite") as db:
        tournaments_str_sql = """
        CREATE TABLE IF NOT EXISTS tournaments (
        gender INTEGER NOT NULL,
        year INTEGER NOT NULL,
        competitionClassificationCode TEXT NOT NULL,
        name TEXT NOT NULL,
        matchesCount INTEGER NOT NULL,
        PRIMARY KEY (year, competitionClassificationCode)
        );
        """

        db.execute(tournaments_str_sql)

        for year in range(start, end + 1):
            rows = []
            with timer(f"Processing tournament of year: {year}"):
                data_set = fetch_json(
                    f"{base_url}/api/data-centre/matches/competitions?gender={men}&year={year}&language=en&count=1000",
                    verify_ssl=False
                )

                for row in data_set:
                    rows.append(row | {"year": year, "gender": men})

                data_set = fetch_json(
                    f"{base_url}/api/data-centre/matches/competitions?gender={women}&year={year}&language=en&count=1000",
                    verify_ssl=False
                )

                for row in data_set:
                    rows.append(row | {"year": year, "gender": women})
                
                db.insert_or_ignore("tournaments", rows)

