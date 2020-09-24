from .coininfo import CoinInfo
import json
from background_task import background
# Delete tweets in tweets.txt which created_time is not in 24hr


def store_as_file(filename, data):
    with open(filename, 'a') as t:
        # coinlist = json.loads(data)
        # for coin in coinlist:
        # t.write()
        t.write(data)
        t.write("\n")


@background(schedule=0)
def get_all_coins(filename):
    coin_info = CoinInfo()
    n = 1
    open(filename, 'w').close()
    while n < 25:
        data = coin_info.get_coins(page=n)
        coinlist = json.loads(data.text)
        for coin in coinlist:
            store_as_file(filename, json.dumps(coin))
        n += 1


def delete_file(filename):
    pass
