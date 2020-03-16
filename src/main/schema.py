from graphene import relay, ObjectType, String, List, Field

from main.models import Society, Club, Activity
from graphene_django import DjangoObjectType


class RenditionType(ObjectType):
    name = String()
    url = String()


class ImageType(ObjectType):
    sizes = List(RenditionType)


class SocietyNode(DjangoObjectType):
    cover = Field(ImageType)

    class Meta:
        model = Society
        fields = ('name', 'slug', 'secretary', 'joint_secretary', 'description', 'mentor', 'club_set', 'cover')
        filter_fields = ('slug',)
        interfaces = (relay.Node,)

    def resolve_cover(self, info):
        from gymkhana.utils import build_image_types
        return ImageType(sizes=build_image_types(info.context, self.cover, 'festival'))


class ClubNode(DjangoObjectType):
    cover = Field(ImageType)

    class Meta:
        model = Club
        fields = '__all__'
        filter_fields = ('slug',)
        interfaces = (relay.Node,)

    def resolve_cover(self, info):
        from gymkhana.utils import build_image_types
        return ImageType(sizes=build_image_types(info.context, self.cover, 'festival'))


class ActivityNode(DjangoObjectType):
    class Meta:
        model = Activity
        fields = '__all__'
        interfaces = (relay.Node,)
