from time import sleep
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
        CREATE TABLE IF NOT EXISTS match_events (
            id TEXT PRIMARY KEY,
            match_id TEXT NOT NULL,

            type TEXT NOT NULL,
            description TEXT,

            match_period TEXT,
            match_minute TEXT,

            team_id INTEGER,
            opponent_team_id INTEGER,

            player_id INTEGER,
            sub_player_id INTEGER
        );
        """
        rows = []

        db.execute(matches_str_sql)

        matches = [dict(row) for row in db.execute("SELECT id_match FROM matches;").fetchall()]

        # for match in matches:
        #     if match.get('id_match'):
        #         events = fetch_json(
        #                 f"https://inside.fifa.com/api/data-centre/matches/live-events?matchId={match.get('id_match')}",
        #                 verify_ssl=False
        #             )
        #         if events:
        #             _events = []
        #             for event in events.get("events"):
        #                 print(events)
        #                 _events.append(event | {"match_id": match["id_match"] })
        #             db.insert_or_ignore("matches_events", _events)

    for match in matches:
        #sleep(1)
        match_id = match["id_match"]
        print(match_id)
        if not match_id:
            continue

        with timer(f"Processing match {match_id}"):
            with DB("fifa.sqlite") as db:

                events = fetch_json(
                    f"https://inside.fifa.com/api/data-centre/matches/live-events?matchId={match_id}",
                    verify_ssl=False,
                )

                if not events:
                    continue

                rows = [
                    event | {"match_id": match_id}
                    for event in events.get("events", [])
                ]

                db.insert_or_ignore("match_events", rows)
                sleep(1)

