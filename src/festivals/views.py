from django.views.generic import DetailView
from django.conf import settings
from .models import Festival
from main.views import MaintenanceAndNavigationMixin
from django.urls import reverse_lazy
from django.shortcuts import Http404

custom_template_folder_name = settings.CUSTOM_TEMPLATE_DIR_NAME


class FestivalView(MaintenanceAndNavigationMixin, DetailView):
    model = Festival

    def get_context_data(self, **kwargs):
        context = super(FestivalView, self).get_context_data(**kwargs)
        event_category_list = self.object.eventcategory_set.filter(event__published=True).distinct()
        context['event_category_list'] = event_category_list
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if self.object.published and context['event_category_list']:
            if self.object.use_custom_html:
                self.template_name = self.object.custom_html.name.split('/')[-1] \
                    if custom_template_folder_name in self.object.custom_html.name else self.object.custom_html.name
            else:
                self.template_name = 'festivals/default.html'
        else:
            if str(reverse_lazy('festivals:festival', kwargs={'slug': self.object.slug})) in self.object.link:
                self.template_name = 'festivals/coming_soon.html'
            else:
                raise Http404
        return self.render_to_response(context)
