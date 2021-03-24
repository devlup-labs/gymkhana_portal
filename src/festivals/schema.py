from graphene import relay, Field
from graphene_django import DjangoObjectType
from festivals.models import Festival, EventCategory, Event
from gymkhana.utils import build_image_types
from main.schema import ImageType


class FestivalNode(DjangoObjectType):
    photo = Field(ImageType)

    class Meta:
        model = Festival
        fields = '__all__'
        filter_fields = ('slug',)
        interfaces = (relay.Node,)

    def resolve_photo(self, info):
        return ImageType(sizes=build_image_types(info.context, self.photo, 'festival'))


class EventCategoryNode(DjangoObjectType):
    cover = Field(ImageType)

    class Meta:
        model = EventCategory
        fields = '__all__'
        filter_fields = ('slug',)
        interfaces = (relay.Node,)

    def resolve_cover(self, info):
        return ImageType(sizes=build_image_types(info.context, self.cover, 'festival'))


class EventFestivalNode(DjangoObjectType):
    cover = Field(ImageType)

    class Meta:
        model = Event
        fields = '__all__'
        filter_fields = ('slug', 'published', 'unique_id',)
        interfaces = (relay.Node,)

    def resolve_cover(self, info):
        return ImageType(sizes=build_image_types(info.context, self.cover, 'festival'))
