from django.db import models
from django.db.models import Q
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from .tokens import account_activation_token
from versatileimagefield.fields import VersatileImageField
from django.db.models.signals import pre_save


class KonnektQueryset(models.query.QuerySet):
    def search(self, query):
        if query:
            result = self.filter(user__isnull=True)
            for term in query.split():
                if len(term) > 3:
                    result = self.filter(Q(skills__icontains=term) |
                                         Q(user__first_name__icontains=term) |
                                         Q(user__last_name__icontains=term)) | result
                else:
                    result = self.filter(Q(skills__icontains=term)) | result
            return result.distinct().order_by('user__first_name')
        else:
            return self.none()


class UserProfileManager(models.Manager):
    uidb64 = None

    def get_konnekt_queryset(self):
        return KonnektQueryset(self.model, using=self._db)

    def search(self, query):
        return self.get_konnekt_queryset().search(query)

    def _get_user_for_activation(self):
        try:
            uid = force_text(urlsafe_base64_decode(self.uidb64))
            return User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None

    def activation_link_valid(self, token=None):
        return account_activation_token.check_token(self._get_user_for_activation(), token)

    def activate_account(self, uidb64=None, token=None):
        self.uidb64 = uidb64
        if self.activation_link_valid(token) and not self._get_user_for_activation().userprofile.email_confirmed:
            user = self._get_user_for_activation()
            user.is_active = True
            user.save()
            user.userprofile.email_confirmed = True
            user.userprofile.save()
        else:
            user = None
        return user


class UserProfile(models.Model):
    # Validators
    valid_year = RegexValidator(r'^[0-9]{4}$', message='Not a valid year!')
    contact = RegexValidator(r'^[0-9]{10}$', message='Not a valid number!')
    # Choices
    PROG_CHOICES = (
        ('BT', 'B.Tech'),
        ('MT', 'M.Tech'),
        ('MSc', 'M.Sc'),
        ('PhD', 'PhD')
    )
    YEAR_CHOICES = (
        # ('0', 'Alumni'),
        ('1', 'First Year'),
        ('2', 'Second Year'),
        ('3', 'Third Year'),
        ('4', 'Fourth Year'),
        ('5', 'Fifth Year')
    )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Transgender')
    )
    BRANCH_CHOICES = (
        ('CSE', 'Computer Science and Engineering'),
        ('EE', 'Electrical Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('CH', 'Chemistry'),
        ('MA', 'Mathematics'),
        ('PHY', 'Physics'),
        ('MME', 'Metallurgical and Materials Engineering'),
        ('HSS', 'Humanities and Social Sciences'),
        ('BBE', 'Biosciences and Bioengineering'),
        ('BISS', 'BISS'),
        ('SS', 'SS')
    )
    # Database Model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    roll = models.CharField(max_length=15, unique=True)
    dob = models.DateField()
    prog = models.CharField(max_length=5, choices=PROG_CHOICES, verbose_name='programme', default='BT')
    year = models.CharField(max_length=1, choices=YEAR_CHOICES, default='1')
    phone = models.CharField(max_length=10, validators=[contact])
    avatar = VersatileImageField(upload_to='avatar', blank=True, null=True)
    cover = VersatileImageField(upload_to='cover', blank=True, null=True)
    hometown = models.CharField(max_length=128, blank=True, null=True)
    branch = models.CharField(max_length=5, choices=BRANCH_CHOICES)
    skills = models.TextField(help_text="Enter your skills, separated by comma.", max_length=1024, blank=True,
                              null=True, default=None)
    about = models.TextField(max_length=160, verbose_name='about you', blank=True, null=True)

    class Meta:
        ordering = ["roll"]

    def get_absolute_url(self):
        return reverse('oauth:detail', kwargs={'roll': self.roll})

    objects = UserProfileManager()

    def __str__(self):
        return self.roll + " (" + self.user.get_full_name() + ")"

    @property
    def get_activation_url(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = account_activation_token.make_token(self.user)
        return reverse('oauth:activate', kwargs={'uidb64': uidb64, 'token': token})

    @property
    def skills_as_list(self):
        if self.skills == '' or not self.skills:
            return ''
        return sorted(self.skills.split(','))


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    social_media = models.CharField(max_length=2, choices=SM_CHOICES)
    link = models.URLField()

    class Meta:
        ordering = ['social_media']

    def get_absolute_url(self):
        return self.user.userprofile.get_absolute_url()

    def __str__(self):
        return self.user.get_full_name() + ' - ' + self.get_social_media_display()

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


def topic_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance._state.adding is True:
        name = instance.first_name.split(' ')
        instance.first_name = name[0].title()
        instance.last_name = ' '.join([x.title() for x in name[1:len(name)]])


pre_save.connect(topic_pre_save_receiver, sender=User)
