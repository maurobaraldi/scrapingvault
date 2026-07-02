from time import sleep
from utils import fetch_json_to_file

start, end = 2000, 2026
men, women = 1, 2

headers = {
    "Referer": "https://inside.fifa.com/data-centre/matches",
    "Origin": "https://inside.fifa.com",
}

if __name__ == "__main__":
    for year in range(start, end + 1):
        sleep(1)
        fetch_json_to_file(
            f"https://inside.fifa.com/api/data-centre/matches/competitions?gender={men}&year={year}&language=en&count=1000",
            f"./data/competitions-by-year/fifa-men-competitions-{year}.json",
            verify_ssl=False
        )
        fetch_json_to_file(
            f"https://inside.fifa.com/api/data-centre/matches/competitions?gender={women}&year={year}&language=en&count=1000",
            f"./data/competitions-by-year/fifa-women-competitions-{year}.json",
            verify_ssl=False
        )
