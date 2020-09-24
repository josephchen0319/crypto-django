from ..types import UserType, MemberType
from django.contrib.auth.models import User
import graphene
from member import models
from filter.models import Filter
from graphql_jwt.decorators import login_required, superuser_required
from api.utils import from_global_id
from api.member.mutations.filter_detail_mutation import FilterDetailInputType


class CreateFilterGroup(graphene.relay.ClientIDMutation):
    class Input:
        group_name = graphene.String()

        filter_details = graphene.List(FilterDetailInputType)

    filter_group = graphene.Field('api.member.types.SavedFilterGroupType')

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            member = info.context.user.member
            filter_group_state = "notify"
            filter_group = models.SavedFilterGroup.objects.create(
                member=member, group_name=input['group_name'], state=filter_group_state
            )
            filter_group.save()
            filter_details = input['filter_details']
            for filter_detail in filter_details:
                filter_id = int(from_global_id(
                    filter_detail['filter_id']).type_id)
                filter = Filter.objects.get(pk=filter_id)
                detail = models.FilterDetail.objects.create(
                    filter_group=filter_group, filter=filter,
                    state=filter_detail['state'], first_argument=filter_detail['first_argument'],
                    second_argument=filter_detail['second_argument'],
                    third_argument=filter_detail['third_argument'],
                    fourth_argument=filter_detail['fourth_argument'],
                    fifth_argument=filter_detail['fifth_argument'])
                detail.save()
        except Exception:
            return "Error creating new filter group!"

        return cls(filter_group=filter_group)


class UpdateFilterGroup(graphene.relay.ClientIDMutation):
    class Input:
        group_id = graphene.String()
        group_name = graphene.String()
        state = graphene.String(default_value="notify")
        filter_details = graphene.List(FilterDetailInputType)

    filter_group = graphene.Field('api.member.types.SavedFilterGroupType')

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            group_id = int(from_global_id(input['group_id']).type_id)
            filter_group = models.SavedFilterGroup.objects.get(pk=group_id)
            filter_group.state = input['state']
            filter_group.group_name = input['group_name']
            filter_group.save()

            original_filterDetails = models.FilterDetail.objects.filter(
                filter_group__pk=group_id).delete()

        except Exception:
            print("Error updating new filter group!")
        finally:
            filter_details = input['filter_details']

            for filter_detail in filter_details:
                filter_id = int(from_global_id(
                    filter_detail['filter_id']).type_id)
                filter = Filter.objects.get(pk=filter_id)
                detail = models.FilterDetail.objects.create(
                    filter_group=filter_group, filter=filter,
                    state=filter_detail['state'], first_argument=filter_detail['first_argument'],
                    second_argument=filter_detail['second_argument'],
                    third_argument=filter_detail['third_argument'],
                    fourth_argument=filter_detail['fourth_argument'],
                    fifth_argument=filter_detail['fifth_argument'])
                detail.save()
        return cls(filter_group=filter_group)


class DeleteFilterGroup(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.String()

    ok = graphene.Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            filter_id = int(from_global_id(input['id']).type_id)
            filter_group = models.SavedFilterGroup.objects.get(pk=filter_id)
            filter_group.delete()
            ok = True
        except Exception:
            ok = False
        return cls(ok=ok)


class SavedFilterGroupMutation(graphene.ObjectType):
    create_filter_group = CreateFilterGroup.Field()
    update_filter_group = UpdateFilterGroup.Field()
    delete_filter_group = DeleteFilterGroup.Field()
