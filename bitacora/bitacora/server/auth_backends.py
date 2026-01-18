import logging
from ldap3 import Server, Connection, NTLM
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

logger = logging.getLogger(__name__)

# Lista de usuarios permitidos (todos en minúsculas para facilitar la comparación)
USUARIOS_PERMITIDOS = ['acanales', 'ksepulveda', 'nvera']

def authenticate_ldap(username, password):
    # Convertir el nombre de usuario ingresado a minúsculas para la comparación
    username = username.lower()

    # Verificar si el usuario está en la lista de permitidos
    if username not in USUARIOS_PERMITIDOS:
        logger.warning(f"El usuario {username} no está autorizado para ingresar.")
        return False
    
    # Primer servidor LDAP
    ldap_server_uri = 'ldap://dc2.corralport.com:389'
    server = Server(ldap_server_uri, get_info='ALL')
    user_dn = f'PCSA\\{username}'
    conn = Connection(server, user=user_dn, password=password, authentication=NTLM)
    
    if conn.bind():
        logger.info(f"Autenticación exitosa con LDAP en {ldap_server_uri}")
        return True
    else:
        logger.warning(f"Fallo en la autenticación con el servidor LDAP {ldap_server_uri}")
    
    # Segundo servidor LDAP
    ldap_server_uri = 'ldap://spr.reloncavi.cl.:389'
    server = Server(ldap_server_uri, get_info='ALL')
    user_dn = f'RELONCAVI_SPR\\{username}'
    conn = Connection(server, user=user_dn, password=password, authentication=NTLM)
    
    if conn.bind():
        logger.info(f"Autenticación exitosa con LDAP en {ldap_server_uri}")
        return True
    else:
        logger.warning(f"Fallo en la autenticación con el servidor LDAP {ldap_server_uri}")
        return False

class LDAPBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if authenticate_ldap(username, password):
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_user(username=username, password=password)
            return user
        return None
