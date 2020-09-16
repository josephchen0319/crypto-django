from member import models
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from graphql_jwt.decorators import login_required, superuser_required


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ("password",)


class MemberType(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.Node,)

    state = graphene.String()
    user = graphene.Field(UserType)
    notifications = graphene.relay.ConnectionField(
        'api.member.types.NotificationConnection')
    following_coins = graphene.relay.ConnectionField(
        'api.member.types.FollowingConnection')
    saved_filter_groups = graphene.relay.ConnectionField(
        'api.member.types.SavedFilterGroupConnection')

    @classmethod
    def is_type_of(cls, root, info: graphene.ResolveInfo) -> bool:
        return isinstance(root, models.Member)

    @classmethod
    def get_node(cls, info: graphene.ResolveInfo, decoded_id: str):
        key = int(decoded_id)
        return info.context.loaders.member.load(key)

    @staticmethod
    def resolve_notifications(root, info):
        return info.context.loaders.notifications_from_member.load(root.id)

    @staticmethod
    def resolve_following_coins(root, info):
        return info.context.loaders.followings_from_member.load(root.id)

    @staticmethod
    def resolve_saved_filter_groups(root, info):
        return info.context.loaders.saved_filter_groups_from_member.load(root.id)


class MemberConnection(graphene.relay.Connection):
    class Meta:
        node = MemberType


class NotificationType(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.Node,)

    member = graphene.Field(MemberType)
    category = graphene.String()
    title = graphene.String()
    content = graphene.String()
    created_time = graphene.DateTime()
    updated_time = graphene.DateTime()

    @classmethod
    def is_type_of(cls, root, info: graphene.ResolveInfo) -> bool:
        return isinstance(root, models.Notification)

    @classmethod
    def get_node(cls, info: graphene.ResolveInfo, decoded_id: str):
        key = int(decoded_id)
        return info.context.loaders.notification.load(key)


class NotificationConnection(graphene.relay.Connection):
    class Meta:
        node = NotificationType


class FollowingType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node,)

    member = graphene.Field(MemberType)
    crypto_id = graphene.String()
    crypto_symbol = graphene.String()
    state = graphene.String()
    created_time = graphene.DateTime()
    updated_time = graphene.DateTime()

    @classmethod
    def is_type_of(cls, root, info: graphene.ResolveInfo) -> bool:
        return isinstance(root, models.Following)

    @classmethod
    def get_node(cls, info: graphene.ResolveInfo, decoded_id: str):
        key = int(decoded_id)
        return info.context.loaders.following.load(key)


class FollowingConnection(graphene.relay.Connection):
    class Meta:
        node = FollowingType


class SavedFilterGroupType(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.Node, )
    member = graphene.Field(MemberType)
    group_name = graphene.String()
    state = graphene.String()
    created_time = graphene.DateTime()
    updated_time = graphene.DateTime()

    filter_details = graphene.relay.ConnectionField(
        'api.member.types.FilterDetailConnection')

    @classmethod
    def is_type_of(cls, root, info: graphene.ResolveInfo) -> bool:
        return isinstance(root, models.SavedFilterGroup)

    @classmethod
    @login_required
    def get_node(cls, info: graphene.ResolveInfo, decoded_id: str):
        key = int(decoded_id)
        return info.context.loaders.saved_filter_group.load(key)

    @staticmethod
    def resolve_filter_details(root, info):
        return info.context.loaders.filter_details_from_saved_filter_group.load(root.id)


class SavedFilterGroupConnection(graphene.relay.Connection):
    class Meta:
        node = SavedFilterGroupType


class FilterDetailType(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.Node, )
    state = graphene.String()
    first_argument = graphene.Float()
    second_argument = graphene.Float()
    third_argument = graphene.Float()
    fourth_argument = graphene.Float()
    fifth_argument = graphene.Float()
    created_time = graphene.DateTime()
    updated_time = graphene.DateTime()
    filter_group = graphene.Field(SavedFilterGroupType)
    filter = graphene.Field('api.filter.types.FilterType')

    @classmethod
    def is_type_of(cls, root, info: graphene.ResolveInfo) -> bool:
        return isinstance(root, models.FilterDetail)

    @classmethod
    def get_node(cls, info: graphene.ResolveInfo, decoded_id: str):
        key = int(decoded_id)
        return info.context.loaders.filter_detail.load(key)


class FilterDetailConnection(graphene.relay.Connection):
    class Meta:
        node = FilterDetailType
