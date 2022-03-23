from .models import User, Coin, Order, Ad, Trade, FakeAd
from rest_framework import serializers


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'token', 'tg_id', 'limit', 'current_limit', 'role', 'USDT_balance', 'TRX_balance', 'XLM_balance',
                  'ADA_balance','DOGE_balance','MATIC_balance','LUNA_balance','DOT_balance','AVAX_balance',
                  'address_USDT', 'address_TRX','address_XLM', 'address_ADA', 'address_DOGE', 'address_MATIC',
                  'address_LUNA', 'address_DOT', 'address_AVAX', 'trade_amount', 'trade_count', 'reg_date', 'state')

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.token = validated_data.get('token', instance.token)
        instance.tg_id = validated_data.get('tg_id', instance.tg_id)
        instance.limit = validated_data.get('limit', instance.limit)
        instance.current_limit = validated_data.get('current_limit', instance.current_limit)
        instance.role = validated_data.get('role', instance.role)

        instance.USDT_balance = validated_data.get('USDT_balance', instance.USDT_balance)
        instance.TRX_balance = validated_data.get('TRX_balance', instance.TRX_balance)
        instance.XLM_balance = validated_data.get('XLM_balance', instance.XLM_balance)
        instance.ADA_balance = validated_data.get('ADA_balance', instance.ADA_balance)
        instance.DOGE_balance = validated_data.get('DOGE_balance', instance.DOGE_balance)
        instance.MATIC_balance = validated_data.get('MATIC_balance', instance.MATIC_balance)
        instance.LUNA_balance = validated_data.get('LUNA_balance', instance.LUNA_balance)
        instance.DOT_balance = validated_data.get('DOT_balance', instance.DOT_balance)
        instance.AVAX_balance = validated_data.get('AVAX_balance', instance.AVAX_balance)

        instance.address_USDT = validated_data.get('address_USDT', instance.address_USDT)
        instance.address_TRX = validated_data.get('address_TRX', instance.address_TRX)
        instance.address_XLM = validated_data.get('address_XLM', instance.address_XLM)
        instance.address_ADA = validated_data.get('address_ADA', instance.address_ADA)
        instance.address_DOGE = validated_data.get('address_DOGE', instance.address_DOGE)
        instance.address_MATIC = validated_data.get('address_MATIC', instance.address_MATIC)
        instance.address_LUNA = validated_data.get('address_LUNA', instance.address_LUNA)
        instance.address_DOT = validated_data.get('address_DOT', instance.address_DOT)
        instance.address_AVAX = validated_data.get('address_AVAX', instance.address_AVAX)

        instance.trade_amount = validated_data.get('trade_amount', instance.trade_amount)
        instance.trade_count = validated_data.get('trade_count', instance.trade_count)
        instance.reg_date = validated_data.get('reg_date', instance.reg_date)
        instance.state = validated_data.get('state', instance.state)


        instance.save()
        return instance


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'status', 'owner_id', 'amount', 'cryptocurrency', 'from_adr', 'to_adr', 'type', 'link', 'flag')

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.owner_id = validated_data.get('owner_id', instance.owner_id)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.cryptocurrency = validated_data.get('cryptocurrency', instance.cryptocurrency)
        instance.from_adr = validated_data.get('from_adr', instance.from_adr)
        instance.to_adr = validated_data.get('to_adr', instance.to_adr)
        instance.type = validated_data.get('type', instance.type)
        instance.link = validated_data.get('link', instance.link)
        instance.flag = validated_data.get('flag', instance.flag)

        instance.save()
        return instance


class CoinListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ('tiker', 'network_type', 'address')

    def update(self, instance, validated_data):
        instance.tiker = validated_data.get('tiker', instance.tiker)
        instance.network_type = validated_data.get('network_type', instance.network_type)
        instance.address = validated_data.get('address', instance.address)

        instance.save()
        return instance


class AdListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ('id', 'owner_id', 'min_amount', 'max_amount', 'state', 'description')

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.owner_id = validated_data.get('owner_id', instance.owner_id)
        instance.min_amount = validated_data.get('min_amount', instance.min_amount)
        instance.max_amount = validated_data.get('max_amount', instance.max_amount)
        instance.state = validated_data.get('state', instance.state)
        instance.description = validated_data.get('description', instance.description)

        instance.save()
        return instance


class TradeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ('id', 'to_id', 'state', 'usdt_amount', 'coin_amount', 'coin')

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.to_id = validated_data.get('to_id', instance.to_id)
        instance.state = validated_data.get('state', instance.state)
        instance.usdt_amount = validated_data.get('usdt_amount', instance.usdt_amount)
        instance.coin_amount = validated_data.get('coin_amount', instance.coin_amount)
        instance.coin = validated_data.get('coin', instance.coin)

        instance.save()
        return instance


class FakeAdListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FakeAd
        fields = ('id', 'owner_name', 'trade_number', 'trade_amount', 'reg_date', 'min_amount', 'max_amount', 'des')

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.owner_name = validated_data.get('owner_name', instance.owner_name)
        instance.trade_number = validated_data.get('trade_number', instance.trade_number)
        instance.trade_amount = validated_data.get('trade_amount', instance.trade_amount)
        instance.reg_date = validated_data.get('reg_date', instance.reg_date)
        instance.min_amount = validated_data.get('min_amount', instance.min_amount)
        instance.max_amount = validated_data.get('max_amount', instance.max_amount)
        instance.des = validated_data.get('des', instance.des)

        instance.save()
        return instance