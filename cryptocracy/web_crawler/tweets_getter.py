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

    def get_search_results(self, query, num_tweets=10):
        # count: The number of results to try and retrieve per page
        # return SearchResults object
        return self.twitter_client.search(q=query, count=num_tweets)

    def get_relevant_users(self, query, count=10, page=1):
        # Search for users by query filter
        return self.twitter_client.search_users(q=query, count=count, page=page)

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

    def get_user_followers(self, id, count=10):
        return self.twitter_client.followers()

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_friends(self, id):
        # Returns an array containing the IDs of users being followed by the specified user.
        return self.twitter_client.friends_ids(id)

    def get_user_followings(self, id):
        # Returns an array containing the IDs of users following the specified user
        return self.twitter_client.followers_ids(id)


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
        # ========================TWEETS KEYS AVAILABLE==========================
        # ['created_at', 'id', 'id_str', 'text', 'source', 'truncated',
        # 'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id',
        # 'in_reply_to_user_id_str', 'in_reply_to_screen_name', 'user', 'geo', 'coordinates',
        # 'place', 'contributors', 'retweeted_status', 'is_quote_status', 'quote_count',
        # 'reply_count', 'retweet_count', 'favorite_count', 'entities', 'favorited',
        # 'retweeted', 'filter_level', 'lang', 'timestamp_ms']
        # ========================================================================
        df = pd.DataFrame(
            data=[tweet.get("text") for tweet in tweets], columns=["tweets"])
        df['user'] = np.array(
            [tweet["user"]["screen_name"] for tweet in tweets])
        df['id'] = np.array([tweet["id"] for tweet in tweets])
        df['timestamp'] = np.array([tweet["created_at"]
                                    for tweet in tweets])
        df['favorite_count'] = np.array(
            [tweet["favorite_count"] for tweet in tweets])
        df['reply_count'] = np.array(
            [tweet["reply_count"] for tweet in tweets])
        df['retweet_count'] = np.array(
            [tweet["retweet_count"] for tweet in tweets])
        return df

    def tweets_users_to_dataframe(self, tweets):
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
        df = pd.DataFrame(data=[tweet["user"]["id"]
                                for tweet in tweets], columns=["users"])
        df['name'] = np.array([tweet["user"]["name"] for tweet in tweets])
        df['followers_count'] = np.array(
            [tweet["user"]["followers_count"] for tweet in tweets])
        df['description'] = np.array(
            [tweet["user"]["description"] for tweet in tweets])

    def users_to_dataframe(self, users):
        # 'contributors_enabled', 'created_at', 'default_profile', 'default_profile_image',
        # 'description', 'entities', 'favourites_count', 'follow', 'follow_request_sent',
        # 'followers', 'followers_count', 'followers_ids', 'following', 'friends',
        # 'friends_count', 'geo_enabled', 'has_extended_profile', 'id', 'id_str',
        # 'is_translation_enabled', 'is_translator', 'lang', 'listed_count', 'lists',
        # 'lists_memberships', 'lists_subscriptions', 'location', 'name', 'notifications',
        # 'parse', 'parse_list', 'profile_background_color', 'profile_background_image_url',
        # 'profile_background_image_url_https', 'profile_background_tile', 'profile_banner_url',
        # 'profile_image_url', 'profile_image_url_https', 'profile_link_color',
        # 'profile_sidebar_border_color', 'profile_sidebar_fill_color', 'profile_text_color',
        # 'profile_use_background_image', 'protected', 'screen_name', 'status',
        # 'statuses_count', 'time_zone', 'timeline', 'translator_type', 'unfollow',
        # 'url', 'utc_offset', 'verified'
        df = pd.DataFrame(
            data=[user.id for user in users], columns=["id"])
        df['followers_count'] = np.array(
            [user.followers_count for user in users])
        df['description'] = np.array([user.description for user in users])
        df['screen_name'] = np.array([user.screen_name for user in users])
        return df

    def get_coins(self, text):
        # Return coins start with $ in text
        coins = re.findall(r'(\$\w+)', text)
        return coins

    def get_hashtags(self, text):
        hashtags = re.findall(r'(\#\w+)', text)
        return hashtags

    def count_occurrence(self, column):
        counts = column.str.split().explode().value_counts()
        return counts


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
    categories = ['crypto', 'defi', 'dapp', 'blockchain']
    file_name = "tweets.txt"
    twitter_client = TwitterClient()
    tweet_analyzer = TwitterAnalyzer()

    # with open(os.path.join(os.path.dirname(__file__), os.pardir, 'tweets.txt'), "r") as t:
    #     # remove blank line, turn non-blank line into dict, and add it to tweets list
    #     tweets = [json.loads(line) for line in t if line.strip()]

    # df = tweet_analyzer.tweets_to_dataframe(tweets)

    # print(df.head(10))

    # query = "crypto OR defi OR dapp OR blockchain"
    query = "crypto"
    df = pd.DataFrame()
    for i in range(1, 50):
        users = twitter_client.get_relevant_users(
            query, count=20, page=i)
        user_df = tweet_analyzer.users_to_dataframe(users)
        df = df.append(user_df, ignore_index=True)

    # df['coins'] = np.array([tweet_analyzer.get_coins(d)
    #                         for d in df['description']])

    filtered_coins = []
    hashtag_list = []
    for d in df['description']:
        coins = tweet_analyzer.get_coins(d)
        coins = list(filter(filter_amount, coins))
        coins = ' '.join(coins)
        filtered_coins.append(coins)
        hashtags = tweet_analyzer.get_hashtags(d)
        hashtags = ' '.join(hashtags)
        hashtag_list.append(hashtags)

    df['coins'] = np.array(filtered_coins)
    df['hashtags'] = np.array(hashtag_list)
    coins_counter = tweet_analyzer.count_occurrence(df['coins'])
    hashtags_counter = tweet_analyzer.count_occurrence(df['hashtags'])
    print(coins_counter)
    print(hashtags_counter)


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
