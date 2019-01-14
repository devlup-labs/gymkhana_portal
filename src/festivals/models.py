from django.db import models
from versatileimagefield.fields import VersatileImageField
from ckeditor_uploader.fields import RichTextUploadingField


class Festival(models.Model):
    FEST_CHOICES = (
        ('IGNS', 'Ignus'),
        ('VRCHS', 'Varchas'),
        ('SPNDN', 'Spandan'),
        ('NMBL', 'Nimble'),
    )
    name = models.CharField(max_length=5, choices=FEST_CHOICES)
    photo = VersatileImageField(upload_to='festival')
    about = models.TextField(max_length=2048)
    link = models.URLField(blank=True, null=True, default=None)

    def __str__(self):
        return self.get_name_display()


class EventCategory(models.Model):
    name = models.CharField(max_length=128)
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE)
    cover = VersatileImageField(upload_to='festival_event_category', blank=True)
    slug = models.SlugField()
    about = RichTextUploadingField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'event categories'


class Event(models.Model):
    event_category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    # limit_choices_to={"event_category__festival": festival.name}, name='Event Category')
    name = models.CharField(max_length=64)
    slug = models.SlugField()
    unique_id = models.CharField(max_length=8)
    description = models.TextField(name='Problem Statement')
    pdf = models.FileField(upload_to='pdf', null=True, blank=True)
    cover = VersatileImageField(upload_to='event', null=True, blank=True)
    location = models.CharField(max_length=64, blank=True)
    date = models.DateTimeField(blank=True, null=True)
    max_team_size = models.PositiveSmallIntegerField(default=1, help_text='Leave 1 for single participant event')
    min_team_size = models.PositiveSmallIntegerField(default=1, help_text='Leave 1 for single participant event')
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.name
