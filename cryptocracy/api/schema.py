import graphene

from api.base.query import Query


SCHEMA = graphene.Schema(
    query=Query,
    # mutation=Mutation,
)
