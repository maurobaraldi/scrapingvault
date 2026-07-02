import csv
import json
import urllib.request
import urllib.error
import ssl


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


def fetch_json(url, headers=None, verify_ssl=True):
    """
    Fetch and return JSON from a URL.

    Args:
        url (str): The JSON endpoint.
        headers (dict, optional): Additional HTTP headers.
        verify_ssl (bool): Whether to verify SSL certificates.

    Returns:
        dict | list
    """
    request_headers = DEFAULT_HEADERS.copy()
    if headers:
        request_headers.update(headers)

    request = urllib.request.Request(url, headers=request_headers)

    context = None
    if not verify_ssl:
        context = ssl._create_unverified_context()

    try:
        with urllib.request.urlopen(request, context=context) as response:
            return json.load(response)

    except urllib.error.HTTPError as e:
        raise RuntimeError(
            f"HTTP Error {e.code}: {e.reason}\n"
            f"{e.read().decode('utf-8', errors='ignore')}"
        )

    except urllib.error.URLError as e:
        raise RuntimeError(f"URL Error: {e.reason}")


def save_json(data, output_file):
    """
    Save a Python object as JSON.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def fetch_json_to_file(url, output_file, headers=None, verify_ssl=True):
    """
    Fetch JSON from a URL and save it to a file.

    Returns:
        dict | list: The downloaded JSON.
    """
    data = fetch_json(url, headers=headers, verify_ssl=verify_ssl)
    save_json(data, output_file)
    return data


def save_dicts_to_csv(rows, output_file):
    """
    Save a list of dictionaries to a CSV file.

    Args:
        rows (list[dict]): List of flat dictionaries.
        output_file (str): Path to the output CSV file.
    """
    if not rows:
        raise ValueError("rows cannot be empty")

    # Collect all keys while preserving order of first appearance.
    fieldnames = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
        

def clean_data(data):
    """
    Extract and clean data from Continental Final.

    Returns:
        list: The matches data sinitized.
    """
    if data.get("stageName") == []:
        stage_name = ""
    else:
        stage_name = data.get("stageName", [{"description": ""}])[0].get("description"),

    if data.get("stadiumName") == []:
        stadium_name = ""
    else:
        stadium_name = data.get("stadiumName", [{"description": ""}])[0].get("description"),


    return {
        "id_match": data.get("idMatch", ""),
        "id_match_ifes": data.get("idMatchIfes", ""),
        "id_competition": data.get("idCompetition", ""),
        "id_season": data.get("idSeason", ""),
        "id_stage": data.get("idStage", ""),
        "competition_name": data.get("competitionName", [{"description": ""}])[0].get("description"),
        "season_name": stage_name,
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
