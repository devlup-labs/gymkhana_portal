"""gymkhana URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.urls import path, re_path
from django.contrib.auth.decorators import user_passes_test
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.views.decorators.csrf import csrf_exempt

from gymkhana.schema import PrivateGraphQLView, PublicGraphQLView
from gymkhana.views import FrontendUpdateView, VueView
from oauth.views import SessionView

admin.site.site_title = 'Gymkhana Administration'
admin.site.site_header = 'Gymkhana Administration'
admin.site.index_title = 'Control Panel'

urlpatterns = [
    url(r'^logout/$', LogoutView.as_view(next_page='login'),
        name='logout'),
    url(r'^session/$', SessionView.as_view(), name='session'),
    url(r'^photologue/', include('photologue.urls', namespace='photologue')),
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^admin/frontend-upload/',
        user_passes_test(lambda u: u.is_superuser, login_url='admin:login')(FrontendUpdateView.as_view()),
        name='admin-frontend-upload'),
    path('', include('social_django.urls', namespace='social')),
]

urlpatterns += [
    path("graphql", csrf_exempt(PublicGraphQLView.as_view(graphiql=True))),
    path("pgraphql", csrf_exempt(PrivateGraphQLView.as_view(graphiql=True)))
]

if settings.DEBUG:  # pragma: no cover
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [re_path(r'.*', VueView.as_view(), name='vue-js')]
