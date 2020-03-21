from graphene import relay, Field

from graphene_django import DjangoObjectType

from gallery.schema import ImageType
from news.models import News


class NewsNode(DjangoObjectType):
    cover = Field(ImageType)

    class Meta:
        model = News
        fields = '__all__'
        interfaces = (relay.Node,)

    def resolve_cover(self, info):
        from gymkhana.utils import build_image_types
        return ImageType(sizes=build_image_types(info.context, self.cover, 'festival'))
