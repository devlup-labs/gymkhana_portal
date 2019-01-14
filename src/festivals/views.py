from django.views.generic import TemplateView
from .models import EventCategory


class NimbleView(TemplateView):
    template_name = 'festivals/nimble/index.html'
    model = EventCategory

    def get_context_data(self, **kwargs):
        context = super(NimbleView, self).get_context_data(**kwargs)
        event_category_list = EventCategory.objects.filter(festival__name='NMBL', event__published=True).distinct()
        context['event_category_list'] = event_category_list
        return context
