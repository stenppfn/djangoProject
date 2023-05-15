from django.shortcuts import render
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from .models import ListModel

# Create your views here.
from rest_framework import viewsets


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

    # pagination_class = MyPageNumberPagination
    # filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    # ordering_fields = ['id', "create_time", "update_time", ]
    # filter_class = Filter

    def get_project(self):
        try:
            id = self.kwargs.get('pk')
            return id
        except:
            return None

    def get_queryset(self):
        id = self.get_project()
        if self.request.user:
            if id is None:
                return ListModel.objects.filter(openid=self.request.auth.openid, is_delete=False)
            else:
                return ListModel.objects.filter(openid=self.request.auth.openid, id=id, is_delete=False)
        else:
            return ListModel.objects.none()

    # def get_serializer_class(self):
    #     if self.action in ['list', 'retrieve', 'destroy']:
    #         return serializers.CustomerGetSerializer
    #     elif self.action in ['create']:
    #         return serializers.CustomerPostSerializer
    #     elif self.action in ['update']:
    #         return serializers.CustomerUpdateSerializer
    #     elif self.action in ['partial_update']:
    #         return serializers.CustomerPartialUpdateSerializer
    #     else:
    #         return self.http_method_not_allowed(request=self.request)
    #
    def create(self, request, *args, **kwargs):
        data = self.request.data
        data['openid'] = self.request.auth.openid
        if ListModel.objects.filter(openid=data['openid'], customer_name=data['customer_name'], is_delete=False).exists():
            raise APIException({"detail": "Data exists"})
        else:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=200, headers=headers)

    # def update(self, request, pk):
    #     qs = self.get_object()
    #     if qs.openid != self.request.auth.openid:
    #         raise APIException({"detail": "Cannot update data which not yours"})
    #     else:
    #         data = self.request.data
    #         serializer = self.get_serializer(qs, data=data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=200, headers=headers)
    #
    # def partial_update(self, request, pk):
    #     qs = self.get_object()
    #     if qs.openid != self.request.auth.openid:
    #         raise APIException({"detail": "Cannot partial_update data which not yours"})
    #     else:
    #         data = self.request.data
    #         serializer = self.get_serializer(qs, data=data, partial=True)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=200, headers=headers)
    #
    # def destroy(self, request, pk):
    #     qs = self.get_object()
    #     if qs.openid != self.request.auth.openid:
    #         raise APIException({"detail": "Cannot delete data which not yours"})
    #     else:
    #         qs.is_delete = True
    #         qs.save()
    #         serializer = self.get_serializer(qs, many=False)
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=200, headers=headers)


class FileDownloadView(viewsets.ModelViewSet):
    pass


