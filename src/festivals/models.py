from django.db import models
from versatileimagefield.fields import VersatileImageField
from ckeditor_uploader.fields import RichTextUploadingField


class Festival(models.Model):
    name = models.CharField(max_length=32)
    photo = VersatileImageField(upload_to='festival')
    about = models.TextField()
    slug = models.SlugField(unique=True, help_text="This will be used as URL. /festivals/slug")
    link = models.URLField(blank=True, null=True, default=None)
    published = models.BooleanField(default=False)
    default_html = models.BooleanField(default=True, help_text="Unselect if you want custom home page")

    def __str__(self):
        return self.name

    def get_name_display(self):
        return self.name.title()


class EventCategory(models.Model):
    name = models.CharField(max_length=128)
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE)
    cover = VersatileImageField(upload_to='festival_event_category', blank=True)
    slug = models.SlugField(unique=True)
    about = RichTextUploadingField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )
        verbose_name = 'Festival Event Category'
        verbose_name_plural = 'Festival Event Categories'


class Event(models.Model):
    event_category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)
    unique_id = models.CharField(unique=True, max_length=8)
    description = RichTextUploadingField(name='Problem Statement')
    pdf = models.FileField(upload_to='pdf', null=True, blank=True)
    cover = VersatileImageField(upload_to='event', null=True, blank=True)
    location = models.CharField(max_length=64, blank=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    max_team_size = models.PositiveSmallIntegerField(default=1, help_text='Leave 1 for single participant event')
    min_team_size = models.PositiveSmallIntegerField(default=1, help_text='Leave 1 for single participant event')
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ('timestamp', )
        verbose_name = 'Festival Event'
        verbose_name_plural = 'Festival Events'

    def __str__(self):
        return self.name
