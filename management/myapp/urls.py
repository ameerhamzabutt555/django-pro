from django.urls import path
from . import views
from .views import (
    ClientListAPIView,
    ExpenessListAPIView,
    StoresListAPIView,
    VendorsListAPIView,
)


urlpatterns = [
    path("", views.index, name="index"),
    path("client/", views.client, name="client"),
    path("expenes/", views.expenes, name="expenes"),
    path("store/", views.store, name="store"),
    path("vendor/", views.vendor, name="vendor"),
    path("clients/", ClientListAPIView.as_view(), name="client-list"),
    path("expeness/", ExpenessListAPIView.as_view(), name="expeness-list"),
    path("stores/", StoresListAPIView.as_view(), name="stores-list"),
    path("vendors/", VendorsListAPIView.as_view(), name="vendors-list"),
]
