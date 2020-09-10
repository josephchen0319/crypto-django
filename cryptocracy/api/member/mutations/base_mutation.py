from api.member.mutations.member_mutation import MemberMutation
from api.member.mutations.notification_mutation import NotificationMutation
from api.member.mutations.following_mutation import FollowingMutation
from api.member.mutations.saved_filter_group_mutation import SavedFilterGroupMutation
from api.member.mutations.filter_detail_mutation import FilterDetailMutation


class Mutation(MemberMutation,
               NotificationMutation,
               FollowingMutation,
               SavedFilterGroupMutation,
               FilterDetailMutation):
    pass
