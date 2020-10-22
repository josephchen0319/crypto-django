from datetime import date
from typing import Any

import graphene
from filter.models import Filter
from filter.services import FilterService
from api.utils import from_global_id


class CreateFilter(graphene.relay.ClientIDMutation):

    class Input:
        category = graphene.String()
        filter_name = graphene.String()
        filter_content = graphene.String()
        filter_to_api_field = graphene.String()

    filter = graphene.Field('api.filter.types.FilterType')

    @classmethod
    def mutate_and_get_payload(cls, root: Any, info: graphene.ResolveInfo,
                               **input_data: dict) -> 'CreateFilter':
        serializer = FilterService(data={
            'category': input_data['category'],
            'filter_name': input_data['filter_name'],
            'filter_content': input_data['filter_content'],
            'filter_to_api_field': input_data['filter_to_api_field'],
        })
        serializer.is_valid(raise_exception=True)
        filter = serializer.save()
        return cls(filter=filter)


class UpdateFilter(graphene.relay.ClientIDMutation):
    class Input:
        filter_id = graphene.ID()
        category = graphene.String()
        filter_name = graphene.String()
        filter_content = graphene.String()

    filter = graphene.Field('api.filter.types.FilterType')

    @classmethod
    def mutate_and_get_payload(cls, root: Any, info: graphene.ResolveInfo,
                               **input_data: dict) -> 'UpdateFilter':

        filter_id = int(from_global_id(input_data['filter_id']).type_id)
        serializer = FilterService.for_instance(filter_id, data={
            'category': input_data['category'],
            'filter_name': input_data['filter_name'],
            'filter_content': input_data['filter_content'],
        })
        serializer.is_valid(raise_exception=True)
        filter = serializer.save()
        return cls(filter=filter)


class DeleteFilter(graphene.ClientIDMutation):
    class Input:
        filter_id = graphene.ID()

    ok = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root: Any, info: graphene.ResolveInfo,
                               **input_data: dict) -> 'DeleteFilter':
        filter_id = int(from_global_id(input_data['filter_id']).type_id)
        ok = FilterService.delete(filter_id)
        return cls(ok=str(ok))


class Mutation(graphene.ObjectType):
    create_filter = CreateFilter.Field()
    update_filter = UpdateFilter.Field()
    delete_filter = DeleteFilter.Field()
