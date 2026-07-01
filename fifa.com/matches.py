from json import loads
from time import sleep
from utils import fetch_json

start, end = 2000, 2026
men, women = 1, 2

headers = {
    "Referer": "https://inside.fifa.com/data-centre/matches",
    "Origin": "https://inside.fifa.com",
}

if __name__ == "__main__":
    for year in range(start, end + 1):
        with open(f"./data/men-competitions-{year}.json") as c:
            competitions = loads(c.read())
        
        for competition in competitions:
            matches = 
            cursor = 25
            competition_code = competition.get("competitionClassificationCode")
            name = competition.get("name")

            while cursor <= competition.get("matchesCount"):
                fetch_json(
                    f"https://inside.fifa.com/api/data-centre/matches?gender=1&competitionClassificationCode={competition_code}&year={year}&language=en&count={cursor}",
                    f"./men-{name}-{year}.json",
        )


            
        sleep(1)
        fetch_json(
            f"https://inside.fifa.com/api/data-centre/matches/competitions?gender={men}&year={year}&language=en",
            f"./men-competitions-{year}.json",
        )
        fetch_json(
            f"https://inside.fifa.com/api/data-centre/matches/competitions?gender={women}&year={year}&language=en",
            f"./women-competitions-{year}.json",
        )
