"""DiyBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import RedirectView

from Blog import views as app_views


SOCIAL_AUTH_URL_NAMESPACE = 'social'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    url(r'^auth/', include('social_django.urls', namespace='social')),
]

urlpatterns += i18n_patterns(
    path('blog/', include('Blog.urls')),
    path('', RedirectView.as_view(url='/blog/'), name='home'),
    url(r'^signup/$', app_views.signup, name='signup'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
