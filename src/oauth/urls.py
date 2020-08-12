from django.conf.urls import url
from django.urls import reverse_lazy
from django.contrib.auth.views import (PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
                                       PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView)
from .views import (ProfileDetailView, ProfileEditView, SocialLinkCreateView, SocialLinkUpdateView,
                    SocialLinkDeleteView, RegisterView, AccountActivationView, get_activation_link, SessionView)

app_name = 'oauth'

urlpatterns = [
    url(r'^session/$', SessionView.as_view(), name='session'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^(?P<roll>[\w]+)/get/$', get_activation_link, name='get-act-link'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\']+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        AccountActivationView.as_view(), name='activate'),
    url(r'^sociallink/add/$', SocialLinkCreateView.as_view(), name='link-add'),
    url(r'^(?P<roll>[\w]+)/$', ProfileDetailView.as_view(), name='detail'),
    url(r'^(?P<roll>[\w]+)/edit/$', ProfileEditView.as_view(), name='edit'),
    url(r'sociallink/(?P<username>[\w.-]+)-(?P<social_media>[\w]{2})/$', SocialLinkUpdateView.as_view(),
        name='link-edit'),
    url(r'sociallink/(?P<username>[\w.-]+)-(?P<social_media>[\w]{2})/delete/$', SocialLinkDeleteView.as_view(),
        name='link-delete'),
]

urlpatterns += [
    url(r'^password-reset/$', PasswordResetView.as_view(
        template_name='oauth/password_reset_form.html',
        email_template_name='oauth/mixins/password_reset_email.html',
        subject_template_name='oauth/mixins/password_reset_subject.txt',
        success_url=reverse_lazy('oauth:password_reset_done')
    ), name='password_reset'),
    url(r'^reset/done/$', PasswordResetDoneView.as_view(template_name='oauth/password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(
            template_name='oauth/password_reset_confirm.html',
            success_url=reverse_lazy('oauth:password_reset_complete')), name='password_reset_confirm'),
    url(r'^reset/complete/$', PasswordResetCompleteView.as_view(template_name='oauth/password_reset_complete.html'),
        name='password_reset_complete'),
    url(r'^password-change/$', PasswordChangeView.as_view(
        template_name='oauth/password_change_form.html',
        success_url=reverse_lazy('oauth:password_change_done')), name='password_change'),
    url(r'^password-change/done/$',
        PasswordChangeDoneView.as_view(template_name='oauth/password_change_done.html'), name='password_change_done')
]
