from django.urls import path
from . import views
from .views import (
    ClientListAPIView,
    ExpenessListAPIView,
    VendorsListAPIView,
)


urlpatterns = [
    path("", views.index, name="index"),
    path("client/", views.client, name="client"),
    path("expenes/", views.expenes, name="expenes"),
    path("vendor/", views.vendor, name="vendor"),
    path("clients/", ClientListAPIView.as_view(), name="client-list"),
    path("expeness/", ExpenessListAPIView.as_view(), name="expeness-list"),
    path("vendors/", VendorsListAPIView.as_view(), name="vendors-list"),
]
