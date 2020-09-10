import graphene
from ..types import FilterConnection
from filter import models


class Query(graphene.ObjectType):
    filters = graphene.relay.ConnectionField(FilterConnection)
    node = graphene.Node.Field()

    @staticmethod
    def resolve_filters(root: None, info: graphene.ResolveInfo, **kwargs):
        return models.Filter.objects.all()
