from django.urls import path
from .views import *
from rest_framework.authtoken import views
from django.conf.urls import *
from .views import custom_page_not_found, custom_server_error, custom_bad_request, custom_unauthorized, custom_permission_denied, custom_method_not_allowed, custom_not_acceptable, custom_proxy_authentication_required, custom_request_timeout, custom_conflict, custom_gone, custom_length_required, custom_precondition_failed, custom_payload_too_large, custom_uri_too_long, custom_unsupported_media_type, custom_range_not_satisfiable, custom_expectation_failed, custom_not_implemented, custom_bad_gateway, custom_service_unavailable, custom_gateway_timeout, custom_http_version_not_supported

handler400 = custom_bad_request
handler401 = custom_unauthorized
handler403 = custom_permission_denied
handler404 = custom_page_not_found
handler405 = custom_method_not_allowed
handler406 = custom_not_acceptable
handler407 = custom_proxy_authentication_required
handler408 = custom_request_timeout
handler409 = custom_conflict
handler410 = custom_gone
handler411 = custom_length_required
handler412 = custom_precondition_failed
handler413 = custom_payload_too_large
handler414 = custom_uri_too_long
handler415 = custom_unsupported_media_type
handler416 = custom_range_not_satisfiable
handler417 = custom_expectation_failed
handler500 = custom_server_error
handler501 = custom_not_implemented
handler502 = custom_bad_gateway
handler503 = custom_service_unavailable
handler504 = custom_gateway_timeout
handler505 = custom_http_version_not_supported

urlpatterns = [
    path('', login_view, name='login'),
    path('menu/', menu, name='menu'),
    path('bitacora_acceso/', bitacora_acceso_view, name='bitacora_acceso'),
    path('bitacora/', bitacora_view, name='bitacora_view'),
    path('bitacora_acceso_externo/', bitacora_acceso_externo, name='bitacora_acceso_externo'),
    path('bitacora_report/', bitacora_report, name='bitacora_report'),
    path('bitacoras/', BitacoraAccesoListCreate.as_view(), name='apilist'),
    path('bitacoras/<int:pk>/', BitacoraAccesoDetail.as_view(), name='apidetalle'),
    path('api-token-auth/', views.obtain_auth_token),

]
