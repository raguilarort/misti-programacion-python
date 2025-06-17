from django.shortcuts import render
from django.http import HttpResponse
from .models import SeguroAuto
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from collections import defaultdict

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


@login_required
def grafica_seguros_usuario(request):
    hoy = now().date()
    hace_7_dias = hoy - timedelta(days=6)

    seguros = SeguroAuto.objects.filter(usuario=request.user, fecha_contratacion__range=[hace_7_dias, hoy])

    datos = defaultdict(int)
    for s in seguros:
        datos[s.fecha_contratacion.strftime("%Y-%m-%d")] += 1

    # Completar días sin registros
    dias = [(hace_7_dias + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    valores = [datos[dia] for dia in dias]

    context = {
        "labels": dias,
        "valores": valores
    }
    return render(request, "grafica_usuario.html", context)
