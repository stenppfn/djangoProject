from django.db.models import Q
from django.utils import timezone
from pip._vendor.requests import Response
from rest_framework import viewsets
from dateutil.relativedelta import relativedelta
from rest_framework.filters import OrderingFilter

from scanner.models import ListModel as scanner
from stock.models import StockListModel as stocklist


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import APIException

from asn.page import MyPageNumberPaginationASNList
from utils.fbmsg import FBMsg
from utils.md5 import Md5
from . import serializers
from .filter import AsnListFilter, AsnDetailFilter
from .models import AsnListModel, AsnDetailModel


class AsnListViewSet(viewsets.ModelViewSet):
    """
        retrieve:
            Response a data list（get）
        list:
            Response a data list（all）
        create:
            Create a data line（post）

        delete:
            Delete a data line（delete)

    """
    pagination_class = MyPageNumberPaginationASNList
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "create_time", "update_time", ]
    filter_class = AsnListFilter

    def get_project(self):
        try:
            id = self.kwargs.get('pk')
            return id
        except:
            return None

    def get_queryset(self):
        id = self.get_project()
        if self.request.user:
            empty_qs = AsnListModel.objects.filter(
                Q(openid=self.request.auth.openid, asn_status=1, is_delete=False) & Q(supplier=''))
            cur_date = timezone.now()
            date_check = relativedelta(day=1)
            if len(empty_qs) > 0:
                for i in range(len(empty_qs)):
                    if empty_qs[i].create_time <= cur_date - date_check:
                        empty_qs[i].delete()
            if id is None:
                return AsnListModel.objects.filter(
                    Q(openid=self.request.auth.openid, is_delete=False) & ~Q(supplier=''))
            else:
                return AsnListModel.objects.filter(
                    Q(openid=self.request.auth.openid, id=id, is_delete=False) & ~Q(supplier=''))
        else:
            return AsnListModel.objects.none()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'destroy']:
            return serializers.ASNListGetSerializer
        elif self.action in ['create']:
            return serializers.ASNListPostSerializer
        elif self.action in ['update']:
            return serializers.ASNListUpdateSerializer
        elif self.action in ['partial_update']:
            return serializers.ASNListPartialUpdateSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def notice_lang(self):
        return FBMsg(self.request.META.get('HTTP_LANGUAGE'))

    def create(self, request, *args, **kwargs):
        data = self.request.data
        data['openid'] = self.request.auth.openid
        custom_asn = self.request.GET.get('custom_asn', '')
        if custom_asn:
            data['asn_code'] = custom_asn
        else:
            qs_set = AsnListModel.objects.filter(openid=self.request.auth.openid, is_delete=False)
            order_day = str(timezone.now().strftime('%Y%m%d'))
            if len(qs_set) > 0:
                asn_last_code = qs_set.order_by('-id').first().asn_code
                if str(asn_last_code[3:11]) == order_day:
                    order_create_no = str(int(asn_last_code[11:]) + 1)
                    data['asn_code'] = 'ASN' + order_day + order_create_no
                else:
                    data['asn_code'] = 'ASN' + order_day + '1'
            else:
                data['asn_code'] = 'ASN' + order_day + '1'
        data['bar_code'] = Md5.md5(data['asn_code'])
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        scanner.objects.create(openid=self.request.auth.openid, mode="ASN", code=data['asn_code'],
                               bar_code=data['bar_code'])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=200, headers=headers)

    def destroy(self, request, pk):
        qs = self.get_object()
        if qs.openid != self.request.auth.openid:
            raise APIException({"detail": "Cannot delete data which not yours"})
        else:
            if qs.asn_status == 1:
                qs.is_delete = True
                asn_detail_list = AsnDetailModel.objects.filter(openid=self.request.auth.openid, asn_code=qs.asn_code,
                                                                asn_status=1, is_delete=False)
                for i in range(len(asn_detail_list)):
                    goods_qty_change = stocklist.objects.filter(openid=self.request.auth.openid,
                                                                goods_code=str(asn_detail_list[i].goods_code)).first()
                    goods_qty_change.goods_qty = goods_qty_change.goods_qty - int(asn_detail_list[i].goods_qty)
                    goods_qty_change.asn_stock = goods_qty_change.asn_stock - int(asn_detail_list[i].goods_qty)
                    goods_qty_change.save()
                asn_detail_list.update(is_delete=True)
                qs.save()
                serializer = self.get_serializer(qs, many=False)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=200, headers=headers)
            else:
                raise APIException({"detail": "This ASN Status Is Not '1'"})
