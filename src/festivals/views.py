from django.views.generic import DetailView
from django.shortcuts import render
from django.conf import settings
from .models import Festival
from main.views import MaintenanceAndNavigationMixin


class FestivalView(MaintenanceAndNavigationMixin, DetailView):
    template_name = 'festivals/index.html'
    model = Festival

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_category_list'] = self.object.eventcategory_set.filter(event__published=True).distinct()
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if not self.object.published or not context['event_category_list']:
            self.template_name = 'festivals/coming_soon.html'
        if self.object.use_custom_html and self.object.published:
            self.template_name = self.object.custom_html.name.split('/')[-1] \
                if settings.CUSTOM_TEMPLATE_DIR_NAME in self.object.custom_html.name \
                else self.object.custom_html.name
        return render(request, self.template_name, context=context)
