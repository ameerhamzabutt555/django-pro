from django.shortcuts import redirect

from django.urls import reverse



def index(request):
    # return redirect('admin:view_on_site')
    # print("reverse___", reverse("admin"))
    response = redirect('admin:index')
    return response