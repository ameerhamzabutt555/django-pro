from django.shortcuts import render
import requests
from rest_framework import generics
from django.http import JsonResponse
from .serializers import ClientSerializer, VendorSerializer, StoreSerializer, SalariesSerializer, ExpensesSerializer
from .models import Client, Vendor, Store, Salaries, Expenses


def index(request):
    return render(request, 'myapp/index.html')

def client(request):
    api_url = 'http://127.0.0.1:8000/myapp/clients/'  # Replace with your API endpoint URL
    response = requests.get(api_url)

    if response.status_code == 200:
        clients_data = response.json()
        # Process the API data as needed
    else:
        error_message = 'API request failed'
        # Handle the error condition
    return render(request, 'myapp/client.html',{'clients': clients_data})


def expenes(request):
    api_url = 'http://127.0.0.1:8000/myapp/expeness/'  # Replace with your API endpoint URL
    response = requests.get(api_url)

    if response.status_code == 200:
        expenses_data = response.json()
        # Process the API data as needed
    else:
        error_message = 'API request failed'
        # Handle the error condition
    return render(request, 'myapp/expenses.html',{'expenses': expenses_data})

def salary(request):
    api_url = 'http://127.0.0.1:8000/myapp/salaries/'  # Replace with your API endpoint URL
    response = requests.get(api_url)

    if response.status_code == 200:
        salaries_data = response.json()
        # Process the API data as needed
    else:
        error_message = 'API request failed'
        # Handle the error condition
    return render(request, 'myapp/salaries.html',{'salaries': salaries_data})


def store(request):
    api_url = 'http://127.0.0.1:8000/myapp/stores/'  # Replace with your API endpoint URL
    response = requests.get(api_url)

    if response.status_code == 200:
        stores_data = response.json()
        # Process the API data as needed
    else:
        error_message = 'API request failed'
        # Handle the error condition
    return render(request, 'myapp/store.html',{'stores': stores_data})

def vendor(request):
    api_url = 'http://127.0.0.1:8000/myapp/vendors/'  # Replace with your API endpoint URL
    response = requests.get(api_url)

    if response.status_code == 200:
        vendor_data = response.json()
        # Process the API data as needed
    else:
        error_message = 'API request failed'
        # Handle the error condition
    return render(request, 'myapp/vendor.html',{'vendors': vendor_data})


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