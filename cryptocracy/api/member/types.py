from member import models
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User


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
    # following_coins = graphene.ConnectionField('api.member.queries.FollowingConnection')

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


class MemberConnection(graphene.Connection):
    class Meta:
        node = MemberType


class NotificationType(graphene.ObjectType):

    member = graphene.Field(MemberType)
    category = graphene.String()
    title = graphene.String()
    content = graphene.String()
    created_time = graphene.DateTime()


class NotificationConnection(graphene.Connection):
    class Meta:
        node = NotificationType
