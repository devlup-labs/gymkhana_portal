from django.views.generic import DetailView
from .models import Festival


class FestivalView(DetailView):
    template_name = 'festivals/index.html'
    model = Festival

    def get_context_data(self, **kwargs):
        context = super(FestivalView, self).get_context_data(**kwargs)
        event_category_list = self.object.eventcategory_set.all().filter(event__published=True).distinct()
        context['festival'] = self.object
        context['event_category_list'] = event_category_list
        return context
