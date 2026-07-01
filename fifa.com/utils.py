import json
import urllib.request
import urllib.error


def fetch_json(url, output_file, headers=None):
    """
    Download JSON from a URL and save it to a file.

    Args:
        url (str): The JSON endpoint.
        output_file (str): Path to the output JSON file.
        headers (dict, optional): Additional HTTP headers.

    Returns:
        dict | list: The parsed JSON object.
    """
    default_headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/137.0 Safari/537.36"
        ),
        "Accept": "application/json",
    }

    if headers:
        default_headers.update(headers)

    request = urllib.request.Request(url, headers=default_headers)

    try:
        with urllib.request.urlopen(request) as response:
            data = json.load(response)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"Saved JSON to '{output_file}'")
        return data

    except urllib.error.HTTPError as e:
        raise RuntimeError(
            f"HTTP Error {e.code}: {e.reason}\n"
            f"{e.read().decode('utf-8', errors='ignore')}"
        )

    except urllib.error.URLError as e:
        raise RuntimeError(f"URL Error: {e.reason}")


if __name__ == "__main__":
    headers = {
        #"User-Agent": "Mozilla/5.0",
        #"Accept": "application/json",
        "Referer": "https://inside.fifa.com/data-centre/teams",
        "Origin": "https://inside.fifa.com",
    }

    fetch_json(
        "https://inside.fifa.com/api/data-centre/matches/teams?gender=1&language=en",
        "mens-teams.json",
    )