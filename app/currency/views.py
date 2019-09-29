import datetime

# from drf_yasg import openapi
# from drf_yasg.utils import swagger_auto_schema
from django.db.models import Sum
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from currency.helper import RateManager
from currency.models import Currency, Rate
from currency.serializers import CurrencySerializer, OneRateSerializer


class CurrencyView(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = (IsAuthenticated,)
    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    pagination_class = PageNumberPagination

    @swagger_auto_schema(
        operation_id='currency-list',
        operation_summary='Currency list',
        operation_description='''''',
        tags=['currency'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class RateView(ViewSet):
    queryset = Rate.objects.all()
    serializer_class = OneRateSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_id='rate',
        operation_summary='Rate',
        operation_description='''''',
        tags=['rate'],
        manual_parameters=[
            openapi.Parameter(
                name='days', in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="",
                required=False
            ),

        ],
        responses={
            status.HTTP_200_OK: openapi.Response('', OneRateSerializer()),
            status.HTTP_400_BAD_REQUEST: openapi.Response('', OneRateSerializer())
        }
    )
    def data(self, request, pk, *args, **kwargs):
        currency = Currency.objects.filter(id=pk).first()
        if currency:

            days = int(request.query_params.get('days', 10))
            interval = datetime.datetime.now() - datetime.timedelta(days=days)
            total_sum = self.queryset.filter(currency_id=pk, date__gt=interval).aggregate(total_sum=Sum('volume'))
            average_volume = total_sum['total_sum'] / days if total_sum['total_sum'] else None
            rm = RateManager()
            last_rate = rm.get_last(pk)
            serializer = self.serializer_class({
                'success': True,
                'average_volume': average_volume,
                'last_rate': last_rate,
                'currency': currency.name
            })
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = self.serializer_class({
                'success': False,
            })
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
