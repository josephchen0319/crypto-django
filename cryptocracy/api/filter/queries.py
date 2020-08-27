import graphene
from promise import Promise
from filter import models


class FilterType(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.Node,)

    category = graphene.String()
    filter_content = graphene.String()
    formula_id = graphene.String()
    created_time = graphene.DateTime()
    updated_time = graphene.DateTime()

    @classmethod
    def is_type_of(cls, root, info: graphene.ResolveInfo) -> bool:
        return isinstance(root, models.Filter)

    @classmethod
    def get_node(cls, info: graphene.ResolveInfo, decoded_id: str):
        key = int(decoded_id)
        return info.context.loaders.filter.load(key)


class FilterConnection(graphene.Connection):

    class Meta:
        node = FilterType


class Query(graphene.ObjectType):
    filters = graphene.ConnectionField(FilterConnection)
    node = graphene.Node.Field()

    @ staticmethod
    def resolve_filters(root: None, info: graphene.ResolveInfo, **kwargs):
        return models.Filter.objects.all()
