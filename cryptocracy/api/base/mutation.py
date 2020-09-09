from api.filter.mutations import Mutation as FilterMutation
from api.member.mutations.base_mutation import Mutation as MemberMutation
import graphql_jwt


class Mutation(FilterMutation, MemberMutation):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
