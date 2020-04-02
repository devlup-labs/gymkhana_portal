import graphene
from django.contrib.auth import get_user_model
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
    gender = graphene.String()
    prog = graphene.String()
    branch = graphene.String()
    year = graphene.String()


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

    def resolve_gender(self,info):
        return info.context.user.userprofile.get_gender_display()

    def resolve_prog(self,info):
        return info.context.user.userprofile.get_prog_display()

    def resolve_branch(self,info):
        return info.context.user.userprofile.get_branch_display()

    def resolve_year(self,info):
        return info.context.user.userprofile.get_year_display()

    @classmethod
    def search(cls, query, info):
        return cls._meta.model.objects.search(query)
