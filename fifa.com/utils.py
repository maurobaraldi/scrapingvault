import csv
import json
import urllib.request
import urllib.error
import ssl
from contextlib import contextmanager
from time import perf_counter

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


def fetch_json(
    url,
    headers=None,
    verify_ssl=True,
    ignore_status_codes=None,
):
    """
    Fetch and return JSON from a URL.

    Args:
        url (str): The JSON endpoint.
        headers (dict, optional): Additional HTTP headers.
        verify_ssl (bool): Whether to verify SSL certificates.
        ignore_status_codes (Iterable[int], optional):
            HTTP status codes to ignore. If encountered, the status
            code and URL are printed and None is returned.

    Returns:
        dict | list | None
    """
    request_headers = DEFAULT_HEADERS.copy()
    if headers:
        request_headers.update(headers)

    request = urllib.request.Request(url, headers=request_headers)

    context = None
    if not verify_ssl:
        context = ssl._create_unverified_context()

    ignored = set(ignore_status_codes or ())

    try:
        with urllib.request.urlopen(request, context=context) as response:
            return json.load(response)

    except urllib.error.HTTPError as e:
        if e.code in ignored:
            print(f"HTTP {e.code}: {url}")
            return None
        
        # Debug purpose
        if e.code == 502:
            import pdb; pdb.set_trace()

        raise RuntimeError(
            f"HTTP Error {e.code}: {e.reason}\n"
            f"{e.read().decode('utf-8', errors='ignore')}"
        ) from e

    except urllib.error.URLError as e:
        raise RuntimeError(f"URL Error: {e.reason}") from e

@contextmanager
def timer(name: str = "Elapsed"):
    start = perf_counter()
    try:
        yield
    finally:
        elapsed = perf_counter() - start
        print(f"{name}: {elapsed:.3f}s")

def clean_data(data):
    """
    Extract and clean data from Continental Final.

    Returns:
        list: The matches data sinitized.
    """
    if data.get("stageName") == []:
        stage_name = ""
    else:
        stage_name = data.get("stageName", [{"description": ""}])[0].get("description")[0]

    if data.get("stadiumName") == []:
        stadium_name = ""
    else:
        stadium_name = data.get("stadiumName", [{"description": ""}])[0].get("description")[0]

    if data.get("competitionName") == []:
        competition_name = ""
    else:
        competition_name = data.get("competitionName", [{"description": ""}])[0].get("description")[0]

    return {
        "id_match": data.get("idMatch", ""),
        "id_match_ifes": data.get("idMatchIfes", ""),
        "id_competition": data.get("idCompetition", ""),
        "id_season": data.get("idSeason", ""),
        "id_stage": data.get("idStage", ""),
        "competition_name": competition_name,
        "season_name": data.get("seasonName",[{"description": ""}])[0].get("description"),
        "stage_name": stage_name
        "match_date": data.get("matchDate", ""),
        "team_A_id": data.get("teamAId", ""),
        "team_B_id": data.get("teamBId", ""),
        "team_A_name": data.get("teamAName", [{"description": ""}])[0].get("description"),
        "team_B_name": data.get("teamBName", [{"description": ""}])[0].get("description"),
        "team_A_country_code": data.get("teamACountryCode", ""),
        "team_B_country_code": data.get("teamBCountryCode", ""),
        "team_A_score": data.get("teamAScore", ""),
        "team_B_score": data.get("teamBScore", ""),
        "team_A_penalty_score": data.get("teamAPenaltyScore", ""),
        "team_B_penalty_score": data.get("teamBPenaltyScore", ""),
        "result_type": data.get("resultType", ""),
        "winner": data.get("winner", ""),
        "has_penalties": data.get("hasPenalties", ""),
    }
