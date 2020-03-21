from django.contrib.auth.models import User
from graphene import relay, Field
from graphene_django import DjangoObjectType

from main.schema import ImageType
from oauth.models import UserProfile


class UserNode(DjangoObjectType):
    class Meta:
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'userprofile')
        model = User
        interfaces = (relay.Node,)


class UserProfileNode(DjangoObjectType):
    user = UserNode()
    cover = Field(ImageType)
    avatar = Field(ImageType)

    class Meta:
        filter_fields = []
        model = UserProfile
        interfaces = (relay.Node,)

    def resolve_cover(self, info):
        from gymkhana.utils import build_image_types
        return ImageType(sizes=build_image_types(info.context, self.cover, 'festival'))

    def resolve_avatar(self, info):
        from gymkhana.utils import build_image_types
        return ImageType(sizes=build_image_types(info.context, self.avatar, 'festival'))

    @classmethod
    def search(cls, query, info):
        return cls._meta.model.objects.search(query)
