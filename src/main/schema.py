from django.db.models import FileField
from graphene import relay, ObjectType, String, List, Field
from photologue.models import Gallery, Photo

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


class GalleryNode(DjangoObjectType):
    class Meta:
        model = Gallery
        fields = '__all__'
        filter_fields = ('slug',)
        interfaces = (relay.Node,)


class GalleryPhoto(DjangoObjectType):
    image = Field(ImageType)

    class Meta:
        model = Photo
        fields = '__all__'
        interfaces = (relay.Node,)

    def resolve_image(self, info):
        from gymkhana.utils import build_image_types
        return ImageType(sizes=build_image_types(request=info.context, image=self.image, key_set='image'))
