from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from .utils import unique_slug_generator
from oauth.models import UserProfile
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from hitcount.models import HitCountMixin


class TopicQueryset(models.query.QuerySet):
    def search(self, query):
        if query:
            return self.filter(
                Q(author__user__first_name__icontains=query) |
                Q(author__user__last_name__icontains=query) |
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__icontains=query) |
                Q(answer__content__icontains=query)
            ).distinct()
        else:
            return self.none()


class TopicManager(models.Manager):
    def get_topic_queryset(self):
        return TopicQueryset(self.model, using=self._db)

    def search(self, query):
        return self.get_topic_queryset().search(query)


class Topic(models.Model, HitCountMixin):
    # Choices
    CAT_CHOICES = (
        ('Q', 'Question'),
        ('F', 'Feedback'),
        ('S', 'Suggestion'),
        ('I', 'Improvement'),
    )
    # Topic Database Model
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="author of topic")
    category = models.CharField(max_length=3, choices=CAT_CHOICES, default='Q')
    title = models.CharField(max_length=256)
    content = RichTextUploadingField()
    tags = models.CharField(max_length=50, blank=True, null=True, default=None)
    upvotes = models.ManyToManyField(UserProfile, blank=True, related_name='topic_upvotes')
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    objects = TopicManager()

    @property
    def number_of_answers(self):
        return self.answer_set.count()

    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse('forum:detail', kwargs={'slug': self.slug})

    def get_api_upvote_toggle_url(self):
        return reverse('forum_api:topic-upvote-toggle', kwargs={'slug': self.slug})

    def get_edit_url(self):
        return reverse('forum:update_topic', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('forum:delete_topic', kwargs={'slug': self.slug})

    def tags_as_list(self):
        if self.tags == '' or not self.tags:
            return ''
        return sorted(self.tags.split(','))

    def __str__(self):
        return self.title


def topic_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(topic_pre_save_receiver, sender=Topic)


class Answer(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name="topic of answer")
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="author of answer")
    content = RichTextUploadingField(blank=True)
    upvotes = models.ManyToManyField(UserProfile, blank=True, related_name='answer_upvotes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def get_api_upvote_toggle_url(self):
        return reverse('forum_api:answer-upvote-toggle', kwargs={'id': self.id})

    def get_absolute_url(self):
        return self.topic.get_absolute_url()

    def get_delete_url(self):
        return reverse('forum:delete_answer', kwargs={'pk': self.pk})

    def __str__(self):
        return "On: " + str(self.topic.title) + " by " + str(self.author.user.first_name) + " " + str(
            self.author.user.last_name)
