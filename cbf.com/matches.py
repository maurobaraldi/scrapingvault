from json import dumps
from time import sleep
from utils import fetch_json, timer

base_url = "https://inside.fifa.com/"
first_round = 1
last_round = 38
tournaments = [
    {"id": 12414, "year": 2018, "serie": "A"}, 
    {"id": 12430, "year": 2019, "serie": "A"}, 
    {"id": 12464, "year": 2020, "serie": "A"}, 
    {"id": 12487, "year": 2021, "serie": "A"}, 
    {"id": 12518, "year": 2022, "serie": "A"}, 
    {"id": 12555, "year": 2023, "serie": "A"}, 
    {"id": 12584, "year": 2024, "serie": "A"}, 
    {"id": 12606, "year": 2025, "serie": "A"}, 
    {"id": 1260611, "year": 2026, "serie": "A"}
]


if __name__ == "__main__":
    rows = []
    for tournament in tournaments:
        for round in range(first_round, last_round + 1):
            with timer(f"Processing tournament Campeonato Brasileiro - Serie {tournament.get('serie')} round {round} of {tournament.get('year')}"):
                sleep(0.5)
                matches = fetch_json(
                        f"https://www.cbf.com.br/api/cbf/jogos/campeonato/{tournament.get('id')}/rodada/{round}/fase",
                        verify_ssl=False
                    )
                #import pdb; pdb.set_trace()
                rows += matches["jogos"][0]["jogo"]
        with open("campeonato_brasileiro_serie_a.json", "w", encoding="utf-8") as f:
            f.write(dumps(rows, ensure_ascii=False, indent=2))
        sleep(2)
