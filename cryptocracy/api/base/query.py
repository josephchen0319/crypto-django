from api.filter.queries import Query as FilterQuery
from api.web_crawler.queries import Query as CrawlerQuery


class Query(FilterQuery, CrawlerQuery):
    pass
