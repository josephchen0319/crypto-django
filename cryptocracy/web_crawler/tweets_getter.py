import json

from tweepy import OAuthHandler, API, Cursor
import twitter_credentials
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from textblob import TextBlob
import re
from tweets_streamer import TwitterStreamer
import os


class TwitterClient():

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate()
        self.twitter_client = API(self.auth, wait_on_rate_limit=True)
        self.twitter_user = twitter_user

    def get_user_timelines(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_users(self, user_ids):
        return self.twitter_client.lookup_users(screen_names=user_ids)

    def get_coins(self, text):
        # Return coins start with $ in text
        coins = re.findall(r'(\$\w+)', text)
        return coins

    def get_hashtags(self, text):
        hashtags = re.findall(r'(\#\w+)', text)
        return hashtags

    def get_search_results(self, query, num_tweets):
        # count: The number of results to try and retrieve per page
        # return SearchResults object
        return self.twitter_client.search(q=query, count=num_tweets)

    def get_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_twitter_client_api(self):
        return self.twitter_client


class TwitterAuthenticator:

    def authenticate(self):
        auth = OAuthHandler(twitter_credentials.API_KEY,
                            twitter_credentials.API_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN,
                              twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth


class TwitterAnalyzer:

    def clean_tweet(self, text):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

    def analyze_sentiment(self, text):
        analysis = TextBlob(self.clean_tweet(text))
        return analysis.sentiment.polarity
        # if analysis.sentiment.polarity > 0:
        #     return 1
        # elif analysis.sentiment.polarity == 0:
        #     return 0
        # else:
        #     return -1

    def tweets_to_dataframe(self, tweets):
        df = pd.DataFrame(
            data=[tweet.text for tweet in tweets], columns=["tweets"])
        df['user'] = np.array([tweet.author.screen_name for tweet in tweets])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['timestamp'] = np.array([tweet.created_at for tweet in tweets])
        # df['retweets'] = np.array([tweet.retweets for tweet in tweets])
        # df['favorite_count'] = np.array(
        #     [tweet.favorite_count for tweet in tweets])
        return df


def is_float(n):
    try:
        float_n = float(n)
    except ValueError:
        return False
    else:
        return True


def filter_amount(dollar):
    sub = dollar[1:]
    if is_float(sub):
        return None
    else:
        return dollar


if __name__ == "__main__":
    categories = ['crypto', 'defi', 'dapp']
    file_name = "tweets.json"
    # users = [
    #     'CryptoGodfatha',
    #     'MoonOverlord',
    #     'MiddleChildPabk',
    #     'CryptoGodJohn',
    #     'DuckwingDark',
    #     'TeddyCleps',
    #     'HerroCrypto',
    #     'YFLinkio',
    #     'damskotrades',
    #     'fonship',
    # ]

    # api = twitter_client.get_twitter_client_api()
    # user_timeline = twitter_client.get_user_timelines(10)

    # ========================TWEETS KEYS AVAILABLE==========================
    # ['created_at', 'id', 'id_str', 'text', 'source', 'truncated',
    # 'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id',
    # 'in_reply_to_user_id_str', 'in_reply_to_screen_name', 'user', 'geo', 'coordinates',
    # 'place', 'contributors', 'retweeted_status', 'is_quote_status', 'quote_count',
    # 'reply_count', 'retweet_count', 'favorite_count', 'entities', 'favorited',
    # 'retweeted', 'filter_level', 'lang', 'timestamp_ms']
    # ========================================================================

    # ========================USER KEYS AVAILABLE==========================
    # ['id', 'id_str', 'name', 'screen_name', 'location', 'url', 'description',
    # 'translator_type', 'protected', 'verified', 'followers_count', 'friends_count',
    # 'listed_count', 'favourites_count', 'statuses_count', 'created_at', 'utc_offset',
    # 'time_zone', 'geo_enabled', 'lang', 'contributors_enabled', 'is_translator',
    # 'profile_background_color', 'profile_background_image_url', 'profile_background_image_url_https',
    # 'profile_background_tile', 'profile_link_color', 'profile_sidebar_border_color',
    # 'profile_sidebar_fill_color', 'profile_text_color', 'profile_use_background_image',
    # 'profile_image_url', 'profile_image_url_https', 'profile_banner_url', 'default_profile',
    # 'default_profile_image', 'following', 'follow_request_sent', 'notifications']
    # ========================================================================

    # with open(os.path.join(os.path.dirname(__file__), os.pardir, 'tweets.txt'), "r") as t:
    #     # remove blank line, turn non-blank line into dict, and add it to tweets list
    #     tweets = [json.loads(line) for line in t if line.strip()]

    # print(tweets[1])

    lines = """
      apple pie

      helolo world
    """
    for line in lines:
        if line.strip():
            print(True)
        else:
            print(False)

    twitter_client = TwitterClient()
    tweet_analyzer = TwitterAnalyzer()

    # search_results = twitter_client.get_search_results(
    #     "#crypto OR #defi OR #dapp OR #blockchain OR crypto OR defi OR dapp OR blockchain", 500)
    # df = tweet_analyzer.tweets_to_dataframe(search_results)

    # df['sentiment'] = np.array(
    #     [tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])

    # filtered_coins = []
    # hashtag_list = []
    # for tweet in df['tweets']:
    #     coins = twitter_client.get_coins(tweet)
    #     coins = list(filter(filter_amount, coins))
    #     coins = ' '.join(coins)
    #     filtered_coins.append(coins)
    #     hashtags = twitter_client.get_hashtags(tweet)
    #     hashtags = ' '.join(hashtags)
    #     hashtag_list.append(hashtags)

    # df['coins'] = np.array(filtered_coins, dtype=object)
    # df['hashtags'] = np.array(hashtag_list, dtype=object)

    # counts = df.coins.str.split().explode().value_counts()
    # print(counts.to_json())
    # for sr in search_results:
    #     print(sr.text)
    #     print('--------------------------------------------------')

    # users = twitter_client.get_users(users)
    # for user in users:
    #     twitter_client.get_coins(user.description)
    #     print(user.screen_name + ": ")
    #     print(*coins)
    #     print("=========================================")

    # tweets = api.user_timeline(screen_name="VitalikButerin", count=5)
    # df = tweet_analyzer.tweets_to_dataframe(tweets)
    # df['sentiment'] = np.array(
    #     [tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])

    # print(df.head(10))
    # print(dir(tweets[0]))
    # print(tweets[0].author.screen_name)
    # print(tweets[0].text)
    # for t in tweets:
    #     print(t.author.screen_name)
    #     print(t.text)
    #     print("=====================RE========================")
    #     rts = t.retweets()
    #     for rt in rts:
    #         # print(rt._json.keys())
    #         # print(rt._json.get('user'))
    #         print(rt._json.get('text'))

    #     print('================================================')
    # print(tweets[0].retweets()[0]._json.get('text'))
    # print(df.head(10))
    # streamer = TwitterStreamer()
    # streamer.stream_tweets(file_name, categories)

    # time_likes = pd.Series(
    #     data=df['favorite_count'].values, index=df['timestamp'])
    # time_likes.plot(figsize=(16, 4), color='r', label='likes', legend=True)
    # plt.show()

    # GET REPLIES OF PARTICULAR USER

    # replies = []
    # non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    # for full_tweets in Cursor(api.user_timeline, screen_name='VitalikButerin', timeout=999999).items(10):
    #     for tweet in Cursor(api.search, q='to:'+'VitalikButerin', result_type='recent', timeout=999999).items(1000):
    #         if hasattr(tweet, 'in_reply_to_status_id_str'):
    #             if (tweet.in_reply_to_status_id_str == full_tweets.id_str):
    #                 replies.append(tweet.text)
    #     print("Tweet :", full_tweets.text.translate(non_bmp_map))
    #     for elements in replies:
    #         print("Replies :", elements)
    #     replies.clear()
