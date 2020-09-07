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


class Query(graphene.ObjectType):
    members = graphene.ConnectionField(MemberConnection)
    node = graphene.Node.Field()
    me = graphene.Field(MemberType)

    @staticmethod
    def resolve_members(root: None, info: graphene.ResolveInfo, **kwargs):
        return models.Member.objects.all()

    @staticmethod
    def resolve_me(root, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged In!")
        return user.member
