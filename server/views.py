from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import BitacoraInterna, BitacoraExterna
from .forms import BitacoraInternaForm, BitacoraExternaForm
from django.db.models import Q, Count
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.utils import timezone
import json


try:
    import openpyxl
    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
    from openpyxl.utils import get_column_letter
except ImportError:
    openpyxl = None

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4, landscape
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas
except ImportError:
    pass

def login_view(request):
    if request.user.is_authenticated:
        return redirect('menu')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('menu')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def menu_view(request):
    return render(request, 'menu.html')

@login_required
def bitacora_interna_view(request):
    if request.method == 'POST':
        form = BitacoraInternaForm(request.POST)
        if form.is_valid():
            bitacora = form.save(commit=False)
            bitacora.creado_por = request.user
            bitacora.save()
            messages.success(request, 'Bitácora interna registrada exitosamente')
            return redirect('bitacora_interna')
    else:
        form = BitacoraInternaForm()
    
    bitacoras = BitacoraInterna.objects.all().order_by('-fecha', '-hora_entrada')[:10]
    return render(request, 'bitacora_interna.html', {
        'form': form, 
        'bitacoras': bitacoras
    })

@login_required
def bitacora_externa_view(request):
    if request.method == 'POST':
        form = BitacoraExternaForm(request.POST)
        if form.is_valid():
            bitacora = form.save(commit=False)
            bitacora.creado_por = request.user
            bitacora.save()
            messages.success(request, 'Bitácora externa registrada exitosamente')
            return redirect('bitacora_externa')
    else:
        form = BitacoraExternaForm()
    
    bitacoras = BitacoraExterna.objects.all().order_by('-fecha', '-hora_entrada')[:10]
    return render(request, 'bitacora_externas.html', {
        'form': form, 
        'bitacoras': bitacoras
    })

@login_required
def api_detalle_bitacora(request, tipo, id):
    """API para obtener los detalles de una bitácora específica"""
    try:
        if tipo == 'interna':
            bitacora = get_object_or_404(BitacoraInterna, id=id)
            data = {
                'id': bitacora.id,
                'tipo': 'interna',
                'fecha': bitacora.fecha.strftime('%d/%m/%Y'),
                'hora_entrada': bitacora.hora_entrada.strftime('%H:%M'),
                'hora_salida': bitacora.hora_salida.strftime('%H:%M') if bitacora.hora_salida else None,
                'nombre_visitante': bitacora.nombre_visitante,
                'apellido_paterno': bitacora.apellido_paterno,
                'apellido_materno': bitacora.apellido_materno,
                'rut': bitacora.rut,
                'modo_visita': bitacora.modo_visita or '', 
                'ticket': bitacora.ticket or '',
                'responsable': bitacora.responsable,
                'responsable_display': bitacora.get_responsable_display(),
                'ubicacion': bitacora.ubicacion,
                'ubicacion_display': bitacora.get_ubicacion_display(),
                'observaciones': bitacora.observaciones or '',
            }
        else:
            bitacora = get_object_or_404(BitacoraExterna, id=id)
            data = {
                'id': bitacora.id,
                'tipo': 'externa',
                'fecha': bitacora.fecha.strftime('%d/%m/%Y'),
                'hora_entrada': bitacora.hora_entrada.strftime('%H:%M'),
                'hora_salida': bitacora.hora_salida.strftime('%H:%M') if bitacora.hora_salida else None,
                'nombre_visitante': bitacora.nombre_visitante,
                'modo_visita': bitacora.modo_visita or '', 
                'ticket': bitacora.ticket or '',
                'responsable': bitacora.responsable,
                'responsable_display': bitacora.get_responsable_display(),
                'ubicacion': bitacora.ubicacion,
                'ubicacion_display': bitacora.get_ubicacion_display(),
                'observaciones': bitacora.observaciones or '',
            }
        
        return JsonResponse(data)
    
    except Exception as e:
        import traceback
        print(f"Error en api_detalle_bitacora: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@require_POST
def api_editar_bitacora(request, tipo, id):
    try:
        data = json.loads(request.body)
        
        if tipo == 'interna':
            bitacora = get_object_or_404(BitacoraInterna, id=id)
            bitacora.apellido_paterno = data.get('apellido_paterno', '')
            bitacora.apellido_materno = data.get('apellido_materno', '')
            bitacora.rut = data.get('rut', '')
        else:
            bitacora = get_object_or_404(BitacoraExterna, id=id)
        
        bitacora.fecha = data.get('fecha')
        bitacora.hora_entrada = data.get('hora_entrada')
        bitacora.hora_salida = data.get('hora_salida') or None
        bitacora.modo_visita = data.get('modo_visita', '')
        bitacora.nombre_visitante = data.get('nombre_visitante')
        bitacora.ticket = data.get('ticket', '')
        bitacora.responsable = data.get('responsable')
        bitacora.ubicacion = data.get('ubicacion')
        bitacora.observaciones = data.get('observaciones', '')
        
        bitacora.save()
        
        return JsonResponse({
            'success': True, 
            'message': f'Bitácora {tipo} actualizada correctamente'
        })
    
    except Exception as e:
        import traceback
        print(f"Error en api_editar_bitacora: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required
@require_POST
def api_eliminar_bitacora(request, tipo, id):
    """API para eliminar una bitácora específica"""
    try:
        if tipo == 'interna':
            bitacora = get_object_or_404(BitacoraInterna, id=id)
        else:
            bitacora = get_object_or_404(BitacoraExterna, id=id)
        
        bitacora.delete()
        return JsonResponse({'success': True, 'message': 'Bitácora eliminada correctamente'})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required
def admin_panel_view(request):
    context = {
        'opciones_ubicacion': BitacoraInterna.UBICACION_CHOICES,
        'opciones_responsable': BitacoraInterna.RESPONSABLE__BITACORA,
    }
    return render(request, 'admin_panel.html', context)




@login_required
def bitacoras_ajax(request):
    f_fecha = request.GET.get('fecha')
    f_ubicacion = request.GET.get('ubicacion')
    f_responsable = request.GET.get('responsable')
    f_tipo = request.GET.get('tipo')

    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))

    qs_interna = BitacoraInterna.objects.all()
    qs_externa = BitacoraExterna.objects.all()

    if f_fecha:
        qs_interna = qs_interna.filter(fecha=f_fecha)
        qs_externa = qs_externa.filter(fecha=f_fecha)
    if f_ubicacion:
        qs_interna = qs_interna.filter(ubicacion=f_ubicacion)
        qs_externa = qs_externa.filter(ubicacion=f_ubicacion)
    if f_responsable:
        qs_interna = qs_interna.filter(responsable=f_responsable)
        qs_externa = qs_externa.filter(responsable=f_responsable)

    if f_tipo == 'interno':
        qs_externa = BitacoraExterna.objects.none()
    elif f_tipo == 'externo':
        qs_interna = BitacoraInterna.objects.none()

    total_internos = qs_interna.count()
    total_externos = qs_externa.count()
    total_general = total_internos + total_externos

    datos_combinados = []

    for b in qs_interna.order_by('-fecha', '-hora_entrada'):
        datos_combinados.append({
            'id': b.id,
            'externo': False,
            'fecha': b.fecha.strftime("%d/%m/%Y"),
            'hora_entrada': b.hora_entrada.strftime("%H:%M"),
            'hora_salida': b.hora_salida.strftime("%H:%M") if b.hora_salida else "--",
            'nombre_visitante': f"{b.nombre_visitante} {b.apellido_paterno}".strip(),
            'responsable': b.get_responsable_display(),
            'ubicacion': b.get_ubicacion_display(),
            'motivo_visita': b.modo_visita,
            'observaciones': getattr(b, 'observaciones', ''),
        })

    for b in qs_externa.order_by('-fecha', '-hora_entrada'):
        datos_combinados.append({
            'id': b.id,
            'externo': True,
            'fecha': b.fecha.strftime("%d/%m/%Y"),
            'hora_entrada': b.hora_entrada.strftime("%H:%M"),
            'hora_salida': b.hora_salida.strftime("%H:%M") if b.hora_salida else "--",
            'nombre_visitante': b.nombre_visitante,
            'responsable': b.get_responsable_display(),
            'ubicacion': b.get_ubicacion_display(),
            'motivo_visita': b.modo_visita,
            'observaciones': b.observaciones,
        })

    datos_paginados = datos_combinados[start:start+length]

    return JsonResponse({
        "draw": int(request.GET.get("draw", 1)),
        "recordsTotal": total_general,
        "recordsFiltered": total_general,
        "data": datos_paginados,
        "totales": {
            "internos": total_internos,
            "externos": total_externos,
            "general": total_general
        }
    })


@login_required
def eliminar_interna(request, id):
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para eliminar registros')
        return redirect('menu')
    
    bitacora = get_object_or_404(BitacoraInterna, id=id)
    bitacora.delete()
    messages.success(request, 'Registro eliminado exitosamente')
    return redirect('admin_panel')

@login_required
def eliminar_externa(request, id):
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para eliminar registros')
        return redirect('menu')
    
    bitacora = get_object_or_404(BitacoraExterna, id=id)
    bitacora.delete()
    messages.success(request, 'Registro eliminado exitosamente')
    return redirect('admin_panel')