from django.urls import path

from . import views

urlpatterns = [
    path('publish', views.get_publish_order),
    path('index', views.query_all_orders),
    path('takeOrder', views.take_order),
    path('detail', views.query_order_detail),
    path('delivery', views.taker_confirm),
    path('token', views.get_token),
    path('setPhoto', views.set_confirm_photo),
    path('receipt', views.rel_receipt),
    path('cancel', views.rel_cancel),
    path('evaluate_positive', views.rel_evaluate_positive),
    path('evaluate_negative', views.rel_evaluate_negative),
    path('my/index', views.query_my_all_orders),
    path('my/take', views.query_my_take),
    path('my/send', views.query_my_send),
    path('my/receive', views.query_my_receive),
    path('my/finish', views.query_my_finish),
    path('my/count', views.query_my_order_count),
    path('my/publish', views.query_my_publish),
]