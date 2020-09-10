from member import models
import graphene
from ..types import UserType, MemberType
from django.contrib.auth.models import User
from graphql_jwt.decorators import login_required, superuser_required
from api.utils import from_global_id


class CreateNotification(graphene.relay.ClientIDMutation):

    class Input:
        category = graphene.String()
        title = graphene.String()
        content = graphene.String()

    notification = graphene.Field('api.member.types.NotificationType')

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        user = info.context.user or None

        notification = models.Notification(
            category=input['category'],
            title=input['title'],
            content=input['content'],
            member=user.member,
        )
        notification.save()
        return cls(notification=notification)


class NotificationMutation(graphene.ObjectType):
    create_notification = CreateNotification.Field()
