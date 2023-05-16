from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r'', views.APIViewSet.as_view({"get": "list", "post": "create"}), name="goods"),
    path(r'file/', views.FileDownloadView.as_view({"get": "list"}), name="goodslistfiledownload"),
    path(r'test/', views.test, name='test_goods')

]
