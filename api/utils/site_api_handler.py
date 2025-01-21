from typing import Dict
import requests


def make_response(url: str, headers: Dict, params: Dict, endpoint: str, timeout=10, success=200):
    url = "{}{}".format(url, endpoint)

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=timeout
    )

    return response.json()
