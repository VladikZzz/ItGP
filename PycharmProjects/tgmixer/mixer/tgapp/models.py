from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    tg_id = models.CharField(max_length=10000, default=None, blank=True, primary_key=True)
    limit = models.IntegerField()
    current_limit = models.IntegerField()
    role = models.CharField(max_length=100)

    USDT_balance = models.FloatField(blank=True, default=0, null=True)
    TRX_balance = models.FloatField(blank=True, default=0, null=True)
    XLM_balance = models.FloatField(blank=True, default=0, null=True)
    ADA_balance = models.FloatField(blank=True, default=0, null=True)
    DOGE_balance = models.FloatField(blank=True, default=0, null=True)
    MATIC_balance = models.FloatField(blank=True, default=0, null=True)
    LUNA_balance = models.FloatField(blank=True, default=0, null=True)
    DOT_balance = models.FloatField(blank=True, default=0, null=True)
    AVAX_balance = models.FloatField(blank=True, default=0, null=True)

    address_USDT = models.CharField(blank=True, null=True, max_length=2000)
    address_TRX = models.CharField(blank=True, null=True, max_length=2000)
    address_XLM = models.CharField(blank=True, null=True, max_length=2000)
    address_ADA = models.CharField(blank=True, null=True, max_length=2000)
    address_DOGE = models.CharField(blank=True, null=True, max_length=2000)
    address_MATIC = models.CharField(blank=True, null=True, max_length=2000)
    address_LUNA = models.CharField(blank=True, null=True, max_length=2000)
    address_DOT = models.CharField(blank=True, null=True, max_length=2000)
    address_AVAX = models.CharField(blank=True, null=True, max_length=2000)

    trade_amount = models.FloatField(blank=True, null=True, default=0)
    trade_count = models.IntegerField(blank=True, null=True, default=0)
    reg_date = models.DateField(blank=True)
    state = models.CharField(max_length=10000, null=True)

    def __str__(self):
        return self.tg_id


class Coin(models.Model):
    tiker = models.CharField(max_length=100, primary_key=True)
    network_type = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)

    def __str__(self):
        return self.tiker


class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=1000)
    owner_id = models.IntegerField()
    amount = models.FloatField()
    cryptocurrency = models.CharField(max_length=100)
    from_adr = models.CharField(max_length=2000)
    to_adr = models.CharField(max_length=2000)
    type = models.CharField(max_length=1000)
    link = models.CharField(max_length=10000, null=True, blank=True)
    flag = models.CharField(max_length=10000, null=True, blank=True)

    def __str__(self):
        return self.id


class Ad(models.Model):
    id = models.IntegerField(primary_key=True)
    owner_id = models.IntegerField()
    min_amount = models.FloatField()
    max_amount = models.FloatField()
    state = models.BooleanField()
    description = models.CharField(max_length=1000000, null=True)

    def __str__(self):
        return self.id


class Trade(models.Model):
    id = models.IntegerField(primary_key=True)
    to_id = models.IntegerField()
    state = models.CharField(max_length=1000)
    usdt_amount = models.FloatField()
    coin_amount = models.FloatField()
    coin = models.CharField(max_length=20000, null=True, blank=True)

    def __str__(self):
        return self.id


class FakeAd(models.Model):
    id = models.IntegerField(primary_key=True)
    owner_name = models.CharField(max_length=10000)
    trade_number = models.IntegerField()
    trade_amount = models.FloatField()
    reg_date = models.DateField()
    min_amount = models.FloatField()
    max_amount = models.FloatField()
    des = models.CharField(max_length=1000000)

    def __str__(self):
        return self.id