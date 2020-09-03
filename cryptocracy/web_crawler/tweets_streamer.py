from tweepy.streaming import StreamListener
from tweepy import Stream
import json


class TwitterStreamer():
    def __init__(self):
        from tweets_getter import TwitterAuthenticator
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_file, hash_tag_list):
        # This handles twitter authentication and connection to the twitter filter stream
        listener = CryptoListener(fetched_tweets_file)
        auth = self.twitter_authenticator.authenticate()
        stream = Stream(auth, listener)
        # stream.filter(track=hash_tag_list, is_async=True)
        stream.filter(track=hash_tag_list)


class CryptoListener(StreamListener):
    # Listener class
    def __init__(self, fetched_tweets_file):
        self.fetched_tweets_file = fetched_tweets_file

    def on_data(self, data):
        try:
            with open(self.fetched_tweets_file, 'a') as t:
                t.write(data)
            return True
        except Exception as e:
            print(f'Error! {e}')
        return True

    def on_error(self, status):
        if status == 420:
            # Return False in case rate limit occurs
            return False
        print(status)


if __name__ == "__main__":
    search_list = [
        "crypto",
        "defi",
        "dapp",
        "blockchain",
    ]
    stream = TwitterStreamer()
    stream.stream_tweets("tweets.txt", search_list)
