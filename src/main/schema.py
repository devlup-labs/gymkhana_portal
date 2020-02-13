from graphene import relay

from main.models import Society, Club, Activity
from graphene_django import DjangoObjectType


class SocietyNode(DjangoObjectType):
    class Meta:
        model = Society
        fields = ('name', 'slug', 'secretary', 'joint_secretary', 'description', 'mentor', 'club_set',)
        filter_fields = ('slug',)
        interfaces = (relay.Node,)


class ClubNode(DjangoObjectType):
    class Meta:
        model = Club
        fields = '__all__'
        filter_fields = ('slug',)
        interfaces = (relay.Node,)


class ActivityNode(DjangoObjectType):
    class Meta:
        model = Activity
        fields = '__all__'
        interfaces = (relay.Node,)
