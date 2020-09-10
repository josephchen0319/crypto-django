from api.filter.queries.filter_query import Query as FilterQuery
from api.web_crawler.queries import Query as CrawlerQuery
from api.member.queries.base_query import Query as MemberQuery


class Query(FilterQuery, CrawlerQuery, MemberQuery):
    pass
