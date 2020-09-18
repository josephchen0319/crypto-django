import requests
import json
from enum import Enum


class Order(Enum):
    MARKET_CAP_DESC = 'market_cap_desc'
    MARKET_CAP_ASC = 'market_cap_asc'
    GECKO_DESC = 'gecko_desc'
    GECKO_ASC = 'gecko_asc'
    VOLUME_DESC = 'volume_desc'
    VOLUME_ASC = 'volume_asc'
    ID_DESC = 'id_desc'
    ID_ASC = 'id_asc'


class CoinInfo:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"

    def check_server_status(self):
        r = requests.get(COINGECKO_BASE_URL+"/ping")
        return r

    def list_all_coins(self, vs_currency="usd", order=Order.MARKET_CAP_DESC.value, page=1, per_page=100, ids=None):
        price_change_percentage = '1h,24h,7d,30d,200d,1y'
        ids = "" if ids == None else ','.join(ids)
        url = self.base_url + f'/coins/markets?vs_currency={vs_currency}'
        # per_page from 1 - 250
        paging = f'&page={page}&per_page={per_page}'
        query = f'&order={order}&price_change_percentage={price_change_percentage}&ids={ids}'
        r = requests.get(url+paging+query)
        return r

    def get_particular_coin(self, id):
        r = requests.get(
            self.base_url+f'/coins/{id}?localization=false')
        return r

    def get_simple_coin_list(self):
        r = requests.get(
            self.base_url+'/coins/list'
        )
        return r

# if __name__ == "__main__":
    # Check server status
    # res = check_server_status()
    # coin_api = CoinInfo()

    # Test list_all_coins
    # res = coin_api.list_all_coins(
    #     order=Order.GECKO_ASC.value, page=2, per_page=10)
    # all_coins = json.loads(res.content)
    # print(all_coins)

    # Test get_particular_coin
    # res = coin_api.get_particular_coin(id='bitcoin')
    # coin_data = json.loads(res.content)
    # print(coin_data)
