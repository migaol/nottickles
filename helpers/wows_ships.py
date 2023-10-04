import bot_secrets, requests
from helpers import constants
from unidecode import unidecode
from typing import Optional

def get_apidata(url: str) -> Optional[dict]:
    """Get an API response from the given URL.

    Args:
        - url (str): str target URL
    Returns:
        - Optional[dict]: A dict containing JSON data if the request is successful,
            or None if there was an error during the request
    Raises: None
    """
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return
    return response.json()

def load_ship_ids():
    """Load WoWS ship IDs via Wargaming API

    Args:
        None
    Returns:
        None
    Raises:
        - requests.exceptions.RequestException: If an error occurred getting API data
    """
    url = f'https://api.worldofwarships.com/wows/encyclopedia/ships/?application_id={bot_secrets.WOWS_APPID}'
    apidata = get_apidata(url)
    if not apidata: raise requests.exceptions.RequestException()

    total_pages = apidata['meta']['page_total']
    for page in range(1, total_pages+1):
        print(f'\tLoading page {page} of {total_pages}')
        url = f'https://api.worldofwarships.com/wows/encyclopedia/ships/?application_id={bot_secrets.WOWS_APPID}&page_no={page}'
        apidata = get_apidata(url)
        if not apidata: raise requests.exceptions.RequestException()
        for ship_id in apidata['data']:
            ship = apidata['data'][ship_id]['name']
            informal = unidecode(ship).lower().removeprefix('admiral ')
            constants.Wows.ship_index[informal] = {'name': ship, 'id': ship_id}
            constants.Wows.ship_id_index[ship_id] = ship