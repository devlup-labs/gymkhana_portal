from django import forms
from django.contrib import admin

from ckeditor.widgets import CKEditorWidget
from photologue.admin import GalleryAdmin as GalleryAdminDefault
from photologue.models import Gallery


class GalleryAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Gallery
        exclude = ['']


class GalleryAdmin(GalleryAdminDefault):
    form = GalleryAdminForm


admin.site.unregister(Gallery)
admin.site.register(Gallery, GalleryAdmin)
