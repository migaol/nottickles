import bot_secrets, requests
from helpers import constants
from unidecode import unidecode

def get_apidata(url):
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return
    return response.json()

def load_ship_ids():
    url = f'https://api.worldofwarships.com/wows/encyclopedia/ships/?application_id={bot_secrets.APPID}'
    apidata = get_apidata(url)
    if not apidata: return

    total_pages = apidata['meta']['page_total']
    for page in range(1, total_pages+1):
        print(f'\tLoading page {page} of {total_pages}')
        url = f'https://api.worldofwarships.com/wows/encyclopedia/ships/?application_id={bot_secrets.APPID}&page_no={page}'
        apidata = get_apidata(url)
        if not apidata: return
        for ship_id in apidata['data']:
            ship = apidata['data'][ship_id]['name']
            informal = unidecode(ship).lower()
            constants.Wows.ship_index[informal] = {'name': ship, 'id': ship_id}