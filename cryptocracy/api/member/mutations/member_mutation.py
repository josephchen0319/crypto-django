import graphene
from ..types import UserType, MemberType
from member import models
import graphql_jwt
from django.contrib.auth.models import User


class CreateMember(graphene.Mutation):
    id = graphene.ID()
    user = graphene.Field(UserType)
    # member = graphene.Field(MemberType)
    state = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String()
        last_name = graphene.String()

    def mutate(parent, info, username, email, password, first_name="", last_name=""):

        user = User.objects.create_user(
            username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        state = "Verified"
        member = models.Member.objects.create(user=user, state=state)
        member.save()
        return CreateMember(user=user, state=state)


class UpdateMember(graphene.Mutation):
    id = graphene.ID()
    user = graphene.Field(UserType)
    state = graphene.String()

    class Arguments:
        original_password = graphene.String()
        new_password = graphene.String()
        confirm_password = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()

    def mutate(parent, info, original_password="", new_password="", confirm_password="", first_name="", last_name=""):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged In!")
        member = user.member

        if first_name:
            user.first_name = first_name

        if last_name:
            user.last_name = last_name

        if original_password and user.check_password(original_password) and new_password == confirm_password != "":
            user.set_password(new_password)
        state = "Verified"
        member.state = state
        user.save()
        member.save()
        return UpdateMember(user=user, state=state)


class CreateNotification(graphene.Mutation):
    id = graphene.ID()
    category = graphene.String()
    title = graphene.String()
    content = graphene.String()
    member = graphene.Field(MemberType)

    class Arguments:
        category = graphene.String()
        title = graphene.String()
        content = graphene.String()

    def mutate(parent, info, category, title, content):
        user = info.context.user or None
        if user.is_anonymous:
            raise Exception("Not logged In!")
        notification = models.Notification(
            category=category,
            title=title,
            content=content,
            member=user.member,
        )
        notification.save()
        return CreateNotification(
            id=notification.id,
            category=notification.category,
            title=notification.title,
            content=notification.content,
            member=notification.member,
        )


class MemberMutation(graphene.ObjectType):
    create_member = CreateMember.Field()
    update_member = UpdateMember.Field()
    create_notification = CreateNotification.Field()
