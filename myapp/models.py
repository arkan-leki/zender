from django.db import models
from django.db.models.aggregates import Sum
from django.db.models.expressions import F
from django.db.models.fields import DecimalField

# Create your models here.


class Region(models.Model):
    name = models.CharField(verbose_name="nawche", max_length=250)
    code = models.CharField("zip code", max_length=150)
    date = models.DateTimeField(verbose_name="rekwt", auto_now_add=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return


class TradeCompany(models.Model):
    name = models.CharField(verbose_name="naw companya", max_length=250)
    code = models.CharField("cody company", max_length=150)
    date = models.DateTimeField(verbose_name="rekwt", auto_now_add=True)
    branch = models.CharField(
        verbose_name="grwpy companya", max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return


class LocalCompany(models.Model):
    name = models.CharField(verbose_name="naw kryar", max_length=250)
    code = models.CharField("cody kryar", max_length=150)
    region = models.ForeignKey("Region", verbose_name="nawche",
                               on_delete=models.CASCADE, related_name="local_region")
    address = models.CharField(
        verbose_name="naw nishan", max_length=150, blank=True, null=True)
    phone = models.CharField(verbose_name="jmare mobile",
                             max_length=150, blank=True, null=True)
    owner_name = models.CharField(
        verbose_name="naw xawenar", max_length=250, blank=True, null=True)
    date = models.DateTimeField(verbose_name="rekwt", auto_now_add=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return

    @property
    def totallSell(self):
        totalls = 0
        for totall in self.sell_compnay.all():
            totalls = totalls + totall.totallint
        return str(totalls)


class Group(models.Model):
    name = models.CharField(verbose_name="nawy group", max_length=250)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return


class Item(models.Model):
    group = models.ForeignKey("Group", verbose_name="naw group",
                              on_delete=models.CASCADE, related_name="item_group")
    name = models.CharField(verbose_name="nawy mawad", max_length=250)
    bag = models.CharField(verbose_name="jor bar", max_length=250)
    quantity = models.CharField(verbose_name="dane", max_length=250)
    barcode = models.CharField("cody mewad", max_length=150)
    price = models.DecimalField(
        verbose_name="nrx kiren", max_digits=5, decimal_places=2)
    addprice = models.DecimalField(
        verbose_name="reje qazanc", max_digits=5, decimal_places=2)
    trader = models.ForeignKey("TradeCompany", verbose_name="naw companyia",
                               on_delete=models.CASCADE, related_name="item_compnay")
    date = models.DateTimeField(verbose_name="rekwt", auto_now_add=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return

    @property
    def mawe(self):
        mawe = 0
        krin = self.item_order.aggregate(Sum('quantity'))['quantity__sum']
        frosh = self.item_sell.aggregate(Sum('quantity'))['quantity__sum']
        if krin == "null" and frosh == 'null':
            mawe = krin - frosh
        return mawe

    @property
    def finalprice(self):
        return str(float('{:.2f}'.format(self.price + (self.price * self.addprice))))


class Sell(models.Model):
    local = models.ForeignKey("LocalCompany", verbose_name="naw kryar",
                              on_delete=models.CASCADE, related_name="sell_compnay")
    discount = models.DecimalField(
        verbose_name="dashkan", max_digits=5, decimal_places=2, blank=True, default=0.0)
    date = models.DateTimeField(verbose_name="rekwt", auto_now_add=True)

    def __str__(self):
        return "wasl " + str(self.id)

    @property
    def totall(self):
        total = float('{:.2f}'.format(self.sell_detail.annotate(answer=F('price') * F('quantity')).aggregate(total=Sum('answer'))['total']))
        return str(total)

    @property
    def totallint(self):
        return self.sell_detail.annotate(answer=F('price') * F('quantity')).aggregate(total=Sum('answer'))['total']


class SellDetail(models.Model):
    sell = models.ForeignKey("Sell", verbose_name="wasl",
                             on_delete=models.CASCADE, related_name="sell_detail")
    item = models.ForeignKey("Item", verbose_name="naw kala",
                             on_delete=models.CASCADE, related_name="item_sell")
    quantity = models.IntegerField(verbose_name="dane")
    price = models.DecimalField(
        verbose_name="nrx", max_digits=5, decimal_places=2)
    date = models.DateTimeField(verbose_name="rekwt", auto_now_add=True)

    def total(self):
        return self.price * self.quantity

    def addprice(self):
        return self.item.finalprice

    def mawe(self):
        return self.item.mawe

    def __str__(self):
        return "forsh kala " + str(self.id)


class Order(models.Model):
    local = models.ForeignKey("TradeCompany", verbose_name="naw compaya",
                              on_delete=models.CASCADE, related_name="order_compnay")
    date = models.DateTimeField(verbose_name="rekwt", auto_now_add=True)

    def __str__(self):
        return "wasl " + str(self.id)


class OrderDetail(models.Model):
    order = models.ForeignKey("Order", verbose_name="wasl",
                              on_delete=models.CASCADE, related_name="order_detail")
    item = models.ForeignKey("Item", verbose_name="naw kala",
                             on_delete=models.CASCADE, related_name="item_order")
    quantity = models.CharField(verbose_name="dane", max_length=250)
    price = models.DecimalField(
        verbose_name="nrx", max_digits=5, decimal_places=2)
    date = models.DateTimeField(verbose_name="rekwt", auto_now_add=True)


class Bar(models.Model):
    trader = models.ForeignKey("TradeCompany", verbose_name="naw kryar",
                               on_delete=models.CASCADE, related_name="Bar_compnay")
    date = models.DateTimeField(verbose_name="rekwt", auto_now_add=True)
    date = models.DateTimeField(verbose_name="rekwt", auto_now_add=True)

    def __str__(self):
        return "wasl bar " + str(self.id)


class BarDetail(models.Model):
    bar = models.ForeignKey("Bar", verbose_name="wasl",
                            on_delete=models.CASCADE, related_name="Bar_detail")
    item = models.ForeignKey("Item", verbose_name="naw kala",
                             on_delete=models.CASCADE, related_name="item_bar")
    quantity = models.CharField(verbose_name="dane", max_length=250)
    price = models.DecimalField(
        verbose_name="nrx", max_digits=5, decimal_places=2)
    date = models.DateTimeField(verbose_name="rekwt", auto_now_add=True)

    def __str__(self):
        return "hawtw kala " + str(self.id)
