from graphene import ResolveInfo, ObjectType, String, Boolean, ID, Int, Field, Float, Date, DateTime, List
from web_crawler.coininfo import Order, CoinInfo
import json
from collections import namedtuple
from web_crawler.coininfo import CoinInfo


class RoiType(ObjectType):
    currency = String()
    times = Float()
    percentage = Float()


class CoinMarketType(ObjectType):
    id = String()
    symbol = String()
    name = String()
    image = String()
    current_price = Float()
    market_cap = Float()
    market_cap_rank = Int()
    fully_diluted_valuation = Float()
    total_volume = Float()
    high_24h = Float()
    low_24h = Float()
    price_change_24h = Float()
    price_change_percentage_24h = Float()
    market_cap_change_24h = Float()
    market_cap_change_percentage_24h = Float()
    circulating_supply = Float()
    total_supply = Float()
    max_supply = Float()
    ath = Float()
    ath_change_percentage = Float()
    ath_date = Date()
    atl = Float()
    atl_change_percentage = Float()
    atl_date = Date()
    last_updated = DateTime()
    price_change_percentage_14d_in_currency = Float()
    price_change_percentage_1h_in_currency = Float()
    price_change_percentage_1y_in_currency = Float()
    price_change_percentage_200d_in_currency = Float()
    price_change_percentage_24h_in_currency = Float()
    price_change_percentage_30d_in_currency = Float()
    price_change_percentage_7d_in_currency = Float()
    roi = Field(RoiType)


def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)


class Query(ObjectType):
    coinlist = List(CoinMarketType, order=String(),
                    page=Int(), per_page=Int())

    # def resolve_coinlist(self, args, context, info):
    @ staticmethod
    def resolve_coinlist(self, info, **args):
        coin_info = CoinInfo()
        coinlist = coin_info.list_all_coins(order=args.get(
            "order"), page=args.get("page"), per_page=args.get("per_page"))
        return json2obj(coinlist.content)
