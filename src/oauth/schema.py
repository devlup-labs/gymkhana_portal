from django.contrib.auth.models import User
from graphene import relay, Field
from graphene_django import DjangoObjectType, DjangoConnectionField
from main.schema import ImageType
from oauth.models import UserProfile, SocialLink


class SocialLinks(DjangoObjectType):
    class Meta:
        model = SocialLink
        fields = ('__all__')
        interfaces = (relay.Node,)


class UserNode(DjangoObjectType):
    class Meta:
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'userprofile')
        model = User
        interfaces = (relay.Node,)


class UserProfileNode(DjangoObjectType):
    user = UserNode()
    cover = Field(ImageType)
    avatar = Field(ImageType)
    social_links = DjangoConnectionField(SocialLinks)

    class Meta:
        filter_fields = []
        model = UserProfile
        fields = (
            'id', 'user', 'email_confirmed', 'gender', 'roll', 'dob', 'prog', 'year', 'phone', 'hometown', 'branch',
            'skills',
            'about')
        interfaces = (relay.Node,)

    def resolve_cover(self, info):
        from gymkhana.utils import build_image_types
        return ImageType(sizes=build_image_types(info.context, self.cover, 'festival'))

    def resolve_avatar(self, info):
        from gymkhana.utils import build_image_types
        return ImageType(sizes=build_image_types(info.context, self.avatar, 'festival'))

    def resolve_social_links(self, info):
        return SocialLink.objects.filter(user=self.user)

    @classmethod
    def search(cls, query, info):
        return cls._meta.model.objects.search(query)
