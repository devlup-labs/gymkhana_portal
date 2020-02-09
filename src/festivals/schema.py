from graphene import relay


from graphene_django import DjangoObjectType
from festivals.models import Festival


class FestivalNode(DjangoObjectType):
    class Meta:
        model = Festival
        fields = '__all__'
        interfaces = (relay.Node,)