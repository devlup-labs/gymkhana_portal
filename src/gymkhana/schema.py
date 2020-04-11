import graphene
import graphql_jwt
from django.conf import settings
from graphene import relay, Connection
from graphene_django import DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.views import GraphQLView
from photologue.models import Gallery
from festivals.schema import FestivalNode
from forum.schema import TopicNode, CreateTopicMutation, AddAnswerMutation, UpvoteMutaiton
from konnekt.schema import Query as KonnektQuery
from oauth.schema import UserProfileNode, UserNode, ProfileMutation
from main.schema import SocietyNode, ClubNode, GalleryNode


class SearchResult(graphene.Union):
    class Meta:
        types = (UserProfileNode, TopicNode,)


class SearchResultConnection(Connection):
    class Meta:
        node = SearchResult


class NodeType(graphene.Enum):
    USER_PROFILE = UserProfileNode
    TOPIC = TopicNode


class PublicQuery(graphene.ObjectType):
    node = relay.Node.Field()
    societies = DjangoFilterConnectionField(SocietyNode)
    clubs = DjangoFilterConnectionField(ClubNode)
    festivals = DjangoConnectionField(FestivalNode)
    home_carousel = graphene.Field(GalleryNode)
    home_gallery = graphene.Field(GalleryNode)

    def resolve_home_carousel(self, info, *args):
        return Gallery.objects.filter(slug=settings.HOME_PAGE_CAROUSEL_GALLERY_SLUG).first()

    def resolve_home_gallery(self, info, *args):
        return Gallery.objects.filter(slug=settings.HOME_PAGE_GALLERY_SLUG).first()


class PrivateQuery(KonnektQuery, PublicQuery):
    viewer = graphene.Field(UserNode)
    search = graphene.ConnectionField(
        SearchResultConnection,
        query=graphene.String(description='Value to search for', required=True),
        node_type=NodeType(required=True)
    )
    forum_topics = graphene.ConnectionField(
        SearchResultConnection,
        query=graphene.String(description='Topic to search for', required=True),
        node_type=NodeType(required=True)
    )

    def resolve_viewer(self, info, *args):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception('Not logged in!')
        return UserNode.get_node(info, id=info.context.user.id)

    def resolve_search(self, info, query=None, node_type=None, first=None, last=None, before=None, after=None):
        # TODO: Add logic to paginate search based on first, last, before and after params
        if node_type == UserProfileNode:
            if first:
                return UserProfileNode.search(query, info)[:first]
            return UserProfileNode.search(query, info)
        return []

    def resolve_forum_topics(self, info, query=None, node_type=None, first=None, last=None, before=None, after=None):
        if node_type == TopicNode:
            if first:
                return TopicNode.search(query, info)[:first]
            return TopicNode.search(query, info)
        return []


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    update_profile = ProfileMutation.Field()
    create_topic = CreateTopicMutation.Field()
    add_answer = AddAnswerMutation.Field()
    upvote = UpvoteMutaiton.Field()


class PrivateGraphQLView(GraphQLView):
    schema = graphene.Schema(PrivateQuery, mutation=Mutation)


class PublicGraphQLView(GraphQLView):
    pass


schema = graphene.Schema(PublicQuery)
