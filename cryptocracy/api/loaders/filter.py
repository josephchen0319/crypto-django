from django.utils.functional import cached_property

from .util import batch_load_primary_key, batch_load_foreign_key, DataLoader


class FilterLoaders:
    @cached_property
    def filter(self) -> DataLoader:
        filter_load_fn = batch_load_primary_key('filter', 'Filter')
        return DataLoader(filter_load_fn)

    @cached_property
    def filters_from_saved_filter_group(self) -> DataLoader:
        filters_from_saved_filter_group_load_fn = batch_load_foreign_key(
            'filter', 'Filter', 'filter_groups')
        return DataLoader(filters_from_saved_filter_group_load_fn)
