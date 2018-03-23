from oauth.models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'konnekt/index.html'


class SearchView(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = 'konnekt/search.html'

    def get_queryset(self):
        if self.request.GET.get('q'):
            query = self.request.GET.get('q')
            return UserProfile.objects.search(query)
        else:
            return UserProfile.objects.none()
