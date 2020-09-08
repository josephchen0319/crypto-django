from django.utils.functional import cached_property

from .util import batch_load_primary_key, batch_load_foreign_key, DataLoader


class FilterLoaders:
    @cached_property
    def filter(self) -> DataLoader:
        filter_load_fn = batch_load_primary_key('filter_load_fn', 'Filter')
        return DataLoader(filter_load_fn)

        # @cached_property
        # def filters_from_member(self) -> DataLoader:
        #     stories_from_author_load_fn = batch_load_foreign_key(
        #         'story', 'Story', 'author')
        #     return DataLoader(stories_from_author_load_fn)
