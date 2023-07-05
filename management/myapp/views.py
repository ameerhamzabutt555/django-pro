from django.shortcuts import render
import requests
from rest_framework import generics
from django.http import JsonResponse
from .serializers import ClientSerializer, VendorSerializer, StoreSerializer, SalariesSerializer, ExpensesSerializer
from .models import Client, Vendor, Store, Salaries, Expenses

def index(request):
    api_url = 'http://127.0.0.1:8000/myapp/clients/'  # Replace with your API endpoint URL
    response = requests.get(api_url)

    if response.status_code == 200:
        clients_data = response.json()
        # Process the API data as needed
    else:
        error_message = 'API request failed'
        # Handle the error condition
    return render(request, 'myapp/index.html',{'clients': clients_data})



class ClientListAPIView(generics.ListAPIView):
    queryset = Client.objects.all() 
    serializer_class = ClientSerializer

class ExpenessListAPIView(generics.ListAPIView):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer

class SalariesListAPIView(generics.ListAPIView):
    queryset = Salaries.objects.all()
    serializer_class = SalariesSerializer

class StoresListAPIView(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

class VendorsListAPIView(generics.ListAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer