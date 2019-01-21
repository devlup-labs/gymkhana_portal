from django.views.generic import DetailView
from django.conf import settings
from .models import Festival

custom_template_folder_name = settings.CUSTOM_TEMPLATE_DIR_NAME


class FestivalView(DetailView):
    template_name = 'festivals/index.html'
    model = Festival

    def get_context_data(self, **kwargs):
        context = super(FestivalView, self).get_context_data(**kwargs)
        event_category_list = self.object.eventcategory_set.filter(event__published=True).distinct()
        context['event_category_list'] = event_category_list
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.use_custom_html:
            self.template_name = self.object.custom_html.name.split('/')[-1] \
                if custom_template_folder_name in self.object.custom_html.name else self.object.custom_html.name
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
