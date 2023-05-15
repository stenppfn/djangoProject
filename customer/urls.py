from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

    path(r'', views.APIViewSet.as_view({"get": "list", "post": "create"}), name="customer"),
    path(r'file/', views.FileDownloadView.as_view({"get": "list"}), name="customerfiledownload"),

]
