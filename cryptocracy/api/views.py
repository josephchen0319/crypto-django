from graphene_django.views import GraphQLView as BaseGraphQLView
from .loaders import Loaders
from web_crawler.daemon_resource import get_all_coins
import time


class GraphQLView(BaseGraphQLView):
    def get_context(self, request):
        filename = "coin_info.txt"
        get_all_coins(filename=filename, repeat=3600)
        request.loaders = getattr(request, 'loaders', Loaders())
        return request
