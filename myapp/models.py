import decimal
from django.db import models
from django.db.models.aggregates import Sum
from django.db.models.expressions import F
from django.db.models.fields.related import ManyToManyField

# Create your models here.


class Group(models.Model):
    name = models.CharField(verbose_name="nawy group", max_length=250)
    phone = models.CharField(verbose_name="jmary mobile",
                             max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return


class Epmploye(models.Model):
    name = models.CharField(verbose_name="nawy krekar", max_length=250)
    phone = models.CharField(verbose_name="jmary mobile",
                             max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return


class Region(models.Model):
    name = models.CharField(verbose_name="nawche", max_length=250)
    code = models.CharField("zip code", max_length=150)
    date = models.DateField(
        verbose_name="barwar", auto_now_add=True, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return


class Vendor(models.Model):
    name = models.CharField(verbose_name="nawy mandub", max_length=250)
    phone = models.CharField(verbose_name="jmary mobile",
                             max_length=250, blank=True, null=True)
    regions = models.ManyToManyField("region")
    group = models.ForeignKey("Group", verbose_name="naw group",
                              on_delete=models.CASCADE, related_name="vendor_group", null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return


class TradeCompany(models.Model):
    name = models.CharField(verbose_name="naw companya", max_length=250)
    code = models.CharField("cody company", max_length=150)
    date = models.DateField(
        verbose_name="barwar", auto_now_add=True, blank=True)
    group = models.ForeignKey("Group", verbose_name="naw group",
                              on_delete=models.CASCADE, related_name="trader_group")
    exchange = models.DecimalField(
        verbose_name="qarz yakam jar", max_digits=22, decimal_places=2, default="0.0")

    def __str__(self):
        return self.name

    def __unicode__(self):
        return

    @property
    def mawe(self):
        paylaon = 0
        buy = 0
        if(self.loan_compnay.all()):
            for pay in self.loan_compnay.all():
                paylaon = paylaon + pay.bank.loan

        if(self.order_compnay.all()):
            for laon in self.order_compnay.all():
                buy = buy + laon.totallint

        return (buy - paylaon) + self.exchange

    @property
    def totallLoan(self):
        totalls = 0
        for pay in self.loan_compnay.all():
            totalls = totalls + pay.bank.loan
        return str(float('{:.2f}'.format(totalls)))
    
    @property
    def totallBuy(self):
        totalls = 0
        for totall in self.order_compnay.all():
            totalls = totalls + totall.totallint
        return str(float('{:.2f}'.format(totalls)))


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
    date = models.DateField(
        verbose_name="barwar", auto_now_add=True, blank=True)
    exchange = models.DecimalField(
        verbose_name="qarz yakam jar", max_digits=22, decimal_places=2, default="0.0")
    location = models.DecimalField(
        max_digits=22, decimal_places=16, blank=True, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return

    @property
    def mawe(self):
        paylaon = 0
        buy = 0
        if(self.payment_compnay.all()):
            for pay in self.payment_compnay.all():
                paylaon = paylaon + pay.bank.income

        if(self.sell_compnay.all()):
            for laon in self.sell_compnay.all():
                buy = buy + laon.totallint

        return (buy - paylaon) + self.exchange - decimal.Decimal(self.totallSellback)

    @property
    def totallPay(self):
        totalls = 0
        for pay in self.payment_compnay.all():
            totalls = totalls + pay.bank.income
        return str(float('{:.2f}'.format(totalls)))

    @property
    def totallSell(self):
        totalls = 0
        for totall in self.sell_compnay.all():
            totalls = totalls + totall.totallint
        return str(float('{:.2f}'.format(totalls)))

    @property
    def totallSellback(self):
        totalls = 0
        for totall in self.sell_compnay.all():
            totalls = totalls + totall.totalback
        return float('{:.2f}'.format(totalls))


class Item(models.Model):
    group = models.ForeignKey("Group", verbose_name="naw group",
                              on_delete=models.CASCADE, related_name="item_group")
    name = models.CharField(verbose_name="nawy mawad", max_length=250)
    bag = models.CharField(verbose_name="jor bar", max_length=250)
    wight = models.DecimalField(
        verbose_name="wazn kala", max_digits=22, decimal_places=2, default="0.0")
    quantity = models.IntegerField(verbose_name="dane")
    barcode = models.CharField("cody mewad", max_length=150)
    price = models.DecimalField(
        verbose_name="nrx kiren", max_digits=22, decimal_places=2)
    addprice = models.DecimalField(
        verbose_name="reje qazanc", max_digits=22, decimal_places=2)
    trader = models.ForeignKey("TradeCompany", verbose_name="naw companyia",
                               on_delete=models.CASCADE, related_name="item_compnay")
    stock = models.IntegerField(verbose_name="stock", default=0)
    date = models.DateField(
        verbose_name="barwar", auto_now_add=True, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return

    @property
    def wightAll(self):
        return self.wight * self.quantity

    @property
    def mawe(self):
        krin = 0
        frosh = 0
        gerawe = 0
        if(self.item_order.aggregate(Sum('quantity'))['quantity__sum']):
            krin = self.item_order.aggregate(Sum('quantity'))['quantity__sum']

        frosh = 0
        if(self.item_sell.aggregate(Sum('quantity'))['quantity__sum']):
            frosh = self.item_sell.aggregate(Sum('quantity'))['quantity__sum']

        if self.ReSell_item.aggregate(Sum('quantity'))['quantity__sum']:
            gerawe = self.ReSell_item.aggregate(
                Sum('quantity'))['quantity__sum']

        return (krin - frosh) + (self.stock) + (gerawe)

    @property
    def finalprice(self):
        return str(float('{:.2f}'.format(self.price + (self.price * self.addprice))))


class Sell(models.Model):
    vendor = models.ForeignKey("Vendor", verbose_name="naw mandub",
                               on_delete=models.CASCADE, related_name="sell_group")
    group = models.ForeignKey("Group", verbose_name="naw group",
                              on_delete=models.CASCADE, related_name="sell_group")
    local = models.ForeignKey("LocalCompany", verbose_name="naw kryar",
                              on_delete=models.CASCADE, related_name="sell_compnay")
    discount = models.DecimalField(
        verbose_name="dashkan", max_digits=22, decimal_places=2, blank=True, default=0.0)
    date = models.DateField(
        verbose_name="barwar", auto_now_add=True, blank=True)
    datetime = models.DateTimeField(
        verbose_name="rekwt", auto_now_add=True, blank=True)

    def __str__(self):
        return "wasl " + str(self.id)

    @property
    def totall(self):
        total = 0
        if len(self.sell_detail.all()):
            total = float('{:.2f}'.format(self.sell_detail.annotate(
                answer=F('price') * F('quantity')).aggregate(total=Sum('answer'))['total']))
        return str(total)

    @property
    def totalback(self):
        tot = 0
        if len(self.ReSell_detail.all()):
            tot = self.ReSell_detail.annotate(
                answer=F('price') * F('quantity')).aggregate(total=Sum('answer'))['total']
        return tot

    @property
    def totallint(self):
        tot = 0
        if len(self.sell_detail.all()):
            tot = self.sell_detail.annotate(
                answer=F('price') * F('quantity')).aggregate(total=Sum('answer'))['total'] - self.discount
        return tot


class SellDetail(models.Model):
    sell = models.ForeignKey("Sell", verbose_name="wasl",
                             on_delete=models.CASCADE, related_name="sell_detail")
    item = models.ForeignKey("Item", verbose_name="naw kala",
                             on_delete=models.CASCADE, related_name="item_sell")
    quantity = models.IntegerField(verbose_name="dane")
    price = models.DecimalField(
        verbose_name="nrx", max_digits=22, decimal_places=2)
    date = models.DateField(
        verbose_name="barwar", auto_now_add=True, blank=True)
    datetime = models.DateTimeField(
        verbose_name="rekwt", auto_now_add=True, blank=True)

    def total(self):
        return self.price * self.quantity

    def addprice(self):
        return self.item.finalprice

    def mawe(self):
        return self.item.mawe

    def __str__(self):
        return "forsh kala " + str(self.id)

# // mewady hawt nek order


class Order(models.Model):
    group = models.ForeignKey("Group", verbose_name="naw group",
                              on_delete=models.CASCADE, related_name="order_group")
    trader = models.ForeignKey("TradeCompany", verbose_name="naw compaya",
                               on_delete=models.CASCADE, related_name="order_compnay")
    code = models.CharField(verbose_name="jamrey wesl",
                            max_length=250, blank=True, default="")
    discount = models.DecimalField(
        verbose_name="dashkandn", max_digits=22, decimal_places=2, blank=True, default="0.0")
    date = models.DateField(
        verbose_name="barwar", auto_now_add=True, blank=True)
    datetime = models.DateTimeField(
        verbose_name="rekwt", auto_now_add=True, blank=True)

    def __str__(self):
        return "wasl dawakary" + str(self.id)

    @property
    def totall(self):
        total = 0
        if len(self.order_detail.all()):
            total = float('{:.2f}'.format(self.order_detail.annotate(
                answer=F('price') * F('quantity')).aggregate(total=Sum('answer'))['total']))
        return str(total)

    @property
    def totallint(self):
        tot = 0
        if len(self.order_detail.all()):
            tot = self.order_detail.annotate(
                answer=F('price') * F('quantity')).aggregate(total=Sum('answer'))['total'] - self.discount
        return tot


class OrderDetail(models.Model):
    order = models.ForeignKey("Order", verbose_name="wasl",
                              on_delete=models.CASCADE, related_name="order_detail")
    item = models.ForeignKey("Item", verbose_name="naw kala",
                             on_delete=models.CASCADE, related_name="item_order")
    quantity = models.IntegerField(verbose_name="dane")
    price = models.DecimalField(
        verbose_name="nrx", max_digits=22, decimal_places=2)
    date = models.DateField(verbose_name="barwar", auto_now_add=True)
    datetime = models.DateTimeField(
        verbose_name="rekwt", auto_now_add=True, blank=True)

    @property
    def total(self):
        return self.price * self.quantity


class Payment(models.Model):
    group = models.ForeignKey("Group", verbose_name="naw group",
                              on_delete=models.CASCADE, related_name="payment_group")
    local = models.ForeignKey("LocalCompany", verbose_name="naw kryar",
                              on_delete=models.CASCADE, related_name="payment_compnay")
    bank = models.ForeignKey("Bank", verbose_name="qase",
                             on_delete=models.CASCADE, related_name="payment_bank")
    date = models.DateField(
        verbose_name="barwar", auto_now_add=True, blank=True)
    datetime = models.DateTimeField(
        verbose_name="rekwt", auto_now_add=True, blank=True)


class Payloan(models.Model):
    group = models.ForeignKey("Group", verbose_name="naw group",
                              on_delete=models.CASCADE, related_name="loan_group")
    trader = models.ForeignKey("TradeCompany", verbose_name="naw kryar",
                               on_delete=models.CASCADE, related_name="loan_compnay")
    bank = models.ForeignKey("Bank", verbose_name="qase",
                             on_delete=models.CASCADE, related_name="loan_bank")
    date = models.DateField(
        verbose_name="barwar", auto_now_add=True, blank=True)
    datetime = models.DateTimeField(
        verbose_name="rekwt", auto_now_add=True, blank=True)


class buy(models.Model):
    name = models.CharField(verbose_name="ho", max_length=250, blank=True)
    group = models.ForeignKey("Group", verbose_name="naw group",
                              on_delete=models.CASCADE, related_name="buy_group")
    bank = models.ForeignKey("Bank", verbose_name="qase",
                             on_delete=models.CASCADE, related_name="buy_bank")
    date = models.DateField(
        verbose_name="barwar", auto_now_add=True, blank=True)
    datetime = models.DateTimeField(
        verbose_name="rekwt", auto_now_add=True, blank=True)


class paysalary(models.Model):
    group = models.ForeignKey("Group", verbose_name="naw group",
                              on_delete=models.CASCADE, related_name="salary_group")
    bank = models.ForeignKey("Bank", verbose_name="qase",
                             on_delete=models.CASCADE, related_name="salary_bank")
    employee = models.ForeignKey("Epmploye", verbose_name="krekar",
                                 on_delete=models.CASCADE, related_name="salary_employee")
    date = models.DateField(
        verbose_name="barwar", auto_now_add=True, blank=True)
    datetime = models.DateTimeField(
        verbose_name="rekwt", auto_now_add=True, blank=True)


class Bank(models.Model):
    group = models.ForeignKey("Group", verbose_name="naw group",
                              on_delete=models.CASCADE, related_name="bank_group")
    income = models.DecimalField(
        verbose_name="hawto", max_digits=22, decimal_places=2)
    loan = models.DecimalField(
        verbose_name="decho", max_digits=22, decimal_places=2)
    date = models.DateField(
        verbose_name="barwar", auto_now_add=True, blank=True)
    datetime = models.DateTimeField(
        verbose_name="rekwt", auto_now_add=True, blank=True)


class ReSell(models.Model):
    sell = models.ForeignKey("Sell", verbose_name="wasl",
                             on_delete=models.CASCADE, related_name="ReSell_detail")
    item = models.ForeignKey("Item", verbose_name="naw kala",
                             on_delete=models.CASCADE, related_name="ReSell_item")
    quantity = models.IntegerField(verbose_name="dane")
    price = models.DecimalField(
        verbose_name="nrx", max_digits=22, decimal_places=2)
    date = models.DateField(verbose_name="barwar", auto_now_add=True)
    datetime = models.DateTimeField(
        verbose_name="rekwt", auto_now_add=True, blank=True)

    @property
    def total(self):
        return self.price * self.quantity

    def __str__(self):
        return

    def __unicode__(self):
        return
