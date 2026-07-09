from time import sleep
from database import Database as DB
from utils import fetch_json, timer, clean_data
from zeroevents import unvailable_ids

base_url = "https://inside.fifa.com/"

headers = {
    "Referer": f"{base_url}/data-centre/matches",
    "Origin": base_url,
}


def normalize_event(match_id, event):
    return {
        "match_id": match_id,
        "id": event.get("id"),
        "type": event.get("type"),
        "description": event.get("description"),
        "match_period": event.get("matchPeriod"),
        "match_minute": event.get("matchMinute"),
        "team_id": event.get("teamId"),
        "opponent_team_id": event.get("opponentTeamId"),
        "player_id": event.get("playerId"),
        "sub_player_id": event.get("subPlayerId"),
    }


if __name__ == "__main__":
    with DB("fifa.sqlite") as db:
        match_events_str_sql = """
        CREATE TABLE IF NOT EXISTS match_events (
            match_id TEXT NOT NULL,
            id TEXT NOT NULL,

            type TEXT NOT NULL,
            description TEXT,

            match_period TEXT,
            match_minute TEXT,

            team_id INTEGER,
            opponent_team_id INTEGER,

            player_id INTEGER,
            sub_player_id INTEGER,

            PRIMARY KEY (match_id, id)
        );
        """
        rows = []

        db.execute(match_events_str_sql)

        strSQL = """
        SELECT id_match
        FROM matches AS m
        WHERE id_match IS NOT NULL
        AND TRIM(id_match) <> ''
        AND NOT EXISTS (
            SELECT 1
            FROM match_events AS e
            WHERE e.match_id = m.id_match
        );
        """

        matches = [dict(row) for row in db.execute(strSQL).fetchall()]

    for match in matches:
        match_id = match["id_match"]
        if not match_id:
            continue
        
        if match_id in unvailable_ids:
            continue

        with timer(f" Processing match {match_id}"):
            with DB("fifa.sqlite") as db:

                events = fetch_json(
                    f"https://inside.fifa.com/api/data-centre/matches/live-events?matchId={match_id}",
                    verify_ssl=False,
                    ignore_status_codes={404}
                )

                if not events:
                    continue
                rows = [
                    normalize_event(match_id, event)
                    for event in events.get("events", [])
                ]

                inserted = db.insert_or_ignore("match_events", rows)
                print(f"{match_id}: inserted {inserted}/{len(rows)} events")
