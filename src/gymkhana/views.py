from os import listdir
from shutil import rmtree, move
from tarfile import open as tar_open
from os.path import join
from django.conf import settings
from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django import forms
from django.core.management import call_command
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView


class UploadForm(forms.Form):
    file = forms.FileField()

    def process(self):
        # Delete directory if present, then extract new archive
        rmtree(join(settings.VUE_ROOT, 'dist'), ignore_errors=True)
        with tar_open(fileobj=self.cleaned_data['file'].file, mode='r:gz') as archive:
            archive.extractall(settings.VUE_ROOT)
            # Extract index.html to templates dir
            archive.extract(archive.getmember('dist/index.html'), settings.TEMPLATES[0]['DIRS'][0])
            archive.close()
        move(join(settings.VUE_ROOT, 'dist/static/js'), join(settings.VUE_ROOT, 'dist/js'))
        move(join(settings.VUE_ROOT, 'dist/static/css'), join(settings.VUE_ROOT, 'dist/css'))
        move(join(settings.VUE_ROOT, 'dist/static/fonts'), join(settings.VUE_ROOT, 'dist/fonts'))
        for i in listdir(join(settings.VUE_ROOT, 'dist/static/img')):
            move(join(settings.VUE_ROOT, f'dist/static/img/{i}'), join(settings.VUE_ROOT, f'dist/img/{i}'))
        call_command('collectstatic', verbosity=0, interactive=False)

    def clean_file(self):
        if not self.cleaned_data['file'].content_type == 'application/gzip':
            raise ValidationError("Not a valid file")
        return self.cleaned_data['file']


class FrontendUpdateView(FormView):
    form_class = UploadForm
    template_name = 'frontend_update.html'
    success_url = reverse_lazy('admin:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Frontend Upload',
            'site_title': admin.site.site_title,
            'site_header': admin.site.site_header,
            'site_url': admin.site.site_url,
            'has_permission': admin.site.has_permission(self.request),
            'is_popup': False,
        })
        return context

    def form_valid(self, form):
        form.process()
        messages.add_message(self.request, messages.INFO, 'The frontend code deployment has started')
        return super().form_valid(form)


class VueView(TemplateView):
    template_name = 'dist/index.html'
