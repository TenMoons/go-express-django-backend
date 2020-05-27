from django.urls import path

from . import views

urlpatterns = [
    path('wxLogin', views.get_openid),
]