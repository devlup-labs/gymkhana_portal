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
from django.contrib.auth.decorators import user_passes_test
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.views.decorators.csrf import csrf_exempt

from gymkhana.schema import PrivateGraphQLView, PublicGraphQLView
from gymkhana.views import FrontendUpdateView

admin.site.site_title = 'Gymkhana Administration'
admin.site.site_header = 'Gymkhana Administration'
admin.site.index_title = 'Control Panel'

urlpatterns = [
    url(
        '^login/$',
        LoginView.as_view(template_name='forum/login.html'), name='login'
    ),
    url(r'^logout/$', LogoutView.as_view(next_page='login'),
        name='logout'),
    url(r'^photologue/', include('photologue.urls', namespace='photologue')),
    url(r'^admin/', admin.site.urls),
    url(r'^admin/frontend-upload/',
        user_passes_test(lambda u: u.is_superuser, login_url='admin:login')(FrontendUpdateView.as_view()),
        name='admin-frontend-upload'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^account/', include('oauth.urls')),
    url(r'^forum/', include('forum.urls')),
    url(r'^forum/api/', include('forum.api.urls')),
    url(r'^konnekt/', include('konnekt.urls')),
    url(r'^festivals/', include('festivals.urls', namespace='festivals')),
    path('', include('social_django.urls', namespace='social')),
    url(r'^', include('main.urls')),
]

urlpatterns += [
    path("graphql", csrf_exempt(PublicGraphQLView.as_view(graphiql=True))),
    path("pgraphql", csrf_exempt(PrivateGraphQLView.as_view(graphiql=True)))
] if settings.DEBUG else [
    path("graphql", PublicGraphQLView.as_view(graphiql=True)),
    path("pgraphql", PrivateGraphQLView.as_view(graphiql=True))
]

if settings.DEBUG:  # pragma: no cover
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
