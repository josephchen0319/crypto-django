import graphene

from api.base.query import Query
from api.base.mutation import Mutation

SCHEMA = graphene.Schema(
    query=Query,
    mutation=Mutation,
)
