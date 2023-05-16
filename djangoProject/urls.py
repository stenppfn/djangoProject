"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve as static_serve
from django.contrib.staticfiles.views import serve

from djangoProject import views, settings


def return_static(request, path, insecure=True, **kwargs):
    return serve(request, path, insecure, **kwargs)


urlpatterns = [
    path('', TemplateView.as_view(template_name='')),

    path('admin/', admin.site.urls),
    path('myip/', views.myip, name='myip'),

    path('asn/', include('asn.urls')),
    path('customer/', include('customer.urls')),
    path('register/', include('userregister.urls')),
    path('login/', include('userlogin.urls')),
    path('staff/', include('staff.urls')),
    path('supplier/', include('supplier.urls')),

    # 静态资源
    re_path(r'^favicon\.ico$', views.favicon, name='favicon'),
    re_path('^css/.*$', views.css, name='css'),
    re_path('^js/.*$', views.js, name='js'),
    re_path('^statics/.*$', views.statics, name='statics'),
    re_path('^fonts/.*$', views.fonts, name='fonts'),
    re_path(r'^robots.txt', views.robots, name='robots'),
    re_path(r'^static/(?P<path>.*)$', return_static, name='static'),
    re_path(r'^media/(?P<path>.*)$', static_serve, {'document_root': settings.MEDIA_ROOT})
]
