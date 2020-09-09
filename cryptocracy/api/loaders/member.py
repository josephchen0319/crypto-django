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
        return DataLoader(notification_load_fn)

    @cached_property
    def saved_filter_group(self) -> DataLoader:
        Saved_filter_group_load_fn = batch_load_primary_key(
            'member', 'Saved_filter_group')
        return DataLoader(Saved_filter_group_load_fn)

    # @cached_property
    # def saved_filter_groups_from_member(self) -> DataLoader:
    #     filters_from_member_load_fn = batch_load_foreign_key(
    #         'filter', 'Filter', 'member')
    #     return DataLoader(stories_from_author_load_fn)
