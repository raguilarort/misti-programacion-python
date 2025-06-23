from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Usuario, Movimiento
from decimal import Decimal
from .models import Usuario, Movimiento, SeguroContratado
from .models import Usuario, Movimiento, SeguroContratado, TipoSeguro
from datetime import datetime
import os
from django.http import FileResponse, HttpResponse
from django.conf import settings
from django.template.loader import render_to_string
#Para graficar con Chart.js
from datetime import timedelta
from django.utils.timezone import now
from .models import Movimiento
#Para graficar con Matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from .models import TipoSeguro, SeguroContratado
from django.db.models import Count
#Para generacion de archivos
import pdfkit

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
            usuario = Usuario.objects.get(username=username)#se busca en la bd el usuario
            if usuario.check_password(password):#se verifica si la contraseña ingresada, después de aplicar el mismo algoritmo de hash (PBKDF2 por defecto en Django) coincide con el hash almacenado del usuario
                request.session["usuario_id"] = usuario.id#si la contraseña es válida, guarda el id del usuario en la sesión del navegador
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

# GRAFICAS
def grafica_movimientos(request):
    usuario_id = request.session.get("usuario_id")#se obtiene el id del usuario que ha iniciado sesión 
    if not usuario_id:
        return redirect("login")#si no hay sesion activa redirige a la pagina para iniciar sesion

    fecha_inicio = now() - timedelta(days=30)
    movimientos = Movimiento.objects.filter(usuario_id=usuario_id, fecha__gte=fecha_inicio)#se consultan todos los movimientos del usuario realizados en los últimos 30 días

    conteo = {"DEPOSITO": 0, "RETIRO": 0}#se inicializa un diccionario para contar cuántos depósitos y retiros hay
    for mov in movimientos:#en donde el for recorrera los movimientos e ira sumando 1 segun corresponda
        tipo = mov.tipo.upper()
        if tipo in conteo:
            conteo[tipo] += 1

    total = sum(conteo.values()) or 1#Se suma la cantidad total de movimientos para luego calcular porcentajes, si es 0, se evita división por cero usando 1
    porcentajes = {k: round((v / total) * 100, 1) for k, v in conteo.items()}
    
#se preparan los datos que se enviarán al template
    context = {
        "labels": list(conteo.keys()),
        "valores": list(conteo.values()),
        "porcentajes": list(porcentajes.values())
    }

    return render(request, "grafica_movimientos.html", context)#se renderiza la plantilla grafica_movimientos.html pasando los datos para que se usen en la gráfica con Chart.js

def grafica_marketing(request):
    datos = (SeguroContratado.objects#se realiza una consulta a la base de datos para ver cuántas veces ha sido contratado cada uno y se ordena de mayor a menor
             .values('tipo_seguro__nombre')
             .annotate(total=Count('id'))
             .order_by('-total'))

    labels = [d['tipo_seguro__nombre'] for d in datos]#se extraen las etiquetas (nombres de seguros) y los valores (cantidad contratados) desde los datos obtenidos
    valores = [d['total'] for d in datos]
    total = sum(valores) or 1  #se calcula la suma total de seguros contratados y se calculan porcentajes

    
    porcentajes = [(v / total) * 100 for v in valores]

    # se define paleta de colores
    colores = ['#007bff', '#28a745', '#dc3545', '#ffc107', '#6f42c1']  # azul, verde, rojo, amarillo, morado

    # procedimiento para crear gráfica por matplotlib
    plt.figure(figsize=(9, 5))#se crea figura de 9x5 pulgadas
    bars = plt.bar(labels, porcentajes, color=colores[:len(labels)])#se dibuja grafica de barras con etiquetas en ejes
    plt.title('Seguros más Contratados')
    plt.ylabel('Porcentaje (%)')
    plt.ylim(0, 100)

    #se coloca etiqueta de porcentaje arriba de cada barra
    for bar, pct in zip(bars, porcentajes):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, f'{pct:.1f}%', ha='center', fontsize=10)

    plt.tight_layout()#se ajusta el diseño

    #se guarda la imagen generada en formato png
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    imagen_base64 = base64.b64encode(buffer.read()).decode('utf-8')#se convierte la imagen a una cadena base 64 para poder insertarla en el html sin necesidad de guardar como archivo
    buffer.close()
    plt.close()

    return render(request, 'grafica_marketing.html', {'grafica': imagen_base64})#se renderiza la plantilla HTML y se inserta la imagen


def estado_cuenta_pdf(request):
    usuario_id = request.session.get("usuario_id")# se recupera el id del usuario desde la sesión
    if not usuario_id:
        return redirect("login")

    usuario = Usuario.objects.get(id=usuario_id)#se obtiene el usuario que coincide con el id 

    #se obtienen todos los movimientos del usuario, ordenándolos del más reciente al más antiguo
    movimientos_qs = Movimiento.objects.filter(usuario=usuario).order_by('-fecha')
    #se crea una lista de diccionarios con los datos dde cada movimiento 
    movimientos = [{
        "fecha": mov.fecha.strftime("%d/%m/%Y"),
        "descripcion": mov.tipo.capitalize(),
        "monto": f"${mov.cantidad:.2f}",
        "canal": "App"
    } for mov in movimientos_qs]

    #se obtiennen todos los seguros contratados por el usuario
    seguros_qs = SeguroContratado.objects.filter(usuario=usuario)
    #se genera una lista de diccionarios con la info de cada seguro contratado
    seguros = [{
        "nombre": s.tipo_seguro.nombre,
        "precio": f"${s.tipo_seguro.precio:.2f}"
    } for s in seguros_qs]
    total_mensual = sum(s.tipo_seguro.precio for s in seguros_qs)#se calcula el total mensual a pagar de los seguros

    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")#se obtiene la fecha para colocarla
#se usa la plantilla para inyectar datos
    html = render_to_string("estado_cuenta_pdf.html", {
        "usuario": usuario,
        "movimientos": movimientos,
        "seguros": seguros,
        "total_mensual": f"${total_mensual:.2f}",
        "fecha_actual": fecha_actual,
    })

    config = pdfkit.configuration(
        wkhtmltopdf=r'C:\Users\ENRIQUE OJEDA\wkhtmltopdf\bin\wkhtmltopdf.exe'#se configura PDFKit especificando la ruta donde está instalado wkhtmltopdf porque es necesario para generar el PDF
    )
    pdf = pdfkit.from_string(html, False, configuration=config)#se convierte el html a pdf

    response = HttpResponse(pdf, content_type="application/pdf")#se crea una respuesta HTTP que devuelve el PDF para que se abra directamente en el navegador para no forzar descargar
    response["Content-Disposition"] = "inline; filename='estado_cuenta.pdf'"
    return response