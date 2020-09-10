from ..types import UserType, MemberType
from django.contrib.auth.models import User
import graphene
from member import models
from graphql_jwt.decorators import login_required, superuser_required
from api.utils import from_global_id
from filter.models import Filter


class FilterDetailInputType(graphene.InputObjectType):
    filter_id = graphene.String(required=True)
    state = graphene.String(default_value="relevant")
    first_argument = graphene.Float(default_value=0.0)
    second_argument = graphene.Float(default_value=0.0)
    third_argument = graphene.Float(default_value=0.0)
    fourth_argument = graphene.Float(default_value=0.0)
    fifth_argument = graphene.Float(default_value=0.0)


class CreateFilterDetail(graphene.relay.ClientIDMutation):
    class Input:
        group_id = graphene.String(required=True)
        filter_detail = graphene.Field(FilterDetailInputType)

    filter_group = graphene.Field('api.member.types.SavedFilterGroupType')

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            group_id = int(from_global_id(input['group_id']).type_id)
            filter_group = models.SavedFilterGroup.objects.get(pk=group_id)
            filter_id = int(from_global_id(
                input['filter_detail']['filter_id']).type_id)
            filter = Filter.objects.get(pk=filter_id)
            filter_detail = models.FilterDetail.objects.create(
                filter_group=filter_group,
                filter=filter,
                state=input['filter_detail']['state'],
                first_argument=input['filter_detail']['first_argument'],
                second_argument=input['filter_detail']['second_argument'],
                third_argument=input['filter_detail']['third_argument'],
                fourth_argument=input['filter_detail']['fourth_argument'],
                fifth_argument=input['filter_detail']['fifth_argument']
            )
            filter_detail.save()
            return cls(filter_group=filter_group)
        except Exception:
            return "Failed to create filter detail!"


class UpdateFilterDetail(graphene.relay.ClientIDMutation):

    class Input:
        filter_detail_id = graphene.String(required=True)
        state = graphene.String(default_value="relevant")
        first_argument = graphene.Float(default_value=0.0)
        second_argument = graphene.Float(default_value=0.0)
        third_argument = graphene.Float(default_value=0.0)
        fourth_argument = graphene.Float(default_value=0.0)
        fifth_argument = graphene.Float(default_value=0.0)

    filter_group = graphene.Field('api.member.types.SavedFilterGroupType')

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        # try:
        filter_detail_id = int(from_global_id(
            input['filter_detail_id']).type_id
        )
        filter_detail = models.FilterDetail.objects.get(
            pk=filter_detail_id)
        filter_group = filter_detail.filter_group

        if 'state' in input.keys():
            filter_detail.state = input['state']
        if input['first_argument'] != 0.0:
            filter_detail.first_argument = input['first_argument']
        if input['second_argument'] != 0.0:
            filter_detail.second_argument = input['second_argument']
        if input['third_argument'] != 0.0:
            filter_detail.third_argument = input['third_argument']
        if input['fourth_argument'] != 0.0:
            filter_detail.fourth_argument = input['fourth_argument']
        if input['fifth_argument'] != 0.0:
            filter_detail.fifth_argument = input['fifth_argument']

        filter_detail.save()
        return cls(filter_group=filter_group)
        # except Exception:
        #     return "Failed to update filter detail!"


class DeleteFilterDetail(graphene.relay.ClientIDMutation):
    class Input:
        filter_detail_id = graphene.String()

    filter_group = graphene.Field('api.member.types.SavedFilterGroupType')

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            filter_detail_id = int(from_global_id(
                input['filter_detail_id']).type_id
            )
            filter_detail = models.FilterDetail.objects.get(
                pk=filter_detail_id)
            filter_group = filter_detail.filter_group
            filter_detail.delete()
            return cls(filter_group=filter_group)
        except Exception:
            return "Failed to delete filter detail!"


class FilterDetailMutation(graphene.ObjectType):
    create_filter_detail = CreateFilterDetail.Field()
    update_filter_detail = UpdateFilterDetail.Field()
    delete_filter_detail = DeleteFilterDetail.Field()
