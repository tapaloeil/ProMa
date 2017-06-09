"""ProMa URL Configuration

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
from django.conf import settings
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView

admin.site.site_header='ProMa Administration'
admin.site.site_title='ProMa Administration'

urlpatterns = i18n_patterns(
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^admin/', admin.site.urls,name='admin'),
    url(r'^tinymce/',include('tinymce.urls')),
    url(r'^rosetta/',include('rosetta.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^frontend/', include('frontend.urls')),
    url(r'^todo/', include('todo.urls')),
    url(r'^scheduling/', include('Scheduling.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)