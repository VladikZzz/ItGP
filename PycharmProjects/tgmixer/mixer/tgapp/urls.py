from django.urls import path, include
from . import views

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('user/', views.user_list),
    path('user/<str:pk>/', views.user_detail),
    path('coin/', views.coin_list),
    path('coin/<str:pk>/', views.coin_detail),
    path('order/', views.order_list),
    path('order/<str:pk>/', views.order_detail),
    path('ad/', views.ad_list),
    path('ad/<str:pk>/', views.ad_detail),
    path('trade/', views.trade_list),
    path('trade/<str:pk>/', views.trade_detail),
    path('fake/', views.fake_list),
    path('fake/<str:pk>/', views.fake_detail),
]