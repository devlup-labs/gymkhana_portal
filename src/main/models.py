import datetime
from django.db import models
from django.core.validators import RegexValidator
from oauth.models import UserProfile
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from versatileimagefield.fields import VersatileImageField
from photologue.models import Gallery

YEAR_CHOICES = []
for r in range(2008, (datetime.datetime.now().year + 2)):
    YEAR_CHOICES.append((str(r), r))

SKIN_CHOICES = (
    ('white-skin', 'White'),
    ('black-skin', 'Black'),
    ('cyan-skin', 'Cyan'),
    ('mdb-skin', 'MDB'),
    ('deep-purple-skin', 'Deep Purple'),
    ('navy-blue-skin', 'Navy Blue'),
    ('pink-skin', 'Pink'),
    ('indigo-skin', 'Indigo'),
    ('light-blue-skin', 'Light Blue'),
    ('grey-skin', 'Grey'),
)


class FacultyAdvisor(models.Model):
    name = models.CharField(max_length=128)
    avatar = VersatileImageField(upload_to='avatar')

    def __str__(self):
        return self.name


class Society(models.Model):
    # Validators
    valid_year = RegexValidator(r'^[0-9]{4}$', message='Not a valid year!')
    # Model
    name = models.CharField(max_length=128)
    description = RichTextUploadingField(blank=True)
    cover = VersatileImageField('Cover', upload_to='society_%Y', help_text="Upload high quality picture")
    skin = models.CharField(max_length=32, choices=SKIN_CHOICES, blank=True, default='mdb-skin',
                            help_text="Choose a skin while displaying society page.")
    secretary = models.ForeignKey(UserProfile, related_name='secy', limit_choices_to={'user__is_staff': True},
                                  null=True, blank=True, on_delete=models.SET_NULL)
    joint_secretary = models.ForeignKey(UserProfile, related_name='joint_secy',
                                        limit_choices_to={'user__is_staff': True}, null=True, blank=True,
                                        on_delete=models.SET_NULL)
    mentor = models.ForeignKey(UserProfile, related_name='smentor', limit_choices_to={'user__is_staff': True},
                               null=True, blank=True, on_delete=models.SET_NULL, default=None)
    faculty_advisor = models.ForeignKey(FacultyAdvisor, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    report_link = models.URLField(help_text='Add a drive link to show on society page', null=True, blank=True)
    gallery = models.ForeignKey(Gallery, blank=True, null=True, on_delete=models.SET_NULL,
                                help_text="Select a carousel gallery to link to this society.")
    custom_html = models.TextField(blank=True, null=True, default=None,
                                   help_text="Add custom HTML to view on society page.")
    slug = models.SlugField(unique=True, help_text="This will be used as URL. /society/slug")
    is_active = models.BooleanField(default=False)
    year = models.CharField(max_length=4, choices=YEAR_CHOICES, validators=[valid_year])

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Societies"

    def get_absolute_url(self):
        return reverse('main:soc-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name + " - " + str(self.year)


class Club(models.Model):
    # Choices
    TYPE_CHOICES = (
        ('C', 'Club'),
        ('T', 'Team'),
    )
    # Model
    name = models.CharField(max_length=128)
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    ctype = models.CharField(max_length=1, choices=TYPE_CHOICES, default='C', help_text="Specify type as Club or Team.",
                             verbose_name="Type")
    description = RichTextUploadingField(blank=True)
    cover = VersatileImageField(upload_to='club_%Y', blank=True, null=True,
                                help_text="Upload high quality picture")
    skin = models.CharField(max_length=32, choices=SKIN_CHOICES, blank=True, default='mdb-skin',
                            help_text="Choose a skin while displaying club page.")
    captain = models.ForeignKey(UserProfile, related_name='captain', limit_choices_to={'user__is_staff': True},
                                null=True, blank=True, on_delete=models.SET_NULL)
    vice_captain_one = models.ForeignKey(UserProfile, related_name='vice_cap_one',
                                         limit_choices_to={'user__is_staff': True},
                                         blank=True, null=True, default=None, on_delete=models.SET_NULL)
    vice_captain_two = models.ForeignKey(UserProfile, related_name='vice_cap_two',
                                         limit_choices_to={'user__is_staff': True},
                                         blank=True, null=True, default=None, on_delete=models.SET_NULL)
    vice_captain_three = models.ForeignKey(UserProfile, related_name='vice_cap_three',
                                           limit_choices_to={'user__is_staff': True},
                                           blank=True, null=True, default=None, on_delete=models.SET_NULL)
    mentor = models.ForeignKey(UserProfile, related_name='cmentor', blank=True, null=True, default=None,
                               on_delete=models.SET_NULL)
    core_members = models.ManyToManyField(UserProfile, blank=True)
    gallery = models.ForeignKey(Gallery, blank=True, null=True, on_delete=models.SET_NULL,
                                help_text="Select a gallery to link to this club.")
    resources_link = models.URLField(blank=True, null=True, default=None)
    custom_html = models.TextField(blank=True, null=True, default=None,
                                   help_text="Add custom HTML to view on club page.")
    slug = models.SlugField(unique=True, help_text="This will be used as URL. /club/slug")
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    @property
    def year(self):
        return self.society.year

    @property
    def is_active(self):
        return self.society.is_active

    def get_absolute_url(self):
        return reverse('main:club-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name + " - " + str(self.year)


class Activity(models.Model):
    name = models.CharField(max_length=64)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    description = RichTextUploadingField()
    custom_html = models.TextField(blank=True, null=True, default=None)

    class Meta:
        verbose_name_plural = 'Activities'

    def get_absolute_url(self):  # pragma: no use
        return reverse('main:activity-gallery', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name + ' - ' + self.club.name


class Senate(models.Model):
    # Validators
    valid_year = RegexValidator(r'^[0-9]{4}$', message='Not a valid year!')
    # Model
    name = models.CharField(max_length=128)
    description = RichTextUploadingField(blank=True)
    cover = VersatileImageField('Cover', upload_to='society_%Y', help_text="Upload high quality picture")
    skin = models.CharField(max_length=32, choices=SKIN_CHOICES, blank=True, default='mdb-skin',
                            help_text="Choose a skin while displaying senate page.")
    members = models.ManyToManyField(UserProfile, through='SenateMembership', through_fields=('senate', 'userprofile'))
    coordinator_student = models.ForeignKey(FacultyAdvisor, blank=True, null=True, default=None,
                                            on_delete=models.SET_NULL)
    report_link = models.URLField(help_text='Add a drive link to show on senate page', null=True, blank=True)
    custom_html = models.TextField(blank=True, null=True, default=None,
                                   help_text="Add custom HTML to view on society page.")
    slug = models.SlugField(unique=True, help_text="This will be used as URL. /senate/slug")
    is_active = models.BooleanField(default=False)
    year = models.CharField(max_length=4, choices=YEAR_CHOICES, validators=[valid_year])

    class Meta:
        ordering = ["-id"]

    def get_absolute_url(self):
        return reverse('main:senate-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name + ' - ' + self.year


class SenateMembership(models.Model):
    ROLE_CHOICES = (
        ('SECY', 'Student Secretary'),
        ('SER', 'Student Elected Representative'),
    )
    P_YEAR_CHOICES = (
        ('1', 'First Year'),
        ('2', 'Second Year'),
        ('3', 'Third Year'),
        ('4', 'Fourth Year'),
    )
    senate = models.ForeignKey(Senate, on_delete=models.CASCADE)
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    role = models.CharField(max_length=5, choices=ROLE_CHOICES)
    year = models.CharField(max_length=1, choices=P_YEAR_CHOICES)

    def __str__(self):
        return self.userprofile.user.get_full_name()


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
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    social_media = models.CharField(max_length=2, choices=SM_CHOICES)
    link = models.URLField()

    class Meta:
        ordering = ['social_media']

    def __str__(self):
        return self.club.name + ' - ' + self.get_social_media_display()

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


class Contact(models.Model):
    # Validators
    contact = RegexValidator(r'^[0-9]{10}$', message='Not a valid number!')
    # Database_model
    name = models.CharField(max_length=64)
    email = models.EmailField()
    phone = models.CharField(max_length=10, validators=[contact])
    subject = models.CharField(max_length=128)
    message = models.TextField(max_length=2048)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.name + ' - ' + self.phone

    @classmethod
    def get_absolute_url(cls):
        return reverse('main:contact')
