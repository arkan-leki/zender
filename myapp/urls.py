from django.db.models.aggregates import Sum
from django.db.models.query import QuerySet
from rest_framework.fields import ReadOnlyField
from myapp.models import Group, Item, LocalCompany, Order, OrderDetail, Region, Sell, SellDetail, TradeCompany
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from . import views
# Serializers define the API representation.


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class SellSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sell
        fields = ['url', 'local', 'sell_detail', 'date','discount']


class TraderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TradeCompany
        fields = '__all__'


class SellDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellDetail
        fields = '__all__'


class SellXDetailSerializer(serializers.HyperlinkedModelSerializer):
    item = serializers.ReadOnlyField(source='item.name')
    sell = serializers.ReadOnlyField(source='sell.id')

    class Meta:
        model = SellDetail
        fields = ['url', 'item', 'quantity', 'price', 'sell', 'date', 'total']


class SellXSerializer(serializers.HyperlinkedModelSerializer):
    local = serializers.ReadOnlyField(source='local.name')
    sell_detail = SellXDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Sell
        fields = ['id','url', 'local', 'sell_detail', 'date', 'totall', 'discount']


class LocalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LocalCompany
        fields = '__all__'


class LocalXSerializer(serializers.ModelSerializer):
    region = serializers.ReadOnlyField(source='region.name')
    sell_compnay = SellXSerializer(read_only=True, many=True)
    totallSell = serializers.ReadOnlyField()

    class Meta:
        model=LocalCompany
        fields=['name', 'phone', 'region',
            'owner_name', 'sell_compnay', 'totallSell']


class GroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model=Group
        fields='__all__'

class RegionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model=Region
        fields='__all__'


class ItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model=Item
        fields='__all__'


class OrderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model=Order
        fields='__all__'

class OrderedSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model=OrderDetail
        fields='__all__'


class ItemXSerializer(serializers.HyperlinkedModelSerializer):
    group=serializers.ReadOnlyField(source='group.name')
    trader=serializers.ReadOnlyField(source='trader.name')

    class Meta:
        model=Item
        fields=['id', 'name', 'group', 'bag', 'quantity',
                  'barcode', 'trader', 'finalprice', 'mawe']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer

class LocalViewSet(viewsets.ModelViewSet):
    queryset=LocalCompany.objects.all()
    serializer_class=LocalSerializer

class LocalXViewSet(viewsets.ModelViewSet):
    queryset=LocalCompany.objects.all()
    serializer_class=LocalXSerializer

class TraderViewSet(viewsets.ModelViewSet):
    queryset=TradeCompany.objects.all()
    serializer_class=TraderSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset=Item.objects.all()
    serializer_class=ItemSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset=Group.objects.all()
    serializer_class=GroupSerializer


class ItemXViewSet(viewsets.ModelViewSet):
    queryset=Item.objects.all()
    serializer_class=ItemXSerializer


class SellDetailViewSet(viewsets.ModelViewSet):
    queryset=SellDetail.objects.all()
    serializer_class=SellDetailSerializer

class SellXDetailViewSet(viewsets.ModelViewSet):
    queryset=SellDetail.objects.all()
    serializer_class=SellXDetailSerializer


class SellViewSet(viewsets.ModelViewSet):
    queryset=Sell.objects.all()
    serializer_class=SellSerializer

class SellXViewSet(viewsets.ModelViewSet):
    queryset=Sell.objects.all()
    serializer_class=SellXSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset=Order.objects.all()
    serializer_class=OrderSerializer

class OrderedViewSet(viewsets.ModelViewSet):
    queryset=OrderDetail.objects.all()
    serializer_class=OrderedSerializer

class RegionViewSet(viewsets.ModelViewSet):
    queryset=Region.objects.all()
    serializer_class=RegionSerializer


# Routers provide an easy way of automatically determining the URL conf.
router=routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'items', ItemXViewSet)
router.register(r'item', ItemViewSet)
router.register(r'sale', SellDetailViewSet)
router.register(r'sales', SellXDetailViewSet)
router.register(r'sell', SellViewSet)
router.register(r'sells', SellXViewSet)
router.register(r'local', LocalViewSet)
router.register(r'locals', LocalXViewSet)
router.register(r'trader', TraderViewSet)
router.register(r'group', GroupViewSet)
router.register(r'region', RegionViewSet)
router.register(r'order', OrderViewSet)
router.register(r'ordered', OrderedViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns=[
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
