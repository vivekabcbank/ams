from django.http import HttpResponse
from django.shortcuts import render

def Index(request):
    return HttpResponse("<h1>Welcome to the AMS index page!</h1>")

def custom_404(request, exception):
    return HttpResponse("<h1>Requested page not found</h1>")
    # return render(request, '404.html', status=404)