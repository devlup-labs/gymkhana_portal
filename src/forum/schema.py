import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql_jwt.decorators import login_required

from forum.forms import TopicForm, AnswerForm
from forum.models import Topic, Answer


class AnswerNode(DjangoObjectType):
    upvotes_count = graphene.Int()
    is_upvoted = graphene.Boolean()
    is_author = graphene.Boolean()

    class Meta:
        model = Answer
        fields = '__all__'
        filter_fields = ()
        interfaces = (relay.Node,)

    def resolve_upvotes_count(self, info):
        return self.upvotes.count()

    def resolve_is_upvoted(self, info):
        if info.context.user.userprofile in self.upvotes.all():
            return True
        return False

    def resolve_is_author(self, info):
        return info.context.user.userprofile == self.author


class TopicNode(DjangoObjectType):
    id = graphene.ID(required=True)
    upvotes_count = graphene.Int()
    answers_count = graphene.Int()
    is_upvoted = graphene.Boolean()
    is_author = graphene.Boolean()

    class Meta:
        model = Topic
        fields = '__all__'
        filter_fields = ('slug',)
        interfaces = (relay.Node,)

    @classmethod
    def search(cls, query, indfo):
        print(cls._meta.model.objects.search(query)[0].created_at)
        return cls._meta.model.objects.search(query)

    def resolve_id(self, info):
        return self.id

    def resolve_upvotes_count(self, info):
        return self.upvotes.count()

    def resolve_answers_count(self, info):
        return self.answer_set.count()

    def resolve_is_upvoted(self, info):
        if info.context.user.userprofile in self.upvotes.all():
            return True
        return False

    def resolve_is_author(self, info):
        return info.context.user.userprofile == self.author


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


class UpvoteMutaiton(graphene.Mutation):
    class Arguments:
        is_topic = graphene.Boolean(required=True)
        id = graphene.ID(required=True)

    updated = graphene.Boolean()
    upvoted = graphene.Boolean()

    def mutate(self, info, id, is_topic):
        updated = False
        upvoted = False
        print(Topic.objects.get(id=id).upvotes)
        user = info.context.user.userprofile
        obj = Topic.objects.get(id=id) if is_topic else Answer.objects.get(id=id)
        if info.context.user.is_authenticated:
            if user in obj.upvotes.all():
                obj.upvotes.remove(user)
                upvoted = False
            else:
                obj.upvotes.add(user)
                upvoted = True
            updated = True
        print(Topic.objects.get(id=id).upvotes)
        return UpvoteMutaiton(updated=updated, upvoted=upvoted)
