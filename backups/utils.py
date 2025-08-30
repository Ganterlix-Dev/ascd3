import os
from django.conf import settings

def get_pg_connection():
    """
    Retorna la URL de la base de datos y el entorno con PGPASSWORD
    para ejecutar pg_dump/pg_restore sin exponer la contraseña.
    """
    cfg = settings.DATABASES['default']

    # Construir DSN sin contraseña
    user     = cfg.get('USER', '')
    host     = cfg.get('HOST', 'localhost')
    port     = cfg.get('PORT', '')
    name     = cfg.get('NAME', '')
    db_url   = f"postgresql://{user}@{host}:{port}/{name}"

    # Clonar el entorno y añadir la contraseña
    env = os.environ.copy()
    password = cfg.get('PASSWORD')
    if password:
        env['PGPASSWORD'] = password

    return db_url, env
