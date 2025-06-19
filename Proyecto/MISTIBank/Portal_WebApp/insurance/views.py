from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Usuario, Movimiento
from decimal import Decimal
from .models import Usuario, Movimiento, SeguroContratado
from .models import Usuario, Movimiento, SeguroContratado, TipoSeguro


# VISTA INICIAL
def hello(request):
    return render(request, "index.html")

# LOGIN 
def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            usuario = Usuario.objects.get(username=username)
            if usuario.check_password(password):
                request.session["usuario_id"] = usuario.id
                return redirect("dashboard")
            else:
                error = "Contraseña incorrecta"
        except Usuario.DoesNotExist:
            error = "Usuario no encontrado"

    return render(request, "login_custom.html", {"error": error})

# DASHBOARD
def dashboard(request):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return redirect("login")

    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        return redirect("login")

    return render(request, "dashboard.html", {"usuario": usuario})

# CERRAR SESIÓN
def logout_view(request):
    request.session.flush()
    return redirect("login")

# DEPOSITAR
def depositar(request):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return redirect("login")
    
    usuario = Usuario.objects.get(id=usuario_id)

    if request.method == 'POST':
        monto = Decimal(request.POST['monto'])
        usuario.saldo += monto
        usuario.save()
        Movimiento.objects.create(usuario=usuario, tipo='DEPOSITO', cantidad=monto)
        return redirect("dashboard")

    return render(request, "depositar.html")

# RETIRAR
def retirar(request):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return redirect("login")
    
    usuario = Usuario.objects.get(id=usuario_id)

    if request.method == 'POST':
        monto = Decimal(request.POST['monto'])

        if monto <= usuario.saldo:
            usuario.saldo -= monto
            usuario.save()
            Movimiento.objects.create(usuario=usuario, tipo='RETIRO', cantidad=monto)
            return redirect("dashboard")
        else:
            return render(request, "retirar.html", {"error": "Saldo insuficiente"})

    return render(request, "retirar.html")

# VISTA DE ABOUT (estática)
def about(request):
    return HttpResponse("About")


# SEGUROS CONTRATADOS
def seguros_contratados(request):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return redirect("login")

    usuario = Usuario.objects.get(id=usuario_id)
    contratos = SeguroContratado.objects.filter(usuario=usuario)
    tipos_contratados = contratos.values_list('tipo_seguro__id', flat=True)
    seguros_disponibles = TipoSeguro.objects.all()
    total_mensual = sum([s.tipo_seguro.precio for s in contratos])

    return render(request, "seguros_contratados.html", {
        "contratos": contratos,
        "seguros_disponibles": seguros_disponibles,
        "tipos_contratados": tipos_contratados,
        "total_mensual": total_mensual,
    })


def contratar_seguro(request, tipo_id):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return redirect("login")

    usuario = Usuario.objects.get(id=usuario_id)
    tipo = TipoSeguro.objects.get(id=tipo_id)

    # Evitar duplicados
    if not SeguroContratado.objects.filter(usuario=usuario, tipo_seguro=tipo).exists():
        SeguroContratado.objects.create(usuario=usuario, tipo_seguro=tipo)

    return redirect("seguros_contratados")