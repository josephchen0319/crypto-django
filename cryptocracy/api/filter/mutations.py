from datetime import date
from typing import Any

import graphene
from filter.models import Filter
from filter.services import FilterService


class CreateFilter(graphene.ClientIDMutation):

    class Input:
        category = graphene.String()
        filter_content = graphene.String()
        formula_id = graphene.String()

    filter = graphene.Field('api.filter.queries.FilterType')

    @classmethod
    def mutate_and_get_payload(cls, root: Any, info: graphene.ResolveInfo,
                               **input_data: dict) -> 'CreateFilter':
        serializer = FilterService(data={
            'category': input_data['category'],
            'filter_content': input_data['filter_content'],
            'formula_id': input_data['formula_id'],
        })
        serializer.is_valid(raise_exception=True)
        filter = serializer.save()
        return cls(filter=filter)


class UpdateFilter(graphene.ClientIDMutation):
    class Input:
        filter_id = graphene.ID()
        category = graphene.String()
        filter_content = graphene.String()
        formula_id = graphene.String()

    filter = graphene.Field('api.filter.queries.FilterType')

    @classmethod
    def mutate_and_get_payload(cls, root: Any, info: graphene.ResolveInfo,
                               **input_data: dict) -> 'UpdateFilter':
        filter_id = input_data['filter_id']  # type: ignore
        serializer = FilterService.for_instance(filter_id, data={
            'category': input_data['category'],
            'filter_content': input_data['filter_content'],
            'formula_id': input_data['formula_id']
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
        filter_id = input_data['filter_id']
        ok = FilterService.delete(filter_id)
        return cls(ok=str(ok))
        # obj = Filter.objects.get(pk=filter_id)
        # obj.delete()
        # return cls(ok=True)


class Mutation(graphene.ObjectType):
    create_filter = CreateFilter.Field()
    update_filter = UpdateFilter.Field()
    delete_filter = DeleteFilter.Field()
