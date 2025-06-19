from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Usuario, Movimiento
from decimal import Decimal
from .models import Usuario, Movimiento, SeguroContratado
from .models import Usuario, Movimiento, SeguroContratado, TipoSeguro
from django.utils.timezone import now
from datetime import timedelta
from .models import Movimiento
from django.db.models import Count
from .models import TipoSeguro, SeguroContratado
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os
from datetime import datetime
from django.http import FileResponse, HttpResponse
from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML




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


def grafica_movimientos(request):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return redirect("login")

    fecha_inicio = now() - timedelta(days=30)
    movimientos = Movimiento.objects.filter(usuario_id=usuario_id, fecha__gte=fecha_inicio)

    conteo = {"DEPOSITO": 0, "RETIRO": 0}
    for mov in movimientos:
        tipo = mov.tipo.upper()
        if tipo in conteo:
            conteo[tipo] += 1

    total = sum(conteo.values()) or 1
    porcentajes = {k: round((v / total) * 100, 1) for k, v in conteo.items()}

    context = {
        "labels": list(conteo.keys()),
        "valores": list(conteo.values()),
        "porcentajes": list(porcentajes.values())
    }

    return render(request, "grafica_movimientos.html", context)

def grafica_marketing(request):
    datos = (SeguroContratado.objects
             .values('tipo_seguro__nombre')
             .annotate(total=Count('id'))
             .order_by('-total'))

    labels = [d['tipo_seguro__nombre'] for d in datos]
    valores = [d['total'] for d in datos]
    total = sum(valores) or 1  # Evitar división por cero

    # Calcular porcentajes
    porcentajes = [(v / total) * 100 for v in valores]

    # Colores llamativos
    colores = ['#007bff', '#28a745', '#dc3545', '#ffc107', '#6f42c1']  # azul, verde, rojo, amarillo, morado

    # Crear gráfica
    plt.figure(figsize=(9, 5))
    bars = plt.bar(labels, porcentajes, color=colores[:len(labels)])
    plt.title('Seguros más Contratados')
    plt.ylabel('Porcentaje (%)')
    plt.ylim(0, 100)

    # Mostrar porcentaje arriba de cada barra
    for bar, pct in zip(bars, porcentajes):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, f'{pct:.1f}%', ha='center', fontsize=10)

    plt.tight_layout()

    # Convertir a imagen base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    imagen_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close()

    return render(request, 'grafica_marketing.html', {'grafica': imagen_base64})


def generar_pdf_estado_cuenta(usuario, mes, anio):
    carpeta_pdfs = os.path.join(settings.MEDIA_ROOT, 'estados_de_cuenta')
    os.makedirs(carpeta_pdfs, exist_ok=True)

    filename = f"estado_{usuario.username}_{mes}_{anio}.pdf"
    ruta_pdf = os.path.join(carpeta_pdfs, filename)

    if os.path.exists(ruta_pdf):
        return ruta_pdf  # Ya existe

    # Datos del usuario y movimientos
    movimientos = Movimiento.objects.filter(
        usuario=usuario,
        fecha__month=mes,
        fecha__year=anio
    ).order_by('-fecha')

    seguros = SeguroContratado.objects.filter(
        usuario=usuario,
        fecha_contratacion__month=mes,
        fecha_contratacion__year=anio
    )

    # Renderizar HTML con adornos
    html = render_to_string("estado_cuenta_pdf.html", {
        "usuario": usuario,
        "movimientos": movimientos,
        "seguros": seguros,
        "mes": mes,
        "anio": anio
    })

    # Crear el PDF con WeasyPrint
    with open(ruta_pdf, "wb") as f:
        HTML(string=html).write_pdf(f)

    return ruta_pdf

def estado_cuenta_pdf(request):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return redirect("login")

    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        return redirect("login")

    ahora = datetime.now()
    mes = ahora.month
    anio = ahora.year

    ruta_pdf = generar_pdf_estado_cuenta(usuario, mes, anio)
    if not os.path.exists(ruta_pdf):
        return HttpResponse("No se pudo generar el PDF", status=500)

    return FileResponse(open(ruta_pdf, "rb"), content_type='application/pdf')
