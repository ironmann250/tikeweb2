"""tikeweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from tikeshell import views as tikeshell_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', tikeshell_views.loginpg),
    url(r'^index/', tikeshell_views.home),
    url(r'^logout/$',auth_views.logout, {'next_page': '/'}),
    url(r'^$',tikeshell_views.home),
    url(r'^yoostudioz/',tikeshell_views.event),
    url(r'^signup/',tikeshell_views.signup),
    url(r'^support/',tikeshell_views.support),
    url(r'^all/',tikeshell_views.all),
    url(r'^search/',tikeshell_views.search),
    url(r'^reset/',tikeshell_views.reset),
    url(r'^pay_portal/',tikeshell_views.pay_portal),
    url(r'^validate/',tikeshell_views.validate),
    url(r'^educational/(?P<event_id>\d+)',tikeshell_views.educational),
    url(r'^entertainment/(?P<event_id>\d+)',tikeshell_views.entertainment),
    url(r'^dashboard/(?P<user>\d+)',tikeshell_views.dashboard),
    url(r'^dashboard/',tikeshell_views.dashboard),
    url(r'^support/',tikeshell_views.support),
    url(r'^test/(?P<val>.*)',tikeshell_views.test),
    url(r'^get_qrcode/(?P<text>.*)',tikeshell_views.render_qrcode),
    url(r'^get_tickets/(?P<id>.*)',tikeshell_views.download_event_tickets),
    url(r'^get_ids/(?P<n>.*)',tikeshell_views.get_event_ids),
    #security vurnel'ability here this can act as truthness function[explanation later]'
]
urlpatterns=urlpatterns+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
