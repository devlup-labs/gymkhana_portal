from django.conf.urls import url
from .views import HomeView, SearchView

app_name = 'konnekt'

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='index'),
    url(r'^search/$', SearchView.as_view(), name='search'),
]
