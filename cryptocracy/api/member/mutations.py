import graphene
from api.member import queries
from member import models
import graphql_jwt


class CreateMember(graphene.Mutation):
    id = graphene.ID()
    user = graphene.Field(queries.UserType)
    # member = graphene.Field(queries.MemberType)
    state = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String()
        last_name = graphene.String()

    def mutate(parent, info, username, email, password, first_name="", last_name=""):

        user = models.User.objects.create(
            username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        state = "Verified"
        member = models.Member.objects.create(user=user, state=state)
        member.save()
        return CreateMember(user=user, state=state)


class UpdateMember(graphene.Mutation):
    id = graphene.ID()
    user = graphene.Field(queries.UserType)
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
    member = graphene.Field(queries.MemberType)

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


class Mutation(graphene.ObjectType):
    create_member = CreateMember.Field()
    update_member = UpdateMember.Field()
    create_notification = CreateNotification.Field()
