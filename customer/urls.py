from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path(r'', views.APIViewSet.as_view({"get": "list", "post": "create"}), name="customer"),
    path(r'file/', views.FileDownloadView.as_view({"get": "list"}), name="customerfiledownload"),
    re_path(r'^(?P<pk>\d+)/$', views.APIViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name="customer_1")
]
