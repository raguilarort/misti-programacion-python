from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def hello(request):
    #return HttpResponse("<h1>Hello World!</h1>")
    return render(request, "index.html")

def login(request):
    return render(request, "login.html")

def dashboard(request):
    return render(request, "dashboard.html")

def about(request):
    return HttpResponse("About")



