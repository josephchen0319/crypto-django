from member import models
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from ..types import MemberConnection, NotificationConnection, MemberType
from graphql_jwt.decorators import login_required, superuser_required


class MemberQuery(graphene.ObjectType):
    node = graphene.Node.Field()
    members = graphene.ConnectionField(MemberConnection)
    me = graphene.Field(MemberType)
    notifications = graphene.relay.ConnectionField(NotificationConnection)

    @staticmethod
    @superuser_required
    def resolve_members(root: None, info: graphene.ResolveInfo, **kwargs):
        return models.Member.objects.all()

    @staticmethod
    @login_required
    def resolve_me(root, info):
        user = info.context.user
        # if user.is_anonymous:
        #     raise Exception("Not logged In!")

        return user.member

    # @staticmethod
    # def resolve_notifications(root, info):
    #     user = info.context.user
    #     if user.is_anonymous:
    #         raise Exception("Not logged In!")
    #     return models.Notification.objects.all()
