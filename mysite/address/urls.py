from django.urls import path

from . import views

urlpatterns = [
    path('index', views.showAddress),
    path('delete', views.deleteAddress),
    path('add', views.addAddress),
]