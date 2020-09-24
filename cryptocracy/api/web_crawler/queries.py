from graphene import ResolveInfo, ObjectType, String, Boolean, ID, Int, Field, Float, Date, List, types
from web_crawler.coininfo import Order, CoinInfo
import json
from collections import namedtuple
from web_crawler.coininfo import CoinInfo
from web_crawler.tweets_getter import TwitterClient, TwitterAnalyzer, filter_amount
import numpy as np
import pandas as pd
import datetime
from graphql.language import ast


class Description(ObjectType):
    en = String()


class Repos_url(ObjectType):
    github = List(type(String()))
    bitbocket = List(type(String()))


class Links(ObjectType):
    homepage = List(type(String()))
    blockchain_site = List(type(String()))
    official_forum_url = List(type(String()))
    chat_url = List(type(String()))
    announcement_url = List(type(String()))
    twitter_screen_name = String()
    facebook_username = String()
    bitcointalk_thread_identifier = String()
    telegram_channel_identifier = String()
    subreddit_url = String()
    repos_url = Field(Repos_url)


class Image(ObjectType):
    thumb = String()
    small = String()
    large = String()


class Currency(ObjectType):
    usd = String()
    btc = String()


class AthDate(ObjectType):
    usd = String()


class AtlDate(ObjectType):
    usd = String()


class MarketData(ObjectType):
    current_price = Field(Currency)
    roi = Field(Currency)
    ath = Field(Currency)
    ath_change_percentage = Field(Currency)
    ath_date = Field(AthDate)
    atl = Field(Currency)
    atl_change_percentage = Field(Currency)
    atl_date = Field(AtlDate)
    market_cap = Field(Currency)
    market_cap_rank = Field(Currency)
    fully_diluted_valuation = Field(Currency)
    total_volume = Field(Currency)
    high_24h = Field(Currency)
    low_24h = Field(Currency)
    price_change_24h = Float()
    price_change_percentage_24h = Float()
    price_change_percentage_7d = Float()
    price_change_percentage_14d = Float()
    price_change_percentage_30d = Float()
    price_change_percentage_60d = Float()
    price_change_percentage_200d = Float()
    price_change_percentage_1y = Float()
    market_cap_change_24h = Float()
    market_cap_change_percentage_24h = Float()
    price_change_24h_in_currency = Field(Currency)
    price_change_percentage_1h_in_currency = Field(Currency)
    price_change_percentage_24h_in_currency = Field(Currency)
    price_change_percentage_7d_in_currency = Field(Currency)
    price_change_percentage_14d_in_currency = Field(Currency)
    price_change_percentage_30d_in_currency = Field(Currency)
    price_change_percentage_60d_in_currency = Field(Currency)
    price_change_percentage_200d_in_currency = Field(Currency)
    price_change_percentage_1y_in_currency = Field(Currency)
    market_cap_change_24h_in_currency = Field(Currency)
    market_cap_change_percentage_24h_in_currency = Field(Currency)
    total_supply = Float()
    max_supply = Float()
    circulating_supply = Float()
    last_updated = String()


class CommunityData(ObjectType):
    facebook_likes = Int()
    twitter_followers = Int()
    reddit_average_posts_48h = Float()
    reddit_average_comments_48h = Float()
    reddit_subscribers = Int()
    reddit_accounts_active_48h = Int()
    telegram_channel_user_count = Int()


class CodeMod4Weeks(ObjectType):
    additions = Int()
    deletions = Int()


class DeveloperData(ObjectType):
    forks = Int()
    stars = Int()
    subscribers = Int()
    total_issues = Int()
    closed_issues = Int()
    pull_requests_merged = Int()
    pull_request_contributors = Int()
    code_additions_deletions_4_weeks = Field(CodeMod4Weeks)
    commit_count_4_weeks = Int()


class PublicInterestStats(ObjectType):
    alexa_rank = Int()
    bing_matches = Int()


class TickerMarket(ObjectType):
    name = String()
    identifier = String()
    has_trading_incentive = Boolean()


class TickerConversion(ObjectType):
    btc = Float()
    eth = Float()
    usd = Float()


class Ticker(ObjectType):
    base = String()
    target = String()
    market = Field(TickerMarket)
    last = Float()
    volume = Float()
    converted_last = Field(TickerConversion)
    converted_volume = Field(TickerConversion)
    trust_score = String()
    bid_ask_spread_percentage = Float()
    timestamp = String()
    last_traded_at = String()
    last_fetch_at = String()
    is_anomaly = Boolean()
    is_stale = Boolean()
    trade_url = String()
    coin_id = String()


class CoinDetail(ObjectType):
    id = String()
    symbol = String()
    name = String()
    asset_platform_id = String()
    block_time_in_minutes = Float()
    hashing_algorithm = String()
    categories = List(type(String()))
    description = Field(Description)
    links = Field(Links)
    image = Field(Image)
    country_origin = String()
    genesis_date = String()
    sentiment_votes_up_percentage = Float()
    sentiment_votes_down_percentage = Float()
    market_cap_rank = Int()
    coingecko_rank = Int()
    coingecko_score = Float()
    developer_score = Float()
    community_score = Float()
    liquidity_score = Float()
    public_interest_score = Float()
    market_data = Field(MarketData)
    community_data = Field(CommunityData)
    developer_data = Field(DeveloperData)
    public_interest_stats = Field(PublicInterestStats)
    status_updates = Field(type(String()))
    last_updated = String()
    tickers = List(Ticker)


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
    ath_date = String()
    atl = Float()
    atl_change_percentage = Float()
    atl_date = String()
    last_updated = String()
    price_change_percentage_14d_in_currency = Float()
    price_change_percentage_1h_in_currency = Float()
    price_change_percentage_1y_in_currency = Float()
    price_change_percentage_200d_in_currency = Float()
    price_change_percentage_24h_in_currency = Float()
    price_change_percentage_30d_in_currency = Float()
    price_change_percentage_7d_in_currency = Float()
    roi = Field(RoiType)


class TwitterUser(ObjectType):
    screen_name = String()
    # followers = Int()
    coins = List(type(String()))
    hashtags = List(type(String()))


class CoinSimpleType(ObjectType):
    id = String()
    symbol = String()


def _json_object_hook(d):
    if 'try' in d:
        d.pop('try')
    return namedtuple('X', d.keys())(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)


class Query(ObjectType):
    coinlist = List(CoinMarketType, page=Int())

    coin_info = CoinInfo()
    twitter_client = TwitterClient()
    tweet_analyzer = TwitterAnalyzer()

    @staticmethod
    def resolve_coinlist(parent, info, **args):
        # coinlist = Query.coin_info.list_all_coins(order=args.get(
        #     "order"), vs_currency=args.get("vs_currency"), page=args.get("page"), per_page=args.get("per_page"))
        coinlist = Query.coin_info.list_all_coins(page=args.get("page"))
        return json2obj(coinlist)

    coin_detail = Field(CoinDetail, id=String())

    @staticmethod
    def resolve_coin_detail(parent, info, **args):
        coin_detail = Query.coin_info.get_particular_coin(id=args.get("id"))
        return json2obj(coin_detail.content)

    twitter_users = List(TwitterUser)

    @staticmethod
    def resolve_twitter_users(parent, info):

        query = "crypto"
        df = pd.DataFrame()
        for i in range(1, 50):
            users = Query.twitter_client.get_relevant_users(
                query, count=20, page=i)
            user_df = Query.tweet_analyzer.users_to_dataframe(users)
            df = df.append(user_df, ignore_index=True)

        filtered_coins = []
        hashtag_list = []
        for d in df['description']:
            coins = Query.tweet_analyzer.get_coins(d)
            coins = list(filter(filter_amount, coins))
            # coins = ' '.join(coins)
            filtered_coins.append(coins)
            hashtags = Query.tweet_analyzer.get_hashtags(d)
            # hashtags = ' '.join(hashtags)
            hashtag_list.append(hashtags)

        df['coins'] = np.array(filtered_coins)
        df['hashtags'] = np.array(hashtag_list)
        json_data = df.to_json(orient="split")
        # print(df)
        return json2obj(json_data)

    coin_simple_list = List(CoinSimpleType)

    @staticmethod
    def resolve_coin_simple_list(parent, info):
        simple_list = Query.coin_info.get_simple_coin_list()
        return json2obj(simple_list.content)
