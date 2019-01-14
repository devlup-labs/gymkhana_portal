from django.views.generic import TemplateView
from .models import FestivalEventCategory


class NimbleView(TemplateView):
    template_name = 'festivals/nimble/index.html'
    model = FestivalEventCategory

    def get_context_data(self, **kwargs):
        context = super(NimbleView, self).get_context_data(**kwargs)
        event_category_list = FestivalEventCategory.objects.filter(festival__name='NMBL',
                                                                   festivalevent__published=True).distinct()
        print(event_category_list)
        context['event_category_list'] = event_category_list
        return context
