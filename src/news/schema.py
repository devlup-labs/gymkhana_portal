from graphene import relay

from graphene_django import DjangoObjectType

from news.models import News


class NewsNode(DjangoObjectType):
    class Meta:
        model = News
        fields = '__all__'
        interfaces = (relay.Node,)
