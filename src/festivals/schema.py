from graphene import relay, Field
from graphene_django import DjangoObjectType
from festivals.models import Festival
from gymkhana.utils import build_image_types
from main.schema import ImageType


class FestivalNode(DjangoObjectType):
    photo = Field(ImageType)

    class Meta:
        model = Festival
        fields = '__all__'
        interfaces = (relay.Node,)

    def resolve_photo(self, info):
        return ImageType(sizes=build_image_types(info.context, self.photo, 'festival'))
