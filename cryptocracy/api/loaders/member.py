from django.utils.functional import cached_property
from .util import batch_load_primary_key, batch_load_foreign_key, DataLoader


class MemberLoaders:
    @cached_property
    def member(self) -> DataLoader:
        member_load_fn = batch_load_primary_key('member', 'Member')
        return DataLoader(member_load_fn)

    @cached_property
    def notification(self) -> DataLoader:
        notification_load_fn = batch_load_primary_key(
            'member', 'Notification')
        return DataLoader(notification_load_fn)

    @cached_property
    def notifications_from_member(self) -> DataLoader:
        notifications_from_member_load_fn = batch_load_foreign_key(
            'member', 'Notification', 'member')
        return DataLoader(notifications_from_member_load_fn)

    @cached_property
    def following(self) -> DataLoader:
        following_load_fn = batch_load_primary_key(
            'member', 'Following')
        return DataLoader(following_load_fn)

    @cached_property
    def followings_from_member(self) -> DataLoader:
        followings_from_member_load_fn = batch_load_foreign_key(
            'member', 'Following', 'member')
        return DataLoader(followings_from_member_load_fn)

    @cached_property
    def saved_filter_group(self) -> DataLoader:
        saved_filter_group_load_fn = batch_load_primary_key(
            'member', 'SavedFilterGroup')
        return DataLoader(saved_filter_group_load_fn)

    @cached_property
    def saved_filter_groups_from_member(self) -> DataLoader:
        saved_filter_groups_from_member = batch_load_foreign_key(
            'member', 'SavedFilterGroup', 'member')
        return DataLoader(saved_filter_groups_from_member)

    @cached_property
    def filter_detail(self) -> DataLoader:
        filter_detail_load_fn = batch_load_primary_key(
            'member', 'FilterDetail')
        return DataLoader(filter_detail_load_fn)

    @cached_property
    def filter_details_from_saved_filter_group(self) -> DataLoader:
        filter_details_from_saved_filter_group_load_fn = batch_load_foreign_key(
            'member', 'FilterDetail', 'filter_group')
        return DataLoader(filter_details_from_saved_filter_group_load_fn)

    @cached_property
    def filter_details_from_filter(self) -> DataLoader:
        filter_details_from_filter_load_fn = batch_load_foreign_key(
            'member', 'FilterDetail', 'filter')
        return DataLoader(filter_details_from_filter_load_fn)
