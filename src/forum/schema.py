import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql_jwt.decorators import login_required

from forum.forms import TopicForm, AnswerForm
from forum.models import Topic, Answer


class AnswerNode(DjangoObjectType):
    class Meta:
        model = Answer
        fields = '__all__'
        filter_fields = ()
        interfaces = (relay.Node,)


class TopicNode(DjangoObjectType):
    id = graphene.ID(required=True)

    class Meta:
        model = Topic
        fields = '__all__'
        filter_fields = ()
        interfaces = (relay.Node,)

    @classmethod
    def search(cls, query, indfo):
        return cls._meta.model.objects.search(query)

    def resolve_id(self, info):
        return self.id


class CreateTopicMutation(DjangoModelFormMutation):
    class Meta:
        form_class = TopicForm

    @classmethod
    @login_required
    def perform_mutate(cls, form, info):
        obj = form.save(commit=False)
        obj.author = info.context.user.userprofile
        obj.save()
        kwargs = {cls._meta.return_field_name: obj}
        return cls(errors=[], **kwargs)


class AddAnswerMutation(DjangoModelFormMutation):
    class Meta:
        form_class = AnswerForm
