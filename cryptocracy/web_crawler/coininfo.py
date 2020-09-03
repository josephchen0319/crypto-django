import requests
import json

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"


def check_server_status():
    r = requests.get(COINGECKO_BASE_URL+"/ping")
    return r


if __name__ == "__main__":
    res = check_server_status()
    status = json.loads(res.text)
    print(type(status))
