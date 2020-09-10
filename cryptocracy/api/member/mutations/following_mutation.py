from ..types import UserType, MemberType
from django.contrib.auth.models import User
import graphene
from member import models
from graphql_jwt.decorators import login_required, superuser_required
from api.utils import from_global_id


class FollowCoin(graphene.relay.ClientIDMutation):
    class Input:
        crypto_id = graphene.String(required=True)
        crypto_symbol = graphene.String(required=True)

    following = graphene.Field('api.member.types.FollowingType')

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        state = 'get notifications'
        member = info.context.user.member
        following = models.Following.objects.create(
            crypto_id=input['crypto_id'], crypto_symbol=input['crypto_symbol'], state=state, member=member)
        following.save()
        return cls(following=following)


class UnfollowCoin(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.String(required=True)
    ok = graphene.Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            _id = int(from_global_id(input['id']).type_id)
            following = models.Following.objects.get(pk=_id)
            following.delete()
            ok = True
        except Exception:
            ok = False
        return cls(ok=ok)


class UpdateFollowingState(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.String(required=True)
        state = graphene.String(required=True)

    following = graphene.Field('api.member.types.FollowingType')

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        # try:
        _id = int(from_global_id(input['id']).type_id)
        following = models.Following.objects.get(pk=_id)
        following.state = input['state']
        following.save()
        # except Exception:
        #     return "Update failed!"
        return cls(following=following)


class FollowingMutation(graphene.ObjectType):
    follow_coin = FollowCoin.Field()
    unfollow_coin = UnfollowCoin.Field()
    update_following_state = UpdateFollowingState.Field()
