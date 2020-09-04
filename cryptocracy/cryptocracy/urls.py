from django.contrib import admin
from django.urls import path

from django.views.decorators.csrf import csrf_exempt
from web_crawler.views import Crawler
from api.schema import SCHEMA
from api.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(GraphQLView.as_view(schema=SCHEMA, graphiql=True))),

]
