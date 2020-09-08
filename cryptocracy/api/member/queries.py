from member import models
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from promise import Promise


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ("password",)


class MemberType(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.Node,)
    state = graphene.String()
    user = graphene.Field(UserType)
    notifications = graphene.ConnectionField(
        'api.member.queries.NotificationConnection')
    # following_coins = graphene.ConnectionField('api.member.queries.FollowingConnection')

    @classmethod
    def is_type_of(cls, root, info: graphene.ResolveInfo) -> bool:
        return isinstance(root, models.Member)

    @classmethod
    def get_node(cls, info: graphene.ResolveInfo, decoded_id: str):
        key = int(decoded_id)
        return info.context.loaders.member.load(key)


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


class Query(graphene.ObjectType):
    node = graphene.Node.Field()
    members = graphene.ConnectionField(MemberConnection)
    me = graphene.Field(MemberType)
    notifications = graphene.ConnectionField(NotificationConnection)

    @staticmethod
    def resolve_members(root: None, info: graphene.ResolveInfo, **kwargs):
        return models.Member.objects.all()

    @staticmethod
    def resolve_me(root, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged In!")

        return user.member

    @staticmethod
    def resolve_notifications(root, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged In!")
        return models.Notification.objects.all()
