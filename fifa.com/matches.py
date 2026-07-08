from json import dumps, loads
from time import sleep
from utils import fetch_json, save_json, clean_data, save_dicts_to_csv

start, end = 2022, 2026
men, women = 1, 2

headers = {
    "Referer": "https://inside.fifa.com/data-centre/matches",
    "Origin": "https://inside.fifa.com",
}

if __name__ == "__main__":
    for year in range(start, end + 1):
        print(f"Working on year {year}")
        for gender in (men, women):
            'men' if gender == 1 else 'women'
            _gender = 'men' if gender == 1 else 'women'
            with open(f"./data/competitions-by-year/fifa-{_gender}-competitions-{year}.json") as c:
                competitions = loads(c.read())
            
            for competition in competitions:
                competition_code = competition.get("competitionClassificationCode")
                name = competition.get("name").replace(" ", "-").replace("™", "").lower()
                print(f" Working on competition {name} - {_gender}")
                matches = fetch_json(
                    f"https://inside.fifa.com/api/data-centre/matches?gender={gender}&competitionClassificationCode={competition_code}&year={year}&language=en&count=100",
                    verify_ssl=False
                )
                if matches:
                    _matches = []
                    for match in matches:
                        _matches.append(clean_data(match))
                    save_dicts_to_csv(_matches, f"./data/fifa-{_gender}-{name}-{year}.csv")
