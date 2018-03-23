from django.conf.urls import url
from forum import views

app_name = 'forum'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^answered-by-me/$', views.AnswerView.as_view(), name='answered-by-user'),
    url(r'^topic/add/$', views.TopicCreateView.as_view(), name='add_topic'),
    url(r'^(?P<slug>[\w-]+)/$', views.TopicDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/update/$', views.TopicUpdateView.as_view(), name='update_topic'),
    url(r'^(?P<slug>[\w-]+)/delete/$', views.TopicDeleteView.as_view(), name='delete_topic'),
    url(r'^answer/(?P<pk>\d+)/delete/$', views.AnswerDeleteView.as_view(), name='delete_answer'),
    url(r'^test/$', views.test, name='test'),
]
