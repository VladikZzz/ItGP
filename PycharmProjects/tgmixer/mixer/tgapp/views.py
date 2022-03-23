from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from .models import User, Coin, Order, Ad, Trade, FakeAd
from rest_framework import status
from .serializer import UserListSerializer, CoinListSerializer, OrderListSerializer, AdListSerializer, \
    TradeListSerializer, FakeAdListSerializer
from rest_framework.response import Response


###############USER####################
@api_view(['GET', 'POST', 'DELETE'])
def user_list(request, format=None):
    if request.method == 'GET':
        tokens = User.objects.all()

        tokens_serializer = UserListSerializer(tokens, many=True)
        return JsonResponse(tokens_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        serializer = UserListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = User.objects.all().delete()
        return JsonResponse({'message': '{} Users were deleted successfully!'.format(count[0])},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk, format=None):
    try:
        token = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        token_serializer = UserListSerializer(token)
        return JsonResponse(token_serializer.data)

    elif request.method == 'PUT':
        token_data = JSONParser().parse(request)
        token_serializer = UserListSerializer(token, data=token_data)
        if token_serializer.is_valid():
            token_serializer.save()
            return Response(token_serializer.data)
        return Response(token_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        token.delete()
        return JsonResponse({'message': 'User was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


###############COIN####################
@api_view(['GET', 'POST', 'DELETE'])
def coin_list(request, format=None):
    if request.method == 'GET':
        coins = Coin.objects.all()

        coins_serializer = CoinListSerializer(coins, many=True)
        return JsonResponse(coins_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        serializer = CoinListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Coin.objects.all().delete()
        return JsonResponse({'message': '{} Coins were deleted successfully!'.format(count[0])},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def coin_detail(request, pk, format=None):
    try:
        coin = Coin.objects.get(pk=pk)
    except Coin.DoesNotExist:
        return JsonResponse({'message': 'The Coin does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        coin_serializer = CoinListSerializer(coin)
        return JsonResponse(coin_serializer.data)

    elif request.method == 'PUT':
        coin_data = JSONParser().parse(request)
        coin_serializer = CoinListSerializer(coin, data=coin_data)
        if coin_serializer.is_valid():
            coin_serializer.save()
            return Response(coin_serializer.data)
        return Response(coin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        coin.delete()
        return JsonResponse({'message': 'Coin was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


#############ORDER##############
@api_view(['GET', 'POST', 'DELETE'])
def order_list(request, format=None):
    if request.method == 'GET':
        orders = Order.objects.all()

        orders_serializer = OrderListSerializer(orders, many=True)
        return JsonResponse(orders_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        serializer = OrderListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Order.objects.all().delete()
        return JsonResponse({'message': '{} Orders were deleted successfully!'.format(count[0])},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def order_detail(request, pk, format=None):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return JsonResponse({'message': 'The Coin does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        order_serializer = OrderListSerializer(order)
        return JsonResponse(order_serializer.data)

    elif request.method == 'PUT':
        order_data = JSONParser().parse(request)
        order_serializer = OrderListSerializer(order, data=order_data)
        if order_serializer.is_valid():
            order_serializer.save()
            return Response(order_serializer.data)
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        order.delete()
        return JsonResponse({'message': 'Order was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


#############AD##############
@api_view(['GET', 'POST', 'DELETE'])
def ad_list(request, format=None):
    if request.method == 'GET':
        ads = Ad.objects.all()

        ads_serializer = AdListSerializer(ads, many=True)
        return JsonResponse(ads_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        serializer = AdListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Ad.objects.all().delete()
        return JsonResponse({'message': '{} Ads were deleted successfully!'.format(count[0])},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def ad_detail(request, pk, format=None):
    try:
        ad = Ad.objects.get(pk=pk)
    except Ad.DoesNotExist:
        return JsonResponse({'message': 'The Ad does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        ad_serializer = AdListSerializer(ad)
        return JsonResponse(ad_serializer.data)

    elif request.method == 'PUT':
        ad_data = JSONParser().parse(request)
        ad_serializer = AdListSerializer(ad, data=ad_data)
        if ad_serializer.is_valid():
            ad_serializer.save()
            return Response(ad_serializer.data)
        return Response(ad_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ad.delete()
        return JsonResponse({'message': 'Ad was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


############trade###########
@api_view(['GET', 'POST', 'DELETE'])
def trade_list(request, format=None):
    if request.method == 'GET':
        trades = Trade.objects.all()

        trades_serializer = TradeListSerializer(trades, many=True)
        return JsonResponse(trades_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        serializer = TradeListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Trade.objects.all().delete()
        return JsonResponse({'message': '{} Trades were deleted successfully!'.format(count[0])},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def trade_detail(request, pk, format=None):
    try:
        trade = Trade.objects.get(pk=pk)
    except Trade.DoesNotExist:
        return JsonResponse({'message': 'The Trade does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        trade_serializer = TradeListSerializer(trade)
        return JsonResponse(trade_serializer.data)

    elif request.method == 'PUT':
        trade_data = JSONParser().parse(request)
        trade_serializer = TradeListSerializer(trade, data=trade_data)
        if trade_serializer.is_valid():
            trade_serializer.save()
            return Response(trade_serializer.data)
        return Response(trade_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        trade.delete()
        return JsonResponse({'message': 'Trade was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


##########fakeAd#################

@api_view(['GET', 'POST', 'DELETE'])
def fake_list(request, format=None):
    if request.method == 'GET':
        fake = FakeAd.objects.all()

        trades_serializer = FakeAdListSerializer(fake, many=True)
        return JsonResponse(trades_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        serializer = FakeAdListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = FakeAd.objects.all().delete()
        return JsonResponse({'message': '{} FakeAds were deleted successfully!'.format(count[0])},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def fake_detail(request, pk, format=None):
    try:
        trade = FakeAd.objects.get(pk=pk)
    except FakeAd.DoesNotExist:
        return JsonResponse({'message': 'The FakeAd does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        trade_serializer = FakeAdListSerializer(trade)
        return JsonResponse(trade_serializer.data)

    elif request.method == 'PUT':
        trade_data = JSONParser().parse(request)
        trade_serializer = FakeAdListSerializer(trade, data=trade_data)
        if trade_serializer.is_valid():
            trade_serializer.save()
            return Response(trade_serializer.data)
        return Response(trade_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        trade.delete()
        return JsonResponse({'message': 'FakeAd was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
