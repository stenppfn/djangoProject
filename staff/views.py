from django.http import JsonResponse
from rest_framework import viewsets
# from .models import ListModel, TypeListModel
# from . import serializers
# from utils.page import MyPageNumberPagination
# from rest_framework.filters import OrderingFilter
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.response import Response
# from .filter import Filter, TypeFilter
# from rest_framework.exceptions import APIException
# from .serializers import FileRenderSerializer
# from django.http import StreamingHttpResponse
# from .files import FileRenderCN, FileRenderEN
# from rest_framework.settings import api_settings
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from staff import serializers
from staff.models import ListModel
from utils.fbmsg import FBMsg


def test(request):
    return JsonResponse(FBMsg.ret())


class APIViewSet(viewsets.ModelViewSet):
    """
        retrieve:
            Response a data list（get）

        list:
            Response a data list（all）

        create:
            Create a data line（post）

        delete:
            Delete a data line（delete)

        partial_update:
            Partial_update a data（patch：partial_update）

        update:
            Update a data（put：update）
    """

    def get_project(self):
        try:
            id = self.kwargs.get('pk')
            # id = '6608c32f0a6e75ce0374df6123b4d1d4'
            return id
        except:
            return None

    def get_queryset(self):
        id = self.get_project()
        if self.request.user:
            if id is None:
                # return ListModel.objects.filter(openid=self.request.auth.openid, is_delete=False)
                return ListModel.objects.filter(openid='6608c32f0a6e75ce0374df6123b4d1d4', is_delete=False)
            else:
                return ListModel.objects.filter(openid=self.request.auth.openid, id=id, is_delete=False)
        else:
            return ListModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'destroy']:
            return serializers.StaffGetSerializer
        elif self.action in ['create']:
            return serializers.StaffPostSerializer
        elif self.action in ['update']:
            return serializers.StaffUpdateSerializer
        elif self.action in ['partial_update']:
            return serializers.StaffPartialUpdateSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, *args, **kwargs):
        # data = self.request.data
        # data['openid'] = self.request.auth.openid
        data = {'staff_name': 'zz'}
        data['openid'] = '6608c32f0a6e75ce0374df6123b4d1d4'
        if ListModel.objects.filter(openid=data['openid'], staff_name=data['staff_name'], is_delete=False).exists():
            raise APIException({"detail": "Data exists"})
        else:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=200, headers=headers)
