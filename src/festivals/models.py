from django.db import models
from versatileimagefield.fields import VersatileImageField
from ckeditor_uploader.fields import RichTextUploadingField


class Festival(models.Model):
    name = models.CharField(max_length=32)
    tag_line = models.CharField(max_length=128, blank=True, null=True)
    photo = VersatileImageField(upload_to='festival')
    about = RichTextUploadingField(blank=True, null=True)
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


class SocialLink(models.Model):
    SM_CHOICES = (
        ('FB', 'Facebook'),
        ('TW', 'Twitter'),
        ('LI', 'LinkedIn'),
        ('GP', 'Google Plus'),
        ('IG', 'Instagram'),
        ('GH', 'GitHub'),
        ('YT', 'YouTube'),
    )
    FA_CHOICES = (
        ('fa fa-facebook', 'FB'),
        ('fa fa-twitter', 'TW'),
        ('fa fa-linkedin', 'LI'),
        ('fa fa-google-plus', 'GP'),
        ('fa fa-instagram', 'IG'),
        ('fa fa-github', 'GH'),
        ('fa fa-youtube', 'YT'),
    )
    IC_CHOICES = (
        ('fb-ic', 'FB'),
        ('tw-ic', 'TW'),
        ('li-ic', 'LI'),
        ('gplus-ic', 'GP'),
        ('ins-ic', 'IG'),
        ('git-ic', 'GH'),
        ('yt-ic', 'YT'),
    )
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE)
    social_media = models.CharField(max_length=2, choices=SM_CHOICES)
    link = models.URLField()

    class Meta:
        ordering = ['social_media']

    def __str__(self):
        return self.festival.name + ' - ' + self.get_social_media_display()

    def get_fai(self):
        for key, value in self.FA_CHOICES:
            if value == self.social_media:
                return key
        return 'fa fa-link'

    def get_sm_ic(self):
        for key, value in self.IC_CHOICES:
            if value == self.social_media:
                return key
        return ''
