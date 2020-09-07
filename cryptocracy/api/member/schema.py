import graphene

from .querys import Query
from .mutations import Mutation


SCHEMA = graphene.Schema(
    query=Query,
    mutation=Mutation,
)
