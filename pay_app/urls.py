from django.urls import path
from . import views

urlpatterns = [
    path('go-to-gateway', views.go_to_gateway),
    path('verify', views.verify),
]
