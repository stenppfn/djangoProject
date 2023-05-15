from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path(r'test/', views.test, name='test_login')
]
