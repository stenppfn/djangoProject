from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r'list/', views.AsnListViewSet.as_view({"get": "list", "post": "create"}), name="asnlist"),

]
