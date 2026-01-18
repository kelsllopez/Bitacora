from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages  # Importa el módulo de mensajes
from django.utils import timezone
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .auth_backends import LDAPBackend
import subprocess
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls import handler404
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from datetime import datetime
from django.shortcuts import render
from django.utils.dateparse import parse_date
from bitacora.email_utils import send_mail_async  # 👈 Importamos la función

def bitacora_acceso_view(request):
    if request.method == "POST":
        form = BitacoraAccesoForm(request.POST)
        
        if form.is_valid():
            acceso = form.save()  # Guardar en DB
            send_mail_async(acceso, form.cleaned_data)  # Enviar correo en segundo plano
            messages.success(request, 'se envio correctamente el formulario')

            return redirect('menu')

        messages.error(request, 'Hubo un error al guardar la bitácora de acceso.')
    
    else:
        form = BitacoraAccesoForm()

    return render(request, 'bitacora_acceso/registrar_acceso.html', {'form': form})


def bitacora_acceso_externo(request):
    if request.method == "POST":
        form = BitacoraAccesoExternaForm(request.POST)
        
        if form.is_valid():
            bitacora = form.save(commit=False)  # No guarda aún en la base de datos
            bitacora.externo = True  # Asigna el valor a la instancia del modelo
            bitacora.save()  # Ahora sí guarda en la base de datos 
            send_mail_async(bitacora, form.cleaned_data)  # Enviar correo en segundo plano
            messages.success(request, 'se envio correctamente el formulario')

            return redirect('menu')

        messages.error(request, 'Hubo un error al guardar la bitácora de acceso.')
    
    else:
        form = BitacoraAccesoExternaForm()

    return render(request, 'bitacora_acceso/registrar_externos.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['usuario']
            password = form.cleaned_data['password']
            backend = LDAPBackend()
            user = backend.authenticate(request, username=username, password=password)

            if user:
                user.backend = 'server.auth_backends.LDAPBackend'
                login(request, user)

                return redirect('menu')  
            else:
                messages.error(request, 'No tiene los permisos para ingresar.')
        else:
            messages.error(request, 'Por favor, rellene todos los campos correctamente.')
    else:
        form = LoginForm()

    return render(request, 'bitacora_acceso/login.html', {'form': form})

@login_required
def menu(request):
        # Pasar el nombre del usuario al contexto si está autenticado
    context = {
        'usuario': request.user.username if request.user.is_authenticated else 'Invitado',
    }
    return render(request, 'bitacora_acceso/menu.html')


class BitacoraAccesoListCreate(generics.ListCreateAPIView):

    queryset = BitacoraAcceso.objects.all()

    serializer_class = BitacoraAccesoSerializer

    permission_classes = [AllowAny] 


class BitacoraAccesoDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = BitacoraAcceso.objects.all()

    serializer_class = BitacoraAccesoSerializer

    permission_classes = [AllowAny] 




@login_required
def bitacora_view(request):
    if request.method == 'GET' and 'search' in request.GET:
        query = request.GET.get('search', '').strip().lower()

        if not query:
            return JsonResponse({'message': 'Consulta vacía. Escribe algo para buscar.', 'results': []})

        url = 'https://talana.com/es/api/persona/'
        headers = {'Authorization': 'Token f309959cca22818d59f1931ba705fcb353024326'}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
        except ValueError:
            return JsonResponse({'message': 'Error al decodificar los datos de la API.', 'results': []})
        except requests.exceptions.RequestException as e:
            return JsonResponse({'message': f'Error al obtener datos de la API: {str(e)}', 'results': []})

        nombres = [
            {
                'nombre': f"{p.get('nombre', '')} {p.get('apellidoPaterno', '')} {p.get('apellidoMaterno', '')}",
                'rut': p.get('rut', ''),
                'apellido_paterno': p.get('apellidoPaterno', ''),
                'apellido_materno': p.get('apellidoMaterno', '')
            }
            for p in data
            if query in f"{p.get('nombre', '')} {p.get('apellidoPaterno', '')} {p.get('apellidoMaterno', '')}".lower()
        ]

        if not nombres:
            return JsonResponse({'message': 'No se encontraron resultados.', 'results': []})

        return JsonResponse({'results': nombres})

    return JsonResponse({'message': 'No se recibió consulta de búsqueda.', 'results': []})

from datetime import datetime
from django.shortcuts import render
from django.utils.dateparse import parse_date

@login_required
def bitacora_report(request):
    # Obtener todas las bitácoras (internos y externos)
    bitacora_acceso = BitacoraAcceso.objects.all()

    # Obtener todas las ubicaciones y responsables para los filtros
    ubicaciones = Ubicacion.objects.all()
    responsables = Responsable.objects.all()

    # Filtros desde GET
    fecha_filter = request.GET.get('fecha', '').strip()
    ubicacion_filter = request.GET.get('ubicacion', '').strip()
    responsable_filter = request.GET.get('responsable', '').strip()
    tipo_filter = request.GET.get('filter-tipo', '').strip()  # Filtro de tipo

    # Aplicar filtros
    if fecha_filter:
        fecha_filtrada = parse_date(fecha_filter)
        if fecha_filtrada:
            bitacora_acceso = bitacora_acceso.filter(fecha=fecha_filtrada)

    if ubicacion_filter:
        bitacora_acceso = bitacora_acceso.filter(ubicacion__id=ubicacion_filter)

    if responsable_filter:
        bitacora_acceso = bitacora_acceso.filter(responsable__id=responsable_filter)

    if tipo_filter:
        if tipo_filter == 'interno':  
            bitacora_acceso = bitacora_acceso.filter(externo=False)
        elif tipo_filter == 'externo':  
            bitacora_acceso = bitacora_acceso.filter(externo=True)

    # Contadores
    total_internos = bitacora_acceso.filter(externo=False).count()
    total_externos = bitacora_acceso.filter(externo=True).count()
    total_general = total_internos + total_externos

    # Renderizar la vista con los datos filtrados y los contadores
    return render(request, 'bitacora_acceso/bitacora_report.html', {
        'bitacora_acceso': bitacora_acceso,
        'ubicaciones': ubicaciones,
        'responsables': responsables,
        'fecha': fecha_filter,
        'ubicacion': ubicacion_filter,
        'responsable': responsable_filter,
        'tipo': tipo_filter,
        'total_internos': total_internos,
        'total_externos': total_externos,
        'total_general': total_general,
    })

# Vista personalizada para el error 404
def custom_page_not_found(request, exception):
    return render(request, 'error/404.html', status=404)

# Vista personalizada para el error 500
def custom_server_error(request):
    return render(request, 'error/500.html', status=500)

# Vista personalizada para el error 400 (Bad Request)
def custom_bad_request(request, exception):
    return render(request, 'error/400.html', status=400)

# Vista personalizada para el error 401 (Unauthorized)
def custom_unauthorized(request, exception):
    return render(request, 'error/401.html', status=401)

# Vista personalizada para el error 403 (Forbidden)
def custom_permission_denied(request, exception):
    return render(request, 'error/403.html', status=403)


# Vista personalizada para el error 405 (Method Not Allowed)
def custom_method_not_allowed(request, exception):
    return render(request, 'error/405.html', status=405)

# Vista personalizada para el error 406 (Not Acceptable)
def custom_not_acceptable(request, exception):
    return render(request, 'error/406.html', status=406)

# Vista personalizada para el error 407 (Proxy Authentication Required)
def custom_proxy_authentication_required(request, exception):
    return render(request, 'error/407.html', status=407)

# Vista personalizada para el error 408 (Request Timeout)
def custom_request_timeout(request, exception):
    return render(request, 'error/408.html', status=408)

# Vista personalizada para el error 409 (Conflict)
def custom_conflict(request, exception):
    return render(request, 'error/409.html', status=409)

# Vista personalizada para el error 410 (Gone)
def custom_gone(request, exception):
    return render(request, 'error/410.html', status=410)

# Vista personalizada para el error 411 (Length Required)
def custom_length_required(request, exception):
    return render(request, 'error/411.html', status=411)

# Vista personalizada para el error 412 (Precondition Failed)
def custom_precondition_failed(request, exception):
    return render(request, 'error/412.html', status=412)

# Vista personalizada para el error 413 (Payload Too Large)
def custom_payload_too_large(request, exception):
    return render(request, 'error/413.html', status=413)

# Vista personalizada para el error 414 (URI Too Long)
def custom_uri_too_long(request, exception):
    return render(request, 'error/414.html', status=414)

# Vista personalizada para el error 415 (Unsupported Media Type)
def custom_unsupported_media_type(request, exception):
    return render(request, 'error/415.html', status=415)

# Vista personalizada para el error 416 (Range Not Satisfiable)
def custom_range_not_satisfiable(request, exception):
    return render(request, 'error/416.html', status=416)

# Vista personalizada para el error 417 (Expectation Failed)
def custom_expectation_failed(request, exception):
    return render(request, 'error/417.html', status=417)

# Vista personalizada para el error 501 (Not Implemented)
def custom_not_implemented(request):
    return render(request, 'error/501.html', status=501)

# Vista personalizada para el error 502 (Bad Gateway)
def custom_bad_gateway(request):
    return render(request, 'error/502.html', status=502)

# Vista personalizada para el error 503 (Service Unavailable)
def custom_service_unavailable(request):
    return render(request, 'error/503.html', status=503)

# Vista personalizada para el error 504 (Gateway Timeout)
def custom_gateway_timeout(request):
    return render(request, 'error/504.html', status=504)

# Vista personalizada para el error 505 (HTTP Version Not Supported)
def custom_http_version_not_supported(request, exception):
    return render(request, 'error/505.html', status=505)