from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
from web_crawler.tweets_streamer import CryptoListener
from tweepy import OAuthHandler, Stream
import json
# Create your views here.


# class Crawler(View):
#     def get(self, request):
#         listener = CryptoListener()
#         auth = OAuthHandler(twitter_credentials.API_KEY,
#                             twitter_credentials.API_SECRET)
#         auth.set_access_token(twitter_credentials.ACCESS_TOKEN,
#                               twitter_credentials.ACCESS_TOKEN_SECRET)
#         stream = Stream(auth, listener)
#         stream.filter(track=['crypto', 'defi', 'dapp'])
#         return HttpResponse(stream.filter(track=['crypto', 'defi', 'dapp']))
# url = "https://twitter.com/VitalikButerin"
# url = "https://requests.readthedocs.io/projects/requests-html/en/latest/#requests_html.HTML"
# json_data = TwitterCrawler.get_links(url)
# articles = TwitterCrawler.get_twitter_articles(url)

# return JsonResponse(json_data)
