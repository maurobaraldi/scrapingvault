from glob import glob
from json import loads
from database import Database as DB


def bulk_ingest_competitions_by_year(path: str):
    """
    Ingest competitions names and count in database.
    """

    competition_classifications_str_sql = """
    CREATE TABLE IF NOT EXISTS competition_classifications (
    year INTEGER NOT NULL,
    competitionClassificationCode TEXT NOT NULL,
    name TEXT NOT NULL,
    matchesCount INTEGER NOT NULL,
    PRIMARY KEY (year, competitionClassificationCode)
    );
    """

    files = glob("./data/competitions-by-year/*[0-9][0-9][0-9][0-9].json")
        
    with DB("fifa.sqlite") as db:
        db.execute(competition_classifications_str_sql)

        for file in files:
            print(f"Working in file: {file}")
            year = int(file.rsplit("-")[-1].replace(".json", ""))
            with open(file) as _:
                data_set = loads(_.read())
                rows = []
                for row in data_set:
                    rows.append(row | {"year": year})

                db.insert_or_ignore("competition_classifications", rows)


def bulk_ingest_matches(path: str):
    """
    Ingest competitions names and count in database.
    """

    competition_classifications_str_sql = """
    CREATE TABLE IF NOT EXISTS matches (
        id_match TEXT,
        id_match_ifes INTEGER PRIMARY KEY,
        id_competition TEXT,
        id_season TEXT,
        id_stage TEXT,

        competition_name TEXT NOT NULL,
        season_name TEXT,

        match_date TEXT NOT NULL, -- ISO-8601 (YYYY-MM-DD)

        team_A_id INTEGER NOT NULL,
        team_B_id INTEGER NOT NULL,

        team_A_name TEXT NOT NULL,
        team_B_name TEXT NOT NULL,

        team_A_country_code TEXT NOT NULL,
        team_B_country_code TEXT NOT NULL,

        team_A_score INTEGER NOT NULL,
        team_B_score INTEGER NOT NULL,

        team_A_penalty_score INTEGER NOT NULL DEFAULT 0,
        team_B_penalty_score INTEGER NOT NULL DEFAULT 0,

        result_type INTEGER NOT NULL,
        winner INTEGER,

        has_penalties BOOLEAN NOT NULL
    );
    """

    files = glob("./data/*[0-9][0-9][0-9][0-9].csv")
        
    with DB("fifa.sqlite") as db:
        db.execute(competition_classifications_str_sql)

        for file in files:
            print(f"Working in file: {file}")
            year = int(file.rsplit("-")[-1].replace(".json", ""))
            with open(file) as _:
                data_set = loads(_.read())
                rows = []
                for row in data_set:
                    rows.append(row | {"year": year})

                db.insert_or_ignore("competition_classifications", rows)
