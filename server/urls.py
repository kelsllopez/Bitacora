from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('menu/', views.menu_view, name='menu'),
    path('bitacora-interna/', views.bitacora_interna_view, name='bitacora_interna'),
    path('bitacora-externa/', views.bitacora_externa_view, name='bitacora_externa'),
    path('admin-panel/', views.admin_panel_view, name='admin_panel'),
    path('admin-panel/ajax/', views.bitacoras_ajax, name='bitacoras_ajax'),

    path('api/bitacora/<str:tipo>/<int:id>/eliminar/', 
         views.api_eliminar_bitacora, 
         name='api_eliminar_bitacora'),
    
    path('api/bitacora/<str:tipo>/<int:id>/editar/', 
         views.api_editar_bitacora, 
         name='api_editar_bitacora'),
    
    path('api/bitacora/<str:tipo>/<int:id>/', 
         views.api_detalle_bitacora, 
         name='api_detalle_bitacora'),

]