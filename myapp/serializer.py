# Serializers define the API representation.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class SellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sell
        fields = ['url', 'local', 'date','discount']


class TraderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeCompany
        fields = '__all__'


class SellDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellDetail
        fields = '__all__'


class LocalXSerializer(serializers.ModelSerializer):
    region = serializers.ReadOnlyField(source='region.name')
    # sell_compnay = SellXSerializer(read_only=True, many=True)
    totallSell = serializers.ReadOnlyField()

    class Meta:
        model=LocalCompany
        fields=['id','name', 'phone','code', 'region',
            'owner_name', 'totallSell']


class SellXDetailSerializer(serializers.ModelSerializer):
    item = serializers.ReadOnlyField(source='item.name')
    sell = serializers.ReadOnlyField(source='sell.id')

    class Meta:
        model = SellDetail
        fields = ['url', 'item', 'quantity', 'price', 'sell', 'date', 'total']

class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalCompany
        fields = '__all__'

class SellXSerializer(serializers.ModelSerializer):
    local_name = serializers.ReadOnlyField(source='local.name')
    local_code = serializers.ReadOnlyField(source='local.code')
    sell_detail = SellXDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Sell
        fields = ['id','url', 'local_id', 'local_name', 'local_code', 'sell_detail', 'date', 'totall', 'discount']


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model=Group
        fields='__all__'

class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model=Region
        fields='__all__'


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model=Item
        fields='__all__'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model=Order
        fields='__all__'

class OrderedSerializer(serializers.ModelSerializer):

    class Meta:
        model=OrderDetail
        fields='__all__'


class ItemXSerializer(serializers.ModelSerializer):
    group=serializers.ReadOnlyField(source='group.name')
    trader=serializers.ReadOnlyField(source='trader.name')

    class Meta:
        model=Item
        fields=['id', 'name', 'group', 'bag', 'quantity',
                  'barcode', 'trader', 'finalprice', 'mawe']

