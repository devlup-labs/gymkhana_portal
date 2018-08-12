from django.conf.urls import url
from .views import (ProfileDetailView, ProfileEditView, SocialLinkCreateView, SocialLinkUpdateView,
                    SocialLinkDeleteView, RegisterView, AccountActivationView, get_activation_link)

app_name = 'oauth'

urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^(?P<roll>[\w]+)/get/$', get_activation_link, name='get-act-link'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        AccountActivationView.as_view(), name='activate'),
    url(r'^sociallink/add/$', SocialLinkCreateView.as_view(), name='link-add'),
    url(r'^(?P<roll>[\w]+)/$', ProfileDetailView.as_view(), name='detail'),
    url(r'^(?P<roll>[\w]+)/edit/$', ProfileEditView.as_view(), name='edit'),
    url(r'sociallink/(?P<username>[\w.-]+)-(?P<social_media>[\w]{2})/$', SocialLinkUpdateView.as_view(),
        name='link-edit'),
    url(r'sociallink/(?P<username>[\w.-]+)-(?P<social_media>[\w]{2})/delete/$', SocialLinkDeleteView.as_view(),
        name='link-delete'),
]
