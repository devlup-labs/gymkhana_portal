from django.core.validators import RegexValidator
from django.db import models
from versatileimagefield.fields import VersatileImageField
from ckeditor_uploader.fields import RichTextUploadingField
from main.models import Society


class Festival(models.Model):
    name = models.CharField(max_length=32)
    tag_line = models.CharField(max_length=128, blank=True, null=True)
    photo = VersatileImageField(upload_to='festival')
    about = RichTextUploadingField(blank=True, null=True)
    slug = models.SlugField(unique=True, help_text="This will be used as URL. /festivals/slug")
    society = models.ManyToManyField(Society, blank=True)
    link = models.URLField(blank=True, null=True, default=None)
    published = models.BooleanField(default=False)
    use_custom_html = models.BooleanField(default=False, help_text="Select if you want custom page")
    custom_html = models.FileField(upload_to='html', verbose_name='Custom HTML', blank=True, null=True)
    custom_css = models.FileField(upload_to='css', verbose_name='Custom CSS', blank=True, null=True)
    custom_js = models.FileField(upload_to='js', verbose_name='Custom JS', blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def assets_present(self):
        return self.custom_html is not None and self.custom_css is not None and self.custom_js is not None

    def clean(self):
        if self.use_custom_html and not self.assets_present:
            pass

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
    # Validators
    contact = RegexValidator(r'^[0-9]{10}$', message='Not a valid number!')

    event_category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)
    unique_id = models.CharField(unique=True, max_length=8)
    about = RichTextUploadingField(verbose_name='About', blank=True)
    pdf = models.FileField(upload_to='pdf', null=True, blank=True)
    cover = VersatileImageField(upload_to='event', null=True, blank=True)
    location = models.CharField(max_length=64, blank=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    register = models.URLField(blank=True, help_text="Registration URL")
    phone = models.CharField(max_length=10, blank=True, verbose_name="Organizer's Contact", validators=[contact])
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
        ('YT', 'YouTube'),
    )
    FA_CHOICES = (
        ('fa fa-facebook', 'FB'),
        ('fa fa-twitter', 'TW'),
        ('fa fa-linkedin', 'LI'),
        ('fa fa-google-plus', 'GP'),
        ('fa fa-instagram', 'IG'),
        ('fa fa-youtube-play', 'YT'),
    )
    IC_CHOICES = (
        ('fb-ic', 'FB'),
        ('tw-ic', 'TW'),
        ('li-ic', 'LI'),
        ('gplus-ic', 'GP'),
        ('ins-ic', 'IG'),
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
