from django.db import models
from oauth.models import UserProfile
from main.models import Club
from ckeditor_uploader.fields import RichTextUploadingField
from versatileimagefield.fields import VersatileImageField


class News(models.Model):
    title = models.CharField(max_length=128)
    cover = VersatileImageField(upload_to='news_%Y', blank=True, null=True,
                                help_text="Upload high quality image to use as cover photo.")
    author = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)
    content = RichTextUploadingField()
    club = models.ForeignKey(Club, blank=True, null=True, on_delete=models.CASCADE, default=None,
                             help_text="Leave blank to make this a general news.")
    date = models.DateField(editable=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'news'

    def __str__(self):
        return self.title


class Update(models.Model):
    title = models.CharField(max_length=128)
    content = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
