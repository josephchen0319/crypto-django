import graphene

from .queries.base_query import Query
from .mutations.base_mutation import Mutation


SCHEMA = graphene.Schema(
    query=Query,
    mutation=Mutation,
)
