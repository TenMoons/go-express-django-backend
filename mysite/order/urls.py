from django.urls import path

from . import views

urlpatterns = [
    path('publish', views.getPublishOrder),
    path('index', views.queryAllOrders)
]