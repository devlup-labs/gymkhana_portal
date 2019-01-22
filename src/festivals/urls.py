from django.conf.urls import url
from .views import FestivalView

app_name = 'festivals'

urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', FestivalView.as_view(), name='detail'),
]
