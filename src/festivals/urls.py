from django.conf.urls import url
from .views import NimbleView

app_name = 'festivals'

urlpatterns = [
    url(r'^nimble$', NimbleView.as_view(), name='nimble'),
]
