from django.urls import path

from . import views

urlpatterns = [
    path('publish', views.getPublishOrder),
    path('index', views.queryAllOrders),
    path('takeOrder', views.takeOrder),
    path('detail', views.queryOrderDetail),
    path('delivery', views.taker_confirm),
    path('receipt', views.rel_receipt),
    path('cancel', views.rel_cancel),
]