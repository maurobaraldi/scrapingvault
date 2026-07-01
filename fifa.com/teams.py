from utils import fetch_json_to_file

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
        fetch_json_to_file(
            f"https://inside.fifa.com/api/data-centre/matches/teams?gender={id}&language=en",
            f"./data/fifa-{team}.json",
            verify_ssl=False
        )
