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
    about = models.TextField()
    link = models.URLField(blank=True, null=True, default=None)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.get_name_display()


class FestivalEventCategory(models.Model):
    name = models.CharField(max_length=128)
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE)
    cover = VersatileImageField(upload_to='festival_event_category', blank=True)
    slug = models.SlugField()
    about = RichTextUploadingField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Festival Event Category'
        verbose_name_plural = 'Festival Event Categories'


class FestivalEvent(models.Model):
    event_category = models.ForeignKey(FestivalEventCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    slug = models.SlugField()
    unique_id = models.CharField(max_length=8)
    description = RichTextUploadingField(name='Problem Statement')
    pdf = models.FileField(upload_to='pdf', null=True, blank=True)
    cover = VersatileImageField(upload_to='event', null=True, blank=True)
    location = models.CharField(max_length=64, blank=True)
    date = models.DateTimeField(blank=True, null=True)
    max_team_size = models.PositiveSmallIntegerField(default=1, help_text='Leave 1 for single participant event')
    min_team_size = models.PositiveSmallIntegerField(default=1, help_text='Leave 1 for single participant event')
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ['date']
        verbose_name = 'Festival Event'
        verbose_name_plural = 'Festival Events'

    def __str__(self):
        return self.name
