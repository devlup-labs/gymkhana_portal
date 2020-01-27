import graphene
from django.contrib.auth.mixins import LoginRequiredMixin
from graphene import relay, Connection
from graphene_django import DjangoConnectionField
from graphene_django.views import GraphQLView

from konnekt.schema import Query as KonnektQuery
from oauth.schema import UserProfileNode, UserNode
from main.schema import SocietyNode, ClubNode


class SearchResult(graphene.Union):
    class Meta:
        types = (UserProfileNode,)


class SearchResultConnection(Connection):
    class Meta:
        node = SearchResult


class NodeType(graphene.Enum):
    USER_PROFILE = UserProfileNode


class Query(KonnektQuery, graphene.ObjectType):
    viewer = graphene.Field(UserNode)
    node = relay.Node.Field()
    search = graphene.ConnectionField(
        SearchResultConnection,
        query=graphene.String(description='Value to search for', required=True),
        node_type=NodeType(required=True)
    )
    societies = DjangoConnectionField(SocietyNode)
    clubs = DjangoConnectionField(ClubNode)

    def resolve_viewer(self, info, *args):
        return UserNode.get_node(info, id=info.context.user.id)

    def resolve_search(self, info, query=None, node_type=None, first=None, last=None, before=None, after=None):
        # TODO: Add logic to paginate search based on first, last, before and after params
        if node_type == UserProfileNode:
            if first:
                return UserProfileNode.search(query, info)[:first]
            return UserProfileNode.search(query, info)
        return []


class PrivateGraphQLView(GraphQLView):
    pass


schema = graphene.Schema(query=Query)
