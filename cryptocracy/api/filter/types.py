from filter import models
import graphene
from graphql_jwt.decorators import login_required, superuser_required
from promise import Promise
from api.utils import from_global_id


class FilterType(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.Node,)

    category = graphene.String()
    filter_name = graphene.String()
    filter_content = graphene.String()
    created_time = graphene.DateTime()
    updated_time = graphene.DateTime()
    filter_details = graphene.relay.ConnectionField(
        'api.member.types.FilterDetailConnection')

    @staticmethod
    def resolve_filter_details(root, info):
        return info.context.loaders.filter_details_from_filter.load(root.id)

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
