from django.views.generic.base import ContextMixin
from .models import Society, Senate


class NavigationMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(NavigationMixin, self).get_context_data(**kwargs)
        societies = Society.objects.filter(is_active=True)
        senate = Senate.objects.filter(is_active=True).order_by('-year').first()
        context['society_link_list'] = societies
        context['senate'] = senate
        return context
