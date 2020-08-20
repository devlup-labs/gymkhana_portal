import graphene
from django.contrib.auth.models import User
from graphene import relay, Field
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql_jwt.decorators import login_required
from main.schema import ImageType
from oauth.forms import UserProfileUpdateForm, UserProfileForm
from oauth.models import UserProfile, SocialLink


class SocialLinks(DjangoObjectType):
    class Meta:
        model = SocialLink
        fields = ('__all__')
        interfaces = (relay.Node,)


class UserNode(DjangoObjectType):
    id = graphene.ID(required=True)

    class Meta:
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'userprofile')
        model = User
        interfaces = (relay.Node,)

    def resolve_id(self, info):
        return self.id


class UserProfileNode(DjangoObjectType):
    user = UserNode()
    cover = Field(ImageType)
    avatar = Field(ImageType)
    social_links = DjangoConnectionField(SocialLinks)
    gender = graphene.String()
    prog = graphene.String()
    branch = graphene.String()
    year = graphene.String()
    id = graphene.ID(required=True)

    class Meta:
        filter_fields = ['roll']
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

    def resolve_gender(self, info):
        return self.user.userprofile.get_gender_display()

    def resolve_prog(self, info):
        return self.user.userprofile.get_prog_display()

    def resolve_branch(self, info):
        return self.user.userprofile.get_branch_display()

    def resolve_year(self, info):
        return self.user.userprofile.get_year_display()

    def resolve_id(self, info):
        return self.id

    @classmethod
    def search(cls, query, info):
        nodes = cls._meta.model.objects.search(query) if query else cls._meta.model.objects
        return nodes.all()


class ProfileMutation(DjangoModelFormMutation):
    class Meta:
        form_class = UserProfileUpdateForm

    @classmethod
    @login_required
    def get_form_kwargs(cls, root, info, **input):
        kwargs = {"data": input}
        instance = cls._meta.model._default_manager.get(user=info.context.user)
        kwargs["instance"] = instance
        return kwargs


class CreateProfileMutation(DjangoModelFormMutation):
    class Meta:
        form_class = UserProfileForm

    @classmethod
    @login_required
    def perform_mutate(cls, form, info):
        obj = form.save(commit=False)
        obj.user_id = info.context.user.id
        obj.save()
        kwargs = {cls._meta.return_field_name: obj}
        return cls(errors=[], **kwargs)
