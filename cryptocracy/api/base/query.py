from api.filter.queries import Query as FilterQuery
from api.web_crawler.queries import Query as CrawlerQuery
from api.member.queries import Query as MemberQuery


class Query(FilterQuery, CrawlerQuery, MemberQuery):
    pass
