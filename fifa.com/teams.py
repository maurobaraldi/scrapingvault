from utils import fetch_json

teams = {
    "men": 1,
    "women": 2
}
headers = {
    "Referer": "https://inside.fifa.com/data-centre/teams",
    "Origin": "https://inside.fifa.com",
}

if __name__ == "__main__":
    for team, id in teams.items():
        fetch_json(
            f"https://inside.fifa.com/api/data-centre/matches/teams?gender={id}&language=en",
            f"./{team}.json",
        )
