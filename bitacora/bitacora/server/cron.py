from django.core.management import call_command

def my_backup():
    """Función para realizar un backup de la base de datos."""
    try:
        call_command('dbbackup')
        print("Backup realizado con éxito.")
    except Exception as e:
        print(f"Ocurrió un error al realizar el backup: {e}")
